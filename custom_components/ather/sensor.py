from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback
from .const import DOMAIN, CONF_VIN, CONF_MODEL, SENSORS_META

async def async_setup_entry(hass, entry, async_add_entities):
    vin = entry.data[CONF_VIN]
    model = entry.data.get(CONF_MODEL, "EV Scooter")
    async_add_entities([AtherSensor(vin, model, key, meta, entry.entry_id) for key, meta in SENSORS_META.items()])

class AtherSensor(SensorEntity):
    def __init__(self, vin, model, key, meta, entry_id):
        self._vin = vin
        self._model = model
        self._key = key
        self._parent = meta["parent"]
        self._entry_id = entry_id
        self._attr_name = f"Ather {model} {meta['name']}"
        self._attr_unique_id = f"ather_{vin}_{key}"
        self._attr_device_class = meta["class"]
        self._attr_native_unit_of_measurement = meta["unit"]
        self._attr_icon = meta["icon"]
        self._state = None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._vin)},
            "name": f"Ather {self._model}",
            "manufacturer": "Ather Energy",
            "model": self._model
        }

    @property
    def native_value(self):
        return self._state

    async def async_added_to_hass(self):
        self.async_on_remove(async_dispatcher_connect(self.hass, f"{DOMAIN}_update_{self._vin}", self._handle_update))

    @callback
    def _handle_update(self):
        cache = self.hass.data[DOMAIN][self._entry_id]["cache"]
        
        if self._parent in cache and self._key in cache[self._parent]:
            val = cache[self._parent][self._key]
            vehicle_state = cache.get("telemetry.bike", {}).get("vehicle_state")
            
            if self._key == "chargingStatus":
                if vehicle_state in ["sleep", "standby", "awake", "ride"]:
                    self._state = "Not Charging"
                elif vehicle_state == "charged":
                    self._state = "Charged"
                elif vehicle_state == "charging":
                    self._state = "Charging"
                else:
                    self._state = str(val) if val else "Not Charging"
            
            elif self._key == "odo":
                try: self._state = round(float(val), 1)
                except: pass
                
            elif self._key in ["battery_soc", "range"]:
                try:
                    parsed_val = int(float(val))
                    if self._key == "battery_soc" and parsed_val == 0 and self._state is not None and self._state > 5:
                        return
                    self._state = parsed_val
                except: pass
            else:
                self._state = str(val) if val is not None else None
                
            self.async_write_ha_state()