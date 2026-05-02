from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

redis_url = os.getenv("REDIS_URL")

celery_app = Celery("app", broker=redis_url, backend=redis_url)






