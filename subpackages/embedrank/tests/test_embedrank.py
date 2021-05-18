import pytest
import spacy

from camphr.pipelines.embedrank import EMBEDRANK_KEYPHRASES, EmbedRank


@pytest.fixture(scope="module", params=["ja_mecab"])
def nlp(request, trf_name_or_path, device, nlp_trf_model):
    request.param
    _nlp = nlp_trf_model
    pipe = EmbedRank(vocab=_nlp.vocab)
    _nlp.add_pipe(pipe)
    _nlp.to(device)
    return _nlp


TEXTS = ["今日はいい天気だった"]


@pytest.mark.parametrize("text", TEXTS)
def test_embedrank(nlp, text):
    doc = nlp(text)
    assert doc._.get(EMBEDRANK_KEYPHRASES) is not None


def test_serialization(nlp, tmp_path):
    nlp.to_disk(tmp_path)
    nlp = spacy.load(tmp_path)
    text = "今日はいい天気だった"
    doc = nlp(text)
    assert doc._.get(EMBEDRANK_KEYPHRASES) is not None
