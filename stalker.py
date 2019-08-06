from bs4 import BeautifulSoup
from pathlib import Path
import argparse
import logging
import os
import requests
import slack
import sys

# parse args
parser = argparse.ArgumentParser(description='Detect changes to Play Store version changes. This requires that you set the env variable of SLACK_API_TOKEN')
parser.add_argument('package', type=str, help="The play store package. E.g. if your full app url is https://play.google.com/store/apps/details?id=com.reddit.frontpage your input here would be 'com.reddit.frontpage'")
parser.add_argument('channel', type=str, help="The channel to send updates to (use a # too)")
parser.add_argument('--debug', '-d', default=False, action='store_true', help="Enable debug logging. defaults to false")
args = vars(parser.parse_args())

# config
URL             = "https://play.google.com/store/apps/details?id=" + args['package']
CHANNEL         = args['channel']
DEBUG           = args['debug']
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]

# setup logger
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if DEBUG else logging.WARN)
logger = logging.getLogger("playstore_stalker")

soup = BeautifulSoup(requests.get(URL).text, "html.parser")
# get the current version
version = (
    soup(text="Current Version")[0]
    .parent.parent.select("div > span > div > span")[0]
    .text
)
logger.debug("Found version " + version)

# what's new??
whats_new = (
    soup(text="What's New")[0]
    .parent.parent.parent
    .select("div:nth-child(2) > div > span")[0].decode_contents()
    .replace("<br/>", "\n")
)
logger.debug("What's new:\n" + whats_new)

# get file
p = Path("~", ".local", "playstore_stalker").expanduser()
p.mkdir(parents=True, exist_ok=True)
# use the package name as the file name so we can run multiple instances of this
file = p / URL.split("=")[-1]


def write_version():
    """
    Write the current version to file
    """
    logger.debug("writing new version to disk")
    with open(file, "w") as f:
        f.write(version)


version_change = False
if file.exists():
    logger.debug("Previous version file exists")
    with open(file, "r") as f:
        prev_version = f.readline()
        if prev_version != version:
            version_change = True
else:
    logger.debug("Previous version file does not exist")
    write_version()

logger.debug("version changed? :" + str(version_change))
if version_change:
    # write the version to file
    write_version()
    logger.debug("Version has changed")
    client = slack.WebClient(token=SLACK_API_TOKEN)

    client.chat_postMessage(
        channel=CHANNEL,
        text="Version *{}* now available on the <{}|Play Store>.\nWhat's New:\n{}".format(version, URL, whats_new),
    )

