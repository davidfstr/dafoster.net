---
layout: post
title: Sending email from command line scripts
tags: [Software, Productivity]

---

This weekend I open-sourced a script called [notifymail] which I have been using for the past few years to send myself emails from automated scripts, particularly Python scripts.

It is very easy to configure `notifymail` for the first time:

```
$ pip install notifymail
$ notifymail.py --setup
SMTP Server Hostname: smtp.gmail.com
SMTP Server Port [465]: 587
SMTP Server Uses TLS (y/n) [n]: yes
SMTP Username: robot@gmail.com
SMTP Password: ********
From Address [robot@gmail.com]: robot@gmail.com
From Name (optional) []: notifymail
To Address: admin@example.com

Verifying connection to SMTP server... OK
```

Check your mail provider's documentation to get the SMTP settings mentioned above. For example I made an internet search for "gmail SMTP settings" to find [Gmail's SMTP settings](https://support.google.com/mail/troubleshooter/1668960?hl=en#ts=1665119,1665162):

* **Gmail SMTP Server:** smtp.gmail.com
* **Gmail SMTP Port:** 587 (for TLS)
* **Gmail SMTP Uses TLS?** yes

Once you have `notifymail` installed, you can send an email to yourself in a Python script with as little code as:

```
import notifymail
notifymail.send('Subject', 'Hello World', from_name='greeting_script')
```

Or you can invoke `notifymail` from the command line:

```
$ echo "Hello World" | notifymail.py -s "Subject"
```

Full documentation is available on the [notifymail project page].

[notifymail]: https://github.com/davidfstr/notifymail
[notifymail project page]: https://github.com/davidfstr/notifymail#readme

## Hasn't this been done before?

I reinvented my own wheel to send email principally because of the poor documentation of other alternatives:

* `mail` and `postfix` were so complicated I couldn't figure out how to set them up.

* `ssmtp` didn't work after I tried to configure it and there was no good documentation to help me debug why it wasn't working.

For reference, here's [some information for setting up those alternatives](http://unix.stackexchange.com/questions/36982/can-i-set-up-system-mail-to-use-an-external-smtp-server).

## Fun things to do with `notifymail`

* I have a script called `heartbeat` that periodically attempts to connect to all of my servers via SSH. If it cannot connect to a server it sends me an email with `notifymail`. If it cannot access email it displays a sticky Growl notification locally.

* I have another script called `meetupfilter` that tracks incoming "New Meetup Group" emails from [Meetup]. It waits until all such announced groups have at least 3 events on their calendar before sending me a notification at my personal email with `notifymail`. That way I don't hear about Meetup groups that appear but then fizzle out immediately, which is a surprising number. I may open-source this script eventually if I [hear there is interest](/contact).

[Meetup]: http://www.meetup.com/