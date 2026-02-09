#!/bin/bash

echo "🚀 Starting ArcGIS Copilot Setup..."
echo ""

# Check if ollama command exists
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is NOT installed on this system"
    echo ""
    echo "⚠️  You need to install Ollama first:"
    echo "   Visit: https://ollama.ai"
    echo "   Or use: brew install ollama (on macOS)"
    echo ""
    exit 1
fi

# Check if Ollama is running
echo "📡 Checking if Ollama server is running..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama server is NOT running"
    echo ""
    echo "🔧 Starting Ollama server in the background..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    OLLAMA_PID=$!
    echo "✅ Ollama started with PID: $OLLAMA_PID"
    echo ""
    echo "⏳ Waiting for Ollama to be ready..."
    sleep 3
else
    echo "✅ Ollama server is already running"
fi

# Check if llama3 model is available
echo ""
echo "📥 Checking if llama3 model is available..."
if ollama list | grep -q "llama3"; then
    echo "✅ llama3 model found"
else
    echo "⚠️  llama3 model not found, pulling it now..."
    echo "(This may take a few minutes...)"
    ollama pull llama3
fi

# Start Streamlit app
echo ""
echo "🎬 Starting Streamlit app..."
echo "📱 App will be available at: http://localhost:8501"
cd /workspaces/arcgis-copilot-poc
python -m streamlit run app.py --server.port 8501
