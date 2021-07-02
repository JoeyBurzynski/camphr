"""
This type stub file was generated by pyright.
"""

from contextlib import contextmanager
from typing import (Any, Callable, Dict, Iterable, List, Optional, Pattern,
                    Sequence, Set, Tuple, Type, TypeVar, Union)

from spacy import pipeline, tokens
from spacy.gold import GoldParse
from spacy.pipeline.pipes import Pipe
from spacy.tokens.doc import Doc
from spacy.vocab import Vocab

ENABLE_PIPELINE_ANALYSIS = False
T = TypeVar("T")

class BaseDefaults(object):
    @classmethod
    def create_lemmatizer(
        cls, nlp: Optional[Any] = ..., lookups: Optional[Any] = ...
    ): ...
    @classmethod
    def create_lookups(cls, nlp: Optional[Any] = ...): ...
    @classmethod
    def create_vocab(cls, nlp: Optional[Any] = ...) -> Vocab: ...
    @classmethod
    def create_tokenizer(cls, nlp: Optional[Any] = ...): ...
    pipe_names: List[str]
    token_match: Pattern
    prefixes: Tuple
    suffixes: Tuple
    infixes: Tuple
    tag_map: Dict
    tokenizer_exceptions: Dict
    stop_words: Set
    morph_rules: Dict
    lex_attr_getters: Any
    syntax_iterators: Dict
    resources: Dict
    writing_system: Dict
    single_orth_variants: List
    paired_orth_variants: List

class Language(object):
    Defaults: Type[BaseDefaults]
    lang: str
    factories: Dict[str, Any]
    _meta: Dict[str, Any]
    pipeline: List[Tuple[str, Pipe]]
    @classmethod
    def factory(cls, name:str,default_config: Dict[str, Any] = {}, assigns: List[str] = [], requires: List[str] = [], retokenizes: bool=False) -> Callable[[T], T]: ...
    def __init__(
        self,
        vocab: bool = ...,
        make_doc: bool = ...,
        max_length=...,
        meta=...,
        **kwargs
    ):
        """Initialise a Language object.

        vocab (Vocab): A `Vocab` object. If `True`, a vocab is created via
            `Language.Defaults.create_vocab`.
        make_doc (callable): A function that takes text and returns a `Doc`
            object. Usually a `Tokenizer`.
        meta (dict): Custom meta data for the Language class. Is written to by
            models to add model meta data.
        max_length (int) :
            Maximum number of characters in a single text. The current v2 models
            may run out memory on extremely long texts, due to large internal
            allocations. You should segment these texts into meaningful units,
            e.g. paragraphs, subsections etc, before passing them to spaCy.
            Default maximum length is 1,000,000 characters (1mb). As a rule of
            thumb, if all pipeline components are enabled, spaCy's default
            models currently requires roughly 1GB of temporary memory per
            100,000 characters in one text.
        RETURNS (Language): The newly constructed object.
        """
        self.vocab: Vocab
        self.tokenizer: Callable[[str], Doc]
        self.max_length: int
    @property
    def path(self): ...
    @property
    def meta(self): ...
    @meta.setter
    def meta(self, value): ...
    @property
    def tensorizer(self): ...
    @property
    def tagger(self): ...
    @property
    def parser(self): ...
    @property
    def entity(self): ...
    @property
    def linker(self): ...
    @property
    def matcher(self): ...
    @property
    def pipe_names(self):
        """Get names of available pipeline components.

        RETURNS (list): List of component name strings, in order.
        """
        ...
    @property
    def pipe_factories(self):
        """Get the component factories for the available pipeline components.

        RETURNS (dict): Factory names, keyed by component names.
        """
        ...
    @property
    def pipe_labels(self):
        """Get the labels set by the pipeline components, if available (if
        the component exposes a labels property).

        RETURNS (dict): Labels keyed by component name.
        """
        ...
    def get_pipe(self, name):
        """Get a pipeline component for a given component name.

        name (unicode): Name of pipeline component to get.
        RETURNS (callable): The pipeline component.

        DOCS: https://spacy.io/api/language#get_pipe
        """
        ...
    def create_pipe(self, name: str, config: Any=...) -> Pipe:
        """Create a pipeline component from a factory.

        name (unicode): Factory name to look up in `Language.factories`.
        config (dict): Configuration parameters to initialise component.
        RETURNS (callable): Pipeline component.

        DOCS: https://spacy.io/api/language#create_pipe
        """
        ...
    def add_pipe(
        self,
        component: Callable[[Doc], Doc],
        name: Optional[Any] = ...,
        before: Optional[Any] = ...,
        after: Optional[Any] = ...,
        first: Optional[Any] = ...,
        last: Optional[Any] = ...,
    ) -> None:
        """Add a component to the processing pipeline. Valid components are
        callables that take a `Doc` object, modify it and return it. Only one
        of before/after/first/last can be set. Default behaviour is "last".

        component (callable): The pipeline component.
        name (unicode): Name of pipeline component. Overwrites existing
            component.name attribute if available. If no name is set and
            the component exposes no name attribute, component.__name__ is
            used. An error is raised if a name already exists in the pipeline.
        before (unicode): Component name to insert component directly before.
        after (unicode): Component name to insert component directly after.
        first (bool): Insert component first / not first in the pipeline.
        last (bool): Insert component last / not last in the pipeline.

        DOCS: https://spacy.io/api/language#add_pipe
        """
        ...
    def has_pipe(self, name):
        """Check if a component name is present in the pipeline. Equivalent to
        `name in nlp.pipe_names`.

        name (unicode): Name of the component.
        RETURNS (bool): Whether a component of the name exists in the pipeline.

        DOCS: https://spacy.io/api/language#has_pipe
        """
        ...
    def replace_pipe(self, name, component):
        """Replace a component in the pipeline.

        name (unicode): Name of the component to replace.
        component (callable): Pipeline component.

        DOCS: https://spacy.io/api/language#replace_pipe
        """
        ...
    def rename_pipe(self, old_name, new_name):
        """Rename a pipeline component.

        old_name (unicode): Name of the component to rename.
        new_name (unicode): New name of the component.

        DOCS: https://spacy.io/api/language#rename_pipe
        """
        ...
    def remove_pipe(self, name):
        """Remove a component from the pipeline.

        name (unicode): Name of the component to remove.
        RETURNS (tuple): A `(name, component)` tuple of the removed component.

        DOCS: https://spacy.io/api/language#remove_pipe
        """
        ...
    def __call__(
        self, text, disable=..., component_cfg: Optional[Any] = ...
    ) -> tokens.Doc:
        """Apply the pipeline to some text. The text can span multiple sentences,
        and can contain arbtrary whitespace. Alignment into the original string
        is preserved.

        text (unicode): The text to be processed.
        disable (list): Names of the pipeline components to disable.
        component_cfg (dict): An optional dictionary with extra keyword arguments
            for specific components.
        RETURNS (Doc): A container for accessing the annotations.

        DOCS: https://spacy.io/api/language#call
        """
        ...
    def disable_pipes(self, *names):
        """Disable one or more pipeline components. If used as a context
        manager, the pipeline will be restored to the initial state at the end
        of the block. Otherwise, a DisabledPipes object is returned, that has
        a `.restore()` method you can use to undo your changes.

        DOCS: https://spacy.io/api/language#disable_pipes
        """
        ...
    def make_doc(self, text): ...
    def _format_docs_and_golds(
        self,
        docs: Iterable[Union[str, Doc]],
        golds: Iterable[Union[Dict[str, Any], GoldParse]],
    ): ...
    def update(
        self,
        docs,
        golds,
        drop=...,
        sgd: Optional[Any] = ...,
        losses: Optional[Any] = ...,
        component_cfg: Optional[Any] = ...,
    ):
        """Update the models in the pipeline.

        docs (iterable): A batch of `Doc` objects.
        golds (iterable): A batch of `GoldParse` objects.
        drop (float): The dropout rate.
        sgd (callable): An optimizer.
        losses (dict): Dictionary to update with the loss, keyed by component.
        component_cfg (dict): Config parameters for specific pipeline
            components, keyed by component name.

        DOCS: https://spacy.io/api/language#update
        """
        ...
    def rehearse(
        self,
        docs,
        sgd: Optional[Any] = ...,
        losses: Optional[Any] = ...,
        config: Optional[Any] = ...,
    ):
        """Make a "rehearsal" update to the models in the pipeline, to prevent
        forgetting. Rehearsal updates run an initial copy of the model over some
        data, and update the model so its current predictions are more like the
        initial ones. This is useful for keeping a pretrained model on-track,
        even if you're updating it with a smaller set of examples.

        docs (iterable): A batch of `Doc` objects.
        drop (float): The dropout rate.
        sgd (callable): An optimizer.
        RETURNS (dict): Results from the update.

        EXAMPLE:
            >>> raw_text_batches = minibatch(raw_texts)
            >>> for labelled_batch in minibatch(zip(train_docs, train_golds)):
            >>>     docs, golds = zip(*train_docs)
            >>>     nlp.update(docs, golds)
            >>>     raw_batch = [nlp.make_doc(text) for text in next(raw_text_batches)]
            >>>     nlp.rehearse(raw_batch)
        """
        ...
    def preprocess_gold(self, docs_golds):
        """Can be called before training to pre-process gold data. By default,
        it handles nonprojectivity and adds missing tags to the tag map.

        docs_golds (iterable): Tuples of `Doc` and `GoldParse` objects.
        YIELDS (tuple): Tuples of preprocessed `Doc` and `GoldParse` objects.
        """
        ...
    def begin_training(
        self,
        get_gold_tuples: Optional[Any] = ...,
        sgd: Optional[Any] = ...,
        component_cfg: Optional[Any] = ...,
        **cfg
    ):
        """Allocate models, pre-process training data and acquire a trainer and
        optimizer. Used as a contextmanager.

        get_gold_tuples (function): Function returning gold data
        component_cfg (dict): Config parameters for specific components.
        **cfg: Config parameters.
        RETURNS: An optimizer.

        DOCS: https://spacy.io/api/language#begin_training
        """
        ...
    def resume_training(self, sgd: Optional[Any] = ..., **cfg):
        """Continue training a pretrained model.

        Create and return an optimizer, and initialize "rehearsal" for any pipeline
        component that has a .rehearse() method. Rehearsal is used to prevent
        models from "forgetting" their initialised "knowledge". To perform
        rehearsal, collect samples of text you want the models to retain performance
        on, and call nlp.rehearse() with a batch of Doc objects.
        """
        ...
    def evaluate(
        self,
        docs_golds,
        verbose: bool = ...,
        batch_size=...,
        scorer: Optional[Any] = ...,
        component_cfg: Optional[Any] = ...,
    ):
        """Evaluate a model's pipeline components.

        docs_golds (iterable): Tuples of `Doc` and `GoldParse` objects.
        verbose (bool): Print debugging information.
        batch_size (int): Batch size to use.
        scorer (Scorer): Optional `Scorer` to use. If not passed in, a new one
            will be created.
        component_cfg (dict): An optional dictionary with extra keyword
            arguments for specific components.
        RETURNS (Scorer): The scorer containing the evaluation results.

        DOCS: https://spacy.io/api/language#evaluate
        """
        ...
    @contextmanager
    def use_params(self, params, **cfg):
        """Replace weights of models in the pipeline with those provided in the
        params dictionary. Can be used as a contextmanager, in which case,
        models go back to their original weights after the block.

        params (dict): A dictionary of parameters keyed by model ID.
        **cfg: Config parameters.

        EXAMPLE:
            >>> with nlp.use_params(optimizer.averages):
            >>>     nlp.to_disk('/tmp/checkpoint')
        """
        ...
    def pipe(
        self,
        texts,
        as_tuples: bool = ...,
        n_threads=...,
        batch_size=...,
        disable=...,
        cleanup: bool = ...,
        component_cfg: Optional[Any] = ...,
        n_process=...,
    ):
        """Process texts as a stream, and yield `Doc` objects in order.

        texts (iterator): A sequence of texts to process.
        as_tuples (bool): If set to True, inputs should be a sequence of
            (text, context) tuples. Output will then be a sequence of
            (doc, context) tuples. Defaults to False.
        batch_size (int): The number of texts to buffer.
        disable (list): Names of the pipeline components to disable.
        cleanup (bool): If True, unneeded strings are freed to control memory
            use. Experimental.
        component_cfg (dict): An optional dictionary with extra keyword
            arguments for specific components.
        n_process (int): Number of processors to process texts, only supported
            in Python3. If -1, set `multiprocessing.cpu_count()`.
        YIELDS (Doc): Documents in the order of the original text.

        DOCS: https://spacy.io/api/language#pipe
        """
        ...
    def _multiprocessing_pipe(self, texts, pipes, n_process, batch_size): ...
    def to_disk(self, path, exclude=..., disable: Optional[Any] = ...):
        """Save the current state to a directory.  If a model is loaded, this
        will include the model.

        path (unicode or Path): Path to a directory, which will be created if
            it doesn't exist.
        exclude (list): Names of components or serialization fields to exclude.

        DOCS: https://spacy.io/api/language#to_disk
        """
        ...
    def from_disk(self, path, exclude=..., disable: Optional[Any] = ...):
        """Loads state from a directory. Modifies the object in place and
        returns it. If the saved `Language` object contains a model, the
        model will be loaded.

        path (unicode or Path): A path to a directory.
        exclude (list): Names of components or serialization fields to exclude.
        RETURNS (Language): The modified `Language` object.

        DOCS: https://spacy.io/api/language#from_disk
        """
        ...
    def to_bytes(self, exclude=..., disable: Optional[Any] = ..., **kwargs):
        """Serialize the current state to a binary string.

        exclude (list): Names of components or serialization fields to exclude.
        RETURNS (bytes): The serialized form of the `Language` object.

        DOCS: https://spacy.io/api/language#to_bytes
        """
        ...
    def from_bytes(
        self, bytes_data, exclude=..., disable: Optional[Any] = ..., **kwargs
    ):
        """Load state from a binary string.

        bytes_data (bytes): The data to load from.
        exclude (list): Names of components or serialization fields to exclude.
        RETURNS (Language): The `Language` object.

        DOCS: https://spacy.io/api/language#from_bytes
        """
        ...

class component(object):
    """Decorator for pipeline components. Can decorate both function components
    and class components and will automatically register components in the
    Language.factories. If the component is a class and needs access to the
    nlp object or config parameters, it can expose a from_nlp classmethod
    that takes the nlp object and **cfg arguments and returns the initialized
    component.
    """

    def __init__(
        self, name: str = ..., assigns=..., requires=..., retokenizes: bool = ...
    ):
        """Decorate a pipeline component.

        name (unicode): Default component and factory name.
        assigns (list): Attributes assigned by component, e.g. `["token.pos"]`.
        requires (list): Attributes required by component, e.g. `["token.dep"]`.
        retokenizes (bool): Whether the component changes the tokenization.
        """
        self.name = ...
        self.assigns = ...
        self.requires = ...
        self.retokenizes = ...
    def __call__(self, *args, **kwargs): ...

def _fix_pretrained_vectors_name(nlp): ...

class DisabledPipes(list):
    """Manager for temporary pipeline disabling."""

    def __init__(self, nlp, *names):
        self.nlp = ...
        self.names = ...
        self.original_pipeline = ...
    def __enter__(self): ...
    def __exit__(self, *args): ...
    def restore(self):
        """Restore the pipeline to its state when DisabledPipes was created."""
        ...

def _pipe(docs, proc, kwargs): ...
def _apply_pipes(make_doc, pipes, reciever, sender):
    """Worker for Language.pipe

    receiver (multiprocessing.Connection): Pipe to receive text. Usually
        created by `multiprocessing.Pipe()`
    sender (multiprocessing.Connection): Pipe to send doc. Usually created by
        `multiprocessing.Pipe()`
    """
    ...

class _Sender:
    """Util for sending data to multiprocessing workers in Language.pipe"""

    def __init__(self, data, queues, chunk_size):
        self.data = ...
        self.queues = ...
        self.chunk_size = ...
        self.count = ...
    def send(self):
        """Send chunk_size items from self.data to channels."""
        ...
    def step(self):
        """Tell sender that comsumed one item.

        Data is sent to the workers after every chunk_size calls."""
        ...
