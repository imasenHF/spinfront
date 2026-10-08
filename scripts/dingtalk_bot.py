"""Reusable DingTalk webhook sender for SpinFront automation.

The actual webhook values are provided by GitHub Actions secret:
DINGTALK_WEBHOOKS

Expected JSON format:
{
  "spinfront": "https://oapi.dingtalk.com/robot/send?...",
  "other_group": "https://oapi.dingtalk.com/robot/send?..."
}
"""

import json
import os
from typing import Dict

import requests


class DingTalkBot:
    def __init__(self, target: str = "spinfront"):
        self.target = target
        self.webhooks = self._load_webhooks()

    @staticmethod
    def _load_webhooks() -> Dict[str, str]:
        value = os.environ.get("DINGTALK_WEBHOOKS")
        if not value:
            raise RuntimeError("Missing DINGTALK_WEBHOOKS secret")
        return json.loads(value)

    def send_markdown(self, title: str, text: str):
        if self.target not in self.webhooks:
            raise KeyError(f"Unknown DingTalk target: {self.target}")

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text,
            },
        }

        response = requests.post(
            self.webhooks[self.target],
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        result = response.json()

        if result.get("errcode") != 0:
            raise RuntimeError(result)

        return result
