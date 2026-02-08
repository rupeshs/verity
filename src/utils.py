import platform
from loguru import logger
from device import get_device_name


def show_system_info(
    device: str,
    llm_provider: str,
):
    try:
        logger.info(f"Running on {platform.system()} platform")
        logger.info(f"OS: {platform.platform()}")
        if llm_provider.lower() == "openvino":
            logger.info(f"Device : {device.upper()}")
            logger.info(f"Processor : {get_device_name(device)}")
        else:
            logger.info(f"Processor: {platform.processor()}")
    except Exception as ex:
        logger.error(f"Error occurred while getting system information {ex}")
