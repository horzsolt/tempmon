class Button:

    def __init__(self, id: float, button1: str, button2: str, button3: str, button4: str, battery: str, misc: str):
        self._device_id = id
        self._button1 = button1
        self._button2 = button2
        self._button3 = button3
        self._button4 = button4
        self._battery = battery
        self._misc = misc

    @property
    def device_id(self):
        return self._device_id

    @property
    def button1(self):
        return self._button1

    @property
    def button2(self):
        return self._button2

    @property
    def button3(self):
        return self._button3

    @property
    def button4(self):
        return self._button4

    @property
    def battery(self):
        return self._battery

    @property
    def misc(self):
        return self._misc

    def __str__(self):
        return f"{self.device_id} {self.button1} {self.button2} {self.battery} {self.channel}"
