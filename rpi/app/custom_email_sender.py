import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

class EmailSender:
  def __init__(self, sender_email, sender_password, recipient_email):
    self.sender_email = sender_email
    self.sender_password = sender_password
    self.recipient_email = recipient_email

  def send_email(self, subject, message_body, image_path):
    smtp_server = 'smtp.mail.yahoo.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = self.sender_email
    msg['To'] = self.recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message_body, 'plain'))

    with open(image_path, "rb") as image_file:
      attachment = image_file.read()

    filename = os.path.basename(image_path)

    image = MIMEImage(img, name=filename)
    image.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
    image.add_header('Content-ID', '<%s>' % filename)
    image.add_header('Content-Type', 'image/jpeg')
    msg.attach(attachment)

    try:
      server = smtplib.SMTP(smtp_server, smtp_port)
      server.starttls()
      server.login(self.sender_email, self.sender_password)

      server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
      print("Email sent successfully.")

    except Exception as e:
      print(f"Error: {str(e)}")

    finally:
      server.quit()
