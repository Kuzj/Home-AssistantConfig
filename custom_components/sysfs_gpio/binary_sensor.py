"""Support for binary sensor sysfs GPIO."""
import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorDevice#BinarySensorEntity

from custom_components import sysfs_gpio
from homeassistant.const import CONF_NAME, DEVICE_DEFAULT_NAME
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_PINS = "pins"
CONF_INVERT_LOGIC = "invert_logic"

PIN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_INVERT_LOGIC, default=False): cv.boolean,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_PINS, default={}): vol.Schema({cv.string: PIN_SCHEMA})}
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sysfs GPIO platform."""
    binary_sensors = []
    pins = config[CONF_PINS]

    for pin, params in pins.items():
        binary_sensors.append(
            sysfsGPIOBinarySensor(pin, params)
        )
    add_entities(binary_sensors)

class sysfsGPIOBinarySensor(BinarySensorDevice):
    """Represent a binary sensor that uses sysfs GPIO."""

    def __init__(self, pin, params):
        """Initialize the sysfs binary sensor."""
        self._name = params[CONF_NAME] or DEVICE_DEFAULT_NAME
        self._pin = pin
        self._invert_logic = params[CONF_INVERT_LOGIC]
        self._gpio = sysfs_gpio.gpio_input(int(pin))
        self._gpio.edge = "both"
        self._state = self._gpio.read()

        def read_gpio():
            """Read state from GPIO."""
            self._state = self._gpio.read()
            self.schedule_update_ha_state()

        sysfs_gpio.listener.start(self._gpio,read_gpio)

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the entity."""
        return self._state != self._invert_logic