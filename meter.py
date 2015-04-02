import mechanize
import urllib
import re
import datetime
import argparse

parser = argparse.ArgumentParser(description='Grabs your usage data from GCI')
parser.add_argument('--html', help='output the data in html to the current dir', action="store_true")
parser.add_argument('--json', help='output the data in JSON format', action="store_true")
parser.add_argument('username', help='username')
parser.add_argument('password', help='password')
args = parser.parse_args()

# output numbers
data_left_per_day = None
percentage_of_month_over = None
percentage_of_data_used = None

# intermediate numbers
updated_date = None
days_in_billing_period = None

# html template
template = """
<html>
	<head>
		<style>
			#data {{
				width: {}%;
			}}
			#month {{
				width: {}%;
			}}
			.container {{
				border: 1px solid black;
				padding: 3px;
				margin-bottom: 20px;
			}}
			.container div {{
				height: 20px;
				background-color: gray;
			}}
		</style>
		<link rel="shortcut icon" href="http://www.gci.com/content/themes/GCI2013/library/favicon.ico">
	</head>
	<body>
		Data Used
		<div class="container">
			<div id="data"></div>
		</div>

		Month Passed
		<div class="container">
			<div id="month"></div>
		</div>

		Updated: {}
	</body>
</html>
"""

# write stuff to the console
def print_percentage(p, message):
	output = '['
	for i in range(1, 50):
		if (i <= p*100/2):
			output += '='
		else:
			output += ' '
	output += ']' + ' ' + message
	print output


b = mechanize.Browser()

url = 'https://login.gci.com/'
parameters = {
	'username': args.username,
	'password': args.password,
	'submit': 'Log In'
}

# request meter page, get login page
page_text = b.open('https://apps.gci.com/um/overview').read()
csrf_token = re.search('name="_csrf" value="([^"]+)"', page_text).groups()[0]
parameters['_csrf'] = csrf_token

page_text = b.open(url, urllib.urlencode(parameters)).read()
#print page_text

total_available = re.search('data-cap="([^"]+)"', page_text).groups()[0]
total_used = re.search('data-total="([^"]+)"', page_text).groups()[0]

percentage_of_data_used = float(total_used) / float(total_available)
billing_period = re.search('Bill Period.*?<dd class="data">([^<]+)<span', page_text, flags=re.MULTILINE|re.DOTALL).groups()[0]

start, end = billing_period.split(' - ')
start = datetime.datetime.strptime(start, '%m/%d')
end = datetime.datetime.strptime(end, '%m/%d')
days_in_billing_period = (end - start).days

page_text = b.open('https://apps.gci.com/um/service/cc:a4:62:67:e9:13').read()
raw_updated_date = re.search('\(as of ([^)]+)\)', page_text).groups()[0]
updated_date = datetime.datetime.strptime(raw_updated_date, '%m/%d')

days_used = (updated_date - start).days
percentage_of_month_over = (1.0 * days_used) / days_in_billing_period

if (args.html):
	output = template.format(
		percentage_of_data_used * 100,
		percentage_of_month_over * 100,
		raw_updated_date)

	output_file = open('gci_usage.html', 'w')
	output_file.write(output)
	output_file.close()

# output stuff to the console
if (args.json):
	out = '{datetime: "' + str(datetime.datetime.now()) + '", '
	out += 'month_over:' + str(percentage_of_month_over*100) + ', '
	out += 'data_used:' + str(percentage_of_data_used*100) + '}'
	print out
else:
	print_percentage(percentage_of_month_over, str(percentage_of_month_over*100) + '% of month over')
	print_percentage(percentage_of_data_used, str(percentage_of_data_used*100) + '% of data used')
