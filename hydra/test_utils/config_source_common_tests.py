# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional, Type

import pytest

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigSource


class ConfigSourceTestSuite:
    @pytest.mark.parametrize(  # type: ignore
        "config_path, expected",
        [
            ("", True),
            ("dataset", True),
            ("optimizer", True),
            ("dataset/imagenet", False),
            ("not_found", False),
        ],
    )
    def test_is_group(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        expected: List[str],
    ) -> None:
        src = type_(provider="foo", path=path)
        ret = src.is_group(config_path=config_path)
        assert ret == expected

    @pytest.mark.parametrize(  # type: ignore
        "config_path, expected",
        [
            ("", False),
            ("dataset", True),
            ("optimizer", False),
            ("dataset/imagenet", True),
            ("dataset/imagenet.yaml", True),
            ("dataset/imagenet.foobar", False),
            ("not_found", False),
        ],
    )
    def test_is_config(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        expected: List[str],
    ) -> None:
        src = type_(provider="foo", path=path)
        ret = src.is_config(config_path=config_path)
        assert ret == expected

    @pytest.mark.parametrize(  # type: ignore
        "config_path,results_filter,expected",
        [
            # one dataset is config, and one is group
            ("", None, ["config_without_group", "dataset", "optimizer"]),
            ("", ObjectType.GROUP, ["dataset", "optimizer"]),
            ("", ObjectType.CONFIG, ["config_without_group", "dataset"]),
            ("dataset", None, ["cifar10", "imagenet"]),
            ("dataset", ObjectType.GROUP, []),
            ("dataset", ObjectType.CONFIG, ["cifar10", "imagenet"],),
        ],
    )
    def test_source_list(
        self,
        type_: Type[ConfigSource],
        path: str,
        config_path: str,
        results_filter: Optional[ObjectType],
        expected: List[str],
    ) -> None:
        src = type_(provider="foo", path=path)
        ret = src.list(config_path=config_path, results_filter=results_filter)
        assert ret == expected

    def test_source_load_config(self, type_: Type[ConfigSource], path: str) -> None:
        assert issubclass(type_, ConfigSource)
        src = type_(provider="foo", path=path)

        assert src.load_config(config_path="config_without_group").config == {
            "group": False
        }

        assert src.load_config(config_path="dataset/imagenet").config == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }

        assert src.load_config(config_path="dataset/cifar10").config == {
            "dataset": {"name": "cifar10", "path": "/datasets/cifar10"}
        }

        with pytest.raises(ConfigLoadError):
            src.load_config(config_path="dataset/not_found")
