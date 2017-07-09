#  Project: WeeChat Windows Notification
#  Description: A libnotify script for weechat. Uses
#  subprocess.call to execute notify-send with arguments.
#  Author: dzfweb / github.com/dzfweb
#  License: GPL3
#

import io
import weechat as weechat
import subprocess
from os import environ, path

windows_notification_name = "windows_notification"
windows_notification_version = "1.0.0"
windows_notification_license = "GPL3"

# convenient table checking for bools
true = { "on": True, "off": False }

# declare this here, will be global config() object
# but is initialized in __main__
cfg = None

class config(object):
    def __init__(self):
        # default options for windows_notification
        self.opts = {
            "highlight": "on",
            "query": "on",
            "notify_away": "off",
			"path": "/mnt/c/Users/dougl/.weechat"
        }

        self.init_config()
        self.check_config()

    def init_config(self):
        for opt, value in self.opts.items():
            temp = weechat.config_get_plugin(opt)
            if not len(temp):
                weechat.config_set_plugin(opt, value)

    def check_config(self):
        for opt in self.opts:
            self.opts[opt] = weechat.config_get_plugin(opt)

    def __getitem__(self, key):
        return self.opts[key]

def printc(msg):
    weechat.prnt("", msg)

def handle_msg(data, pbuffer, date, tags, displayed, highlight, prefix, message):
    highlight = bool(highlight) and cfg["highlight"]
    query = true[cfg["query"]]
    notify_away = true[cfg["notify_away"]]
    buffer_type = weechat.buffer_get_string(pbuffer, "localvar_type")
    away = weechat.buffer_get_string(pbuffer, "localvar_away")
    x_focus = False
    window_name = ""
    my_nickname = "nick_" + weechat.buffer_get_string(pbuffer, "localvar_nick")

    # Check to make sure we're in X and xdotool exists.
    # This is kinda crude, but I'm no X master.
    if (environ.get('DISPLAY') != None) and path.isfile("/bin/xdotool"):
        window_name = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowname"])

    if "WeeChat" in window_name:
        x_focus = True

    if pbuffer == weechat.current_buffer() and x_focus:
        return weechat.WEECHAT_RC_OK

    if away and not notify_away:
        return weechat.WEECHAT_RC_OK

    if my_nickname in tags and my_nickname != 'nick_':
        return weechat.WEECHAT_RC_OK

    if 'nick_unknown' in tags:
        return weechat.WEECHAT_RC_OK

    if 'no_highlight' in tags:
        return weechat.WEECHAT_RC_OK

    buffer_name = weechat.buffer_get_string(pbuffer, "short_name")

    if buffer_type == "private" and query:
        notify_user(buffer_name, message)
    elif buffer_type == "channel" and highlight:
        notify_user("{} @ {}".format(prefix, buffer_name), message)

    return weechat.WEECHAT_RC_OK

def process_cb(data, command, return_code, out, err):
    if return_code == weechat.WEECHAT_HOOK_PROCESS_ERROR:
        weechat.prnt("", "Error with command '%s'" % command)
    elif return_code != 0:
        weechat.prnt("", "return_code = %d" % return_code)
        weechat.prnt("", "notify-send has an error")
    return weechat.WEECHAT_RC_OK

def notify_user(origin, message):
    file = "{}/{}.notify".format(cfg['path'], origin[1:]);
    with io.FileIO(file, "w") as file:
        file.write(message)
        file.close()

    return weechat.WEECHAT_RC_OK

# execute initializations in order

weechat.register(windows_notification_name, 'dzfweb', windows_notification_version, windows_notification_license, 'Script for windows notification', '', '')

cfg = config()
print_hook = weechat.hook_print("", "", "", 1, "handle_msg", "")

