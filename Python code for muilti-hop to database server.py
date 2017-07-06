with SSHTunnelForwarder(
    ('rcg-linux-ts1.rcg.sfu.ca', 22), ssh_username = "cla315", ssh_password="*********", 
              remote_bind_address=('cs-oschulte-01.cs.sfu.ca', 3306)) as server:
    mydb = mysql.connector.connect(host='127.0.0.1', port = server.local_bind_port, user='root', passwd='*********',
	                       db='chao_draft')
    cursor = mydb.cursor()
