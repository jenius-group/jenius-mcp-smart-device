import logging
import colorlog
from colorlog import ColoredFormatter

# # 配置日志
# logging.basicConfig(
#     level=logging.INFO,
#     format='[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s'
# )

# # 创建全局日志记录器
# logger = logging.getLogger(__name__)

COLOR_RESET = '\033[0m'
COLOR_TIME = '\033[36m'
COLOR_NAME = '\033[35m'
COLOR_LEVEL = '\033[33m'
COLOR_MESSAGE = '\033[37m'

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = colorlog.ColoredFormatter(
        fmt=(
            f"{COLOR_TIME}[%(asctime)s]{COLOR_RESET} "
            f"{COLOR_NAME}[%(name)s]{COLOR_RESET} "
            f"%(log_color)s[%(levelname)s]{COLOR_RESET} "
            f"{COLOR_MESSAGE}%(message)s{COLOR_RESET}"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )

    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


logger = get_logger(__name__)