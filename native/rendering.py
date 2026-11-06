"""Pixel envelopes preserve sampled extrema; never modify source samples."""
import math

def envelope(samples, first, stop, pixels):
    if pixels < 1 or not 0 <= first < stop <= len(samples):
        raise ValueError("Ongeldig weergavevenster.")
    count = stop-first
    result = []
    for x in range(pixels):
        a = first + math.floor(x*count/pixels)
        b = first + math.ceil((x+1)*count/pixels)
        segment = samples[a:min(stop,b)]
        result.append((min(segment), max(segment)))
    return result
