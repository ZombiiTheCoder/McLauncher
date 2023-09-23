import os

from helpers.FolderStructure import DownloadFile, GetNameAndExt, OpenJsonfile, CreateFolderStructure
from helpers.libraries import CollectLibraries
from helpers.libraries.prune import Prune

def JarRipper(config):
    Libraries = []
    Config = OpenJsonfile(config)

    CreateFolderStructure(Config["version"])

    VersionManifestUrl = Config["version_manifest"]
    VersionFolder = "{0}/.minecraft/versions/{1}".format(os.getcwd(), Config["version"])

    DownloadFile(VersionManifestUrl, ".minecraft/versions/"+GetNameAndExt(VersionManifestUrl))

    for x in OpenJsonfile(".minecraft/versions/"+GetNameAndExt(VersionManifestUrl))["versions"]:
        
        ReleaseData = {
            "Version": x["id"],
            "PkgType": x["type"],
            "InfoUrl": x["url"],
        }

        if ReleaseData["Version"] == Config["version"]:
            print(ReleaseData)
            VersionInfoPath = "{0}/{1}".format(VersionFolder, GetNameAndExt(ReleaseData["InfoUrl"]))

            DownloadFile(ReleaseData["InfoUrl"], VersionInfoPath)
            VersionInfo = OpenJsonfile(VersionInfoPath)

            # Download client.jar
            ClientJarPath = "{0}/{1}".format(VersionFolder, GetNameAndExt(VersionInfo["downloads"]["client"]["url"]))
            DownloadFile(VersionInfo["downloads"]["client"]["url"], ClientJarPath)
            # If Version has a server Download server.jar
            if "server" in VersionInfo["downloads"]:
                ServerJarPath = "{0}/{1}".format(VersionFolder, GetNameAndExt(VersionInfo["downloads"]["server"]["url"]))
                DownloadFile(VersionInfo["downloads"]["server"]["url"], ServerJarPath)

            i=0
            for x in Prune(CollectLibraries(VersionInfo)):
                i+=1
                print(i)
                DownloadFile(x, "{0}/libs/{1}".format(VersionFolder, GetNameAndExt(x)))
                Libraries.append("{0}/libs/{1}".format(VersionFolder, GetNameAndExt(x)))

            DownloadFile(VersionInfo["assetIndex"]["url"], ".minecraft/assets/indexes/{0}.json".format(VersionInfo["assetIndex"]["id"]))

            return Libraries, ClientJarPath, ServerJarPath, VersionInfo, ReleaseData["Version"], ReleaseData["PkgType"]
        
def JarRipper_Custom(config):
    Libraries = []
    Config = OpenJsonfile(config)

    CreateFolderStructure(Config["version"])

    VersionFolder = "{0}/.minecraft/versions/{1}".format(os.getcwd(), Config["version"])

    VersionInfoPath = "{0}/{1}.json".format(VersionFolder, Config["version"])
    print("Loading_Custom_Version:", Config["version"])
    VersionInfo = OpenJsonfile(VersionInfoPath)
    
    ClientJarPath = "{0}/client.jar".format(VersionFolder)
    ServerJarPath = ""

    for x in Prune(CollectLibraries(VersionInfo)):
        DownloadFile(x, "{0}/libs/{1}".format(VersionFolder, GetNameAndExt(x)))
        Libraries.append("{0}/libs/{1}".format(VersionFolder, GetNameAndExt(x)))

    DownloadFile(VersionInfo["assetIndex"]["url"], ".minecraft/assets/indexes/{0}.json".format(VersionInfo["assetIndex"]["id"]))
    if "logging" in VersionInfo:
        DownloadFile(VersionInfo["logging"]["client"]["file"]["url"], ".minecraft/assets/log_configs/{0}.xml".format(VersionInfo["logging"]["client"]["file"]["id"]))

    return Libraries, ClientJarPath, ServerJarPath, VersionInfo, Config["version"], VersionInfo["type"]