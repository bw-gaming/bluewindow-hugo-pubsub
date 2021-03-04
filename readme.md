

Set appropriate variables to configure supervisor app properly

```bash
sudo sed -e "s=#approot#=$APP_ROOT=" \
 -e "s=#venv#=$APP_ENV=" \
 -e "s=#path#=$APP_ENV/bin=" \
 -e "s=#home#=/home/$APP_USER=" \
 -e "s=#user#=$APP_USER=g" \
 -e "s=#PUBSUB_PROJECT#=$PROJECT=" \
 -e "s=#PUBSUB_PUBLISH_SUBSCRIPTION#=$PUBSUB_PUBLISH_SUBSCRIPTION=" \
 -e "s=#PUBSUB_PUBLISH_TOPIC#=$PUBSUB_PUBLISH_TOPIC=" \
 -e "s=#PUBSUB_NOTIFY_TOPIC#=$PUBSUB_NOTIFY_TOPIC=" \
   python-app.conf.tpl > /etc/supervisor/conf.d/python-app.conf
```