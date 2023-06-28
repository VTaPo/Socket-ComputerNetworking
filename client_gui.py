from tkinter import*
import socket
from tkinter import font
from tkinter import messagebox
import tkinter.scrolledtext as scrollText
from typing import Sized
from requests.api import options
from tkcalendar import DateEntry
import tkinter.ttk as exTk
# import tkcalendar

FORMAT = 'utf8'
LOGIN = 'login'
REGISTER = 'register'
LOGOUT='logout'
LOGOUT2='logout2'
SEARCH='search'
PORT = 65432

global time_to_update
time_to_update=""
global check_click_refresh_btn
check_click_refresh_btn=False
global ttu 
global provinces
provinces=[]

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

def convertDate(date):
	newDate = ''
	if len(date)==6:	
		newDate = newDate + '0' + date[2] + "-" + '0' + date[0] + "-" + "20" + date[4] + date[5]
	if len(date)==7:
		if date[0]!='0':
			newDate = newDate + '0' + date[3] + "-" + date[0] + date[1] + "-" + "20" + date[5] + date[6]
		else:
			newDate = newDate + date[2] + date[3] + "-" + '0' + date[0] + "-" + "20" + date[5] + date[6]
	else:
		newDate = newDate + date[3] + date[4] + "-" + date[0] + date[1] + "-" + "20" + date[6] + date[7]
	return newDate

class SocketPage(Frame):
	def checkIPServer(self, newFrame, mainSelf):
		SERVERID = self.ip_server_input.get()
		try:
			global client
			client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client.connect((SERVERID, PORT))
			self.ip_server_input.delete("0", "end")
			self.notify["text"] = ""
			mainSelf.changePage(LoginPage)
		except:
			self.notify["text"] = "Wrong IP"
				
	def __init__(self, master, mainSelf):
		Frame.__init__(self, master)
		self.socket_label = Label(self, text = "CLIENT SIDE", font  = "Times 20 bold", bg = "#009DAE")
		self.ip_server_label = Label(self, text = "Input IP Server", font = "Times 14 bold", bg = "#009DAE")
		self.ip_server_input = Entry(self, font = "Times 14", justify='center')
		

		self.notify = Label(self, text = "", font = "Times 14 bold", fg = "red",  bg = "#009DAE")
		self.connect_btn = Button(self, text= "Connect", font = "Times 18 bold", bg = "#FFE652", borderwidth=1, relief="raised",
		command = lambda: self.checkIPServer(LoginPage, mainSelf))
		self.socket_label.pack(pady= 12)
		self.ip_server_label.pack(pady= 90)

		self.ip_server_input.focus()
		self.ip_server_input.place(width = 150, height = 25, x = 275, y = 200)
		self.notify.place(width = 150, height= 25, x = 275, y = 240)
		self.connect_btn.place(width = 120, height= 30, x = 290, y = 270)
		self.configure(bg= "#009DAE")

class CreditPage(Frame):
	def changePage(self, mainSelf):
		mainSelf.changePage(LoginPage)
	def placeGUI(self):
		self.credit_label.pack(pady = 8)
		self.background_img_label.pack()
		self.name1_label.pack(pady = 2)
		self.name2_label.pack(pady = 2)
		self.name3_label.pack(pady = 2)
		self.back_btn.place(x = 580, y = 360)
		self.configure(bg = "#009DAE")
	def __init__(self, master, mainSelf):
		Frame.__init__(self, master)
		self.credit_label = Label(self, text = "CREDIT", font = "Times 20 bold", bg = "#009DAE")
		self.background_img = PhotoImage(file="resource/logo.png")
		self.background_img_label = Label(self, bd=0, image = self.background_img)
		self.name1_label = Label(self, text = "20120547 - Võ Thành Phong", font = "Times 14 bold",bg = "#009DAE")
		self.name2_label = Label(self, text = "20120555 - Nguyễn Xuân Quân", font = "Times 14 bold",bg = "#009DAE")
		self.name3_label = Label(self, text = "20120578 - Phạm Quốc Thái", font = "Times 14 bold",bg = "#009DAE")
		self.back_btn = Button(self, text = "BACK", width = 10, bg = "#FFE652", font = "Times 12 bold",
		fg = "blue", borderwidth=1, relief="raised", command = lambda: self.changePage(mainSelf))
		self.placeGUI()

class LoginPage(Frame):
	def changePageAndDeleteContent(self, mainSelf, newFrame):
		self.user_input.delete("0", "end")
		self.pass_input.delete("0", "end")
		self.notify["text"] = ""
		mainSelf.changePage(newFrame)
	def placeGUI(self):
		self.login_label.pack(pady = 8)
		self.user_label.pack()
		self.user_input.pack()
		self.pass_label.pack()
		self.pass_input.pack()
		self.notify.pack(pady = 4)
		self.login_btn.pack(pady=8)
		self.register_btn.pack(pady=8)
		self.disconnect_btn.place(x = 590, y = 360)
		self.credit_btn.place(x = 10, y = 360)
		self.configure(bg = "#009DAE")
	def __init__(self, master, mainSelf):
		Frame.__init__(self, master)
		self.login_label = Label(self, text = "LOGIN PAGE", font = "Times 20 bold", bg = "#009DAE")
		self.user_label = Label(self, text = "Username", font = "Times 14 bold",bg = "#009DAE")
		self.user_input = Entry(self, width = 24, font = "Times 14",bg = "#C2FFF9", borderwidth= 1)
		self.user_input.focus()
		self.pass_label = Label(self, text = "Password", font = "Times 14 bold", bg = "#009DAE")
		self.pass_input = Entry(self, width = 24, font = "Times 14", bg = "#C2FFF9", borderwidth= 1, show="*")
		self.notify = Label(self,text = "", fg = "red", font = "Times 15 bold",bg = "#009DAE")
		self.login_btn = Button(self, text = "LOGIN", width = 20, bg = "#FFE652", font = "Times 12 bold",
		fg = "blue", borderwidth=1, relief="raised", command=lambda: mainSelf.login(self, client))
		self.disconnect_btn = Button(self, text = "Disconnect", width = 10, bg = "#FFE652", font = "Times 12 bold",
		fg = "red", borderwidth=1, relief="raised", command=lambda: mainSelf.disconnect(client,SocketPage, self))
		self.register_btn = Button(self, text = "Register", width = 20, bg = "#FFE652", font = "Times 12 bold", 
		fg = "blue", borderwidth=1, relief="raised", command = lambda: self.changePageAndDeleteContent(mainSelf, RegisterPage))
		self.credit_btn = Button(self, text = "Credit", width = 10, bg = "#FFE652", font = "Times 12 bold", 
		fg = "blue", borderwidth=1, relief="raised", command = lambda: self.changePageAndDeleteContent(mainSelf, CreditPage))
		self.placeGUI()

class RegisterPage(Frame):
	def placeGUI(self):
		self.login_label.pack(pady = 8)
		self.user_label.pack()
		self.user_input.pack()
		self.pass_label.pack()
		self.pass_input.pack()
		self.pass_again_label.pack()
		self.pass_again_input.pack()
		self.notify.pack(pady = 6)
		self.register_btn.pack()
		self.back_btn.pack(pady = 12)
		self.configure(bg = "#009DAE")

	def changePageAndDeleteContent(self, mainSelf):
		self.user_input.delete("0", "end")
		self.pass_input.delete("0", "end")
		self.pass_again_input.delete("0", "end")
		self.notify["text"] = ""
		mainSelf.changePage(LoginPage)

	def __init__(self, master, mainSelf):
		Frame.__init__(self, master)
		self.login_label = Label(self, text = "REGISTER PAGE", font = "Times 20 bold", bg = "#009DAE")
		self.side = Label(self, text = "Client side", font = "Times 12 bold", bg = "#009DAE")
		self.user_label = Label(self, text = "Username", font = "Times 14 bold",bg = "#009DAE")
		self.user_input = Entry(self, width = 24, font = "Times 14",bg = "#C2FFF9", borderwidth= 1)
		self.user_input.focus()
		self.pass_label = Label(self, text = "Password", font = "Times 14 bold", bg = "#009DAE")
		self.pass_input = Entry(self, width = 24, font = "Times 14", bg = "#C2FFF9", borderwidth= 1, show="*")
		self.pass_again_label = Label(self, text = "Confirm password", font = "Times 14 bold", bg = "#009DAE")
		self.pass_again_input = Entry(self, width = 24, font = "Times 14", bg = "#C2FFF9", borderwidth= 1, show="*")
		self.notify = Label(self,text = "", fg = "red", font = "Times 15 bold",bg = "#009DAE")
		self.register_btn = Button(self, text = "REGISTER", width = 20, bg = "#FFE652", font = "Times 12 bold",
		fg = "blue", borderwidth=1, relief="raised", command=lambda: mainSelf.register(self, client))
		self.back_btn = Button(self, text = "Back to Login", width = 20, bg = "#FFE652", font = "Times 12 bold", 
		fg = "blue", borderwidth=1, relief="raised", command = lambda: self.changePageAndDeleteContent(mainSelf))
		self.placeGUI()

class HomePage(Frame):
	def placeGUI(self):
		self.search_label.place(width=50, height = 25, x = 10, y = 40)
		self.search_input.place(width= 260,height = 25, x = 60, y = 40)
		self.calendar_label.place(width = 50, height = 25, x = 360, y = 40)
		self.calendar_input.place(width = 100, height = 25, x = 420, y = 40)
		self.search_btn.place(width= 80,height = 25, x = 590, y = 40)
		self.search_output.place(width = 670, height = 260, x = 15, y = 80)
		self.refresh_btn.place(width = 80, height =25, x = 15, y = 350)
		self.logOut.place(width = 80, height= 25, x = 605, y = 350)
		self.home_label.pack()

	def RefreshOutput(self):
		self.search_output.delete("2.0", 'end')
		self.search_output.insert("end","\n")
		time_to_update=""
		ttu = Label(self, text = time_to_update, font = "Times 14 bold", fg = "#009DAE", bg = "#C2FFF9")
		ttu.place(width=470,height=25,x=115,y=350)

	def __init__(self, parent, mainSelf):
		Frame.__init__(self, parent)
		self.home_label = Label(self, text = "HOME PAGE", font = "Times 20 bold", fg = "#009DAE", bg = "#C2FFF9")
		self.search_label = Label(self, text = "City: ", font ="Times 14 bold ", fg = "#009DAE", bg = "#C2FFF9")
		self.search_input = exTk.Combobox(self, font = "Times 13 bold", state="readonly")
		provinces=("An Giang","Bà Rịa – Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre",
		"Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao Bằng","Đà Nẵng","Đắk Lắk","Đắk Nông","Điện Biên"
		,"Đồng Nai","Đồng Tháp","Gia Lai","Hà Giang","Hà Nam","Hà Nội","Hà Tĩnh","Hải Dương","Hải Phòng","Hậu Giang","Hòa Bình",
		"Hưng Yên","Khánh Hòa","Kiên Giang","Kon Tum","Lai Châu","Lâm Đồng","Lạng Sơn","Lào Cai","Long An","Nam Định","Nghệ An",
		"Ninh Bình","Ninh Thuận","Phú Thọ","Phú Yên","Quảng Bình","Quảng Nam","Quảng Ngãi","Quảng Ninh","Quảng Trị","Sóc Trăng",
		"Sơn La","Tây Ninh","Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","TP. Hồ Chí Minh","Trà Vinh",
		"Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái")
		self.search_input['value'] = provinces
		self.search_input.current(0)
		self.calendar_label = Label(self, text = "Date", font = "Times 14 bold",fg = "#009DAE", bg = "#C2FFF9") 
		self.calendar_input = DateEntry(self, selectmode ="day", font = "Times 12 bold")
		self.search_btn = Button(self, text = "Search", font ="Times 14 bold ", fg = "#009DAE", bg = "#C2FFF9",command=lambda:mainSelf.SearchData(self.search_input.get(),client,self))
		self.search_output = scrollText.ScrolledText(self)
		self.search_output.insert("end","Location"+(" "*15)+"Total cases"+(" "*15)+"Today cases"+(" "*14)+"Date\n")
		self.refresh_btn = Button(self, text = "Refresh", font = "Times 14 bold", fg = "#009DAE", bg = "#C2FFF9", 
		command=self.RefreshOutput)
		self.logOut = Button(self, text= "Log Out", font = "Times 14", fg = "red", bg = "#C2FFF9",
		command=lambda:mainSelf.Logout(client,LoginPage,self))
		self.configure(bg = "#C2FFF9")
		self.placeGUI()

class main(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title("CLIENT SIDE")
		self.geometry('700x400')
		self.protocol("WM_DELETE_WINDOW",self.on_closing)
		self.resizable(width = False, height = False)
		self.user=''
		self.pwd=''
		container = Frame(self)
		container.pack(side = "top", fill = "both", expand = True)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)
		self.frames = {}
		for f in (HomePage, LoginPage,CreditPage, RegisterPage, SocketPage):
			frame = f(container, self)
			frame.grid(row = 0, column = 0, sticky ="nsew")
			self.frames[f] = frame
		
		self.frames[SocketPage].tkraise()
	def changePage(self, newFrame:Frame):
		self.frames[newFrame].tkraise()
	
	def on_closing(self):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			self.destroy()
			try:
				if self.user!='' and self.pwd!='':
					client.sendall(LOGOUT2.encode(FORMAT))
					client.recv(1024).decode(FORMAT)
					client.sendall(self.user.encode(FORMAT))
					client.recv(1024).decode(FORMAT)
					client.sendall(self.pwd.encode(FORMAT))
					client.recv(1024).decode(FORMAT)
					client.recv(1024).decode(FORMAT)
				option = LOGOUT
				client.sendall(option.encode(FORMAT))
				client.recv(1024).decode(FORMAT)
			except:
				pass
			
	def login(self, loginFrame, socket:socket):
		username = loginFrame.user_input.get()
		pwd = loginFrame.pass_input.get()
		self.user=username
		self.pwd=pwd
		if(username == "" and pwd == ""):
			loginFrame.notify["text"] = "Username and Password are empty!"
			return
		if(username == ""):
			loginFrame.notify["text"] = "Username is empty!"
			return
		if(pwd == ""):
			loginFrame.notify["text"] = "Password is empty!"
			return
		else:
			try:
				check = None
				socket.sendall(LOGIN.encode(FORMAT))
				socket.recv(1024).decode(FORMAT)
				socket.sendall(username.encode(FORMAT))
				socket.recv(1024).decode(FORMAT)
				socket.sendall(pwd.encode(FORMAT))
				socket.recv(1024).decode(FORMAT)
				check = socket.recv(1024).decode(FORMAT)
				if(check == LOGIN):
					loginFrame.user_input.delete("0", "end")
					loginFrame.pass_input.delete("0", "end")
					loginFrame.notify["text"] = ""
					self.changePage(HomePage)
				else:
					loginFrame.notify["text"] = "Login failed!"
			except:
				loginFrame.notify["text"] = "Server disconnected!"
				socket.close()        

	def register(self, loginFrame, socket:socket):
		username = loginFrame.user_input.get()
		pwd = loginFrame.pass_input.get()
		pwd_again = loginFrame.pass_again_input.get()
		if(username == "" and pwd == ""):
			loginFrame.notify["text"] = "Username and Passwords are empty!"
			return
		if(username == ""):
			loginFrame.notify["text"] = "Username is empty!"
			return
		if(pwd == "" or pwd_again == ""):
			loginFrame.notify["text"] = "Passwords are empty!"
			return
		if(pwd != pwd_again):
			loginFrame.notify["text"] = "Passwords are not the same!"
			return
		else:
			try:
				socket.sendall(REGISTER.encode(FORMAT))
				x = socket.recv(1024).decode(FORMAT)
				socket.sendall(username.encode(FORMAT))
				socket.recv(1024).decode(FORMAT)
				socket.sendall(pwd.encode(FORMAT))
				socket.recv(1024).decode(FORMAT)
				check = socket.recv(1024).decode(FORMAT)
				if(check == REGISTER):
					loginFrame.notify["text"] = "Register's successfull!"
				else:
					loginFrame.notify["text"] = "Username already exists!"
			except:
				loginFrame.notify["text"] = "Server disconnected!"
				socket.close()

	def SearchData(self,msg,socket:socket,newFrame:Frame):
		time_zone=newFrame.calendar_input.get()
		time_zone=convertDate(time_zone)
		try:
			socket.sendall(SEARCH.encode(FORMAT))
			socket.recv(1024).decode(FORMAT)
			location=msg
			socket.sendall(location.encode(FORMAT))
			socket.recv(1024).decode(FORMAT)
			socket.sendall(time_zone.encode(FORMAT))
			socket.recv(1024).decode(FORMAT)
			info=recvList(socket)
			if len(info)!=1:
				time_to_update=str(info[3])+' '+str(info[5])
				newFrame.search_output.insert("end",info[0]+(" "*(23-len(info[0])))+str(info[1])+" "*(49-23-len(str(info[1])))+str(info[2])+" "*(71-49-len(str(info[2])))+str(info[4])+"\n")
			else:
				newFrame.search_output.insert("end","No information found in database.\n")
				time_to_update=""
			ttu = Label(newFrame, text = time_to_update, font = "Times 14 bold", fg = "#009DAE", bg = "#C2FFF9")
			ttu.place(width=470,height=25,x=115,y=350)
		except:
			if messagebox.showinfo("ATTENTION","Server has disconnected"):
				self.changePage(SocketPage)
			socket.close()
	def Logout(self,socket:socket,newFrame,oldFrame):
		socket.sendall(LOGOUT2.encode(FORMAT))
		socket.recv(1024).decode(FORMAT)
		socket.sendall(self.user.encode(FORMAT))
		socket.recv(1024).decode(FORMAT)
		socket.sendall(self.pwd.encode(FORMAT))
		socket.recv(1024).decode(FORMAT)
		socket.recv(1024).decode(FORMAT)
		oldFrame.RefreshOutput()
		self.frames[newFrame].tkraise()
	def disconnect(self,socket:socket,newFrame, oldFrame):
		socket.sendall(LOGOUT.encode(FORMAT))
		socket.recv(1024).decode(FORMAT)
		socket.close()
		oldFrame.user_input.delete("0","end")
		oldFrame.pass_input.delete("0", "end")
		oldFrame.notify["text"] = ""
		self.changePage(newFrame)	

win = main()
win.mainloop()