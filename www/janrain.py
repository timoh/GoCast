'''
login module
Sign up and log in system
'''
import requests
import simplejson as json
from urllib import urlencode


app_domain = "https://4cash.rpxnow.com/"
app_id = "cfcemoakonilkpmhlkmj"
app_key = "900e0ad014cb7ebe5713c71830c62b2ff1c03911"
url = "https://rpxnow.com/api/v2/auth_info"

def authenticate(token):
	'''
	does user authentification against JanRain service
	Returns:
		* dictionary with user info or just None
	'''
	result  = None

	api_params = {
		'token': token,
    	'apiKey': app_key,
    	'format': 'json',
	}
	response = requests.post(url, api_params)
	if response.ok:
		result = json.loads(response.content)
		print result

	return result['profile']


