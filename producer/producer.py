import os
import signal
import sys
import random
import string

import boto3

# Specify the AWS default region or else code must fail
os.environ["AWS_DEFAULT_REGION"] = "us-east-2"
# Specify the endpoint URL for LocalStack
ENDPOINT_URL = os.getenv("LOCALSTACK_ENDPOINT", None)
if ENDPOINT_URL:
    os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"
    os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
# Specify worker queue or else code must fail
WORKER_QUEUE = os.getenv("WORKER_QUEUE", None)
# Create an SQS client with the specified endpoint
sqs = boto3.resource("sqs", endpoint_url=ENDPOINT_URL)
queue = sqs.get_queue_by_name(QueueName=WORKER_QUEUE)


def generate_random_message() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def send_message(queue):
    message = generate_random_message()
    queue.send_message(QueueUrl=queue.url, MessageBody=message)


def sigterm_handler(_signo, _frame):
    print("SIGTERM received, shutting down gracefully...")
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)

while True:
    send_message(queue)
