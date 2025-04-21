import sys
import subprocess
from get_info.wiki import get_summary

# your Wikipedia content
qurey=sys.argv[1]
wiki_text = get_summary(qurey)

#voice models
piper="../tts/piper/piper"
tts_model="../tts/voice/hfc_female/hfc_female.onnx"

piper_cmd = [
    "../tts/piper/piper",
    "--model", "../tts/voice/hfc_female/hfc_female.onnx",
    "--output-raw"  # stream audio as raw PCM
]

aplay_cmd=["aplay", "-f", "S16_LE", "-r", "22050", "-c", "1"]

# Start both Piper and ffplay
piper = subprocess.Popen(piper_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
aplay = subprocess.Popen(aplay_cmd, stdin=piper.stdout)

# Send text to Piper
piper.stdin.write(wiki_text.encode("utf-8"))
piper.stdin.close()

# Wait for both to finish
aplay.wait()
piper.wait()
