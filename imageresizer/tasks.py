"""
Schedule tasks related to the image resizer
"""
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from imageresizer import purge

from imageresizer.repository.database import SessionLocal

app = Celery("tasks", broker="redis://localhost:6379/0")
logger = get_task_logger(__name__)


@app.on_after_configure.connect
# pylint: disable=unused-argument
def setup_periodic_tasks(sender, **kwargs):
    """
    Schedules our tasks
    """
    sender.add_periodic_task(
        crontab(hour=2, minute=20),
        purge_data.s(),
        name="purge data",
    )


@app.task(track_started=True)
def purge_data():
    """
    Scheduled task to purge the db
    """
    with SessionLocal() as session:
        purge.purge_old_images(session)
