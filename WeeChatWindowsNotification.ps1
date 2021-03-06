$folder = 'C:\Users\dougl\.weechat' # Enter the root path of weechat (!!windows path)
$filter = '*.notify'  # You can enter a wildcard filter here.

get-childitem $folder  -include $filter  -recurse | foreach ($_) {remove-item $_.fullname}
get-childitem $folder  -include '*.hash' -recurse | foreach ($_) {remove-item $_.fullname}

$fsw = New-Object IO.FileSystemWatcher $folder, $filter -Property @{IncludeSubdirectories = $false;NotifyFilter = [IO.NotifyFilters]'FileName, LastWrite'}

Register-ObjectEvent $fsw Created -SourceIdentifier WeeChatWindowsNotification -Action {          
Param(            
)            
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class UserWindows {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
"@            
  try {            
  $ActiveHandle = [UserWindows]::GetForegroundWindow()            
  $Process = Get-Process | ? {$_.MainWindowHandle -eq $activeHandle}               
  
  } catch {            
  Write-Error "Failed to get active Window details. More Info: $_"            
  }
  function Hash($textToHash)
  {
      $hasher = new-object System.Security.Cryptography.SHA256Managed
      $toHash = [System.Text.Encoding]::UTF8.GetBytes($textToHash)
      $hashByteArray = $hasher.ComputeHash($toHash)
      foreach($byte in $hashByteArray)
      {
           $res += $byte.ToString()
      }
      return $res;
  }

  $name = $Event.SourceEventArgs.Name -replace ".notify",""
  $message = (Get-Content $Event.SourceEventArgs.FullPath)
  $messageFormated = $message.substring(0, [System.Math]::Min(100, $message.Length))
  $hash = Hash($messageFormated)
  $file = Get-ChildItem $Event.SourceEventArgs.FullPath
  $dir = $file.DirectoryName
  $fullHashFile = "$($dir)\$($hash).hash"
  $hashExists = Test-Path $fullHashFile

  if ($hashExists) {
    Remove-Item $fullHashFile -Force
  } else {
    if (-Not [string]::IsNullOrEmpty($Process)) {
      New-Item $fullHashFile  -type file -force
      New-BurntToastNotification -Text $name, $messageFormated -AppLogo 'C:\Dev\weechat-windows-notification\ico.png' -Silent
    }
  }

  Remove-Item $file -Force
}

# To stop the monitoring, run the following commands:
# Unregister-Event WeeChatWindowsNotification