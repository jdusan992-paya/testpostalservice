# testpostalservice
Local SMTP server for testing application email sending capabilities. 
This project is created to simplify testing mail functionalities during application development


Quick start
python3 main.py


Sending mail using telnet:

telnet localhost 8025

EHLO localhost
MAIL FROM:<sender@example.com>
RCPT TO:<test@example.com>
DATA
From: sender@example.com
To: test@example.com
Subject: Hello from terminal

This is a test message.
.
QUIT

