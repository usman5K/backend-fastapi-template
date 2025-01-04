import json
import logging


class JSONExtraFormatter(logging.Formatter):
    """
    Custom formatter that adds JSON formatted extra data to log records.
    """

    def format(self, record):
        """
        Format the log record and add JSON formatted extra data to the log record.
        :param record: Log record to format. Must be a logging.LogRecord object.
        :return: Formatted log record with JSON formatted extra data.
        """
        # Combine all `extra` keys and values into a JSON string
        extra_keys = (
            set(record.__dict__.keys())
            - logging.LogRecord(
                "", logging.NOTSET, "", 0, "", (), None, ""
            ).__dict__.keys()
        )
        extra_data = {key: record.__dict__[key] for key in extra_keys}
        record.extra_json = json.dumps(extra_data, separators=(",", ":"))

        return super().format(record)


logger = logging.getLogger("Application Logs")

handler = logging.StreamHandler()
handler.setFormatter(
    JSONExtraFormatter("%(asctime)s - %(levelname)s - %(message)s - %(extra_json)s")
)
logger.addHandler(handler)
