#!/usr/bin/env python3
"""
Simple launcher for ArcGIS Copilot that handles Ollama connectivity
"""
import subprocess
import sys
import time
import requests

def check_ollama():
    """Check if Ollama server is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama server is running")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Ollama server is NOT running on localhost:11434")
        return False
    except Exception as e:
        print(f"⚠️  Error checking Ollama: {e}")
        return False

def main():
    print("🚀 ArcGIS Copilot Launcher")
    print("=" * 50)
    
    # Check Ollama
    if not check_ollama():
        print("\n⚠️  Ollama is required but not running!")
        print("\nTo start Ollama:")
        print("  1. Install from https://ollama.ai")
        print("  2. Run: ollama serve")
        print("  3. Download model: ollama pull llama3 (in another terminal)")
        print("\nContinuing without Ollama - the app will show an error message.")
    
    # Start Streamlit
    port = "8502"  # Use 8502 if 8501 is already in use
    print(f"\n🎬 Starting Streamlit app on http://localhost:{port}")
    print("=" * 50)
    
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "/workspaces/arcgis-copilot-poc/app.py",
        "--server.port", port
    ])

if __name__ == "__main__":
    main()
