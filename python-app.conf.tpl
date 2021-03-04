[program:pythonapp]
directory=#approot#
command=#approot#/env/bin/honcho start -f ./procfile pubsub
autostart=true
autorestart=true
user=#user#
# Environment variables ensure that the application runs inside of the
# configured virtualenv.
environment=VIRTUAL_ENV="#venv#",PATH="#path#",HOME="#home#",USER="#user#",PUBSUB_PROJECT="#PUBSUB_PROJECT#",PUBSUB_PUBLISH_SUBSCRIPTION="#PUBSUB_PUBLISH_SUBSCRIPTION#",PUBSUB_PUBLISH_TOPIC="#PUBSUB_PUBLISH_TOPIC#",PUBSUB_NOTIFY_TOPIC="#PUBSUB_NOTIFY_TOPIC#"
stdout_logfile=syslog
stderr_logfile=syslog
 
