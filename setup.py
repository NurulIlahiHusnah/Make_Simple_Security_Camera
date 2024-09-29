import sys 
from cx_Freeze import setup, Executable

#my_options = {"packages": ['os'], "excludes" :['tkinter']}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
setup(
    name ='Camera Security',
    version = "2.0",
    executables = [Executable("camera.py", base=base)]
)