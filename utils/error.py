# This file is part of the jenius-mcp-smart-device project.
# This file constructs the error message for the project and return to LLM

import json
from utils.logger import logger

def error_json_msg(errorMsg):

    logger.error(errorMsg)

    json_result = dict()
    json_result['code'] = 299
    json_result['message'] = errorMsg
    json_result_str = json.dumps(json_result, ensure_ascii=False)

    return json_result_str