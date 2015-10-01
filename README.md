# What is this?

A program that can be run on a regular schedule (ex: cronjob), and sends
notifications to a pushbullet channel when there is availability for goes.
Note: This is hardcoded to the Austin center for now.

# Usage:

1. Set the following enviroment variables:
    - PB_KEY = The pushbullet api key to use
    - PB_CHAN = The pushbullet channel to post to (the tag name). This must have been created under your account.
    - USERNAME = The username for goes.
    - PASSWORD = The password for goes.
2. Run the following: ```python kicknotify/run.py```
