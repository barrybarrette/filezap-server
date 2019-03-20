# filezap-server
[![Build Status](https://travis-ci.org/whitebarry/filezap-server.svg?branch=master)](https://travis-ci.org/whitebarry/filezap-server)
[![Coverage Status](https://coveralls.io/repos/github/whitebarry/filezap-server/badge.svg)](https://coveralls.io/github/whitebarry/filezap-server)

FileZap is a very simple temporary file storage platform that allows users to send files from their mobile device and then access them via a web browser on any device. This project is the backend service that handles user management and file storage. 

The Android app is now available on [Google Play](https://play.google.com/store/apps/details?id=com.shredderstudios.filezap)

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
