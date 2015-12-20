#!/bin/bash

cd $(dirname $0)
./bin/supervisord -n -c supervisord.conf
