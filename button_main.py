import logging.config
import yaml
import sys

logging.config.dictConfig(yaml.load(open('logging.yml', 'r')))

import argparse
from power import EdimaxPowerPlug, FixPowerSupply
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
                
def find_joystick(name):
    all_found = []
    try:
        for i in range(10):
            device_file = '/dev/input/event' + str(i)
            device = InputDevice(device_file)
            found = str(device)
            if name in found:
                logger.info("Found joystick: " + found)
                return device
            else:
                all_found.append(found)    
    except:
        logger.error("Did not find a joystick named '" + name + "'. Found the following devices:")
        for found in all_found:
            logger.error("\t" + found)
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Starts button-based WS2801 controller')
    parser.add_argument("-joy", required=True, metavar='joystick_name', help="Name of the joystick to use")
    parser.add_argument("-edimax", required=False, nargs=2, metavar=('host', 'pass'), help="Use edimax power supply")
    args = parser.parse_args()

    joystick = find_joystick(args.joy)   
    if joystick is None: 
        sys.exit()
 
    led_thread = LEDThread()
    if args.edimax == None:
        on_off_switch = FixPowerSupply(led_thread)
    else: 
        on_off_switch = EdimaxPowerPlug(led_thread, args.edimax[0], 'admin', args.edimax[1])
 
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
