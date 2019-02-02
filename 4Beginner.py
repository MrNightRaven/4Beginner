#Write for beginner
from line.linepy import *
from datetime import datetime
from googletrans import googletrans
import ast, codecs, json, os, re, random, requests, sys, time, pytz #Module

#========= Bagian login =========
#Choose 1 method from 3 | Pilih 1 cara dari 3 | Delete Comment(#) to choose
client = LINE(showQr=True)
#client = LINE('email', 'password')
#client = LINE('auth_token')
clientMid = client.profile.mid
clientStart = time.time() #Waktu bot dijalankan | Time the bot starts
clientPoll = OEPoll(client)
#========= Membuka file data =========
settingsOpen = codecs.open('settings.json', 'r', 'utf-8') #Membuka pengaturan, format (nama file, r = read, encoding)
#========= Mengatur variable =========
settings = json.load(settingsOpen)

def Jadwal(sendto, HARI, when, what):
	Day = ""
	if when == "Now":
		TXT = "╔══[ %s ]" % (HARI)
		num=0
		if what == "Pelajaran":
			for i in settings["Jadwal"][HARI]:
				num+=1
				TXT+="\n╠ [%s] %s" % (num, i)
			TXT+="\n╚══[ X RPL 2 ]"
			client.sendMessage(sendto, TXT)
		if what == "Piket":
			for i in settings["JadwalPiket"][HARI]:
				num+=1
				TXT+="\n╠ [%s] %s" % (num, i)
			TXT+="\n╚══[ X RPL 2 ]"
			client.sendMessage(sendto, TXT)
	if when == "Tommorow":
		if HARI == "Senin":
			Day = "Selasa"
		if HARI == "Selasa":
			Day = "Rabu"
		if HARI == "Rabu":
			Day = "Kamis"
		if HARI == "Kamis":
			Day = "Jumat"
		if HARI == "Jumat":
			Day = "Sabtu"
		if HARI == "Sabtu":
			Day = "Minggu"
		TXT = "╔══[ %s ]" % (Day)
		num=0
		if what == "Pelajaran":
			for i in settings["Jadwal"][Day]:
				num+=1
				TXT+="\n╠ [%s] %s" % (num, i)
			TXT+="\n╚══[ X RPL 2 ]"
			client.sendMessage(sendto, TXT)
#		if what == "Piket":
#			for i in settings["JadwalPiket"][Day]:
#				num+=1
#				TXT+="\n╠ [%s] %s" % (num, i)
#			TXT+="\n╚══[ X RPL 2 ]"
#			client.sendMessage(sendto, TXT)

def RestartBot():
	print("[ INFO ] : BOT RESETTED")
	python = sys.executable
	os.execl(python, python, * sys.argv)

def ChangeVideoProfile(pict, vids):
	try:
		files = {'file': open(vids, 'rb')}
		obs_params = client.genOBSParams({'oid': clientMid, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4', 'name': 'TMFS.mp4'})
		data = {'params': obs_params}
		r_vp = client.server.postContent('{}/talk/vp/upload.nh'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
		if r_vp.status_code != 201:
			return "Failed update profile"
		client.updateProfilePicture(pict, 'vp')
		return "Success update profile"
	except Exception as error:
		raise Exception("Error change video and picture profile %s" % (str(error)))

def logError(text):
	client.log("[ ERROR ] {}".format(str(text)))
	tz = pytz.timezone("Asia/Makassar")
	timeNow = datetime.now(tz=tz)
	timeHours = datetime.strftime(timeNow, "(%H:%M)")
	day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
	bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
	inihari = datetime.now(tz=tz)
	hr = inihari.strftime('%A')
	bln = inihari.strftime('%m')
	for i in range(len(day)):
		if hr == day[i]: hasil = hari[i]
	for k in range(0, len(bulan)):
		if bln == str(k): bln = bulan[k-1]
	time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
	with open("errorLog.txt","a") as error:
		error.write("\n[{}] {}".format(str(time), text))

def timeChange(secs):
	mins, secs = divmod(secs,60)
	hours, mins = divmod(mins,60)
	days, hours = divmod(hours,24)
	weeks, days = divmod(days,7)
	months, weeks = divmod(weeks,4)
	text = ""
	if months != 0: text += "%02d Bulan" % (months)
	if weeks != 0: text += " %02d Minggu" % (weeks)
	if days != 0: text += " %02d Hari" % (days)
	if hours !=  0: text +=  " %02d Jam" % (hours)
	if mins != 0: text += " %02d Menit" % (mins)
	if secs != 0: text += " %02d Detik" % (secs)
	if text[0] == " ":
		text = text[1:]
	return text

def backupData():
	try:
		backup = settings
		f = codecs.open('settings.json', 'w', 'utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as error:
		logError(error)
		return False

def HelpMenu(): #Isi menu bantuan, terserah anda | Fill in the help menu, Up to you
	HelpMenu = "╔══[ Isi dengan daftar menu ]\n" + \
				"╠ \n" + \
				"╠ \n" + \
				"╠ \n" + \
				"╠ \n" + \
				"╠ \n" + \
				"╠ \n" + \
				"╠ \n" + \
				"╠ \n" + \
				"╚══[ NRCT ]"
	return HelpMenu

def clientBot(op):
	try:
		#Anda bisa melihat optype di line/akad/ttypes.py | You can see the optype on line/akad/ttypes.py
		if op.type == 0: #Nothing ~
			print("[ 0 ] END OF OPERATION")
			return

		if op.type == 5:
			print("[ 5 ] NOTIFIED ADD CONTACT")
			if settings["autoAdd"] == True:
				client.findAndAddContactByMid(op.param1)
			client.sendMention(op.param1, settings["autoAddMessage"], [op.param1])

		if op.type == 13:
			print("[ 13 ] NOTIFIED INVITE INTO GROUP")
			if settings["autoJoin"] and clientMid in op.param1:
				client.acceptGroupInvitation(op.param1)
				client.sendMention(op.param1, settings["autoJoinMessage"], [op.param2])
			else:
				pass

		if op.type == 26: #26 == Menerima Pesan | Receive Message
			try:
				print("[ 26 ] RECEIVE MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				sender = msg._from
				contact = client.getContact(sender)
				pesandia = '%s [ %s ]' % (text, contact.displayName)
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if settings["autoRead"] == True:
							client.sendChatChecked(to, msg_id)
						if msg.text in ["Logout"]:
							if sender in settings["Pengurus"]["Admin"]:
								client.sendMessage(to, "Berhasil mematikan bot")
								sys.exit("[ INFO ] BOT SHUTDOWN")
								return
							else:
								client.sendMessage(to, "Access Denied")
						elif msg.text in ["Help","help","hElp","heLp","helP","HELP"]:
							helpMessage = HelpMenu()
							client.sendMessage(to, helpMessage)
#=======================================================================
#						elif msg.text in ["Jadwal piket lengkap"]:#Jadwal piket | Task schedule
#							TXT = "╔══[ %s ]" % ("Jadwal Piket")
#							num = 0
#							try:
#								TXT+= "\n╠══[ Senin ]"
#								for i in settings["JadwalPiket"]["Senin"]:
#									num+=1
#									TXT+="\n╠ [%s] %s" % (num, i)
#								num=0
#								TXT+= "\n╠══[ Selasa ]"
#								for i in settings["JadwalPiket"]["Selasa"]:
#									num+=1
#									TXT+="\n╠ [%s] %s" % (num, i)
#								num=0
#								TXT+= "\n╠══[ Rabu ]"
#								for i in settings["JadwalPiket"]["Rabu"]:
#									num+=1
#									TXT+="\n╠ [%s] %s" % (num, i)
#								num=0
#								TXT+= "\n╠══[ Kamis ]"
#								for i in settings["JadwalPiket"]["Kamis"]:
#									num+=1
#									TXT+="\n╠ [%s] %s" % (num, i)
#								num=0
#								TXT+= "\n╠══[ Jumat ]"
#								for i in settings["JadwalPiket"]["Jumat"]:
#									num+=1
#									TXT+="\n╠ [%s] %s" % (num, i)
#								num=0
#								TXT+= "\n╠══[ Sabtu ]"
#								for i in settings["JadwalPiket"]["Sabtu"]:
#									num+=1
#									TXT+="\n╠ [%s] %s" % (num, i)
#								num=0
#								TXT+="\n╚══[ X RPL 2 ]"
#								client.sendMessage(to, TXT)
#							except Exception as error:
#								client.log("[ ERROR ] : " + str(error))
#=======================================================================================
						elif msg.text in ["Jadwal lengkap"]:#Jadwal pelajaran | Schedules
							TXT = "╔══[ %s ]" % ("Jadwal Pelajaran")
							num = 0
							try:
								TXT+= "\n╠══[ Senin ]"
								for i in settings["Jadwal"]["Senin"]:
									num+=1
									TXT+="\n╠ [%s] %s" % (num, i)
								num=0
								TXT+= "\n╠══[ Selasa ]"
								for i in settings["Jadwal"]["Selasa"]:
									num+=1
									TXT+="\n╠ [%s] %s" % (num, i)
								num=0
								TXT+= "\n╠══[ Rabu ]"
								for i in settings["Jadwal"]["Rabu"]:
									num+=1
									TXT+="\n╠ [%s] %s" % (num, i)
								num=0
								TXT+= "\n╠══[ Kamis ]"
								for i in settings["Jadwal"]["Kamis"]:
									num+=1
									TXT+="\n╠ [%s] %s" % (num, i)
								num=0
								TXT+= "\n╠══[ Jumat ]"
								for i in settings["Jadwal"]["Jumat"]:
									num+=1
									TXT+="\n╠ [%s] %s" % (num, i)
								num=0
								TXT+= "\n╠══[ Sabtu ]"
								for i in settings["Jadwal"]["Sabtu"]:
									num+=1
									TXT+="\n╠ [%s] %s" % (num, i)
								num=0
								TXT+="\n╚══[ X RPL 2 ]"
								client.sendMessage(to, TXT)
							except Exception as error:
								client.log("[ ERROR ] : " + str(error))
#						elif msg.text in ["Jadwal piket besok"]:# Schedule assignments tomorrow
#							tz = pytz.timezone("Asia/Makassar")
#							timeNow = datetime.now(tz=tz)
#							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
#							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
#							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
#							hr = timeNow.strftime("%A")
#							bln = timeNow.strftime("%m")
#							for i in range(len(day)):
#								if hr == day[i]: hasil = hari[i]
#							for k in range(0, len(bulan)):
#								if bln == str(k): bln = bulan[k-1]
#							Hari = hasil
#							Jadwal(to, Hari, "Tommorow", "Piket")
						elif msg.text in ["Jadwal besok"]:#Tomorrow's schedule
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							Hari = hasil
							Jadwal(to, Hari, "Tommorow", "Pelajaran")
						elif msg.text in ["Jadwal"]:#Jadwal hari ini | Schedule today
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							Tanggal = hasil# + ", " + timeNow.strftime('%d')# + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							TXT = "╔══[ %s ]" % (Tanggal)
							num = 0
							try:
								if Tanggal == "Minggu":
									TXT+="\n╠ GK ADA YANG SEKOLAH WOI"
								else:
									for i in settings["Jadwal"][Tanggal]:
										num+=1
										TXT+="\n╠ [%s] %s" % (num, i)
								TXT+="\n╚══[ X RPL 2 ]"
								client.sendMessage(to, TXT)
							except Exception as error:
								client.log("[ ERROR ] : " + str(error))
#==========================================================================================
#						elif msg.text in ["Jadwal piket"]:
#							tz = pytz.timezone("Asia/Makassar")
#							timeNow = datetime.now(tz=tz)
#							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
#							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
#							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
#							hr = timeNow.strftime("%A")
#							bln = timeNow.strftime("%m")
#							for i in range(len(day)):
#								if hr == day[i]: hasil = hari[i]
#							for k in range(0, len(bulan)):
#								if bln == str(k): bln = bulan[k-1]
#							Tanggal = hasil# + ", " + timeNow.strftime('%d')# + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
#							TXT = "╔══[ %s ]" % (Tanggal)
#							num = 0
#							try:
#								if Tanggal == "Minggu":
#									TXT+="\n╠ "
#								else:
#									for i in settings["JadwalPiket"][Tanggal]:
#										num+=1
#										TXT+="\n╠ [%s] %s" % (num, i)
#								TXT+="\n╚══[ X RPL 2 ]"
#								client.sendMessage(to, TXT)
#							except Exception as error:
#								client.log("[ ERROR ] : " + str(error))
#==============================================================================================
						elif msg.text in ["Creator"]:
							client.Creator(to)
						elif "Spam " in msg.text:
							rep = msg.text.split(" ")
							jmlh = int(rep[2])
							teks = msg.text.replace("Spam "+str(rep[1])+" "+str(jmlh)+" ","")
							tulisan = jmlh * (teks+"\n")
							if rep[1] == "on":
								if jmlh <= 100000:
									for x in range(jmlh):
										client.sendMessage(to, teks)
								else:
									client.sendMessage(to, "Out Of Range!")
							elif rep[1] == "off":
								if jmlh <= 100000:
									client.sendMessage(to, tulisan)
								else:
									client.sendMessage(to, "Out Of Range!")
						elif msg.text in ["Restart"]:
							if sender in settings["Pengurus"]["Owner"]:
								client.sendMessage(to, "Berhasil mereset bot")
								RestartBot()
							else:
								client.sendMessage(to, "Access Denied")
						elif msg.text in ["Cek btc"]:
							check = requests.get('https://vip.bitcoin.co.id/api/btc_idr/ticker')
							data = check.text
							data = json.loads(data)
							last = data['ticker']['last']
							buy = data['ticker']['buy']
							sell = data['ticker']['sell']
							client.sendMessage(to, '[*] Harga bitcoin saat ini : Rp.%s/BTC\n[*] Harga Jual : Rp.%s/BTC\n[*] Harga Beli : Rp.%s/BTC\n' % (last, sell, buy))
						elif cmd == "speed":
							start = time.time()
							client.sendMessage(to, "Menghitung kecepatan...")
							elapsed_time = time.time() - start
							client.sendMessage(to, "Kecepatan mengirim pesan {} detik".format(str(elapsed_time)))
						elif cmd == "runtime":
							timeNow = time.time()
							runtime = timeNow - clientStart
							runtime = timeChange(runtime)
							client.sendMessage(to, "Bot telah aktif selama {}".format(str(runtime)))
						elif "!Add " in msg.text:
							if sender in settings["Pengurus"]["Owner"]:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									lists = []
									for mention in mentionees:
										if mention['M'] not in lists:
											lists.append(mention["M"])
									for ls in lists:
										try:
											settings["Pengurus"]["Admin"][ls] = True
											client.sendMessage(to, "Berhasil menambahkan Admin")
										except Exception as error:
											client.sendMessage(to, "Gagal menambahkan Admin "+str(error))
							else:
								client.sendMessage(to, "Hanya owner yang bisa menambahkan Admin")
						elif "Del " in msg.text:
							if sender in settings["Pengurus"]["Owner"]:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									lists = []
									for mention in mentionees:
										if mention['M'] not in lists:
											lists.append(mention["M"])
									for ls in lists:
										try:
											if ls not in settings["Pengurus"]["Admin"]:
												client.sendMessage(to, "Bukan Admin")
											else:
												del settings["Pengurus"]["Admin"][ls]
												client.sendMessage(to, "Berhasil menghapus Admin")
										except Exception as error:
											client.sendMessage(to, "Gagal menghapus Admin "+str(error))
							else:
								client.sendMessage(to, "Hanya Owner yang bisa menghapus Admin")
						elif msg.text in ["AmidG"]:
							if sender in settings["Pengurus"]["Admin"]:
								gid = client.getGroupIdsJoined()
								h = ""
								for i in gid:
									h += "[ %s ] : %s\n" % (client.getGroup(i).name, i)
								client.sendMessage(sender, h)
								client.log(h)
			except Exception as error:
				logError(error)
		if op.type == 25: # Mengirim Pesan | Send Message
			try:
				print("[ 25 ] SEND MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from #Use your creativity
				if msg.text in ["Test"]:
					print("TEST")
				elif msg.text in ["Bla bla bla"]:
					client.sendMessage(to, "Kreasikan sendiri WOE")
				elif msg.text in ["Haha"]:
					client.sendMessage(to, "Cape ngetiknya WOE")
			except Exception as error:
				logError(error)
		backupData()
	except Exception as error:
		logError(error)

def Checktime():
	tz = pytz.timezone("Asia/Makassar")
	timeNow = datetime.now(tz=tz)
	day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
	hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
	bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
	hr = timeNow.strftime("%A")
	bln = timeNow.strftime("%m")
	for i in range(len(day)):
		if hr == day[i]: hasil = hari[i]
	for k in range(0, len(bulan)):
		if bln == str(k): bln = bulan[k-1]
	Jam = timeNow.strftime('%H:%M:%S')
	Hari = hasil
	Result = "%s" % (Jam)
	if Result == "19:00:00":
		Jadwal(RPL2, Hari, "Tommorow", "Pelajaran")
	if Result == "05:00:00":
		Jadwal(RPL2, Hari, "Now", "Pelajaran")
#		Jadwal(RPL2, Hari, "Now", "Piket")

def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
					Checktime()
				except Exception as error:
					logError(error)
				clientPoll.setRevision(op.revision)
if __name__ == "__main__":
	run()

#Gunakanlah dengan bijak
#Use it wisely