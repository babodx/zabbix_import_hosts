# zabbix_import_hosts
zabbix批量导入监控主机

## 用途
从excel表中批量导入被监控主机

自动根据分组名称创建分组

根据模板名称匹配主机监控模板


# 使用前提
程序需要使用pyzabbix xlrd requests三个库
```
pip install xlrd
pip install requests
pip install pyzabbix

```

# 用法演示
```
python zabbix_import_hosts.py 

请输入导入文件名hostlist.xls
主机 主机1 已经存在
添加主机: 数据库1 
添加主机: 数据库2
添加主机: WEB主机1
添加主机: WEB主机2 
添加主机: WEB主机3

```
