import os
import subprocess
import threading
import time

retArr = {}

def prinfResult(name:str, rslt) -> None:
    hasErr = False

if isinstance(rslt, bool):
    if not rslt:
        hasErr = True
    elif isinstance(rslt, dict):
        for k,v in rslt.items():
            if isinstance(v, bool) and not v:
                hasErr = True
                break
    else:
        raise TypeError({"err": "not supported rslt type %s"%type(rslt)})

    color = "32m"
    if hasErr:
        color = "31m"

print(f'''\033[{color} {name} : {rslt} \033[0m''')

def tskill(tsname:str) -> int :
    return subprocess.call(f'taskkill /F /T /FI "IMAGENAME eq {tsname}*"', shell = True)

def build(sourcePath:str, buildPath:str, install:bool = True, export:str="conan_export_dev", app = False,gitName = "") -> dict :
    #qmlDebugParam = r'-DCMAKE_CXX_FLAGS:STRING="-DQT_QML_DEBUG" -DCMAKE_CXX_FLAGS_INIT:STRING=-DQT_QML_DEBUG'
    #if not app:
    qmlDebugParam = ""

    cmakeRet = subprocess.call(f'cmake -S {sourcePath} -B {buildPath} -G"Visual Studio 15 2017 Win64" {qmlDebugParam}', shell = True)

    if(cmakeRet == 0) :
        buildRet = subprocess.call(f'cmake --build {buildPath} --target ALL_BUILD --config Release', shell = True)
    else :
        buildRet = -999

    if(install & (buildRet == 0)) :
        installRet = subprocess.call(f'cmake --build {buildPath} --target INSTALL --config Release', shell = True)
    else :
        installRet = -999

    if(install & (installRet == 0) & (export != "")) :
        exportRet = subprocess.call(f'cmake --build {buildPath} --target {export} --config Release', shell = True)
    else :
        exportRet = -999

    rsltMap = {-999: "NotRun", 0: True}

    retArr[gitName] = {"cmake": rsltMap.get(cmakeRet, False),
        "build": rsltMap.get(buildRet, False),
        "install": rsltMap.get(installRet, False),
        "export": rsltMap.get(exportRet, False)
        }

    return {"cmake": rsltMap.get(cmakeRet, False),
        "build": rsltMap.get(buildRet, False),
        "install": rsltMap.get(installRet, False),
        "export": rsltMap.get(exportRet, False)
        }

tskill("scanhub")
tskill("SnSyncService")
tskill("ScanService")
tskill("OptimScan")
tskill("Sn3DApp")
tskill("EXStar")
tskill("EXScan_EA")
tskill("informationCollect")
tskill("sn3DCommunity")
tskill("processManager")
tskill("EXScan S")
tskill("EXScanSService")
tskill("EXScanPro")
tskill("einscan_net_svr")
tskill("Shining3DUserAccount")

buildArr = [
["Sn3DCommonDepenDence"],
["Sn3DFrameWork","Sn3DDigitGlobal"],
["sn3ddeviceconnectmanger"],
["Sn3DDigtalAlgorithm","Sn3DImageQueue","Sn3DFirmwareUpdate","Sn3DSoftWareUpdate","Sn3DUICommon","Sn3DPlayer","Sn3DUserAccount","Sn3DProjDefaultPath"],
["Sn3DTexture","Sn3DSecurity","Sn3DInformation","Sn3DAutoExposure"],
["Sn3DFunction","Sn3DClientFrameWork","Sn3DCalibration"],
["Sn3DAlgorithmWrapper","Sn3DProjectFile","Sn3DDevice"],
["Sn3DCodeProject"],
["Sn3DMultiProjects"],
["Sn3DManualAlign"],
["Sn3DCommonLib"],
["Sn3DSerialTool","Sn3DDataBaseConfig","Sn3DMeasure","Sn3DPostProcess"],
["Sn3DNavigation"],
["Sn3DSceneController","Sn3DGenerateCloudController","Sn3DFrameDataEditController","Sn3DDeviceController","Sn3DCalibrateController"],
["Sn3DScanController"],
["Sn3DTools","Sn3DScanEditController"],
["Sn3DApplications"]

]
subPath = "codes/"

def main():
    exePath = os.getcwd()
for buildSubArr in buildArr:
    stop = False
    threadArr = []
    for buildOne in buildSubArr:
        oneT = threading.Thread(target=build,args=("./" +subPath+ buildOne, "./build/" + buildOne, True, "conan_export_dev", False, buildOne))
        oneT.setName(buildOne)
        threadArr.append(oneT)
    for runOne in threadArr:
        time.sleep(1)
        runOne.start()
    for joinOne in threadArr:
        joinOne.join();
        oneRet = retArr[joinOne.getName()]
    if(oneRet.get("build")):
        pass
        #prinfResult(buildOne,oneRet)
    else:
        print("build err:"+buildOne)
        stop = True
    if(stop):
        break
threadArr.clear

for buildSubArr in buildArr:
    for buildOne in buildSubArr:
        oneRet = retArr[buildOne]
        prinfResult(buildOne,oneRet)


if __name__ == "__main__":
    main()