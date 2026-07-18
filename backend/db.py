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
  summary_text TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS visits (
  id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL, date TEXT NOT NULL,
  intent_text TEXT NOT NULL DEFAULT '', plan_confirmed INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS journey_nodes (
  id INTEGER PRIMARY KEY, visit_id INTEGER NOT NULL, station TEXT NOT NULL,
  specialist_name TEXT NOT NULL, specialist_profile TEXT NOT NULL DEFAULT '',
  goals_json TEXT NOT NULL DEFAULT '[]',
  status TEXT NOT NULL DEFAULT 'pending',           -- done|active|pending
  position INTEGER NOT NULL, sched_time TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS journey_edges (
  id INTEGER PRIMARY KEY, visit_id INTEGER NOT NULL,
  from_node_id INTEGER NOT NULL, to_node_id INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS guardrails (
  id INTEGER PRIMARY KEY, visit_id INTEGER NOT NULL, num INTEGER NOT NULL,
  condition_text TEXT NOT NULL, action_text TEXT NOT NULL,
  proposed_insert_json TEXT                          -- NULL or {"station":..,"specialist_name":..,"specialist_profile":..,"before_station":..}
);
CREATE TABLE IF NOT EXISTS node_briefs (
  id INTEGER PRIMARY KEY, node_id INTEGER NOT NULL, from_node_id INTEGER NOT NULL,
  from_station TEXT NOT NULL, summary_md TEXT NOT NULL,
  action_items_json TEXT NOT NULL DEFAULT '[]',      -- [{"text":..,"priority":..}]
  created_ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY, node_id INTEGER NOT NULL,
  started_ts TEXT NOT NULL, ended_ts TEXT
);
CREATE TABLE IF NOT EXISTS transcript_turns (
  id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL,
  speaker TEXT NOT NULL,                             -- staff|patient
  text TEXT NOT NULL, ts TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT 'inject'              -- soniox|inject
);
CREATE TABLE IF NOT EXISTS suggestions (
  id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL,
  kind TEXT NOT NULL, text TEXT NOT NULL, reason TEXT NOT NULL DEFAULT '',
  priority TEXT NOT NULL DEFAULT 'normal', ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS guardrail_alerts (
  id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL, guardrail_id INTEGER NOT NULL,
  triggered_by TEXT NOT NULL, action TEXT NOT NULL, ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS contradictions (
  id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL,
  statement TEXT NOT NULL, conflicts_with TEXT NOT NULL,
  severity TEXT NOT NULL DEFAULT 'note', suggested_probe TEXT NOT NULL DEFAULT '',
  ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS chart_entries (
  id INTEGER PRIMARY KEY, visit_id INTEGER NOT NULL, node_id INTEGER NOT NULL,
  ts TEXT NOT NULL, category TEXT NOT NULL, text TEXT NOT NULL
);  -- APPEND-ONLY: no UPDATE or DELETE, ever (SPEC.md)
CREATE TABLE IF NOT EXISTS todos (
  id INTEGER PRIMARY KEY, visit_id INTEGER NOT NULL,
  created_by_node_id INTEGER NOT NULL, for_node_id INTEGER NOT NULL,
  text TEXT NOT NULL, priority TEXT NOT NULL DEFAULT 'normal',
  status TEXT NOT NULL DEFAULT 'open'                -- open|done
);
CREATE TABLE IF NOT EXISTS journey_mutations (
  id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL, guardrail_id INTEGER NOT NULL,
  description TEXT NOT NULL, insert_station TEXT NOT NULL,
  insert_specialist_name TEXT NOT NULL DEFAULT '',
  insert_specialist_profile TEXT NOT NULL DEFAULT '',
  before_node_id INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'proposed',           -- proposed|accepted|dismissed
  ts TEXT NOT NULL
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
