#C:\Users\mwhitenett\Documents\Security\Scripts\Message.txt

#============================================= File Functionality =====================================================
from string import Template

#Function to pull names and email addresses from a file.
def get_respondents(filename):                                           #contacts_file will be defined in the main method
    names = []
    emails = []
    vendors = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:    #open the file, and reach each line.
        for a_contact in contacts_file:                                  #split each line(contact) into a name and email.
            names.append(a_contact.split(',')[0])
            emails.append(a_contact.split(',')[1])
            vendors.append("\n- ".join(a_contact.split(',')[2].split('|')))

    return names, emails, vendors                                                 #return three lists

#Function to create a template object of the email that needs to be sent out. It reads this template from a txt file
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()                     #Adds the contents of the template file to an object, which is then returned.
    return Template(template_file_content)


#============================================= Email Functionality =====================================================
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

#----- Authentication Method -----
MY_ADDRESS = input("What is your email?")
type(MY_ADDRESS)

#Password Input
PASSWORD=input("What is your password?")
type(PASSWORD)
def getPass(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()                     #Adds the contents of the template file to an object, which is then returned.
    return Template(template_file_content)

def main():
    #File Fetches
    names, emails, vendors = get_respondents('C:/Users/mwhitenett/Documents/Security/Scripts/mycontacts.txt')
    message_template = read_template('C:/Users/mwhitenett/Documents/Security/Scripts/message.txt')

    #Variables:
    cc_email = "email@companyname.com"

    # Setup the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email separately                                #For each name, email, and vendor name create a message as a MIMEMultipart object.
    for name, email, vendor in zip(names, emails, vendors):
        msg = MIMEMultipart()

        # Add in the actual persons name and vendor name to the message template
        message = message_template.substitute(PERSON_NAME=name.title(), VENDOR_NAME=vendor.title())

        # Prints out the message body for QA
        print(message)

        # Setup the message parameters
        msg['From'] = MY_ADDRESS  # This may change to a default company/customer email.
        msg['To'] = email
        msg['CC'] = cc_email
        msg['Subject'] = "Third Party Risk Governance Annual Vendor Review - " + vendor.split("\n")[0]

        # Add in the message body
        msg.attach(MIMEText(message))

        #Send emails 20 seconds apart to avoid SPAM filters
        time.sleep(5)

        # Send the message via the server set up earlier
        server.send_message(msg)

        del msg  # Delete the object as you iterate through the loop.

if __name__ == '__main__':
    main()
