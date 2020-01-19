# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from typing import List, Optional

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource


class FileConfigSource(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        if path.find("://") == -1:
            path = f"{self.scheme()}://{path}"
        super().__init__(provider=provider, path=path)

    @staticmethod
    def scheme() -> str:
        return "file"

    def _resolve(self, config_path: str) -> Optional[str]:
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        full_path_yaml = full_path + ".yaml"
        candidates = [full_path_yaml, full_path]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate

        return None

    def load_config(self, config_path: str) -> ConfigResult:
        full_path = self._resolve(config_path)
        if full_path is None:
            raise ConfigLoadError(f"FileConfigSource: Config not found : {config_path}")
        return ConfigResult(
            config=OmegaConf.load(full_path),
            path=f"{self.scheme()}://{self.path}",
            provider=self.provider,
        )

    def exists(self, config_path: str) -> bool:
        return self._resolve(config_path) is not None

    def get_type(self, config_path: str) -> ObjectType:
        full_path = self._resolve(config_path)
        if full_path is not None:
            if os.path.isdir(full_path):
                return ObjectType.GROUP
            else:
                return ObjectType.CONFIG
        else:
            return ObjectType.NOT_FOUND

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        files: List[str] = []
        full_path = os.path.realpath(os.path.join(self.path, config_path))
        for file in os.listdir(full_path):
            file_path = os.path.join(config_path, file)
            self._list_add_result(
                files=files,
                file_path=file_path,
                file_name=file,
                results_filter=results_filter,
            )

        return sorted(files)
