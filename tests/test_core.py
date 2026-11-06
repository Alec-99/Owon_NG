import dataclasses
import hashlib
import json
import math
import pathlib
import struct
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from native.capture import Capture, ChannelConfig, ViewState
from native.recording import load_recording, save_recording, encoded
from native.acquisition import Acquisition, SimulatedScope, Vds1022Adapter
from native.rendering import envelope

def wait_for(predicate, timeout=3):
    deadline = time.monotonic()+timeout
    while time.monotonic()<deadline:
        if predicate():
            return
        threading.Event().wait(.005)
    raise AssertionError("Timed out waiting for acquisition")

class RecordingTests(unittest.TestCase):
    def test_immutable_frame_defensively_copies_samples(self):
        values = [[0.0, -0.0, 1e-12], [1, 2, 3]]
        frame = Capture("fixture", 12345.6789, values)
        values[0][0] = 100
        self.assertEqual(frame.channels[0][0], 0.0)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            frame.rate = 99
        with self.assertRaises(TypeError):
            frame.channels[0][0] = 99

    def test_lossless_round_trip_timing_metadata_and_view(self):
        frame = Capture("fixture", 12345.6789,
                        ((-0.0, 1e-12, math.pi), (-1e-9, 2.0, 1.797e8)),
                        sample_start=12345678, frame_index=42,
                        channel_config=(ChannelConfig("CH1", probe_ratio=10, coupling="DC"),
                                        ChannelConfig("CH2", probe_ratio=1)))
        view = ViewState(.00123456789, .4321, (.2, 5), (-3, 10), (False, True), (.1,.9),"UART 8N1",115200)
        with tempfile.TemporaryDirectory() as folder:
            p = pathlib.Path(folder)/"frame.json"
            save_recording(p, frame, "µs\nvoorbeeld", view)
            loaded, note, restored = load_recording(p)
            self.assertEqual(loaded.source, "import")
            self.assertEqual(loaded.original, "simulation")
            self.assertEqual(dataclasses.replace(loaded, source="simulation"), frame)
            self.assertEqual(view, restored)
            self.assertEqual(note, "µs\nvoorbeeld")
            for a,b in zip(frame.channels[0],loaded.channels[0]):
                self.assertEqual(struct.pack("<d",a),struct.pack("<d",b))
            loaded.save(p,note,restored)
            twice,_,_ = load_recording(p)
            self.assertEqual(twice.original,"simulation")
            self.assertEqual(twice.capture_id,frame.capture_id)

    def test_integrity_and_schema_rejections(self):
        frame = Capture("PWM", 1000, ((0,1),(1,0)))
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/"frame.json"
            frame.save(p)
            doc=json.loads(p.read_bytes())
            doc["capture"]["channels"][0][0]=900
            p.write_text(json.dumps(doc))
            with self.assertRaisesRegex(ValueError,"Integriteitscontrole"):
                load_recording(p)
            doc["capture"]["rate"]=False
            body={k:v for k,v in doc.items() if k!="sha256"}
            doc["sha256"]=hashlib.sha256(encoded(body)).hexdigest()
            p.write_text(json.dumps(doc))
            with self.assertRaises(ValueError):load_recording(p)
            p.write_text('{"schema":2,"schema":1}')
            with self.assertRaises(ValueError):load_recording(p)
            p.write_text('{"schema":999}')
            with self.assertRaises(ValueError):load_recording(p)

    def test_failed_atomic_save_keeps_original_and_cleans_temporary(self):
        frame=Capture("PWM",1000,((0,1),(1,0)))
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/"frame.json";p.write_bytes(b"original")
            with patch("native.recording.os.replace",side_effect=OSError("disk failure")):
                with self.assertRaises(OSError):frame.save(p)
            self.assertEqual(p.read_bytes(),b"original")
            self.assertEqual(list(pathlib.Path(folder).iterdir()),[p])

    def test_legacy_migration_does_not_invent_acquisition_time(self):
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/"old.json"
            p.write_text(json.dumps(dict(schema=1,profile="PWM",rate=1000,channels=[[0,1],[1,0]],source="simulation",note="oud")))
            frame,note,view=load_recording(p)
            self.assertIsNone(frame.received_at_ns)
            self.assertEqual(frame.source,"import")
            self.assertEqual(frame.channel_config[0].probe_ratio,None)
            self.assertEqual(note,"oud")
            self.assertEqual(view,ViewState())

    def test_rejects_invalid_frame_and_view(self):
        for samples in (((0,float("nan")),(1,0)),((True,1),(1,0)),((1,),(1,)),((1,2),(1,2,3))):
            with self.assertRaises(ValueError):Capture("test",1000,samples)
        with self.assertRaises(ValueError):ViewState(scales=(True,2))
        with self.assertRaises(ValueError):ViewState(cursors=(-.1,.5))

class AcquisitionTests(unittest.TestCase):
    def test_simulator_sample_clock_continues_across_frames(self):
        adapter=SimulatedScope();adapter.connect();adapter.configure("PWM")
        first=adapter.read_frame();second=adapter.read_frame()
        self.assertEqual(second.sample_start,len(first.channels[0]))
        self.assertEqual(second.frame_index,1)
        self.assertEqual(second.stream_id,first.stream_id)
        self.assertEqual(first.sample_start,0)
        adapter.disconnect()
        with self.assertRaises(RuntimeError):adapter.read_frame()

    def test_bounded_buffer_pause_single_and_shutdown(self):
        controller=Acquisition(capacity=1,interval=.001)
        try:
            controller.configure("PWM")
            wait_for(lambda:controller.status().produced>=4)
            self.assertGreaterEqual(controller.status().overflow,3)
            controller.pause();wait_for(lambda:controller.status().state=="stopped")
            count=controller.status().produced
            self.assertIsNone(controller.latest())
            controller.single();wait_for(lambda:controller.status().produced==count+1)
            frame=controller.latest()
            self.assertEqual(frame.profile,"PWM")
            self.assertEqual(controller.status().state,"stopped")
            controller.resume();wait_for(lambda:controller.status().produced>count+1)
        finally:
            self.assertTrue(controller.close())

    def test_inflight_previous_profile_is_not_published(self):
        entered=threading.Event();release=threading.Event()
        class Blocking(SimulatedScope):
            def read_frame(self, timeout=0.25):
                entered.set()
                if not release.wait(2):raise TimeoutError("test read timed out")
                return super().read_frame()
        controller=Acquisition(Blocking(),interval=.001)
        try:
            controller.configure("PWM");self.assertTrue(entered.wait(2))
            controller.configure("Sinus",running=False);release.set()
            wait_for(lambda:controller.status().state=="stopped")
            self.assertIsNone(controller.latest())
            controller.single();wait_for(lambda:controller.status().produced==1)
            self.assertEqual(controller.latest().profile,"Sinus")
        finally:
            release.set();self.assertTrue(controller.close())

    def test_adapter_errors_are_visible_and_recoverable(self):
        class Failing(SimulatedScope):
            broken=True
            def read_frame(self, timeout=0.25):
                if self.broken:raise OSError("simulated disconnect")
                return super().read_frame()
        adapter=Failing();controller=Acquisition(adapter)
        try:
            controller.configure("PWM");wait_for(lambda:controller.status().state=="error")
            self.assertIn("simulated disconnect",controller.status().error)
            adapter.broken=False;controller.configure("PWM");wait_for(lambda:controller.status().produced>0)
            self.assertIsNone(controller.status().error)
        finally:self.assertTrue(controller.close())
        with self.assertRaises(RuntimeError):controller.resume()

    def test_hardware_boundary_never_claims_to_connect(self):
        controller=Acquisition(Vds1022Adapter())
        try:
            controller.configure("PWM");wait_for(lambda:controller.status().state=="error")
            self.assertIn("niet geïmplementeerd",controller.status().error)
            self.assertIsNone(controller.latest())
        finally:self.assertTrue(controller.close())

class RenderingTests(unittest.TestCase):
    def test_single_sample_spikes_survive_zoom_out(self):
        samples=[0.0]*10000;samples[1234]=42;samples[9998]=-39
        original=list(samples)
        result=envelope(samples,0,len(samples),200)
        self.assertEqual(max(v[1] for v in result),42)
        self.assertEqual(min(v[0] for v in result),-39)
        self.assertEqual(samples,original)
        clipped=envelope(samples,2000,9000,100)
        self.assertTrue(all(lo==hi==0 for lo,hi in clipped))
