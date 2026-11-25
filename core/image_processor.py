import io
import uuid

from pathlib import Path

from PIL import Image, ImageOps

from config.settings import IMAGE_DIR


class ImageProcessor:

    RESOLUTIONS = {
        "square": (1024, 1024),
        "landscape": (1024, 576),
        "portrait": (576, 1024)
    }

    @staticmethod
    def validate_image(image_data):

        try:

            image = Image.open(
                io.BytesIO(image_data)
            )

            image.verify()

            return True

        except Exception as error:

            raise ValueError(
                "O arquivo recebido não é uma imagem válida."
            ) from error

    @staticmethod
    def save_image(
        image_data,
        output_format="png",
        resolution="square",
        quality=95
    ):

        ImageProcessor.validate_image(image_data)

        if output_format not in {"png", "jpeg", "webp"}:
            raise ValueError(
                "Formato de imagem inválido."
            )

        if resolution not in ImageProcessor.RESOLUTIONS:
            raise ValueError(
                "Resolução ou proporção inválida."
            )

        if not 70 <= quality <= 100:
            raise ValueError(
                "A qualidade deve estar entre 70 e 100."
            )

        with Image.open(
            io.BytesIO(image_data)
        ) as original:

            image = ImageOps.exif_transpose(original)
            image.load()

            target_size = ImageProcessor.RESOLUTIONS[
                resolution
            ]

            image = ImageOps.fit(
                image,
                target_size,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5)
            )

            image_id = uuid.uuid4().hex

            extension = output_format.lower()

            filename = f"{image_id}.{extension}"

            output_path = IMAGE_DIR / filename

            if extension == "jpeg":

                if image.mode not in ("RGB", "L"):
                    image = image.convert("RGB")

                image.save(
                    output_path,
                    format="JPEG",
                    quality=quality,
                    optimize=True
                )

            elif extension == "webp":

                if image.mode not in ("RGB", "RGBA"):
                    image = image.convert("RGB")

                image.save(
                    output_path,
                    format="WEBP",
                    quality=quality,
                    method=6
                )

            else:

                image.save(
                    output_path,
                    format="PNG",
                    optimize=True
                )

        return output_path

    @staticmethod
    def get_image_info(image_path):

        with Image.open(image_path) as image:

            return {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode,
                "size_bytes": Path(
                    image_path
                ).stat().st_size
            }
