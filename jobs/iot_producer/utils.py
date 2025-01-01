import uuid
import json


def json_serializer(obj):
    """
    ensures UUID types are converted to strings for JSON serialization.
    """
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def is_destination_reached(current_location, destination):
    """
    check to see if the vehicle has reached or passed the destination.
    """
    if (current_location["latitude"] >= destination["latitude"]
            and current_location["longitude"] <= destination["longitude"]):
        return True
    return False
