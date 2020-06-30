# window.py
#
# Copyright 2020 Latesil
#
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

from gi.repository import Gtk, GLib, Gio
import re
import os

@Gtk.Template(resource_path='/org/github/Latesil/project-starter/window.ui')
class ProjectStarterWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ProjectStarterWindow'

    switch_btn = Gtk.Template.Child()
    second_btn = Gtk.Template.Child()
    change_path_btn = Gtk.Template.Child()
    main_view = Gtk.Template.Child()
    lang_btn = Gtk.Template.Child()
    template_btn = Gtk.Template.Child()
    lang_btn_box = Gtk.Template.Child()
    template_btn_box = Gtk.Template.Child()
    lang_revealer = Gtk.Template.Child()
    template_revealer = Gtk.Template.Child()
    project_name_entry = Gtk.Template.Child()
    project_id_entry = Gtk.Template.Child()
    path_entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_path = ""
        self.switch_btn.props.sensitive = False
        self.project_name_ready = False
        self.project_id_ready = False

    @Gtk.Template.Callback()
    def on_switch_btn_clicked(self, w):
        self.main_path = self.path_entry.props.text
        if self.main_path[0] == '~':
            self.main_path = GLib.get_home_dir() + self.main_path[1:]
        if not os.path.exists(self.main_path):
            os.makedirs(self.main_path)
        self.main_view.set_visible_child_name('page1')

    @Gtk.Template.Callback()
    def on_second_btn_clicked(self, w):
        GLib.spawn_async(['/usr/bin/xdg-open', self.main_path])
        self.close() #self.main_view.set_visible_child_name('page0')

    @Gtk.Template.Callback()
    def on_change_path_btn_clicked(self, btn):
        pass

    @Gtk.Template.Callback()
    def on_lang_btn_clicked(self, btn):
        if self.template_revealer.get_reveal_child():
            self.template_revealer.set_reveal_child(False)

        if self.lang_revealer.get_reveal_child():
            self.lang_revealer.set_reveal_child(False)
        else:
            self.lang_revealer.set_reveal_child(True)

    @Gtk.Template.Callback()
    def on_template_btn_clicked(self, btn):
        if self.lang_revealer.get_reveal_child():
            self.lang_revealer.set_reveal_child(False)

        if self.template_revealer.get_reveal_child():
            self.template_revealer.set_reveal_child(False)
        else:
            self.template_revealer.set_reveal_child(True)

    @Gtk.Template.Callback()
    def on_project_name_entry_changed(self, e):
        if self.check_entry(e, self.check_project_name):
            self.project_name_ready = True
            self.ready_check()


    @Gtk.Template.Callback()
    def on_project_id_entry_changed(self, e):
        if self.check_entry(e, self.check_project_id):
            self.project_id_ready = True
            self.ready_check()


    ##########################################################################

    def check_entry(self, e, func):
        text = e.props.text
        e.props.secondary_icon_name = ''
        if text:
            if not func(text):
                e.props.secondary_icon_name = 'dialog-warning-symbolic'
                return False
            else:
                e.props.secondary_icon_name = ''
                return True

    def check_project_name(self, text):
        if text:
            return False if text[0].isdigit() or re.search('\s', text) or not text.islower() else True

    def check_project_id(self, text):
        if text:
            return True if re.match('[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+', text) else False

    def ready_check(self):
        self.switch_btn.props.sensitive = True if self.project_name_ready and self.project_id_ready else False

        
