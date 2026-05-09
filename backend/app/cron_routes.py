from fastapi import APIRouter

from .job_service import process_scheduled_jobs

router = APIRouter()


# =========================
# CRON ENDPOINT
# =========================

@router.get("/run-job-check")
def run_job_check():

    process_scheduled_jobs()

    return {
        "message": "Scheduled job check completed"
    }