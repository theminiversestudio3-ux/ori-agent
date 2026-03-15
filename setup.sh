#!/bin/bash

# --- OriAgent Ultra: Universal Setup Script ---
# Optimized for Termux (Android) on Moto G32
# This script installs all dependencies, compiles the local LLM, 
# downloads a model, and starts the agent.

set -e # Exit on error

echo "🚀 Starting OriAgent Ultra Setup..."

# 1. Update System
echo "🔄 Updating system packages..."
pkg update -y && pkg upgrade -y

# 2. Install Core Dependencies
echo "📦 Installing system dependencies (Node.js, Python, C++, Git)..."
pkg install -y git nodejs python wget cmake ninja clang binutils build-essential lsof

# 3. Setup Python Environment
echo "🐍 Setting up Python Brain dependencies..."
pip install flask requests python-dotenv googlesearch-python beautifulsoup4

# 4. Setup Node.js Gateway
echo "📱 Setting up Node.js WhatsApp Gateway..."
cd gateway
npm install
cd ..

# 5. Local LLM Setup (llama.cpp)
if [ ! -d "llama.cpp" ]; then
    echo "🏗️ Cloning llama.cpp for local intelligence..."
    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp
    echo "🔨 Compiling llama.cpp (this may take a few minutes)..."
    cmake -B build
    cmake --build build --config Release -j$(nproc)
    cd ..
else
    echo "✅ llama.cpp already exists, skipping clone/compile."
fi

# 6. Download Model (Qwen-1.5B-Chat GGUF - Lightweight for old phones)
MODEL_DIR="llama.cpp/models"
MODEL_PATH="$MODEL_DIR/qwen-1.5b-chat.gguf"
mkdir -p $MODEL_DIR

if [ ! -f "$MODEL_PATH" ]; then
    echo "📥 Downloading lightweight 1.5B Model (Optimized for Moto G32)..."
    # Using a high-quality, small GGUF from HuggingFace
    wget -O "$MODEL_PATH" https://huggingface.co/Qwen/Qwen2-1.5B-Instruct-GGUF/resolve/main/qwen2-1.5b-instruct-q4_k_m.gguf
else
    echo "✅ Model already exists, skipping download."
fi

# 7. Process Management (PM2)
echo "⚙️ Setting up PM2 for background execution..."
npm install -g pm2

# 8. Create Default .env if not exists
if [ ! -f ".env" ]; then
    echo "📝 Creating default .env file..."
    echo "GEMINI_API_KEY=not_needed_for_local_mode" > .env
fi

# 9. Final Verification Script
cat <<EOF > check_health.sh
#!/bin/bash
echo "🔍 Checking OriAgent Health..."
pm2 status
echo "-----------------------------------"
curl -s http://localhost:8080/health || echo "❌ Local Model Server not responding yet."
curl -s http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message": "health check"}' || echo "❌ Brain API not responding yet."
EOF
chmod +x check_health.sh

# 10. Auto-Start everything
echo "🔥 Launching OriAgent Ultra..."
pm2 delete all 2>/dev/null || true
pm2 start llama.cpp/build/bin/llama-server --name "llama-server" -- -m $MODEL_PATH -t 4 -c 2048 --port 8080 --host 0.0.0.0
pm2 start brain/engine.py --name "brain-api" --interpreter python3
pm2 start gateway/index.js --name "wa-gateway" --interpreter node
pm2 save

echo "🎉 SETUP COMPLETE!"
echo "-------------------------------------------------------"
echo "1. Wait 1 minute for the model to load."
echo "2. Run 'pm2 logs wa-gateway' to see the WhatsApp QR code."
echo "3. Scan it and you're live!"
echo "-------------------------------------------------------"
