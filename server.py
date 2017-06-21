from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
import os

class TheServer(BaseHTTPRequestHandler):
	addressbook = {
		'g': 'http://www.google.com'
	}

	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>HTML Form</title>
	<link rel="stylesheet" href="" >
</head>
<body>
	<form action="/" method="post">
		<!-- <input type="text" name="q"> -->
		<input type="text" name="s" placeholder="Short code">
		<input type="text" name="l" placeholder="Long address">
		<!-- <input type="text" name="q"> -->
		<button type="submit">Submit</button>
	</form>

	<div class="msg">
		{}
	</div>
</body>
</html>
	'''

	def do_GET(self):
		if self.path == '/':
			self.send_response(200)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			self.wfile.write(self.make_HTML().encode())
		elif self.addressbook[self.path[1:]] is not None:
			self.send_response(303)
			self.send_header("Location", self.addressbook[self.path[1:]])
			self.end_headers()
		else:
			self.send_response(404)
			self.send_header("Content-Type", "text/plain")
			self.end_headers()
			self.wfile.write("Not Found.".encode())

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		args = parse_qs(self.rfile.read(content_length).decode())

		key = str(args['s'][0])
		value = str(args['l'][0])

		if self.check_URL(value) is True:
			self.addressbook[key] = value

			self.send_response(303)
			self.send_header("Location", "/")
			self.end_headers()
		else:
			self.send_response(404)
			self.send_header("Content-Type", "text/plain")
			self.end_headers()
			self.wfile.write("URL invalid".encode())


	def check_URL(self, url):
		try:
			r = requests.get(url)
		except:
			return False
		return r.status_code == 200

	def make_HTML(self):
		addressStrings = []

		for address in self.addressbook:
			addressStrings.append(address + ' : ' + self.addressbook[address])
		addressLines = "<br>".join(addressStrings)
		return self.html.format(addressLines)

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 8000))
	server_address = ('', port)
	httpd = HTTPServer(server_address, TheServer)
	httpd.serve_forever()