from contextlib import contextmanager
import dataclasses
from typing import Any, Dict, Optional, Set, Type, TypeVar

from camphr_core.utils import resolve_alias
import dataclass_utils
import yaml

from camphr_pipelines.models import (
    ALIASES,
    LangConfig,
    NLPConfig,
    PIPELINE_ALIGNMENT,
    _add_required_pipes,
    _align_pipeline,
    correct_model_config,
    create_lang,
    create_model,
)
from camphr_torch.lang import TorchLanguage
from camphr_transformers.model import TRANSFORMERS_MODEL
from camphr_transformers.ner import TRANSFORMERS_NER
from camphr_transformers.seq_classification import TRANSFORMERS_SEQ_CLASSIFIER
from camphr_transformers.tokenizer import TRANSFORMERS_TOKENIZER
import pytest

from .utils import BERT_DIR

T = TypeVar("T")


def from_yml(kls: Type[T], yml: str) -> T:
    return dataclass_utils.into(yaml.safe_load(yml), kls)


def yml_to_nlpconfig(yml: str) -> NLPConfig:
    return from_yml(NLPConfig, yml)


@pytest.mark.parametrize(
    "yml",
    [
        """
    name: en
    """,
        """
    name: en
    torch: false
    """,
    ],
)
def test_create_nlp(yml: str):
    config = from_yml(LangConfig, yml)
    nlp = create_lang(config)
    assert not config.torch or isinstance(nlp, TorchLanguage)
    assert nlp.lang == config.name


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(
    "yml,modified,error",
    [
        (
            f"""
    lang:
        name: en
    pipeline:
        {TRANSFORMERS_NER}:
    """,
            None,
            pytest.raises(ValueError),
        ),
        (
            f"""
    lang:
        name: en
    pipeline:
        {TRANSFORMERS_NER}:
            trf_name_or_path: foo
            labels: ['-', 'O', 'I-Foo', 'B-Foo']
    """,
            f"""
    lang:
        name: en
        torch: true
    pipeline:
        {TRANSFORMERS_TOKENIZER}:
            trf_name_or_path: foo
        {TRANSFORMERS_MODEL}:
            trf_name_or_path: foo
        {TRANSFORMERS_NER}:
            trf_name_or_path: foo
            labels: ['-', 'O', 'I-Foo', 'B-Foo']
    """,
            does_not_raise(),
        ),
        (
            f"""
    lang:
        name: en
    pipeline:
        {TRANSFORMERS_NER}:
            trf_name_or_path: foo
            labels: ["Foo"]
    """,
            f"""
    lang:
        name: en
        torch: true
    pipeline:
        {TRANSFORMERS_TOKENIZER}:
            trf_name_or_path: foo
        {TRANSFORMERS_MODEL}:
            trf_name_or_path: foo
        {TRANSFORMERS_NER}:
            trf_name_or_path: foo
            labels: ['-', 'O', 'B-Foo','I-Foo']
    """,
            does_not_raise(),
        ),
    ],
)
def test_correct(yml: str, modified: Optional[str], error):
    cfg_dict = yaml.safe_load(yml)
    with error as e:
        cfg_dict = resolve_alias(ALIASES, cfg_dict)
        config = dataclass_utils.into(cfg_dict, NLPConfig)
        correct_model_config(config)
    if not e:
        assert modified
        assert config == dataclass_utils.into(yaml.safe_load(modified), NLPConfig)


@pytest.fixture(scope="session")
def inject_dummy():
    PIPELINE_ALIGNMENT["foo"] = ["bar", "baz"]


@pytest.mark.parametrize(
    "yml,modified",
    [
        (
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_NER}: {{}}
    """,
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_TOKENIZER}: {{}}
        {TRANSFORMERS_MODEL}: {{}}
        {TRANSFORMERS_NER}: {{}}
    """,
        ),
        (
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_MODEL}: {{}}
    """,
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_TOKENIZER}: {{}}
        {TRANSFORMERS_MODEL}: {{}}
    """,
        ),
        (
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_MODEL}: {{}}
        {TRANSFORMERS_TOKENIZER}: {{}}
    """,
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_TOKENIZER}: {{}}
        {TRANSFORMERS_MODEL}: {{}}
    """,
        ),
        (
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_NER}: {{}}
        {TRANSFORMERS_MODEL}: {{}}
        {TRANSFORMERS_TOKENIZER}: {{}}
    """,
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_TOKENIZER}: {{}}
        {TRANSFORMERS_MODEL}: {{}}
        {TRANSFORMERS_NER}: {{}}
    """,
        ),
        (
            """
    lang:
        name: ja
    pipeline:
        foo: {}
        baz: {}
    """,
            """
    lang:
        name: ja
    pipeline:
        bar: {}
        baz: {}
        foo: {}
    """,
        ),
    ],
)
def test_assign_and_align_pipeline(yml: str, modified: str, inject_dummy):
    config = yml_to_nlpconfig(yml)
    config = _add_required_pipes(config)
    config = _align_pipeline(config)
    assert config.pipeline == yml_to_nlpconfig(modified).pipeline


@pytest.mark.parametrize(
    "yml,modified",
    [
        (
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_NER}:
    pretrained: foo
    """,
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_TOKENIZER}: {{}}
        {TRANSFORMERS_MODEL}:
            trf_name_or_path: foo
        {TRANSFORMERS_NER}: {{}}
    pretrained: foo
    """,
        ),
        (
            """
    lang:
        name: ja
    ner_label: foo
    """,
            f"""
    lang:
        name: ja
    pipeline:
        {TRANSFORMERS_TOKENIZER}: {{}}
        {TRANSFORMERS_MODEL}:
        {TRANSFORMERS_NER}: {{}}
    ner_label: foo
    """,
        ),
    ],
)
def test_align_pipeline_and_alias(yml: str, modified: str):
    config_dict = yaml.safe_load(yml)
    config_dict: Dict[str, Any] = resolve_alias(ALIASES, config_dict)  # type: ignore
    config = dataclass_utils.into(config_dict, NLPConfig)
    config = _add_required_pipes(config)
    config = _align_pipeline(config)

    expected = dataclass_utils.into(yaml.safe_load(modified), NLPConfig)
    assert list(config.pipeline) == list(expected.pipeline)


@pytest.mark.parametrize(
    "yml,pipe",
    [
        (
            f"""
    lang:
        name: en
    task: textcat
    labels: ["a", "b", "c"]
    pretrained: {BERT_DIR}
    optimizer: {{}}
    """,
            TRANSFORMERS_SEQ_CLASSIFIER,
        ),
        (
            f"""
    lang:
        name: en
    task: ner
    labels: ["a", "b", "c"]
    pretrained: {BERT_DIR}
    optimizer: {{}}
    """,
            TRANSFORMERS_NER,
        ),
    ],
)
def test_add_pipes_parser(yml, pipe):
    nlp = create_model(yml)
    assert nlp.get_pipe(pipe)
