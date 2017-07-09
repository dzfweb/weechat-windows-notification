$folder = 'C:\Users\dougl\.weechat' # Enter the root path of weechat (!!windows path)
$filter = '*.notify'  # You can enter a wildcard filter here.
                         
$fsw = New-Object IO.FileSystemWatcher $folder, $filter -Property @{IncludeSubdirectories = $false;NotifyFilter = [IO.NotifyFilters]'FileName, LastWrite'}

Register-ObjectEvent $fsw Created -SourceIdentifier WeeChatWindowsNotification -Action {
  $name = $Event.SourceEventArgs.Name -replace ".notify",""
  $message = (Get-Content $Event.SourceEventArgs.FullPath)
  $messageFormated = $message.substring(0, [System.Math]::Min(100, $message.Length))
  Remove-Item $Event.SourceEventArgs.FullPath -Force
  New-BurntToastNotification -Text $name, $messageFormated -AppLogo 'C:\Dev\weechat-windows-notification\ico.png'
}

# To stop the monitoring, run the following commands:
# Unregister-Event WeeChatWindowsNotification