import time
import json

from kafka_producer import KafkaProducer
from data_generators import DataGenerator
from models import Vehicle
from config import (
    VEHICLE_TOPIC, GPS_TOPIC, TRAFFIC_TOPIC, WEATHER_TOPIC, EMERGENCY_TOPIC
)
from utils import json_serializer


def main():
    producer = KafkaProducer()
    data_generator = DataGenerator()
    vehicle = Vehicle(vehicle_id="Vehicle-IoT-Data")

    try:
        while True:
            data_bundle = data_generator.generate_all_data(vehicle)

            # Convert each dict to JSON (with our custom serializer if needed)
            vehicle_json = json.dumps(data_bundle["vehicle_data"], default=json_serializer)
            gps_json = json.dumps(data_bundle["gps_data"], default=json_serializer)
            traffic_json = json.dumps(data_bundle["traffic_data"], default=json_serializer)
            weather_json = json.dumps(data_bundle["weather_data"], default=json_serializer)
            emergency_json = json.dumps(data_bundle["emergency_data"], default=json_serializer)

            # Produce to Kafka
            producer.produce(
                VEHICLE_TOPIC,
                key=str(data_bundle["vehicle_data"]["id"]),
                value=vehicle_json,
                callback=KafkaProducer.delivery_report
            )
            producer.produce(
                GPS_TOPIC,
                key=str(data_bundle["gps_data"]["id"]),
                value=gps_json,
                callback=KafkaProducer.delivery_report
            )
            producer.produce(
                TRAFFIC_TOPIC,
                key=str(data_bundle["traffic_data"]["id"]),
                value=traffic_json,
                callback=KafkaProducer.delivery_report
            )
            producer.produce(
                WEATHER_TOPIC,
                key=str(data_bundle["weather_data"]["id"]),
                value=weather_json,
                callback=KafkaProducer.delivery_report
            )
            producer.produce(
                EMERGENCY_TOPIC,
                key=str(data_bundle["emergency_data"]["id"]),
                value=emergency_json,
                callback=KafkaProducer.delivery_report
            )

            # Check if the vehicle has reached the destination
            if data_bundle["destination_reached"]:
                print("Vehicle has reached Birmingham. Simulation ending...")
                break

            time.sleep(5)

    except KeyboardInterrupt:
        print("Simulation interrupted by user.")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
