import json
from confluent_kafka import Producer

producer_config = {'bootstrap.servers': 'localhost:9092'}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for Order {msg.key()}: {err}")
    else:
        print(f"Delivered {msg.value().decode('utf-8')}")

def send_task_notification(task_title, user_id):
    notification = {
        'task_title': task_title,
        'user_id': user_id
    }
    value = json.dumps(notification).encode('utf-8')

    producer.produce(
        topic='task_notifications',
        value=value,
        callback=delivery_report
    )
    producer.flush()