[program:pythonapp]
directory=#approot#
command=python3 main.py
autostart=true
autorestart=true
user=#user#
startretries=5
# Environment variables ensure that the application runs inside of the
# configured virtualenv.
environment=VIRTUAL_ENV="#venv#",PATH="#path#",HOME="#home#",USER="#user#",PUBSUB_PROJECT="#PUBSUB_PROJECT#",PUBSUB_PUBLISH_SUBSCRIPTION="#PUBSUB_PUBLISH_SUBSCRIPTION#",PUBSUB_PUBLISH_TOPIC="#PUBSUB_PUBLISH_TOPIC#",PUBSUB_NOTIFY_TOPIC="#PUBSUB_NOTIFY_TOPIC#",BUCKET_INPUT="#BUCKET_INPUT#",BUCKET_OUTPUT="#BUCKET_OUTPUT#",PUBLISH_SCRIPT="#PUBLISH_SCRIPT#"
stdout_syslog=true
stderr_syslog=true
 
