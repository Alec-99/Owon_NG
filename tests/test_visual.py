"""Contrast regression with a deliberately dark inherited system palette."""
import unittest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor,QPalette
from PySide6.QtWidgets import QApplication
from native.app import ScopeWindow

def luminance(color):
    values=[color.redF(),color.greenF(),color.blueF()]
    values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(a*b for a,b in zip(values,(.2126,.7152,.0722)))

def contrast(a,b):
    high,low=sorted((luminance(a),luminance(b)),reverse=True)
    return (high+.05)/(low+.05)

class VisualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])
    def setUp(self):
        dark=QPalette()
        for role in (QPalette.Base,QPalette.Button,QPalette.Window):
            dark.setColor(role,QColor("#252525"))
        for role in (QPalette.Text,QPalette.ButtonText,QPalette.WindowText):
            dark.setColor(role,QColor("#eeeeee"))
        self.app.setPalette(dark)
        self.app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
        self.w=ScopeWindow();self.w.timer.stop();self.w.show();self.app.processEvents()
    def tearDown(self):
        self.w.close()
    def test_active_inputs_remain_light_and_readable(self):
        for widget in (self.w.profile,self.w.time,self.w.channel_scales[0],self.w.channel_offsets[0]):
            image=widget.grab().toImage()
            scale=image.devicePixelRatio()
            surface=image.pixelColor(round(max(4,widget.width()-35)*scale),round((widget.height()-6)*scale))
            text=widget.palette().color(QPalette.Text)
            self.assertGreater(luminance(surface),.7,type(widget).__name__)
            self.assertGreaterEqual(contrast(text,surface),4.5,type(widget).__name__)
        self.assertNotEqual(self.app.styleHints().colorScheme(),Qt.ColorScheme.Dark)
        # Offscreen Qt reports Unknown; rendered input contrast is checked above.
    def test_run_analyse_and_import_states_explain_available_actions(self):
        self.assertEqual(self.w.acquisition_state.text(),"Simulatie loopt")
        self.assertEqual(self.w.run.text(),"Pauzeer")
        self.w.toggle_run()
        self.assertEqual(self.w.run.text(),"Start simulatie")
        self.assertEqual(self.w.acquisition_state.text(),"Gepauzeerd")
        self.w.profile.setCurrentText("UART 8N1")
        self.assertEqual(self.w.decoder.currentText(),"UART 8N1")
        self.assertTrue(self.w.baud.isVisible())
        self.w.analyse()
        self.assertIn("Analyse gereed",self.w.flow_hint.text())
        self.assertNotIn("000000",self.w.time.text())
        self.w.profile.setCurrentText("PWM")
        self.assertFalse(self.w.baud.isVisible())
        self.assertFalse(self.w.radix.isVisible())
    def test_dropdown_arrows_are_present_and_compact_size_is_honored(self):
        self.w.resize(1040,760);self.app.processEvents()
        self.assertEqual((self.w.width(),self.w.height()),(1040,760))
        for widget in (self.w.profile,self.w.channel_scales[0]):
            image=widget.grab().toImage()
            dark_pixels=sum(luminance(image.pixelColor(x,y))<.35
                for x in range(round((widget.width()-17)*image.devicePixelRatio()),round((widget.width()-6)*image.devicePixelRatio()))
                for y in range(round((widget.height()/2-4)*image.devicePixelRatio()),round((widget.height()/2+4)*image.devicePixelRatio())))
            self.assertGreaterEqual(dark_pixels,4,"Dropdown affordance missing")
