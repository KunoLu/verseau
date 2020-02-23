注：

该脚本需要调用的模块为：os, re, shutil；

使用的模块均为python自带模块；


作用：

性能测试工具Loadrunner在以多台其他windows系统的机器作为远程执行机时，
"%USERPROFILE%\AppData\Local\Temp"目录下会生成大量临时日志文件，
每次执行测试场景时候远程连接执行机后，会在上述目录下生成一个"brr_"开头的临时文件目录，该目录及其下所有文件均可删除！
本脚本即在需要清理执行机磁盘空间时，删除所有以"brr_"开头的临时文件目录。
建议该脚本使用前先将主控制机上的执行机远程连接均关闭，或直接关闭测试场景！


使用说明：

在Windows下调用格式为：python clsLrTmp.py

或至clsLrTmp\dist文件夹下，双击clsLrTmp.exe




