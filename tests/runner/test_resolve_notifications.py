""" Test errors helper class"""
# Interface ---  API-space federation for software forges
# Copyright © 2022 Aravinth Manivannan <realaravinth@batsense.net>
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
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from datetime import datetime

import pytest
from rfc3339 import rfc3339
from dynaconf import settings

from interface.app import create_app
from interface.forges.notifications import ISSUE, PULL, Notification, Comment
from interface.runner.events import resolve_notification, PrEvent, IssueEvent

from tests.test_utils import register_ns
from tests.forges.gitea.test_utils import register_gitea


def test_notifications_resolve(client, requests_mock):
    """Test resolve_notification"""
    id_ = "1"
    state = "open"
    updated_at = rfc3339(datetime.now())
    title = "test notification"
    upstream = "https://git.batsense.net/forgefedv2/interface"
    html_url = f"{upstream}/issues/8"
    repo_url: str = upstream

    comment = Comment(
        body=upstream, updated_at=updated_at, author=title, id=id_, url=upstream
    )

    notification = Notification(
        id=id_,
        type=ISSUE,
        state=state,
        updated_at=updated_at,
        title=title,
        upstream=upstream,
        repo_url=repo_url,
        web_url=html_url,
    )
    with pytest.raises(Exception) as _:
        resolve_notification(notification)

    notification.pr_url = upstream
    with pytest.raises(Exception) as _:
        resolve_notification(notification)

    repo_url = f"https://git.batsense.net/{settings.GITEA.username}/foo"
    notification.repo_url = repo_url
    web_url = f"{repo_url}/issues/9"
    notification.web_url = web_url
    with pytest.raises(Exception) as _:
        resolve_notification(notification)

    notification.comment = comment
    resolved = resolve_notification(notification)
    isinstance(resolved, IssueEvent)

    notification = Notification(
        id=id_,
        type=PULL,
        state=state,
        updated_at=updated_at,
        title=title,
        repo_url=repo_url,
        web_url=web_url,
    )
    with pytest.raises(Exception) as _:
        resolve_notification(notification)

    notification.pr_url = upstream
    with pytest.raises(Exception) as _:
        resolve_notification(notification)

    notification.repo_url = f"https://git.batsense.net/{settings.GITEA.username}/foo"
    print(notification.repo_url)
    with pytest.raises(Exception) as _:
        resolve_notification(notification)

    notification.upstream = upstream
    resolved = resolve_notification(notification)
    isinstance(resolved, PrEvent)
