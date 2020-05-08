"""Support for controlling GPIO pins over sysfs"""
import logging
import threading

from periphery import GPIO  # pylint: disable=import-error

from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sysfs_gpio"


def setup(hass, config):
    """Set up sysfs GPIO component."""
    # pylint: disable=import-error

    def cleanup_gpio(event):
        """Stuff to do before stopping."""
        listener.stop()

    def prepare_gpio(event):
        """Stuff to do when Home Assistant starts."""
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup_gpio)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare_gpio)
    return True

def gpio_input(pin):
    return GPIO(pin, 'in')

def gpio_output(pin):
    return GPIO(pin, 'out')

def gpio_output_high(pin):
    return GPIO(pin, 'high')

class EventListener():

    _thread = None
    _stopevent = None

    def gpio_poll(self,gpio,callback):
        while not self._stopevent.isSet():
            modify = gpio.poll(0.1)
            if modify:
                try:
                    callback()
                except Exception as e:
                    _LOGGER.error(e)
        gpio.close()
        _LOGGER.info(f"Stop event listener on {gpio.line} GPIO")

    def start(self,gpio,callback):
        if self._thread is not None:
            return
        self._stopevent = threading.Event()
        self._thread = threading.Thread(
            target=self.gpio_poll,
            args=(gpio,callback),
            daemon = True)
        self._thread.start()
        _LOGGER.info(f"Start event listener on {gpio.line} GPIO")

    def stop(self):
        if self._stopevent is not None:
            self._stopevent.set()
        if self._thread is not None:
            self._thread.join()

listener = EventListener()