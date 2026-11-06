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
