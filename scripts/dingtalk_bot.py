"""Reusable DingTalk webhook sender for SpinFront automation.

Webhook values are provided by GitHub Actions secret:
SPINFRONT_DINGTALK_WEBHOOKS

Expected JSON format:
{
  "ciqtek": {
    "enabled": true,
    "webhook": "https://oapi.dingtalk.com/robot/send?..."
  },
  "test": {
    "enabled": false,
    "webhook": "https://oapi.dingtalk.com/robot/send?..."
  }
}

All enabled targets receive the same message. Adding or disabling a target
only requires editing the secret value.
"""

import json
import os
from typing import Dict, Any

import requests


class DingTalkBot:
    def __init__(self):
        self.webhooks = self._load_webhooks()

    @staticmethod
    def _load_webhooks() -> Dict[str, Any]:
        value = os.environ.get("SPINFRONT_DINGTALK_WEBHOOKS")
        if not value:
            raise RuntimeError("Missing SPINFRONT_DINGTALK_WEBHOOKS secret")
        return json.loads(value)

    def send_markdown(self, title: str, text: str):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text,
            },
        }

        results = {}

        for name, config in self.webhooks.items():
            if not config.get("enabled", False):
                continue

            webhook = config.get("webhook")
            if not webhook:
                raise ValueError(f"Missing webhook for target: {name}")

            response = requests.post(
                webhook,
                json=payload,
                timeout=20,
            )
            response.raise_for_status()

            result = response.json()
            if result.get("errcode") != 0:
                raise RuntimeError(f"DingTalk target {name} failed: {result}")

            results[name] = result

        if not results:
            raise RuntimeError("No enabled DingTalk webhook targets")

        return results
