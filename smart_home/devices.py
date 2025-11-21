from abc import ABC, abstractmethod


class Device(ABC):
    """
    SOLID:
    - S (Single Responsibility):
        Defines common attributes and the abstract interface for devices.
        Does not handle device-specific validation or behavior.
    - O (Open/Closed):
        New device types can be added by subclassing without modifying
        the base class itself.
    - I (Interface Segregation):
        Exposes only minimal required methods (`change_params`, `__eq__`),
        avoiding unnecessary interface burden for subclasses.
    - D (Dependency Inversion):
        Higher-level code works with the `Device` abstraction instead of
        concrete implementations.
    """
    def __init__(self, device_type: str, device_name: str, params: str):
        self.__device_type = device_type
        self.__device_name = device_name
        self.params = params

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    def __str__(self) -> str:
        return f"{self.get_type()}, {self.get_name()}, {self.get_params()}"

    def __repr__(self) -> str:
        return f"Type = {self.get_type()}, Name = {self.get_name()}, Params = {self.get_params()}"

    @abstractmethod
    def change_params(self, **kwargs) -> str:
        pass

    def get_type(self) -> str:
        return self.__device_type

    def get_name(self) -> str:
        return self.__device_name

    def get_params(self) -> str:
        return self.params


class Light(Device):
    """
    SOLID:
    - S:
        Responsible only for managing light-specific parameters.
    - O:
        Can be extended (e.g., SmartLight) without modifying this class.
    - L (Liskov Substitution):
        Fully substitutable for `Device` — preserves expected behavior
        and interface contracts.
    """
    def __init__(self, device_type: str, device_name: str, params: str):
        super().__init__(device_type, device_name, params)

    def __eq__(self, other: "Light"):
        if not isinstance(other, Light):
            return NotImplemented
        return (
                self.get_power() == other.get_power()
                and self.get_state() == other.get_state()
        )

    def change_params(self, **kwargs):
        power = kwargs.get("power")
        state = kwargs.get("state")
        if not isinstance(power, int):
            raise TypeError("power must be an integer")
        if state not in ("on", "off"):
            raise ValueError("state must be 'on' or 'off'")
        if not (0 < power < 150):
            raise ValueError("power must be between 1 and 149")
        self.params = f"power={power}, state={state}"
        return self.params

    def get_power(self) -> int:
        return int(self.params[6:self.params.find(",")])

    def get_state(self) -> str:
        return self.params.split("=", maxsplit=3)[2]


class Thermostat(Device):
    """
    SOLID:
    - S:
        Responsible only for thermostat logic and parameters.
    - O:
        Can be extended by new thermostat types without modification.
    - L:
        Can be used anywhere a `Device` is expected.
    """
    def __init__(self, device_type: str, device_name: str, params: str):
        super().__init__(device_type, device_name, params)

    def __eq__(self, other: "Thermostat"):
        if not isinstance(other, Thermostat):
            return NotImplemented
        return (
                self.get_temperature() == other.get_temperature()
                and self.get_target() == other.get_target()
        )

    def change_params(self, **kwargs):
        temperature = kwargs.get("temperature")
        target = kwargs.get("target")
        if not isinstance(temperature, int):
            raise TypeError("temperature must be an integer")
        if not isinstance(target, int):
            raise TypeError("target must be an integer")
        if not (-30 < temperature < 60):
            raise ValueError("temperature must be between -29 and 59")
        if not (-30 < target < 60):
            raise ValueError("target must be between -29 and 59")
        self.params = f"temperature={temperature}, target={target}"
        return self.params

    def get_temperature(self) -> int:
        return int(self.params.split(",")[0].split("=")[1])

    def get_target(self) -> int:
        return int(self.params.split(",")[1].split("=")[1])


class Sensor(Device):
    """
        SOLID:
        - S:
            Handles only the `value` parameter.
        - O:
            New sensor types can be created by inheritance.
        - L:
            Substitutable for `Device` without breaking behavior.
    """
    def __init__(self, device_type: str, device_name: str, params: str):
        super().__init__(device_type, device_name, params)

    def __eq__(self, other: "Sensor"):
        if not isinstance(other, Sensor):
            return NotImplemented
        return (
            self.get_value() == other.get_value()
        )

    def change_params(self, **kwargs):
        value = kwargs.get("value")
        if not isinstance(value, int):
            raise TypeError("value must be an integer")
        if not (0 < value < 100):
            raise ValueError("value must be between 1 and 99")
        self.params = f"value={value}"
        return self.params

    def get_value(self) -> int:
        return int(self.params.rsplit("=", 1)[1])


class SmartThermostat(Thermostat, Sensor):
    """
    SOLID:
    - S:
        Responsible only for combining thermostat and sensor functionality,
        not reinventing either separately.
    - O:
        Extends behavior of two existing classes without modifying them.
    - L:
        Can be used in place of `Device` or `Thermostat` while preserving
        expected interface behavior. Method signatures are compatible and
        behavior remains consistent with parent contracts.
    - D:
        External systems depend on the `Device` abstraction, not this class
        directly.
    """
    def __init__(self, device_type: str, device_name: str, params: str):
        super().__init__(device_type, device_name, params)

    def __eq__(self, other: "SmartThermostat"):
        if not isinstance(other, SmartThermostat):
            return NotImplemented
        return (
            self.get_temperature() == other.get_temperature()
            and self.get_target() == other.get_target()
            and self.get_value() == other.get_value()
        )

    def change_params(self, **kwargs):
        temperature = kwargs.get("temperature", self.get_temperature())
        target = kwargs.get("target", self.get_target())
        value = kwargs.get("value", self.get_value())
        self.params = f"temperature={temperature},target={target},value={value}"
        return self.params
