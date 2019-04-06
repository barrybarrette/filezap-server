# filezap-server
[![Build Status](https://travis-ci.org/whitebarry/filezap-server.svg?branch=master)](https://travis-ci.org/whitebarry/filezap-server)
[![Coverage Status](https://coveralls.io/repos/github/whitebarry/filezap-server/badge.svg)](https://coveralls.io/github/whitebarry/filezap-server)

FileZap is a very simple temporary file storage platform that allows users to send files from their mobile device and then access them via a web browser on any device. This project is the backend service that handles user management and file storage. 

The Android app is now available on [Google Play](https://play.google.com/store/apps/details?id=com.shredderstudios.filezap)

[Release Notes](https://github.com/whitebarry/filezap-server/releases/latest)

# FAQ

**How do I get started?**
1) [Register for an account](https://filezap.net/register) 
2) [Install the Android app](https://play.google.com/store/apps/details?id=com.shredderstudios.filezap) 
3) Enter your username and password in the app 
4) Use any app on your Android device that has the share menu and select FileZap to send files to your account 
5) Access your files on any device on [FileZap.net](https://filezap.net)


 **Are my files secure?**
 
Your files will be stored on BackBlaze currently and though this may change in the future, any content manager I implement will store the data securely. You can read about BackBlaze security [here](https://www.backblaze.com/security.html)


**Is there a size limit?**

At this time there is no size limit per account or per file. However, there is a 4 MB download limit - see [#19](https://github.com/whitebarry/filezap-server/issues/19). Additionally, in the interest of full disclosure, I'm using the BackBlaze free tier which has a 10GB limit, so if I get a sudden influx of active users it will cut off and I'll need to evaluate costs if that happens.



# Contributing
**Project setup**

1. [Install Python 3.6](https://www.python.org/downloads/) Other Python versions may work, I am developing on 3.6
2. Clone this repo: `git clone https://github.com/whitebarry/filezap-server.git && cd filezap-server`
3. Create a virtual environment: 
  * Linux: `python3 -m venv venv && source venv/bin/activate`
  * Windows: `python -m venv venv && venv\scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Verify install by running `bolt ut`. This will execute the unit tests and confirm you are set up. While developing, use `bolt ct` to run the unit tests continuously. 

You can start a local server by running `python main.py` from within your virtual environment. However, you will get errors for any actions you take without having the proper environment set up. The following environment variables must be set: 

* AWS_ACCESS_KEY_ID={your aws api key id}
* AWS_SECRET_ACCESS_KEY={your aws api key secret}
* BACKBLAZE_ACCOUNT_ID={your backblaze account id}
* BACKBLAZE_BUCKET_ID={the bucket id on backblaze you want to store files in}
* BACKBLAZE_MASTER_APP_ID={backblaze api key id that has the createKeys permission}
* BACKBLAZE_MASTER_SECRET_KEY={backblaze api key secret}
* USER_REGISTRATION_ENABLED=True
* FILEZAP_ENV=Production
 
**Environment setup**

**AWS**
* [Create an AWS account](https://portal.aws.amazon.com/billing/signup)
* Create an IAM user with the following permissions:
![](https://i.imgur.com/WcuiAKS.png)
* Create an access key and secret, save these as AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
![](https://i.imgur.com/22mA0W5.png)

**BackBlaze**
* [Create a BackBlaze account](https://www.backblaze.com/b2/sign-up.html)
* Save your account id as BACKBLAZE_ACCOUNT_ID
![](https://i.imgur.com/lMqmAqS.png)
* Create a bucket called filezap-server, make it private and save your bucket id as BACKBLAZE_BUCKET_ID
![](https://i.imgur.com/4209pva.png)
* Generate a master application key, save these as BACKBLAZE_MASTER_APP_ID and BACKBLAZE_MASTER_SECRET_KEY
![](https://i.imgur.com/LcIUJV7.png)
