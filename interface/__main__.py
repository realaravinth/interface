#!venv/bin/python
"""
Run ForgeFed Interface flask application
"""
# Bridges software forges to create a distributed software development environment
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
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from dynaconf import settings
from interface.app import create_app
from interface.runner import runner

if __name__ == "__main__":
    app = create_app()
    worker = runner.init_app(app)
    port = int(settings.SERVER.url.split(":").pop())
    app.run(threaded=True, host=settings.SERVER.ip, port=port)
    worker.kill()
