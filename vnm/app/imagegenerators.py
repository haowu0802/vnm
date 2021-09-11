from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, ResizeToFit, ResizeCanvas, ResizeToCover, SmartResize


class LocalImage(ImageSpec):
    processors = [SmartResize(1768, 992)]
    format = 'JPEG'
    options = {'quality': 100}

register.generator('app:localimage', LocalImage)