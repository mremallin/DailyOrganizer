#
# DailyOrganizer - A simple daily notes organizer for Sublime Text
# Copyright (C) 2021-2023 Mike Mallin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sublime
import sublime_plugin
import os
import shutil

from functools import wraps
from datetime import datetime

# Goals
# - Easy way to maintain structured notes that are not just transient in ST
# - New command to create a text/markdown file with a configurable folder structure
# - New command to create a meeting notes file within the same day

def get_folder_structure():
    settings = sublime.load_settings("DailyOrganizer.sublime-settings")
    return settings.get("folder_structure", "~/DailyOrganizer/%Y/%m/%d")


def get_main_notes_file_name():
    settings = sublime.load_settings("DailyOrganizer.sublime-settings")
    return settings.get("main_notes_file_name", "Today.txt")


def get_user_meeting_templates_folder():
    settings = sublime.load_settings("DailyOrganizer.sublime-settings")
    return settings.get("meeting_template_folder", "~/DailyOrganizer/MeetingTemplates")


def create_folder(folder):
    if not os.path.exists(folder):
        print("Creating notes folder:" + folder)
        os.makedirs(folder)


def get_current_folder():
    folder_path = datetime.now().strftime(get_folder_structure())
    folder_path = os.path.expanduser(folder_path)

    create_folder(folder_path)
    return folder_path


def get_current_file():
    return datetime.now().strftime(get_main_notes_file_name())


def create_note_file(file_name):
    if not os.path.exists(file_name):
        print("Creating note file " + file_name)
        note_file = open(file_name, "x")
        note_file.close()


def copy_template_into_note(note_file_name, template_file):
    shutil.copyfile(template_file, note_file_name)


def get_todays_note_file_path():
    return (get_current_folder() + "/" + get_current_file())


class OpenTodaysNoteCommand(sublime_plugin.WindowCommand):
    def run(self):
        note_file_path = get_todays_note_file_path()
        create_note_file(note_file_path)
        todays_note = self.window.open_file(note_file_path)

### This is a hack to work around the API of show_input_panel where the on_done callback
### only accepts a single input string. Still looking for a better way to come back to the
### same command object to complete the creation of the meeting file
new_meeting_obj = None

def got_meeting_file_name(file_name):
    global new_meeting_obj
    new_meeting_obj.create_meeting_file(file_name)
    new_meeting_obj = None


def cancel_meeting_file_name():
    new_meeting_obj = None


class MeetingTemplateChooserCommand(sublime_plugin.ListInputHandler):
    def get_list_of_user_meeting_template_files(self):
        user_templates_folder = get_user_meeting_templates_folder()
        user_templates_folder = os.path.expanduser(user_templates_folder)

        user_templates = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) \
                            in os.walk(user_templates_folder) for \
                                f in filenames]
        return user_templates


    def list_items(self):
        return sorted(self.get_list_of_user_meeting_template_files()) + ["None"]


class NewMeetingNoteCommand(sublime_plugin.WindowCommand):
    def input(self, args):
        return MeetingTemplateChooserCommand()


    def run(self, meeting_template_chooser_command):
        global new_meeting_obj
        self.chosen_meeting_template = meeting_template_chooser_command
        new_meeting_obj = self
        meeting_file_name_panel = self.window.show_input_panel(
            "Meeting File Name", "", got_meeting_file_name, None, cancel_meeting_file_name)


    def create_meeting_file(self, file_name):
        meeting_file_path = (get_current_folder() + "/" + file_name)

        # Make sure we don't overwrite user data with a template accidentally
        if not os.path.exists(file_name):
            create_note_file(meeting_file_path)
            if self.chosen_meeting_template != "None":
                copy_template_into_note(meeting_file_path, self.chosen_meeting_template)
        meeting_note = self.window.open_file(meeting_file_path)

