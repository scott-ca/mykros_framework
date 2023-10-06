Set objShell = CreateObject("WScript.Shell")

' Specify the path to the batch file
strBatchFile = "verbose_windows.bat"

' Run the batch file silently and hide the window
intWindowStyle = 0
objShell.Run strBatchFile, intWindowStyle, False
