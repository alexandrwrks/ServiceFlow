from taskiq import SimpleRetryMiddleware
from taskiq_aio_pika import AioPikaBroker

from utils.settings import settings

broker = AioPikaBroker(
    settings.RabbitMQ_URL
).with_middlewares(
    SimpleRetryMiddleware(default_retry_count=3)
)