from datetime import datetime
from settings import Config


class SessionLogger:
    def __init__(self, username):

        self.username = username

        self.time_in = datetime.now().strftime(Config.DATE_FORMAT)

        self.time_out = ""

    def close_session(self):

        self.time_out = datetime.now().strftime(Config.DATE_FORMAT)

        self._write_log()

    def _write_log(self):

        log_line = f"login {self.time_in} {self.time_out} {self.username}\n"


        with open(Config.LOG_FILE, "w", encoding="utf-8") as file:
            file.write(log_line)