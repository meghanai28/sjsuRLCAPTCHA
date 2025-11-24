import psycopg2
from dotenv import load_dotenv, dotenv_values
import os


load_dotenv()
psql_password = os.getenv("PSQL_PASSWORD") #Update your .env file with PSQL_PASSWORD=insert_password_here

connection = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password=psql_password,
    port=5432
)

cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS webUser (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    is_verified_human BOOLEAN
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    ip_address TEXT,
    session_start_time TEXT,
    session_end_time TEXT,
    session_status TEXT,
    FOREIGN KEY (user_id) REFERENCES webUser(user_id)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS rl_experience (
    experience_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    state JSON,
    action_taken TEXT,
    reward REAL,
    next_state JSON,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS mouseDynamics (
    mouse_event_id TEXT PRIMARY KEY,
    movement_speed REAL,
    pause_duration REAL,
    honeypot_clicked BOOLEAN
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS keystrokeDynamics (
    keystroke_id TEXT PRIMARY KEY,
    typing_speed REAL
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS challengeCAPTCHA (
    challenge_id TEXT PRIMARY KEY,
    challenge_type TEXT,
    difficulty_level TEXT
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS s_mouse (
    session_id TEXT NOT NULL,
    mouse_event_id TEXT NOT NULL,
    PRIMARY KEY (session_id, mouse_event_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (mouse_event_id) REFERENCES mouseDynamics(mouse_event_id)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS s_keystroke (
    session_id TEXT NOT NULL,
    keystroke_id TEXT NOT NULL,
    PRIMARY KEY (session_id, keystroke_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (keystroke_id) REFERENCES keystrokeDynamics(keystroke_id)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS s_challenge (
    session_id TEXT NOT NULL,
    challenge_id TEXT NOT NULL,
    PRIMARY KEY (session_id, challenge_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (challenge_id) REFERENCES challengeCAPTCHA(challenge_id)
);
""")

connection.commit()

cursor.close()
connection.close()