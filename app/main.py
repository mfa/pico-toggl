import datetime
import json
from base64 import b64encode
from functools import cache
from pathlib import Path

from flask import Flask, jsonify
from requests import request

app = Flask(__name__)


@cache
def secrets(key):
    return json.load(open(Path(__file__).parent.parent / ".secrets")).get(key)


def toggl_api(method, path, data=None):
    headers = {
        "content-type": "application/json",
        "Authorization": "Basic %s"
        % b64encode(f"{secrets('token')}:api_token".encode()).decode("ascii"),
    }
    data = request(
        method,
        f"https://api.track.toggl.com/api/v9{path}",
        headers=headers,
        **{"json": data} if data else {},
    )
    return data.json()


def toggle():
    if current := toggl_api("GET", "/me/time_entries/current"):
        return toggl_api(
            "PATCH",
            f"/workspaces/{secrets('workspace_id')}/time_entries/{current['id']}/stop",
        )
    return toggl_api(
        "POST",
        f"/workspaces/{secrets('workspace_id')}/time_entries",
        {
            "created_with": "pico",
            "description": "working",
            "duration": -1,
            "workspace_id": secrets("workspace_id"),
            "start": f"{datetime.datetime.utcnow().replace(microsecond=0).isoformat()}Z",
            "pid": secrets("project_id"),
        },
    )


@app.route("/")
def index_view():
    return "nothing to see"


@app.route("/state")
def state_view():
    if result := toggl_api("GET", "/me/time_entries/current"):
        return jsonify(result)
    return jsonify({"started": False})


@app.route("/toggle")
def toggle_view():
    return jsonify(toggle())
