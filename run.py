import os
os.chdir(r'D:\图片\小思框架\m第十二代\wanlyOS-Python\System_Program\pyexe\firewall')
import tkinter
import pyautogui
##print(pyautogui.confirm(text='请问是否需要继续?',title="提示"))##(win32api.MessageBox(0,'你好',['呵呵','12'],win32con.MB_OK))
def askc(t):
    return pyautogui.confirm(text='未知端口：'+str(t)+' 是否阻止通讯并关闭发起程序？',title='WanlyOS_FireWall')=='OK'#askquestion('WanlyOS_FireWall', '未知端口：'+str(t)+' 是否阻止通讯并关闭发起程序？')=='yes'

# -*- coding: UTF-8 -*-
def netportpid(port: int):
    """根据端口寻找该进程对应的pid"""
    adict = {}
    # 获取当前的网络连接信息
    net_con = psutil.net_connections()
    for con_info in net_con:
        if con_info.laddr.port == port:
            adict[port] = con_info.pid
    return adict
'''
————————————————
版权声明：本文为CSDN博主「adsszl_no_one」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/adsszl_no_one/article/details/103665341
'''


import os
import re


def kill_process(port):
    ret = os.popen("netstat -nao|findstr " + str(port))
    #注意解码方式和cmd要相同，即为"gbk"，否则输出乱码
    
    str_list = ret.read()##.encode('utf-8').decode('gbk')
    ##print('1',str_list)
    
    ret_list = re.split('\n',str_list)
    ##print('list',ret_list)
    try:
        process_pid = list(ret_list[0].replace('  ',' ').split(' '))[-1]

        os.popen('taskkill /pid ' + str(process_pid) + ' /F')
        return 0
    except KeyError:
        return -1


from os import name
import threading
from socket import *
import tqdm                                 # 进度条，可自行加上
import psutil
   
 
lock = threading.Lock()                     # 确保 多个线程在共享资源的时候不会出现脏数据
openNum=0                                   # 端口开放数量统计
threads=[]                                  # 线程池

with open('name.txt','r',encoding='utf-16 be') as f:
    read=f.readlines()
    for i in range(len(read)):
        read[i]=read[i].replace('\n','').replace('','')
print(read)
def update():#更新数据库
    global read
    with open('name.txt','r',encoding='utf-16 be') as f:
        read=f.readlines()
        for i in range(len(read)):
            read[i]=read[i].replace('\n','').replace('','')
def portscanner(host,port,mode=3):
    
    global openNum,read,askc
    
    try:
        s=socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        lock.acquire()
        openNum+=1
        ##print(f"{port} open")
        lock.release()
        s.close()
        if 1:
            ##print(port,22222222222)
            p = psutil.Process(list(netportpid(port).values())[0])
            ##print(11111111111)
            n=p.name()
            e=p.exe()##.split('\\')[-1]
            ##print(e,e in read,'\n\n')
            '''
            f=0
            
            for i in read:
                if mode==1:#仅全部数据，极疏松
                    if i!=n and i!=e and i!=str(port):
                        f=1
                elif mode==2:#关注进程名，疏松
                    if i!=n:
                        f=1
                elif mode==3:#关注发起程序，严格（默认）
                    if i!=e:
                        f=1
            '''
            if e!='':
                if mode==1:#严格
                    if not e in read:#f:
                        try:
                            if askc(str(port)+',发起程序：'+e):
                                kill_process(port)
                                print('kill:\t'+str(port)+'\nname:\t'+str(n)+'\ndir:\t'+str(e)+'\n\n')
                            else:
                                print('ignore:\t'+str(port)+'\nname:\t'+str(n)+'\ndir:\t'+str(e)+'\n\n')
                                with open('name.txt','a',encoding='utf-16 be') as f:
                                    f.write('\n'+e)
                                    update()
                        except Exception as err:
                            print('err',err)
                if mode==2 or mode==3:#疏松（默认）
                    if not e in read and not n in read and not str(port)in read:#f:
                        try:
                            if askc(str(port)+',发起程序：'+e):
                                kill_process(port)
                                print('kill:\t'+str(port)+'\nname:\t'+str(n)+'\ndir:\t'+str(e)+'\n\n')
                            else:
                                print('ignore:\t'+str(port)+'\nname:\t'+str(n)+'\ndir:\t'+str(e)+'\n\n')
                                with open('name.txt','a',encoding='utf-16 be') as f:
                                    f.write('\n'+e+'\n'+str(port)+'\n'+n)
                                    update()
                        except Exception as err:
                            print('err',err)
                        
    except:
        ##print(111)
        pass
    return
def main(ip,ports=range(1024,65535),mode=3):            #全端口扫描 设置端口缺省值0-65535
    print('start')
    setdefaulttimeout(1)
    idx=1
    le=len(ports)
    for port in (ports):
        ##print(idx/le*100,'%')
        t=threading.Thread(target=portscanner,args=(ip,port,mode))
        threads.append(t)
        t.setDaemon(True)
        th=threading.active_count()
        while th>7000:
            time.sleep(1)
            print('threading too much.',th)
            ##threads[0].join()
            th=threading.active_count()
            print('threading much.',len(threads))
        while len(threads)>60000:
            threads.pop(0)
        t.start()
        ##print()
        idx+=1
    idx=1
    le=len(ports)
    for t in threads:
        ##print(idx/le*100,'%')
        t.join()
        idx+=1
    print('end')
    ##print(f"PortScan is Finish ，OpenNum is {openNum}")  
def amain(ip,ports=[3000],mode=3):            # 单个端口扫描
    print('start')
    setdefaulttimeout(1)
    idx=1
    le=len(ports)
    for port in (ports):
        t=threading.Thread(target=portscanner,args=(ip,port,mode))
        threads.append(t)
        t.setDaemon(True)
        
        print(threading.active_count())
        t.start()
        ##print()
        idx+=1
    idx=1
    le=len(ports)
    for t in threads:
        t.join()
        idx+=1
    print('end')

from PIL import Image

import pystray
def dei():
    global app1
    app1.deiconify()
def wd():
    global app1
    app1.withdraw()
image = Image.open('logo.ico')
icon = pystray.Icon('Neural', image, title='WanlyOS_FireWall', menu=pystray.Menu(
    pystray.MenuItem('打开主界面', dei, default=True),  # 鼠标被单击事件
    pystray.Menu.SEPARATOR,

    pystray.MenuItem('隐藏主界面', wd),  # 鼠标被单击事件
    pystray.Menu.SEPARATOR,
    
    pystray.MenuItem('退出', lambda y: quit()),
    pystray.Menu.SEPARATOR,
))


##icon.run()  # 【注】 此方式为阻塞
t=threading.Thread(target=icon.run,args=())
t.setDaemon(True)
t.start()
##t.join()


on=0
def on_switch1():
    global on
    if on==1:
        on=0
    else:
        on=1

import tkinter as tk
from PIL import Image, ImageTk



class FirewallWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        ##self.master = self##tk.Tk()
        self.master = master
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        # 创建画布对象
        self.canvas = tk.Canvas(self, width=400, height=200)
        self.canvas.pack()

        # 创建图像对象并加载防火墙图标
        firewall_image = Image.open("logo.ico")
        firewall_image = firewall_image.resize((128, 128))
        self.firewall_img = ImageTk.PhotoImage(firewall_image)

        # 创建标签控件并添加图像对象
        label = tk.Label(self, image=self.firewall_img)
        label.pack()

        

        # 创建开关控件并添加事件处理函数
        self.switch = tk.BooleanVar()
        self.switch.set(False)
        self.on_switch = lambda: self.update_status()
        self.toggle_button = tk.Checkbutton(self, text="开启防火墙", variable=self.switch, command=self.on_switch)
        self.toggle_button.pack()

        # 创建文本框控件并添加事件处理函数
        self.status_text = tk.Label(self, height=10, state='disabled')
        self.status_text.pack()
        self.update_status()

        #隐藏按钮
        labe = tk.Button(self, text='隐藏', command=wd)
        labe.pack()
    def update_status(self):
        on_switch1()
        # 根据开关状态更新防火墙状态文本框内容
        if self.switch.get():
            
            status = "已开启防火墙"
            self.status_text.config(state='normal', text=status)
        else:
            
            status = "未开启防火墙"
            self.status_text.config(state='disabled', text=status)
    

app1=tk.Tk()
app=FirewallWindow(app1)
app1.title('FirewallWindow')
on=0

##tk.Tcl().start()
##
'''
t=threading.Thread(target=app.mainloop,args=())
t.setDaemon(True)
t.start()
'''
if __name__ == '__main__':
    import time
    def start():
        global on
        while True:
            if on:
                t1=time.time()
                ip='127.0.0.1'
                main(ip,mode=1)                               # 全端口扫描
                print('time',time.time()-t1)
            else:
                time.sleep(0.1)
    t=threading.Thread(target=start,args=())
    t.setDaemon(True)
    t.start()
    app.mainloop()
