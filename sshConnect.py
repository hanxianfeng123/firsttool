#coding:utf-8
__author__ = 'qiyanming'
__date__ = '2017/12/18'
import paramiko
from datetime import datetime

class SSHConnection(object):
    def __init__(self, host,  username, pwd, port=22):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self, local_path, remote_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, remote_path)

    def down(self,remote_path,local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        for m in command:
            print('执行命令为：{}'.format(m))
            stdin, stdout, stderr = ssh.exec_command(m)
            # stdin.write("Y")   #简单交互，输入 ‘Y’
            res = stdout.read().decode()
            err = stderr.read().decode()
            result = res if res else err
            print(result)
            # result = stdout.readlines()
            # 屏幕输出
            #for o in result:
            #    print(o)
        return result

    def run(self,command=None,upLoad=None,downLoad=None):
        self.connect()  # 连接远程服务器
        print('执行远程机器为：', self.host)
        sum=''
        if upLoad != None:
            self.upload(upLoad[0],upLoad[1])
            print('将本地文件{}上传成功到服务器{}'.format(upLoad[0],upLoad[1]))
        if downLoad != None:
            self.down(downLoad[0], downLoad[1])
            print('将服务器文件{}下载成功到本地{}'.format(downLoad[0], downLoad[1]))
            #self.upload('/Users/qiyanming/Documents/rootTest/apiTest/testCase/cp/test6.py', '/root/test1.py')  # 将本地的db.py文件上传到远端服务器的/tmp/目录下并改名为1.py
        if command != None:
            sum=self.cmd(command)
        #print(sum)
        self.close()  # 关闭连接
        return sum

if __name__=='__main__':
    obj = SSHConnection(host='10.69.43.28', username='root', pwd='EthicI4APEVeVR')
    obj.run(['ls','pwd'])
    #obj.run(['ls'],downLoad=['/root/test1.py','/Users/qiyanming/Documents/rootTest/apiTest/testCase/cp/test16.py'])
    obj.run(['ls'],upLoad=['/Users/qiyanming/Documents/rootTest/apiTest/testCase/cp/test6.py', '/root/test1.py'])