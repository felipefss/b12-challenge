import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
import requests

# ---------- payload construction ----------
now = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
timestamp = now.replace("+00:00", "Z")

github_action_run_link = os.environ.get("ACTION_RUN_LINK")

payload = {
    "timestamp": timestamp,
    "name": "Felipe Santos",
    "email": "felipefss@gmail.com",
    "resume_link": "https://www.linkedin.com/in/felipefss/",
    "repository_link": "https://github.com/felipefss/b12-challenge",
    "action_run_link": github_action_run_link,
}

# compact JSON string (no extra whitespace): the API expects exactly this form
payload_str = json.dumps(payload, separators=(",", ":"), sort_keys=True)

# ---------- compute signature ----------
secret = os.environ.get("SIGNING_SECRET").encode()

signature = hmac.new(
    secret,
    payload_str.encode("utf-8"),
    hashlib.sha256
).hexdigest()


# ---------- send request ----------
api_url = "https://play.svix.com/in/e_YiB7zoO0tTgOgL5RvmWw74h3KY4?echo_body=true"

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

response = requests.post(api_url, data=payload_str, headers=headers)
if response.status_code == 200:
    body = response.json()
    print("Receipt:", body.get("name"))