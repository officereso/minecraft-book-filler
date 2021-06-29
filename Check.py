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

file = open("text.txt", 'r', encoding="utf8")

pageNumber = 1
page = Page(pageNumber)
book = Book()
lineLength = 0
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

print("All good files in check.")
