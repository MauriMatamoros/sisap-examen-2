#!/bin/bash
echo "$(cat /var/log/syslog | grep errorBadCommand)"
