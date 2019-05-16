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


from flask import Flask, current_app, send_from_directory, jsonify, request

from prometheus_client import multiprocess
from prometheus_client.core import CollectorRegistry
from prometheus_flask_exporter import PrometheusMetrics

from review_manager import create_app, __version__


DEBUG = bool(os.getenv("DEBUG", False))


daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger("label_checker")

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


app = create_app()


if __name__ == "__main__":
    logger.info(f"Review Manager v{__version__}")
    logger.debug("... and I am running in DEBUG mode!")

    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry, path="/tmp")
    metrics = PrometheusMetrics(app, registry=registry)

    metrics.info("app_info", "Review Manager info", version=f"v{__version__}")

    # TODO figure out why prometheus metrics are not exported if we run with DEBUG=1
    app.run(host="0.0.0.0", port=8080, debug=DEBUG)

