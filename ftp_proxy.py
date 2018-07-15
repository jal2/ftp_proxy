import ftplib
import os
import os.path
import tempfile
import cgi
try:
# Python 2.6-2.7 
	from HTMLParser import HTMLParser
except ImportError:
# Python 3
	from html.parser import HTMLParser

def download(host, path, remote_file, local_fd):
	"""download a file with ftp,
		host - host name
		path - path to the file
		remote_file - remote file name
		local_fd - local fd to write file to
	"""
	print('#DBG host %s path %s remote_file %s' % (host,path,remote_file))
	ftp = ftplib.FTP(host)
	print('#DBG connected')
	ftp.login()
	print('#DBG after login')
	if path:
		ftp.cwd(path)
		print('#DBG after cwd')
	else:
		print('#DBG path is empty')
	ftp.retrbinary('RETR ' + remote_file, local_fd.write)
	print('#DBG after retrbinary')
	ftp.quit()

def split_url(url):
	"""Split the ftp url into host, path and filename and return a tripel"""
	l = url.split("/",1)
	host = l[0]
	path = os.path.dirname(l[1])
	filename = os.path.basename(l[1])
	return (host, path, filename)

def response_error(start_response):
	"""response with an error 422"""
	start_response('422 Unprocessable Entity', [('Content-type', 'text/html')])
	
def application(environ,start_response):
	block_size = 4096
	h = HTMLParser()
	parameters = cgi.parse_qs(environ.get('QUERY_STRING', ''))
	if 'ftpurl' not in parameters:
		response_error(start_response)
		return 'Missing ftpurl parameter\r\n'
	else:
		ftpurl = h.unescape(parameters['ftpurl'][0])
	# TODO: we may use urlparse module here to split the ftpurl value
	# ftpurl contains both host, path and filename
	try:
		h,p,f = split_url(ftpurl)
	except ValueError:
		response_error(start_response)
		return 'invalid ftpurl parameter (cannot split into host,path,filename)\r\n'
# we must create an unqiue local filename for the ftp download
# this one will automatically be unlinked after usage
	fd = tempfile.TemporaryFile()
	try:
		download(h,p,f,fd)
	except Exception as ex:
		response_error(start_response)
		return 'ftp download failed: %s\r\n' % (ex.args)
# get the file size
	size = os.fstat(fd.fileno()).st_size
	status = "200 OK"
	response = [('Content-Disposition', 'attachment; filename="' + f + '"'),
		('Content-Type', 'application/octet-stream')]
	start_response(status, response)
# rewind the seek pointer for reading
	fd.seek(0)
# see PEP 333
	if 'wsgi.file_wrapper' in environ:
		return environ['wsgi.file_wrapper'](fd, block_size)
	else:
		return iter(lambda: fd.read(block_size), '')

