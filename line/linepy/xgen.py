from datetime import datetime
from .object import Object
from .talk import Talk
from random import randint
import json, shutil, time, os, base64, tempfile
start = time.time()
class Modules(object):
	def __init__(self):
		Object.__init__(self)
	"""System"""
	def restart_program(self):
		python = sys.executable
		line.sendMessage(receiver,"Bot Restarted")
		os.execl(python, python, * sys.argv)
		return
	def Ls(self, path):
		files = os.listdir(path)
		no=1
		border=" ════════ List File ════════"
		for file in files:
			border+="\n [%i] %s" % (no, file)
			no=(no+1)
		border+="\n ════════ List File ════════\n Total files : %i" % len(file)
		return self.sendMessage(msg.to, border)
	def AmidG(self, to):
		gid = self.getGroupIdsJoined()
		h = ""
		for i in gid:
			h += "[%s]: %s\n" % (self.getGroup(i).name,i)
		self.log("[ Memeriksa daftar group ] : Executed")
		return self.log(h)
	def Time(secs):
		mins, secs = divmod(secs,60)
		hours, mins = divmod(mins,60)
		return '%02d Jam %02d Menit %02d Detik' % (hours, mins, secs)
	def runtime():
		elapsed_time = time.time() - start
		lol = "╭[Runtime]\n"
		lol += "╰[ "+Time(elapsed_time)+"]"
		line.sendMessage(msg.to,lol)