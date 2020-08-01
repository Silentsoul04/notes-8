---

- https://docs.celeryproject.org/en/master/django/first-steps-with-django.html

```python
import os

from celery import Celery
from kombu import Exchange
from kombu import Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app_name = "%s_%s" % (os.getenv("CFGAPP", "app"), os.getenv("CFGENV", "feature"))
app = Celery(app_name)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.timezone = "Asia/Shanghai"
app.autodiscover_tasks(["apps.schedulers.tasks"])
app.conf.task_queues = (Queue(app_name, exchange=Exchange(app_name + "_exchange"), routing_key="default"),)
app.conf.task_default_queue = app_name
app.conf.task_default_exchange_type = "direct"
app.conf.task_default_routing_key = "default"

```
> namespace表示配置键值需要以`CELERY_`作为前缀


```shell script
# 启动命令
celery --app=apps.schedulers.tasks worker --loglevel=info -Ofair -Q app_feature -n app_feature
```

