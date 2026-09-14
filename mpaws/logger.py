"""Logger configuration for mpaws."""

from conflog import Conflog


def init():
    """Initialize and return the mpaws logger.

    The logger is configured via :class:`conflog.Conflog` with an ``info``
    log level and a ``[mpaws] LEVEL message`` output format.

    :returns: A configured logger instance.
    :rtype: logging.Logger
    """
    cfl = Conflog(
        conf_dict={"level": "info", "format": "[mpaws] %(levelname)s %(message)s"}
    )
    return cfl.get_logger(__name__)
