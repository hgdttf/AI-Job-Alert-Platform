from apscheduler.schedulers.background import BackgroundScheduler

from backend.pipeline import run_pipeline

scheduler = BackgroundScheduler()

scheduler.add_job(
    run_pipeline,
    "interval",
    minutes=5,
    max_instances=1
)

scheduler.start()