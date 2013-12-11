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
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

from sugar3.graphics import style
from jarabe.webservice import accountsmanager
from cpsection.webaccount.web_service import WebService


class WebService(WebService):

    def __init__(self):
        self._account = accountsmanager.get_account('sugarupload')
        self._timeout_id = None

    def _restore_user_data(self):
        client = GConf.Client.get_default()
        user = client.get_string(self._account.USER)
        password = client.get_string(self._account.PASSWORD)
        if user:
            self._entry_user.set_text(user)
        if password:
            self._entry_password.set_text(password)

    def __pressed_start_cb(self, entry, data=None):
        if self._timeout_id is not None:
            GLib.source_remove(self._timeout_id)
        self._timeout_id = GLib.timeout_add_seconds(2, self.__save_user_data_cb)

    def __save_user_data_cb(self):
        client = GConf.Client.get_default()
        user = self._entry_user.get_text()
        password = self._entry_password.get_text()
        client.set_string(self._account.USER, user)
        client.set_string(self._account.PASSWORD, password)

        self._timeout_id = None
        return False

    def get_icon_name(self):
        return 'sugarupload'

    def config_service_cb(self, widget, event, container):
        separator = Gtk.HSeparator()

        title = Gtk.Label(label=_('Upload files to PutLocker'))
        title.set_alignment(0, 0)
        title.set_line_wrap(True)

        info = Gtk.Label()
        here = "http://www.putlocker.com/authenticate.php?signup"
        markup = _("Please enter your username."
                   " You can register in "
                   "<a href='%s'>%s</a>" % (here, here))
        info.set_markup(markup)
        info.set_alignment(0, 0)
        info.set_line_wrap(True)

        user = Gtk.Label(_('User'))
        user.set_alignment(1, 0.5)
        user.modify_fg(Gtk.StateType.NORMAL,
                        style.COLOR_SELECTION_GREY.get_gdk_color())

        password = Gtk.Label(_('Password'))
        password.set_alignment(1, 0.5)
        password.modify_fg(Gtk.StateType.NORMAL,
                        style.COLOR_SELECTION_GREY.get_gdk_color())

        self._entry_user = Gtk.Entry()
        self._entry_user.set_size_request(int(Gdk.Screen.width() / 3), -1)

        self._entry_password = Gtk.Entry()
        self._entry_password.set_size_request(int(Gdk.Screen.width() / 3), -1)
        self._entry_password.set_visibility(False)

        self._entry_user.connect('key-press-event', self.__pressed_start_cb)
        self._entry_password.connect('key-press-event', self.__pressed_start_cb)

        grid = Gtk.Grid()
        grid.attach(user, 0, 1, 1, 1)
        grid.attach(self._entry_user, 1, 1, 1, 1)
        grid.attach(password, 0, 2, 1, 1)
        grid.attach(self._entry_password, 1, 2, 1, 1)
        grid.set_row_spacing(style.DEFAULT_SPACING)
        grid.set_column_spacing(style.DEFAULT_SPACING)

        vbox = Gtk.VBox()
        vbox.set_border_width(style.DEFAULT_SPACING * 2)
        vbox.set_spacing(style.DEFAULT_SPACING)
        vbox.pack_start(title, False, True, 0)
        vbox.pack_start(info, False, True, 0)
        vbox.pack_start(grid, False, True, 0)

        for c in container.get_children():
            container.remove(c)

        container.pack_start(separator, False, False, 0)
        container.pack_start(vbox, False, True, 0)
        container.show_all()

        self._restore_user_data()


def get_service():
    return WebService()
