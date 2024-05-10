import traceback

from loguru import logger

from src.env import (ACCESS_KEY_ID, API_TOKEN, BUCKET, DOMAIN, EMAIL,
                     SECRET_ACCESS_KEY)
from src.views.build_wheel import BuildView
from src.views.extract import ExtractView

if __name__ == "__main__":
    exctract = ExtractView(domain=DOMAIN, api_token=API_TOKEN, email=EMAIL)
    build = BuildView(
        access_key_id=ACCESS_KEY_ID, secret_access_key=SECRET_ACCESS_KEY, bucket=BUCKET
    )
    try:
        # exctract.process()
        build.process()
        build.plot_leadtime_graff()
        build.plot_evolution_graff()
    except Exception as error:
        logger.error(error)
        msg = traceback.format_exc()
        logger.error(msg)
        exctract._status = "Fail"
    finally:
        logger.info(f"Process has finished! Status: {exctract._status}")
