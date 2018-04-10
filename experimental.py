# Read files in a directory

import os

def getThemesMenu():
    files = os.listdir('static/css/lib')
    key=0
    cssFiles=[]
    for file in files:
        cssExt = file.split('.css')
        if (len(cssExt)>0):
            if cssExt[1]=='':
                cssFiles.append({'fileName':file, 'menuName':cssExt[0]})

    return cssFiles

menuItems = getThemesMenu()

[print(menuItem['fileName'], menuItem['menuName']) for menuItem in menuItems]