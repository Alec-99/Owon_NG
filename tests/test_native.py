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
 def test_cursor_plot_coordinates_and_decoder_controls(self):
  from PySide6.QtTest import QTest
  from PySide6.QtCore import Qt,QPoint
  self.w.resize(1040,760);self.w.show();self.app.processEvents()
  canvas=self.w.canvas;rect=canvas.plot_rect()
  point=QPoint(round(rect.left()+rect.width()*.6),round(rect.center().y()))
  QTest.mousePress(canvas,Qt.LeftButton,pos=point);QTest.mouseRelease(canvas,Qt.LeftButton,pos=point)
  self.assertAlmostEqual(canvas.cursors[1],.6,delta=.01)
  self.assertFalse(self.w.baud.isEnabled())
  self.w.decoder.setCurrentText("UART 8N1");self.assertTrue(self.w.baud.isEnabled())
  self.w.modes.setCurrentIndex(1);self.assertEqual(self.w.profile.currentText(),"PWM")
 def test_saved_view_restores_and_import_cannot_be_overwritten_by_worker(self):
  from native.capture import ViewState
  from PySide6.QtTest import QTest
  view=ViewState(.00123456789,.12345,(.2,5),(1,-2),(False,True),(.2,.8),"UART 8N1",115200)
  self.w.profile.setCurrentText("PWM")
  saved=self.w.capture
  with tempfile.TemporaryDirectory() as folder:
   path=pathlib.Path(folder)/"frame.json";saved.save(path,"herstel",view)
   self.w.read_capture(str(path))
   QTest.qWait(80);self.w.frame()
   self.assertEqual(self.w.capture.capture_id,saved.capture_id)
   self.assertEqual(self.w.capture.source,"import")
   self.assertEqual(self.w.view_state(),view)
   self.assertFalse(self.w.channel_checks[0].isChecked())
   self.assertEqual(self.w.channel_scales[1].currentText(),"5")
   self.assertEqual(self.w.note.toPlainText(),"herstel")
