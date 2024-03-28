import logging

from django.core.management.base import (
    BaseCommand,
    CommandError,  # noqa - to make it on subclasses to import from only one place
)
from django.conf import settings


class LogBaseCommand(BaseCommand):
    verbosity = 1
    custom_stdout = False
    custom_stderr = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        prefix = getattr(settings, "LOGBASECOMMAND_PREFIX", None) or __name__
        self.logger = logging.getLogger(prefix + "." + self.__module__.split(".")[-1])

    def __handle_custom_std(self, ifstd, std, msg, *args):
        if ifstd:
            std.write(str(msg) if not args else msg % args)

    def __custom_stderr(self, msg, *args):
        self.__handle_custom_std(self.custom_stderr, self.stderr, msg, *args)

    def __custom_stdout(self, msg, *args):
        self.__handle_custom_std(self.custom_stdout, self.stdout, msg, *args)

    def log_debug(self, msg, *args, **kwargs):
        if self.verbosity >= 2:
            self.__custom_stdout(msg, *args)
        return self.logger.debug(msg, *args, **kwargs)

    def log(self, msg, *args, **kwargs):
        if self.logger.level <= logging.INFO:
            self.__custom_stdout(msg, *args)
        return self.logger.info(msg, *args, **kwargs)

    def log_warning(self, msg, *args, **kwargs):
        if self.logger.level <= logging.WARNING:
            self.__custom_stderr(msg, *args)
        return self.logger.warning(msg, *args, **kwargs)

    def log_error(self, msg, *args, **kwargs):
        if self.logger.level <= logging.ERROR:
            self.__custom_stderr(msg, *args)
        return self.logger.error(msg, *args, **kwargs)

    def log_exception(self, msg, *args, **kwargs):
        self.__custom_stderr(msg, *args)
        return self.logger.exception(msg, *args, **kwargs)

    def execute(self, *args, **options):
        self.verbosity = options["verbosity"]
        self.logger.setLevel(
            [
                logging.ERROR,
                logging.INFO,
                logging.WARNING,
                logging.DEBUG,
            ][self.verbosity]
        )

        if options.get("stdout") is not None:
            self.custom_stdout = True
        if options.get("stderr") is not None:
            self.custom_stderr = True

        super().execute(*args, **options)
