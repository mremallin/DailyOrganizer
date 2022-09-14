# Introduction
DailyOrganizer is a simple organizational tool to help create meeting minutes and daily notes.

Once installed, there are two new options added:
- Open Today's Note
- Create a new meeting minutes note

## Open Today's Note
This will either create or open a note file for today. The default location of the note will be at `~/DailyOrganizer/%Y/%m/%d/Today.txt`

## Create a new meeting minutes note
This will prompt the user for a file name to store the new meeting minutes in the same folder as `Today.txt`

# Configuration
## folder_structure
This is the folder layout of how to store the note files. It accepts formatting specifiers from strftime as well. (https://docs.python.org/3.6/library/datetime.html#strftime-strptime-behavior)

## main_notes_file_name
This is the name of the singular note file in each directory. This also accepts formatting specifiers from strftime.
