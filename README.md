# ftp_proxy
This WSGI script implements a http to ftp proxy for Apache2 (tested under Ubuntu 16.04).
Nexus Repository Manager from Sonatype is able to base raw proxies on http and https,
but not on ftp and this script shall help to circumvent this.

This is my first attempt on WSGI, Python programming and Apache2 configuration, please be nice with any comments :-)

## Invocation

Call
```bash
wget http://localhost/ftp_proxy?ftpurl=ftp.gnu.org/gnu/hello/hello-2.7.tar.gz
```
in order to perform a ftp download from *ftp://ftp.gnu.org/gnu/hello/hello-2.7.tar.gz*.

## TODO
1. Test with Nexus Repository Manager - we may have problems with the name
of the downloaded file
2. Use mod_rewrite of Apache2 to get rid of the CGI style parameter passing in the URL - I'm not sure, if Nexus Repository Manager is happy with this. Preferably, the download above should work with this URL:
*http://localhost/ftp/ftp.gnu.org/gnu/hello/hello-2.7.tar.gz*
