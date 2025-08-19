#!/bin/bash

# Change to the directory containing licenses.json
cd "$(dirname "$0")" || exit

# Check if licenses.json exists
if [ ! -f "../licenses.json" ]; then
    echo "licenses.json not found"
    exit 1
fi

# Run the Python script
python << END
import json

with open('../licenses.json', 'r') as f:
    licenses = json.load(f)


approved_licenses = [
  'Apache Software License',
  'Apache Software License; BSD License',
  'BSD License',
  'GNU Lesser General Public License v2 or later (LGPLv2+)',
  'GNU Lesser General Public License v3 (LGPLv3)',
  'MIT',
  'Mozilla Public License 2.0 (MPL 2.0)',
  'Python Software Foundation License',
  'MIT License',
  'Historical Permission Notice and Disclaimer (HPND)',
  'GNU Library or Lesser General Public License (LGPL)',
  'GNU',
]

for package in licenses:
    if package['License'] not in approved_licenses:
        print(f"License for {package['Name']} is not approved: {package['License']}")
        exit(1)

print("All licenses are compliant")
END