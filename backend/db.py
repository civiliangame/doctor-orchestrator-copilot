"""SQLite layer. One module-level connection, WAL mode, dict rows.

Schema mirrors SPEC.md § Data model; JSON shapes in API_CONTRACT.md are built
from these rows by the route serializers.
"""

import json
import sqlite3
import threading
from datetime import datetime, timezone

from config import DB_PATH

_lock = threading.Lock()
_conn: sqlite3.Connection | None = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS patients (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, dob TEXT NOT NULL,
  phone TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL,
  title TEXT NOT NULL, doc_type TEXT NOT NULL, author TEXT NOT NULL,
  date TEXT NOT NULL, content_md TEXT NOT NULL
);  -- APPEND-ONLY: agents never rewrite the record (SPEC.md)
CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'analyzing',  -- analyzing|planning|calling|compiling|done|failed
  transport TEXT NOT NULL DEFAULT 'sim',     -- sim|telnyx
  started_ts TEXT NOT NULL, ended_ts TEXT
);
CREATE TABLE IF NOT EXISTS specialists (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL,
  key TEXT NOT NULL, display_name TEXT NOT NULL, rationale TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'running'     -- running|done
);
CREATE TABLE IF NOT EXISTS findings (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL,
  specialist_id INTEGER,                     -- NULL = discovered live on the call
  kind TEXT NOT NULL,                        -- contradiction|gap|ambiguity
  severity TEXT NOT NULL DEFAULT 'normal',   -- high|normal
  title TEXT NOT NULL, detail TEXT NOT NULL DEFAULT '',
  quotes_json TEXT NOT NULL DEFAULT '[]',    -- [{"doc_title":..,"quote":..}]
  patient_answerable INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL,
  finding_ids_json TEXT NOT NULL DEFAULT '[]',
  ord INTEGER NOT NULL,
  question TEXT NOT NULL, sub_questions_json TEXT NOT NULL DEFAULT '[]',
  completeness_criteria TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'pending'     -- pending|asking|answered|deferred
);
CREATE TABLE IF NOT EXISTS specialist_tasks (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL, finding_id INTEGER NOT NULL,
  for_specialist TEXT NOT NULL, instruction TEXT NOT NULL, why TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS calls (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL,
  transport TEXT NOT NULL,                   -- sim|telnyx
  telnyx_call_control_id TEXT,
  status TEXT NOT NULL DEFAULT 'dialing',    -- dialing|active|ended
  started_ts TEXT NOT NULL, ended_ts TEXT
);
CREATE TABLE IF NOT EXISTS call_turns (
  id INTEGER PRIMARY KEY, call_id INTEGER NOT NULL,
  speaker TEXT NOT NULL,                     -- agent|patient
  text TEXT NOT NULL, ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS answers (
  id INTEGER PRIMARY KEY, question_id INTEGER NOT NULL,
  summary_text TEXT NOT NULL, complete INTEGER NOT NULL DEFAULT 1, ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS intakes (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL,
  chief_complaint TEXT NOT NULL, hpi_md TEXT NOT NULL,
  meds_reconciliation_md TEXT NOT NULL DEFAULT '',
  resolved_contradictions_md TEXT NOT NULL DEFAULT '',
  open_items_md TEXT NOT NULL DEFAULT '',
  created_ts TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
    return _conn


def q(sql: str, params: tuple = ()) -> list[dict]:
    with _lock:
        rows = conn().execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def one(sql: str, params: tuple = ()) -> dict | None:
    rows = q(sql, params)
    return rows[0] if rows else None


def ex(sql: str, params: tuple = ()) -> int:
    """Execute + commit; returns lastrowid."""
    with _lock:
        cur = conn().execute(sql, params)
        conn().commit()
        return cur.lastrowid


def ins(table: str, **cols) -> int:
    keys = ", ".join(cols)
    ph = ", ".join("?" for _ in cols)
    return ex(f"INSERT INTO {table} ({keys}) VALUES ({ph})", tuple(cols.values()))


def jloads(s: str | None, default=None):
    if not s:
        return default if default is not None else []
    return json.loads(s)


def init_db() -> None:
    with _lock:
        conn().executescript(SCHEMA)
        conn().commit()


def wipe_db() -> None:
    tables = [r["name"] for r in q("SELECT name FROM sqlite_master WHERE type='table'")]
    with _lock:
        for t in tables:
            conn().execute(f"DELETE FROM {t}")
        conn().execute("DELETE FROM sqlite_sequence") if "sqlite_sequence" in tables else None
        conn().commit()
