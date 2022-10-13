import os
from bs4 import BeautifulSoup
import requests


def ping_test(ip):
    """
    ping测试
    :param ip: (str) 测试目标IP地址
    :return: (boolean) 成功为True 失败为False
    """
    p = os.popen("ping " + ip + " -n 1")
    line = p.read()
    if "请求超时" in line:
        return False
    else:
        return True


def api_ip138(domain):
    """
    ip138的域名IP查询接口
    :param domain: (str) 域名
    :return: (list) IP列表
    """
    api = "https://site.ip138.com/domain/read.do?domain="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37'
    }
    json = requests.get(api + domain, headers=headers).json()
    ip_list = []
    if json["status"]:
        data = json["data"]
        for item in data:
            ip_list.append(item["ip"] + " " + domain)
    return ip_list


def api_chinaz(domain):
    """
    chinaz的域名IP查询接口
    :param domain: (str) 域名
    :return: (list) IP列表
    """
    api = "https://ip.tool.chinaz.com/github.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37'
    }
    data = {
        "ip": domain
    }
    r = requests.post(api, json=data).text
    soup = BeautifulSoup(r, "html.parser")
    ip_list = []
    for item in soup.select("#IpValue"):
        ip_list.extend(item.contents)
    ip_list = [item + " " + domain for item in ip_list]
    return ip_list


# todo
# 网站有加密 没能解开所以暂时留着
def api_tool_lu(domain):
    """
    tool.lu的域名IP查询接口
    :param domain: (str) 域名
    :return: (list) IP列表
    """
    api = "https://tool.lu/ip/ajax.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37'
    }
    data = {
        "ip": domain
    }
    session = requests.session()
    session.get("https://tool.lu/ip", headers=headers)
    print(session.cookies.get_dict())
    r = session.post(api, headers=headers, data=data).text
    print(r)
    soup = BeautifulSoup(r, "html.parser")
    # ip_list = []
    # for i in soup.select("#IpValue"):
    #     ip_list.append(i.contents)
    # return ip_list


def get_domain_ip(domains):
    """
    调用多个接口聚合查询
    :param domains: (list) 域名列表
    :return: (list) IP 域名列表
    """
    domain_ip = []
    for domain in domains:
        try:
            if domain == "" or domain == "\n":
                continue
            domain_ip.extend(api_ip138(domain))
            domain_ip.extend(api_chinaz(domain))
        except:
            pass
    domain_ip.extend(get_my_domain())
    return list(set(domain_ip))


def get_replace_dict():
    """
    获取要替换的域名字典
    :return: (dict) 替换规则字典
    """
    with open("replace.txt", "r") as r:
        domains_str = r.readlines()
    domain_dict = {}
    for domain in domains_str:
        if " " not in domain:
            continue
        domain = domain.replace("\n", "")
        line = domain.split(" ")
        domain_dict[line[0]] = line[1]
    return domain_dict


def get_my_domain():
    """
    获取自定义domain列表
    :return: (list) 自定义的domain列表
    """
    with open("my_domain.txt", "r") as r:
        return r.readlines()


# 替换
if __name__ == '__main__':
    print("hosts自动修改 by jack_ma")
    print("开源地址：https://github.com/1689798397/hosts")
    print("\n")
    with open("domain.txt", "r") as f:
        domain_list = f.readlines()
    domain_str = ""
    for i in get_domain_ip(domain_list):
        domain_str = domain_str + i
    re_dict = get_replace_dict()
    for i in re_dict:
        domain_str = domain_str.replace(i, re_dict[i])
    try:
        with open("C:\Windows\System32\drivers\etc\hosts", "w") as f:
            f.write(domain_str)
            os.system("ipconfig/flushdns")
            os.system("修改成功！")
            print("\n")
    except:
        print("\n")
        print("权限不足，修改失败！")
        print("请鼠标右键此程序 使用管理员身份运行！ ")
    print("\n")
    os.system("pause")
