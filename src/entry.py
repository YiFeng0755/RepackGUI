#-*-coding:utf8 -*-


import sys
import os
sys.path.append(os.path.realpath(__file__))
import json
from config import ConfigParse
import env


def php_entry(arg):
    # 单例
    ConfigParse.shareInstance().initData(arg)
    from pack_managers.newengine_pack_manager import NewEnginePackManager
    NewEnginePackManager().run()

def windowsDebugJson(apkPath=r'E:\TestHoldemSina\apk\sina-release201607311846.apk', targetDir=None, saveLog=False, saveFile=False, timestamp=None, lua_version='3.x'):
    #rsplit()对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串
    # outputDir = apkPath.rsplit('\\',1)[0]
    if targetDir != None:
        outputDir = targetDir
    else:
        outputDir = os.path.dirname(apkPath)
    arg = {
        'apkPath':apkPath.decode('utf-8'),#用户上传的母包的可访问路径
        'configDir':os.path.join(env.GOD_WORK_DIR.decode('utf-8'), 'res_for_autotest'),#预处理资源路径，跟sdkLs中的sdkRelativePath拼接为最终sdk目录
        'outDir':outputDir,#外部路径
        'packageName':'com.boyaa.sina',
        'logDir': os.path.join(outputDir, 'log'),
        'saveLog': saveLog,
        'saveFile': saveFile,
        'timestamp': timestamp,
        'keystore':{#最终反编译二次打包时需要的签名文件,暂时写死使用龙卷风项目组签名文件，后续优化根据需求使用各个项目的签名文件
            'file':os.path.join(env.GOD_TOOL_DIR.decode('utf-8'), 'debug.keystore'),
            'storePassword':'android',
            'keyAlias':'androiddebugkey',
            'aliasPassword':'android'
        },
        'luaversion': lua_version
       }
    # dict -> str
    return json.dumps(arg)
