Dim objShell
Dim PythonExe
Dim PythonScript

Set objShell = CreateObject("Wscript.shell")

PythonExe = "python3 "
PythonScript = """C:\Users\rlau0\Documents\Parselmouth\stockTrading\Live_Ticker.py"""

objShell.Run "cmd /C " & PythonExe & PythonScript