from setuptools import setup, find_packages

setup(
    name="nanobot-webchat-plugin",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=["nanobot-ai>=0.1.0", "websockets>=12.0"],
    entry_points={
        "nanobot.channels": [
            "webchat = nanobot_webchat.channel:WebchatChannel",
        ],
    },
)
