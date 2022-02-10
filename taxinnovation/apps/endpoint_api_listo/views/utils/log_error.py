import google.cloud.logging
import logging
# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.get_default_handler()
client.setup_logging()


def logger(exception):
    # Iniciamos cliente para logging
    logging.error(exception, exc_info=True)
