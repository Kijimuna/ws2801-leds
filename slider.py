import threading, time

DOWN = 0
UP = 1


class SliderThread(threading.Thread):

    def __init__(self, resolution = 0.0001, full_slide_time = 10):
        threading.Thread.__init__(self)

        self._shutdown = False

        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)

        self.resolution = resolution
        self._wait = float(full_slide_time) * float(resolution)
        
        self._slider_movements = dict()
        self._active_movements = set()
        
        
    def registerSlider(self, slider_id, up_function, down_function):
        self._slider_movements[(slider_id, UP)] = up_function
        self._slider_movements[(slider_id, DOWN)] = down_function
    
    def start_movement(self, sliderId, direction):    
        try:
            self._lock.acquire()
            self._active_movements.add((sliderId, direction))
            self._cond.notify()
        finally:
            self._lock.release()

    def stop_movement(self, slider_id, direction):    
        try:
            self._lock.acquire()
            if (slider_id, direction) in self._active_movements:
                self._active_movements.remove((slider_id, direction))
        finally:
            self._lock.release()
    
    def shutdown(self):
        try:
            self._lock.acquire()
            self._shutdown = True
            self._cond.notify()
        finally:
            self._lock.release()

    def is_running(self):
        return not self._shutdown    
        
    def run(self):
        print "Starting slider thread ..."
        while not self._shutdown:

            # sleep until we have work to do
            try:
                self._cond.acquire()
                if not self._active_movements and not self._shutdown:
                    self._cond.wait()
            finally:
                self._cond.release()
                        
            # work until nothing is do do and sleep again            
            while self._active_movements and not self._shutdown:
                try:
                    self._cond.acquire()
                    for movement in self._active_movements:
                        self._slider_movements.get(movement)(self.resolution)
                finally:       
                    self._cond.release()        
                time.sleep(self._wait)
                
        print "Shutdown slider thread..."    
        
        
if __name__ == '__main__':

    # just for testing the sliderthread ...
    class Mock:
        def __init__(self):
            self.light = 0.5
            self.color = 0.3333

        def light_up(self, step=0.01):
            self.light = min(1.0, self.light + step)
            print 'light + ' + str(step) + " = " + str(self.light)
    
        def light_down(self, step=0.01):
            self.light = max(0.02, self.light - step)
            print 'light + ' + str(step) + " = " + str(self.light)
    
        def color_up(self, step=0.01):
            self.color = (self.color + step) % 1 
            print 'color + ' + str(step) + " = " + str(self.color)
    
        def color_down(self, step=0.01):
            self.color = (self.color - step) % 1 
            print 'color - ' + str(step) + " = " + str(self.color)
    
    
    mock = Mock()
    
    slider_buttons = { 'light_down' : ('light', DOWN),
                     'light_up' :  ('light', UP),
                     'colorDown' : ('color', DOWN),
                     'colorUp' :  ('color', UP) } ;
    
    slider_thread = SliderThread()
    slider_thread.registerSlider('light', mock.light_up, mock.light_down)
    slider_thread.registerSlider('color', mock.color_up, mock.color_down)
    slider_thread.start()
    
    slider_thread.start_movement(*slider_buttons['light_up'])
    time.sleep(2)
    slider_thread.start_movement(*slider_buttons['colorDown'])
    time.sleep(3)
    
    slider_thread.stop_movement(*slider_buttons['colorDown'])
    slider_thread.stop_movement(*slider_buttons['light_down']) # no active movement
    time.sleep(2)
    
    slider_thread.stop_movement(*slider_buttons['light_up'])
    time.sleep(2)

    slider_thread.start_movement(*slider_buttons['light_down'])
    time.sleep(2)

    slider_thread.shutdown()

