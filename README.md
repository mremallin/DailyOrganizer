# Introduction
DailyOrganizer is a simple organizational tool to help create meeting minutes and daily notes.

Once installed, there are two new options added:
- Open Today's Note
- Create a new meeting minutes note

## Open Today's Note
This will either create or open a note file for today. The default location of the note will be at `~/DailyOrganizer/%Y/%m/%d/Today.txt`

## Create a new meeting minutes note
This will first prompt the user to choose one of their available templates (Default at `~/DailyOrganizer/MeetingTemplates`) and then to choose a file name to store the new meeting minutes in the same folder as `Today.txt`.

The contents of the template file will be copied into the meeting file when it is first created. If the file already exists, it will remain untouched.

The "None" template is special and indicates that a blank file will be created.

# Configuration
## folder_structure
This is the folder layout of how to store the note files. It accepts formatting specifiers from strftime as well. (https://docs.python.org/3.6/library/datetime.html#strftime-strptime-behavior)

## main_notes_file_name
This is the name of the singular note file in each directory. This also accepts formatting specifiers from strftime.

## meeting_template_folder
This is the folder which stores meeting templates. The folder and all subdirectories will be searched for any files to be used as a template. The chosen template is copied without change into the newly created meeting file.
