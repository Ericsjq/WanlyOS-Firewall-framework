@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin
D:
cd D:\图片\小思框架\m第十二代\wanlyOS-Python\System_Program\pyexe\firewall
python3.8 run.py
