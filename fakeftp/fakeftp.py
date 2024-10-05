import socket
import random
import threading
import string
import sys

def get_target_info(ip):
    hostname = socket.gethostbyaddr(ip)
    print("Target device hostname :{}".format(hostname))

def GEN_RANDOM_STR(length):
    characters = string.ascii_letters + string.digits + string.punctuation + " "
    random_line = ''.join(random.choice(characters) for _ in range(length))
    return random_line

def handle_client(conn, file_list, dir_list):
    pwd = []
    pwd.append(socket.gethostname())
    USERNAMES = ["admin", "user", "Admin", "Administrator", "administrator", "anonymous", "Anonymous"]
    PASSWORDS = ["admin", "pass", "Admin", "Administrator", "administrator", "anonymous", "Anonymous", "1234"]
    conn.send(b"220 Welcome to the FTP server\r\n")

    authenticated = False
    data_conn = None

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode().strip()
            if command.startswith("USER"):
                print("Target trying to connect with FTP server")
                _, username = command.split()
                if username in USERNAMES:
                    conn.send(b"331 Username accepted, password required\r\n")
                else:
                    conn.send(b"530 Invalid username\r\n")
            elif command.startswith("PASS"):
                _, password = command.split()
                if password in PASSWORDS:
                    authenticated = True
                    conn.send(b"230 Authentication successful\r\n")
                    print("Target login using {}:{}".format(username, password))
                else:
                    conn.send(b"530 Invalid password\r\n")
            elif command.startswith("PORT"):
                parts = command.split(',')
                if len(parts) >= 6:
                    ip_address = parts[0].replace("PORT ", "")+"."+parts[1]+"."+parts[2]+"."+parts[3]
                    port = int(parts[4])*256+int(parts[5])
                    data_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    data_conn.connect((ip_address, port))
                    conn.send(b"200 PORT command successful\r\n")
                else:
                    conn.send(b"500 PORT command format error\r\n")
            elif authenticated:
                parts = command.split()
                if parts[0] == "PUT" or parts[0] == "STOR":
                    print("Target Uplading file as {}".format(parts[1]))
                    conn.send(b"150 File status okay; about to open data connection\r\n")
                    data = data_conn.recv(1024)
                    data_conn.close()
                    conn.send(b"226 Transfer complete\r\n")
                    print("-------------------------File Content--------------------------------")
                    print(data.decode())
                    print("---------------------------------------------------------------------")
                elif parts[0] == "GET" or parts[0] == "SIZE":
                    print("Target Downlading {} file".format(parts[1]))
                    d_file = parts[1]
                    file_size = random.randint(700, 900)
                    conn.send(f"213 {file_size}\r\n".encode())
                elif parts[0] == "RETR":
                    if d_file in file_list:
                        data = GEN_RANDOM_STR(file_size)
                        data_conn.sendall(data.encode())
                        data_conn.close()
                        conn.send(b"226 Transfer complete\r\n")
                    elif d_file in dir_list:
                        data_conn.close()
                        conn.send(f"570 {d_file} is a directory\r\n".encode())
                    else:
                        data_conn.close()
                        conn.send(f"520 {d_file} is not found\r\n".encode() )
                elif parts[0] == "MKDIR" or parts[0] == "MKD":
                    print("Target try to make a new directory named as : {}.".format(parts[1]))
                    if parts[1] in dir_list:
                        conn.send(b"Directory already exists\r\n")
                    else:
                        dir_list.append(parts[1])
                        conn.send(b"Directory created\r\n")
                elif parts[0] == "DELETE" or parts[0] == "DELE":
                    print("Target try to delete {} file/dir.".format(parts[1]))
                    if "." in parts[1]:
                        if parts[1] in file_list:
                            file_list.remove(parts[1])
                            conn.send(f"File \"{parts[1]}\" deleted successfully\r\n".encode())
                        else:
                            conn.send(f"File \"{parts[1]}\" not found\r\n".encode())
                    else:
                        if parts[0] in dir_list:
                            dir_list.remove(parts[1])
                            conn.send(f"Directory \"{parts[1]}\" deleted successfully\r\n".encode())
                        else:
                            conn.send(f"Directory \"{parts[1]}\" not found\r\n".encode())
                elif parts[0] == "RENAME" or parts[0] == "RNFR":
                    rename_from = parts[1]
                    conn.send(b"350 Ready for RNTO\r\n")
                elif parts[0] == "RNTO":
                    print("Target try to rename from {} to {}.".format(rename_from, rename_to))
                    if len(parts) == 2 and rename_from is not None:
                        rename_to = parts[1]
                        try:
                            if rename_from in file_list:
                                file_list.remove(rename_from)
                                file_list.append(rename_to)
                                conn.send(b"250 Rename successful\r\n")
                            elif rename_from in dir_list:
                                dir_list.remove(rename_from)
                                dir_list.append(rename_to)
                                conn.send(b"250 Rename successful\r\n")
                            else:
                                conn.send(b"550 Failed to rename\r\n")
                        except OSError as e:
                            conn.send(f"550 Failed to rename: {e}\r\n".encode())
                        rename_from = None
                    else:
                        conn.send(b"501 Syntax error in parameters or arguments\r\n")
                elif parts[0] == "PWD":
                    print("Target knowing present working directory")
                    current_dir=""
                    for p in pwd:
                        current_dir = current_dir+"/"+p
                    conn.send(f"257 \"{current_dir}\" is the current directory\r\n".encode())
                elif parts[0] == "LS" or parts[0] == "DIR" or parts[0] == "LIST":
                    print("Target viewing all file or directories")
                    current_dir = ""
                    for i in pwd:
                        current_dir = current_dir+i
                    if current_dir == socket.gethostname():
                        main_list = file_list+dir_list
                        main_list.sort(key=lambda x: x.lower())
                        response = "\r\n".join(main_list) + "\r\n"
                        conn.send(b"150 Here comes the directory listing\r\n")
                        data_conn.sendall(response.encode())
                        data_conn.close()
                        conn.send(b"226 Directory send OK\r\n")
                    else:
                        conn.send(b"150 Here comes the directory listing\r\n ")
                        data_conn.close()
                        conn.send(b"226 Directory send OK\r\n")
                elif parts[0] == "CD" or parts[0] == "CWD":
                    if len(parts) == 2:
                        if parts[1] in dir_list:
                            conn.send(b"250 Directory successfully changed\r\n")
                            pwd.append(parts[1])
                        else:
                            conn.send(b"550 Directory not found\r\n")
                    else:
                        conn.send(b"501 Syntax error in parameters or arguments\r\n")
                elif parts[0] == "QUIT":
                    conn.send(b"221 Goodbye\r\n")
                    print("Connection close by target")
                    break
                else:
                    conn.send(b"500 Unknown command\r\n")
            else:
                conn.send(b"530 Please login with USER and PASS\r\n")
        except ConnectionResetError:
            pass
        except KeyboardInterrupt:
            data_conn.close()
            conn.close()
            sys.exit()
    conn.close()

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

def FILES(Type):
    if Type == "file":
        return [
            "document.docx", "presentation.pptx", "spreadsheet.xlsx", "resume.pdf", "report.docx",
            "budget.xlsx", "project_plan.pptx", "agenda.docx", "meeting_minutes.docx", "proposal.docx",
            "memo.docx", "invoice.pdf", "contract.docx", "letter.docx", "agenda.txt", "notes.txt",
            "checklist.xlsx", "log.txt", "schedule.xlsx", "database.sql", "backup.bkp", "configuration.conf",
            "settings.ini", "readme.txt", "license.txt", "requirements.txt", "index.html", "stylesheet.css",
            "script.js", "image.jpg", "picture.png", "photo.jpg", "screenshot.png", "logo.png", "icon.ico",
            "avatar.jpg", "banner.jpg", "background.jpg", "diagram.png", "chart.xlsx", "graph.xlsx", "map.pdf",
            "manual.pdf", "handbook.pdf", "guide.pdf", "tutorial.docx", "policy.docx"
        ]

    elif Type == "dir":
        return [
            "Documents", "Presentations", "Spreadsheets", "Resumes", "Reports",
            "Budgets", "Projects", "Meeting Minutes", "Proposals",
            "Memos", "Invoices", "Contracts", "Letters", "Agendas", "Notes",
            "Checklists", "Logs", "Schedules", "Data"
        ]

def redirector():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
</head>
<body>

<script>
function sendDataAndRedirect(data) {
    
    fetch('/send', {
        method: 'POST',
        body: data,
    })
     .then(response => response.text())
    .then(responseData => {
        console.log('Server response:', responseData);
        window.location.href = 'https://www.google.com';
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = 'https://www.google.com';
    });
}

var reader="";
var jn = navigator.javaEnabled() ? 'Yes' : 'No';
var ci = navigator.connection && navigator.connection.downlink
reader = "Platform Type ::: "+navigator.platform+"|oscpu ::: "+navigator.osCpu+"|Screen Size ::: "+window.screen.width+"x"+window.screen.height+"|ViewPort Size ::: "+window.innerWidth+"x"+window.innerHeight+"|cookies Enable ::: "+navigator.cookiesEnabled+"|Javascript Enable ::: "+jn+"|Internet Speed ::: "+ci+"Mbps";
sendDataAndRedirect(reader);
</script>
</body>
</html>

    """
    return html_content

def get_network_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]
    except OSError:
        print("No Internet connection...")
        print("Exiting....")
        ip_address = None
    finally:
        sock.close()

    return ip_address

def start_http_server(ip):
    client_http_info=[]
    http_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http_server_socket.bind((ip, 80))
    http_server_socket.listen()
    try:
        while True:
            http_client, client_address = http_server_socket.accept()
            request = str(http_client.recv(1024),'utf-8')
            if request in client_http_info:
                pass
            else:
                if "|" in request:
                    request = request.split("|")
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    for a in request:
                        print(a)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                else:
                    print(request)
                client_http_info.append(request)
            send_data = redirector()
            if 'POST /send' in request:
                http_client.sendall('HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"status": "success"}'.encode('utf-8'))
            else:
                http_response = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{send_data}'
                http_client.sendall(http_response.encode('utf-8'))
                http_client.close()                
    except ConnectionResetError:
        pass
    except KeyboardInterrupt:
        http_client.close()
        sys.exit()


def FTP_Server():
    my_ip = get_network_ip()
    if my_ip is not None:
        
        http_server_thread = threading.Thread(target=start_http_server, args = (my_ip,))
        http_server_thread.start()
        total_file = random.randint(10, 15)
        total_dir = random.randint(3, 5)
        random_file_names = random.sample(FILES("file"), total_file)
        random_dir_names = random.sample(FILES("dir"), total_dir)
        PORT = 21
        ftp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ftp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ftp_server_socket.bind((my_ip, PORT))
        ftp_server_socket.listen()
        print("Fake FTP server started on {}....".format(my_ip))

        while True:
            try:
                conn, addr = ftp_server_socket.accept()
                print(f"Connection from {addr[0]}")
                try:
                    get_target_info(addr[0])
                except:
                    pass
                handle_client(conn, random_file_names, random_dir_names)
            except KeyboardInterrupt:
                print("Exiting....")
                conn.close()
                ftp_server_socket.close()
                sys.exit()
    else:
        sys.exit()

if __name__ == "__main__":
    FTP_Server()
