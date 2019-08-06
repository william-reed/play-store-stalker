# Play Store Stalker
Get notified via Slack whenever your new Play Store release is available. Meant to be run as a cron job.

## Setup
1. Create a new app [on slack](https://api.slack.com/apps)
2. Grant it permission to send messages as a bot
3. Clone this repo on some computer where you can add a cron task
4. Create and enter your virtual environment. `python3 -m venv env && source env/bin/activate`
5. Install dependencies `pip3 install -r requirements.txt`
6. Set your `SLACK_API_TOKEN` environment variable to the app you previously created.
7. Run the program as a test then add as a cron task when you are ready e.g. `*/5 * * * *` for every 5 minutes.

## Running
```
$ python stalker.py --help

usage: stalker.py [-h] [--debug] package channel

Detect changes to Play Store version changes. This requires that you set the
env variable of SLACK_API_TOKEN

positional arguments:
  package      The play store package. E.g. if your full app url is https://pl
               ay.google.com/store/apps/details?id=com.reddit.frontpage your
               input here would be 'com.reddit.frontpage'
  channel      The channel to send updates to (use a # too)

optional arguments:
  -h, --help   show this help message and exit
  --debug, -d  Enable debug logging. defaults to false
```


