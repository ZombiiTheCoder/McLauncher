import platform

from helpers.libraries import CollectLibraries

from ..FolderStructure import GetName, GetNameAndExt
from .version_grabber import GetVersion, GetVersion_STR

def GetRequiredNativeArch():
    arch = platform.architecture()[0].replace("bit", "")
    SysArchPair = "{0}-{1}".format(platform.system().lower(), arch)
    if arch == "64":
        SysArchPair = platform.system().lower()
    return "natives-{0}.jar".format(SysArchPair)

def RemoveDuplicateLibs(libs):
    DupesRemoved = set()
    for x in libs:
        DupesRemoved.add(x.strip(" "))
    return DupesRemoved

def RemoveIncorrectNatives(libs):
    Libs = []
    MacNatives = []
    WindowsNatives = []
    LinuxNatives = []
    for x in libs:
        if "natives-macos.jar" in x or "natives-osx.jar" in x:
            MacNatives.append(x)
            # print(x)
        elif "natives-linux.jar" in x:
            LinuxNatives.append(x)
        elif "natives-windows.jar" in x:
            WindowsNatives.append(x)
        
        if GetRequiredNativeArch() in x:
            Libs.append(x)
        if not x.__contains__("natives-macos") and not x.__contains__("natives-osx") and not x.__contains__("natives-linux") and not x.__contains__("natives-windows"):
            Libs.append(x)
    return Libs, MacNatives, LinuxNatives, WindowsNatives

def CompareVersion(v1, v2):
    print(GetName(v1))
    print(GetVersion(GetName(v1)))
    v1MajorMinor = float(".".join(GetVersion(GetName(v1))[0].split(".")[:2]))
    v2MajorMinor = float(".".join(GetVersion(GetName(v2))[0].split(".")[:2]))
    v1Bugfix = float(".".join(GetVersion(GetName(v1))[0].split(".")[1:]))
    v2Bugfix = float(".".join(GetVersion(GetName(v2))[0].split(".")[1:]))
    winner = ""
    if v1MajorMinor > v2MajorMinor:
        winner = v2 # v1 won
    elif v1MajorMinor < v2MajorMinor:
        winner = "none" # v2 won
    elif v1MajorMinor == v2MajorMinor:
        if v1Bugfix > v2Bugfix:
            winner = v2 # v1 won
        elif v1Bugfix < v2Bugfix:
            winner = "none" # v2 won
        elif v1Bugfix == v2Bugfix:
            winner = "none"
    
    return winner



def CheckVersionDifferenceBetweenNatives(libs, MacNatives, WindowsNatives):
    MacNatives2 = MacNatives

    WinUNatives = []
    MacUNatives = []
    ie=0
    if True:
    # if len(MacNatives) <= len(WindowsNatives):
        for x in MacNatives:
            if x.replace("osx", "windows").replace("macos", "windows").replace("-"+GetVersion(GetName(x))[0], "") in WindowsNatives[ie].replace("-"+GetVersion(GetName(WindowsNatives[ie]))[0], ""):
                WinUNatives.append(WindowsNatives[ie])
                MacUNatives.append(x)
            # else:
                # print(x)
            ie+=1

        for x in range(len(WindowsNatives)-len(MacNatives)):
            MacUNatives.append("e")

    # else:
    # if True:
        # for x in WindowsNatives:
        #     if x.replace("windows", "osx").replace("windows", "macos").replace("-"+GetVersion(GetName(x))[0], "") in WindowsNatives[ie].replace("-"+GetVersion(GetName(WindowsNatives[ie]))[0], ""):
        #         WinUNatives.append(x)
        #         MacUNatives.append(MacNatives[ie])

        #     ie+=1

    print(MacUNatives)
    print("\n")
    print(WinUNatives)
    print("\n")
    # e5 = MacNatives2[5]
    # e6 = MacNatives2[6]
    # MacNatives2[5] = e6
    # MacNatives2[6] = e5
    w = []
    i=0
    for x in WinUNatives:
        def v():
            l = GetName(x).replace("-"+GetVersion(GetName(x))[0], "").split("-")
            return "-".join(l[:len(l)-2])
        if v() in MacUNatives[i]:
            w.append(CompareVersion(x, MacUNatives[i]))
        i+=1

    if len(w) > 0:
        return RemoveMacNatives(libs, w)
    else:
        return libs
            
def RemoveMacNatives(libs, MacNatives):
    same = set()
    for x in MacNatives:
        same.add(GetName(x).replace("-natives-macos", "").replace("-natives-osx", "")+".jar")
        same.add(GetName(x)+".jar")
    macRemoved = []
    for x in libs:
        if GetNameAndExt(x) not in same:
            print(x)
            macRemoved.append(x)

    f = open("Libs_MAC.txt", "w")
    f.write("\n".join(macRemoved))
    f.close()

    return macRemoved

def Compare(Libs, MacNatives, WindowsNatives):
    Libss = []
    ToRemove = []
    for x in WindowsNatives:
        Libss.append(x.replace("-windows", "").replace("-"+GetVersion_STR(x), ""))
        Libss.append(GetVersion_STR(x))
    
    for x in MacNatives:
        if not (GetVersion_STR(x) in Libss):
            ToRemove.append(x.replace("-natives-osx", "").replace("-natives-macos", ""))
            print(x +  " is not up to date/ macos only")
        else:
            print(x +  " is up to date or does not exist for windows")

    Libs.extend(WindowsNatives)
    
    return RemoveMacNatives(Libs, ToRemove)

def Prune_Old(Libs):
    Libs2 = RemoveDuplicateLibs(Libs)
    Libs3, MacNatives, _, WindowsNatives = RemoveIncorrectNatives(Libs2)
    Libs4 = CheckVersionDifferenceBetweenNatives(Libs3, MacNatives, WindowsNatives)
    return Libs4

def Prune(Libs):
    NoDupe = RemoveDuplicateLibs(Libs)
    NativesRemoved, MacNatives, _, WindowsNatives = RemoveIncorrectNatives(NoDupe)
    return RemoveDuplicateLibs(Compare(NativesRemoved, MacNatives, WindowsNatives))