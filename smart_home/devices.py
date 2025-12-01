from abc import ABC, abstractmethod

class DevicePrintableMixin:
    def __str__(self) -> str:
        params_str = ",".join(f"{k}={v}" for k, v in self._params.items())
        return f"{self._device_type}|{self._device_name}|{params_str}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self._device_type}, name={self._device_name}, params={self._params})"

class Device(DevicePrintableMixin, ABC):
    @abstractmethod
    def __init__(self, device_type: str, device_name: str, params: dict):
        self._device_type = device_type
        self._device_name = device_name
        self._params = params

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def serialize_params(self) -> str:
        pass

    @property
    def device_type(self) -> str:
        return self._device_type

    @property
    def device_name(self) -> str:
        return self._device_name


class PowerConsumerMixin:
    @property
    def power(self) -> int:
        """Return power in watt"""
        raise NotImplementedError("A subclass must implement the power property")


class Light(Device, PowerConsumerMixin):
    def __init__(self, device_type: str, device_name: str, params: dict):
        params_copy = params.copy()
        params_copy.setdefault("power", 0)
        params_copy.setdefault("state", "off")
        params_copy["power"] = max(0, params_copy.get("power"))
        super().__init__(device_type, device_name, params_copy)

    def __eq__(self, other: "Light"):
        if not isinstance(other, Light):
            return NotImplemented
        return (
                self.power == other.power
                and self.state == other.state
        )

    @property
    def power(self) -> int:
        return self._params.get("power") if self._params.get("state") == "on" else 0

    @property
    def state(self) -> str:
        return self._params.get("state")

    @power.setter
    def power(self, power: int):
        self._params["power"] = max(0, power)

    def turn_off(self):
        self._params["state"] = "off"

    def turn_on(self):
        self._params["state"] = "on"
        
    def serialize_params(self) -> dict:
        return self._params


class Thermostat(Device):
    def __init__(self, device_type: str, device_name: str, params: dict):
        params_copy = params.copy()
        params_copy.setdefault("temperature", -30)
        params_copy.setdefault("target", -30)
        params_copy["temperature"] = max(-30, params_copy.get("temperature"))
        params_copy["target"] = max(-30, params_copy.get("target"))
        super().__init__(device_type, device_name, params_copy)

    def __eq__(self, other: "Thermostat"):
        if not isinstance(other, Thermostat):
            return NotImplemented
        return (
                self.temperature == other.temperature
                and self.target == other.target
        )

    @property
    def temperature(self) -> int:
        return self._params.get("temperature")

    @property
    def target(self) -> int:
        return self._params.get("target")

    @temperature.setter
    def temperature(self, temperature: int):
        self._params["temperature"] = max(-30, temperature)

    @target.setter
    def target(self, target: int):
        self._params["target"] = max(-30, target)
    
    def serialize_params(self) -> dict:
        return self._params


class Sensor(Device):
    def __init__(self, device_type: str, device_name: str, params: dict):
        params_copy = params.copy()
        params_copy.setdefault("value", 0)
        params_copy["value"] = max(0, params_copy.get("value"))
        super().__init__(device_type, device_name, params_copy)

    def __eq__(self, other: "Sensor"):
        if not isinstance(other, Sensor):
            return NotImplemented
        return (
            self.value == other.value
        )

    @property
    def value(self) -> int:
        return self._params.get("value")

    @value.setter
    def value(self, value: int):
        self._params["value"] = max(0, value)
        
    def serialize_params(self) -> dict:
        return self._params


class SmartThermostat(Thermostat, Sensor):
    def __init__(self, device_type: str, device_name: str, params: dict):
        super().__init__(device_type, device_name, params)

    def __eq__(self, other: "SmartThermostat"):
        if not isinstance(other, SmartThermostat):
            return NotImplemented
        return (
            self.temperature == other.temperature
            and self.target == other.target
            and self.value == other.value
        )
    
    def serialize_params(self) -> dict:
        return self._params


class SmartLight(Light, Thermostat, PowerConsumerMixin):
    def __init__(self, device_type: str, device_name: str, params: dict):
        super().__init__(device_type, device_name, params)

    @property
    def power(self) -> int:
        return self._params.get("power") if self._params.get("state") == "on" else 0

    def __eq__(self, other: "SmartLight"):
        if not isinstance(other, SmartLight):
            return NotImplemented
        return (
            self.temperature == other.temperature
            and self.target == other.target
            and self.power == other.power
            and self.state == other.state
        )

    def serialize_params(self) -> dict:
        return self._params
