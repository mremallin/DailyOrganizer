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
        self.settings = sublime.load_settings("daily-organizer.sublime_settings")

    def get_folder_structure(self):
        return self.settings.get("folder_structure", "~/DailyOrganizer/%Y/%m/%d")

    def get_main_notes_file_name(self):
        return self.settings.get("main_notes_file_name", "Organizer.txt")

def create_folder(folder):
    if not os.path.exists(folder):
        print("Creating " + folder)
        os.makedirs(folder)

def get_current_folder():
    folder_path = datetime.now().strftime(DailyOrganizerConfig().get_folder_structure())
    folder_path = os.path.expanduser(folder_path)
    print("Current folder path: " + folder_path)

    create_folder(folder_path)
    return folder_path

def create_note_file(file_name):
    print("Creating file " + file_name)
    if not os.path.exists(file_name):
        note_file = open(file_name, "x")
        note_file.close()

def get_todays_note_file_path():
    return (get_current_folder() + "/" + DailyOrganizerConfig().get_main_notes_file_name())

class OpenTodaysNoteCommand(sublime_plugin.WindowCommand):
    def run(self):
        note_file_path = get_todays_note_file_path()
        create_note_file(note_file_path)
        todays_note = self.window.open_file(note_file_path)
