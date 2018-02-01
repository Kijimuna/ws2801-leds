import logging.config
import yaml

logging.config.dictConfig(yaml.load(open('logging.yml', 'r')))

from power import EdimaxPowerPlug
from leds import LEDThread
from slider import SliderThread, UP, DOWN

try:
    from evdev import InputDevice, categorize, ecodes, event
except ImportError:    
    # probably not running on a pi ... 
    pass

logger = logging.getLogger(__name__)

button_names = dict()

trigger_buttons = dict()
slider_buttons = dict();

def register_slider_buttons(downButton, upButton, sliderId):
    slider_buttons[downButton] = (sliderId, DOWN);
    slider_buttons[upButton] = (sliderId, UP);


def register_trigger_button(button, function):
    trigger_buttons[button] = function;


def on_off():
    if on_off_switch.is_on():
        on_off_switch.off()
    else:    
        on_off_switch.on()

def next_mode():
    if on_off_switch.is_on():
        led_thread.next_mode()

def light_up(step):
    if on_off_switch.is_on():
        led_thread.light_up(step)

def light_down(step):
    if on_off_switch.is_on():
        led_thread.light_down(step)

def next_color(step):
    if on_off_switch.is_on():
        led_thread.next_color(step)

def prev_color(step):
    if on_off_switch.is_on():
        led_thread.prev_color(step)

def log_button_event(event):
    if not logger.isEnabledFor(logging.INFO): 
        return
    
    if event.code in button_names:
        button_name = button_names.get(event.code)
    else: 
        button_name = "Unknown Button"    
        
    logger.info("Recognized " + button_name + ": " + str(categorize(event)))
                

    

if __name__ == '__main__':


    led_thread = LEDThread()
    on_off_switch = EdimaxPowerPlug(led_thread)

    button_names[288] = "On/Off Button"
    button_names[290] = "Left Light Button"
    button_names[294] = "Right Light Button"
    button_names[295] = "Left Color Button"
    button_names[298] = "Right Color Button"
    button_names[299] = "Next Effect Button"
    
    register_trigger_button(288, on_off)    # button 1
    register_slider_buttons(290, 294, 'light')         # button  2, 3
    register_slider_buttons(295, 298, 'color')         # buttons 4, 5
    register_trigger_button(299, next_mode) # button 6

    slider_thread = SliderThread()
    slider_thread.registerSlider('light', light_up, light_down)
    slider_thread.registerSlider('color', next_color, prev_color)
    
    led_thread.start()
    slider_thread.start()
        
    try:
        joystick = InputDevice('/dev/input/event1')
        logger.info("Found joystick: " + str(joystick))
        for event in joystick.read_loop():
            if event.type == ecodes.EV_KEY:
                log_button_event(event)
                if event.code in trigger_buttons and event.value == 1:  # button pressed
                    trigger_buttons[event.code]();
                elif event.code in slider_buttons:
                    if(event.value == 1):  # button pressed
                        slider_thread.start_movement(*slider_buttons[event.code])
                    if(event.value == 0):  # button released
                        slider_thread.stop_movement(*slider_buttons[event.code])

    except KeyboardInterrupt:
        logger.info('Shutting all down ...')
        slider_thread.shutdown()
        slider_thread.join()
        led_thread.set_mode(1)
        led_thread.shutdown()
        led_thread.join()
