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
        _yaml_data = yaml.safe_load(file)
    return _yaml_data

def run_command_file(host, command_file, ssh_port, username, password):
    _client = paramiko.SSHClient()
    _client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _client.connect(host, ssh_port, username, password)
    _output = ""
    _allowed_to_exec = True

    # read file
    commands = read_command_from_file(command_file)

    #sanitize input
    disallowed_commands = ["factoryreset", "factoryreset2", "shutdown", "reboot", "delete", "purge", "set"]
    commands_split = commands.split('\n')

    # Check if the command is in the disallowed commands list
    for cmd in commands_split:
       cmd = cmd.strip()
       if any(dcmd in cmd for dcmd in disallowed_commands):
         print(f"command file '{command_file}' contains the disallowed command '{cmd}'. Commands are not run.")
         _allowed_to_exec = False

    # send command to _client
    if _allowed_to_exec:
        _stdin, _stdout, _stderr = _client.exec_command(commands)
        _output = _stdout.read().decode()
        del _stdin, _stdout, _stderr

    _client.close()

    return _output


# read vars.yml
vars = open_yaml_vars(vars_file)

# SEG1
print(str(vars['secgws']['seg1']['name']))
output = run_command_file(vars['secgws']['seg1']['mgmtip'], str(vars['secgws']['seg1']['mgmtip'] + ".ssh"), vars["ssh_port"], vars["username"], vars["password"])

# SEG2
print(str(vars['secgws']['seg2']['name']))
output = run_command_file(vars["secgws"]["seg2"]["mgmtip"], str(vars["secgws"]["seg2"]["mgmtip"] + ".ssh"), vars["ssh_port"], vars["username"], vars["password"])
