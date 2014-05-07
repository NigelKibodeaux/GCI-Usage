import mechanize
import urllib
import re
import datetime
import argparse

parser = argparse.ArgumentParser(description='Writes your GCI usage into a file called gci_usage.html')
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
percentage_of_data_used = re.search('data-percent="([^"]+)"', page_text).groups()[0]
percentage_of_data_used = float(percentage_of_data_used)
billing_period = re.search('Bill Period.*?<dd class="data">([^<]+)<span', page_text, flags=re.MULTILINE|re.DOTALL).groups()[0]

start, end = billing_period.split(' - ')
start = datetime.datetime.strptime(start, '%m/%d')
end = datetime.datetime.strptime(end, '%m/%d')
days_in_billing_period = (end - start).days

raw_updated_date = re.search('\(as of ([^)]+)\)', page_text).groups()[0]
updated_date = datetime.datetime.strptime(raw_updated_date, '%m/%d')

days_used = (updated_date - start).days
percentage_of_month_over = (1.0 * days_used) / days_in_billing_period


output = template.format(
	percentage_of_data_used * 100, 
	percentage_of_month_over * 100, 
	raw_updated_date)

output_file = open('gci_usage.html', 'w')
output_file.write(output)
output_file.close()
