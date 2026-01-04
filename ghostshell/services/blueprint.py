
from typing import Optional
import yaml

from ghostshell.models.blueprint import Blueprint
from ghostshell.utils import get_blueprint_path
from ghostshell.logger import Logger


def load() -> Optional[Blueprint]:
    blueprint_path = get_blueprint_path()

    with open(blueprint_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return Blueprint(**data)


def save(blueprint: Blueprint) -> None:
    blueprint_path = get_blueprint_path()

    data = blueprint.model_dump()

    with open(blueprint_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def display(blueprint: Blueprint) -> None:
    Logger.success("Blueprint created!\n")

    Logger.bold("Voice:")
    Logger.info(f"{blueprint.voice}\n")

    Logger.bold("Target Audience:")
    Logger.info(f"{blueprint.target_audience}\n")

    Logger.bold("Core Philosophy:")
    Logger.info(f"{blueprint.core_philosophy}\n")

    Logger.dim(f"Full details saved to blueprint.yaml")
