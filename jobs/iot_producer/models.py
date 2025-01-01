import uuid
import random
from datetime import datetime


class Vehicle:
    """
    Represents a vehicle object with base attributes.
    """
    def __init__(self, vehicle_id, make="Tesla", model="Model S", year=2024, fuel_type="Electric"):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.fuel_type = fuel_type

    def move(self, latitude, longitude, lat_inc, long_inc):
        """
        Moves the vehicle incrementally towards a destination with slight randomness.
        """
        return {
            "latitude": latitude + lat_inc + random.uniform(-0.0005, 0.0005),
            "longitude": longitude + long_inc + random.uniform(-0.0005, 0.0005),
        }


class VehicleData:
    @staticmethod
    def generate(vehicle_id, timestamp, location):
        """
        Generates data about the vehicle’s current state (speed, location, direction, etc.)
        """
        return {
            "id": str(uuid.uuid4()),
            "vehicle_id": vehicle_id,
            "timestamp": timestamp.isoformat(),
            "location": (location['latitude'], location['longitude']),
            "speed": random.uniform(10, 40),
            "direction": "North-East",
            "make": "Tesla",
            "model": "Model S",
            "year": 2024,
            "fuelType": "Electric",
        }


class GPSData:
    @staticmethod
    def generate(vehicle_id, timestamp):
        return {
            "id": str(uuid.uuid4()),
            "vehicle_id": vehicle_id,
            "timestamp": timestamp.isoformat(),
            "speed": random.uniform(0, 40),  # km/h
            "direction": "North-East",
            "vehicleType": "private",
        }


class TrafficCameraData:
    @staticmethod
    def generate(vehicle_id, timestamp, location, camera_id="Intelligent AI-powered Camera"):
        return {
            "id": str(uuid.uuid4()),
            "vehicle_id": vehicle_id,
            "camera_id": camera_id,
            "location": (location['latitude'], location['longitude']),
            "timestamp": timestamp.isoformat(),
            "snapshot": "Base64EncodedString",
        }


class WeatherData:
    @staticmethod
    def generate(vehicle_id, timestamp, location):
        return {
            "id": str(uuid.uuid4()),
            "vehicle_id": vehicle_id,
            "location": (location['latitude'], location['longitude']),
            "timestamp": timestamp.isoformat(),
            "temperature": random.uniform(-5, 26),
            "weatherCondition": random.choice(["Sunny", "Cloudy", "Rain", "Snow"]),
            "precipitation": random.uniform(0, 25),
            "windSpeed": random.uniform(0, 100),
            "humidity": random.randint(0, 100),
            "airQualityIndex": random.uniform(0, 500),
        }


class EmergencyIncidentData:
    @staticmethod
    def generate(vehicle_id, timestamp, location):
        return {
            "id": str(uuid.uuid4()),
            "vehicle_id": vehicle_id,
            "incidentId": str(uuid.uuid4()),
            "type": random.choice(["Accident", "Fire", "Medical", "Police", "None"]),
            "timestamp": timestamp.isoformat(),
            "location": (location['latitude'], location['longitude']),
            "status": random.choice(["Active", "Resolved"]),
            "description": "Description of the incident",
        }
