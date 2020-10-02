import re, time
import win32gui, win32con, win32com.client

class GameProcessNotFoundException(Exception):
    def __init__(self):
        super(GameProcessNotFoundException, self)
    
    def __str__(self):
        return "cannot find game window."

game_window_rect = (-1, -1, -1, -1)
    
def setActiveCallback(hwnd, wildcard):
    '''check all windows
    '''
    global game_window_rect
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        win32gui.BringWindowToTop(hwnd)
        # prevent this error：pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        # set foreground window
        win32gui.SetForegroundWindow(hwnd)
        game_window_rect = win32gui.GetWindowRect(hwnd)

def activeGameWindow():
    '''set foreground window
    '''
    global game_window_rect
    game_window_rect = (-1, -1, -1, -1)
    win32gui.EnumWindows(setActiveCallback, ".*%s.*"%"DUEL LINKS")
    if game_window_rect[0] == -1:
        raise GameProcessNotFoundException()
