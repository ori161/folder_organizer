# imports

import logging


# --- Configure Logger ---
def setup_logger():
    logger = logging.getLogger("FileOrganizerLogger")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Formatter for log messages
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 1. File Handler
        file_handler = logging.FileHandler("organizer.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # 2. Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
