import requests

def send_verification_code(phone_number, code):
    url = "https://api.sms.ir/v1/send/verify"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": "C3NkMwIelbIIBEx9CuiS9GJ5SU8HUsCB0crHaFApHuw0sDay"
    }
    json_data = {
        "mobile": phone_number,
        "templateId": 231572,
        "parameters": [
            {
                "name": "CODE",
                "value": code
            }
        ]
    }

    response = requests.post(url, json=json_data, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to send SMS: {response.status_code} | Response: {response.text}")
