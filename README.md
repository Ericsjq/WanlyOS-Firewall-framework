WanlyOS-Firewall-framework(WanlyOS防火墙框架)
==========================
# 中文文档

WannyOS 的防火墙框架，这只是规则检索的最基本部分。

支持最小化至系统托盘：

![alt 主界面](https://4147093qp2.imdo.co/bbb.png)

![alt 系统托盘](https://4147093qp2.imdo.co/aaa.png)

窗口界面使用tkinter编辑，系统托盘功能需要pyautogui库。


# 主要功能
实时检索本机所有开放端口，获取占用端口的程序，如果程序不存在于规则文件name.txt (utf-16 be) 中，则询问并关闭该进程。

# 引用函数
```python
amain(ip='127.0.0.1',ports=[3000],mode=3)#检索指定端口
main(ip='127.0.0.1',ports=range(1024,65535),mode=3)#检索1024-65535端口
#两个函数代码类似
#mode=1为疏松模式
#mode=2或3为严格模式
```

English document
----------------
WannyOS firewall framework, this is only the most basic part of rule retrieval.

Support minimization to system tray:

![ alt home screen ](https://4147093qp2.imdo.co/bbb.png )

![ Alt System Tray ](https://4147093qp2.imdo.co/aaa.png )

The window interface is edited using tkinter, and the system tray functions require PYAUTOGUI libraries.

# the main function

Real-time retrieval of all open ports of the machine, access to the ports occupied by the program, if the program does not exist in the rules file name.txt (utf-16 be) , the process is queried and shut down.



@2023小思框架 https://xiaothink.mysxl.cn
