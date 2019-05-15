#!/usr/bin/env python3
# Review Manager
# Copyright(C) 2019 Christoph Görn
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""The Review Manager will manage the review process of Pull Requests on GitHub."""


import os
import logging
import hmac

import daiquiri


from flask import Flask, send_from_directory, jsonify, request

from prometheus_client import multiprocess
from prometheus_client.core import CollectorRegistry
from prometheus_flask_exporter import PrometheusMetrics

from review_manager import __version__


app = Flask(__name__)

registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry, path="/tmp")

metrics = PrometheusMetrics(app, registry=registry)

metrics.info("app_info", "Review Manager info", version=f"v{__version__}")


@app.route("/healthz")
@metrics.do_not_track()
def test():
    return "OK"


@app.route("/favicon.ico")
@metrics.do_not_track()
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/github", methods=["POST"])
def handle_github_hook():
    """Entry point for GitHub webhook """

    signature = request.headers.get("X-Hub-Signature")
    if signature == None:
        return jsonify({}), 200

    sha, signature = signature.split("=")

    secret = str.encode(os.environ.get("GITHUB_SECRET"))

    hashhex = hmac.new(secret, request.data, digestmod="sha1").hexdigest()
    if hmac.compare_digest(hashhex, signature):
        print("here we go")

    return jsonify({}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

