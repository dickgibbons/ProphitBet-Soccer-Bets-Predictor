import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from web.config import DATABASE_PATH

_lock = threading.Lock()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_conn():
    with _lock:
        conn = _connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_type TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT,
                progress REAL DEFAULT 0,
                payload_json TEXT,
                result_json TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS eval_filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                league_id TEXT NOT NULL,
                model_id TEXT NOT NULL,
                name TEXT NOT NULL,
                filter_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(league_id, model_id, name)
            );

            CREATE TABLE IF NOT EXISTS models_meta (
                league_id TEXT NOT NULL,
                model_id TEXT NOT NULL,
                model_type TEXT NOT NULL,
                target_type TEXT NOT NULL,
                metrics_json TEXT,
                created_at TEXT NOT NULL,
                PRIMARY KEY (league_id, model_id)
            );
            """
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job(job_type: str, payload: Dict[str, Any], message: str = "Queued") -> int:
    now = _now()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO jobs (job_type, status, message, progress, payload_json, created_at, updated_at)
            VALUES (?, 'queued', ?, 0, ?, ?, ?)
            """,
            (job_type, message, json.dumps(payload), now, now),
        )
        return int(cur.lastrowid)


def update_job(
    job_id: int,
    *,
    status: Optional[str] = None,
    message: Optional[str] = None,
    progress: Optional[float] = None,
    result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
) -> None:
    fields: List[str] = ["updated_at = ?"]
    values: List[Any] = [_now()]
    if status is not None:
        fields.append("status = ?")
        values.append(status)
    if message is not None:
        fields.append("message = ?")
        values.append(message)
    if progress is not None:
        fields.append("progress = ?")
        values.append(progress)
    if result is not None:
        fields.append("result_json = ?")
        values.append(json.dumps(result))
    if error is not None:
        fields.append("error = ?")
        values.append(error)
    values.append(job_id)
    with get_conn() as conn:
        conn.execute(f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?", values)


def get_job(job_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None


def list_jobs(limit: int = 50) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM jobs ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def save_eval_filter(league_id: str, model_id: str, name: str, filter_data: Dict[str, Any]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO eval_filters (league_id, model_id, name, filter_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(league_id, model_id, name) DO UPDATE SET
                filter_json = excluded.filter_json,
                created_at = excluded.created_at
            """,
            (league_id, model_id, name, json.dumps(filter_data), _now()),
        )


def list_eval_filters(league_id: str, model_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, name, filter_json, created_at
            FROM eval_filters
            WHERE league_id = ? AND model_id = ?
            ORDER BY name
            """,
            (league_id, model_id),
        ).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        item["filter"] = json.loads(item.pop("filter_json"))
        out.append(item)
    return out


def delete_eval_filter(filter_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM eval_filters WHERE id = ?", (filter_id,))


def upsert_model_meta(
    league_id: str,
    model_id: str,
    model_type: str,
    target_type: str,
    metrics: Optional[Dict[str, Any]] = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO models_meta (league_id, model_id, model_type, target_type, metrics_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(league_id, model_id) DO UPDATE SET
                model_type = excluded.model_type,
                target_type = excluded.target_type,
                metrics_json = excluded.metrics_json
            """,
            (
                league_id,
                model_id,
                model_type,
                target_type,
                json.dumps(metrics or {}),
                _now(),
            ),
        )


def list_model_meta(league_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT league_id, model_id, model_type, target_type, metrics_json, created_at
            FROM models_meta
            WHERE league_id = ?
            ORDER BY model_id
            """,
            (league_id,),
        ).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        item["metrics"] = json.loads(item.pop("metrics_json") or "{}")
        out.append(item)
    return out


def delete_model_meta(league_id: str, model_id: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM models_meta WHERE league_id = ? AND model_id = ?",
            (league_id, model_id),
        )


def delete_league_model_meta(league_id: str) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM models_meta WHERE league_id = ?", (league_id,))
        conn.execute("DELETE FROM eval_filters WHERE league_id = ?", (league_id,))
