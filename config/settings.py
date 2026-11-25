import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

IMAGE_DIR = BASE_DIR / "data" / "images"
DATABASE_PATH = BASE_DIR / "data" / "pixelforge.db"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)


class Settings:
    APP_NAME = "PixelForge AI"
    VERSION = "1.0.0"

    CLOUDFLARE_ACCOUNT_ID = os.getenv(
        "CLOUDFLARE_ACCOUNT_ID", ""
    )

    CLOUDFLARE_API_TOKEN = os.getenv(
        "CLOUDFLARE_API_TOKEN", ""
    )

    IMAGE_MODEL = os.getenv(
        "CLOUDFLARE_IMAGE_MODEL",
        "@cf/black-forest-labs/flux-1-schnell"
    )

    DEFAULT_STEPS = 4
    DEFAULT_FORMAT = "png"
    DEFAULT_QUALITY = 95


class GenerationConfig(BaseModel):

    prompt: str = Field(
        min_length=3,
        max_length=2048
    )

    steps: int = Field(
        default=4,
        ge=1,
        le=8
    )

    output_format: str = "png"

    resolution: str = "square"

    quality: int = Field(
        default=95,
        ge=70,
        le=100
    )

    def validate_options(self):

        allowed_formats = {
            "png",
            "jpeg",
            "webp"
        }

        allowed_resolutions = {
            "square",
            "landscape",
            "portrait"
        }

        if self.output_format not in allowed_formats:
            raise ValueError(
                "Formato de imagem inválido."
            )

        if self.resolution not in allowed_resolutions:
            raise ValueError(
                "Resolução ou proporção inválida."
            )

        return self
