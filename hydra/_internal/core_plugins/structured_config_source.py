# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from typing import List
from typing import Optional
import importlib

from hydra.core.object_type import ObjectType
from hydra.core.structured_config_store import StructuredConfigStore
from hydra.plugins.config_source import ConfigSource, ConfigResult


class StructuredConfigSource(ConfigSource):
    def __init__(self, provider: str, path: str) -> None:
        super().__init__(provider=provider, path=path)
        # Import the module, the __init__ there is expected to register the configs.
        importlib.import_module(self.path)

    @staticmethod
    def scheme() -> str:
        return "structured"

    def load_config(self, config_path: str) -> ConfigResult:
        return ConfigResult(
            config=StructuredConfigStore.instance().load(config_path=config_path),
            path=f"{self.scheme()}://{self.path}",
            provider=self.provider,
        )

    def exists(self, config_path: str) -> bool:
        return self.get_type(config_path) is not ObjectType.NOT_FOUND

    def get_type(self, config_path: str) -> ObjectType:
        return StructuredConfigStore.instance().get_type(config_path)

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        ret: List[str] = []
        files = StructuredConfigStore.instance().list(config_path)

        for file in files:
            self._list_add_result(
                files=ret,
                file_path=f"{config_path}/{file}",
                file_name=file,
                results_filter=results_filter,
            )
        return ret
