from confluent_kafka import Consumer
from django.core.mail import send_mail
from django.conf import settings
import json
import logging

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'notification-consumers',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)

consumer.subscribe(['task_notifications'])

def process_notification(self, payload):
        """Helper to handle the actual alert logic"""
        email = payload.get('user_email')
        task_name = payload.get('task_name')

        self.stdout.write(f"Processing: Sending email to {email} for task: {task_name}")

        send_mail(
            subject=f"New Task Assigned: {task_name}",
            message=f"Hi! A new task '{task_name}' has been assigned to you in the Smart Task System.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )


print("Consumer is running and subscribed to 'task_notifications' topic...")


try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        try:
            data = json.loads(msg.value().decode('utf-8'))
            event_type = data.get('event')
            payload = data.get('payload', {})

            if event_type == "TASK_CREATED":
                process_notification(payload)
                
        except Exception as e:
            print(f"Error processing message: {e}")
except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()

