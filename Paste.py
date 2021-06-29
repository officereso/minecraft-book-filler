import ctypes
import time

import pyautogui
import pyperclip

class Book:
    def __init__(self, pages=None):
        if pages is None:
            pages = []
        self.pages = pages

    def AddPage(self, page):
        self.pages.append(page)

    def GetPages(self):
        return self.pages


class Page:
    def __init__(self, pageNumber, lines=None):
        if lines is None:
            lines = []
        self.pageNumber = pageNumber
        self.lines = lines

    def AddLine(self, line):
        if len(self.lines) > 14:
            raise ValueError("Page: " + str(self.pageNumber) + " Exceeds length of 14.")
        self.lines.append(line)

    def GetLines(self):
        return self.lines


SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

charLengths = {
    ' ': 3,
    '!': 1,
    '\"': 3,
    '\'': 1,
    '(': 3,
    ')': 3,
    '*': 3,
    ',': 1,
    '.': 3,
    ':': 1,
    ';': 1,
    '<': 4,
    '>': 4,
    '@': 6,
    'I': 3,
    '[': 3,
    ']': 3,
    '`': 2,
    'f': 4,
    'i': 1,
    'k': 4,
    'l': 2,
    't': 3,
    '{': 3,
    '}': 3,
    '|': 1,
    '~': 6,
    '‣': 2,
    '•': 2,
    '⁃': 2,
    '◦': 3,
    '⁍': 3
}
file = open("text.txt", 'r', encoding="utf8")

pageNumber = 1
page = Page(pageNumber)
book = Book()
lineLength = 0

for line in file:
    line = line.rstrip('\n')
    print(line)
    for char in line:
        if char == '§' or char == 'Â':
            continue
        try:
            lineLength += charLengths[char]
        except KeyError:
            lineLength += 5
        lineLength += 1
        print("  "+char+" : "+str(lineLength))
    print("    "+str(lineLength))
    if lineLength > 113:
        raise ValueError("Line: " + line + " Exceeds line length of 113.")
    if "§" in line:
        line = line.replace('Â§', '')
        pageNumber += 1
        page.AddLine(line)
        book.AddPage(page)
        page = Page(pageNumber)
        lineLength = 0
        continue
    page.AddLine(line)
    lineLength = 0

pyautogui.hotkey('alt', 'tab')
print(pyautogui.position())
pyautogui.moveTo(1061, 497)
pyautogui.FAILSAFE = True

for page in book.GetPages():
    for line in page.GetLines():
        time.sleep(.1)
        pyperclip.copy(line)
        PressKey(29)
        PressKey(47)
        ReleaseKey(29)
        ReleaseKey(47)

        PressKey(28)
        ReleaseKey(28)
    pyautogui.click()

pyautogui.hotkey('alt', 'tab')
