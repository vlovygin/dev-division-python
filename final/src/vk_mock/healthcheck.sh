#!/usr/bin/env bash

#set -ex


# Вывод в лог о неуспешном хелзчеке, но если он успешный, то ничего не делать (exit code 0)
echo -e "Test" > "testfile"
netstat -ant | grep 5000 | grep -w LISTEN
