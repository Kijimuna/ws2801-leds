import logging.config
import yaml
from time import sleep

logging.config.dictConfig(yaml.load(open('logging_dev.yml', 'r')))

from power import FixPowerSupply
from leds import LEDThread

logger = logging.getLogger(__name__)

print("--------------------------------------------------------")
print("Make sure power is turned on!")
print("--------------------------------------------------------")
print()

logger.info('Starting ...')

led_thread = LEDThread(183)

power = FixPowerSupply(led_thread)
power.on()

led_thread.set_mode(1)
led_thread.start()


while led_thread.is_running():
    try:
        sleep(20)
    except KeyboardInterrupt:
        logger.info('Shutting all down ...')
        led_thread.set_mode(0)
        led_thread.shutdown()
        led_thread.join()
