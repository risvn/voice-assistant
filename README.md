# 🧠🎙️ PILL – Pi LLaMA Voice-to-Voice AI Assistant

**PILL** (Pi LLaMA) is an offline, privacy-first, real-time voice assistant powered by Whisper (STT), TinyLLaMA (LLM), and Piper (TTS), built specifically for the Raspberry Pi 4. It was created as a Bachelor's Major Project to demonstrate an end-to-end voice interaction system on constrained hardware.

---

## 🔧 Key Features

- 🎤 Real-time voice input and output
- 🧠 LLM-powered response with TinyLLaMA (via llama.cpp)
- 🗣️ Natural-sounding speech via Piper TTS
- 🐧 Fully local and open-source
- 🍓 Optimized for Raspberry Pi 4

---

## 🗂️ Project Structure

```bash
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

## 🔁 Workflow Overview

### 🗣️ 1. User Speaks
Microphone input is captured via PyAudio.

### 🧏 2. Speech-to-Text (STT)
Audio stream is transcribed in real-time using [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) running a base or tiny model.

**Result:** `"What’s the weather today?"`

### 🧠 3. Text Generation with LLaMA
Transcribed text is sent to [TinyLLaMA](https://huggingface.co/TinyLlama) running via [llama.cpp](https://github.com/ggerganov/llama.cpp) with a lightweight quantized model (e.g., 3B Q4_K_M).

Context is preserved to maintain conversation state.

**Result:** `"I'm not connected to the internet, but it's always sunny with me!"`

### 🗣️ 4. Text-to-Speech (TTS)
Generated response is passed to [Piper TTS](https://github.com/rhasspy/piper) using a selected voice model.

Audio is streamed back to the speaker in real time.

## 🛠 Dependencies

* [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) – Real-time STT
* [LLaMA.cpp](https://github.com/ggerganov/llama.cpp) – TinyLLaMA inference
* [Piper TTS](https://github.com/rhasspy/piper) – Lightweight TTS engine

# setup.sh
mkdir -p stt/models llm/models tts/voice/libritts_r
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin -P stt/models/
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US-libritts_r-medium.onnx -P tts/voice/libritts_r/


### Build Whisper, LLaMA, Piper
Follow official repo instructions or use your own builds and place the binaries in:
## 🧠 Models & Binaries

### 1. Whisper (STT)
* **🔧 Binary:** `whisper-cli` (from [whisper.cpp](https://github.com/ggerganov/whisper.cpp))
    ```
    📁 Path: stt/bin/whisper-cli
    ```
* **📄 Model File:** `ggml-tiny.bin`
    ```
    📁 Path: stt/models/ggml-tiny.bin
    ```
    ```bash
    # Download model
    wget [https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin) -P stt/models/
    ```

### 2. TinyLLaMA (LLM)
* **🔧 Binary:** `llama-cli` (from [llama.cpp](https://github.com/ggerganov/llama.cpp))
    ```
    📁 Path: llm/bin/llama-cli
    ```
* **📄 Model File:** `tinyllama_1b_q4_chat.gguf`
    ```
    📁 Path: llm/models/tinyllama_1b_q4_chat.gguf
    ```
    ```bash
    # Example download source (you may need to convert to GGUF format):
    wget [https://huggingface.co/cognitivecomputations/TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/cognitivecomputations/TinyLlama-1.1B-Chat-v1.0) -O /tmp/tinyllama.pth
    # (Conversion to GGUF not shown here - refer to llama.cpp documentation)
    # Move the converted GGUF file to llm/models/tinyllama_1b_q4_chat.gguf
    ```
    Make sure your version is quantized (e.g., Q4 or Q5) for Raspberry Pi compatibility.

### 3. Piper (TTS)
* **🔧 Binary:** `piper` (from [piper](https://github.com/rhasspy/piper))
    ```
    📁 Path: tts/piper/piper
    ```
* **📄 Voice Model:** `en_US-libritts_r-medium.onnx`
    ```
    📁 Path: tts/voice/libritts_r/en_US-libritts_r-medium.onnx
    ```
    ```bash
    # Download from official model list:
    # [https://huggingface.co/rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices)

    # Example:
    wget [https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US-libritts_r-medium.onnx](https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US-libritts_r-medium.onnx) -P tts/voice/libritts_r/
    ```

## ✅ Additional Notes

### Audio Format Requirements:

* WAV
* Mono
* 16-bit
* 16000 Hz sample rate

### Environment Variables:

Set `LD_LIBRARY_PATH` to include `llm/bin` for `llama.cpp` dynamic libraries:

```bash
export LD_LIBRARY_PATH=llm/bin:$LD_LIBRARY_PATH
Hardware Tested:
Raspberry Pi 4 (4GB/8GB)
USB mic or onboard mic (via arecord)
📁 Directory Summary
Bash

stt/
├── bin/whisper-cli
└── models/ggml-tiny.bin

llm/
├── bin/llama-cli
└── models/tinyllama_1b_q4_chat.gguf

tts/
├── piper/piper
└── voice/libritts_r/en_US-libritts_r-medium.onnx
🧪 Verification
After setup, you can test each module separately:

Whisper:
Bash

./stt/bin/whisper-cli ../audio/speech.wav --model ../stt/models/ggml-tiny.bin
LLaMA:
Bash

./llm/bin/llama-cli -m ../llm/models/tinyllama_1b_q4_chat.gguf -p "Hello, who are you?" -n 50
Piper:
Bash

./tts/piper/piper --model ../tts/voice/libritts_r/en_US-libritts_r-medium.onnx --text "Hello, world." --output_file output.wav
# Play the output audio file (e.g., using aplay on Linux):
# aplay output.wav
