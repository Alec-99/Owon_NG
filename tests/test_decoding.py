import unittest
from native.decoding import decode_capture,DecodeEvent
from native.capture import Capture
from native.model import fixture

class DecoderEventTests(unittest.TestCase):
    def test_uart_sample_spans_formats_and_truncation(self):
        c=fixture("UART 8N1")
        result=decode_capture(c,"UART 8N1")
        self.assertEqual(result.capture_id,c.capture_id)
        values=[e for e in result.events if e.kind=="data"]
        self.assertEqual([e.value for e in values[:4]],[0x55,0xA5,0x55,0xA5])
        self.assertEqual(values[0].start,42)
        self.assertGreater(values[0].stop,values[0].start)
        for e in result.events:
            self.assertTrue(0<=e.start<e.stop<=len(c.channels[0]))
        self.assertEqual(values[0].label("Hex"),"0x55")
        self.assertEqual(values[0].label("ASCII"),"U")
        self.assertEqual(values[0].label("Bin"),"01010101")
        self.assertEqual(DecodeEvent(0,1,"data",10).label("ASCII"),"\\x0A")
    def test_i2c_address_ack_and_incomplete_end(self):
        c=fixture("I²C");result=decode_capture(c,"I²C")
        data=[e for e in result.events if e.value is not None]
        self.assertEqual(data[0].kind,"address")
        self.assertEqual(data[0].label(),"Adr 0x50 W · ACK")
        self.assertEqual(data[1].label(),"0x55 · ACK")
        self.assertEqual(len(data),8)
        self.assertEqual(sum(e.kind=="incomplete" for e in result.events),1)
        self.assertTrue(any(e.kind=="stop" for e in result.events))
    def test_uart_framing_error_is_not_valid_data(self):
        samples=[5.0]*20+[0.0]*100+[5.0]*20
        c=Capture("test",96000,(samples,[0.0]*len(samples)))
        r=decode_capture(c,"UART 8N1")
        self.assertTrue(any(e.kind=="framing" for e in r.events))
        self.assertFalse(any(e.kind=="data" for e in r.events))
    def test_pwm_intervals_bound_full_cycles(self):
        c=fixture("PWM");r=decode_capture(c,"PWM")
        for a,b in zip(r.events,r.events[1:]):
            self.assertEqual(a.stop,b.start)
            self.assertIn("%",a.label())
        self.assertIn("100",r.description)
