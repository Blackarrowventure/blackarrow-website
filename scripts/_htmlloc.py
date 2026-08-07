"""
Shared HTML locator for the Black Arrow site scripts.

Design decision: this uses html.parser as a LOCATOR ONLY. It records byte
offsets into the original source string and later splices replacements in.
It never rebuilds HTML from a parse tree.

That matters because these pages carry hand-written comments, inline JSON-LD,
inline <style>, HTML entities and specific indentation. Any re-serialising
parser would silently normalise all of it. Splicing preserves every byte we
did not explicitly target.

Used by: build_ar.py, normalize_paths.py, fix_img_attrs.py, check_links.py,
         strip_keywords.py, bump_assets.py
"""

from html.parser import HTMLParser

# Void elements never have a closing tag, so they never open a content span.
VOID = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'source', 'track', 'wbr',
}


class Locator(HTMLParser):
    """Records the byte offsets of every tag and element content span.

    After feed():
      .tags  -> [(tag, attrs_dict, tag_start, tag_end, raw_text), ...]
                offsets delimit the start tag itself, e.g. '<img src="x">'
      .spans -> [(tag, attrs_dict, content_start, content_end), ...]
                offsets delimit what sits BETWEEN a start and end tag
    """

    def __init__(self, src):
        # convert_charrefs=False is essential: with the default True, the
        # parser decodes &amp; -> & behind our back and offsets drift.
        super().__init__(convert_charrefs=False)
        self.src = src
        # Line-start offset table so getpos() (1-based line, 0-based col)
        # can be converted to an absolute offset.
        self._line_offsets = [0]
        for line in src.split('\n')[:-1]:
            self._line_offsets.append(self._line_offsets[-1] + len(line) + 1)
        self._open = []
        self.tags = []
        self.spans = []

    def _offset(self):
        line, col = self.getpos()
        return self._line_offsets[line - 1] + col

    def handle_startendtag(self, tag, attrs):
        # Must override. The default implementation forwards to
        # handle_starttag + handle_endtag, which corrupts the open-tag stack
        # on self-closing SVG children like <path/> and <polyline/>.
        raw = self.get_starttag_text()
        start = self._offset()
        self.tags.append((tag, dict(attrs), start, start + len(raw), raw))

    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        start = self._offset()
        end = start + len(raw)
        self.tags.append((tag, dict(attrs), start, end, raw))
        # XHTML-style self-closing tags in this codebase (mostly inside SVG)
        # open no content span.
        if tag in VOID or raw.rstrip().endswith('/>'):
            return
        self._open.append((tag, dict(attrs), end))

    def handle_endtag(self, tag):
        end = self._offset()
        # Walk back to the matching open tag. Anything above it on the stack
        # was left unclosed, so discard it rather than mis-pair later tags.
        for i in range(len(self._open) - 1, -1, -1):
            if self._open[i][0] == tag:
                otag, attrs, content_start = self._open[i]
                self.spans.append((otag, attrs, content_start, end))
                del self._open[i:]
                return

    @property
    def unclosed(self):
        """Tags still open at EOF - a malformed-source signal."""
        return [(t, s) for t, _a, s in self._open]


def locate(src):
    """Parse src and return a finished Locator."""
    loc = Locator(src)
    loc.feed(src)
    loc.close()
    return loc


def splice(src, edits):
    """Apply [(start, end, replacement), ...] to src.

    Applied right-to-left so earlier offsets stay valid. Raises on overlap,
    which would otherwise corrupt output silently.
    """
    edits = sorted(edits, key=lambda e: e[0])
    for i in range(1, len(edits)):
        if edits[i][0] < edits[i - 1][1]:
            raise ValueError(
                f'Overlapping edits: {edits[i-1][:2]} and {edits[i][:2]}'
            )
    out = src
    for start, end, replacement in reversed(edits):
        out = out[:start] + replacement + out[end:]
    return out


def read(path):
    """Read a file preserving exact bytes-as-text, tracking any BOM."""
    raw = path.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    if bom:
        raw = raw[3:]
    return raw.decode('utf-8'), bom


def write(path, text, bom=False):
    """Write text back, preserving LF endings and any original BOM."""
    data = text.encode('utf-8')
    if bom:
        data = b'\xef\xbb\xbf' + data
    path.write_bytes(data)
