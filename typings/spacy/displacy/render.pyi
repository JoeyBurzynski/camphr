"""
This type stub file was generated by pyright.
"""

DEFAULT_LANG = "en"
DEFAULT_DIR = "ltr"

class DependencyRenderer(object):
    """Render dependency parses as SVGs."""

    style = ...
    def __init__(self, options=...):
        """Initialise dependency renderer.

        options (dict): Visualiser-specific options (compact, word_spacing,
            arrow_spacing, arrow_width, arrow_stroke, distance, offset_x,
            color, bg, font)
        """
        self.compact = ...
        self.word_spacing = ...
        self.arrow_spacing = ...
        self.arrow_width = ...
        self.arrow_stroke = ...
        self.distance = ...
        self.offset_x = ...
        self.color = ...
        self.bg = ...
        self.font = ...
        self.direction = ...
        self.lang = ...
    def render(self, parsed, page: bool = ..., minify: bool = ...):
        """Render complete markup.

        parsed (list): Dependency parses to render.
        page (bool): Render parses wrapped as full HTML page.
        minify (bool): Minify HTML markup.
        RETURNS (unicode): Rendered SVG or HTML markup.
        """
        ...
    def render_svg(self, render_id, words, arcs):
        """Render SVG.

        render_id (int): Unique ID, typically index of document.
        words (list): Individual words and their tags.
        arcs (list): Individual arcs and their start, end, direction and label.
        RETURNS (unicode): Rendered SVG markup.
        """
        self.levels = ...
        self.highest_level = ...
        self.offset_y = ...
        self.width = ...
        self.height = ...
        self.id = ...
    def render_word(self, text, tag, i):
        """Render individual word.

        text (unicode): Word text.
        tag (unicode): Part-of-speech tag.
        i (int): Unique ID, typically word index.
        RETURNS (unicode): Rendered SVG markup.
        """
        ...
    def render_arrow(self, label, start, end, direction, i):
        """Render individual arrow.

        label (unicode): Dependency label.
        start (int): Index of start word.
        end (int): Index of end word.
        direction (unicode): Arrow direction, 'left' or 'right'.
        i (int): Unique ID, typically arrow index.
        RETURNS (unicode): Rendered SVG markup.
        """
        ...
    def get_arc(self, x_start, y, y_curve, x_end):
        """Render individual arc.

        x_start (int): X-coordinate of arrow start point.
        y (int): Y-coordinate of arrow start and end point.
        y_curve (int): Y-corrdinate of Cubic Bézier y_curve point.
        x_end (int): X-coordinate of arrow end point.
        RETURNS (unicode): Definition of the arc path ('d' attribute).
        """
        ...
    def get_arrowhead(self, direction, x, y, end):
        """Render individual arrow head.

        direction (unicode): Arrow direction, 'left' or 'right'.
        x (int): X-coordinate of arrow start point.
        y (int): Y-coordinate of arrow start and end point.
        end (int): X-coordinate of arrow end point.
        RETURNS (unicode): Definition of the arrow head path ('d' attribute).
        """
        ...
    def get_levels(self, arcs):
        """Calculate available arc height "levels".
        Used to calculate arrow heights dynamically and without wasting space.

        args (list): Individual arcs and their start, end, direction and label.
        RETURNS (list): Arc levels sorted from lowest to highest.
        """
        ...

class EntityRenderer(object):
    """Render named entities as HTML."""

    style = ...
    def __init__(self, options=...):
        """Initialise dependency renderer.

        options (dict): Visualiser-specific options (colors, ents)
        """
        self.default_color = ...
        self.colors = ...
        self.ents = ...
        self.direction = ...
        self.lang = ...
    def render(self, parsed, page: bool = ..., minify: bool = ...):
        """Render complete markup.

        parsed (list): Dependency parses to render.
        page (bool): Render parses wrapped as full HTML page.
        minify (bool): Minify HTML markup.
        RETURNS (unicode): Rendered HTML markup.
        """
        ...
    def render_ents(self, text, spans, title):
        """Render entities in text.

        text (unicode): Original text.
        spans (list): Individual entity spans and their start, end and label.
        title (unicode or None): Document title set in Doc.user_data['title'].
        """
        ...