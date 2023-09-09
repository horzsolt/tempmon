class Metric:

    def __init__(self, temperature : float, humidity : float, battery : float, device_id : int=1):
        self._device_id = device_id
        self._temperature = temperature
        self._humidity = humidity
        self._battery = battery

    @property
    def temperature(self):
        return self._temperature

    @property
    def humidity(self):
        return self._humidity

    @property
    def battery(self):
        return self._battery

    @property
    def device_id(self):
        return self._device_id

    def __str__(self):
        return f"{self._device_id} {str(self.temperature)} {str(self.humidity)} {str(self.battery)}"