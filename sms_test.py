import requests
import urllib.parse

sms_api_key = 'JuNmPITACKGwRikU1sWDcyh9BYaEjfSXz3QgxdnL4t2vOqrVeb5r6JoQF1geNbSPxikl7GvY9UXLIEKy'
phone = "9548543105"

def send_sms(message, phone_number):
    url = 'https://www.fast2sms.com/dev/bulkV2'
    options = {
        'message' : message,
        'language' : 'english',
        'route' : 'q',
        'numbers' : phone_number
    }
    payload = urllib.parse.urlencode(options)
    headers = {
        'authorization' : sms_api_key,
        'Content-type' : 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url = url, data = payload, headers = headers)
    print(response.text)

send_sms("This message is sent using fast2sms api!", phone)
