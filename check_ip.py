import requests
import smtplib
from email.message import EmailMessage
import sys
import argparse

URL = "https://www.jakoumamip.cz"
HEADER_KEY = "public-ip"
FILE_WITH_IP = "/tmp/current_ip.tmp"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def main():

	email_login, email_pass, email_send_to = get_args()

	# retrieve current ip from external source
	try:
		old_ip = read_ip(FILE_WITH_IP)
		current_ip = get_current_ip(url = URL, option = HEADER_KEY)

	except ConnectionError:
		print(f"Failed to connect to {URL}")
		sys.exit()

	except KeyError:
		print(f"{URL} did not provide actual ip information")
		sys.exit()

	if old_ip == current_ip:
		print("IP did not change.")
		sys.exit()

	# save the current ip
	store_ip(ip = current_ip, file = FILE_WITH_IP)

	print(f"current ip '{current_ip}' differs from '{old_ip}'")

	# Send out the email
	try:
		send_mail(
			ip = current_ip,
			email_login = email_login,
			email_pass = email_pass,
			email_send_to = email_send_to
		)

	except Exception as e:
		print(f"Failed to send message, error: {str(e)}")


def get_args():
	"""Parse command line arguments"""
	parser = argparse.ArgumentParser(description="Checks if public ip has changed from last run and informs the user via email with the new ip information. You can add this script to your crontab so you can check your ip periodically")
	parser.add_argument("-l", "--login", required=True, help="gmail email account")
	parser.add_argument("-p", "--password", required=True, help="smtp password")
	parser.add_argument("-s", "--send_to", required=True, help="email recepient of ip changes")
	args = parser.parse_args()

	return args.login, args.password, args.send_to


def send_mail(ip, email_login, email_pass, email_send_to):
	"""Sends the email about ip change with the ip in the subject."""
	s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	s.starttls()
	s.login(email_login, email_pass)

	msg = EmailMessage()
	msg['Subject'] = f"New IP detected: {ip}"
	msg['From']    = email_login
	msg['To']      = email_send_to

	s.send_message(msg)


def read_ip(file):
	"""Reads the last ip from a file."""
	try:
		f = open(file, "r")
		old_ip =f.read()
		f.close()
	except FileNotFoundError:
		return None

	return old_ip


def get_current_ip(url, option):
	"""Sends an request for the actual ip."""
	"""Currently stored as a header param."""
	ip = None
	try:
		response = requests.head(url)
		ip = response.headers[option]
	except KeyError:
		raise KeyError
	except:
		raise ConnectionError from None

	return ip


def store_ip(ip, file):
	"""Stores the ip into a file."""
	f = open(file, "w+")
	f.write(ip)
	f.close()


if __name__ == "__main__":
   main()
