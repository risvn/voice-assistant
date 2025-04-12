#!/bin/bash

# Ensure required directories exist
echo "Creating necessary directories..."
mkdir -p stt/models llm/models tts/voice/libritts_r

# Download Whisper model
echo "Downloading Whisper model..."
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin -P stt/models/

# Download LLaMA model
echo "Downloading LLaMA model..."
wget https://huggingface.co/cognitivecomputations/TinyLlama-1.1B-Chat-v1.0/resolve/main/tinyllama_1b_q4_chat.gguf -P llm/models/

# Download Piper TTS model
echo "Downloading Piper TTS model..."
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US-libritts_r-medium.onnx -P tts/voice/libritts_r/

# Notify user of completion
echo "Setup completed successfully! You can now run the voice assistant."
