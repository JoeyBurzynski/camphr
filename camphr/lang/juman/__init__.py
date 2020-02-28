"""The package juman defines Japanese spacy.Language with JUMAN tokenizer."""
from collections import namedtuple
from typing import Any, Callable, Dict, List, Optional, Type

from spacy.compat import copy_reg
from spacy.language import Language
from spacy.tokens import Doc, Token

from camphr.consts import JUMAN_LINES, KEY_FSTRING
from camphr.lang.stop_words import STOP_WORDS
from camphr.utils import (
    JumanMixin,
    SerializationMixin,
    get_juman_command,
    han_to_zen_normalize,
)

ShortUnitWord = namedtuple(
    "ShortUnitWord", ["surface", "lemma", "pos", "fstring", "space"]
)


class Tokenizer(JumanMixin, SerializationMixin):
    """Juman tokenizer

    Note:
        `spacy.Token._.fstring` is set. The Juman's output is stored into it during tokenizing.
    """

    serialization_fields = ["preprocessor", "juman_kwargs"]
    key_fstring = KEY_FSTRING

    @classmethod
    def install_extensions(cls):
        """See https://github.com/explosion/spacy-pytorch-transformers#extension-attributes."""
        Token.set_extension(cls.key_fstring, default=None, force=True)

    def __init__(
        self,
        cls: Type["Defaults"],
        nlp: Optional[Language] = None,
        juman_kwargs: Optional[Dict[str, str]] = None,
        preprocessor: Optional[Callable[[str], str]] = han_to_zen_normalize,
    ):
        """

        Args:
            juman_kwargs: passed to `pyknp.Juman.__init__`
            preprocessor: applied to text before tokenizing. `mojimoji.han_to_zen` is often used.
        """
        juman_kwargs = juman_kwargs or {}
        default_command = get_juman_command()
        assert default_command
        juman_kwargs.setdefault("command", default_command)

        self.vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        self.reset_tokenizer()
        self.juman_kwargs = juman_kwargs
        self.preprocessor = preprocessor

    def __call__(self, text: str) -> Doc:
        """Make doc from text. Juman's `fstring` is stored in `Token._.fstring`"""
        if self.preprocessor:
            text = self.preprocessor(text)
        juman_lines = self._juman_string(text)
        dtokens = self._detailed_tokens(juman_lines)
        doc = self._dtokens_to_doc(dtokens)
        doc.user_data[JUMAN_LINES] = juman_lines
        return doc

    def _dtokens_to_doc(self, dtokens: List[ShortUnitWord]) -> Doc:
        words = [x.surface for x in dtokens]
        spaces = [x.space for x in dtokens]
        doc = Doc(self.vocab, words=words, spaces=spaces)
        for token, dtoken in zip(doc, dtokens):
            token.lemma_ = dtoken.lemma
            token.tag_ = dtoken.pos
            token._.set(self.key_fstring, dtoken.fstring)
        doc.is_tagged = True
        return doc

    def _detailed_tokens(self, juman_lines: str) -> List[ShortUnitWord]:
        """Tokenize text with Juman and format the outputs for further processing"""
        from pyknp import MList

        ml = MList(juman_lines).mrph_list()
        words: List[ShortUnitWord] = []
        for m in ml:
            surface = m.midasi
            pos = m.hinsi + "," + m.bunrui
            lemma = m.genkei or surface
            words.append(ShortUnitWord(surface, lemma, pos, m.fstring, False))
        return words


# for pickling. see https://spacy.io/usage/adding-languages
class Defaults(Language.Defaults):  # type: ignore
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    stop_words = STOP_WORDS
    writing_system = {"direction": "ltr", "has_case": False, "has_letters": False}

    @classmethod
    def create_tokenizer(
        cls,
        nlp=None,
        juman_kwargs: Optional[Dict[str, Any]] = None,
        preprocessor: Optional[Callable[[str], str]] = None,
    ):
        return Tokenizer(cls, nlp, juman_kwargs=juman_kwargs, preprocessor=preprocessor)


class Japanese(Language):
    lang = "ja_juman"
    Defaults = Defaults

    def make_doc(self, text: str) -> Doc:
        return self.tokenizer(text)


# avoid pickling problem (see https://github.com/explosion/spaCy/issues/3191)
def pickle_japanese(instance):
    return Japanese, tuple()


copy_reg.pickle(Japanese, pickle_japanese)
Language.factories[Japanese.lang] = Japanese

# for lazy loading. see https://spacy.io/usage/adding-languages
__all__ = ["Japanese"]

Tokenizer.install_extensions()
