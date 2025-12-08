#!/usr/bin/python3

import paramiko
import json
import re
import os
import sys
from dotenv import load_dotenv


script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)
commandfile_path = os.path.join(script_dir, "commands/")


# --- HELPER FUNCTIONS ---
def read_command_from_file(file_path):
    with open(file_path, 'r') as file:
        _command = file.read().strip()
    return _command

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

def get_token(command_output):
    ## Split the string based on "key:"
    split_result = command_output.split("key:")

    ## Check if the split was successful (the output contains "key:")
    if len(split_result) <= 1:
        print("No API key found in the output.", file=sys.stderr)
        exit(-1)

    api_key = split_result[1].strip()

    ## check if there is new line char in api_key if so, remove it
    if "\n" in api_key:
        split_result = api_key.split("\n")

        api_key = split_result[0].strip()

    return api_key

def get_serial_number(command_output):
    """
    Extracts the serial number from command output using a flexible regex pattern.
    This version correctly handles formats like 'Serial Number : ...'
    """
    # This corrected pattern looks for:
    # - "Serial Number" (with a space), "Serial-Number", or "SN"
    # - Followed by an optional colon and whitespace
    # - And captures the alphanumeric string that follows (the serial number)
    pattern = re.compile(r"(?:Serial[\s-]?Number|SN)\s*:\s*(\w+)", re.IGNORECASE)

    match = pattern.search(command_output)

    if match:
        # The serial number is in the first captured group
        serial_number = match.group(1).strip()
        return serial_number
    else:
        # If no match is found, print an error and the output for debugging
        print("ERROR: Could not find a serial number.", file=sys.stderr)
        print("------- Full Device Output -------", file=sys.stderr)
        print(command_output, file=sys.stderr)
        print("------------------------------------", file=sys.stderr)
        exit(-1)

def build_results_dict(fmg_data, faz_data, seg1_sn, seg2_sn, password):
    """Assembles all gathered data into a single dictionary."""
    return {
        "FMG_ACCESS_TOKEN": fmg_data.get('access_token', ''),
        "FMG_SN": fmg_data.get('sn', ''),
        "FAZ_ACCESS_TOKEN": faz_data.get('access_token', ''),
        "FAZ_SN": faz_data.get('sn', ''),
        "SEG1_SN": seg1_sn,
        "SEG2_SN": seg2_sn,
        "DEVICE_PASSWORD": password
    }

# --- MAIN LOGIC ---
def main():
    # Read the JSON data object from standard input
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from stdin.", file=sys.stderr)
        sys.exit(1)

    password = os.getenv("DEVICE_PASSWORD")
    if not password:
        print("Error: DEVICE_PASSWORD not found in .env file or environment variables.", file=sys.stderr)
        sys.exit(1)

    # Use the data passed from Ansible
    fmg_host = data['fmg_host']
    faz_host = data['faz_host']
    seg1_ip = data['seg1_ip']
    seg2_ip = data['seg2_ip']
    ssh_port = data['ssh_port']
    username = data['username']

    # Create empty dicts to store the results
    fmg_results = {}
    faz_results = {}

    # FMG
    print("FortiManager", file=sys.stderr)
    output = run_command_file(fmg_host, os.path.join(commandfile_path, f"{fmg_host}.ssh"), ssh_port, username, password)
    fmg_results["access_token"] = get_token(output)
    fmg_results["sn"] = get_serial_number(output)

    # FAZ
    print("FortiAnalyzer", file=sys.stderr)
    output = run_command_file(faz_host, os.path.join(commandfile_path, f"{faz_host}.ssh"), ssh_port, username, password)
    faz_results["access_token"] = get_token(output)
    faz_results["sn"] = get_serial_number(output)

    # SEG1
    print("FGT-SEG-1", file=sys.stderr)
    output = run_command_file(seg1_ip, os.path.join(commandfile_path, f"{seg1_ip}.ssh"), ssh_port, username, password)
    seg1_sn = get_serial_number(output)

    # SEG2
    print("FGT-SEG-2", file=sys.stderr)
    output = run_command_file(seg2_ip, os.path.join(commandfile_path, f"{seg2_ip}.ssh"), ssh_port, username, password)
    seg2_sn = get_serial_number(output)

    # REFACTOR: Build the results dictionary and print it as a JSON string to stdout.
    # All human-readable output should go to stderr.
    final_results = build_results_dict(fmg_results, faz_results, seg1_sn, seg2_sn, password)
    print(json.dumps(final_results))


if __name__ == "__main__":
    main()