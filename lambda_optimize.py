"""AWS Lambda stub for route optimization.

Deploy behind API Gateway (HTTP API). Accepts JSON body:
{
  "points": [[lat, lon], ...],  # includes source, optional waypoints, destination
  "strategy": "nearest" | "tsp" | "none"
}
Returns optimized order and simple metrics. For production you might:
- Integrate OR-Tools for full TSP/VRP/CVRPTW
- Add traffic / fuel / time window constraints
- Cache OSRM sub-routes for efficiency
"""

import json
import math
import urllib.request

OSRM_BASE = "https://router.project-osrm.org"  # Replace with self-hosted for scale


def distance_sq(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2


def nearest_neighbor(points):
    if len(points) <= 2:
        return points
    source = points[0]
    destination = points[-1]
    middle = points[1:-1]
    order = []
    current = source
    remaining = middle[:]
    while remaining:
        remaining.sort(key=lambda p: distance_sq(p, current))
        nxt = remaining.pop(0)
        order.append(nxt)
        current = nxt
    return [source] + order + [destination]


def osrm_distance(route):
    # Build OSRM query; coordinates are lon,lat
    coord_str = ";".join(f"{p[1]},{p[0]}" for p in route)
    url = f"{OSRM_BASE}/route/v1/driving/{coord_str}?overview=false"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("routes"):
            r = data["routes"][0]
            return r.get("distance", None), r.get("duration", None)
    except Exception:
        return None, None
    return None, None


def handler(event, context):  # Lambda entry point
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        points = body.get("points")
        strategy = body.get("strategy", "nearest")
        if not points or len(points) < 2:
            return _response(400, {"error": "Need at least source and destination"})

        if strategy == "nearest":
            ordered = nearest_neighbor(points)
        elif strategy == "none":
            ordered = points
        elif strategy == "tsp":
            # Placeholder: use nearest + return to destination
            ordered = nearest_neighbor(points)
        else:
            return _response(400, {"error": "Unknown strategy"})

        dist, dur = osrm_distance(ordered)
        return _response(200, {
            "ordered_points": ordered,
            "strategy": strategy,
            "distance_m": dist,
            "duration_s": dur
        })
    except Exception as e:
        return _response(500, {"error": str(e)})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

# For local testing
if __name__ == "__main__":
    sample = {
        "body": json.dumps({
            "points": [[12.9716,77.5946],[12.9730,77.5970],[12.9700,77.6000],[12.9685,77.5930]],
            "strategy": "nearest"
        })
    }
    print(handler(sample, None))
