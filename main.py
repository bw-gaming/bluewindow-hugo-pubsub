import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

def receive_messages_with_custom_attributes(project_id, subscription_id, timeout=None):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull_custom_attributes]

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received {message.data}.")
        if message.attributes:
            print("Attributes:")
            for key in message.attributes:
                value = message.attributes.get(key)
                print(f"{key}: {value}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
    # [END pubsub_subscriber_async_pull_custom_attributes]

if __name__ == "__main__":
    project_id = os.environ.get('PUBSUB_PROJECT')
    subscription_id = os.environ.get('PUBSUB_PUBLISH_SUBSCRIPTION')
    publish_topic_name = os.environ.get('PUBSUB_PUBLISH_TOPIC')
    notify_topic_name = os.environ.get('PUBSUB_NOTIFY_TOPIC')
    print(f"{os.environ}")
    print(f"project_id: {project_id} \nsubscription_id: {subscription_id}\publish_topic_name: {publish_topic_name}")
    receive_messages_with_custom_attributes(project_id, subscription_id, timeout=None)
