import json
import base64


def decode_state(state):
    """Decode state data."""
    try:
        # Decode the state parameter
        decoded_bytes = base64.urlsafe_b64decode(state)
        decoded_str = decoded_bytes.decode()
        state_data = json.loads(decoded_str)  # Convert JSON string to dictionary
        return state_data
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid state parameter: {e}")


def encode_state(state_data):
    """Encode state data."""
    # Convert the state data to a JSON string
    state_str = json.dumps(state_data)

    # Encode the state string
    encoded_bytes = base64.urlsafe_b64encode(state_str.encode())
    encoded_state = encoded_bytes.decode()

    return encoded_state
