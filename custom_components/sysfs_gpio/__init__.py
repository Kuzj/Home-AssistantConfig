"""Support for controlling GPIO pins over sysfs"""
import logging

from periphery import GPIO  # pylint: disable=import-error

from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sysfs_gpio"


def setup(hass, config):
    """Set up the BeagleBone Black GPIO component."""
    # pylint: disable=import-error

    def cleanup_gpio(event):
        """Stuff to do before stopping."""
        pass
        #for gpio in gpio_list:
        #    gpio.close()
        #GPIO.cleanup()

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