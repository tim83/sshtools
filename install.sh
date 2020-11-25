#! /bin/bash

path=$(dirname $0)
cd $path
./setup.py build && ./setup.py install --user
