import traceback

from loguru import logger

from src.const import STATUS as ST
from src.env import (ACCESS_KEY_ID, API_TOKEN, BUCKET, DOMAIN, EMAIL,
                     SECRET_ACCESS_KEY)
from src.process.build_wheel import BuildView
from src.process.extract import ExtractView


def run():
    try:
        exctract = ExtractView(domain=DOMAIN, api_token=API_TOKEN, email=EMAIL)
        exctract.process()
        build = BuildView()
    except Exception as error:
        logger.error(error)
        msg = traceback.format_exc()
        logger.error(msg)
        if exctract._status == ST.ONGOING:
            exctract._status = ST.FAIL
        else:
            build._status = ST.FAIL
    finally:
        build.process_leadtime()
        logger.info(f"Extract Status: {exctract._status}")
        logger.info(f"Build Status: {build._status}")


if __name__ == "__main__":
    run()
