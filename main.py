import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
import requests

# payload construction
now = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
timestamp = now.replace("+00:00", "Z")

github_server_url = os.environ.get("GITHUB_SERVER_URL")
github_repository = os.environ.get("GITHUB_REPOSITORY")
github_run_id = os.environ.get("GITHUB_RUN_ID")
github_action_run_link = f"{github_server_url}/{github_repository}/actions/runs/{github_run_id}"

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

# compute signature
secret = os.environ.get("SIGNING_SECRET").encode()

signature = hmac.new(
    secret,
    payload_str.encode("utf-8"),
    hashlib.sha256
).hexdigest()


# send request
api_url = "https://b12.io/apply/submission"

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}


response = requests.post(api_url, data=payload_str, headers=headers)
print(f"Response status code: {response.status_code}")
print(f"Response body: {response.text}")

if response.status_code == 200:
    body = response.json()
    receipt = body.get("receipt")
    print(f"Receipt: {receipt}")