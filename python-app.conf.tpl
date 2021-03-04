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
stdout_logfile=#approot#/logs/pubsublogs
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
stderr_logfile=#approot#/logs/pubsublogs
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stderr_events_enabled=false
 
