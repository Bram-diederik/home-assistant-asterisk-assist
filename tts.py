#!/usr/bin/env python3
import sys
import os
import subprocess

# --- Configuration ---
lang = sys.argv[1] if len(sys.argv) > 1 else None
message = sys.argv[2] if len(sys.argv) > 2 else None
tts = "google"  # or "google"
piper_en = "en_US-lessac-medium.onnx"
piper_nl = "nl-NL-mark-medium.onnx"
dir = "/usr/share/asterisk/sounds/en_US_f_Allison/"
messageFile = "sascha-longmessage"
gsm_path = os.path.join(dir, messageFile + ".gsm")

if not lang or not message:
    print("Usage: genttslong.py <lang> <message>")
    sys.exit(1)

# --- Sanitization ---
message = message.replace("'", "")

# --- Check existing file ---
if os.path.exists(gsm_path):
    print(messageFile)
    sys.exit(0)

# --- Synthesis ---
retval = 1

try:
    if tts == "google":
        cmd = f"gtts-cli -l {lang} '{message}' | sox -t mp3 - -r 8000 -c1 {gsm_path}"
    elif tts == "piper":
        model = piper_nl if lang == "nl" else piper_en
        cmd = f"echo '{message}' | piper --model {model} --download-dir /opt/piper/ --data-dir /opt/piper/ | sox -t wav - -r 8000 -c1 {gsm_path}"
    else:
        print("Unsupported TTS engine")
        sys.exit(2)

    retval = subprocess.call(cmd, shell=True)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(3)

# --- Result ---
if retval == 0 or os.path.exists(gsm_path):
    print(messageFile)
    sys.exit(0)
else:
    sys.exit(4)
