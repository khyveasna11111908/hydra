# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.core.structured_config_store import StructuredConfigStore
from dataclasses import dataclass
from omegaconf import MISSING, OmegaConf

from typing import Any


@dataclass
class ConfigWithoutGroup:
    group: bool = False


@dataclass
class Cifar10:
    name: str = "cifar10"
    path: str = "/datasets/cifar10"


@dataclass
class ImageNet:
    name: str = "imagenet"
    path: str = "/datasets/imagenet"


@dataclass
class ConfigWithoutExt:
    foo: str = "bar"


@dataclass
class Adam:
    type: str = "adam"
    lr: float = 0.1
    beta: float = 0.01


@dataclass
class Nesterov:
    type: str = "nesterov"
    lr: float = 0.001


@dataclass
class Optimizer:
    optimizer: Any = MISSING


store = StructuredConfigStore.instance()
store.add(path="", name="config_without_group", node=ConfigWithoutGroup)


store.mkdir(dir_path="dataset")
store.add(path="dataset", name="cifar10", node=OmegaConf.create({"dataset": Cifar10}))
store.add(path="dataset", name="imagenet", node=OmegaConf.create({"dataset": ImageNet}))
store.add(path="dataset", name="config_without_extension", node=ConfigWithoutExt)

store.mkdir(dir_path="optimizer")
store.add(path="optimizer", name="adam", node=Optimizer(optimizer=Adam))
store.add(path="optimizer", name="nesterov", node=Optimizer(optimizer=Nesterov))
