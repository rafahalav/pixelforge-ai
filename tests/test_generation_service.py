import sys
import io

from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import GenerationConfig
from core.generation_service import GenerationService


def create_test_image():

    buffer = io.BytesIO()

    image = Image.new(
        "RGB",
        (100, 100),
        color="blue"
    )

    image.save(buffer, format="PNG")

    return buffer.getvalue()


def test_generation_service(monkeypatch, tmp_path):

    import core.database as database_module
    import core.image_processor as processor_module
    import core.generation_service as service_module

    test_database = tmp_path / "test.db"
    test_image_dir = tmp_path / "images"

    test_image_dir.mkdir(parents=True)

    monkeypatch.setattr(
        database_module,
        "DATABASE_PATH",
        test_database
    )

    monkeypatch.setattr(
        processor_module,
        "IMAGE_DIR",
        test_image_dir
    )

    class FakeGenerator:

        def __init__(self):
            pass

        def generate(self, config):
            assert config.steps == 4
            return create_test_image()

    monkeypatch.setattr(
        service_module,
        "ImageGenerator",
        FakeGenerator
    )

    service = GenerationService()

    config = GenerationConfig(
        prompt="Imagem de teste automatizado",
        steps=4,
        output_format="png",
        resolution="square",
        quality=95
    )

    result = service.generate(config)

    image_path = Path(result["image_path"])

    assert image_path.exists()
    assert image_path.suffix == ".png"

    assert result["prompt"] == config.prompt
    assert result["output_format"] == "png"
    assert result["steps"] == 4
    assert result["resolution"] == "square"
    assert result["size"] == "1024x1024"
    assert result["quality"] == "Sem perdas"

    with Image.open(image_path) as image:
        assert image.size == (1024, 1024)
        assert image.format == "PNG"

    history = service.database.get_history()

    assert len(history) == 1

    assert history[0]["image_id"] == result["image_id"]
    assert history[0]["prompt"] == config.prompt
    assert history[0]["image_path"] == str(image_path)
    assert history[0]["steps"] == 4

    assert history[0]["size"] == "1024x1024"
    assert history[0]["quality"] == "Sem perdas"
    assert history[0]["output_format"] == "png"

    print("\nGenerationService: integração validada.")


