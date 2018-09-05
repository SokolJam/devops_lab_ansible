ANSIBLE_METADATA = {'metadata_version': '1.1',
    		    'status': ['preview'],
    		    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: My_custom_module
version_added: "1.0"
short_description: Simple Ansible Module written on Python
description:
    "This is a module which which performs service's tests:
    - process is running as expected (by name, under user)
    - port is handled by proper process, in listening mode
    - web content of given url contains given regexp string
    - web server information (curl -IL url) contains given regexp string"
options:
    name:
        description: Simple Ansible Module written on Python
        required: true
author:
    - "Yauheni Sokal"
'''


EXAMPLES = """
# Standalone mode launch.
ansible localhost -M ./roles/my_test/library/ -m ysokal_module.py -a 'process=httpd owner=apache port=80'
"""

RETURN = '''webserver => {
    "msg": {
        "port_check": {
            "port": 80, 
            "listening": "yes"
        }, 
        "process_check": {
            "process": "httpd", 
            "owner": "apache", 
            "status": "running"
        }
    }, 
    "changed": false
}'''


from ansible.module_utils.basic import *
import subprocess
import psutil
import socket


def process_check(name, user):
    for proc in psutil.process_iter():
        if name == proc.name():
            if user == proc.username():
                return True
    else:
        return False


def port_handler(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('127.0.0.1', port)) == 0:
        return True
    else:
        return False


def check_server(url, regexp, key=''):
    proc = subprocess.Popen("curl {} {} | grep -e {}".format(key, url, regexp),
                               shell=True, stdout=subprocess.PIPE)
    if proc.communicate()[0]:
        return True
    else:
        return False


def main():
    module = AnsibleModule(
        argument_spec=dict(process=dict(required=True, type=str),
                           owner=dict(required=True, type=str),
                           port=dict(required=True, type=int),
                           content=dict(required=False, type=str),
                           server=dict(required=False, type=str)),
        supports_check_mode=True)

    process_name = module.params['process']
    user_process = module.params['owner']
    port_number = module.params['port']
    content = module.params['content']
    server = module.params['server']
    
    result = {}

    if process_check(process_name, user_process):
        result["process_check"] = {"process": process_name, "owner": user_process, "status": "running"}
    else:
        result["process_check"] = {"process": process_name, "owner": user_process, "status": "not exist"}

    if port_number:
       if port_handler(port_number):
            result["port_check"] = {"port": port_number, "listening": "yes"}
       else:
            result["port_check"] = {"port": port_number, "listening": "no"}

    if server and content:
        if check_server(server, content):
            result["server_content_check"] = {"url": server, "content": content, "state": "exist"}
        else:
            result["server_content_check"] = {"url": server, "content": content, "state": "not exist"}

        if check_server(server, content, '-IL'):
            result["server_info_check"] = {"url": server, "content": content, "state server information": "exist"}
        else:
            result["server_info_check"] = {"url": server, "content": content, "state server information": "not exist"}

    module.exit_json(changed=False, msg=result)
    module.fail_json(changed=False, msg=result)


if __name__ == '__main__':
    main()

