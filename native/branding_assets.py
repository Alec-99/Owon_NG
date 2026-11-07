"""Deterministic platform conversion of the owner's selected concept artwork.

The square excludes only the caption beneath reference 1. Originals stay intact.
"""
import struct
from pathlib import Path
from PySide6.QtCore import QBuffer,QByteArray,QIODevice,QRect,Qt
from PySide6.QtGui import QImage

ICON_RECT=QRect(10,0,132,132)

def icon_image(source):
    image=QImage(str(source))
    if image.isNull():raise RuntimeError("Selected app icon unavailable: "+str(source))
    return image.copy(ICON_RECT)

def write_windows_icon(source,destination):
    """ICO directory with PNG frames, using Qt (no additional dependency)."""
    original=icon_image(source)
    sizes=(16,24,32,48,64,128,256)
    frames=[]
    for size in sizes:
        data=QByteArray();buffer=QBuffer(data);buffer.open(QIODevice.WriteOnly)
        image=original.scaled(size,size,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        if not image.save(buffer,"PNG"):raise RuntimeError("Icon conversion failed")
        frames.append(bytes(data))
    offset=6+16*len(frames);entries=[]
    for size,frame in zip(sizes,frames):
        entries.append(struct.pack("<BBBBHHII",size%256,size%256,0,0,1,32,len(frame),offset))
        offset+=len(frame)
    Path(destination).write_bytes(struct.pack("<HHH",0,1,len(frames))+b"".join(entries)+b"".join(frames))
