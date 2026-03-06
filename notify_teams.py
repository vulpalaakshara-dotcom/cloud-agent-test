import os
import sys
import json
import requests

TEAMS_WEBHOOK_URL = os.environ["TEAMS_WEBHOOK_URL"]

COMMIT_MESSAGE = os.environ.get(
    "COMMIT_MESSAGE",
    "Update print statement in test.py to change output to 'testing'",
)
BRANCH_NAME = os.environ.get("BRANCH_NAME", "main")
REPO_URL = os.environ.get(
    "REPO_URL", "https://github.com/vulpalaakshara-dotcom/cloud-agent-test"
)
REPO_NAME = REPO_URL.rstrip("/").split("/")[-1]

card = {
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "New changes pushed",
                        "weight": "Bolder",
                        "size": "Large",
                    },
                    {
                        "type": "TextBlock",
                        "text": COMMIT_MESSAGE,
                        "wrap": True,
                    },
                    {
                        "type": "FactSet",
                        "facts": [
                            {"title": "Repository", "value": REPO_NAME},
                            {"title": "Branch", "value": BRANCH_NAME},
                        ],
                    },
                ],
            },
        }
    ],
}

response = requests.post(
    TEAMS_WEBHOOK_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(card),
    timeout=15,
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code not in (200, 202):
    sys.exit(1)
