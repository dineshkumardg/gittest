#!/bin/bash

/bin/mv "/var/log/rsync/rsync-$(date +%w).log" "/var/log/rsync/rsync-$(date +%w).log.old"

/usr/local/bin/rsync-3.1.0/rsync -ah --delete-delay --progress --log-file="/var/log/rsync/rsync-$(date +%w).log" --exclude 'lost+found' /GAIA/ /GAIA_MIRROR/

/bin/mail -s "ukandgaia07: rsync-$(date +%w).log" james.sears@cengage.com < /var/log/rsync/rsync-$(date +%w).log
/bin/mail -s "ukandgaia07: rsync-$(date +%w).log" emea.serverteamalert@corproot.local < /var/log/rsync/rsync-$(date +%w).log
