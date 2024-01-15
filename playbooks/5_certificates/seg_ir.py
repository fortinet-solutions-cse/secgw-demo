#!/usr/bin/python3

import paramiko
import yaml

vars_file = "/fortipoc/ansible/vars/global.yml"

# Read the local command from the file
def read_command_from_file(file_path):
    with open(file_path, 'r') as file:
        _command = file.read().strip()
    return _command

# def load yaml file
def open_yaml_vars(yaml_file_path):
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def run_command_file(host, command_file, ssh_port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, ssh_port, username, password)

    ## read file
    command = read_command_from_file(command_file)
    _stdin, _stdout, _stderr = client.exec_command(command)
    output = _stdout.read().decode()
    
    client.close()
    del _stdin, _stdout, _stderr
    
    return output


# read vars.yml
vars = open_yaml_vars(vars_file)

# SEG1
print(str(vars['secgws']['seg1']['name']))
output = run_command_file(vars['secgws']['seg1']['mgmtip'], str(vars['secgws']['seg1']['mgmtip'] + ".ssh"), vars["ssh_port"], vars["username"], vars["password"])

# SEG2
print(str(vars['secgws']['seg2']['name']))
output = run_command_file(vars["secgws"]["seg2"]["mgmtip"], str(vars["secgws"]["seg2"]["mgmtip"] + ".ssh"), vars["ssh_port"], vars["username"], vars["password"])
