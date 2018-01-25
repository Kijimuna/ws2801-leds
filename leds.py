import threading, time
from effects.off import Off
from effects.unicolor import *
from effects.multicolor import *
from ediplug.smartplug import SmartPlug


class OnOff(object):
    
    def __init__(self, led_thread, host='192.168.1.35', username='admin', password='493856'):
        self._led_thread = led_thread
        self._ediplug = SmartPlug(host, (username, password))
        print ('Found edimax smartplug')
        if self._ediplug.state == 'OFF':
            self._on = False   
        else:
            print ('Oops, leds are already on.')
            self._on = True
            self._off()
        
    
    def is_on(self):
        return self._on

    def on(self):
        if not self.is_on():
            print ('Turning leds on.')
            self._ediplug.state = 'ON'
            time.sleep(2)
            self._on = True
            self._led_thread.set_mode(2)
            print ('Turned leds on.')
    
    def off(self):
        if self.is_on():
            print ('Turning leds off.')
            self._led_thread.set_mode(0)
            time.sleep(0.3)
            self._ediplug.state = 'OFF'
            self._on = False
            print ('Turned leds off.')
            
            

class LEDThread(threading.Thread):

    def __init__(self, pixelcount=183):
        threading.Thread.__init__(self)

        self._shutdown = False

        self._mode = 0
        
        self._effects = [Off(pixelcount),
                   White(pixelcount),      
                   SingleColor(pixelcount),
                   KnightRider(pixelcount),
                   RainbowColors(pixelcount),
                   RainbowCycle(pixelcount),
                   RainbowCycleSuccessive(pixelcount),
                   MovingRGBCycle(pixelcount),
                   AppearFromBack(pixelcount)]       
    
    def _mode_name(self, mode):
        return self._effects[mode].get_name()
        
    def current_effect(self):
        return self._effects[self._mode]
    
    def shutdown(self):
        self._shutdown = True
        self._effects[self._mode].hide() 

    def is_running(self):
        return not self._shutdown    
            
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
            print 'Ignoring switch to next mode (leds are off)'
            return

        new_mode = self._mode + 1
        if new_mode >= len(self._effects):
            new_mode = 1
        self.set_mode(new_mode)
        
    def set_mode(self, mode):
        if(not isinstance(mode, int) or mode >= len(self._effects) or mode < 0):
            print 'Mode ' + str(mode) + ' is not known!'
        elif(mode != self._mode):
            old_mode = self._mode
            print "Switching from '" + self._mode_name(old_mode) + "' to '" + self._mode_name(mode) + "'"
            self._mode = mode
            self._effects[old_mode].hide()

    def run(self):
        print "Starting LED thread ..."
        while not self._shutdown:
            self._effects[self._mode].show()  # blocks until hide() or _wake()
        print "Shutdown LED thread..."

