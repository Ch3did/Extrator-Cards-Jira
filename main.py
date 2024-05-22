import traceback

from loguru import logger

from src.const import STATUS as ST
from src.env import API_TOKEN, DOMAIN, EMAIL
from src.process.build_wheel import BuildView
from src.process.extract import ExtractView


def run():
    exctract = ExtractView(domain=DOMAIN, api_token=API_TOKEN, email=EMAIL)
    build = BuildView()
    try:
        exctract.process()
        build.process_leadtime()
        build.process_velocity()
    except Exception as error:
        logger.error(error)
        msg = traceback.format_exc()
        logger.error(msg)
        if exctract._status == ST.ONGOING:
            exctract._status = ST.FAIL
        else:
            build._status = ST.FAIL
    finally:
        logger.info(f"Extract Status: {exctract._status}")
        logger.info(f"Build Status: {build._status}")


if __name__ == "__main__":
    run()
