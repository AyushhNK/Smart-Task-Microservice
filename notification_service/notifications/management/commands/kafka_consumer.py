from django.core.management.base import BaseCommand
from confluent_kafka import Consumer
import json
import signal
import sys


class Command(BaseCommand):
    help = "Kafka consumer for task notifications"

    def handle(self, *args, **options):
        consumer_config = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "notification-consumers",
            "auto.offset.reset": "earliest",
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe(["task_notifications"])

        self.stdout.write(
            self.style.SUCCESS(
                "Kafka Consumer started. Listening to 'task_notifications'..."
            )
        )

        # Graceful shutdown
        def shutdown(sig, frame):
            self.stdout.write(self.style.WARNING("Stopping Kafka consumer..."))
            consumer.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                self.stderr.write(f"Consumer error: {msg.error()}")
                continue

            try:
                data = json.loads(msg.value().decode("utf-8"))
                self.process_notification(data)

            except json.JSONDecodeError as e:
                self.stderr.write(f"Invalid JSON message: {e}")

            except Exception as e:
                self.stderr.write(f"Error processing message: {e}")

    def process_notification(self, data):
        """
        Handle notification logic
        """
        user_id = data.get("user_id")
        task_title = data.get("task_title")
        user_email = data.get("user_email")

        if not task_title or not user_email:
            self.stderr.write(f"Incomplete message: {data}")
            return

        self.stdout.write(
            f"Sending notification to {user_email} for task '{task_title}'"
        )

        # Example email logic (enable when ready)
        # send_mail(
        #     subject=f"New Task Assigned: {task_title}",
        #     message=f"A new task '{task_title}' has been assigned to you.",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[user_email],
        #     fail_silently=False,
        # )

        self.stdout.write(self.style.SUCCESS("Notification processed"))
