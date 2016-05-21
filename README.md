# Team
Team Blog System

# LICENSE
MIT

# 使用
> 1. yum -y install mysql-devel python-devel gcc gcc-c++
> 2. pip install -r requirements.txt
> 3. 修改pub/config.py配置文件，四段内容，GLOBAL、PRODUCT、MYSQL、BLOG，根据实际情况配置。
> 4. sh ./ControlTeamApiRun.sh

此时netstat -anptl查看进程，应该可以看到类似以下的信息(其中Team.Api是你配置文件中定义的)：

```tcp        0      0 0.0.0.0:10040               0.0.0.0:*                   LISTEN      31355/Team.Api```

或者ps aux | grep Team.Api过滤下，应该可以看到类似以下的信息(其中Team.Api是你配置文件中定义的)：

```500      31355  0.0  2.1 334368 21424 ?        S    May20   0:00 Team.Api```

如果没有正常监听系统，请直接运行，查看具体输出或查看logs/sys.log：

```python Product.py```

如有问题，请到[https://github.com/saintic/Team/issues][1]提出问题。

[1]: https://github.com/saintic/Team/issues
