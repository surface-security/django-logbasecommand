# django-logbasecommand

Minimal package to add logging helpers to Django management commands

## Usage

Replace

```
from django.core.management.base import BaseCommand

class YourCommand(BaseCommand):
```

with

```
from logbasecommand.base import LogBaseCommand

class LogBaseCommand(BaseCommand):
```

and now you can use the drop-in methods to replace `self.stdout`/`self.stderr`:
* `log`
* `log_debug`
* `log_warning`
* `log_error`
* `log_exception`

Or access `self.logger` directly.


All command logger names are derived from the command module name and prefixed with `logbasecommand.base` (by default, use `LOGBASECOMMAND_PREFIX` setting to change it), so logging can be configured from your project settings.py, with `LOGGING`, ie (full example, check the `loggers` part):

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'},
    },
    'formatters': {
        'verbose': {'format': '[%(asctime)s] [%(process)s] [%(levelname)s] [%(name)s] %(message)s'},
        'minimal': {'format': '[%(levelname)s] [%(name)s] %(message)s'},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'console_minimal': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'minimal',
        },
        'console_debug_minimal': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'minimal',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        '': {'handlers': ['console', 'console_debug'], 'level': 'INFO', 'propagate': True},
        'logbasecommand.base': {
            'handlers': ['console_minimal', 'console_debug_minimal'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```