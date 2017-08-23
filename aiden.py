#!/usr/bin/python
# -*- coding: utf-8 -*-
"""for dedecms 
*Version:v1.0
*Time   :2017.04.20 
"""
__author__ = '陈金林'

import os
import sys
import glob
import re
import pymysql
import pwd
import time

class Web(object):
    __hostName = '' #域名：www.xxx.com
    __confPath = '/usr/local/nginx/conf/vhost/' #host 配置文件夹
    __dbConfigFile = 'data/common.inc.php' #数据库配置文件 
    __tplKey = 'nk' #网站当前风格模板目录通配字符
    __templets = 'templets' #网站所有模板总目录
    __specialTypename = '专题管理' #存放专题的目录

    __webuser = 'htdocs' #网站目录所属用户

    def __init__(self,host=''):
        self.__hostName = host

    @property
    def host(self):
        return self.__hostName
    @host.setter
    def host(self,host):
        self.__hostName = host
        return self.__hostName
    #域名与目录绑定
    def serverRoot(self):
        conf_list = glob.glob(os.path.join(self.__confPath,"*.conf")) #配置文件列表
        serverRoot = {}
        for conf in conf_list:
            with open(conf,'r') as f:
                sroot = ''
                sserver = ''
                for line in f.readlines():
                    mserver = re.match("^server_name.*;$",line.strip())
                    mroot = re.match("^root.*;$",line.strip())
                    if mserver:
                        sserver = mserver.group(0).strip(";").split()[1:]
                        continue
                    if mroot:
                        sroot = mroot.group(0).strip(";").split()[-1]
                        continue
                    if sroot and sserver:
                        break
                if sroot not in serverRoot:
                    serverRoot[sroot]=sserver
                else:
                    serverRoot[sroot]=serverRoot[sroot]+sserver
        return serverRoot
    #根据域名获取域名对应实际绝对路径
    def documentRoot(self):
        host = self.__hostName
        serverRoot = self.serverRoot()
        for (root,server) in serverRoot.items():
            if host in server:
                return root

    #获取数据库配置信息
    def dbConfig(self):
        configFile = os.path.join(self.documentRoot(),self.__dbConfigFile)
        if not os.path.exists(configFile):
            print('配置文件不存在或路径错误！')
            exit()
        config = {}
        with open(configFile,'r') as f:
            for line in f.readlines():
                dbname = re.match("^\$cfg_dbname.*;$",line.strip()) # 有三行以上注释的情况下可能会出错
                if dbname:
                    dbname = dbname.group(0)
                    db_name = dbname.split('\'') if dbname.find("'")!=-1 else dbname.split('"')
                    config['db_name'] = db_name[1]
                    continue
                dbuser = re.match("^\$cfg_dbuser.*;$",line.strip())
                if dbuser:
                    dbuser = dbuser.group(0)
                    db_user = dbuser.split('\'') if dbuser.find("'")!=-1 else dbuser.split('"')
                    config['db_user'] = db_user[1]
                    continue
                dbpwd = re.match("^\$cfg_dbpwd.*;$",line.strip())
                if dbpwd:
                    dbpwd = dbpwd.group(0)
                    db_password = dbpwd.split('\'') if dbpwd.find("'")!=-1 else dbpwd.split('"')
                    config['db_password'] = db_password[1]
                    continue
                dbprefix = re.match("^\$cfg_dbprefix.*;$",line.strip())
                if dbprefix:
                    dbprefix = dbprefix.group(0)
                    db_prefix = dbprefix.split('\'') if dbprefix.find("'")!=-1 else dbprefix.split('"')
                if len(config) >= 4:
                    break
        return config
        tplKey= self.__tplKey
        templetDir = os.path.join(self.documentRoot(),self.__templets)
        tempdirs = os.listdir(templetDir)
        for i in tempdirs:
            if not i.find(tplKey) == -1:
                return os.path.join(templetDir,i)
    #网站用户的uid gid
        user={}
        user['name']= webuser.pw_name
        user['uid']= webuser.pw_uid
                if dbname:
                    dbname = dbname.group(0)
                    db_name = dbname.split('\'') if dbname.find("'")!=-1 else dbname.split('"')
                    config['db_name'] = db_name[1]
                    continue
                dbuser = re.match("^\$cfg_dbuser.*;$",line.strip())
                if dbuser:
                    dbuser = dbuser.group(0)
                    db_user = dbuser.split('\'') if dbuser.find("'")!=-1 else dbuser.split('"')
                    config['db_user'] = db_user[1]
                    continue
                dbpwd = re.match("^\$cfg_dbpwd.*;$",line.strip())
                if dbpwd:
                    dbpwd = dbpwd.group(0)
                    db_password = dbpwd.split('\'') if dbpwd.find("'")!=-1 else dbpwd.split('"')
                    config['db_password'] = db_password[1]
                    continue
                dbprefix = re.match("^\$cfg_dbprefix.*;$",line.strip())
                if dbprefix:
                    dbprefix = dbprefix.group(0)
                    db_prefix = dbprefix.split('\'') if dbprefix.find("'")!=-1 else dbprefix.split('"')
                    config['db_prefix'] = db_prefix[1]
                    continue
                if len(config) >= 4:
                    break
        return config


