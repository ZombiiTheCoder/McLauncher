import os, json, requests

def CreateFolder(name):
    if not os.path.exists(name):
        os.mkdir(name)

def ClearDir(dirr):
    print(dirr)
    for root, dirs, files in os.walk(dirr):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            Remove(os.path.join(root, name))

def Remove(dirr):
    print(dirr)
    for root, dirs, files in os.walk(dirr):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            Remove(os.path.join(root, name))
    os.rmdir(dirr)

def CreateFolder_RREC(name):
    if os.path.exists(name):
        Remove(name)
    os.mkdir(name)
    
def GetNameAndExt(url):
    return url.split("/")[len(url.split("/"))-1]

def GetName(url):
    nameExt = url.split("/")[len(url.split("/"))-1]
    return '.'.join(nameExt.split(".")[:len(nameExt.split("."))-1])

def OpenJsonfile(file):
    f = open(file, "r")
    jsonData = json.load(f)
    f.close()    
    return jsonData

def DownloadFile(url, file):
    if os.path.exists(file):
        os.remove(file)
    resp = requests.get(url)
    print("Downloading "+GetNameAndExt(file), " STATUS: ", resp.status_code)
    f = open(file, "xb")
    f.write(resp.content)
    f.close()

def DownloadFileC(url, file, msg):
    if os.path.exists(file):
        os.remove(file)
    # print("Downloading "+url, msg)
    resp = requests.get(url, timeout=10000)
    f = open(file, "xb")
    f.write(resp.content)
    f.close()

def CreateFolderStructure(Version):
    #.minecraft    
    CreateFolder(".minecraft")

    # Assets
    CreateFolder(".minecraft/assets")
    CreateFolder(".minecraft/assets/indexes")
    CreateFolder(".minecraft/assets/log_configs")
    CreateFolder(".minecraft/assets/skins")
    CreateFolder(".minecraft/assets/virtual")

    # Versions
    CreateFolder(".minecraft/versions")
    CreateFolder(".minecraft/natives")
    CreateFolder(".minecraft/versions/"+Version)
    CreateFolder(".minecraft/versions/"+Version+"/libs")