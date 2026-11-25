import io

from PIL import Image

from core.image_processor import ImageProcessor


def create_test_image():

    buffer = io.BytesIO()

    image = Image.new(
        "RGB",
        (1024, 1024),
        color="blue"
    )

    image.save(buffer, format="PNG")

    return buffer.getvalue()


def test_square_resolution(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "core.image_processor.IMAGE_DIR",
        tmp_path
    )

    image_path = ImageProcessor.save_image(
        image_data=create_test_image(),
        output_format="png",
        resolution="square"
    )

    with Image.open(image_path) as image:
        assert image.size == (1024, 1024)


def test_landscape_resolution(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "core.image_processor.IMAGE_DIR",
        tmp_path
    )

    image_path = ImageProcessor.save_image(
        image_data=create_test_image(),
        output_format="png",
        resolution="landscape"
    )

    with Image.open(image_path) as image:
        assert image.size == (1024, 576)


def test_portrait_resolution(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "core.image_processor.IMAGE_DIR",
        tmp_path
    )

    image_path = ImageProcessor.save_image(
        image_data=create_test_image(),
        output_format="png",
        resolution="portrait"
    )

    with Image.open(image_path) as image:
        assert image.size == (576, 1024)


def test_png_format(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "core.image_processor.IMAGE_DIR",
        tmp_path
    )

    image_path = ImageProcessor.save_image(
        image_data=create_test_image(),
        output_format="png"
    )

    with Image.open(image_path) as image:
        assert image.format == "PNG"


def test_jpeg_format(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "core.image_processor.IMAGE_DIR",
        tmp_path
    )

    image_path = ImageProcessor.save_image(
        image_data=create_test_image(),
        output_format="jpeg",
        quality=90
    )

    with Image.open(image_path) as image:
        assert image.format == "JPEG"
        assert image.size == (1024, 1024)


def test_webp_format(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "core.image_processor.IMAGE_DIR",
        tmp_path
    )

    image_path = ImageProcessor.save_image(
        image_data=create_test_image(),
        output_format="webp",
        quality=85
    )

    with Image.open(image_path) as image:
        assert image.format == "WEBP"
        assert image.size == (1024, 1024)


def test_invalid_format():

    try:
        ImageProcessor.save_image(
            image_data=create_test_image(),
            output_format="bmp"
        )
    except ValueError as error:
        assert "Formato de imagem inválido" in str(error)
    else:
        raise AssertionError("Formato inválido foi aceito.")


def test_invalid_resolution():

    try:
        ImageProcessor.save_image(
            image_data=create_test_image(),
            resolution="ultrawide"
        )
    except ValueError as error:
        assert "Resolução ou proporção inválida" in str(error)
    else:
        raise AssertionError("Resolução inválida foi aceita.")


def test_invalid_quality():

    try:
        ImageProcessor.save_image(
            image_data=create_test_image(),
            output_format="jpeg",
            quality=50
        )
    except ValueError as error:
        assert "qualidade deve estar entre 70 e 100" in str(error)
    else:
        raise AssertionError("Qualidade inválida foi aceita.")


def test_invalid_image():

    try:
        ImageProcessor.save_image(
            image_data=b"arquivo_invalido"
        )
    except ValueError as error:
        assert "imagem válida" in str(error)
    else:
        raise AssertionError("Arquivo inválido foi aceito.")


