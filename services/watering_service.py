class WateringService:
    def __init__(self, watering_config):
        self.__config = watering_config

    def calculate_milliseconds(self, soil_moisture):
        if soil_moisture > self.__config['minSoilMoisture']:
            # no watering
            return 0

        # watering
        return self.__config['wateringMilliseconds']