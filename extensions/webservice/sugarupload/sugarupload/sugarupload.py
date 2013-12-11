# Copyright (c) 2013 Ignacio Rodriguez <ignacio@sugarlabs.org>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gettext import gettext as _

from gi.repository import GConf
import xml.etree.ElementTree as ET

from .grestful.object import Object
from .grestful.decorators import asynchronous
from .grestful.helpers import param_upload

client = GConf.Client.get_default()


class Upload(Object):
    UPLOAD_SERVER = 'http://upload.putlocker.com/uploadapi.php'

    @asynchronous
    def upload(self, path, user, password):
        user = client.get_string(user)
        password = client.get_string(password)
        params = [('user', user),
                ('password', password)]

        self._post(self.UPLOAD_SERVER, params,
            param_upload('file', path))

    def _completed_cb(self, data):
        data = "<data>%s</data>" % data

        xml = ET.fromstring(data)
        message = xml[0].text

        if len(xml) > 1:
            link = xml[1].text

        alert_title = _('Upload service')

        if len(xml) > 1:
            self.emit('completed', [alert_title, message, link])
        else:
            self.emit('failed', [alert_title, message])
