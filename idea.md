# Local learn python app
User can choose local dir of a course in video. Start learning and app record the state of latest lesson that user learned in a json file.
When choose the course again, first thing app do is scan the json state file to bring user back to latest state so that can continue learn.

# Key features
  - Choose course folder -> init a json state file.
  - Choose video to learn.
  - Learn the course video via a player using ffmpeg.
  - Update the state of the course when pause or quit learning.
  - When open the course back, have 2 option:
    - Continue learning from latest state.
    - Let user browse through the course video list
  - Support view image and text files.
  - Sidebar contain videos, images, text files, etc. Next to sidebar is the content zone which play the video or view other files.
  - Sidebar can collapse and reopen.
  - If text file, can edit it and save.
