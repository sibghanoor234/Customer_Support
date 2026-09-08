import json
from config.logger_config import logger

def read_tickets_json_file():
    try:
        with open("tickets.json", "r") as f:
            try:
                tickets_list = json.load(f)
                logger.info(tickets_list)
            except Exception as e:
                logger.exception(str(e))# exception use kya error nhi q ky exception details dta hai ky eroor exactly kha hai
                return []
        return tickets_list
    except Exception as e:
        logger.exception(str(e))
        return []
