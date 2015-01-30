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

