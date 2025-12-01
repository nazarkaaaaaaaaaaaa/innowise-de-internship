from abc import ABC, abstractmethod

class DevicePrintableMixin:
    def __str__(self) -> str:
        params_str = ",".join(f"{k}={v}" for k, v in self._params.items())
        return f"{self._device_type}|{self._device_name}|{params_str}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self._device_type}, name={self._device_name}, params={self._params})"

class Device(DevicePrintableMixin, ABC):
    """
    SOLID:
    - SRP: Single responsibility - defines the core device interface and properties.
    - OCP: Open for extension - allows creating new device types through inheritance.
    - LSP: Liskov Substitution - ensures all subclasses maintain device interface compatibility.
    - ISP: Interface Segregation - provides minimal essential interface for devices.
    - DIP: Dependency Inversion - high-level modules depend on this abstraction.
    """
    @abstractmethod
    def __init__(self, device_type: str, device_name: str, params: dict):
        self._device_type = device_type
        self._device_name = device_name
        self._params = params

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @property
    def serialize_params(self) -> dict:
        return self._params

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
    """
    SOLID:
    - LSP: Liskov Substitution - can be substituted for Device and PowerConsumerMixin.
    - SRP: Single responsibility - manages light-specific state and behavior.
    - OCP: Open for extension - can be extended without modifying this class.
    """
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


class Thermostat(Device):
    """
    SOLID:
    - SRP: Single responsibility - manages temperature settings only.
    - LSP: Liskov Substitution - can be substituted for Device.
    - OCP: Open for extension - can be inherited by SmartThermostat.
    """
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


class Sensor(Device):
    """
    SOLID:
    - SRP: Single responsibility - handles sensor value management only.
    - ISP: Interface Segregation - provides clean sensor-specific interface.
    - LSP: Liskov Substitution - can be substituted for Device.
    """
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


class SmartThermostat(Thermostat, Sensor):
    """
    SOLID:
    - LSP: Liskov Substitution - can be substituted for both Thermostat and Sensor.
    - SRP: Single responsibility - combines temperature control and sensing.
    - ISP: Interface Segregation - inherits only necessary interfaces from parents.
    - OCP: Open for extension - can be further extended without modification.
    """
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


class SmartLight(Light, Thermostat, PowerConsumerMixin):
    """
    SOLID:
    - LSP: Liskov Substitution - can be substituted for Light, Thermostat and PowerConsumerMixin.
    - SRP: Single responsibility - combines lighting, temperature control and power monitoring.
    - ISP: Interface Segregation - inherits multiple focused interfaces.
    - OCP: Open for extension - can be extended with additional functionality.
    """
    def __init__(self, device_type: str, device_name: str, params: dict):
        super().__init__(device_type, device_name, params)

    def __eq__(self, other: "SmartLight"):
        if not isinstance(other, SmartLight):
            return NotImplemented
        return (
            self.temperature == other.temperature
            and self.target == other.target
            and self.power == other.power
            and self.state == other.state
        )
