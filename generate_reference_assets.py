"""Build the local KnowledgeShare reference library.

The attachment directory is intentionally passed in as an argument so this
script never depends on a machine-specific path when the repository is shared.
Each duplicate attachment is collapsed by content hash. Pages are written at
their source dimensions and PDFs use those same dimensions, which prevents
browser/print-style cropping.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import OrderedDict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


GROUPS = OrderedDict(
    [
        ("api", ("APIs & testing", "Engineering", "Testing an API from contract to resilience.", ["API testing types"])),
        (
            "prompt-systems",
            ("Prompt systems", "AI & ML", "The layers that make model work reliable and repeatable.", ["Prompt Context Harness Loop Engineering"]),
        ),
        (
            "math-probability",
            ("Math & probability", "Foundations", "The geometry and uncertainty behind intelligent systems.", ["AI Math", "Linear Algebra", "Probablity Distribution", "Probablity Distribution Graph", "CLT Statistics", "Hypothesis Testing", "z-distribution"]),
        ),
        (
            "machine-learning",
            ("Machine learning", "AI & ML", "A practical map of algorithms, training, and evaluation.", ["ML All", "ML Essential", "ML Type", "Ml Formulas", "Imp ML", "Aupervised Learning Algo", "Regression Algo", "Regression Metrics", "KNN", "PCA", "Regularization in ML", "Gradient Descent", "Loss fn", "Activation fn", "Activation fn2"]),
        ),
        (
            "python-data",
            ("Python & data analysis", "Data", "The everyday tools and workflows for turning data into insight.", ["Imp Python", "pyhton fn", "python fn", "DS Python", "Python EDA", "Python Library", "Numpy fn", "Pandas Operation", "SciPy", "Matplotlib viz", "EDA Q", "Exploratory Data Analysis", "Exploratory Data Analysis Workflow", "DA types", "Data Analytics Formula"]),
        ),
        (
            "data-systems",
            ("SQL & data systems", "Data", "How data moves from storage to dependable analytical systems.", ["Imp SQL", "DB Concept", "DE flow", "Data Analytics Stack"]),
        ),
        (
            "deep-learning",
            ("Deep learning", "AI & ML", "Architectures that learn representations, sequences, and structure.", ["Deep Learning Anatomy Structure", "Neural Network Types", "Backpropagation", "Encoder ML", "RNN vs LSTM vs GRU", "TensorFlow"]),
        ),
        (
            "llm-generative-ai",
            ("LLMs & generative AI", "AI & ML", "From transformer blocks to practical generative systems.", ["LLM Architecture", "LLM Basic", "Transformer", "Gen AI Models", "Gen AI pre", "GenAI Simple Project", "Gen AI Library", "AI frameworks"]),
        ),
        (
            "rag-agents",
            ("RAG & agents", "AI & ML", "Retrieval, tools, planning, and the systems that connect them.", ["RAG", "RAG vs Agentic RAG", "Agent Framework"]),
        ),
        (
            "computer-vision",
            ("Computer vision", "AI & ML", "How machines see, represent, and reason over images.", ["Computer Vision", "Computer VIsion Explained"]),
        ),
        (
            "mlops",
            ("MLOps", "Engineering", "The delivery, monitoring, and operating layer for models.", ["MLOps cheatsheet"]),
        ),
        (
            "learning-paths",
            ("AI learning paths", "Foundations", "Curated maps for finding the next useful concept.", ["Imp Free AI courses"]),
        ),
    ]
)

# These pages contain an explicit promotional footer rather than ordinary
# infographic content. The bands are intentionally narrow and are filled from
# the page immediately above them, so they disappear into the original paper.
FOOTER_BANDS = {
    "agent-framework": [(0.935, 1.0)],
    "ai-math": [(0.91, 1.0)],
    "computer-vision": [(0.94, 1.0)],
    "computer-vision-explained": [(0.92, 1.0)],
    "gradient-descent": [(0.965, 1.0)],
    "genai-simple-project": [(0.945, 1.0)],
    "hypothesis-testing": [(0.935, 1.0)],
    "imp-sql": [(0.94, 1.0)],
    "imp-python": [(0.945, 1.0)],
    "imp-ml": [(0.945, 1.0)],
    "ml-essential": [(0.95, 1.0)],
    "clt-statistics": [(0.97, 1.0)],
    "llm-basic": [(0.935, 1.0)],
    "prompt-context-harness-loop-engineering": [(0.935, 1.0)],
    "python-library": [(0.965, 1.0)],
    "rnn-vs-lstm-vs-gru": [(0.935, 1.0)],
    "aupervised-learning-algo": [(0.965, 1.0)],
    "z-distribution": [(0.97, 1.0)],
}

# Credits and logos also occur between vertically stacked sheets. These are
# page-relative rectangles, not broad crops, so surrounding diagrams remain
# intact.
SPECIAL_RECTS = {
    "linear-algebra": [
        (0.40, 0.965, 0.61, 1.0),
    ],
    "genai-simple-project": [
        (0.76, 0.0, 1.0, 0.065),
        (0.12, 0.49, 0.25, 0.57),
        (0.76, 0.49, 1.0, 0.57),
    ],
    "gradient-descent": [
        (0.84, 0.46, 1.0, 0.56),
        (0.84, 0.965, 1.0, 1.0),
    ],
}


def display_name(raw: str) -> str:
    raw = raw.replace("pyhton", "Python").replace("Probablity", "Probability")
    raw = raw.replace("Aupervised", "Supervised").replace("fn", "functions")
    raw = raw.replace("DA", "Data analytics").replace("DE", "Data engineering")
    return raw.strip()


def logo_mask(image: Image.Image) -> Image.Image:
    """Find the small MLTut mark in either upper corner and mask it.

    The mask is deliberately conditional: many sheets use the same area for a
    real diagram, so only a dense orange+green mark is treated as a watermark.
    """

    rgb = image.convert("RGB")
    w, h = rgb.size
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    corner_w, corner_h = int(w * 0.1), int(h * 0.09)
    for left, right in ((0, corner_w), (w - corner_w, w)):
        orange = yellow = 0
        for y in range(corner_h):
            for x in range(left, right):
                r, g, b = rgb.getpixel((x, y))
                if r > 145 and g > 65 and g < 220 and b < 125 and r > g * 1.2:
                    orange += 1
                if r > 150 and g > 100 and b < 120 and r > b * 1.4:
                    yellow += 1
        if orange >= 18 and yellow >= 10:
            draw.rounded_rectangle((left, 0, right, corner_h), radius=max(3, int(w * 0.008)), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(max(1, int(w * 0.002))))


def inpaint(image: Image.Image, mask: Image.Image) -> Image.Image:
    """Softly reconstruct a masked mark from nearby pixels, without a white box."""

    if not any(mask.getdata()):
        return image.convert("RGB")
    base = image.convert("RGB")
    # The marks sit on the light paper margin. Reconstruct that margin from a
    # perimeter median rather than blurring nearby title lettering into it.
    bounds = mask.getbbox()
    assert bounds is not None
    left, top, right, bottom = bounds
    perimeter = []
    for x in range(left, min(right + 8, base.width)):
        for y in (max(0, top - 8), min(base.height - 1, bottom + 8)):
            perimeter.append(base.getpixel((x, y)))
    for y in range(top, min(bottom, base.height)):
        for x in (max(0, left - 8), min(base.width - 1, right + 8)):
            perimeter.append(base.getpixel((x, y)))
    channels = list(zip(*perimeter))
    fill = tuple(sorted(channel)[len(channel) // 2] for channel in channels)
    work = Image.new("RGB", base.size, fill)
    result = base.copy()
    result.paste(work, (0, 0), mask)
    return result


def cover_bands(image: Image.Image, bands: list[tuple[float, float]]) -> Image.Image:
    """Replace promotional footer bands with the median color above each band."""

    result = image.convert("RGB")
    draw = ImageDraw.Draw(result)
    w, h = result.size
    for start, end in bands:
        top, bottom = int(h * start), min(h, int(h * end))
        sample_top = max(0, top - max(4, int(h * 0.012)))
        pixels = [result.getpixel((x, y)) for y in range(sample_top, top) for x in range(0, w, max(1, w // 120))]
        channels = list(zip(*pixels))
        fill = tuple(sorted(channel)[len(channel) // 2] for channel in channels)
        draw.rectangle((0, top, w, bottom), fill=fill)
    return result


def cover_rects(image: Image.Image, rects: list[tuple[float, float, float, float]]) -> Image.Image:
    result = image.convert("RGB")
    draw = ImageDraw.Draw(result)
    w, h = result.size
    for left, top, right, bottom in rects:
        x1, y1, x2, y2 = int(w * left), int(h * top), int(w * right), int(h * bottom)
        # Use a broader, nearby patch so text strokes or borders do not turn
        # into visible horizontal seams inside the flat replacement.
        if left > 0.03:
            ref_left, ref_right = max(0, int(w * max(0.01, left - 0.08))), max(1, int(w * max(0.02, left - 0.03)))
        else:
            ref_left, ref_right = x2 + 3, min(w, x2 + 24)
        pixels = [result.getpixel((x, y)) for y in range(max(0, y1 - 12), min(h, y2 + 12)) for x in range(ref_left, ref_right)]
        channels = list(zip(*pixels))
        fill = tuple(sorted(channel)[len(channel) // 2] for channel in channels)
        draw.rectangle((x1, y1, x2, y2), fill=fill)
    return result


def unique_sources(attachments: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in sorted(attachments.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        found.setdefault(digest, path)
    return found


def classify(name: str) -> str:
    for slug, (_, _, _, names) in GROUPS.items():
        if name in names:
            return slug
    raise ValueError(f"Unclassified attachment: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("attachments", type=Path)
    parser.add_argument("--output", type=Path, default=Path("assets/reference"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for old in args.output.glob("*"):
        if old.name != ".gitkeep" and old.is_file():
            old.unlink()

    sources = unique_sources(args.attachments)
    by_name: dict[str, Path] = {}
    for source in sources.values():
        name = re.sub(r"^[0-9a-f-]{36}-", "", source.stem, flags=re.I).strip()
        by_name[name] = source

    catalog = []
    for slug, (title, category, blurb, names) in GROUPS.items():
        pages = []
        for name in names:
            source = by_name.get(name)
            if not source:
                raise FileNotFoundError(f"Missing source for {name}")
            clean_name = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            clean_path = args.output / f"{clean_name}.jpg"
            image = Image.open(source).convert("RGB")
            cleaned = inpaint(image, logo_mask(image))
            cleaned = cover_bands(cleaned, FOOTER_BANDS.get(clean_name, []))
            cleaned = cover_rects(cleaned, SPECIAL_RECTS.get(clean_name, []))
            cleaned.save(clean_path, "JPEG", quality=88, optimize=True, progressive=True)
            pages.append({"title": display_name(name), "image": clean_path.name})

        pdf_path = args.output / f"{slug}.pdf"
        pdf_images = [Image.open(args.output / page["image"]).convert("RGB") for page in pages]
        pdf_images[0].save(pdf_path, "PDF", save_all=True, append_images=pdf_images[1:], resolution=96.0)
        catalog.append(
            {
                "id": slug,
                "category": category,
                "title": title,
                "blurb": blurb,
                "pages": pages,
                "preview": pages[0]["image"],
                "pdf": pdf_path.name,
            }
        )

    (args.output / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {sum(len(item['pages']) for item in catalog)} pages in {len(catalog)} grouped PDFs.")


if __name__ == "__main__":
    main()
