import platform
import torch
import openvino as ov

core = ov.Core()


def is_openvino_device(device: str) -> bool:
    if device.lower() == "cpu" or device.lower()[0] == "g" or device.lower()[0] == "n":
        return True
    else:
        return False


def get_device_name(device: str) -> str:
    if device == "cuda":
        default_gpu_index = torch.cuda.current_device()
        return torch.cuda.get_device_name(default_gpu_index)
    elif platform.system().lower() == "darwin":
        return platform.processor()
    elif is_openvino_device(device):
        return core.get_property(device.upper(), "FULL_DEVICE_NAME")
