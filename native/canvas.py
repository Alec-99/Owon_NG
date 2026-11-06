from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt, Signal

class ScopeCanvas(QWidget):
 cursorsChanged = Signal()
 def __init__(self, capture):
  super().__init__()
  self.capture=capture;self.visible=[True,True];self.scales=[2.,2.];self.offsets=[0.,0.]
  self.time_div=.01;self.pan=0.;self.cursors=[.3,.7];self.drag=None
  self.setMinimumSize(320,280)
  self.setAccessibleName("Oscilloscoop met twee gesimuleerde kanalen")
  self.setFocusPolicy(Qt.StrongFocus)
  self.setToolTip("Sleep cursors A/B. Gebruik links/rechts om cursor A te verplaatsen; Shift voor cursor B. Muiswiel zoomt.")
 def duration(self):return (len(self.capture.channels[0])-1)/self.capture.rate
 def span(self):return min(self.duration(),self.time_div*10)
 def start(self):return self.pan*max(0,self.duration()-self.span())
 def sample(self,channel,x):
  i=round((self.start()+x*self.span())*self.capture.rate)
  return self.capture.channels[channel][max(0,min(i,len(self.capture.channels[channel])-1))]
 def paintEvent(self,event):
  p=QPainter(self);p.fillRect(self.rect(),QColor("#0a121a"));p.setRenderHint(QPainter.Antialiasing)
  w,h=self.width(),self.height()
  p.setPen(QPen(QColor("#263845"),1))
  for i in range(11):p.drawLine(round(w*i/10),0,round(w*i/10),h)
  for i in range(9):p.drawLine(0,round(h*i/8),w,round(h*i/8))
  for channel,color in enumerate(("#f2c26b","#74dca6")):
   if not self.visible[channel]:continue
   path=QPainterPath()
   for x in range(w):
    v=self.sample(channel,x/max(1,w-1))
    y=h/2-(v+self.offsets[channel])/self.scales[channel]*h/8
    if x==0:path.moveTo(x,y)
    else:path.lineTo(x,y)
   p.setPen(QPen(QColor(color),1.5));p.drawPath(path)
  p.setPen(QPen(QColor("#85d8e1"),1,Qt.DashLine))
  for i,r in enumerate(self.cursors):
   x=round(r*w);p.drawLine(x,0,x,h);p.drawText(x+6,30+i*20,"AB"[i])
  p.setPen(QColor("#b7cbd7"));p.drawText(12,h-12,f"{self.span()*1000/10:.3g} ms/div · CH1 {self.scales[0]:g} V/div · CH2 {self.scales[1]:g} V/div")
 def mousePressEvent(self,e):
  x=e.position().x()/self.width();self.drag=min(range(2),key=lambda i:abs(self.cursors[i]-x));self.move_cursor(x)
 def mouseMoveEvent(self,e):
  if self.drag is not None:self.move_cursor(e.position().x()/self.width())
 def mouseReleaseEvent(self,e):self.drag=None
 def move_cursor(self,x):
  self.cursors[self.drag]=max(0,min(1,x));self.update();self.cursorsChanged.emit()
 def keyPressEvent(self,e):
  if e.key() in (Qt.Key_Left,Qt.Key_Right):
   self.drag=1 if e.modifiers()&Qt.ShiftModifier else 0
   self.move_cursor(self.cursors[self.drag]+(.01 if e.key()==Qt.Key_Right else -.01));self.drag=None
  else:super().keyPressEvent(e)
 def wheelEvent(self,e):
  self.time_div=max(.00005,min(self.duration()/10,self.time_div*(.8 if e.angleDelta().y()>0 else 1.25)));self.update();self.cursorsChanged.emit()
