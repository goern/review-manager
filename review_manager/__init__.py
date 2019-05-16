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
import hmac

from flask import Flask, send_from_directory, jsonify, request


__version__ = "0.1.0-dev"


def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask("review-manager")

    @app.route("/healthz")
    # FIXME @metrics.do_not_track()
    def healthz():
        """This is a liveness and readyness probe for OpenShift."""
        return "OK"

    @app.route("/github", methods=["POST"])
    def handle_github_hook():
        """Entry point for GitHub webhook."""

        signature = request.headers.get("X-Hub-Signature")
        if signature == None:
            return jsonify({}), 200

        sha, signature = signature.split("=")

        secret = str.encode(os.environ.get("GITHUB_SECRET"))

        hashhex = hmac.new(secret, request.data, digestmod="sha1").hexdigest()
        if hmac.compare_digest(hashhex, signature):
            print("here we go")

        return jsonify({}), 200

    @app.route("/")
    def index():
        return f"This is Review Manager, {__version__}. Humans! Go away!"

    @app.route("/favicon.ico")
    # FIXME @metrics.do_not_track()
    def favicon():
        """Just return the favicon."""
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app
