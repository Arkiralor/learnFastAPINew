#!/bin/bash

python -m pip install pip-tools
pip-compile --output-file=dev-requirements.txt dev-requirements.in
python -m pip install -r dev-requirements.txt