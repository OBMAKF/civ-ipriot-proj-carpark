from sensor import Sensor


class MotionSensor(Sensor):
    def __init__(self, carpark) -> None:
        self.carpark = carpark

    def read_sensor(self) -> None:
        pass

    def on_entrance(self, isle: int, bay: int, number_plate: str = None):
        if not self.carpark.is_available((bay, isle)):
            return
        self.carpark.assign_vehicle((bay, isle), number_plate)

    def on_exit(self, number_plate: str = None):
        if self.carpark.get_bay(number_plate) is None:
            return
        self.carpark.free_bay(self.carpark.get_bay(number_plate))

