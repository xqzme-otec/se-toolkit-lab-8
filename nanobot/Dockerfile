FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir nanobot-ai websockets

COPY entrypoint.py /app/entrypoint.py
COPY config.json /app/config.json

COPY --from=repo nanobot-websocket-channel /app/nanobot-websocket-channel

RUN pip install --no-cache-dir --ignore-requires-python -e /app/nanobot-websocket-channel/nanobot-channel-protocol -e /app/nanobot-websocket-channel/nanobot-webchat -e /app/nanobot-websocket-channel/mcp-webchat

ENV PYTHONPATH="/app:/app/mcp"

CMD ["python", "/app/entrypoint.py"]
