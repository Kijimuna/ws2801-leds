import colorsys as _colorsys

from base import _BaseEffect


def _hex(self, i):             
    return '{:0>2}'.format(hex(i)[2:])


class _UniColor(_BaseEffect):

    def __init__(self, pixelcount):
        super(_UniColor, self).__init__(pixelcount)

        # Default values for starting color (about green)
        self._h, self._l, self._s = 0.3333, 0.5, 1.0

    def _update_color(self):    
        r, g, b = _colorsys.hls_to_rgb(self._h, self._l, self._s)
        self._r, self._g, self._b = int(round(r * 255.0)), int(round(g * 255.0)), int(round(b * 255.0))
    
    def next_color(self, step):
        #print self.get_name() + ": next color"
        self._h = (self._h + step) % 1 # h=0|1 -> red h=1/3 -> green h=2/3=blue
        self._update_color()

    def prev_color(self, step):
        #print self.get_name() + ": prev color"
        self._h = (self._h - step) % 1
        self._update_color()
    
    def light_up(self, step):
        #print self.get_name() + ": light up"
        self._l = min(1.0, self._l + step) # l=1 -> white, l=0 -> black , l=0.5 plain color
        self._update_color()
    
    def light_down(self, step):
        #print self.get_name() + ": light down"
        self._l = max(0.02, self._l - step)
        self._update_color()

    def get_light(self): 
        return self._l

    def get_html_color(self): 
        return "#" + _hex(self._r) + _hex(self._g) + _hex(self._b)

        
    
class SingleColor(_UniColor):

    def __init__(self, pixelcount):
        super(SingleColor, self).__init__(pixelcount)

    def get_name(self):
        return "Single Color"
    
    def _update_color(self):    
        self._wake()
        
    def _show(self):
        super(SingleColor, self)._update_color()
        self._set_all_pixels(self._r, self._g, self._b)
        self._flush()
        self._wait()
   


class AppearFromBack(_UniColor):
    
    def __init__(self, pixelcount):
        super(AppearFromBack, self).__init__(pixelcount)

    def get_name(self):
        return "Appear From Back"

    def _show(self):
        self._update_color()
        count = self.get_count()
        while not self._hide:
            for i in range(count):
                for run in reversed(range(i, count)):
                    if self._hide: return
                    self._clear()
                    
                    # already cumulated pixels
                    for led in range(i):
                        self._set_pixel(led, self._r, self._g, self._b)
                    
                    # running pixel
                    self._set_pixel(run, self._r, self._g, self._b)
                    
                    self._flush()
                    if self._hide: return
                    self._wait(0.005)                
