import math
from native.rendering import envelope
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt, Signal, QRectF

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
 def plot_rect(self):
  return QRectF(52,28,max(1,self.width()-72),max(1,self.height()-64))
 def cursor_x(self,position):
  r=self.plot_rect();return (position.x()-r.left())/r.width()
 def paintEvent(self,event):
  p=QPainter(self);p.fillRect(self.rect(),QColor("#151b20"));p.setRenderHint(QPainter.Antialiasing)
  r=self.plot_rect()
  p.fillRect(r,QColor("#10161b"))
  for i in range(51):
   x=r.left()+r.width()*i/50
   p.setPen(QPen(QColor("#303a42" if i%5==0 else "#202a31"),1,Qt.SolidLine if i%5==0 else Qt.DotLine))
   p.drawLine(int(x),int(r.top()),int(x),int(r.bottom()))
  for i in range(41):
   y=r.top()+r.height()*i/40
   p.setPen(QPen(QColor("#303a42" if i%5==0 else "#202a31"),1,Qt.SolidLine if i%5==0 else Qt.DotLine))
   p.drawLine(int(r.left()),int(y),int(r.right()),int(y))
  p.setPen(QColor("#9baab5"))
  for i in range(11):
   value=(self.start()+self.span()*i/10)*1000
   p.drawText(QRectF(r.left()+r.width()*i/10-30,r.bottom()+5,60,20),Qt.AlignCenter,f"{value:.3g}")
  for i in range(9):
   value=(4-i)*self.scales[0]-self.offsets[0]
   p.drawText(QRectF(0,r.top()+r.height()*i/8-9,44,18),Qt.AlignRight|Qt.AlignVCenter,f"{value:g}")
  p.drawText(int(r.right()-12),self.height()-4,"ms")
  p.drawText(8,18,"V")
  for channel,color in enumerate(("#f0c34d","#43b5e2")):
   p.setPen(QColor(color));p.drawText(int(r.left()+channel*220),18,f"CH{channel+1}  {self.scales[channel]:g} V/div"+("" if self.visible[channel] else "  uit"))
   if not self.visible[channel]:continue
   p.save();p.setClipRect(r);path=QPainterPath()
   first=max(0,math.floor(self.start()*self.capture.rate))
   stop=min(len(self.capture.channels[channel]),math.ceil((self.start()+self.span())*self.capture.rate)+1)
   pixels=max(1,int(r.width()))
   if stop-first>pixels:
    p.setPen(QPen(QColor(color),1))
    for x,(low,high) in enumerate(envelope(self.capture.channels[channel],first,stop,pixels)):
     y1=r.center().y()-(high+self.offsets[channel])/self.scales[channel]*r.height()/8
     y2=r.center().y()-(low+self.offsets[channel])/self.scales[channel]*r.height()/8
     p.drawLine(int(r.left()+x),round(y1),int(r.left()+x),round(y2))
   else:
    for x in range(pixels+1):
     v=self.sample(channel,x/r.width())
     y=r.center().y()-(v+self.offsets[channel])/self.scales[channel]*r.height()/8
     if x==0:path.moveTo(r.left()+x,y)
     else:path.lineTo(r.left()+x,y)
    p.setPen(QPen(QColor(color),1.35));p.drawPath(path)
   p.restore()
  for i,ratio in enumerate(self.cursors):
   x=r.left()+ratio*r.width();p.setPen(QPen(QColor("#bdc8d0"),1,Qt.DashLine))
   p.drawLine(int(x),int(r.top()),int(x),int(r.bottom()))
   p.fillRect(QRectF(x-8,r.top(),16,18),QColor("#44535e"));p.setPen(QColor("#ffffff"));p.drawText(QRectF(x-8,r.top(),16,18),Qt.AlignCenter,"AB"[i])
 def mousePressEvent(self,e):
  x=self.cursor_x(e.position());self.drag=min(range(2),key=lambda i:abs(self.cursors[i]-x));self.move_cursor(x)
 def mouseMoveEvent(self,e):
  if self.drag is not None:self.move_cursor(self.cursor_x(e.position()))
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
