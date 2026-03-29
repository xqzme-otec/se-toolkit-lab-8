#!/usr/bin/env python3
import subprocess
import sys
import os

# Сначала запускаем entrypoint.py в фоне (он запустит gateway)
gateway_proc = subprocess.Popen(
    [sys.executable, "/app/entrypoint.py"],
    env=os.environ
)

# Даём gateway время стартовать
import time
time.sleep(3)

# Теперь запускаем webchat-сервер
# (путь может отличаться, попробуем несколько вариантов)
webchat_paths = [
    "/app/nanobot-websocket-channel/nanobot-webchat/src/nanobot_webchat/server.py",
    "/app/nanobot-websocket-channel/nanobot-webchat/nanobot_webchat/__main__.py",
]

for path in webchat_paths:
    if os.path.exists(path):
        print(f"🚀 Starting webchat server from {path}")
        os.execvp(sys.executable, [sys.executable, path])
        break
else:
    print("⚠️  Webchat server not found, keeping gateway only")
    gateway_proc.wait()
