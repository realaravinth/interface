"""
Errors
"""
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
from flask import jsonify
from requests import Response


class Error(Exception):
    """Helper class for presenting errors in the format specified by the specification"""

    def __init__(self, errcode: str, error: str, status: int):
        super().__init__(error)
        self.__errcode = errcode
        self.__error = error
        self.__status = status

    def get_error(self):
        """Get error in serialziable form"""
        error = {}
        error["errcode"] = self.__errcode
        error["error"] = self.__error
        return error

    def status(self):
        """Get error status"""
        return self.__status

    def get_error_resp(self):
        """Get error response"""
        resp = jsonify(self.get_error())
        resp.status = self.__status
        return resp

    @staticmethod
    def from_resp(resp: Response):
        if resp.status_code != 200:
            data = resp.json()
            print(data)
            return Error(
                status=resp.status_code, error=data["error"], errcode=data["errcode"]
            )
        return None


F_D_INTERFACE_UNREACHABLE = Error(
    errcode="F_D_INTERFACE_UNREACHABLE",
    error="Interface unreachable",
    status=503,
)

F_D_INVALID_PAYLOAD = Error(
    errcode="F_D_INVALID_PAYLOAD",
    error="Please submit valid payload",
    status=400,
)

F_D_FORGE_UNKNOWN_ERROR = Error(
    errcode="F_D_FORGE_UNKNOWN_ERROR",
    error="Something went wrong on the Software Forge side",
    status=502,
)
