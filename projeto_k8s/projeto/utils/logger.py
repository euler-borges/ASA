import logging
import colorlog

# Configuração básica do logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))

logger = colorlog.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

