from motion_sensor import MotionSensor
from temperature_sensor import TemperatureSensor
from tk_display import TkDisplay
from car_bay import CarBay


class Carpark:
    TOTAL_BAYS = 0
    ISLE_COUNT = 0
    BAY_LENGTH = 0
    LOCATION = None
    BROKER_HOST = 1883
    PORT = None

    def __init__(
            self, location: str, total_car_bays: int, isles: int,
            broker_host: str = "TPD", port: int = 1883) -> None:

        self.motion_sensor = MotionSensor(self)
        self.temperature_sensor = TemperatureSensor(self)

        self.LOCATION = location
        self.BROKER_HOST = broker_host
        self.PORT = port
        self.TOTAL_BAYS = total_car_bays
        self.ISLE_COUNT = isles
        self.BAY_LENGTH = int(self.TOTAL_BAYS / self.ISLE_COUNT)

        self.available_bays = []
        self.assigned_bays = []

        self.car_bays = [
            [CarBay(self, isle=isle, bay=bay) for bay in range(self.BAY_LENGTH)]
            for isle in range(self.ISLE_COUNT)
        ]

        self.display = TkDisplay(self)

    def assign_vehicle(self, bay_number: tuple[int, int], number_plate: str) -> bool:
        bay, isle = bay_number
        if self.car_bays[isle][bay].is_assigned and \
                len(self.assigned_bays) < self.TOTAL_BAYS:
            return False
        self.car_bays[isle][bay].assign(number_plate)
        self.update()
        return True

    def free_bay(self, bay_number: tuple[int, int]) -> bool:
        bay, isle = bay_number
        if not self.car_bays[isle][bay].is_assigned and \
                len(self.available_bays) < self.TOTAL_BAYS:
            return False
        self.car_bays[isle][bay].free_bay()
        self.update()
        return True

    def update(self) -> None:
        self.available_count = []
        for isle in self.car_bays:
            for bay in isle:
                if bay.is_assigned:
                    self.assigned_bays.append(bay)
                    continue
                self.available_bays.append(bay)

    def get_bay(self, number_plate: str) -> tuple[int, int] | None:
        for i, isle in enumerate(self.car_bays):
            for j, bay in enumerate(isle):
                if not bay.is_assigned:
                    continue
                if bay.vehicle != number_plate:
                    continue
                return tuple(bay())
        return None