from base import _BaseEffect

def _wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)
 
def _wheel_rgb(pos):
    if pos < 85:
        return (255, 0, 0)
    elif pos < 170:
        return (0, 255, 0)
    else:
        return (0, 0, 255)  


class RainbowColors(_BaseEffect):
    
    def __init__(self, pixelcount):
        super(RainbowColors, self).__init__(pixelcount)

    def get_name(self):
        return "Rainbow Colors"

    def _show(self):
        count = self.get_count()
        while not self._hide:
            for i in range(256):
                for led in range(count):
                    if self._hide: return
                    r, g, b = _wheel((256 // count + i) % 256)
                    self._set_pixel(led, r, g, b)
                self._flush()
                if self._hide: return
                self._wait(0.001)                


class RainbowCycle(_BaseEffect):
    
    def __init__(self, pixelcount):
        super(RainbowCycle, self).__init__(pixelcount)

    def get_name(self):
        return "Rainbow Cycle"

    def _show(self):
        count = self.get_count()
        while not self._hide:
            for i in range(256):
                for led in range(count):
                    if self._hide: return
                    r, g, b = _wheel(((led * 256 // count) + i) % 256)
                    self._set_pixel(led, r, g, b)
                self._flush()
                if self._hide: return
                self._wait(0.001) 

                
class RainbowCycleSuccessive(_BaseEffect):
    
    def __init__(self, pixelcount):
        super(RainbowCycleSuccessive, self).__init__(pixelcount)

    def get_name(self):
        return "Successive Rainbow Cycle"

    def _show(self):
        wait=0.05
        count = self.get_count()
        self._clear()
        while not self._hide:
            for led in range(count):
                if self._hide: return
                r, g, b = _wheel(((led * 256 // count)) % 256)
                self._set_pixel(led, r, g, b)
                self._flush()
                if self._hide: return
                self._wait(wait)                
            for led in range(count):
                if self._hide: return
                self._set_pixel(led, 0, 0, 0)
                self._flush()
                if self._hide: return
                self._wait(wait)                

                
class MovingRGBCycle(_BaseEffect):
    
    def __init__(self, pixelcount):
        super(MovingRGBCycle, self).__init__(pixelcount)

    def get_name(self):
        return "Moving RGB Cycle"

    def _show(self):
        count = self.get_count()
        self._clear()
        while not self._hide:
            for j in range(count):
                for i in range(count):
                    if self._hide: return
                    led = (j + i) % count
                    r, g, b = _wheel_rgb(i * 256 // count % 256)
                    self._set_pixel(led, r, g, b)
                self._flush()
                if self._hide: return
                self._wait(0.01)

class Arthur(_BaseEffect):
    
    def __init__(self, pixelcount):
        super(Arthur, self).__init__(pixelcount)

    def get_name(self):
        return "Arthur's effect"

    def _show(self):
        count = self.get_count()
        self._clear()
        while not self._hide:
            for i in range(count-1):
                self._set_all_pixels(0, 255, 0)
                self._set_pixel(i, 255, 0, 0)
                self._set_pixel(i+1, 255, 0, 0)
                self._flush()
                if self._hide: return
                self._wait(0.01)
                
class Arthur2(_BaseEffect):
    
    def __init__(self, pixelcount):
        super(Arthur2, self).__init__(pixelcount)

    def get_name(self):
        return "Arthur's second effect"

    def _show(self):
        count = self.get_count()
        while not self._hide:
            self._set_all_pixels(0, 255, 0)
            for color in range(256):
                r, g, b = _wheel((color*7)%256)
                
                for i in range(count//2 + count%2):
                    self._set_pixel(i*2, r, g, b)
                self._flush()
                if self._hide: return
                self._wait(0.02)                
                
class Arthur3(_BaseEffect):
    
    def __init__(self, pixelcount):
        super(Arthur3, self).__init__(pixelcount)

    def get_name(self):
        return "Arthur's third effect"

    def _show(self):
        count = self.get_count()
        while not self._hide:
            for color in range(256):
                for led in range(count):
                    if self._hide: return
                    r, g, b = _wheel((256 // count + (17*led)+ (17*color)) % 256)
                    self._set_pixel(led, r, g, b)
                self._flush()
                if self._hide: return
                self._wait(0.05)                
