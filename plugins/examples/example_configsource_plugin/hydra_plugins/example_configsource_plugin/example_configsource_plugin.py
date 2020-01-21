# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Dict, List, Optional

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource


class ConfigSourceExample(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        super().__init__(provider=provider, path=path)
        self.configs: Dict[str, Dict[str, Any]] = {
            "config_without_group": {"group": False},
            "dataset/imagenet": {
                "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
            },
            "dataset/cifar10": {
                "dataset": {"name": "cifar10", "path": "/datasets/cifar10"}
            },
        }

    @staticmethod
    def scheme() -> str:
        return "example"

    def load_config(self, config_path: str) -> ConfigResult:
        if config_path not in self.configs:
            raise ConfigLoadError("Config not found : " + config_path)
        return ConfigResult(
            config=OmegaConf.create(self.configs[config_path]),
            path=f"{self.scheme()}://{self.path}",
            provider=self.provider,
        )

    def is_group(self, config_path: str) -> bool:
        groups = {
            "": True,
            "dataset": True,
            "optimizer": True,
            "dataset/imagenet": False,
            "not_found": False,
        }
        return groups[config_path]

    def is_config(self, config_path: str) -> bool:
        configs = {
            "": False,
            "dataset": True,
            "optimizer": False,
            "dataset/imagenet": True,
            "dataset/imagenet.yaml": True,
            "dataset/imagenet.foobar": False,
            "not_found": False,
        }
        return configs[config_path]

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:

        groups: Dict[str, List[str]] = {"": ["dataset", "optimizer"], "dataset": []}
        configs = {
            "": ["config_without_group", "dataset"],
            "dataset": ["cifar10", "imagenet"],
        }
        if results_filter is None:
            return sorted(groups[config_path] + configs[config_path])
        elif results_filter == ObjectType.GROUP:
            return groups[config_path]
        elif results_filter == ObjectType.CONFIG:
            return configs[config_path]
        else:
            raise ValueError()
