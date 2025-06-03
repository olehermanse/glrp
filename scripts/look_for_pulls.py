import sys
import os

import requests

pat = os.getenv("GH_PAT")

for line in sys.stdin:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {pat}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    line = line.replace("github.com", "api.github.com/repos").replace("/commit/", "/commits/").strip() + "/pulls"
    r = requests.get(line, headers=headers)
    if r.status_code != 200:
        print("Bad status code: " + str(r.status_code) + " " + line)
    data = r.json()
    if len(data) == 0:
        print("Empty: " + line)
        continue
    target = data[0]["url"]
    print(line + " -> " + target)
