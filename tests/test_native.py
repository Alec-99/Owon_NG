import tempfile,pathlib,unittest
from PySide6.QtWidgets import QApplication
from native.app import ScopeWindow,STYLE
from native.model import fixture,load
class NativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.app=QApplication.instance() or QApplication([]);cls.app.setStyleSheet(STYLE)
 def setUp(self):self.w=ScopeWindow();self.w.timer.stop()
 def tearDown(self):self.w.close()
 def test_native_interactions(self):
  self.w.nav.setCurrentRow(1);self.assertEqual(self.w.profile.currentText(),'PWM')
  self.w.time.setValue(2);self.assertEqual(self.w.canvas.time_div,.002)
  self.w.canvas.drag=0;self.w.canvas.move_cursor(.2);self.assertEqual(self.w.canvas.cursors[0],.2)
  self.w.single();self.assertFalse(self.w.running)
  for i in range(8):self.w.nav.setCurrentRow(i)
 def test_fixture_and_recording(self):
  a=fixture('PWM');self.assertEqual(a.channels,fixture('PWM').channels)
  with tempfile.TemporaryDirectory() as tmp:
   p=pathlib.Path(tmp)/'a.json';a.save(p,'Notitie');b,note=load(p)
   self.assertEqual(a.channels,b.channels);self.assertEqual(b.source,'import');self.assertEqual(note,'Notitie')
   p.write_text('{"schema":42}');self.assertRaises(ValueError,load,p)
 def test_sample_decoders(self):
  from native.analysis import pwm,uart,i2c
  c=fixture("PWM");r=pwm(c.channels[0],c.rate)
  self.assertAlmostEqual(r["frequency_hz"],100);self.assertLess(abs(r["duty_percent"]-42),1)
  c=fixture("UART 8N1");data,errors=uart(c.channels[0],c.rate)
  self.assertEqual([x[1] for x in data[:4]],[0x55,0xA5,0x55,0xA5]);self.assertEqual(errors,0)
  self.assertRaises(ValueError,uart,c.channels[0],100,9600)
  c=fixture("I²C");data,starts=i2c(*c.channels,c.rate)
  self.assertGreater(starts,0);self.assertEqual([(x[1],x[2]) for x in data[:2]],[(0xA0,True),(0x55,True)])
  self.w.profile.setCurrentText("I²C");self.w.decoder.setCurrentText("I²C");self.w.analyse()
  self.assertIn("ACK",self.w.analysis_result.text())
