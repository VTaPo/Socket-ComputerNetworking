from tkinter import*
import socket
import threading
from tkinter import messagebox
import tkinter.scrolledtext as scrollText
import string
import csv
from cloud_mongo import*

account_logined_list=[]
check_logined=False

global db
database_name = "data"
mongo_uri = 'mongodb+srv://phong:fwK3jiK2zlDStafv@tapo.uufh4.mongodb.net/data?retryWrites=true&w=majority'
try:
    client = MongoClient(mongo_uri)
    client.server_info() # will throw an exception
    db=client[database_name]
except:
	pass

SERVERID = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDRESS=(SERVERID,PORT)
LOGIN = 'login'
REGISTER = 'register'
LOGOUT='logout'
LOGOUT2='logout2'
FORMAT = 'utf8'
SEARCH='search'

def sendList(socket, list):
	Item = None
	for Item in list:
		socket.sendall(Item.encode(FORMAT))
		socket.recv(1024).decode(FORMAT)
	Item = 'End'
	socket.sendall(Item.encode(FORMAT))
def recvList(socket):
	list = []
	Item = None
	while(True):
		Item = socket.recv(1024).decode(FORMAT)
		if(Item == 'End'):
			break
		list.append(Item)
		socket.sendall(Item.encode(FORMAT))
	return list

class main(Tk):
	def RefreshOutput(self):
		self.list_output.delete("2.0", 'end')
	def placeGUI(self):
		self.list_label.place(width=125, height = 25, x = 15, y = 40)
		self.list_output.place(width = 670, height = 260, x = 15, y = 80)
		self.close_btn.place(width = 200, height =25, x = 480, y = 350)
		self.home_label.pack()
	def __init__(self):
		Tk.__init__(self)
		self.title("SERVER SIDE")
		self.geometry('700x400')
		self.resizable(width = False, height = False)
		self.home_label = Label(self, text = "SERVER SIDE", font = "Times 20 bold", fg = "#009DAE", bg = "#C2FFF9")
		self.list_label = Label(self, text = "List of clients: ", font ="Times 16 bold ", fg = "#009DAE", bg = "#C2FFF9")
		self.list_output = scrollText.ScrolledText(self, font = "Times 14", wrap='word')
		self.close_btn = Button(self, text = "Close all connections", font = "Times 14 bold", fg = "#009DAE", bg = "#C2FFF9")
		self.configure(bg = "#C2FFF9")
		self.check_info_exist=False

		thr1 = threading.Thread(target= self.placeGUI)
		thr2 = threading.Thread(target = self.startServer)
		thr1.start()
		thr2.start()

	def on_closing(self):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			server.close()
			self.destroy()

	def ClientLogOut(self,conn:socket,addr):
		self.list_output.insert('end', f"Client {addr} has disconnected.\n")
		conn.sendall(LOGOUT.encode(FORMAT))

	def handleLoginAndRegisterOfClient(self, conn:socket, option):
		user = conn.recv(1024).decode(FORMAT)
		conn.sendall(user.encode(FORMAT))
		pwd = conn.recv(1024).decode(FORMAT)
		conn.sendall(pwd.encode(FORMAT))

		accounts=db.Users.find({})
		usersName=[]
		passWord=[]
		size=0
		if accounts:
			for item in accounts:
				usersName.append(item['username'])
				passWord.append(item['pwd'])
		check = None
		global account_logined_list
		global check_logined
		if(option == LOGIN):
			if accounts:
				for i in range(0,len(passWord)):
					if(pwd == passWord[i] and user == usersName[i]):
						for j in range(0,len(account_logined_list)):
							if len(account_logined_list)==0:
								break
							if(pwd==account_logined_list[j][0]) and (user==account_logined_list[j][1]):
								check_logined=True
								break
						if check_logined:
							check = 'loginFailed'
							check_logined=False
						else:
							account_logined_list.append([pwd,user])
							check = LOGIN
							break
				if check==None:
					check = 'loginFailed'
			else:
				check='loginFailed'

		elif(option==LOGOUT2):
			for i in range(0,len(account_logined_list)):
				if(account_logined_list[i][0]==pwd) and (account_logined_list[i][1]==user):
					account_logined_list.pop(i)
					break
			check=LOGOUT2

		elif(option == REGISTER):
			if len(usersName)!=0:
				for username in usersName:
					if(username == user):
						check='False'
						break
			if len(usersName)==0 or check!='False':
				check=REGISTER
				db.Users.insert_one({"username":user,"pwd":pwd})

		conn.sendall(check.encode(FORMAT))

	def SearchData(self, conn:socket):
		names=[]
		total_case=[]
		today_case=[]
		date_update=''
		time_update=''

		location=conn.recv(1024).decode(FORMAT)
		conn.sendall(location.encode(FORMAT))
		time_zone=conn.recv(1024).decode(FORMAT)
		conn.sendall(time_zone.encode(FORMAT))
		send_msg=[]
		dt=db.covids.find({"date":time_zone})
		if dt:
			for item in dt:
				date_update=item['date']
				time_update=item['time']
				for info in item['data']['locations']:
					names.append(info['name'])
					total_case.append(info['cases'])
					today_case.append(info['casesToday'])
		if len(names)!=0:
			for i in range(0,len(names)):
				if(location==names[i]):
					send_msg.append(names[i])
					send_msg.append(str(total_case[i]))
					send_msg.append(str(today_case[i]))
					send_msg.append('Server updated in: ')
					send_msg.append(date_update)
					send_msg.append(time_update)
					self.check_info_exist=True
					break;
		if self.check_info_exist==False or len(names)==0:
			send_msg.append('Invalid')
		else:
			self.check_info_exist=False
		sendList(conn,send_msg)

	def handleClient(self,conn,addr):
		self.list_output.insert('end', f"Client {addr} is connecting.\n")
		try:
			selection = None
			while(selection != 'Exit'):
				selection = conn.recv(1024).decode(FORMAT)
				conn.sendall(selection.encode(FORMAT))
				if(selection == LOGIN):
					self.handleLoginAndRegisterOfClient(conn, LOGIN)
				elif(selection == REGISTER):
					self.handleLoginAndRegisterOfClient(conn, REGISTER)
				elif(selection == LOGOUT):
					self.ClientLogOut(conn,addr)
				elif selection==SEARCH:
					self.SearchData(conn)
				elif selection==LOGOUT2:
					self.handleLoginAndRegisterOfClient(conn, LOGOUT2)
			conn.close()
		except:
			conn.close()

	def startServer(self):
		global server
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(ADDRESS)
		server.listen()
		self.list_output.insert('end', f"Server is launching on {SERVERID}.")
		self.list_output.insert('end','\n')
		while True:
			try:
				conn, addr = server.accept()
				client_thread = threading.Thread(target = self.handleClient, args = (conn, addr))
				client_thread.daemon = True
				client_thread.start()
			except:
				break


def get_data():
	crawling_data(60,db)
def on_screen():
	win = main()
	win.protocol("WM_DELETE_WINDOW", win.on_closing)
	win.mainloop()
sv=threading.Thread(target=on_screen)
dt=threading.Thread(target=get_data)
dt.daemon=True
sv.start()
dt.start()
