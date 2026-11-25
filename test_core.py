from config.settings import Settings, GenerationConfig
from core.database import Database
from core.image_processor import ImageProcessor

print("\nPIXELFORGE AI - TESTE DO NÚCLEO")
print("=" * 45)

print("\n[1] Configurações")
print("Aplicação:", Settings.APP_NAME)
print("Versão:", Settings.VERSION)
print("Modelo:", Settings.IMAGE_MODEL)

print("\n[2] Validação de parâmetros")

config = GenerationConfig(
    prompt="Uma paisagem futurista em estilo cinematográfico",
    steps=4,
    output_format="png"
)

config.validate_options()
print("Configuração validada com sucesso.")
print("Steps:", config.steps)

print("\n[3] Banco de dados")

database = Database()
print("SQLite inicializado com sucesso.")

history = database.get_history()
print("Registros encontrados:", len(history))

print("\n[4] Processador de imagens")

print(
    "Validador disponível:",
    callable(ImageProcessor.validate_image)
)

print(
    "Salvamento disponível:",
    callable(ImageProcessor.save_image)
)

print("\n" + "=" * 45)
print("TESTES DO NÚCLEO CONCLUÍDOS.")
