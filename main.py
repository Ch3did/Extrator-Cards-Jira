import traceback

from loguru import logger

from src.const import STATUS as ST
from src.env import (ACCESS_KEY_ID, API_TOKEN, BUCKET, DOMAIN, EMAIL,
                     SECRET_ACCESS_KEY)
from src.views.build_wheel import BuildView
from src.views.extract import ExtractView


def main():
    try:
        exctract = ExtractView(domain=DOMAIN, api_token=API_TOKEN, email=EMAIL)
        exctract.process()
        build = BuildView(
            access_key_id=ACCESS_KEY_ID,
            secret_access_key=SECRET_ACCESS_KEY,
            bucket=BUCKET,
        )
    except Exception as error:
        logger.error(error)
        msg = traceback.format_exc()
        logger.error(msg)
        if exctract._status == ST.ONGOING:
            exctract._status = ST.FAIL
        else:
            build._status = ST.FAIL
    finally:
        build.process()
        build.plot_leadtime_graff()
        build.plot_evolution_graff()
        logger.info(f"Extract Status: {exctract._status}")
        logger.info(f"Build Status: {build._status}")


if __name__ == "__main__":
    main()
