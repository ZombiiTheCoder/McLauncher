import os
from ..print import MakeIndent

Libraries = []

def CollectParentAndChild(deepness, ParentLib, SubLib):
    def PrintAndAddLib(ChildLib):
        Libraries.append(ChildLib["url"])
        print(MakeIndent(deepness+1), ChildLib["url"])
    ChildLib = SubLib
    for x in ChildLib:
        ChildLib = SubLib
        print(MakeIndent(deepness), x)
        if x in ChildLib:
            ChildLib = ChildLib[x]
            if "url" in ChildLib:
                PrintAndAddLib(ChildLib)
            else:
                CollectParentAndChild(deepness+1, ParentLib, ChildLib)
        else:
            PrintAndAddLib(ChildLib)

def CollectLibraries(versionInfo):
    for x in versionInfo["libraries"]:
        CollectParentAndChild(0, x["downloads"], x["downloads"])
    return Libraries

def CollectPreDownloadedLibraries(Config, path):
    libs = []
    for paths in os.walk(path):
        for path in paths:
            for file in path:
                if file.__contains__(".jar"):
                    libs.append('{0}/.minecraft/versions/{1}/libs/{2}'.format(os.getcwd(), Config["version"], file))
                    print("Found", '{0}/.minecraft/versions/{1}/libs/{2}'.format(os.getcwd(), Config["version"], file))
    return libs