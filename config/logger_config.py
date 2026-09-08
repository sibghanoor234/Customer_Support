

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"), # File mein save karega
        logging.StreamHandler(sys.stdout)     # PyCharm Console par print karega
        ]
    )

logger = logging.getLogger(__name__)