import json
from typing import Dict, List

from camphr_core.ner_labels.labels_ene import ALL_LABELS as enes
from camphr_core.ner_labels.labels_irex import ALL_LABELS as irexes
from camphr_core.ner_labels.utils import make_ner_labels
from camphr_test.utils import check_mecab, check_serialization
from camphr_torch.lang import TorchLanguage
import pytest
from spacy.language import Language
import torch
import yaml

from camphr_transformers.model import TRANSFORMERS_MODEL, TrfModel
from camphr_transformers.ner import _convert_goldner
from camphr_transformers.ner import (
    TRANSFORMERS_NER,
    TrfForNamedEntityRecognition,
    _convert_goldner,
    _create_target,
)
from camphr_transformers.tokenizer import TRANSFORMERS_TOKENIZER, TrfTokenizer
from camphr_transformers.tokenizer import TRANSFORMERS_TOKENIZER, TrfTokenizer
from tests.utils import BERT_JA_DIR, DATA_DIR
from tests.utils import BERT_JA_DIR, DATA_DIR

label_types = ["ene", "irex"]


@pytest.fixture(scope="module", params=label_types)
def label_type(request):
    return request.param


@pytest.fixture(scope="module")
def labels(label_type):
    if label_type == "ene":
        shortenes = [label.split("/")[-1] for label in enes]
        return make_ner_labels(shortenes)
    elif label_type == "irex":
        return make_ner_labels(irexes)
    else:
        raise ValueError


@pytest.fixture(scope="module")
def nlp(labels, lang, trf_name_or_path: str, device):
    _nlp = TorchLanguage(
        meta={"lang": lang},
        optimizer_config={"class": "torch.optim.SGD", "params": {"lr": 0.01}},
    )
    _nlp.add_pipe(TrfTokenizer.from_pretrained(_nlp.vocab, trf_name_or_path))
    _nlp.add_pipe(TrfModel.from_pretrained(_nlp.vocab, trf_name_or_path))
    _nlp.add_pipe(
        TrfForNamedEntityRecognition.from_pretrained(
            _nlp.vocab, trf_name_or_path, labels=labels
        )
    )
    _nlp.to(device)
    return _nlp


TESTCASE_ENE = [
    (
        "ＥＸＩＬＥのＡＴＳＵＳＨＩと中島美嘉が１４日ニューヨーク入り",
        {
            "entities": [
                (0, 5, "SHOW_ORGANIZATION"),
                (6, 13, "PERSON"),
                (14, 18, "PERSON"),
                (19, 22, "DATE"),
                (22, 28, "CITY"),
            ]
        },
    ),
    (
        "夏休み真っただ中の8月26日の夕方。",
        {"entities": [(0, 3, "DATE"), (9, 14, "DATE"), (15, 17, "TIME")]},
    ),
    ("。", {"entities": []}),
    (" おはよう", {"entities": []}),
    ("　おはよう", {"entities": []}),
    ("", {"entities": []}),
    ("\n\n\n", {"entities": []}),
]


@pytest.mark.parametrize("text,gold", TESTCASE_ENE)
def test_call(nlp: Language, text, gold, label_type):
    if label_type == "irex":
        pytest.skip("label type mismatch")
    nlp(text)


def test_update(nlp: Language, label_type):
    if label_type == "irex":
        pytest.skip("label type mismatch")
    optim = nlp.resume_training()
    nlp.update(*zip(*TESTCASE_ENE), optim)


@pytest.fixture(
    scope="module",
    params=["ner/ner-ene.json", "ner/ner-irex.json", "ner/ner-ene2.json"],
)
def example_gold(request, label_type):
    fname = request.param
    if label_type in fname:
        with (DATA_DIR / fname).open() as f:
            d = json.load(f)
        return d
    else:
        pytest.skip("label type mismatch")


@pytest.fixture(scope="module", params=["ner/ner-irex-long.json"])
def example_long(request, label_type, trf_name_or_path):
    fname = request.param
    if label_type in fname:
        with (DATA_DIR / fname).open() as f:
            d = json.load(f)
        return d
    else:
        pytest.skip()


def test_example_batch(nlp: Language, example_gold):
    texts, golds = zip(*example_gold)
    optim = nlp.resume_training()
    nlp.update(texts, golds, optim)


def test_example_batch_eval(nlp: Language, example_gold):
    score = nlp.evaluate(example_gold)
    assert score["loss"]


def test_serialization(nlp):
    check_serialization(nlp)


@pytest.mark.parametrize(
    "ners,length,dim", [([{1: "B-A", 2: "I-A", 3: "O", 5: "O"}], 7, 10)]
)
def test_create_target(ners: List[Dict[int, str]], length, dim):
    LABELS = ["-", "O", "B-A", "I-A", "B-B", "B-B"]
    label2id = {s: i for i, s in enumerate(LABELS)}
    logits = torch.empty(len(ners), length, dim)
    ignore_index = 0
    targets = _create_target(ners, logits, ignore_index, label2id)
    assert targets.shape == (len(ners), length)
    for ner, target in zip(ners, targets):
        idx = list(ner)
        labels = [label2id[s] for s in ner.values()]
        not_idx = [i for i in range(len(target)) if i not in idx]
        assert target[idx].tolist() == labels
        assert torch.all(target[not_idx] == ignore_index)


@pytest.mark.skipif(not check_mecab(), reason="mecab is required")
def test_kbeam_config(labels):
    k_beam = 111
    _nlp = TorchLanguage(
        meta={"lang": "ja_mecab"},
        optimizer_config={},
    )
    _nlp.add_pipe(TrfTokenizer.from_pretrained(_nlp.vocab, str(BERT_JA_DIR)))
    _nlp.add_pipe(TrfModel.from_pretrained(_nlp.vocab, str(BERT_JA_DIR)))
    _nlp.add_pipe(
        TrfForNamedEntityRecognition.from_pretrained(
            _nlp.vocab, str(BERT_JA_DIR), labels=labels, k_beam=k_beam
        )
    )
    ner = _nlp.get_pipe(TRANSFORMERS_NER)
    assert ner.k_beam == 111


@pytest.mark.parametrize(
    "ner_labels,alignments,expected",
    [
        (
            ["O", "B-FOO", "I-FOO", "-"],
            [[0, 1], [2, 3], [4], [5]],
            {0: "O", 1: "O", 2: "B-FOO", 3: "I-FOO", 4: "I-FOO", 5: "-"},
        ),
        (["U-FOO"], [[1, 2, 3]], {1: "B-FOO", 2: "I-FOO", 3: "I-FOO"}),
    ],
)
def test_convert_goldner(ner_labels, alignments, expected):
    assert expected == _convert_goldner(ner_labels, alignments)
