#!/bin/bash
echo "[Issabel]" >/etc/prosody/sharedgroups.txt
sqlite3 /var/www/db/acl.db "select name || '@issabel' from acl_user" >>/etc/prosody/sharedgroups.txt
chgrp prosody /etc/prosody/sharedgroups.txt
/etc/prosody/runprosodycmd 'module:reload("roster","issabel")'
/etc/prosody/runprosodycmd 'module:reload("groups","issabel")'
