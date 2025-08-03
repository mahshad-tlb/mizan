import requests
import logging

logger = logging.getLogger(__name__)

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
                "name": "CODE",  # مطابق قالب پنل SMS.ir
                "value": code
            }
        ]
    }

    response = requests.post(url, json=json_data, headers=headers)

    # چاپ کامل وضعیت و متن پاسخ سرور (برای دیباگ)
    print("SMS API status:", response.status_code)
    print("SMS API response body (raw):", repr(response.text))

    try:
        # تلاش برای لاگ کردن پیام بدون ایجاد خطای یونیکد
        safe_text = response.text.encode('ascii', errors='ignore').decode('ascii')
        logger.info(f"SMS API response: {response.status_code}, body: {safe_text}")
    except Exception as e:
        logger.warning(f"Could not log SMS response text due to encoding: {e}")

    if response.status_code != 200:
        # ارور با پیام کامل پاسخ سرور
        raise Exception(f"Failed to send SMS: {response.status_code} | Response: {response.text}")
