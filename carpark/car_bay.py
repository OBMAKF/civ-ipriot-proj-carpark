class CarBay:
    def __init__(self, carpark, bay: int, isle: int) -> None:
        self.carpark = carpark
        self.number = (bay, isle)
        self.is_assigned = False
        self.vehicle = None

    def __call__(self, *args, **kwargs) -> tuple[int, int]:
        return self.number

    def assign(self, number_plate: str) -> None:
        if self.is_assigned:
            return
        self.vehicle = number_plate
        self.is_assigned = True

    def free_bay(self) -> None:
        if not self.is_assigned:
            return
        self.vehicle = None
        self.is_assigned = False