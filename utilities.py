from exchangelib import DELEGATE, Account, Credentials, EWSDateTime
from exchangelib import Configuration
from exchangelib import Message, Mailbox, FileAttachment
from exchangelib.folders import Calendar, Root
from exchangelib import CalendarItem, UTC_NOW
from datetime import timedelta
from exchangelib import EWSDateTime, FolderCollection, Q, Message
import datetime
import calendar as cal
import os
import locale
import re
from threading import Timer
import datetime
import config
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')


class Email:
    account = None

    def __init__(self, account):
        self.account = account

    def send_email(self, subject, body, recipients, files=None):
        """
        Send an email.
        Parameters
        ----------
        account : Account object
        subject : str
        body : str
        recipients : list of str
            Each str is and email adress
        attachments : list of tuples or None
            (filename, binary contents)
        Examples
        --------
        >>> send_email(account, 'Subject line', 'Hello!', ['info@example.com'])
        """
        to_recipients = []
        for recipient in recipients:
            to_recipients.append(Mailbox(email_address=recipient))
        # Create message
        m = Message(account=self.account,
                    folder=self.account.sent,
                    subject=subject,
                    body=body,
                    to_recipients=to_recipients)

        attachments = []
        for path, name in files:
            with open(path, 'rb') as f:
                content = f.read()
            attachments.append((name, content))

        # attach files
        for attachment_name, attachment_content in attachments or []:
            file = FileAttachment(name=attachment_name,
                                  content=attachment_content)
            m.attach(file)
        m.send_and_save()


class Appointment:
    def __init__(self, subject, body, start, end, location, duration, calendar_name):
        self.subject = subject
        self.body = body
        self.start = start
        self.end = end
        self.location = location
        self.calendar_name = calendar_name
        hasHours = duration.find("H") != -1
        hasMinutes = duration.find("M") != -1
        duration = duration[2:]
        hour = duration.find("H")
        minute = duration.find("M")

        if duration == "D":
            # is day long event
            self.duration = 24
        else:
            if hasHours:
                if hasMinutes:
                    self.duration = int(
                        duration[:hour])+int(duration[hour+1:minute])/60
                else:
                    self.duration = float(duration[:hour])
            else:
                self.duration = int(duration[:minute])/60
        self.fancyDate()

    def __str__(self):
        return str(self.subject)+", "+str(self.body)+str(self.start)+", "+str(self.end)+", "+str(self.duration)+", "+str(self.location)

    def fancyTime(self):
        return self.parseTime(self.start)+" Uhr - " + self.parseTime(self.end)+" Uhr"

    def fancyDate(self):
        startString = str(self.start)
        if " " in startString:
            space = startString.find(" ")+1
            tempDate = startString[:space]
            tempDate = tempDate.strip()
        else:
            tempDate = startString
        realDate = datetime.datetime.strptime(tempDate, '%Y-%m-%d')

        return realDate.strftime("%A %d. %B %Y")

    def parseTime(self, datetime):
        datetime = str(datetime)
        space = datetime.find(" ")+1
        plus = datetime.find("+")-3
        return datetime[space:plus]


class Calendar_Manager:
    account = None

    def __init__(self, account):
        self.account = account

    def get_Appointments(self, include_day_long=False):

        x = EWSDateTime.today()

        start = self.account.default_timezone.localize(x)

        x = EWSDateTime.today()
        end_date = x + datetime.timedelta(days=10)

        end = self.account.default_timezone.localize(end_date)

        output = []

        summertimeOffset = 1

        if not config.summertime:
            summertimeOffset += 1

        dstOffset = datetime.timedelta(hours=summertimeOffset)

        cals = [self.account.calendar]
        for cal_folder in self.account.calendar.children:
            if "Calendar" in str(cal_folder):
                cals.append(cal_folder)

        for cal in cals:
            calendar_name = str(cal)
            calendar_name = calendar_name[calendar_name.find(" ")+2:-1]

            view = cal.view(start=start, end=end)

            for appointment in view:

                subject = appointment.subject
                body = appointment.text_body
                startAp = appointment.start+dstOffset
                endAp = appointment.end+dstOffset
                location = appointment.location
                duration = appointment.duration
                if include_day_long or (" " in str(appointment.start)):
                    output.append(Appointment(
                        subject, body, startAp, endAp, location, duration, calendar_name))

        '''
        for a in output:
            print(a.subject, a.calendar_name)
        '''
        return output


class Routine:
    def __init__(self):
        return

    def startToday(self, function):
        x = datetime.datetime.today()
        y = x.replace(day=x.day, hour=18, minute=0, second=0, microsecond=0)
        delta_t = y-x

        secs = delta_t.total_seconds()
        if secs > 0:
            t = Timer(secs, function)
            t.start()

    def start(self, function):

        x = datetime.datetime.today()
        y = x.replace(day=x.day, hour=18, minute=0, second=0,
                      microsecond=0) + timedelta(days=1)
        delta_t = y-x

        secs = delta_t.total_seconds()

        t = Timer(secs, function)
        t.start()
