import json
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional

from web import db

logger = logging.getLogger(__name__)

_executor = ThreadPoolExecutor(max_workers=1)


def enqueue(job_type: str, payload: Dict[str, Any], handler: Callable[[int, Dict[str, Any]], Dict[str, Any]], message: str = "Queued") -> int:
    job_id = db.create_job(job_type=job_type, payload=payload, message=message)

    def _run():
        db.update_job(job_id, status="running", message="Starting...", progress=0.05)
        try:
            result = handler(job_id, payload)
            db.update_job(
                job_id,
                status="completed",
                message="Done",
                progress=1.0,
                result=result or {},
            )
        except Exception as exc:
            logger.exception("Job %s failed", job_id)
            db.update_job(
                job_id,
                status="failed",
                message="Failed",
                error=f"{exc}\n{traceback.format_exc()}",
                progress=1.0,
            )

    _executor.submit(_run)
    return job_id


def job_view(job_id: int) -> Optional[Dict[str, Any]]:
    job = db.get_job(job_id)
    if not job:
        return None
    for key in ("payload_json", "result_json"):
        raw = job.get(key)
        if raw:
            try:
                job[key.replace("_json", "")] = json.loads(raw)
            except json.JSONDecodeError:
                job[key.replace("_json", "")] = None
        else:
            job[key.replace("_json", "")] = None
    return job
