# Check IP

A script to check if your public ip has changed from the last time you have run the script. If so it will send an email informing the change

## Getting Started

```
$ python3 ~/check_ip.py -l a.account@gmail.com -p secretPassword -s recipient@gmail.com
```

**arguments:**
```
  -h, --help            show this help message and exit
  -l LOGIN, --login LOGIN
                        gmail email account
  -p PASSWORD, --password PASSWORD
                        smtp password
  -s SEND_TO, --send_to SEND_TO
                        email recepient of ip changes
```

### Prerequisites

* python 3 on a linux/macosx OS
* spare gmail account credentials

### Installing

You can add this script as a cron job.

5h example:

```
0 */5 * * * python3 /home/<change_to_your_home>/check_ip.py -l <from>@gmail.com -p <password> -s someone@somewhere.com 
```

## Authors

* **Nikolas Kuimcidis**

## License

This project is licensed under the MIT License
