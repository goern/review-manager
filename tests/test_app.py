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


import pytest

import review_manager


def test_metrics(client):
    """Let's see if we have some metrics."""

    r = client.get("/metrics")
    assert f'app_info{{version="{review_manager.__version__}"}} 1.0' in str(r.data)


def test_index(client):
    """Get the banner and done..."""

    r = client.get("/")
    assert (
        f"This is Review Manager, {review_manager.__version__}. Humans! Go away!"
        in str(r.data)
    )
