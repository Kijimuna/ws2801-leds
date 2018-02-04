import threading, time, logging
from effects.off import Off
from effects.unicolor import *
from effects.multicolor import *

logger = logging.getLogger(__name__)
            
class LEDThread(threading.Thread):

    def __init__(self, pixelcount=183):
        threading.Thread.__init__(self)

        self._shutdown = False

        self._mode = 0
        
        self._effects = [Off(pixelcount),
                   KnightRider(pixelcount),
                   Arthur3(pixelcount),
                   MovingRGBCycle(pixelcount),
                   Arthur2(pixelcount),
                   Arthur(pixelcount),
#                   White(pixelcount),      
                   SingleColor(pixelcount),
                   RainbowColors(pixelcount),
                   RainbowCycle(pixelcount),
                   RainbowCycleSuccessive(pixelcount),
                   AppearFromBack(pixelcount)
                   ]       
    
    def _mode_name(self, mode):
        return self._effects[mode].get_name()
        
    def current_effect(self):
        return self._effects[self._mode]
    
    def shutdown(self):
        self._shutdown = True
        self._effects[self._mode].hide() 

    def is_running(self):
        return not self._shutdown    
    
    def on_power_on(self):
        self.set_mode(1)

    def before_power_off(self):
        self.set_mode(0)
        time.sleep(0.3)
            
    def next_color(self, step=0.01):
        self.current_effect().next_color(step)

    def prev_color(self, step=0.01):
        self.current_effect().prev_color(step)

    def light_up(self, step=0.01):
        self.current_effect().light_up(step)
    
    def light_down(self, step=0.01):
        self.current_effect().light_down(step)
                
    def next_mode(self):  
        if self._mode == 0:
            logger.error ('Ignoring switch to next mode (leds are off)')
            return

        new_mode = self._mode + 1
        if new_mode >= len(self._effects):
            new_mode = 1
        self.set_mode(new_mode)
        
    def set_mode(self, mode):
        if(not isinstance(mode, int) or mode >= len(self._effects) or mode < 0):
            logger.error ('Mode ' + str(mode) + ' is not known!')
        elif(mode != self._mode):
            old_mode = self._mode
            logger.info ("Switching from '" + self._mode_name(old_mode) + "' to '" + self._mode_name(mode) + "'")
            self._mode = mode
            self._effects[old_mode].hide()

    def run(self):
        logger.info("Starting LED thread ...")
        while not self._shutdown:
            self._effects[self._mode].show()  # blocks until hide() or _wake()
        logger.info("Shutdown LED thread...")

