# weblog
api错误统计 /实时日志 web显示
-----------------------------------  
    为方便统计 服务器日志错误,查询出mi,ms 出错文件 (400+服务器)
    设想:
      每台服务器计划任务 脚本过滤出错误日志,得出数据后提交至http接口
      curl -d "rc=20043&uin=43252452&mbox=/home/xxoo&des=error" http://ip:5000/api  
    服务器上统计出报表

    实时日志设计: 
      无需登录服务器,web 使用 Server-Sent Events(SSE)保持长连接,实时输出日志,支持关键过虑,红色标记
      方便快速查询日志
### 基本流程<br /> 
![image](https://github.com/llych/weblog/blob/master/screenshots/3.png)

### web实时日志,支持关键字红色标记<br /> 
![image](https://github.com/llych/weblog/blob/master/screenshots/4.png)

### 统计折线图<br /> 
![image](https://github.com/llych/weblog/blob/master/screenshots/5.png)

### 日志查询<br /> 
![image](https://github.com/llych/weblog/blob/master/screenshots/1.png)
![image](https://github.com/llych/weblog/blob/master/screenshots/2.png)



