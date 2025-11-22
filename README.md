# Vehicle Tracking & Route Optimization

A web-based vehicle tracking and intelligent route optimization system built with Leaflet, OSRM public routing, and a pluggable AWS Lambda optimization backend.

## Features
- Live vehicle tracking (auto refresh every ~7s) with status badges (active/warning/critical).
- Click-to-set Source, Destination, and multiple Waypoints directly on the map.
- Standard route along real roads using OSRM (no straight-line air paths).
- Optimized route ordering (nearest-neighbor heuristic) with distance & ETA summary.
- Manual Clear Route & visual markers for all route points.
- Modular architecture ready for AWS Lambda based advanced optimization (e.g., traffic, fuel, constraints).

## Novelty & Differentiators
- Unified UI combining live telemetry and ad-hoc route planning for dispatch decisions.
- Point-and-click route construction lowers friction vs manual coordinate entry.
- Optimization is abstracted for easy swap: local heuristic → AI-assisted (Gemini) → server-side Lambda (e.g., constraint solver).
- Resilient UI: vehicle updates no longer disrupt route inputs or selection state.
- Extensible: add cost models (fuel burn rate, time windows) in Lambda without changing front-end.

## Quick Start
Open `index.html` in a local server (recommended to avoid CORS issues):
```bash
python3 -m http.server 8000
# Visit http://localhost:8000/index.html
```
Run telemetry simulation (optional):
```bash
python3 simul.py
```

## Route Workflow
1. Click "Set Source" then click a point on the map.
2. Click "Set Destination" and map click again.
3. Optionally add any number of waypoints via "Add Waypoint".
4. Click "Draw Standard Route" for ordered path as added.
5. Click "Optimize Route" to reorder waypoints for shorter travel (heuristic).
6. Review distance & ETA summary in Route Status box.

## AWS Lambda Integration (Planned)
Deploy `lambda_optimize.py` behind API Gateway. Front-end can POST:
```json
{
  "points": [[lat, lon], [lat, lon], ...],
  "mode": "fastest"
}
```
Lambda responds with optimized ordering & metrics. Replace local `optimizeRoute()` with a fetch to that endpoint.

## Gemini / AI Extension (Optional)
Use Gemini to:
- Recommend additional stop consolidation.
- Predict congestion (if historical data provided).
- Suggest alternate depots.
Do this by sending waypoint list & constraints to Gemini and merging response before OSRM routing.

## Security Notes
- Avoid committing real API keys; use environment variables for production.
- Public OSRM is rate-limited; self-host for scale.

## Future Enhancements
- Time window & capacity constraints (CVRPTW via OR-Tools in Lambda).
- Fuel-aware optimization (penalize low fuel segments, prioritize refuel stops).
- Traffic layer overlays (e.g., from Mapbox/Google if licensed).
- Persistent route plans saved to DynamoDB.
- WebSocket streaming for sub-second telemetry.

## Folder Overview
- `index.html` – UI + Leaflet + routing logic.
- `simul.py` – Vehicle telemetry simulator.
- `lambda_optimize.py` – Sample AWS Lambda route optimization stub.

## License
Internal / Hacktoberfest demo. Add a license file if distributing.
