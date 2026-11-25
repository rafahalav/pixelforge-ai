import streamlit as st

from pathlib import Path

from config.settings import (
    GenerationConfig,
    Settings
)

from core.database import Database
from core.generation_service import GenerationService
from core.prompt_engine import PromptEngineer


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="PixelForge AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def get_mime_type(output_format):
    mime_types = {
        "png": "image/png",
        "jpeg": "image/jpeg",
        "webp": "image/webp"
    }

    return mime_types.get(output_format, "application/octet-stream")

# ============================================================
# BANNER DA SIDEBAR
# ============================================================

SIDEBAR_BANNER = (
    Path(__file__).resolve().parent
    / "assets"
    / "sidebar-banner.png"
)

PIXELFORGE_ICON = (
    Path(__file__).resolve().parent
    / "assets"
    / "pixelforge-icon.png"
)

# ============================================================
# ESTILO VISUAL - DARK TECH
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #080d18;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background-color: #0d1423;
    border-right: 1px solid #1e293b;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    color: #e2e8f0;
}

p, label {
    color: #cbd5e1;
}

.pixel-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: 2px;
    color: #38bdf8;
    margin-bottom: 0;
}

.pixel-subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    letter-spacing: 3px;
    margin-top: 4px;
}

.section-title {
    color: #38bdf8;
    font-size: 1.15rem;
    font-weight: 700;
    margin-top: 1rem;
}

.info-panel {
    background: linear-gradient(
        135deg,
        #111c30,
        #0d1423
    );
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 20px;
}

div.stButton > button {
    background: linear-gradient(
        90deg,
        #0284c7,
        #2563eb
    );
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    min-height: 45px;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #0ea5e9,
        #3b82f6
    );
    border: none;
    color: white;
}

div.stButton > button:disabled {
    background: #263449;
    color: #64748b;
}

.stTextArea textarea,
.stTextInput input {
    background-color: #111c30;
    color: #e2e8f0;
    border: 1px solid #334155;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #111c30;
}

.stSlider [data-baseweb="slider"] {
    color: #38bdf8;
}

hr {
    border-color: #1e293b;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CABEÇALHO
# ============================================================

header_icon, header_text = st.columns(
    [0.13, 0.87],
    vertical_alignment="center"
)

with header_icon:
    if PIXELFORGE_ICON.exists():
        st.image(
            str(PIXELFORGE_ICON),
            width=105
        )

with header_text:
    st.markdown("""
    <div style="margin-bottom: 0.5px;">
        <div class="pixel-title">PixelForge AI</div>
        <div class="pixel-subtitle">
            AI IMAGE GENERATION STUDIO
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    "Transforme suas ideias em imagens com inteligência artificial."
)

# ============================================================
# ESTADO DA SESSÃO
# ============================================================

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# BANCO DE DADOS
# ============================================================

database = Database()


# ============================================================
# BARRA LATERAL - HISTÓRICO
# ============================================================

with st.sidebar:

    # Banner institucional
    if SIDEBAR_BANNER.exists():
        st.image(
            str(SIDEBAR_BANNER),
            use_container_width=True
        )

    st.markdown("## 🗂️ Histórico")
    st.caption("Suas imagens geradas")

    history = database.get_history()

    if not history:

        st.info("Nenhuma imagem no histórico.")

    else:

        for item in history:

            image_id = item["image_id"]
            image_path = Path(item["image_path"])

            with st.expander(
                f"🖼️ {image_id[:16]}",
                expanded=False
            ):

                if image_path.exists():

                    st.image(
                        str(image_path),
                        use_container_width=True
                    )

                    with open(image_path, "rb") as image_file:

                        st.download_button(
                            label="⬇️ Baixar imagem",
                            data=image_file.read(),
                            file_name=image_path.name,
                            mime=get_mime_type(item["output_format"]),
                            key=f"download_{image_id}",
                            use_container_width=True
                        )

                else:

                    st.warning(
                        "Arquivo de imagem não encontrado."
                    )

                st.caption(
                    f"Modelo: {item['model']}"
                )

                st.caption(
                    f"Etapas: {item['steps']}"
                )

                st.caption(
                    f"Dimensões: {item.get('size', 'N/A')}"
                )

                st.caption(
                    f"Formato: {item['output_format'].upper()}"
                )

                st.caption(
                    f"Qualidade: {item.get('quality', 'N/A')}"
                )

                if st.button(
                    "🗑️ Excluir imagem",
                    key=f"delete_{image_id}",
                    use_container_width=True
                ):

                    database.delete_generation(image_id)

                    if image_path.exists():
                        image_path.unlink()

                    if (
                        st.session_state.last_result
                        and st.session_state.last_result["image_id"] == image_id
                    ):
                        st.session_state.last_result = None

                    st.rerun()


# ============================================================
# FORMULÁRIO DE ENGENHARIA DE PROMPT
# ============================================================

st.markdown(
    '<div class="section-title">✦ Criar nova imagem</div>',
    unsafe_allow_html=True
)

st.write(
    "Descreva os elementos da imagem separadamente "
    "para construir instruções mais claras e organizadas."
)

st.markdown("### 1. Assunto principal")

subject = st.text_area(
    "O que deverá aparecer na imagem?",
    placeholder=(
        "Ex.: A futuristic digital art studio "
        "with an advanced artificial intelligence core."
    ),
    height=90,
    max_chars=1000,
    key="prompt_subject"
)

st.markdown("### 2. Composição e enquadramento")

composition = st.text_area(
    "Como os elementos devem estar organizados?",
    placeholder=(
        "Ex.: Wide horizontal composition, "
        "central subject, balanced visual elements."
    ),
    height=75,
    max_chars=500,
    key="prompt_composition"
)

st.markdown("### 3. Estilo visual")

style = st.text_area(
    "Qual estética ou estilo artístico deseja?",
    placeholder=(
        "Ex.: Premium cinematic digital art, "
        "photorealistic, futuristic technology."
    ),
    height=75,
    max_chars=500,
    key="prompt_style"
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 4. Iluminação e atmosfera")

    lighting = st.text_area(
        "Descreva a iluminação.",
        placeholder=(
            "Ex.: Soft neon lighting, "
            "dramatic shadows, cinematic atmosphere."
        ),
        height=100,
        max_chars=500,
        key="prompt_lighting"
    )

with col2:

    st.markdown("### 5. Paleta de cores")

    colors = st.text_area(
        "Quais cores devem predominar?",
        placeholder=(
            "Ex.: Dark navy, cyan, "
            "electric blue and subtle purple."
        ),
        height=100,
        max_chars=500,
        key="prompt_colors"
    )

st.markdown("### 6. Elementos obrigatórios")

required_elements = st.text_area(
    "Quais elementos precisam aparecer na imagem?",
    placeholder=(
        "Ex.: Glowing digital core, neural networks, "
        "holographic interfaces and light particles."
    ),
    height=90,
    max_chars=500,
    key="prompt_required"
)


# ============================================================
# CONSTRUÇÃO E PRÉ-VISUALIZAÇÃO DO PROMPT
# ============================================================

final_prompt = None
prompt_error = None

if subject.strip():

    try:

        final_prompt = PromptEngineer.build_prompt(
            subject=subject,
            composition=composition,
            style=style,
            lighting=lighting,
            colors=colors,
            required_elements=required_elements
        )

    except ValueError as error:

        prompt_error = str(error)

else:

    prompt_error = (
        "Informe o assunto principal para construir o prompt."
    )


st.markdown("---")
st.markdown("### 🔍 Pré-visualização do prompt")

if final_prompt:

    st.code(
        final_prompt,
        language="text"
    )

    st.caption(
        f"{len(final_prompt)} / 2048 caracteres"
    )

elif prompt_error:

    st.info(prompt_error)


# ============================================================
# CONFIGURAÇÕES DE GERAÇÃO
# ============================================================

st.markdown("---")
st.markdown("### ⚙️ Configurações de geração")

st.markdown("#### 📐 Proporção da imagem")

resolution_options = {
    "Quadrada (1:1) — 1024 × 1024": "square",
    "Paisagem (16:9) — 1024 × 576": "landscape",
    "Retrato (9:16) — 576 × 1024": "portrait"
}

resolution_label = st.selectbox(
    "Escolha o enquadramento",
    options=list(resolution_options.keys()),
    index=0,
    help=(
        "A imagem será inicialmente gerada em formato quadrado "
        "pelo modelo e depois adaptada localmente."
    )
)

resolution = resolution_options[resolution_label]

col1, col2 = st.columns(2)

with col1:

    steps = st.slider(
        "Etapas de geração",
        min_value=1,
        max_value=8,
        value=4,
        help=(
            "Controla o número de etapas enviado ao modelo. "
            "O FLUX.1 Schnell utiliza normalmente 4."
        )
    )

with col2:

    output_format = st.selectbox(
        "Formato da imagem",
        options=["png", "jpeg", "webp"],
        index=0,
        format_func=lambda value: value.upper(),
        help=(
            "PNG oferece compressão sem perdas. "
            "JPEG e WebP permitem controlar a qualidade."
        )
    )


# ============================================================
# CONTROLE DE QUALIDADE
# ============================================================

if output_format in ("jpeg", "webp"):

    st.markdown("#### 🎚️ Qualidade de compressão")

    quality = st.slider(
        "Qualidade da imagem",
        min_value=70,
        max_value=100,
        value=95,
        step=1,
        help=(
            "Valores maiores preservam mais qualidade visual, "
            "mas podem gerar arquivos maiores."
        )
    )

    st.caption(
        f"Qualidade selecionada: {quality}/100"
    )

else:

    quality = 95

    st.info(
        "PNG utiliza compressão sem perdas. "
        "O controle de qualidade não se aplica a esse formato."
    )


# ============================================================
# RESUMO DAS CONFIGURAÇÕES
# ============================================================

st.markdown("""
<div class="info-panel">
    <strong style="color:#38bdf8;">
        CONFIGURAÇÃO DE SAÍDA
    </strong>
</div>
""", unsafe_allow_html=True)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric(
        "Proporção",
        {
            "square": "1:1",
            "landscape": "16:9",
            "portrait": "9:16"
        }[resolution]
    )

with summary_col2:
    st.metric(
        "Formato",
        output_format.upper()
    )

with summary_col3:
    st.metric(
        "Qualidade",
        "Sem perdas" if output_format == "png" else f"{quality}/100"
    )


# ============================================================
# GERAÇÃO DA IMAGEM
# ============================================================

st.markdown("")

generate_button = st.button(
    "⚡ GERAR IMAGEM",
    use_container_width=True,
    disabled=not bool(final_prompt)
)

if generate_button:

    try:

        config = GenerationConfig(
            prompt=final_prompt,
            steps=steps,
            output_format=output_format,
            resolution=resolution,
            quality=quality
        )

        with st.spinner(
            "PixelForge AI está criando sua imagem..."
        ):

            service = GenerationService()

            result = service.generate(config)

        st.session_state.last_result = result

        st.success(
            "Imagem gerada e salva com sucesso!"
        )

        st.rerun()

    except Exception as error:

        st.error(
            f"Não foi possível gerar a imagem: {error}"
        )


# ============================================================
# RESULTADO DA ÚLTIMA GERAÇÃO
# ============================================================

result = st.session_state.last_result

if result:

    st.markdown("---")
    st.markdown("## ✨ Resultado da geração")

    image_path = Path(result["image_path"])

    if image_path.exists():

        st.image(
            str(image_path),
            caption="Imagem gerada pelo PixelForge AI",
            use_container_width=True
        )

        with open(image_path, "rb") as image_file:

            st.download_button(
                label="⬇️ Baixar imagem gerada",
                data=image_file.read(),
                file_name=image_path.name,
                mime=get_mime_type(result["output_format"]),
                key=f"result_download_{result['image_id']}"
            )

        with st.expander("Detalhes da geração"):

            st.write(
                f"**Identificador:** {result['image_id']}"
            )

            st.write(
                f"**Modelo:** {result['model']}"
            )

            st.write(
                f"**Etapas:** {result['steps']}"
            )

            st.write(
                f"**Proporção:** {result.get('resolution', 'N/A')}"
            )

            st.write(
                f"**Dimensões:** {result.get('size', 'N/A')}"
            )

            st.write(
                f"**Formato:** {result['output_format'].upper()}"
            )

            st.write(
                f"**Qualidade:** {result.get('quality', 'N/A')}"
            )

            st.markdown("**Prompt utilizado:**")

            st.code(
                result["prompt"],
                language="text"
            )

    else:

        st.warning(
            "O arquivo da última geração não foi encontrado."
        )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")

st.caption(
    f"{Settings.APP_NAME} v{Settings.VERSION} "
    "| Powered by Cloudflare Workers AI"
)

