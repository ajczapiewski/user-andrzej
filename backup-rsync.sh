#!/bin/bash
rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" root@cytora.org:/usr/lib/cytora/backups /usr/lib/cytora

