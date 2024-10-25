import utils

def sendMail():
    print("Sending mail")
    with open('text.txt') as f:
        
        lines = f.readlines()
        
        for line in lines:
            data = line.split()
            email = data[0]
            name = ' '.join(data[1:])
            body = f"Hello {name},\n\nThis is a test email.\n\nThanks,\n\nAdmin"

            print(f"Email sent to {name} at {email}")

            # utils.sendEmail("Test Email", body, email)

            # print(f"Email sent to {name} at {email}")


sendMail()