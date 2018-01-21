import sys
from leds import LEDThread

led_thread = LEDThread(9)
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
        print >> sys.stderr, 'Shutdown ...'
        led_thread.set_mode(1)
        led_thread.shutdown()
        led_thread.join()
