from smart_home import Device, Light, Room, Sensor, SmartThermostat, Thermostat
from typing import Type

"""Methods for reading data from a file and creating a device 
(light, thermostat, sensor)"""
def read_file(filename) -> list[list[str]]:
    rooms_values = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for room_values in file.readlines():
                rooms_values.append(list(room_values.strip().split("|", maxsplit=3)))
    except FileNotFoundError:
        print(f"{filename} not found")
    return rooms_values

DEVICE_CLASSES: dict[str, Type[Device]] = {
    "Light": Light,
    "Thermostat": Thermostat,
    "Sensor": Sensor,
    "SmartThermostat": SmartThermostat
}

def create_device_from_file(device_type, name, params) -> Device:
    return DEVICE_CLASSES[device_type](device_type, name, params)

if __name__ == "__main__":
    """Creating rooms and devices from a file and printing them"""
    parlor = Room("Гостиная")
    kitchen = Room("Кухня")
    bedroom = Room("Спальня")
    for room in read_file("config.txt"):
        if room[0] == parlor.get_room_name():
            parlor.add_device(create_device_from_file(room[1], room[2], room[3]))
        elif room[0] == kitchen.get_room_name():
            kitchen.add_device(create_device_from_file(room[1], room[2], room[3]))
        elif room[0] == bedroom.get_room_name():
            bedroom.add_device(create_device_from_file(room[1], room[2], room[3]))
    parlor.add_device(Light("Light", "Лампа4", "power=100,state=off"))
    print(parlor)
    print(kitchen)
    print(bedroom)

    """Output total power consumption"""
    print(parlor.get_total_power())
    print(kitchen.get_total_power())
    print(bedroom.get_total_power())

    """Changing parameters of different devices:
    In the living room sensor: 25 -> 45
    In the kitchen light: 40 -> 45, on -> off
    In the bedroom thermostat: 20 -> 45, 22 -> 54"""
    parlor[2].change_params(value=45)
    kitchen[0].change_params(power=45, state="off")
    bedroom[0].change_params(temperature=45, target=54)
    print(parlor)
    print(kitchen)
    print(bedroom)

    """Testing magic methods
    String and debug representations:"""
    print(parlor)
    print(kitchen)
    print(bedroom)
    print(repr(parlor))
    print(repr(kitchen))
    print(repr(bedroom))

    """Device comparison:"""
    print(parlor[2] == kitchen[1])
    bedroom[0].change_params(temperature=22, target=24)
    print(bedroom[0] == parlor[1])

    """Adding a room with elements:"""
    new_parlor = parlor + kitchen[0]
    print(new_parlor)

    """Iteration"""
    for device in new_parlor:
        print(device)

    """Length"""
    print(len(new_parlor))

    """Index access for rooms"""
    print(new_parlor[0])
    print(new_parlor[2:])

    """Creating a 'smart thermostat' (thermostat + sensor)"""
    smart_thermostat1 = SmartThermostat(
        "SmartThermostat",
        "УмныйТермостат1",
        "temperature=12,target=14,value=15"
    )
    smart_thermostat2 = SmartThermostat(
        "SmartThermostat",
        "УмныйТермостат2",
        "temperature=12,target=14,value=15"
    )
    print(smart_thermostat1 == smart_thermostat2)
    print(smart_thermostat1)
    smart_thermostat1.change_params(temperature=13, target=15, value=89)
    print(smart_thermostat1)
