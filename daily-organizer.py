import sublime
import sublime_plugin
import os

from functools import wraps
from datetime import datetime

# Goals
# - Easy way to maintain structured notes that are not just transient in ST
# - New command to create a text/markdown file with a configurable folder structure
# - New command to create a meeting notes file within the same day

def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls, *args, **kwargs)
        return instance
    orig_cls.__new__ = __new__
    return orig_cls

@singleton
class DailyOrganizerConfig():
    def __init__(self):
        self.settings = sublime.load_settings("daily-organizer.sublime-settings")

    def get_folder_structure(self):
        return self.settings.get("folder_structure", "~/DailyOrganizer/%Y/%m/%d")

    def get_main_notes_file_name(self):
        return self.settings.get("main_notes_file_name", "Organizer.txt")

def create_folder(folder):
    if not os.path.exists(folder):
        print("Creating notes folder:" + folder)
        os.makedirs(folder)

def get_current_folder():
    folder_path = datetime.now().strftime(DailyOrganizerConfig().get_folder_structure())
    folder_path = os.path.expanduser(folder_path)

    create_folder(folder_path)
    return folder_path

def create_note_file(file_name):
    if not os.path.exists(file_name):
        print("Creating note file " + file_name)
        note_file = open(file_name, "x")
        note_file.close()

def get_todays_note_file_path():
    return (get_current_folder() + "/" + DailyOrganizerConfig().get_main_notes_file_name())

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

class NewMeetingNoteCommand(sublime_plugin.WindowCommand):
    def run(self):
        global new_meeting_obj
        new_meeting_obj = self
        meeting_file_name_panel = self.window.show_input_panel(
            "Meeting File Name", "", got_meeting_file_name, None, cancel_meeting_file_name)

    def create_meeting_file(self, file_name):
        meeting_file_path = (get_current_folder() + "/" + file_name)
        create_note_file(meeting_file_path)
        meeting_note = self.window.open_file(meeting_file_path)
