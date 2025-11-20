from flask import request
from main import app

@app.route('/')
def index():
    return "Hello, World"

@app.route("/api/events", methods=["POST"])
def events():
    events = request.json.get("events", [])
    return events
    # return {"status": "ok"}



# sample post for /api/events using curl in powershell
# curl -Method POST http://localhost:8080/api/events `
#   -Headers @{ "Content-Type"="application/json" } `
#   -Body '{
#     "events": [
#       { "type": "page_view", "page": "/home", "timestamp": "2025-01-01T12:00:00Z" },
#       { "type": "login", "user_id": 42, "timestamp": "2025-01-01T12:01:30Z" }
#     ]
#   }'