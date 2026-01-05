"""
Automated retraining trigger.

Uses MLflow to log retraining runs and invokes the retraining
shell script. Designed to be called by a scheduler (cron / Airflow)
or by the drift-detection module when data drift is detected.
"""

import logging
from datetime import datetime, timezone
from subprocess import run, CalledProcessError

from mlflow import start_run, log_metric, log_params

_logger = logging.getLogger(__name__)


def trigger_retraining(reason: str = "scheduled") -> bool:
    """
    Kick off a model retraining run.

    Args:
        reason: Why the retrain was triggered (e.g. 'scheduled',
                'drift_detected', 'manual').

    Returns:
        True if the retraining completed successfully, False otherwise.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    _logger.info("Retraining triggered — reason=%s, time=%s", reason, timestamp)

    with start_run(run_name=f"retrain-{reason}-{timestamp}"):
        log_params({"trigger_reason": reason, "started_at": timestamp})

        try:
            result = run(
                ["bash", "retraining/retrain.sh"],
                check=True,
                capture_output=True,
                text=True,
            )
            log_metric("retrain_success", 1)
            _logger.info("Retraining finished successfully")
            return True

        except CalledProcessError as exc:
            log_metric("retrain_success", 0)
            _logger.error("Retraining failed (exit %d): %s", exc.returncode, exc.stderr)
            return False

        except Exception as exc:
            log_metric("retrain_success", 0)
            _logger.exception("Unexpected error during retraining: %s", exc)
            return False
