"""Initial offline sample analysis. No hardware timing or noise validation."""
from statistics import median

def pwm(samples, rate, threshold=2.5):
 edges=[i for i in range(1,len(samples)) if samples[i-1]<threshold<=samples[i]]
 if len(edges)<3:raise ValueError("Minimaal drie stijgende flanken vereist.")
 periods=[];duties=[]
 for a,b in zip(edges,edges[1:]):
  if b-a<8:raise ValueError("Te weinig samples per PWM-periode.")
  periods.append((b-a)/rate);duties.append(sum(v>=threshold for v in samples[a:b])/(b-a))
 return {"frequency_hz":1/median(periods),"duty_percent":100*median(duties)}

def uart(samples,rate,baud=9600,threshold=2.5):
 spb=rate/baud
 if spb<8:raise ValueError("UART vereist minimaal 8 samples per bit.")
 out=[];i=1;framing=0
 while i<len(samples):
  if samples[i-1]>=threshold>samples[i]:
   end=round(i+9.5*spb)
   if end>=len(samples):break
   if samples[round(i+.5*spb)]>=threshold:i+=1;continue
   value=sum((samples[round(i+(1.5+b)*spb)]>=threshold)<<b for b in range(8))
   if samples[end]>=threshold:out.append((i/rate,value))
   else:framing+=1
   i=max(i+1,round(i+10*spb))
  else:i+=1
 return out,framing

def i2c(clock,data,rate,threshold=2.5):
 if len(clock)!=len(data):raise ValueError("SCL en SDA moeten even lang zijn.")
 active=False;bits=[];out=[];starts=0
 for i in range(1,len(clock)):
  scl=clock[i]>=threshold;scl0=clock[i-1]>=threshold
  sda=data[i]>=threshold;sda0=data[i-1]>=threshold
  if scl and scl0 and sda!=sda0:
   if not sda:active=True;bits=[];starts+=1
   else:active=False;bits=[]
  elif active and scl and not scl0:
   bits.append(sda)
   if len(bits)==9:
    value=sum(int(bit)<<(7-n) for n,bit in enumerate(bits[:8]))
    out.append((i/rate,value,not bits[8]));bits=[]
 return out,starts
