#!/usr/bin/env python
# -*- coding: utf_8 -*-

import os
import shutil

import logging
from logging.handlers import RotatingFileHandler

logPath = os.getcwd() + os.path.sep + "logs"
if not os.path.exists(logPath):
    os.makedirs(logPath)

fh = RotatingFileHandler("showcase.log", maxBytes=10 * 1024 * 1024, backupCount=100)
fh.setLevel(logging.DEBUG)
#log write in console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#log formatter
formatter = logging.Formatter(
    '%(asctime)s %(levelname)8s [%(filename)25s%(funcName)20s%(lineno)06s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger = logging.root
logger.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(ch)


def copydirs(from_file, to_file):
    if not os.path.exists(to_file):  # 如不存在目标目录则创建
        os.makedirs(to_file)
    files = os.listdir(from_file)  # 获取文件夹中文件和目录列表
    for f in files:
        if os.path.isdir(from_file + os.sep + f):  # 判断是否是文件夹
            copydirs(from_file + os.sep + f, to_file + os.sep + f)  # 递归调用本函数
        else:
            shutil.copy(from_file + os.sep + f, to_file + os.sep + f)  # 拷贝文件

def rmdirs(dirpath):
    if os.path.exists(dirpath):
        files = os.listdir(dirpath)
        for file in files:
            filepath = os.path.join(dirpath, file).replace("\\",'/')
            if os.path.isdir(filepath):
                rmdirs(filepath)
            else:
                os.remove(filepath)
        os.rmdir(dirpath)

def generateProjects(path):
    '''
        获取指定path下的所有文件列表
    '''
    ignore_dir = ['.git']
    templateDir = os.sep.join([os.getcwd(), "helloworld"])
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for d in ignore_dir:
            # print(dirpath)
            # print(os.sep.join([os.getcwd(), d]))
            # print(dirpath.startswith(os.sep.join([os.getcwd(), d])))
            if dirpath.startswith(os.sep.join([os.getcwd(), d])):
                continue
        # print(dirpath, dirnames, filenames)
        if filenames == ['index.css', 'index.hml', 'index.js']:
            # componentID = "%s-%s" %    os.path.basename(dirpath)
            pathkeys = dirpath.split(os.sep)
            if 'component' in dirpath:
                index = pathkeys.index('component')
                projectName = "showcase-%s" % "-".join(pathkeys[index+1:])
            else:
                index = pathkeys.index('examples')
                projectName = pathkeys[index+1]
                if projectName == "showcase":
                    projectName = "showcase-index"
            
            #创建目录
            projectDir = os.sep.join([os.getcwd(), projectName])
            if os.path.exists(projectDir):
                rmdirs(projectDir)
            if not os.path.isdir(projectDir):
                os.makedirs(projectDir)

            logger.info("generate project [%s]-[%s]" % (projectName, projectDir))
            copydirs(templateDir , projectDir)

            defaultDir = os.sep.join(pathkeys[0:pathkeys.index('default')+1])
            projectDir =  os.sep.join([projectDir, "entry", "src", "main", "js","default"])
            if os.path.exists(defaultDir):
                copydirs(defaultDir , projectDir)
                rmdirs(os.sep.join([projectDir, "pages"]))
            
            projectPageDir = os.sep.join([projectDir, "pages"])
            if os.path.exists(projectPageDir):
                rmdirs(projectPageDir)
            os.makedirs(projectPageDir)

            projectIndexDir = os.sep.join([projectPageDir, "index"])
            if os.path.exists(projectIndexDir):
                rmdirs(projectIndexDir)
            # 拷贝源文件index.hml index.css index.js
            # indexDir = os.sep.join([projectDir, "entry", "src", "main", "js","default","pages","index"])
            os.makedirs(projectIndexDir)
            copydirs(dirpath , projectIndexDir)

            indexFile = os.sep.join([projectIndexDir, "index.js"])
            with open(indexFile, "r") as f:
                content = str(f.read())
            isReWrite = False
            if "../../../../../common/js/general" in content:
                content = content.replace("../../../../../common/js/general", "../../common/js/general")
                isReWrite = True
            elif "../../../../common/js/general" in content:
                content = content.replace("../../../../common/js/general", "../../common/js/general")
                isReWrite = True
            elif "../../../common/js/general" in content:
                content = content.replace("../../../common/js/general", "../../common/js/general")
                isReWrite = True
            if isReWrite:
                with open(indexFile, "w") as f:
                    f.write(content)

def main():
    generateProjects(os.sep.join([os.getcwd(), "examples"]))


if __name__ == '__main__':
    main()
