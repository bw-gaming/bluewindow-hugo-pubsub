import datetime
import json
import logging
import os
import subprocess

from concurrent.futures import TimeoutError
import google.cloud.logging
from google.cloud import pubsub_v1


class HugoRunner:
    def __init__(self, project_id, subscription_id, notification_topic, bucket_in, bucket_out, publish_script, timeout=None):
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.notification_topic = notification_topic
        self.bucket_in = bucket_in
        self.bucket_out = bucket_out
        self.publish_script = publish_script

        self.timeout = timeout

        self.publisher = pubsub_v1.PublisherClient()
        self.notification_topic_path = self.publisher.topic_path(
            project_id, notification_topic)

    def notify(self, payload, update):
        logging.info(f"Notify :{payload}, {update}.")

        _payload = {**payload, **update}

        data = json.dumps(_payload).encode("utf-8")

        notification = self.publisher.publish(
            self.notification_topic_path, data)
        logging.info(notification.result())

    def run_build(self, payload):
        buildId = payload['buildId']
        environment = payload['environment']
        website = payload['website']
        theme = payload['theme']

        output = subprocess.run(f'{self.publish_script} {environment} {website} {self.bucket_in} {self.bucket_out} {buildId} {theme}',
                                capture_output=True,
                                shell=True,
                                text=True,
                                executable='/bin/bash',
                                env={"PATH": "/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games"}
                                )
        return {
            'returncode': output.returncode,
            'stderr': output.stderr,
            'stdout': output.stdout,
            'args': output.args
        }

    def callback(self, message):
        try:
            logging.info(f"Received {message.data}.")

            message.ack()
            payload = json.loads(message.data)

            self.notify(payload, {'status': 'running'})
            result = self.run_build(payload)

            timestamp = int(datetime.datetime.now().timestamp() * 1000)

            self.notify(payload, {
                'output': result,
                'status': 'succeded' if result['returncode'] == 0 else 'failed',
                'endDate': timestamp
            })
        except Exception as ex:
            logging.error(ex)

    def receive_publish_request(self):
        subscriber = pubsub_v1.SubscriberClient()

        subscription_path = subscriber.subscription_path(
            self.project_id, self.subscription_id)

        streaming_pull_future = subscriber.subscribe(
            subscription_path, callback=self.callback)

        logging.info(f"Listening for messages on {subscription_path}..\n")
        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result(timeout=self.timeout)
            except TimeoutError:
                streaming_pull_future.cancel()


if __name__ == "__main__":

    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()

    project_id = os.environ.get('PUBSUB_PROJECT')
    subscription_id = os.environ.get('PUBSUB_PUBLISH_SUBSCRIPTION')
    publish_topic_name = os.environ.get('PUBSUB_PUBLISH_TOPIC')
    notify_topic_name = os.environ.get('PUBSUB_NOTIFY_TOPIC')
    bucket_in = os.environ.get('BUCKET_INPUT')
    bucket_out = os.environ.get('BUCKET_OUTPUT')
    publish_script = os.environ.get('PUBLISH_SCRIPT')

    runner = HugoRunner(project_id, subscription_id,
                        notify_topic_name, bucket_in, bucket_out, publish_script)

    logging.info(
        f"project_id: {project_id} \nsubscription_id: {subscription_id}\npublish_topic_name: {publish_topic_name}\nBucket in : {bucket_in}\nBucket out : {bucket_out}")

    runner.receive_publish_request()
    receive_publish_request(
        project_id, subscription_id, timeout=None)
