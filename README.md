GCI-Usage
=========
####No longer maintained. Switched to the node version here: https://github.com/NigelKibodeaux/gci-data-display


Scrapes gci.com to get your internet usage from the command line. Displays the percentage of the current month that has passed as well as the percentage of data you've used.

It will output your usage on the command line and optionally generate an HTML display of it.

```
usage: meter.py [-h] [--html] username password

Grabs your usage data from GCI

positional arguments:
  username    username
  password    password

optional arguments:
  -h, --help  show this help message and exit
  --html      output the data in html to the current dir
  ```
