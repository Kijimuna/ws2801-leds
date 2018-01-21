import sys
from leds import LEDThread
from slider import SliderThread, UP, DOWN

try:
    from evdev import InputDevice, categorize, ecodes, event
except ImportError:    
    # probably not running on a pi ... 
    pass

trigger_buttons = dict()
slider_buttons = dict();


def register_slider_buttons(downButton, upButton, sliderId):
    slider_buttons[downButton] = (sliderId, DOWN);
    slider_buttons[upButton] = (sliderId, UP);


def register_trigger_button(button, function):
    trigger_buttons[button] = function;


if __name__ == '__main__':

    led_thread = LEDThread()

    slider_thread = SliderThread()
    slider_thread.registerSlider('light', led_thread.light_up, led_thread.light_down)
    slider_thread.registerSlider('color', led_thread.next_color, led_thread.prev_color)

    register_trigger_button(288, led_thread.on_off)    # button 1
    register_slider_buttons(290, 294, 'light')         # button  2, 3
    register_slider_buttons(295, 298, 'color')         # buttons 4, 5
    register_trigger_button(299, led_thread.next_mode) # button 6
    
    led_thread.start()
    slider_thread.start()
        
    try:
        joystick = InputDevice('/dev/input/event1')
        print (joystick)
        for event in joystick.read_loop():
            if event.type == ecodes.EV_KEY:
                print categorize(event)
                
                if event.code in trigger_buttons and event.value == 1:  # button pressed
                    trigger_buttons[event.code]();
                elif event.code in slider_buttons:
                    if(event.value == 1):  # button pressed
                        slider_thread.start_movement(*slider_buttons[event.code])
                    if(event.value == 0):  # button released
                        slider_thread.stop_movement(*slider_buttons[event.code])

    except KeyboardInterrupt:
        print >> sys.stderr, 'Shutdown ...'
        slider_thread.shutdown()
        slider_thread.join()
        led_thread.set_mode(1)
        led_thread.shutdown()
        led_thread.join()
