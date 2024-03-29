random-snippets
===============

random snippets of code

I should really commit more.

All code is in this repo is covered by LICENSE, unless otherwise stated in the file

## snmp_oid_collect.sh

This script does a bulkwalk of a snmp table

and turns the output into a key-value pair, suitable for ingestion into Splunk

## split_json.sh

Converts ${INPUT} into single line objects,

then splits on a given size.   Then uses --filter to

place each split back into an array an outputs to 

given filename


## json_xml_parse.py

Takes a json file with string that has XML in it and rewrites it as json

```
usage: json_xml_parse.py [-h] [-i INPUT_FILE] [-f JSON_FIELD] [-o OUTPUT_FILE]

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
  -f JSON_FIELD, --json_field JSON_FIELD
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
```

### input.json

```
[{
  "id": 1,
  "first_name": "Jeanette",
  "last_name": "Penddreth",
  "email": "jpenddreth0@census.gov",
  "gender": "Female",
  "ip_address": "26.58.193.2",
  "xmldata": "<catalog>\n      <book id=\"bk112\">\n      <author>Galos, Mike</author>\n      <title>Visual Studio 7: A Comprehensive Guide</title>\n      <genre>Computer</genre>\n      <price>49.95</price>\n      <publish_date>2001-04-16</publish_date>\n      <description>Microsoft Visual Studio 7 is explored in depth,\n      looking at how Visual Basic, Visual C++, C#, and ASP+ are \n      integrated into a comprehensive development \n      environment.</description>\n   </book>\n</catalog>" 
}]
```

### output.json

```

[
  {
    "id": 1,
    "first_name": "Jeanette",
    "last_name": "Penddreth",
    "email": "jpenddreth0@census.gov",
    "gender": "Female",
    "ip_address": "26.58.193.2",
    "xmldata": {
      "catalog": {
        "book": {
          "@id": "bk112",
          "author": "Galos, Mike",
          "title": "Visual Studio 7: A Comprehensive Guide",
          "genre": "Computer",
          "price": "49.95",
          "publish_date": "2001-04-16",
          "description": "Microsoft Visual Studio 7 is explored in depth,\n      looking at how Visual Basic, Visual C++, C#, and ASP+ are \n      integrated into a comprehensive development \n      environment."
        }
      }
    }
  }
]
```

## syslog_json_splunk_format.py 

This is a ansible callback 

- This plugin logs ansible-playbook and ansible runs to a syslog server in JSON format suitable for Splunk

- This plugin has been adapted from the the syslog_json plugin - https://github.com/ansible-collections/community.general/blob/main/plugins/callback/syslog_json.py

- The syslog msg information has been adjusted to be key=value pairs

- The task name has been added to the logged information

### example output

```
2024-03-19 23:30:42,055 p=1179951 u=nak n=ansible logger | self_hostname="gistrate" ansible-command="task" execution="OK" hostname="test5" task="show the groups the host(s) are in" message="{
    "changed": false,
    "msg": [
        "group2"
    ]
}"
```
