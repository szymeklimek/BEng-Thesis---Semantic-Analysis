#!/bin/sh
cd public_mm
sh bin/install.sh
sh bin/skrmedpostctl start
cd ..
rm setup.sh
python mm_server.py