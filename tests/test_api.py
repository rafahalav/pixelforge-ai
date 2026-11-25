from config.settings import Settings


def test_cloudflare_configuration():

    print("\nPIXELFORGE AI - CONFIGURAÇÃO CLOUDFLARE")
    print("=" * 45)

    assert Settings.CLOUDFLARE_ACCOUNT_ID
    assert Settings.CLOUDFLARE_API_TOKEN

    assert (
        Settings.IMAGE_MODEL
        == "@cf/black-forest-labs/flux-1-schnell"
    )

    print("Account ID: configurado")
    print("API Token: configurado")
    print("Modelo:", Settings.IMAGE_MODEL)

    print("\nConfiguração Cloudflare validada.")
