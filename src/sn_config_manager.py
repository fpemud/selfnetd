#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import pyinotify
from gi.repository import GObject

class SnCfgPeer:
	hostname = ""
	publicKey = ""

class SnPeerInfo:
	name = ""
	publicKey = ""
	arch = ""
	coreNumber = -1

class SnPeerInfoUser:
	name = ""
	publicKey = ""

class SnPeerInfoService:
	name = ""

class SnService:
	user = ""
	name = ""

class SnConfigManager(GObject.GObject):
	"""/etc/self-net
	    |----key
	          |----rsa-key-public.pem			# mode 644
	          |----rsa-key-private.pem			# mode 600
	    |----peers
	          |----HOSTNAME1
	                |----rsa-key-public.pem
	          |----HOSTNAME2
	                |----rsa-key-public.pem"""

	__gsignals__ = {
		'cfg_peer_add': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()),
		'cfg_peer_delete': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()),
		'local_info_changed': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()),
		'service_add': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()),
		'service_delete': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()),
	}

	def __init__(self, param):
		GObject.GObject.__init__(self)

		self.param = param
		self.listenPort = 2107
		self.publicKey = ""
		self.localInfo = None
		self.peerList = []
		self.serviceDict = dict()

	def init(self):
		# create local info
		self.localInfo = SnPeerInfo()

		# add all peers
		for f in os.listdir(os.path.join(self.param.cfgDir, "peers")):
			pobj = SnCfgPeer()
			pobj.hostname = f
			pobj.publicKey = ""
			self.peerList.append(pobj)

	def getPort(self):
		return self.listenPort

	def getLocalInfo(self):
		return self.localInfo

	def getCfgPeerList(self):
		"""Returns SnCfgPeer object list"""

		return self.peerList

	def getCfgPeer(self, peerName):
		"""Returns SnCfgPeer object"""

		for item in self.peerList:
			if item.hostname == peerName:
				return item
		assert False

	def addService(self, userName, serviceName, serviceObj):
		key = (userName, serviceName)
		assert key not in self.serviceDict
		self.serviceDict[key] = serviceObj

	def removeService(self, userName, serviceName):
		key = (userName, serviceName)
		self.serviceDict.remove(key)

	def getService(self, userName, serviceName):
		key = (userName, serviceName)
		assert key in self.serviceDict
		self.serviceDict[key]


GObject.type_register(SnConfigManager)

