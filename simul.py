import requests
import time
import random
from datetime import datetime


# ==========================
# CONFIGURATION
# ==========================
API_URL = "https://uqrm1hfskb.execute-api.ap-south-1.amazonaws.com/prod/telemetry"
API_KEY = "my-secret-key-123"
   # You’ll get this from API Gateway in Step 2

# Vehicle IDs (you can add more)
VEHICLE_IDS = ["veh-001", "veh-002", "veh-003", "veh-004"]

# Center coordinates for simulation area (e.g., Bangalore)
BASE_LAT = 12.9716
BASE_LON = 77.5946

# Movement radius (degrees ~ roughly 100m per 0.001)
MOVE_DELTA = 0.002

# ==========================
# HELPER FUNCTION
# ==========================
def random_move(lat, lon, delta=MOVE_DELTA):
    """Generate small random movement around given coordinates."""
    return lat + random.uniform(-delta, delta), lon + random.uniform(-delta, delta)


# ==========================
# MAIN LOOP
# ==========================
def main():
    print("Starting vehicle simulator...")
    print(f"Sending data to: {API_URL}")
    print("Press Ctrl+C to stop.\n")

    vehicle_positions = {vid: (BASE_LAT, BASE_LON) for vid in VEHICLE_IDS}

    while True:
        for vid in VEHICLE_IDS:
            # Move each vehicle a bit randomly
            lat, lon = random_move(*vehicle_positions[vid])
            vehicle_positions[vid] = (lat, lon)

            # Create telemetry payload
            payload = {
                "vehicle_id": vid,
                "timestamp": datetime.utcnow().isoformat(),
                "latitude": lat,
                "longitude": lon,
                "speed_kmh": round(random.uniform(20, 100), 2),
                "fuel_percent": round(random.uniform(30, 100), 2)
            }

            headers = {
                "Content-Type": "application/json",
                "x-api-key": API_KEY
            }

            try:
                response = requests.post(API_URL, json=payload, headers=headers, timeout=5)
                if response.status_code == 200:
                    print(f"[{vid}] Sent → lat={lat:.5f}, lon={lon:.5f}, speed={payload['speed_kmh']} km/h")
                else:
                    print(f"[{vid}] Failed ({response.status_code}): {response.text}")
            except Exception as e:
                print(f"[{vid}] Error sending data: {e}")

        time.sleep(3)  # Send updates every 3 seconds


# ==========================
# ENTRY POINT
# ==========================
if __name__ == "__main__":
    main()
