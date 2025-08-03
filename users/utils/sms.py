import requests
import logging

logger = logging.getLogger(__name__)

def send_verification_code(phone_number, code):
    url = "https://api.sms.ir/v1/send/verify"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
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

    # لاگ امن با جایگزینی کاراکترهای غیرقابل نمایش
    safe_text = response.text.encode('utf-8', errors='replace').decode('utf-8')

    print(f"SMS API status: {response.status_code}")
    print(f"SMS API response body: {safe_text}")

    try:
        logger.info(f"SMS API response: {response.status_code}, body: {safe_text}")
    except Exception as e:
        logger.warning(f"Could not log SMS response due to encoding error: {e}")

    if response.status_code != 200:
        raise Exception(f"Failed to send SMS: {response.status_code} | Response: {safe_text}")
