from logbasecommand.base import LogBaseCommand


class Command(LogBaseCommand):
    def handle(self, *args, **options):
        self.log('info message')
        self.log_debug('debug message')
        self.log_error('error message')
        try:
            1 / 0
        except ZeroDivisionError:
            self.log_exception('exception handled')
