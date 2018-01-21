from __future__ import print_function
import time


class WS2801Pixels(object):
    """WS2801/SPI interface addressable RGB LED lights."""

    def __init__(self, count, clk=None, do=None, spi=None, gpio=None):

        # Setup buffer for pixel RGB data.
        self._count = count
        self._pixels = [0] * (count * 3)

    def show(self):
        """Push the current pixel values out to the hardware.  Must be called to
        actually change the pixel colors.
        """
        print('|', end='')
        for i in range(self._count):
            print (self._channel(3 * i) + ':' + self._channel(3 * i + 1) + ':' + self._channel(3 * i + 2), end='|')
        print('')
        time.sleep(0.002)

    def _channel(self, pos):         
        return '{:0>3}'.format(str(self._pixels[pos]))
 
    def count(self):
        """Return the count of pixels."""
        return self._count

    def set_pixel(self, n, color):
        """Set the specified pixel n to the provided 24-bit RGB color.  Note you
        MUST call show() after setting pixels to see the LEDs change color!"""
        r = color >> 16
        g = color >> 8
        b = color
        # Note the color components will be truncated to 8-bits in the
        # set_pixel_rgb function call.
        self.set_pixel_rgb(n, r, g, b)

    def set_pixel_rgb(self, n, r, g, b):
        """Set the specified pixel n to the provided 8-bit red, green, blue
        component values.  Note you MUST call show() after setting pixels to
        see the LEDs change color!
        """
        assert n >= 0 and n < self._count, 'Pixel n outside the count of pixels!'
        self._pixels[n * 3] = r & 0xFF
        self._pixels[n * 3 + 1] = g & 0xFF
        self._pixels[n * 3 + 2] = b & 0xFF

    def get_pixel(self, n):
        """Retrieve the 24-bit RGB color of the specified pixel n."""
        r, g, b = self.get_pixel_rgb(n)
        return (r << 16) | (g << 8) | b

    def get_pixel_rgb(self, n):
        """Retrieve the 8-bit red, green, blue component color values of the
        specified pixel n.  Will return a 3-tuple of red, green, blue data.
        """
        assert n >= 0 and n < self._count, 'Pixel n outside the count of pixels!'
        return (self._pixels[n * 3], self._pixels[n * 3 + 1], self._pixels[n * 3 + 2])

    def set_pixels(self, color=0):
        """Set all pixels to the provided 24-bit RGB color value.  Note you
        MUST call show() after setting pixels to see the LEDs change!"""
        for i in range(self._count):
            self.set_pixel(i, color)

    def set_pixels_rgb(self, r, g, b):
        """Set all pixels to the provided 8-bit red, green, blue component color
        value.  Note you MUST call show() after setting pixels to see the LEDs
        change!
        """
        for i in range(self._count):
            self.set_pixel_rgb(i, r, g, b)

    def clear(self):
        """Clear all the pixels to black/off.  Note you MUST call show() after
        clearing pixels to see the LEDs change!
        """
        self.set_pixels(0)
