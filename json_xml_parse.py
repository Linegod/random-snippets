#!/usr/bin/python
# json with embedded XML conversion
# J.P. Pasnak, CD
# 09/01/2024

import sys
import json
import xmltodict
import argparse
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import warnings
warnings.simplefilter("ignore")

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i","--input_file", help="Input File")
parser.add_argument("-f","--json_field", help="JSON field that contains XML")
parser.add_argument("-o","--output_file", help="Output File")
args = parser.parse_args()

# Set args
input_file = args.input_file
output_file = args.output_file
json_field = args.json_field

# Read the JSON file
with open(input_file, 'r') as file:
    data = json.load(file)

# Iterate through the list of items
for item in data:
    # Extract the field containing XML from each item
    xml_data = item[json_field]

    # Convert XML to JSON, strip out newlines
    json_data = json.dumps(xmltodict.parse(xml_data), indent=2).replace("\n", "")

    # Update the original item with the new JSON data
    item[json_field] = json.loads(json_data)

# Write the updated JSON to a new file
with open(output_file, 'w') as updated_file:
    json.dump(data, updated_file, indent=2)
