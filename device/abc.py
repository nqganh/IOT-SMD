import requests
import json


api_token = '337bdd5a-2ee8-415b-a432-4460c725f1b4'
api_url_base = 'https://leadsync.optionwide.com/lead/phone-lookup?access_token=337bdd5a-2ee8-415b-a432-4460c725f1b4&phone=3109201362'
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}

# Replace with the correct URL
url = "https://leadsync.optionwide.com/lead/phone-lookup?access_token=337bdd5a-2ee8-415b-a432-4460c725f1b4&phone=3109201362"

def get_account_info():

    api_url = format(api_url_base)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

account_info = get_account_info()
print account_info

if account_info is not None:
    print("Here's your info: ")
    for k in account_info['extension']:
        print('{0}'.format(k))

else:
    print('[!] Request Failed')
# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
#print (myResponse.status_code)

# For successful API call, response code will be 200 (OK)
