import base64
import json

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config.settings import Settings, GenerationConfig


class ImageGenerator:

    def __init__(self):
        if not Settings.CLOUDFLARE_ACCOUNT_ID:
            raise ValueError(
                "Cloudflare Account ID não configurado no .env."
            )

        if not Settings.CLOUDFLARE_API_TOKEN:
            raise ValueError(
                "Cloudflare API Token não configurado no .env."
            )

        self.account_id = Settings.CLOUDFLARE_ACCOUNT_ID
        self.api_token = Settings.CLOUDFLARE_API_TOKEN
        self.model = Settings.IMAGE_MODEL

        self.api_url = (
            "https://api.cloudflare.com/client/v4/accounts/"
            f"{self.account_id}/ai/run/{self.model}"
        )

    def generate(self, config: GenerationConfig):

        config.validate_options()

        payload = {
            "prompt": config.prompt,
            "steps": config.steps
        }

        request = Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urlopen(request, timeout=180) as response:
                response_data = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as error:
            if error.code in (401, 403):
                raise RuntimeError(
                    "Falha de autenticação ou permissão na Cloudflare."
                ) from error

            if error.code == 429:
                raise RuntimeError(
                    "Limite de utilização da Cloudflare atingido. "
                    "Verifique sua cota gratuita."
                ) from error

            raise RuntimeError(
                f"Erro HTTP da Cloudflare: {error.code}."
            ) from error

        except URLError as error:
            raise RuntimeError(
                "Não foi possível conectar à Cloudflare."
            ) from error

        except TimeoutError as error:
            raise RuntimeError(
                "A geração excedeu o tempo limite."
            ) from error

        if not response_data.get("success"):
            errors = response_data.get("errors", [])
            message = (
                errors[0].get("message", "Erro desconhecido.")
                if errors else "Erro desconhecido."
            )

            raise RuntimeError(
                f"A Cloudflare não concluiu a geração: {message}"
            )

        result = response_data.get("result", {})
        image_data = result.get("image")

        if not image_data:
            raise RuntimeError(
                "A Cloudflare não retornou os dados da imagem."
            )

        try:
            return base64.b64decode(
                image_data,
                validate=True
            )
        except Exception as error:
            raise RuntimeError(
                "Os dados da imagem retornados são inválidos."
            ) from error
