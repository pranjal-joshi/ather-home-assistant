from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback
from .const import DOMAIN, CONF_VIN, CONF_MODEL

async def async_setup_entry(hass, entry, async_add_entities):
    vin = entry.data[CONF_VIN]
    model = entry.data.get(CONF_MODEL, "EV Scooter")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AtherDeviceTracker(vin, model, coordinator)])

class AtherDeviceTracker(TrackerEntity):
    def __init__(self, vin, model, coordinator):
        self._vin = vin
        self._model = model
        self._coordinator = coordinator
        self._attr_name = f"Ather {model} Location"
        self._attr_unique_id = f"ather_{vin}_location"
        self._latitude = None
        self._longitude = None
        self._accuracy = 0

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._vin)},
            "name": f"Ather {self._model}",
            "manufacturer": "Ather Energy",
            "model": self._model
        }

    @property
    def latitude(self): return self._latitude
    @property
    def longitude(self): return self._longitude
    @property
    def gps_accuracy(self): return self._accuracy
    @property
    def source_type(self): return SourceType.GPS

    async def async_added_to_hass(self):
        self.async_on_remove(async_dispatcher_connect(self.hass, f"{DOMAIN}_update_{self._vin}", self._handle_update))
        self._handle_update()

    @callback
    def _handle_update(self):
        cache = self._coordinator.data
        if "telemetry.bike" in cache and "gps_location" in cache["telemetry.bike"]:
            gps = cache["telemetry.bike"]["gps_location"]
            if "lat" in gps and "lng" in gps:
                self._latitude = gps["lat"]
                self._longitude = gps["lng"]
                self._accuracy = gps.get("Accuracy", 0)
                self.async_write_ha_state()