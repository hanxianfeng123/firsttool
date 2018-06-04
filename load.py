#coding:utf-8
__author__ = 'qiyanming'
__date__ = '2017/12/18'
import sys
sys.path.append('../')
from sshConnector.sshConnect import SSHConnection
import threading
import time
from sshConnector.config import ld35,ld70,ld2,ld17,sbasedir
import configparser
from configparser import MissingSectionHeaderError

class load():
    def __load__(self,ldfile,hosts,jtlfile):
        return ['/root/jmeter/bin/jmeter -n -t /root/jmeter/bin/test/qym/{0} -R {1} -l /root/jmeter/bin/test/qym/{2}'.format(ldfile,hosts,jtlfile)]

    def __delf__(self,file):
        return ['rm -rf /root/jmeter/bin/test/qym/{}'.format(file)]

    def __killp__(self,process='jmeter'):
        return ['ps -ef|grep {}|grep -v grep|cut -c 9-15|xargs kill -9'.format(process)]

    def __startServer__(self,hosts):
        return ['nohup /root/jmeter/bin/jmeter-server -Djava.rmi.server.hostname={} &'.format(hosts)]

    def get_settings(self,filename):
        config = configparser.ConfigParser()
        try:
            config.read(filename, encoding='utf-8')
        except MissingSectionHeaderError:
            config.read(filename, encoding='utf-8-sig')
        return config

    def load(self,ld,upfile,downfile,lbasedir,load,update,server):
        client = SSHConnection(host=ld['hosts'], username=ld['username'], pwd=ld['pwd'])
        if server == 'N':
            #删除服务器jtl文件
            if downfile is not None:
                client.run(self.__delf__(downfile))
            else:
                raise AttributeError("没有输入jtl文件名称,或输入错误")
            #上传jmx文件到服务器
            if update == 'Y':
                if upfile is not None:
                    client.run(upLoad=[lbasedir + upfile, sbasedir + upfile])
                else:
                    raise AttributeError("没有输入jmx文件名称，或输入错误")

            # 运行jmeter脚本
            if load == 'Y':
                client.run(self.__load__(upfile, ld['hosts'], downfile))
                # 下载jtl文件到本地
                if downfile.lower() != 'no':
                    if ld['hosts'] == '10.70.20.35':
                        client.run(downLoad=[sbasedir + downfile, lbasedir + downfile])
        elif server == 'Y':
            client.run(self.__killp__())
            print('重启完毕jmeter服务,请把server参数改为N,并停止程序重新运行！')
            client.run(self.__startServer__(ld['hosts']))
        else:
            raise AttributeError("server参数输入错误，只允许输入Y或者N")

    def choice(self,num,upfile,downfile,lbasedir,load,update,server):
        if num == 1:
            print('只启动1台机器,压力机35')
            self.load(ld35,upfile,downfile,lbasedir,load,update,server)
        elif num == 2:
            print('同时启动2台机器,压力机35/70')
            threading.Thread(target=self.load, args=(ld35,upfile,downfile,lbasedir,load,update,server,)).start()
            threading.Thread(target=self.load, args=(ld70,upfile,downfile,lbasedir,load,update,server,)).start()
        elif num == 3:
            print('同时启动3台机器,压力机35/70/2')
            threading.Thread(target=self.load, args=(ld35,upfile,downfile,lbasedir,load,update,server,)).start()
            threading.Thread(target=self.load, args=(ld70,upfile,downfile,lbasedir,load,update,server,)).start()
            threading.Thread(target=self.load, args=(ld2,upfile,downfile,lbasedir,load,update,server,)).start()
        elif num == 4:
            print('同时启动压力机35/70/2/17')
            threading.Thread(target=self.load, args=(ld35,upfile,downfile,lbasedir,load,update,server,)).start()
            threading.Thread(target=self.load, args=(ld70,upfile,downfile,lbasedir,load,update,server,)).start()
            threading.Thread(target=self.load, args=(ld2,upfile,downfile,lbasedir,load,update,server,)).start()
            threading.Thread(target=self.load, args=(ld17,upfile,downfile,lbasedir,load,update,server,)).start()
        else:
            raise AttributeError("目前只允许最多4台压力机")

if __name__=='__main__':
    ld = load()
    config = ld.get_settings('config.ini')
    lbasedir = config['File']['FilePath']
    if not lbasedir.endswith('/'):
        lbasedir += '/'
    num = int(config['Load']['Num'])
    upfile = None if not config['File']['UpFile'] else config['File']['UpFile']
    downfile = None if not config['File']['DownFile'] else config['File']['DownFile']
    load = config['Load']['Load']
    update = config['Load']['Update']
    server = config['Server']['Server']
    ld.choice(num,upfile,downfile,lbasedir,load,update,server)
    from sshConnector.saveLog import save
    import os
    print("输入任意按键开始保存日志文件")
    os.system('pause')
    os.system('read -n 1')
    save()