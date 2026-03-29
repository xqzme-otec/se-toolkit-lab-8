#!/usr/bin/env python3
import json
import os

def main():
    config_path = os.environ.get("NANOBOT_CONFIG", "/app/nanobot/config.json")
    workspace = os.environ.get("NANOBOT_WORKSPACE", "/app/nanobot/workspace")
    resolved_path = "/app/config.resolved.json"

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # LLM
    if "providers" in config and "custom" in config["providers"]:
        config["providers"]["custom"]["apiKey"] = os.environ.get("LLM_API_KEY", "")
        config["providers"]["custom"]["apiBase"] = os.environ.get("LLM_API_BASE_URL", "")
    
    if "agents" in config and "defaults" in config["agents"]:
        config["agents"]["defaults"]["model"] = os.environ.get("LLM_API_MODEL", "coder-model")
    
    # Gateway
    if "gateway" not in config:
        config["gateway"] = {}
    config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790"))
    
    # Webchat канал
    if "channels" not in config:
        config["channels"] = {}
    if "webchat" not in config["channels"]:
        config["channels"]["webchat"] = {}
    config["channels"]["webchat"]["enabled"] = True
    config["channels"]["webchat"]["host"] = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    config["channels"]["webchat"]["port"] = int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765"))
    config["channels"]["webchat"]["allowFrom"] = ["*"]

    with open(resolved_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace])

if __name__ == "__main__":
    main()
