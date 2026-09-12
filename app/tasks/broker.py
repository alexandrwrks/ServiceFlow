from taskiq import SimpleRetryMiddleware
from taskiq_aio_pika import AioPikaBroker


broker = AioPikaBroker(
    "amqp://guest:guest@localhost:5672/"
).with_middlewares(
    SimpleRetryMiddleware(default_retry_count=3)
)