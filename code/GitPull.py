import os
import sys
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

    color = "31m"
    if not hasErr:
        color = "32m"

    print(f'''\033[{color} {name} : {rslt} \033[0m''')

def pull(giturl:str, destdir:str, remoteBranch:str, myBranch:str, gitName:str) -> bool :
    exePath = os.getcwd();

    cloneRet = subprocess.call(f"git clone {giturl} {destdir} --verbose --progress", cwd=exePath, shell = True)
    print(f"clone {remoteBranch}:{cloneRet}.")

    subprocess.call(f"git -c diff.mnemonicprefix=false -c core.quotepath=false --no-optional-locks fetch --prune --tags origin --verbose --progress", cwd=destdir, shell = True)

    #切换远端到需要拉取的分支
    checkRet = subprocess.call(f"git checkout -b {myBranch} origin/{remoteBranch}", cwd=destdir, shell = True)
    checkRet &= subprocess.call(f"git checkout -b {myBranch} ", cwd=destdir, shell = True)

    print(f"checkout {remoteBranch}:{checkRet}.")
    #拉取
    pullRet = subprocess.call(f"git pull --progress -v --no-rebase \"origin\" {remoteBranch} --verbose --progress", cwd=destdir, shell = True)
    print(f"pull {remoteBranch}:{pullRet}.")
    #推送到远端个人分支（默认和本地分支同名）
    pushRet = subprocess.call(f"git push --progress \"origin\" {myBranch}:{myBranch}",cwd=destdir, shell = True)
    print(f"push {myBranch}:{pushRet}.")
    #更改默认推送的远端分支（避免使用小乌龟等工具推送时推送到了非个人远端分支上）
    checkRet = subprocess.call(f" git push --set-upstream origin {myBranch}", cwd=destdir, shell = True)

    retArr[gitName]=pushRet == 0 and checkRet == 0

    return pushRet == 0 and checkRet == 0

branthName = "wangshuo_dev_freescan_v2.2.0"
subPath = "codes"
remoteBranch = "dev_freescan_v2.2.0"

pullArr = [
    "Sn3DCommonDepenDence",
    "Sn3DFrameWork",
    "Sn3DDigitGlobal",
    "sn3ddeviceconnectmanger",
    "Sn3DDigtalAlgorithm",
    "Sn3DImageQueue",
    "Sn3DFirmwareUpdate",
    "Sn3DSoftWareUpdate",
    "Sn3DUICommon",
    "Sn3DPlayer",
    "Sn3DUserAccount",
    "Sn3DProjDefaultPath",
    "Sn3DTexture",
    "Sn3DSecurity",
    "Sn3DInformation",
    "Sn3DAutoExposure",
    "Sn3DFunction",
    "Sn3DClientFrameWork",
    "Sn3DCalibration",
    "Sn3DAlgorithmWrapper",
    "Sn3DProjectFile",
    "Sn3DDevice",
    "Sn3DCodeProject",
    "Sn3DMultiProjects",
    "Sn3DManualAlign",
    "Sn3DCommonLib",
    "Sn3DSerialTool",
    "Sn3DDataBaseConfig",
    "Sn3DMeasure",
    "Sn3DPostProcess",
    "Sn3DNavigation",
    'Sn3DSceneController',
    "Sn3DGenerateCloudController",
    "Sn3DFrameDataEditController",
    "Sn3DDeviceController",
    "Sn3DCalibrateController",
    "Sn3DScanController",
    "Sn3DTools",
    "Sn3DScanEditController",
    "Sn3DApplications"
]

threadArr = []
for pullOne in pullArr:
    oneT = threading.Thread(target=pull,args=("ssh://git@gitlab.shining3d.io:10122/sn3dscanplatform2022/"+pullOne.lower()+".git", "./"+subPath+"/"+pullOne, remoteBranch, branthName,pullOne))
    oneT.setName(pullOne)
    threadArr.append(oneT)
for oneThread in threadArr:
    time.sleep(1)
    oneThread.start()
for oneJoin in threadArr:
    oneJoin.join()
    oneRet = retArr[oneJoin.getName()]
    print("-------------------------------",oneRet)
    prinfResult(oneJoin.getName(),oneRet)