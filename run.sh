#!/bin/sh

pm2 kill
pm2 start pm2.json
pm2 logs