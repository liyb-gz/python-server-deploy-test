from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

class TheServer(BaseHTTPRequestHandler):
	message = []

	html = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>HTML Form</title>
	<link rel="stylesheet" href="">
</head>
<body>
	<form action="http://localhost:8000/" method="post">
		<!-- <input type="text" name="q"> -->
		<textarea name="msg" id="msg" cols="30" rows="10"></textarea>
		<!-- <input type="text" name="q"> -->
		<button type="submit">Go!</button>
	</form>

	<div class="msg">{0}</div>
</body>
</html>
	'''

	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-Type", "text/html")
		self.end_headers()
		self.wfile.write(self.make_HTML().encode())

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		args = parse_qs(self.rfile.read(content_length).decode())
		content = args['msg'][0]
		self.message.append(content)

		self.send_response(200)
		self.send_header("Content-Type", "text/html")
		self.end_headers()
		self.wfile.write(self.make_HTML().encode())

	def make_HTML(self):
		messages = "<br>".join(self.message)
		return self.html.format(messages)

if __name__ == "__main__":
	server_address = ('', 8000)
	httpd = HTTPServer(server_address, TheServer)
	httpd.serve_forever()