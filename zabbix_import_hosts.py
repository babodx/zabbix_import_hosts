# -*- coding: utf-8 -*- 
import xlrd
from pyzabbix import ZabbixAPI
import pprint

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#获取导入的xls文件名
file_name=raw_input('请输入导入文件名')

#尝试登陆zabbix平台
try:
    zapi = ZabbixAPI("http://localhost/zabbix")
    zapi.login("admin", "zabbix")
except:
    print '\n 登录zabbix平台出现错误'
    sys.exit()

#通过模板名获取模板ID
def get_templateid(template_name):
    template_data = {
        "host": [template_name]
    }
    result = zapi.template.get(filter=template_data)
    if result:
        return result[0]['templateid']
    else:
        return result

#检查组名是否已经存在
def check_group(group_name):
    return zapi.hostgroup.exists(name=group_name.strip())

#创建组
def create_group(group_name):
    groupid=zapi.hostgroup.create(name=group_name)

#通过组名获取组ID
def get_groupid(group_name):
    group_date = {
        "name":[group_name]
    }
    return str(zapi.hostgroup.get(filter=group_date)[0]['groupid'])

#添加主机
def create_host(host_data):
    if zapi.host.exists(host=host_data["host"]):
      print "主机 %s 已经存在" % host_data["name"]
    else:
      zapi.host.create(host_data)
      print "添加主机: %s " % (host_data["name"])

#打开xls文件 
def open_excel(file= file_name):
     try:
         data = xlrd.open_workbook(file)
         return data
     except Exception,e:
         print str(e)

#将xls文件内主机导入到list
def get_hosts(file):
    data = open_excel(file)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    list = []
    for rownum in range(1,nrows):
      #print table.row_values(rownum)[0]
      list.append(table.row_values(rownum)) 
    return list

def main():
  hosts=get_hosts(file_name)
  for host in hosts:
      host_name=host[0]
      visible_name=host[1]
      host_ip=host[2]
      group=host[3]
      template=host[4]
      templateid=get_templateid(template)
      inventory_location=host[5]
      #print templateid
      if check_group(group)==False:
          print u'添加主机组: %s' % group
          groupid=create_group(group)
          #print groupid
      groupid=get_groupid(group)
      host_data = {
          "host": host_name,
          "name": visible_name,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": host_ip.strip(),
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": groupid
            }
        ],
        "templates": [
            {
                "templateid": templateid
            }
        ],
        "inventory": {
            "location": inventory_location
        }
      }
      #print "添加主机: %s ,分组: %s ,模板ID: %s" % (visible_name,group,templateid)
      create_host(host_data)

if __name__=="__main__":
    main()
