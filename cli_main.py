import logging.config
import yaml

logging.config.dictConfig(yaml.load(open('logging_dev.yml', 'r')))

import time

from power import FixPowerSupply
from leds import LEDThread


logger = logging.getLogger(__name__)


logger.info('Starting ...')

led_thread = LEDThread(9)

power = FixPowerSupply(led_thread)
power.on()

time.sleep(1)
led_thread.start()


while led_thread.is_running():
    try:
        print '(d) darken'
        print '(l) lighten'
        print '(c) change color '
        print '(C) change color back'
        print '(<i>) change mode'
        value = raw_input('Please choose: ')
        try: 
            print " got " + value
            mode = int(value)
            led_thread.set_mode(mode)
        except ValueError:
            if(value == 'd'):
                led_thread.light_down()
            elif(value == 'l'):
                led_thread.light_up()
            elif(value == 'c'):
                led_thread.next_color()
            elif(value == 'C'):
                led_thread.prev_color()
            else:
                print "'" + value + "' is not recognized"
    except KeyboardInterrupt:
        logger.info('Shutting all down ...')
        led_thread.set_mode(1)
        led_thread.shutdown()
        led_thread.join()
