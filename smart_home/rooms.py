from smart_home.devices import Light, Device
from typing import Iterator


class PowerCalculationMixin:
    devices: list[Device]

    def get_total_power(self):
        return sum(device.get_power() for device in self.devices if isinstance(device, Light))


class Room(PowerCalculationMixin):
    """
    SOLID Compliance:
        - S (Single Responsibility):
          Room stores devices and provides high-level operations on them.
          Power calculation is delegated to PowerCalculationMixin instead of this class.

        - O (Open/Closed):
          New behaviors (e.g., aggregation logic, filtering, metrics) can be added via mixins
          or composition without modifying the class itself.

        - L (Liskov Substitution):
          Works with any object implementing the Device interface; subclasses of Device
          can be freely substituted.

        - I (Interface Segregation):
          Room depends only on the minimal Device interface (e.g., __str__, get_power),
          not on concrete implementations like Light or Thermostat.

        - D (Dependency Inversion):
          Room relies on the abstract Device type rather than concrete device classes,
          allowing extensibility and loose coupling.
    """
    def __init__(self, room_name: str):
        self.__room_name = room_name
        self.devices = []

    def __add__(self, other: Device) -> "Room":
        new_room = Room(self.__room_name)
        new_room.devices = self.devices + [other]
        return new_room

    def __getitem__(self, item: int|slice) -> Device:
        return self.devices[item]

    def __len__(self) -> int:
        return len(self.devices)

    def __iter__(self) -> Iterator[Device]:
        return iter(self.devices)

    def __str__(self) -> str:
        room_str = "\n    ".join(str(device) for device in self.devices)
        return f"{self.__room_name}: {room_str}"

    def __repr__(self) -> str:
        room_str = "\n    ".join(repr(device) for device in self.devices)
        return f"Room's name - {self.__room_name}: {room_str}"

    def get_room_name(self) -> str:
        return self.__room_name

    def add_device(self, device: Device) -> list[Device]:
        self.devices.append(device)
        return self.devices

    def remove_device(self, device: Device) -> list[Device]:
        self.devices.remove(device)
        return self.devices
