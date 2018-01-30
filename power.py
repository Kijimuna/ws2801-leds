from spx import Smartplug

class SwitchablePower(object):
    """
    This is the base class of switchable power plugs.
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
                print ('Oops, power is already on on boot. This is unsuspected on boot. Better turn it off ...')
                self.off()
        except Exception as e:
            print ("Failed to request power state on boot ... let's hope it is off ;-)")
            print(e.__str__())
            self._on = False   
        
    
    def is_on(self):
        """
        Cheap method that relies on the internal state only (i.e. does not interact with the real world hardware).
        """
        return self._on

    def on(self):
        try:
            if self._is_off():
                print ('Turning power on.')
                self._turn_on()
                print ('Turned power on.')
            else:
                print ('Power is already on.')
            self._on = True
            self._callback.on_power_on()
        except Exception as e:
            print ("Failed to connect to power switch, can't turn it on")
            print(e.__str__())

            
    def off(self):
        self._callback.before_power_off()
        try:
            if self._is_on():
                print ('Turning power off.')
                self._turn_off()
                print ('Turned power off.')
            else:
                print ('Power is already off.')
            self._on = False
        except Exception as e:
            print ("Failed to connect to power switch, can't turn it off")
            print(e.__str__())


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

            
class EdimaxPowerPlug(SwitchablePower):
    """
    Edimax SP-1101W implementation of the SwitchablePower class.
    """
    
    def __init__(self, callback, host='192.168.1.35', username='admin', password='1234'):
        print ('Using edimax smartplug as switchable power supply.')
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
