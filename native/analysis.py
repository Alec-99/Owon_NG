"""Compatibility APIs for the shared sample-indexed decoding implementation."""
from statistics import median
from native.decoding import pwm_periods, uart_events, i2c_events

def pwm(samples, rate, threshold=2.5):
    periods = pwm_periods(samples,rate,threshold)
    return {"frequency_hz": 1/median((b-a)/rate for a,b,_ in periods),
            "duty_percent": 100*median(v for _,_,v in periods)}

def uart(samples, rate, baud=9600, threshold=2.5):
    events = uart_events(samples,rate,baud,threshold)
    return [(e.start/rate,e.value) for e in events if e.kind=="data"], sum(e.kind=="framing" for e in events)

def i2c(clock, data, rate, threshold=2.5):
    events = i2c_events(clock,data,rate,threshold)
    return [( (e.stop-1)/rate,e.value,e.ack) for e in events if e.value is not None], sum(e.kind=="start" for e in events)
