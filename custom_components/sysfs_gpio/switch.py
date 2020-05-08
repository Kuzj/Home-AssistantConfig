"""Allows to configure a switch GPIO."""
import logging

import voluptuous as vol

from custom_components import sysfs_gpio
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, DEVICE_DEFAULT_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import ToggleEntity


_LOGGER = logging.getLogger(__name__)

CONF_PINS = "pins"
CONF_INITIAL = "initial"
CONF_INVERT_LOGIC = "invert_logic"

PIN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_INITIAL, default=False): cv.boolean,
        vol.Optional(CONF_INVERT_LOGIC, default=False): cv.boolean,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_PINS, default={}): vol.Schema({cv.string: PIN_SCHEMA})}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up GPIO devices."""
    pins = config[CONF_PINS]

    switches = []
    for pin, params in pins.items():
        switches.append(GPIOSwitch(pin, params))
    add_entities(switches)


class GPIOSwitch(ToggleEntity):
    """Representation of GPIO."""

    def __init__(self, pin, params):
        """Initialize the pin."""
        self._pin = pin
        self._name = params[CONF_NAME] or DEVICE_DEFAULT_NAME
        self._state = params[CONF_INITIAL]
        self._invert_logic = params[CONF_INVERT_LOGIC]
        self._gpio = sysfs_gpio.gpio_output(int(pin))

        if self._state is False:
            self._gpio.write(True if self._invert_logic else False)
        else:
            self._gpio.write(False if self._invert_logic else True)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self._gpio.write(False if self._invert_logic else True)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._gpio.write(True if self._invert_logic else False)
        self._state = False
        self.schedule_update_ha_state()