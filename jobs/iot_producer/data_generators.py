import random
from datetime import datetime, timedelta

from models import (
    VehicleData, GPSData, TrafficCameraData, WeatherData, EmergencyIncidentData
)
from config import (
    LATITUDE_INCREMENT, LONGITUDE_INCREMENT,
    LONDON_COORDINATES, BIRMINGHAM_COORDINATES
)
from utils import is_destination_reached


class DataGenerator:
    def __init__(self):
        self.current_time = datetime.now()
        self.current_location = LONDON_COORDINATES.copy()

    def get_next_time(self):

        self.current_time += timedelta(seconds=random.randint(30, 60))
        return self.current_time

    def move_vehicle(self, vehicle):

        moved_coords = vehicle.move(
            self.current_location["latitude"],
            self.current_location["longitude"],
            LATITUDE_INCREMENT,
            LONGITUDE_INCREMENT,
        )
        self.current_location = moved_coords
        return moved_coords

    def generate_all_data(self, vehicle):

        timestamp = self.get_next_time()
        location = self.move_vehicle(vehicle)

        vehicle_data = VehicleData.generate(vehicle.vehicle_id, timestamp, location)
        gps_data = GPSData.generate(vehicle.vehicle_id, timestamp)
        traffic_data = TrafficCameraData.generate(vehicle.vehicle_id, timestamp, location)
        weather_data = WeatherData.generate(vehicle.vehicle_id, timestamp, location)
        emergency_data = EmergencyIncidentData.generate(vehicle.vehicle_id, timestamp, location)

        return {
            "vehicle_data": vehicle_data,
            "gps_data": gps_data,
            "traffic_data": traffic_data,
            "weather_data": weather_data,
            "emergency_data": emergency_data,
            "destination_reached": is_destination_reached(location, BIRMINGHAM_COORDINATES)
        }
