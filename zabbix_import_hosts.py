# -*- coding: utf-8 -*- 
import xlrd
from pyzabbix import ZabbixAPI
import pprint

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

file_name=raw_input('请输入导入文件名')
try:
    zapi = ZabbixAPI("http://localhost/zabbix")
    zapi.login("admin", "zabbix")
except:
    print '\n 登录zabbix平台出现错误'
    sys.exit()

def get_templateid(template_name):
    template_data = {
        "host": [template_name]
    }
    result = zapi.template.get(filter=template_data)
    if result:
        return result[0]['templateid']
    else:
        return result

def check_group(group_name):
    return zapi.hostgroup.exists(name=group_name.strip())

def create_group(group_name):
    groupid=zapi.hostgroup.create(name=group_name)

def get_groupid(group_name):
    group_date = {
        "name":[group_name]
    }
    return str(zapi.hostgroup.get(filter=group_date)[0]['groupid'])

def create_host(host_data):
    zapi.host.create(host_data)
 
def open_excel(file= file_name):
     try:
         data = xlrd.open_workbook(file)
         return data
     except Exception,e:
         print str(e)

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
  hosts=get_hosts(file)
  for host in hosts:
      host_name=host[0]
      visible_name=host[1]
      host_ip=host[2]
      group=host[3]
      template=host[4]
      templateid=get_templateid(template)
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
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
      }
      print "添加主机: %s ,分组: %s ,模板ID: %s" % (visible_name,group,templateid)
      create_host(host_data)

if __name__=="__main__":
    main()
