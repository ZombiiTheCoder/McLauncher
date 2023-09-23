import os, subprocess
from JarRipper_Lib import JarRipper, JarRipper_Custom
# from asset_installer import Download_Assets
from helpers.FolderStructure import OpenJsonfile, DownloadFile
from helpers.libraries import CollectPreDownloadedLibraries
from helpers.libraries.prune import Prune
from uuid import UUID, uuid4, uuid5
import platform
# from adal import AuthenticationContext

Config = OpenJsonfile("./config.json")
Libraries = []
ClientJarPath = ""
ServerJarPath = ""
ReleaseType = ""
Version = Config["version"]
VersionInfo = {}

if Config["versionLoader"] == "custom":
    if os.path.exists('{0}/.minecraft/versions/{1}/'.format(os.getcwd(), Config["version"])):
        Libraries = CollectPreDownloadedLibraries(Config, '{0}/.minecraft/versions/{1}/libs'.format(os.getcwd(), Config["version"]))
        ClientJarPath = '{0}/.minecraft/versions/{1}/client.jar'.format(os.getcwd(), Config["version"])
        Libraries.append(ClientJarPath)
        ServerJarPath = '{0}/.minecraft/versions/{1}/server.jar'.format(os.getcwd(), Config["version"])
        VersionInfo = OpenJsonfile('{0}/.minecraft/versions/{1}/{2}.json'.format(os.getcwd(), Config["version"], Config["version"]))
        ReleaseType = VersionInfo["type"]
    else:
        Libraries, ClientJarPath, ServerJarPath, VersionInfo, Version, ReleaseType = JarRipper_Custom("./config.json")
        Libraries.append(ClientJarPath)

else:
    if os.path.exists('{0}/.minecraft/versions/{1}/'.format(os.getcwd(), Config["version"])):
        Libraries = CollectPreDownloadedLibraries(Config, '{0}/.minecraft/versions/{1}/libs'.format(os.getcwd(), Config["version"]))
        ClientJarPath = '{0}/.minecraft/versions/{1}/client.jar'.format(os.getcwd(), Config["version"])
        Libraries.append(ClientJarPath)
        ServerJarPath = '{0}/.minecraft/versions/{1}/server.jar'.format(os.getcwd(), Config["version"])
        VersionInfo = OpenJsonfile('{0}/.minecraft/versions/{1}/{2}.json'.format(os.getcwd(), Config["version"], Config["version"]))
        ReleaseType = VersionInfo["type"]
    else:
        Libraries, ClientJarPath, ServerJarPath, VersionInfo, Version, ReleaseType = JarRipper("./config.json")
        Libraries.append(ClientJarPath)
        # Libraries.append(ServerJarPath)

AssetJsonPath = os.getcwd()+"/.minecraft/assets/indexes/{0}.json".format(VersionInfo["assetIndex"]["id"])
# Download_Assets(AssetJsonPath)

AssetIndex = VersionInfo["assetIndex"]["id"]

MainClass = VersionInfo["mainClass"]
if MainClass == "net.minecraft.launchwrapper.Launch":
    MainClass = "net.minecraft.client.Minecraft"

# JDK = r'C:\Program Files\Java\jdk-13\bin\java.exe'
JDK = r'C:\Program Files\Java\jdk-20\bin\java.exe'
# JDK = r'E:\Program Files\Java\jdk-20\bin\java.exe'
# JDK = "java"
args = [
    JDK,
    "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump", 
    "-Dos.name=Windows 10", 
    "-Dos.version=10.0", 
    "-Xss1M",
    # r'-Djava.library.path=C:\Users\Zombi\AppData\Roaming\.minecraft\bin\ad91b9597c82446c9a2e23cecb86e50529b7ac4f',
    '-Djava.library.path={0}/.minecraft/natives'.format(os.getcwd()),
    '-Dminecraft.client.jar={0}'.format(ClientJarPath),
    '-Dminecraft.launcher.brand=minecraft-launcher',
    '-Dminecraft.launcher.version=2.6.16',
    '-cp',
    ";".join(Libraries),
    "-Xmx2G",
    "-XX:+UnlockExperimentalVMOptions",
    "-XX:+UseG1GC",
    "-XX:G1NewSizePercent=20",
    "-XX:G1ReservePercent=20",
    "-XX:MaxGCPauseMillis=50",
    "-XX:G1HeapRegionSize=32M",
]

if "logging" in VersionInfo:
    if not (os.path.exists(".minecraft/assets/log_configs/{0}".format(VersionInfo["logging"]["client"]["file"]["id"]))):
        DownloadFile(VersionInfo["logging"]["client"]["file"]["url"], ".minecraft/assets/log_configs/{0}".format(VersionInfo["logging"]["client"]["file"]["id"]))
    args.append("-Dlog4j.configurationFile={0}/.minecraft/assets/log_configs/{1}".format(os.getcwd(), VersionInfo["logging"]["client"]["file"]["id"]))

profiles = OpenJsonfile("./profiles.json")
profile = profiles[Config["profileID"]]
uuidh = UUID("8df5a464-38de-11ec-aa66-3fd636ee2ed7")
uuid = ""
username = "anonomous"
userType = 'msa'
accessToken = ""
clientID = ""
xuid = 0
if profile["type"] == "custom":
    username = profile["username"]
    uuid = uuid5(uuidh, platform.node()).hex
    userType = ''
    accessToken = ""
    clientID = ""
if profile["type"] == "premium":
    username = profile["username"]
    uuid = profile["uuid"]
    userType = 'msa'
    accessToken = profile["accessToken"]
    clientID = profile["clientID"]
    xuid = profile["xuid"]
gameArgs = [
    MainClass,
    '--username',
    username,
    '--version',
    Version,
    '--gameDir',
    "{0}/.minecraft".format(os.getcwd()),
    '--assetsDir',
    "{0}/.minecraft/assets".format(os.getcwd()),
    '--assetIndex',
    AssetIndex,
    '--uuid',
    uuid,
    '--accessToken',
    accessToken,
    '--userProperties',
    '{}',
    '--clientId',
    clientID,
    '--userType',
    userType,
    '--versionType',
    ReleaseType,
    "--xuid",
    str(xuid)
]
args.extend(gameArgs)

print("\n\n")
print("\n".join(args))
print("\n\n")
os.chdir("{0}/.minecraft/versions".format(os.getcwd()))

subprocess.call(args)