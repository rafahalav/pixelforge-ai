#!/bin/bash

# PixelForge AI - Startup Script
# This script sets up the environment and runs the Streamlit application.

echo "🚀 Iniciando PixelForge AI..."

# 1. Verificar se o ambiente virtual existe, se não, criar
if [ ! -d "venv" ]; then
    echo "📦 Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar o ambiente virtual. Verifique se o Python 3 está instalado."
        exit 1
    fi
    echo "✅ Ambiente virtual criado com sucesso."
else
    echo "✅ Ambiente virtual encontrado."
fi

# 2. Ativar o ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# 3. Verificar e instalar dependências
if [ -f "requirements.txt" ]; then
    echo "📥 Verificando dependências..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo "✅ Dependências atualizadas."
else
    echo "⚠️ Arquivo requirements.txt não encontrado. Pulando instalação."
fi

# 4. Verificar arquivo .env
if [ ! -f ".env" ]; then
    echo "⚠️ Arquivo .env não encontrado!"
    echo "   Por favor, copie .env.example para .env e configure suas chaves da Cloudflare antes de continuar."
    echo "   (Você pode pausar este script com Ctrl+C, configurar e rodar novamente)"
    # Opcional: descomente a linha abaixo se quiser que o script pare aqui
    # exit 1
fi

# 5. Iniciar a aplicação Streamlit
echo "🎨 Iniciando a interface do PixelForge AI..."
streamlit run app.py
