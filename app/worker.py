from pydantic.utils import import_string
from saq import Queue
from tortoise import Tortoise

from .core.config import settings
from .db.config import TORTOISE_ORM

BACKGROUND_FUNCTIONS = [
    "app.users.tasks.log_user_email",
    "app.services.email.send_email_task",
]
FUNCTIONS = [import_string(bg_func) for bg_func in BACKGROUND_FUNCTIONS]


async def startup(_: dict):
    """
    Binds a connection set to the db object.
    """
    await Tortoise.init(config=TORTOISE_ORM)


async def shutdown(_: dict):
    """
    Pops the bind on the db object.
    """
    await Tortoise.close_connections()


queue = Queue.from_url(settings.REDIS_URL)

settings = {
    "queue": queue,
    "functions": FUNCTIONS,
    "concurrency": 10,
    "startup": startup,
    "shutdown": shutdown,
}
