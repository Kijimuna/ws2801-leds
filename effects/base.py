import threading

try:
    import RPi.GPIO as GPIO
    import Adafruit_WS2801
    import Adafruit_GPIO.SPI as SPI
except ImportError:    
    # probably not running on a pi ... emulate all the PI stuff
    import mocks.GPIO as GPIO
    import mocks.WS2801 as Adafruit_WS2801
    import mocks.SPI as SPI

    
class _BaseEffect(object):

    def __init__(self, pixelcount):
        
        self._hide = True
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)

        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0
        
        self._pixels = Adafruit_WS2801.WS2801Pixels(pixelcount, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE), gpio=GPIO)
            
    def next_color(self, step):
        pass

    def prev_color(self, step):
        pass

    def light_up(self, step):
        pass
    
    def light_down(self, step):
        pass
    
    def get_count(self):
        return self._pixels.count()

    def get_name(self):
        pass

    def get_light(self): 
        pass

    def get_html_color(self): 
        pass

    def show(self):
        try:
            self._cond.acquire()
            print "Showing '" + self.get_name() + "'"
            self._hide = False
        finally:
            self._cond.release()
        self._show()

    def _show(self):
        pass

    def hide(self):
        try:
            self._lock.acquire()
            print "Hiding '" + self.get_name() + "'"
            self._hide = True
            self._cond.notify()
        finally:
            self._lock.release()

    def _set_pixel(self, led, r, g, b):
        self._pixels.set_pixel_rgb(led, r, b, g) # b and g are mixed up

    def _set_all_pixels(self, r, g, b):
        # self._pixels.set_pixels_rgb(r, g, b) <-- this is broken :-(
        for i in range(self._pixels.count()):
            self._pixels.set_pixel_rgb(i, r, b, g)  # b and g are mixed up
    
    def _clear(self):
        self._pixels.clear()
        
    def _flush(self):  
        self._pixels.show()
    
    def _wait(self, timeout = None):
        try:
            self._lock.acquire()
            if not self._hide:
                self._cond.wait(timeout)
        finally:
            self._lock.release()

    def _wake(self):
        try:
            self._lock.acquire()
            self._cond.notify()
        finally:
            self._lock.release()
