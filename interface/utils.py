# Bridges software forges to create a distributed software development environment
# Copyright © 2021 Aravinth Manivannan <realaravinth@batsense.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import random
import string
from urllib.parse import urlparse, urlunparse
import requests

from interface.meta import VERSIONS


def clean_url(url: str):
    """Remove paths and tracking elements from URL"""
    parsed = urlparse(url)
    cleaned = urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
    return cleaned


def trim_url(url: str) -> str:
    if url.endswith("/"):
        url = url[0:-1]
    return url


def verify_interface_online(url: str, version: str = None):
    """Verify if interface instance is reachable"""
    parsed = urlparse(url)
    path = "/_ff/interface/versions"
    url = urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if version:
                return version in data["versions"]
            return "versions" in data and len(data["versions"]) != 0
        return False
    except Exception as _:
        return False


def get_rand(len: int) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(len)
    )
