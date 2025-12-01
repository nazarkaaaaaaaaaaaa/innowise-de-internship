from smart_home.devices import Device, PowerConsumerMixin
from typing import Iterator

class RoomPrintableMixin:
    """
    SOLID:
    - SRP: Single responsibility - manages collection of devices in a room.
    - OCP: Open for extension - can be extended with new room types or functionalities.
    - LSP: Liskov Substitution - can be used wherever a room-like container is expected.
    - ISP: Interface Segregation - provides clean room management interface.
    - DIP: High-level modules depend on Device abstraction, not concrete implementations.
    """
    def __str__(self) -> str:
        return "\n".join(f"{self.room_name}|{device}" for device in self.devices)

    def __repr__(self) -> str:
        return "\n".join(f"Room name={self.room_name}|{repr(device)}" for device in self.devices)


class Room(RoomPrintableMixin):
    def __init__(self, room_name: str):
        self._room_name = room_name
        self.devices = []

    def __add__(self, other: "Room") -> "Room":
        if not isinstance(other, Room):
            raise TypeError(f"Cannot add {type(self)} with {type(other)}")
        new_room = Room("_combined")
        new_room.devices = self.devices + other.devices
        return new_room

    def __getitem__(self, item: int|slice) -> Device:
        return self.devices[item]

    def __len__(self) -> int:
        return len(self.devices)

    def __iter__(self) -> Iterator[Device]:
        return iter(self.devices)

    def __lt__(self, other: "Room") -> bool:
        if not isinstance(other, Room):
            raise TypeError(f"Cannot compare {type(self)} with {type(other)}")
        return self._room_name < other._room_name

    @property
    def room_name(self) -> str:
        return self._room_name

    def rename(self, new_name: str) -> "Room":
        self._room_name = new_name
        return self

    def add_device(self, device: Device) -> list[Device]:
        self.devices.append(device)
        return self.devices

    def remove_device(self, device: Device) -> list[Device]:
        self.devices.remove(device)
        return self.devices

    def get_total_power(self) -> int:
        total = 0
        for device in self.devices:
            if isinstance(device, PowerConsumerMixin):
                total += device.power
        return total

    def get_by_name(self, name: str) -> Device:
        for device in self.devices:
            if device.device_name == name:
                return device
        raise KeyError(f"Device with name '{name}' not found in room '{self._room_name}'")
