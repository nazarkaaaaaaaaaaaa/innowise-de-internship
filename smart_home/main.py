from smart_home import Device, Light, Room, Sensor, SmartThermostat, SmartLight, Thermostat
from typing import Any, Type

DEVICE_CLASSES: dict[str, Type[Device]] = {
    "Light": Light,
    "Thermostat": Thermostat,
    "Sensor": Sensor,
    "SmartThermostat": SmartThermostat
}

def create_device(device_type: str, device_name: str, params: dict) -> Device:
    device_class = DEVICE_CLASSES[device_type]
    return device_class(device_type, device_name, params)

def cast(value):
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    return value

def read_file(filepath: str) -> dict[str, Any]:
    loaded_rooms = {}
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                room_name, dev_type, dev_name, params_str = line.split("|")
                params = {}
                for pair in params_str.split(","):
                    key, value = pair.split("=")
                    params[key] = cast(value.strip())
                if room_name not in loaded_rooms:
                    loaded_rooms[room_name] = Room(room_name)
                room_device = create_device(dev_type, dev_name, params)
                loaded_rooms[room_name].add_device(room_device)
    except FileNotFoundError:
        print(f"File {filepath} not found")
    return loaded_rooms

def write_rooms_to_file(rooms: dict[str, Room], filepath: str):
    with open(filepath, "w", encoding="utf-8") as file:
        for room in rooms.values():
            file.write(str(room) + "\n")

if __name__ == "__main__":
    """Creating rooms and devices from a file and printing them"""
    rooms = read_file("config.txt")
    for room in rooms.values():
        print(room)
    parlor = rooms.get("Гостиная")
    kitchen = rooms.get("Кухня")
    bedroom = rooms.get("Спальня")

    """Changing parameters of different devices:
        In the parlor sensor: 25 -> 45
        In the kitchen light: 40 -> 50
        In the bedroom thermostat: 20 -> 45, 22 -> 54"""
    parlor.get_by_name("Датчик1").value = 45
    kitchen.get_by_name("Лампа2").power = 50
    bedroom.get_by_name("Термостат2").temperature = 45
    bedroom.get_by_name("Термостат2").target = 54
    print("\nChanging parameters of different devices:")
    print(parlor)
    print(kitchen)
    print(bedroom)

    """Output total power consumption"""
    print("\nOutput total power consumption:")
    print(parlor.get_total_power())
    print(kitchen.get_total_power())
    print(bedroom.get_total_power())

    """Testing magic methods
    String and debug representations:"""
    print("\nTesting magic methods")
    print("String and debug representations:")
    print(parlor)
    print(kitchen)
    print(bedroom)
    print(repr(parlor))
    print(repr(kitchen))
    print(repr(bedroom))

    """Device comparison:"""
    print("\nDevice comparison:")
    print(parlor[2] == kitchen[1])
    bedroom[0].params = 22, 24
    print(bedroom[0] == parlor[1])

    """Adding a room with elements:"""
    print("\nAdding a room with elements:")
    parlor_kitchen = (parlor + kitchen).rename("Гостиная-Кухня")
    print(parlor_kitchen)

    """Iteration"""
    print("\nIteration:")
    for device in parlor_kitchen:
        print(device)

    """Length"""
    print("\nRoom's length:")
    print(len(parlor_kitchen))

    """Index access for rooms"""
    print("\nIndex access for rooms:")
    print(parlor_kitchen[0])
    print(parlor_kitchen[2:])

    """Sorting"""
    print("\nSorting:")
    rooms["Гостиная-Кухня"] = parlor_kitchen
    sorted_rooms = sorted(rooms.values())
    for room in sorted_rooms:
        print(room)

    """Creating a 'smart thermostat' (thermostat + sensor)"""
    print("\nCreating a 'smart thermostat' (thermostat + sensor)")
    smart_thermostat1 = SmartThermostat("SmartThermostat","УмныйТермостат1",{"temperature": 14, "target": 15, "value": 12})
    print(smart_thermostat1)
    smart_thermostat2 = SmartThermostat("SmartThermostat","УмныйТермостат2", {"temperature": 14, "target": 15, "value": 12})
    print(smart_thermostat2)

    """MRO"""
    print("\nMRO:")
    for cls in SmartThermostat.mro():
        print(cls)

    """Smart thermostat comparison:"""
    print("\nSmart thermostat comparison:")
    print(smart_thermostat1 == smart_thermostat2)

    """Changing parameters of smart thermostat:"""
    print("\nChanging parameters of smart thermostat:")
    print(smart_thermostat1)
    smart_thermostat1.temperature = 13
    smart_thermostat1.target = 15
    smart_thermostat1.value = 89
    print(smart_thermostat1)

    """Creating a 'smart light'"""
    print("\nCreating a 'smart light'")
    smart_light1 = SmartLight("SmartLight", "УмнаяЛампа1", {"temperature": 14, "target": 15, "power": 12, "state": "on"})
    print(smart_light1.power)

    parlor_kitchen.add_device(smart_thermostat1)
    write_rooms_to_file(rooms, "report.txt")
