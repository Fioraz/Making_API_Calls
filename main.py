import requests
from datetime import datetime
import smtplib
import time

MY_LAT = float(53.480709)
MY_LNG = float(-2.234380)
my_email = "sender_email@gmail.com"
password = "abcdefghijklmn"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")

    # print(response.status_code)    # Check the http status of response: if 1XX - hold on,
    # # 2XX - here you go, 3XX - Go away (no permission), 4XX - You screwed up (not found),
    # # 5XX - I screwed up (server issue)

    response.raise_for_status()     # raise an exception
    all_data = response.json()  # All the data in the dictionary

    iss_longitude = float(all_data["iss_position"]["longitude"])
    iss_latitude = float(all_data["iss_position"]["latitude"])

    if MY_LNG-5 <= iss_longitude <= MY_LNG+5 and MY_LAT-5 <= iss_latitude <= MY_LAT+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="receiver_email@gmail.com",
            msg="Subject: Look Up\n\nThe ISS is above you in the sky.",
        )

