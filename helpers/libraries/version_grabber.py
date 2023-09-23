import re

tests = [
    "lwjgl-platform-2.9.4-nightly-20150209-natives-windows.jar",
    "lwjgl-platform-2.9.4-natives-windows.jar",
    "lwjgl-platform-2.9.4.jar",
    "lwjgl-2.9.4-nightly-20150209-natives-windows.jar",
    "lwjgl-2.9.4-natives-windows.jar",
    "lwjgl-2.9.4.jar",
]

def testVerGrab():
    for test in tests:
        print(re.findall("[0-9][.][0-9]*[.][0-9]", test)[0])

def GetVersion(stri):
    print(stri)
    print(re.findall("[0-9][.][0-9]*[.][0-9]", stri))
    return re.findall("[0-9][.][0-9]*[.][0-9]", stri)

def GetVersion_STR(stri):
    print(stri)
    print(re.findall("[0-9][.][0-9]*[.][0-9]", stri))
    return "".join(re.findall("[0-9][.][0-9]*[.][0-9]", stri))