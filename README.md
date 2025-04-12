# 🧠 PILL: Pi LLaMA Voice-to-Voice AI Assistant

**PILL** (Pi LLaMA) is an offline, fully local voice assistant for Raspberry Pi, integrating:

- 🎙️ **Whisper.cpp** — Speech-to-Text (STT)
- 🧠 **TinyLLaMA (via llama.cpp)** — Language Model for text generation
- 🔊 **Piper TTS** — Text-to-Speech (TTS)

Built as a **Bachelor's Major Project**, it delivers real-time, low-latency voice interactions on constrained hardware.

---

## 📁 Project Structure

```
pill/
├── audio/                          # Temporary audio files
│   └── speech.wav
├── bin/                            # Executable scripts
│   ├── run.sh                      # Main voice-to-voice pipeline
│   ├── speak                       # TTS wrapper
│   └── tokens                      # LLaMA wrapper
├── stt/
│   ├── bin/                        # Whisper binary
│   └── models/                     # Whisper model (e.g. ggml-tiny.bin)
├── llm/
│   ├── bin/                        # llama.cpp binary and shared libs
│   └── models/                     # GGUF LLaMA models
├── tts/
│   ├── piper/                      # Piper binary
│   └── voice/                      # ONNX voice models
├── requirements.txt
└── README.md
```

---

## 🔁 Workflow Overview

### 🗣️ 1. User Speaks
- Audio is recorded with a microphone and saved to `audio/speech.wav`.

### 🧏 2. Speech-to-Text (STT)
- Audio is transcribed using Whisper.cpp with a small model like `ggml-tiny.bin`.

### 🧠 3. Text Generation with LLaMA
- Transcribed text is passed to TinyLLaMA via `llama.cpp`.
- A quantized model (Q4/Q5) ensures fast inference on Raspberry Pi.

### 🔊 4. Text-to-Speech (TTS)
- Piper TTS synthesizes the response using a pre-downloaded ONNX voice model.

---

## 🛠️ Step-by-Step Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pill.git
cd pill
```

### 2️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Build/Download Binaries

- **Whisper.cpp:** Build `main` as `whisper-cli`
- **llama.cpp:** Build `main` as `llama-cli`
- **Piper:** Build binary and required shared libs

Place them in:
```
stt/bin/whisper-cli
llm/bin/llama-cli
tts/piper/piper
```

### 4️⃣ Download Models

#### Whisper Model

```bash
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin -P stt/models/
```

#### TinyLLaMA (GGUF)

- Source: https://huggingface.co/cognitivecomputations/TinyLlama-1.1B-Chat-v1.0

Ensure format is `.gguf` and quantized (e.g., Q4_K_M):

```bash
# Example (after conversion if needed)
mv <downloaded>.gguf llm/models/tinyllama_1b_q4_chat.gguf
```

#### Piper Voice Model

```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US-libritts_r-medium.onnx -P tts/voice/libritts_r/
```

---

## ⚙️ Environment Configuration

Ensure `llm/bin` is in your shared library path:

```bash
export LD_LIBRARY_PATH=llm/bin:$LD_LIBRARY_PATH
```

---

## 🚀 Run the Assistant

```bash
cd bin
./run.sh
```

This pipeline will:
1. Record audio from mic
2. Transcribe with Whisper
3. Generate reply with LLaMA
4. Speak with Piper

---

## 🧪 Manual Testing

### Whisper (STT)

```bash
./stt/bin/whisper-cli ../audio/speech.wav --model ../stt/models/ggml-tiny.bin
```

### LLaMA (LLM)

```bash
./llm/bin/llama-cli -m ../llm/models/tinyllama_1b_q4_chat.gguf -p "Hello, who are you?" -n 50
```

### Piper (TTS)

```bash
./tts/piper/piper --model ../tts/voice/libritts_r/en_US-libritts_r-medium.onnx --text "Hello, I am your Pi assistant."
```

---



## 🧠 Hardware Requirements

- Raspberry Pi 4 (4GB or 8GB)
- USB Microphone (or onboard mic)
- Speakers (3.5mm jack or HDMI)
- MicroSD card (32GB+ recommended)

---

## 📅 Last Updated

April 12, 2025
