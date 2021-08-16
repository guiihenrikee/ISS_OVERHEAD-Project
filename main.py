import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 0  # Your latitude
MY_LONG = 0  # Your longitude
MY_EMAIL = "......@gmail.com"  # Your email
PASSWORD = "YOUR PASSWORD"  # Your password


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    # NOTE: All times are in UTC and summer time adjustments are not included in the returned data.
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])-3
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])-3
    # I had to include the -3 at the end because I live in GMT-3 timezone and the API returns UTC timezone.
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg="Subject: ISS ON THE SKY!\n\nRUN OUTSIDE AND LOOK AT THE SKY!")
            connection.close()
