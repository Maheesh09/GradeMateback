import fitz  # PyMuPDF
import re
from typing import Dict

# ---------- line patterns ----------
Q_LINE     = re.compile(r'^\s*(\d+)\.\s*$')                 # "1."
PART_LINE  = re.compile(r'^\s*([ivxlcdm]+)\.\s*(.*)$', re.I) # "i. text" / "ii. text" / "iv. text" ...
# (No a./b./c. lines; <> delimiter removed)

def _norm(s: str) -> str:
    """Normalize odd PDF whitespace so regexes match reliably."""
    return (s.replace('\u00A0', ' ')   # NBSP -> space
             .replace('\ufeff', '')    # BOM
             .rstrip())

def extract_text(path: str) -> str:
    """Extract text in natural reading order and lightly clean it."""
    doc = fitz.open(path)
    txt = "\n".join(page.get_text("text", sort=True) for page in doc)
    # light cleanup
    txt = txt.replace('\r', '')
    txt = re.sub(r'-\n', '', txt)          # join hyphenated line breaks
    txt = re.sub(r'[ \t]+\n', '\n', txt)   # strip trailing spaces
    txt = re.sub(r'\n{3,}', '\n\n', txt)   # collapse extra blank lines
    return txt

def parse_questions(text: str) -> Dict[str, Dict[str, str]]:
    """
    Parse a document formatted as:
        1.
        i. ...
        ii. ...
        iii. ...
        2.
        i. ...
        ...
    Returns: {"1": {"i": "...", "ii": "...", ...}, "2": {...}, ...}
    """
    lines = [_norm(ln) for ln in text.splitlines()]
    data: Dict[str, Dict[str, str]] = {}

    qid = None            # current question number as str
    part_key = None       # current roman key: "i", "ii", ...
    buf = []              # accumulates lines for current roman part

    def flush_part():
        nonlocal buf, part_key, qid
        if qid and part_key:
            chunk = "\n".join(buf).strip()
            if chunk:
                data.setdefault(qid, {})[part_key] = chunk
        buf = []

    for ln in lines:
        # New question?
        m_q = Q_LINE.match(ln)
        if m_q:
            # close previous part (if any)
            flush_part()
            qid = m_q.group(1)
            part_key = None
            continue

        # New roman subpart?
        m_p = PART_LINE.match(ln)
        if m_p:
            # close previous part first
            flush_part()
            part_key = m_p.group(1).lower()    # e.g., "i", "ii", "iv"
            buf = [m_p.group(2)]
            continue

        # Otherwise, keep appending lines to the current part buffer
        if part_key is not None:
            buf.append(ln)
        else:
            # lines before first roman part in a question are ignored
            pass

    # flush last buffered part at EOF
    flush_part()
    return data

# -------- usage ----------
if __name__ == "__main__":
    pdf_path = "answers.pdf"  # <- your PDF with the 1..10 + i/ii/iii format
    text = extract_text(pdf_path)
    qa_dict = parse_questions(text)
    print(qa_dict)            # or json.dumps for pretty print
