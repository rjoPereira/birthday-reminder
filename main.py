import smtplib
import datetime
from time import sleep

import pandas as pd


def smtp_setup(email_provider):
    providers = {
        "gmail": "smtp.gmail.com",
        "yahoo": "smtp.mail.yahoo.com",
        "live": "smtp.live.com"
    }
    return providers.get(email_provider, "No email provider with that name...")


def main():
    dates_df = pd.read_csv("dates.csv")
    email = ""
    email_to_send = ""
    password = ""
    email_provider = ""

    while email == "" or email_to_send == "" or password == "" or email_provider == "":
        email = input("Insert your email: ")
        email_to_send = input("Insert the email which will receive the emails: ")
        password = input("Insert your email password: ")
        email_provider = input("insert your email provider: ")
    try:
        host = smtp_setup(email_provider)
        email_sender = smtplib.SMTP(host)
        email_sender.starttls()
        email_sender.login(user=email, password=password)
    except UnicodeError:
        print("Incorrect data given. Quitting...")
    except smtplib.SMTPAuthenticationError:
        print("Enable the option 'Access to less secure apps'")
    else:
        while True:
            today_date = datetime.date.today()
            month = today_date.month
            day = today_date.day
            for f in range(0, len(dates_df.index)):
                birthday = str(dates_df["Dates"][f]).split("-")
                month_df = int(birthday[0])
                day_df = int(birthday[1])
                if month == month_df and day == day_df:
                    file = open("reminder.txt", "r")
                    message = file.read()
                    file.close()
                    message = message.replace("[x]", dates_df["Names"][f])
                    email_sender.sendmail(from_addr=email, to_addrs=email_to_send, msg="Subject:Birthday Reminder\n\n"
                                                                                       + message)
                    print("Email sent.")
            sleep(86400)


if __name__ == "__main__":
    main()
