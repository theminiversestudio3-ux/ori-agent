#!/bin/bash
# Clean up old processes
echo "🧹 Cleaning up old OriAgent processes..."
pkill -f engine.py 2>/dev/null
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
sleep 1

# Start the Python Brain
echo "🧠 Starting the Brain (Python)..."
python3 ori-agent/brain/engine.py > ori-agent/brain.log 2>&1 &
BRAIN_PID=$!

# Wait for brain to start
sleep 3
if ! ps -p $BRAIN_PID > /dev/null; then
    echo "❌ Brain failed to start. Check ori-agent/brain.log"
    exit 1
fi
echo "✅ Brain is running (PID: $BRAIN_PID)"

# Start the WhatsApp Gateway
echo "📱 Starting the Gateway (Node.js)..."
node ori-agent/gateway/index.js
