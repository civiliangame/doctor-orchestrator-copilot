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
  summary_text TEXT NOT NULL,
  md_file TEXT NOT NULL DEFAULT '',                  -- markdown chart file in seed/patients ('' = none)
  fhir_patient_id TEXT NOT NULL DEFAULT '',          -- FHIR Patient.id when ingested from a bundle
  meta_json TEXT NOT NULL DEFAULT '{}'               -- identity/encounter framing for renderers
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

-- == Patient Context Model — the living belief state the agentic harness     ==
-- == reasons over. Slots are PATIENT-scoped (the running status across all   ==
-- == sources); visit_slot_requirements marks which slots TODAY's visit needs ==
-- == and why. context_slots holds the CURRENT belief; context_ledger is the  ==
-- == append-only provenance trail behind every belief. Every ledger row      ==
-- == carries a typed source_ref pointing at the exact origin:                ==
-- ==   fhir:<record_id>#<ResourceType>/<id>[,<ResourceType>/<id>...]         ==
-- ==   fhir:<record_id>#longitudinal      (record-level summarized fact)     ==
-- ==   turn:<turn_id>                     (conversation turn + actor cols)   ==
-- ==   note:<date>:<author>               (clinical note)                    ==
-- ==   file:<md_file>                     (markdown chart file ingest)       ==
-- ==   agent:<name>[:<run>]               (async agent contribution)         ==
CREATE TABLE IF NOT EXISTS context_slots (
  id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL,
  key TEXT NOT NULL,                                 -- stable slot key, e.g. "chest_pain.radiation"
  label TEXT NOT NULL,                               -- human display label
  category TEXT NOT NULL DEFAULT 'clinical',         -- problem|history|medication|social|vital|lab|assessment|procedure|imaging|report|immunization|encounter|symptom|risk|logistics
  status TEXT NOT NULL DEFAULT 'missing',            -- known|uncertain|stale|contradicted|missing
  value TEXT NOT NULL DEFAULT '',                    -- current best value ('' when missing)
  confidence REAL NOT NULL DEFAULT 0.0,              -- 0..1
  current_ledger_id INTEGER,                         -- provenance pointer -> context_ledger.id
  updated_ts TEXT NOT NULL DEFAULT '',
  UNIQUE(patient_id, key)
);
CREATE TABLE IF NOT EXISTS visit_slot_requirements (
  id INTEGER PRIMARY KEY, visit_id INTEGER NOT NULL,
  slot_key TEXT NOT NULL,                            -- -> context_slots.key (patient of this visit)
  why_required TEXT NOT NULL DEFAULT '',             -- goal / guardrail that made it required
  UNIQUE(visit_id, slot_key)
);
CREATE TABLE IF NOT EXISTS context_ledger (
  id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL,
  visit_id INTEGER,                                  -- NULL for pre-visit sources (e.g. FHIR ingest)
  slot_id INTEGER,                                   -- NULL if it could not be matched to a slot
  slot_key TEXT NOT NULL DEFAULT '',
  value_written TEXT NOT NULL DEFAULT '',
  status_written TEXT NOT NULL DEFAULT '',
  confidence REAL NOT NULL DEFAULT 0.0,
  -- provenance / quality dimensions (this is the whole point of the ledger):
  source_kind TEXT NOT NULL,                         -- fhir|seed|speech|typed|image|measurement|inferred
  source_ref TEXT NOT NULL DEFAULT '',               -- typed pointer to the exact origin (grammar above)
  source_channel TEXT NOT NULL DEFAULT '',           -- fhir_bundle|seed|soniox|inject|image_upload|manual|compiler
  actor_role TEXT NOT NULL DEFAULT 'system',         -- patient|staff|clinician|nurse|ehr|system|intake_agent
  actor_id TEXT NOT NULL DEFAULT '',                 -- stable id of who: "patient", specialist name, agent
  actor_name TEXT NOT NULL DEFAULT '',               -- display name of who
  from_patient INTEGER NOT NULL DEFAULT 0,           -- did this originate from the patient?
  extracted_from_speech INTEGER NOT NULL DEFAULT 0,  -- pulled from live/transcribed speech (vs typed/seed)
  model TEXT NOT NULL DEFAULT '',                    -- model that asserted it, if inferred
  session_id INTEGER, node_id INTEGER, turn_id INTEGER,
  raw_quote TEXT NOT NULL DEFAULT '',                -- verbatim supporting text (the citation)
  ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS chart_files (
  id INTEGER PRIMARY KEY, visit_id INTEGER NOT NULL UNIQUE,
  path TEXT NOT NULL,
  content_hash TEXT NOT NULL DEFAULT '',             -- hash of the file MINUS the DOC-managed section
  last_synced_ts TEXT NOT NULL DEFAULT '',           -- last read (markdown -> PCM ingest)
  last_written_ts TEXT NOT NULL DEFAULT ''           -- last append (PCM -> markdown)
);
"""


def _table_columns(c: sqlite3.Connection, table: str) -> list[str]:
    return [r[1] for r in c.execute(f"PRAGMA table_info({table})").fetchall()]


def _migrate(c: sqlite3.Connection) -> None:
    """Bring pre-existing DBs up to the current schema.

    The PCM tables are DERIVED state (the chart is the source of truth), so the
    visit-scoped v1 tables are dropped and rebuilt patient-scoped; seed_all
    re-derives and re-seeds them on startup. patients gains columns in place.
    """
    slots_cols = _table_columns(c, "context_slots")
    if slots_cols and "patient_id" not in slots_cols:
        c.execute("DROP TABLE context_slots")
        c.execute("DROP TABLE IF EXISTS context_ledger")
    patient_cols = _table_columns(c, "patients")
    if patient_cols and "md_file" not in patient_cols:
        c.execute("ALTER TABLE patients ADD COLUMN md_file TEXT NOT NULL DEFAULT ''")
    if patient_cols and "fhir_patient_id" not in patient_cols:
        c.execute("ALTER TABLE patients ADD COLUMN fhir_patient_id TEXT NOT NULL DEFAULT ''")
        c.execute("ALTER TABLE patients ADD COLUMN meta_json TEXT NOT NULL DEFAULT '{}'")


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
        _migrate(conn())
        conn().executescript(SCHEMA)
        conn().commit()


def wipe_db() -> None:
    tables = [r["name"] for r in q("SELECT name FROM sqlite_master WHERE type='table'")]
    with _lock:
        for t in tables:
            conn().execute(f"DELETE FROM {t}")
        conn().execute("DELETE FROM sqlite_sequence") if "sqlite_sequence" in tables else None
        conn().commit()
