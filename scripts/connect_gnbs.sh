#!/bin/bash

# Define the hosts and credentials
HOSTS=("10.254.1.1" "10.254.1.2")
USER="root"
PASSWORD="$DEVICE_PASSWORD"

# Command sequence to execute on the remote hosts
COMMANDS="source /etc/profile; cd /fabric; ./genrsa; ./ir; ./config_ss.sh; swanctl --initiate --child secgw"

# Iterate over each host and execute the commands, capturing the output
for HOST in "${HOSTS[@]}"; do
    echo "Executing commands on $HOST"
    sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$HOST" "$COMMANDS" 2>&1 | while IFS= read -r line; do
        echo "[$HOST] $line"
    done
done
#!/bin/bash

