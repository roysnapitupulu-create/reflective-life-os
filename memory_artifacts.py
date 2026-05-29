from pathlib import Path
import random
from typing import Any


MAX_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

SIDE_NOTES = [
    "Coffee trees can live for decades.",
    "The smell after rain has a name: petrichor.",
    "Many old books release compounds similar to vanilla.",
    "Graphite pencils do not contain lead.",
    "Clouds can weigh hundreds of thousands of kilograms.",
    "A single sheet of paper can be folded only a limited number of times by hand.",
    "The first umbrellas were often used for shade before rain.",
    "Some seashells keep growing in a spiral because one side grows faster than the other.",
    "Bread gets its airy texture from tiny pockets of carbon dioxide.",
    "Tea leaves and white tea can come from the same plant.",
    "The word window comes from an old phrase meaning wind eye.",
    "Rainbows are full circles, but the ground usually hides the lower half.",
    "Old film photographs are made from tiny light-sensitive crystals.",
    "A ceramic mug is hardened by heat high enough to change the clay itself.",
    "Many city streets are warmer at night because stone and asphalt hold heat.",
    "Paper was invented long before bound books became common.",
    "Some stars visible tonight may no longer exist in the same form.",
    "The color of sunset changes as light travels through more atmosphere.",
    "Denim was originally valued because it was sturdy work fabric.",
    "A candle flame has different colors because its parts burn at different temperatures.",
    "Glass is made mostly from sand heated until it changes form.",
    "The scent of fresh-cut grass comes from compounds plants release when damaged.",
    "Some flowers close at night in a movement called nyctinasty.",
    "Salt was once valuable enough to shape trade routes.",
    "A handwritten line carries small pressure changes from the writer's hand.",
]


def choose_side_note() -> str:
    return random.choice(SIDE_NOTES)


def get_image_extension(filename: str, mime_type: str = "") -> str:
    extension = Path(str(filename or "")).suffix.lower()
    if extension in ALLOWED_IMAGE_EXTENSIONS:
        return extension
    if mime_type == "image/png":
        return ".png"
    if mime_type == "image/webp":
        return ".webp"
    return ".jpg"


def validate_image_upload(uploaded_file: Any) -> str | None:
    if uploaded_file is None:
        return None

    mime_type = str(getattr(uploaded_file, "type", "") or "")
    extension = Path(str(getattr(uploaded_file, "name", "") or "")).suffix.lower()
    if mime_type not in ALLOWED_IMAGE_TYPES and extension not in ALLOWED_IMAGE_EXTENSIONS:
        return "Foto perlu berupa JPG, PNG, atau WebP."

    try:
        size = int(getattr(uploaded_file, "size", 0) or 0)
    except (TypeError, ValueError):
        size = 0
    if size > MAX_IMAGE_BYTES:
        return "Ukuran foto maksimal 5 MB untuk versi awal ini."

    return None
