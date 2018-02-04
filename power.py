import logging
from spx import Smartplug

logger = logging.getLogger(__name__)


class PowerSupply(object):
    """
    This is the base class of power supply.
    The methods to turn the power of or on send switch the respective power supply hardware 
    of concrete implementations and invokes on_power_on()/before_power_off() on the callback
    objects that relies on the power supply in the real world.
    
    The base class also acts as No-Power-Switch delegator, i.e. it invokes the callback methods
    directly without interacting with any power switch hardware in the real world.
    """
    
    def __init__(self, callback):
        self._callback = callback
        try:
            if self._is_off():
                self._on = False   
            else:
                logger.warn ('Oops, power is already on on boot. This is unsuspected on boot. Better turn it off ...')
                self.off()
        except Exception as e:
            logger.error ("Failed to initalize power supply on boot ... let's hope it is off ;-)")
            logger.error (e.__str__())
            self._on = False   
    
    def is_on(self):
        """
        Cheap method that relies on the internal state only (i.e. does not interact with the real world hardware).
        """
        return self._on

    def on(self):
        try:
            if self._is_off():
                logger.info ('Turning power on.')
                self._turn_on()
                logger.info  ('Turned power on.')
            else:
                logger.info  ('Power is already on.')
            self._on = True
            self._callback.on_power_on()
        except Exception as e:
            logger.error ("Failed to connect to power switch, can't turn it on")
            logger.error (e.__str__())
            
    def off(self):
        self._callback.before_power_off()
        try:
            if self._is_on():
                logger.info ('Turning power off.')
                self._turn_off()
                logger.info ('Turned power off.')
            else:
                logger.info ('Power is already off.')
            self._on = False
        except Exception as e:
            logger.error ("Failed to connect to power switch, can't turn it off")
            logger.error (e.__str__())

    def _is_on(self):
        """
        This (more expensive) method is expected to request the real world hardware.
        """
        return True # power plugs without back channel are regarded as being ON ...

    def _is_off(self):
        """
        This (more expensive) method is expected to request the real world hardware.
        """
        return True # ... and being OFF at the same time

    def _turn_on(self):
        pass

    def _turn_off(self):
        pass


class FixPowerSupply(PowerSupply):
    """
    Power supply that is not programmatically switchable.
    """
    
    def __init__(self, callback):
        logger.info ('Using a not programmatically switchable power supply.')
        super(FixPowerSupply, self).__init__(callback)
            
            
class EdimaxPowerPlug(PowerSupply):
    """
    Edimax SP-1101W implementation of the PowerSupply class.
    """
    
    def __init__(self, callback, host='192.168.1.35', username='admin', password='1234'):
        logger.info ('Using edimax smartplug as switchable power supply.')
        self._ediplug = Smartplug(host, username, password)
        super(EdimaxPowerPlug, self).__init__(callback)
            
    def _is_on(self):
        return self._ediplug.get_state() == 'ON'

    def _is_off(self):
        return self._ediplug.get_state() == 'OFF'

    def _turn_on(self):
        return self._ediplug.on()

    def _turn_off(self):
        return self._ediplug.off()
