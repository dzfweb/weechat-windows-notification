# Weechat Windows Notification

![Emoji](print.png)

## Requirements
* Windows 10
* Powershell 5 or higher
* WeeChat running on bash (not cygwin)

## Instalation 
### 1- Install BurntToast

`Install-Module -Name BurntToast`

Execute the command after the BurntToast installation

`New-BTAppId`

### 2- Register PowerShell Script
- `git clone https://github.com/dzfweb/weechat-windows-notification`
- `cd weechat-windows-notification`

Edit the file WeeChatWindowsNotification.ps1 and replace the folder configuration. 
*Important: use a folder accessible both powershell and bash* 
- `$folder = 'C:\Users\dougl\.weechat'`

Register the powershell script by running the following command on powershell `WeeChatWindowsNotification.ps1`

### 3- Get WeeChat Plugin (windows bash)
Get the plugin script
```
wget https://raw.githubusercontent.com/dzfweb/weechat-windows-notification/master/windows_notification.py
cp windows_notification.py ~/.weechat/python/autoload
``` 
Start WeeChat and configure the path.
`/set plugins.var.python.windows_notification.path /mnt/c/Users/dougl/.weechat`

*Obs: you can set any folder, it is used to share temp files between powershell and bash only*