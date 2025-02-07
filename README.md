# SecGW Demo
This is a repo of Ansible playbooks to deploy Fortinet SecGWs in FortiPoC.
It can be used to demo automated provisioning of the Fortinet SecGW Solution in a realistic environment, Hands-On-Labs learning or even just as inspirations for Ansible playbooks to configure FortiGates through FortiManager.  
For details refer to the Hands-On-Lab Guide.  

The playbooks are designed to be used in a FortiPoC named "MNO-SecGW-HoL.fpoc". 
To get access to the FortiPoC or the Hands-On-Lab Guide contact your local Fortinet SE or Telco SME.

# How to use demo mode
The demo mode will pre-configure FMG / FAZ / FGT-SEG-1 and FGT-SEG-2 so you quickly can spin up the whole lab. It can be useful as customer demos, self-paced learning, verification of a feature or troubleshooting.

1. Start the poc "MNO SecGW HoL"
1. When the PoC is started. Log into the LXC device named Runner.
1. Initialize the Ansible playbooks with

        cd /fortipoc/init
        ./init.py

1. Start the demo playbook with

        cd /fortipoc/ansible
        ansible-playbook demo.yml

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


# Vars
The file `vars/global.yml` contains all variables required to provision the FortiPoC.  
The `init.py` script mentioned above sets the following variables in `vars/global.yml`

- password
- fmg_access_token
- fmg_sn
- faz_access_token
- faz_sn
- secgws[seg1][sn]
- secgws[seg2][sn]


# Prerequisites
- FortiPoC v.1.9.8  
- FortiManager v.7.2.7 or higher on the 7.2 release train  
- FortiAnalyzer v.7.2.7 or higher on the 7.2 release train  
- FortiGate v.7.2.10 or higher on the 7.2 release train  
- FortiAuthenticator v.6.6.2 or higher on the 6.6 release train  

Enjoy:)