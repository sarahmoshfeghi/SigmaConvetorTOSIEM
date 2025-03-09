import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename

def send_mail(to_addr, cc_addr, subject):
    try:
        # Check if the attachment file is empty
        attachment_file = "/pathtothesplrulefile/splrule.zip"
        with open(attachment_file, 'rb') as f:
            if len(f.read()) == 0:
                print(f"The file {attachment_file} is empty.")
                return
    except Exception as e:
        print(f"Error reading {attachment_file}: {e}")
        return

    fromaddr = 'senderemail'
    toaddrs = to_addr.split(",")
    ccaddrs = cc_addr.split(",")

    msg = MIMEMultipart('alternative')
    msg['From'] = fromaddr
    msg['To'] = to_addr
    msg['Cc'] = cc_addr
    msg['Subject'] = subject

    # Email body
    text = 'SigmaRule'
    html = """\
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { direction: rtl; }
            h3, p { font-family: "SG Kara Light"; }
            .vuln { direction: ltr; }
        </style>
    </head>
    <body>
        <p class="vuln">https://github.com/SigmaHQ/sigma</br>
    </body>
    </html>
    """

    # Attach both plain text and HTML versions
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Attach the zip file
    zip_file = "/pathtothesplrulefile/splrule.zip"
    try:
        with open(zip_file, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(zip_file))
            part['Content-Disposition'] = f'attachment; filename="{basename(zip_file)}"'
            msg.attach(part)
    except Exception as e:
        print(f"Failed to attach the file: {e}")
        return

    # Send the email
    try:
        server = smtplib.SMTP('mailserver', 25)
        server.starttls()
        server.sendmail(fromaddr, toaddrs + ccaddrs, msg.as_string())
        server.quit()
        print(f"Email sent to {to_addr} with {zip_file} attached.")
    except Exception as e:
        print(f"Failed to send email: {e}")

