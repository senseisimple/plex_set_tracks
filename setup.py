import subprocess
import sys
import os.path
from shutil import copyfile

def install(packages):
    """ Invokes pip to install list of packages.

        Parameters:
            packages(list<str>): Packages to install, in requirements.txt format
    """
    for package in packages:
        subprocess.call([sys.executable, "-m", "pip", "install", package])

def getListFromFile(file, ignoreStart="#"):
    """ Return list of packages to install given a requirements.txt file.

        Parameters:
            file(str): The requirements.txt file to parse.
            ignoreStart(str): Ignore all lines that start with this string (optional).
    """
    list = []
    with open(file) as handle:
        for line in handle.readlines():
            if not line.startswith(ignoreStart):
                list.append(line)
    return list


# Get dependencies for each OS
requirements = getListFromFile("setup/requirements.txt")
windows = getListFromFile("setup/windows.txt", "-r")
linux = getListFromFile("setup/linux.txt", "-r")
mac = getListFromFile("setup/mac.txt", "-r")

# Install dependencies
install(requirements)
if sys.platform == 'win32':
    install(windows)
if sys.platform.startswith('linux'):
    install(linux)
if sys.platform == 'darwin':    # MacOS
    install(mac)

# Create config file
if not os.path.isfile("config.ini"):
    copyfile("./setup/config_template.ini", "config.ini")
    print("Config file created")