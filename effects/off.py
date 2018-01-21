from base import _BaseEffect

class Off(_BaseEffect):

    def __init__(self, pixelcount):
        super(Off, self).__init__(pixelcount)

    def get_name(self):
        return "Off"
    
    def _show(self):
        self._clear()
        self._flush()
        self._wait()
        
    
