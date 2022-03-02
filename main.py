import requests
from datetime import datetime
import smtplib
import time

MY_LAT =28.698997
MY_LON =77.138420
EMAIL = "shootygun20@gmail.com"
PASSWORD = "shootygun120"

def is_iss_overhead():
        response= requests.get(url="http://api.open-notify.org/iss-now.json") #will help us get data from the endpoint
        response.raise_for_status()
        # print(response.status_code) #prints response code which tells us if our requests was successful like 404 does not exist

        iss_longitude = float(response.json()["iss_position"]["longitude"])
        iss_latitude = float(response.json()["iss_position"]["latitude"])

        if MY_LAT-5<= iss_latitude <=MY_LAT+7 and MY_LON-5 <= iss_longitude <=MY_LON+5:
            return True

def is_night():
        parameters= {
            "lat": MY_LAT,
            "long": MY_LON,
            "formatted": 0
        }
        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()

        data = response.json()
        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
        #Split converts the sunrise time to a list and we get the hour
        time_now= datetime.now()
        hour_time=time_now.hour
        if hour_time >sunset and hour_time < sunrise-2:
            return True

while True:
    time.sleep(80)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp@gmail.com")
        connection.starttls() #The starttls puts the connection to the SMTP server into TLS mode.
        # Transport Layer Security (TLS) encrypts data sent over the Internet
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject:Now Look Up\n\n The ISS is above you in the sky")
