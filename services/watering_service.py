class WateringService:
    def __init__(self, watering_config):
        config = watering_config

        self.__min_soil_moisture = int(config['minSoilMoisture'])
        self.__watering_milliseconds = int(config['wateringMilliseconds'])

    def calculate_milliseconds(self, soil_moisture):
        if soil_moisture <= self.__min_soil_moisture:
            # no watering
            return 0

        # watering
        return self.__watering_milliseconds
