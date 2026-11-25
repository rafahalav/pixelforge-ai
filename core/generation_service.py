from pathlib import Path

from core.generator import ImageGenerator
from core.image_processor import ImageProcessor
from core.database import Database

from config.settings import GenerationConfig, Settings


class GenerationService:

    def __init__(self):

        self.generator = ImageGenerator()
        self.processor = ImageProcessor()
        self.database = Database()

    def generate(self, config: GenerationConfig):

        config.validate_options()

        # A API recebe somente prompt e steps.
        image_data = self.generator.generate(config)

        # O processamento de resolução e qualidade é local.
        image_path = self.processor.save_image(
            image_data=image_data,
            output_format=config.output_format,
            resolution=config.resolution,
            quality=config.quality
        )

        image_id = Path(image_path).stem

        image_info = self.processor.get_image_info(
            image_path
        )

        size = (
            f"{image_info['width']}x"
            f"{image_info['height']}"
        )

        quality = (
            "Sem perdas"
            if config.output_format == "png"
            else config.quality
        )

        try:

            self.database.add_generation(
                image_id=image_id,
                prompt=config.prompt,
                model=Settings.IMAGE_MODEL,
                steps=config.steps,
                output_format=config.output_format,
                image_path=image_path,
                size=size,
                quality=quality
            )

        except Exception:

            Path(image_path).unlink(missing_ok=True)

            raise

        return {
            "image_id": image_id,
            "image_path": str(image_path),
            "prompt": config.prompt,
            "model": Settings.IMAGE_MODEL,
            "steps": config.steps,
            "output_format": config.output_format,
            "resolution": config.resolution,
            "size": size,
            "quality": quality
        }
