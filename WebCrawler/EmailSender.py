import smtplib, ssl



class EmailSender():

    Port = 465  # For SSL
    MessageTemplate = "Subject: {0}\n\n{1} . Element text = {2} ."

    def __init__(self):
        self.Address =  #Add your email address here
        self.Password = #Add your account password. For Gmail, you need to turn on "Less secure app access"

    def SendEmail(self, title, url, elementText):
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.Port, context=context) as server:
            server.login(self.Address, self.Password)
            server.sendmail(self.Address, self.Address, self.MessageTemplate.format(title, url, elementText))