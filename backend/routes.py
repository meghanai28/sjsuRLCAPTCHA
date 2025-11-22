from flask import request
from main import app

@app.route('/')
def index():
    return "Hello, World"


# IGNORE ALL THIS JUNK BELOW!

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

# db.py
# import psycopg2
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_connection():
#     return psycopg2.connect(
#         host="localhost",
#         dbname="postgres",
#         user="postgres",
#         password=os.getenv("PSQL_PASSWORD"),
#         port=5432
#     )

# from flask import request, jsonify
# from main import app
# from db import get_connection


# @app.route("/")
# def index():
#     return "Hello, World"

# @app.route("/user", methods=["POST"])
# def create_user():
#     data = request.json
#     conn = get_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute("""
#             INSERT INTO webUser (user_id, username, email, is_verified_human)
#             VALUES (%s, %s, %s, %s)
#         """, (data["user_id"], data["username"], data["email"], data.get("is_verified_human", False)))

#         conn.commit()
#         return jsonify({"message": "User created"}), 201
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"error": str(e)}), 400
#     finally:
#         cur.close()
#         conn.close()

# @app.route("/user/<user_id>", methods=["GET"])
# def get_user(user_id):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM webUser WHERE user_id = %s", (user_id,))
#     row = cur.fetchone()

#     cur.close()
#     conn.close()

#     if not row:
#         return jsonify({"error": "User not found"}), 404

#     return jsonify({
#         "user_id": row[0],
#         "username": row[1],
#         "email": row[2],
#         "is_verified_human": row[3]
#     })

# @app.route("/user/<user_id>", methods=["PUT"])
# def update_user(user_id):
#     data = request.json
#     conn = get_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute("""
#             UPDATE webUser
#             SET username = %s,
#                 email = %s,
#                 is_verified_human = %s
#             WHERE user_id = %s
#         """, (data["username"], data["email"], data.get("is_verified_human"), user_id))

#         conn.commit()

#         if cur.rowcount == 0:
#             return jsonify({"error": "User not found"}), 404

#         return jsonify({"message": "User updated"})
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"error": str(e)}), 400
#     finally:
#         cur.close()
#         conn.close()

# @app.route("/user/<user_id>", methods=["DELETE"])
# def delete_user(user_id):
#     conn = get_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute("DELETE FROM webUser WHERE user_id = %s", (user_id,))
#         conn.commit()

#         if cur.rowcount == 0:
#             return jsonify({"error": "User not found"}), 404

#         return jsonify({"message": "User deleted"})
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"error": str(e)}), 400
#     finally:
#         cur.close()
#         conn.close()

# @app.route("/session", methods=["POST"])
# def create_session():
#     data = request.json
#     conn = get_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute("""
#             INSERT INTO sessions (session_id, user_id, ip_address, session_start_time, session_end_time, session_status)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (
#             data["session_id"],
#             data["user_id"],
#             data.get("ip_address"),
#             data.get("session_start_time"),
#             data.get("session_end_time"),
#             data.get("session_status")
#         ))

#         conn.commit()
#         return jsonify({"message": "Session created"}), 201
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"error": str(e)}), 400
#     finally:
#         cur.close()
#         conn.close()

# @app.route("/session/<session_id>", methods=["GET"])
# def get_session(session_id):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM sessions WHERE session_id = %s", (session_id,))
#     row = cur.fetchone()

#     cur.close()
#     conn.close()

#     if not row:
#         return jsonify({"error": "Session not found"}), 404

#     return jsonify({
#         "session_id": row[0],
#         "user_id": row[1],
#         "ip_address": row[2],
#         "session_start_time": row[3],
#         "session_end_time": row[4],
#         "session_status": row[5]
#     })