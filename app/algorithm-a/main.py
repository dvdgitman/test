import os
import time
import json
import pika
import numpy as np

# Configuration from Environment Variables (injected via K8s Secrets)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD", "password")
QUEUE_IN = "audio-stream"
QUEUE_OUT = "features-stream"

def process_audio(audio_data):
    """
    Simulates complex audio processing (Algo A).
    In reality, this might use PyTorch/TensorFlow.
    """
    # Simulate CPU processing time
    time.sleep(0.1) 
    # Generate mock 'features'
    return {
        "timestamp": audio_data.get("timestamp", time.time()),
        "sensor_id": audio_data.get("sensor_id", "unknown"),
        "features": np.random.rand(5).tolist() # Mock feature vector
    }

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        print(f" [x] Received audio from sensor {data.get('sensor_id')}")

        # Process the data
        features = process_audio(data)

        # Publish to Features Stream
        ch.basic_publish(
            exchange='',
            routing_key=QUEUE_OUT,
            body=json.dumps(features),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ))
        print(f" [x] Sent features to {QUEUE_OUT}")

        # Acknowledge completion
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f" [!] Error processing message: {e}")
        # Negative Acknowledgement to requeue the message
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Declare queues to ensure they exist
            channel.queue_declare(queue=QUEUE_IN, durable=True)
            channel.queue_declare(queue=QUEUE_OUT, durable=True)

            # Quality of Service: Process 1 message at a time per pod
            channel.basic_qos(prefetch_count=1)
            
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.basic_consume(queue=QUEUE_IN, on_message_callback=callback)
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Connection failed, retrying in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    main()
