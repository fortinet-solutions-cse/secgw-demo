# Fortinet SecGW Solution Stack Demo
This is a repo of Ansible playbooks to deploy the whole Fortinet SecGW Solution Stack in Fortinet Fabric Studio.
It can be used to demo automated provisioning of the Fortinet SecGW Solution in a realistic environment, Hands-On-Labs learning or even just as inspirations for Ansible playbooks to configure FortiGates through FortiManager.  
For details refer to the Hands-On-Lab Guide.  

The playbooks are designed to be used in a Fortinet Fabric Studio named "MNO-SecGW-HoL". 
To get access to the Fabric Studio or the Hands-On-Lab Guide contact your local Fortinet SE or Telco SME.


# How to use demo mode
The demo mode will pre-configure FMG / FAZ / FGT-SEG-1 and FGT-SEG-2 so you quickly can spin up the whole lab. It can be useful as customer demos, self-paced learning, verification of a feature or troubleshooting.

1. Start the Fabric "MNO-SecGW-HoL"
1. When the Fabric is started. Log into the LXC device named Runner.
1. Start the playbook with

        cd /fabric/ansible
        ansible-playbook hol.yml

    This will configure all Fortinet equipment.
1. When playbooks have finished check there are no failed plays.
1. If it is all super green, then log into gNodeB1 and bring up the tunnel

        cd /fortipoc
        ./genrsa
        ./ir
        ./config_ss.sh
        ping 10.30.2.2 -i0.2

    Notice: You don't need to manually bring up the tunnel. Linux routing policies will detect a match to the child-SA and bring up the tunnel.
1. Repeat the same procedure for gNodeB2.
1. You now have a fully functioning SecGW solution with traffic running.

# Password to devices
Device password in set in Fabric studio. Remember to create a `.env` file in the `scripts` directory with the following content:  
DEVICE_PASSWORD='your_password_here'

# Variables
Variables can be found in `group_vars`. This directory contains all variables required to provision the Fabric.  
Notices that some variables are initialized during the first task (init) and it creates a number of variables that are store in the ansible fact database. These variables are:

- password
- fmg_access_token
- fmg_sn
- faz_access_token
- faz_sn
- secgws.seg1.sn
- secgws.seg2.sn


# Component versions
The demo has been verified with the following versions:
- Fabric Studio v.2.0.4
- FortiManager v.7.6.4
- FortiAnalyzer v.7.6.4
- FortiGate v.7.4.9
- FortiAuthenticator v.6.6.7

Enjoy:)
