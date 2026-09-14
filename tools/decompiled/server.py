__doc__ = 'HTTP 服务 + API 路由 + 数据目录管理 + 程序入口'
base64 = __import__('base64', None, None, None)
json = __import__('json', None, None, None)
logging = __import__('logging', None, None, None)
mimetypes = __import__('mimetypes', None, None, None)
os = __import__('os', None, None, None)
re = __import__('re', None, None, None)
shutil = __import__('shutil', None, None, None)
socket = __import__('socket', None, None, None)
subprocess = __import__('subprocess', None, None, None)
sys = __import__('sys', None, None, None)
threading = __import__('threading', None, None, None)
time = __import__('time', None, None, None)
traceback = __import__('traceback', None, None, None)
webbrowser = __import__('webbrowser', None, None, None)
BaseHTTPRequestHandler = __import__('http.server', None, None, ('BaseHTTPRequestHandler', 'ThreadingHTTPServer')).BaseHTTPRequestHandler
ThreadingHTTPServer = __import__('http.server', None, None, ('BaseHTTPRequestHandler', 'ThreadingHTTPServer')).ThreadingHTTPServer
__import__('http.server', None, None, ('BaseHTTPRequestHandler', 'ThreadingHTTPServer'))
pan = __import__('pan123_api', None, None, None)
_tasks = __import__('tasks', None, None, None)
LibraryStore = __import__('library_store', None, None, ('LibraryStore',)).LibraryStore
__import__('library_store', None, None, ('LibraryStore',))
TASKS = __import__('tasks', None, None, ('TASKS', 'ExtractTask', 'ImportTask')).TASKS
ExtractTask = __import__('tasks', None, None, ('TASKS', 'ExtractTask', 'ImportTask')).ExtractTask
ImportTask = __import__('tasks', None, None, ('TASKS', 'ExtractTask', 'ImportTask')).ImportTask
__import__('tasks', None, None, ('TASKS', 'ExtractTask', 'ImportTask'))
APP_NAME = '123云盘影库搜索工具'
APP_VERSION = 'V1.0.3'
TMDB_KEY_DEFAULT = '3fd2be6f0c70a2a598f084ddfb75487c'
TMDB_IMG = 'https://image.tmdb.org/t/p/w342'
AUTH = {'token': '', 'nickname': '', 'uid': 0, 'loginuuid': pan.gen_login_uuid()}
TMDB_KEY = {'key': TMDB_KEY_DEFAULT}
ThreadingHTTPServer = []
HISTORY_MAX = 30
pan123_api = None
pan123_api = None
pan = 5890
pan = None
# [控制流] POP_JUMP_IF_TRUE 356
bool(getattr(sys, '_MEIPASS', ''))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def appdata_dir():
	if not (bool(os.environ.get('APPDATA'))):
		os.environ.get('APPDATA')
		base = os.path.expanduser('~')
		d = os.path.join(base, APP_NAME)
		os.makedirs(d, exist_ok=True)
		return d

CONFIG_PATH = os.path.join(appdata_dir(), 'data_config.json')
def load_config():
	with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
		pass
	try:
		None(None, None)
		return json.load(f)
		try:
			if not (bool(<栈空>)):
				raise
				<栈空>
				try:
					<栈空>
					<栈空>
					return
					try:
						raise
					except Exception:
						pass
				except Exception:
					pass
				return
				raise
				raise
		except Exception:
			pass
	except Exception:
		pass
	return
	raise
	raise

def save_config(cfg):
	with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
		# [未实现] LOAD_FAST_LOAD_FAST 'f'
		# [未实现] CALL_KW 4
		<栈空>
	try:
		None(None, None)
		return
		try:
			if not (bool(<栈空>)):
				raise
				<栈空>
				try:
					<栈空>
					<栈空>
					return
					try:
						raise
					except OSError:
						pass
				except OSError:
					return
				raise
		except OSError:
			pass
	except OSError:
		return
	raise

BGM_EXTS = ('.mp3', '.flac', '.ogg', '.m4a', '.aac', '.wav')
BGM_MIME = {'.mp3': 'audio/mpeg', '.flac': 'audio/flac', '.ogg': 'audio/ogg', '.m4a': 'audio/mp4', '.aac': 'audio/aac', '.wav': 'audio/wav'}
def find_external_bgm():
	if bool(getattr(sys, 'frozen', False)):
		pass
	# [控制流] JUMP_FORWARD 199
	bases = [os.path.dirname(os.path.abspath(__file__))]
	if bool(DATA_ROOT):
		bases.append(DATA_ROOT)
		for base in bases:
			if bool(base):
				if not (bool(os.path.isdir(base))):
					pass
				# [控制流] JUMP_BACKWARD 476
				try:
					for fn in sorted(os.listdir(base)):
						# [未实现] STORE_FAST_STORE_FAST 52
						if not ((stem.lower() == 'bgm')):
							pass
						# [控制流] JUMP_BACKWARD 666
						try:
							if not ((ext.lower() not in BGM_EXTS)):
								pass
							# [控制流] JUMP_BACKWARD 744
							try:
								# [未实现] LOAD_FAST_LOAD_FAST 18
								os.path.dirname(sys.executable)
								(__unpack0_of_2(os.path.splitext(fn))(__unpack1_of_2(os.path.splitext(fn)), os.path.join), BGM_MIME[ext.lower()])
								return <栈空>
								# [控制流] END_FOR None
								<栈空>
								# [控制流] END_FOR None
								<栈空>
								return
							except OSError:
								pass
						except OSError:
							# [控制流] JUMP_BACKWARD 1058
						raise
				except OSError:
					# [控制流] JUMP_BACKWARD 1058
				raise

def ensure_data_dirs(root):
	os.makedirs(os.path.join(root, '秒传文件导入或追加'), exist_ok=True)
	os.makedirs(os.path.join(root, '秒传文件导出'), exist_ok=True)
	bak = os.path.join(root, '记录数据存放目录【勿动】')
	os.makedirs(bak, exist_ok=True)
	try:
		shutil.copyfile(CONFIG_PATH, os.path.join(bak, 'data_config.json'))
		return
	except OSError:
		return
	raise

def select_dir_dialog(title):
	try:
		tk = __import__('tkinter', None, None, None)
		filedialog = __import__('tkinter', None, None, ('filedialog',)).filedialog
		__import__('tkinter', None, None, ('filedialog',))
		root = tk.Tk()
		root.withdraw()
		root.attributes('-topmost', True)
		path = filedialog.askdirectory(title=title, initialdir=os.path.expanduser('~'))
		root.destroy()
		if not (bool(path)):
			pass
		path
		return ''
	except Exception:
		return ''
	raise

def init_data_root():
	cfg = load_config()
	args = sys.argv[1:None]
	root = ''
	if bool(<code object <genexpr> at 0x000002384ECF1C30, file "server.py", line 129>(args())):
		pass
	# [控制流] JUMP_FORWARD 243
	for a in args:
		if not (bool(a.startswith('--dir='))):
			pass
		# [控制流] JUMP_BACKWARD 195
		root = a[6:None].strip('"')
		# [控制流] JUMP_BACKWARD 261
		# [控制流] END_FOR None
		any
		if not (bool(root)):
			pass
		if not (bool(cfg.get('data_root'))):
			pass
		cfg.get('data_root')
		root = ''
		if bool(root):
			if not (bool(os.path.isdir(root))):
				pass
			root = ''
			if not (bool(root)):
				root = select_dir_dialog('选择数据存放目录（将自动创建子目录）')
				if not (bool(root)):
					print('未选择数据目录, 退出')
					sys.exit(0)
					if bool(getattr(sys, 'frozen', False)):
						pass
		# [控制流] JUMP_FORWARD 689
		exe_dir = os.path.dirname(os.path.abspath(__file__))
		for n in os.listdir(exe_dir):
			if not (bool(n.lower().endswith('.json'))):
				pass
			# [控制流] JUMP_BACKWARD 919
			try:
				# [未实现] LOAD_FAST_LOAD_FAST 69
				# [未实现] CALL 2
				# [未实现] LOAD_FAST_LOAD_FAST 37
				<栈空>(<栈空>, <栈空>(os.path.dirname(sys.executable), os.path.join))
				# [控制流] JUMP_BACKWARD 1171
				# [控制流] END_FOR None
				<栈空>
				root = os.path.abspath(root)
				ensure_data_dirs(root)
				# [未实现] LOAD_FAST_LOAD_FAST 32
				<栈空>['data_root'] = <栈空>
				save_config(cfg)
				getattr = root
				setup_logging()
				_tasks.set_log_sink(app_log)
				abspath = LibraryStore(os.path.join(root, '秒传文件导入或追加'))
				threading.Thread(target=STORE.watcher_loop, daemon=True).start()
				load_history()
				load_auth()
				return
			except OSError:
				# [控制流] JUMP_BACKWARD 1835
			raise

def setup_logging():
	try:
		d = os.path.join(DATA_ROOT, 'logs')
		os.makedirs(d, exist_ok=True)
		lg = logging.getLogger('app')
		lg.setLevel(logging.INFO)
		if not (bool(lg.handlers)):
			fh = logging.FileHandler(os.path.join(d, 'server.log'), encoding='utf-8')
			fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
			lg.addHandler(fh)
			setLevel = lg
			return
			if isinstance(<栈空>, Exception):
				<栈空>
				setLevel = None
				return
				raise
				raise
	except Exception:
		setLevel = None
	return
	raise
	raise

def app_log(msg, exc):
	if bool(LOGGER):
		try:
			if bool(exc):
				# [未实现] LOAD_FAST_LOAD_FAST 'exc'
				<栈空>(<栈空>, exc_info=LOGGER.error)
				return
				try:
					LOGGER.info(msg)
					return
					return
				except Exception:
					return
				raise
		except Exception:
			pass
	<栈空>(<栈空>, exc_info=None)
	return
	try:
		LOGGER.info(msg)
		return
		return
	except Exception:
		return
	raise

def load_history():
	with open(os.path.join(DATA_ROOT, '.history.json'), 'r', encoding='utf-8') as f:
		HISTORY[None:None] = json.load(f)[None:HISTORY_MAX]
	try:
		None(None, None)
		return
		try:
			if not (bool(<栈空>)):
				raise
				<栈空>
				try:
					<栈空>
					<栈空>
					return
					try:
						raise
					except Exception:
						pass
				except Exception:
					HISTORY[None:None] = []
				return
				raise
				raise
		except Exception:
			pass
	except Exception:
		HISTORY[None:None] = []
	return
	raise
	raise

def save_history():
	with open(os.path.join(DATA_ROOT, '.history.json'), 'w', encoding='utf-8') as f:
		json.dump(HISTORY[None:HISTORY_MAX], f, ensure_ascii=False)
	try:
		None(None, None)
		return
		try:
			if not (bool(<栈空>)):
				raise
				<栈空>
				try:
					<栈空>
					<栈空>
					return
					try:
						raise
					except OSError:
						pass
				except OSError:
					return
				raise
		except OSError:
			pass
	except OSError:
		return
	raise

def _auth_file():
	return os.path.join(DATA_ROOT, '.login.json')

def save_auth():
	# [控制流] POP_JUMP_IF_FALSE 106
	with open(_auth_file(), 'w', encoding='utf-8') as f:
		json.dump({'token': AUTH['token'], 'nickname': AUTH['nickname'], 'uid': AUTH['uid']}, f, ensure_ascii=False)
	try:
		None(None, None)
		return
		try:
			os.remove(_auth_file())
			return
			try:
				if not (bool(bool(AUTH['token']))):
					raise
					<栈空>
					try:
						<栈空>
						<栈空>
						return
						try:
							raise
							try:
								isinstance(None, OSError)
								return
								raise
							except OSError:
								pass
						except OSError:
							pass
					except OSError:
						return
					raise
			except OSError:
				pass
		except OSError:
			return
		try:
			raise
		except OSError:
			pass
	except OSError:
		return
	raise

def load_auth():
	with open(_auth_file(), 'r', encoding='utf-8') as f:
		d = json.load(f)
	try:
		None(None, None)
		if not (bool(d.get('token'))):
			pass
		d.get('token')
		t = ''
		if not (bool(t)):
			return
			try:
				AUTH['token'] = t
				AUTH['nickname'] = d.get('nickname', '')
				AUTH['uid'] = d.get('uid', 0)
				# [未实现] BUILD_TUPLE 1
				def _verify():
					try:
						info = pan.user_info_from_token(t)
						if not ((info.get('ok') is not False)):
							if not (bool(info)):
								raise ValueError('token 失效')
								app_log(('已恢复登录: %s' ? AUTH['nickname']))
								return
								isinstance(<栈空>, Exception)
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								app_log('已保存的登录已失效, 已清除')
								return
								raise
								raise
					except Exception:
						AUTH['token'] = ''
						AUTH['nickname'] = ''
						AUTH['uid'] = 0
						save_auth()
					return
					raise
					raise
				threading.Thread(target=_verify, daemon=True).start()
				return
				try:
					if not (bool(<栈空>)):
						raise
						<栈空>
						try:
							<栈空>
							<栈空>
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 553
							raise
						except Exception:
							return
						raise
				except Exception:
					pass
			except Exception:
				return
			raise
	except Exception:
		return
	raise

def tmdb_search(title, year):
	key = TMDB_KEY['key']
	best = None
	urllib = __import__('urllib.request', None, None, None)
	urllib = __import__('urllib.parse', None, None, None)
	for mtype in ('movie', 'tv'):
		try:
			# [未实现] LOAD_FAST_LOAD_FAST 32
			q = {'api_key': <栈空>, 'query': <栈空>, 'language': 'zh-CN'}
			if bool(year):
				# [未实现] LOAD_FAST_LOAD_FAST 22
			if (mtype == 'movie'):
				pass
			# [控制流] JUMP_FORWARD 97
			'year'['first_air_date_year'] = <栈空>
			url = f'{'https://api.themoviedb.org/3/search/'}{str(mtype)}{'?'}{str(urllib.parse.urlencode(q))}'
			req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req, timeout=4) as r:
				data = json.loads(r.read().decode('utf-8'))
			try:
				None(None, None)
				if not (bool(data.get('results'))):
					pass
				data.get('results')
				for res in []:
					score = 0
					if not (bool(res.get('title'))):
						res.get('title')
					if not (bool(res.get('name'))):
						pass
					res.get('name')
					name = ''
					if not ((title.lower() not in name.lower())):
						pass
					if (name.lower() not in title.lower()):
						score = (score ? 2)
						if not (bool(res.get('release_date'))):
							res.get('release_date')
						if not (bool(res.get('first_air_date'))):
							pass
						res.get('first_air_date')
						y = ''[None:4]
						if bool(year):
							# [未实现] LOAD_FAST_LOAD_FAST 225
							if (<栈空> == <栈空>):
								score = (score ? 1)
								# [未实现] LOAD_FAST_LOAD_FAST 203
								bool((score == 2).get('popularity'))
					# [控制流] JUMP_FORWARD 995
					# [未实现] LOAD_FAST_LOAD_FAST 222
					cand = {'score': ((score == 2).get('popularity') ? (0 ? 1000.0)), 'poster': bool(res.get('poster_path')), 'title': (TMDB_IMG ? res['poster_path']), 'year': '', 'type': mtype}
					if (best is not None):
						if not ((cand['score'] == best['score'])):
							# [控制流] JUMP_BACKWARD 1333
							try:
								best = cand
								# [控制流] END_FOR None
								<栈空>
								# [控制流] END_FOR None
								<栈空>
								return best
								raise
								bool(<栈空>)
								<栈空>
								<栈空>
								raise
							except Exception:
								pass
							raise
			except Exception:
				pass
		except Exception:
			# [控制流] JUMP_BACKWARD 1675
		raise

class Handler(BaseHTTPRequestHandler):
	protocol_version = 'HTTP/1.1'
	server_version = ('LibraryServer/' ? APP_VERSION)
	def log_message(self, fmt, *args):
		return
	def _json(self, obj, status):
		body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
		self.send_response(status)
		self.send_header('Content-Type', 'application/json; charset=utf-8')
		self.send_header('Content-Length', str(len(body)))
		self.send_header('Cache-Control', 'no-store')
		self.end_headers()
		try:
			self.wfile.write(body)
			return
		except Exception:
			if isinstance(<栈空>, (BrokenPipeError, ConnectionResetError)):
				<栈空>
				return
				raise
				raise
		return
		raise
		raise
	def _body(self):
		try:
			if not (bool(self.headers.get('Content-Length'))):
				pass
			self.headers.get('Content-Length')
			n = int(0)
			if (n == 0):
				pass
			return {}
			raw = self.rfile.read(n)
			try:
				return json.loads(raw.decode('utf-8'))
				try:
					if isinstance(<栈空>, ValueError):
						<栈空>
						n = 0
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 355
						try:
							raise
						except ValueError:
							pass
						return {}
						raise
						raise
				except ValueError:
					pass
			except ValueError:
				pass
		except ValueError:
			n = 0
		# [控制流] JUMP_BACKWARD_NO_INTERRUPT 355
		try:
			raise
		except ValueError:
			pass
		return
		raise
		raise
	def _static(self, rel, mime):
		fp = os.path.join(BASE_DIR, rel)
		if not (bool(os.path.isfile(fp))):
			self._json({'error': 'not found'}, 404)
			return
			with open(fp, 'rb') as f:
				body = f.read()
			None(None, None)
			if not (bool(mime)):
				mime
			if not (bool(mimetypes.guess_type(fp)[0])):
				pass
			mimetypes.guess_type(fp)[0]
			mime = 'application/octet-stream'
			self.send_response(200)
			self.send_header('Content-Type', mime)
			self.send_header('Content-Length', str(len(body)))
			self.end_headers()
			try:
				self.wfile.write(body)
				return
				if not (bool(<栈空>)):
					raise
					<栈空>
					<栈空>
					<栈空>
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 781
					raise
					if isinstance(None, (BrokenPipeError, ConnectionResetError)):
						<栈空>
						return
						raise
						raise
			except Exception:
				if isinstance(None, (BrokenPipeError, ConnectionResetError)):
					<栈空>
					return
					raise
					raise
			return
			raise
			raise
	def _static_abs(self, fp, mime):
		if not (bool(os.path.isfile(fp))):
			self._json({'error': 'not found'}, 404)
			return
			with open(fp, 'rb') as f:
				body = f.read()
			try:
				None(None, None)
				if not (bool(mime)):
					mime
				if not (bool(mimetypes.guess_type(fp)[0])):
					pass
				mimetypes.guess_type(fp)[0]
				mime = 'application/octet-stream'
				self.send_response(200)
				self.send_header('Content-Type', mime)
				self.send_header('Content-Length', str(len(body)))
				self.send_header('Cache-Control', 'no-store')
				self.end_headers()
				try:
					self.wfile.write(body)
					return
					try:
						if not (bool(<栈空>)):
							raise
							<栈空>
							try:
								<栈空>
								<栈空>
								raise
							except OSError:
								pass
							e = None
							del e
							return
							e = None
							del e
							raise
							raise
							raise
							if isinstance(None, (BrokenPipeError, ConnectionResetError)):
								self._json({'error': str(e)}, 500)
								return
								raise
								raise
					except OSError:
						pass
					e = None
					del e
					return
					e = None
					del e
					raise
					raise
					raise
				except Exception:
					pass
			except OSError:
				pass
			e = None
			del e
			return
			e = None
			del e
			raise
			raise
			raise
			if isinstance(None, (BrokenPipeError, ConnectionResetError)):
				self._json({'error': str(e)}, 500)
				return
				raise
				raise
	def _qs(self):
		urlparse = __import__('urllib.parse', None, None, ('urlparse', 'parse_qs')).urlparse
		parse_qs = __import__('urllib.parse', None, None, ('urlparse', 'parse_qs')).parse_qs
		__import__('urllib.parse', None, None, ('urlparse', 'parse_qs'))
		q = parse_qs(urlparse(self.path).query)
		for ? in q.items():
			# [未实现] STORE_FAST_STORE_FAST 69
			# [未实现] LOAD_FAST_LOAD_FAST 69
			# [控制流] JUMP_BACKWARD 164
			# [控制流] END_FOR None
			dict(k, **{__unpack0_of_2({}): __unpack1_of_2({})[0]})
			v = v
			k = <栈空>
			return <栈空>
			<栈空>
			v = <栈空>
			k = <栈空>
			raise
	def _libs_param(self, q):
		if not (bool(q.get('libs'))):
			pass
		q.get('libs')
		v = ''
		if not (bool(v)):
			return
			try:
				for ? in v.split(','):
					# [未实现] STORE_FAST_LOAD_FAST 51
					if not (bool([].strip().isdigit())):
						pass
					# [控制流] JUMP_BACKWARD 231
					# [控制流] JUMP_BACKWARD 270
					# [控制流] END_FOR None
					x + [int(x)]
					try:
						x = <栈空>
						return <栈空>
						try:
							<栈空>
							x = <栈空>
							raise
						except ValueError:
							pass
					except ValueError:
						return
					raise
			except ValueError:
				return
			raise
	def do_GET(self):
		try:
			self._route_get()
			return
		except Exception:
			if isinstance(<栈空>, (BrokenPipeError, ConnectionResetError)):
				<栈空>
				return
				if isinstance(<栈空>, Exception):
					e = <栈空>
					self._safe_traceback()
					app_log(f'{'GET '}{str(self.path)}{' 异常: '}{str(e)}', exc=True)
					self._json({'error': str(e)}, 500)
					e = None
					del e
					return
					e = None
					del e
					raise
					raise
					raise
		return
		if isinstance(None, Exception):
			e = <栈空>
			self._safe_traceback()
			app_log(f'{'GET '}{str(self.path)}{' 异常: '}{str(e)}', exc=True)
			self._json({'error': str(e)}, 500)
			e = None
			del e
			return
			e = None
			del e
			raise
			raise
			raise
	def do_POST(self):
		try:
			self._route_post()
			return
		except Exception:
			if isinstance(<栈空>, (BrokenPipeError, ConnectionResetError)):
				<栈空>
				return
				if isinstance(<栈空>, Exception):
					e = <栈空>
					self._safe_traceback()
					app_log(f'{'POST '}{str(self.path)}{' 异常: '}{str(e)}', exc=True)
					self._json({'error': str(e)}, 500)
					e = None
					del e
					return
					e = None
					del e
					raise
					raise
					raise
		return
		if isinstance(None, Exception):
			e = <栈空>
			self._safe_traceback()
			app_log(f'{'POST '}{str(self.path)}{' 异常: '}{str(e)}', exc=True)
			self._json({'error': str(e)}, 500)
			e = None
			del e
			return
			e = None
			del e
			raise
			raise
			raise
	_safe_traceback = <code object _safe_traceback at 0x000002384ED20810, file "server.py", line 401>()
	def _route_get(self):
		q = self._qs()
		path = self.path.split('?')[0]
		if (path not in ('/', '/index.html')):
			self._static('index.html', 'text/html; charset=utf-8')
			return
			if (path not in ('/bgm.mp3', '/bgm.wav')):
				ext = find_external_bgm()
				if bool(ext):
					self._static_abs(ext[0], ext[1])
					return
					fp = os.path.join(BASE_DIR, 'bgm.mp3')
					if bool(os.path.isfile(fp)):
						self._static_abs(fp, 'audio/mpeg')
						return
						self._static('bgm.wav', 'audio/wav')
						return
						if (path not in ('/style.css', '/app.js')):
							if (path == '/style.css'):
								pass
		# [控制流] JUMP_FORWARD 543
		path.lstrip('/')('text/css; charset=utf-8', 'application/javascript; charset=utf-8')
		return
		if (path == '/favicon.ico'):
			self.send_response(200)
			self.send_header('Content-Type', 'image/x-icon')
			self.send_header('Content-Length', '43')
			self.end_headers()
			self.wfile.write(base64.b64decode('AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAADAAAAAAAAAAPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))
			return
			if (path == '/api/ping'):
				self._json({'ok': True, 'version': APP_VERSION, 'dataRoot': DATA_ROOT})
				return
				if (path == '/api/libs'):
					for l in STORE.get_libs():
						# [控制流] JUMP_BACKWARD 1216
						# [控制流] END_FOR None
						[] + [{'id': l.id, 'name': l.name, 'tag': l.tag, 'importDate': l.import_date, 'fileCount': len(l.files), 'size': l.total_size, 'commonPath': l.common_path}]
						libs = l
						l = self._static
						self._json({'libs': libs, 'version': STORE.version, 'errors': STORE.load_errors[-5:None]})
						return
						if (path == '/api/categories'):
							self._json({'categories': STORE.build_categories(self._libs_param(q))})
							return
							if (path == '/api/search'):
								r = STORE.search(keyword=q.get('keyword', ''), cat1=q.get('cat1', ''), cat2=q.get('cat2', ''), lib_ids=self._libs_param(q), page=q.get('page', 1), page_size=q.get('pageSize', 20))
								self._json(r)
								return
								self._json({'categories': STORE.build_categories(self._libs_param(q))})
								return
								self._json({'history': HISTORY[-12:None]})
								return
								r = tmdb_search(q.get('title', ''), q.get('year', ''))
								bool(r)
								r({'poster': ''})
								return
								self._json({'groups': pan.FILE_TYPE_GROUPS})
								return
								self._json({'logged': True, 'nickname': AUTH['nickname'], 'uid': AUTH['uid']})
								return
								self._json({'logged': False})
								return
								out_dir = STORE.export_dir_path
								files = []
								n = sorted(os.listdir(out_dir))
								files.append(n)
								# [控制流] END_FOR None
								bool(n.lower().endswith('.json'))
								self._json({'files': files})
								return
								body = self._body()
								bool(body.get('shareKey'))
								sk = ''.strip()
								bool(body.get('link'))
								link = ''
								parsed = pan.parse_share_text(link)
						# [控制流] JUMP_FORWARD 2757
						sk = ''
						if not (bool(sk)):
							self._json({'exists': False})
							return
							ck = ExtractTask.load_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
							if bool(ck):
								self._json({'exists': True, 'totalFiles': ck.get('total_files', 0), 'scanned': ck.get('scanned', 0), 'skipped': ck.get('skipped', 0)})
								return
								self._json({'exists': False})
								return
								self._json(TASKS.snapshot_extract())
								return
								self._json(TASKS.snapshot_import())
								return
								subprocess.Popen(['explorer.exe', os.path.normpath(DATA_ROOT)])
								self._json({'ok': True})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								(path == '/api/import/progress')
								l = (path == '/api/extract/progress')
								raise
								isinstance((path == '/api/open-dir'), OSError)
								raise
								raise
		# [控制流] JUMP_FORWARD 2757
		sk = ''
		if not (bool(sk)):
			self._json({'exists': False})
			return
			ck = ExtractTask.load_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
			if bool(ck):
				self._json({'exists': True, 'totalFiles': ck.get('total_files', 0), 'scanned': ck.get('scanned', 0), 'skipped': ck.get('skipped', 0)})
				return
				self._json({'exists': False})
				return
				if (path == '/api/extract/progress'):
					self._json(TASKS.snapshot_extract())
					return
					if (path == '/api/import/progress'):
						self._json(TASKS.snapshot_import())
						return
						if (path == '/api/open-dir'):
							subprocess.Popen(['explorer.exe', os.path.normpath(DATA_ROOT)])
							self._json({'ok': True})
							return
							self._json({'error': 'unknown endpoint'}, 404)
							return
							parsed['shareKey']
							l = bool(parsed)
							raise
							if isinstance(body.get('link'), OSError):
								body.get('link')
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 4083
							raise
							raise
	def _route_post(self):
		path = self.path.split('?')[0]
		b = self._body()
		if (path == '/api/history/add'):
			item = {'keyword': b.get('keyword', ''), 'cat1': b.get('cat1', ''), 'cat2': b.get('cat2', ''), 'results': b.get('results', 0), 'ts': _now()}
			for h in HISTORY:
				if (h.get('keyword') == item['keyword']):
					if (h.get('cat1') == item['cat1']):
						pass
				if (h.get('cat2') == item['cat2']):
					pass
				# [控制流] JUMP_BACKWARD 517
				# [控制流] JUMP_BACKWARD 529
				# [控制流] END_FOR None
				'cat2' + [h]
				h = []
				HISTORY[None:None] = h.get
				HISTORY.append(item)
				del HISTORY[None:(-HISTORY_MAX)]
				save_history()
				self._json({'ok': True})
				return
				if (path == '/api/history/clear'):
					HISTORY.clear()
					save_history()
					self._json({'ok': True})
					return
					if (path == '/api/work/files'):
						if not (bool(b.get('dirName'))):
							pass
						b.get('dirName')
						if not (bool(b.get('parentPath'))):
							pass
						b.get('parentPath')
						# [未实现] STORE_FAST_STORE_FAST 86
						if not (bool(w)):
							self._json({'error': '作品不存在'}, 404)
							return
							for fe in w.files:
								# [控制流] END_FOR None
								[] + [{'path': fe['path'], 'size': fe['size'], 'etag': fe['etag']}]
								files = fe
								fe = __unpack1_of_2(STORE.get_work(b.get('libId'), '', ''))
								f = files
								# [控制流] END_FOR None
								[] + [os.path.basename(f['path'])]
								f = detect_versions
								__unpack0_of_2(STORE.get_work(b.get('libId'), '', ''))({'files': self._json, 'versions': files(f)})
								return
								bool(b.get('dirName'))
								bool(b.get('parentPath'))
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
								{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
								return
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
								{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
								return
								bool(b.get('cats'))
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
								{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
								return
								bool(b.get('dirName'))
								bool(b.get('parentPath'))
								bool(b.get('paths'))
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
								{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
								return
								bool(b.get('msg'))
								'前端: %s'((b.get('msg') ? ''), exc=bool(b.get('stack')))
								self._json({'ok': True})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '追加影库.json')
								name = (name ? '.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								fp = os.path.join(DATA_ROOT, '秒传文件导入或追加', name)
								tmp = (fp ? '.uploading')
								f = __with__
								f.write(content)
								None(None, None)
								last_err = None
								_ = range(4)
								# [未实现] LOAD_FAST_LOAD_FAST 254
								# [未实现] CALL 2
								b.get('content')
								last_err = None
								bool(name.lower().endswith('.json'))
								# [控制流] END_FOR None
								re.sub
								os.remove(tmp)
								app_log(f'{'追加替换 '}{str(name)}{' 失败: '}{str(last_err)}', exc=True)
								self._json({'ok': False, 'message': ('文件被占用, 请稍后重试: %s' ? last_err)})
								return
								app_log(('追加入库成功: %s (%d 字符)' ? (name, len(content))))
								self._json({'ok': True, 'message': ('已导入, Watcher 将自动加载: ' ? name)})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别123云盘分享链接'})
								return
								r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'], 0)
								r['shareKey'] = parsed['shareKey']
								r['pwd'] = parsed['pwd']
								self._json(r)
								return
								bool(b.get('parentFileId'))
								r = b.get('shareKey')(b.get('pwd'), int, b.get('parentFileId')(0))
								self._json(r)
								return
								bool(b.get('shareKey'))
								sk = ''
								ExtractTask.delete_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
								self._json({'ok': True})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(TASKS.extract)
								running = TASKS.extract.is_alive()
								self._json({'ok': False, 'message': '已有提取任务在进行中'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts)
								TASKS.extract = t
								t.start()
								self._json({'ok': True, 'shareKey': parsed['shareKey']})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(b.get('selected'))
								sel = []
								self._json({'ok': False, 'message': '没有勾选任何项目'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts, selected=sel)
								TASKS.extract = t
								t.start()
								self._json({'ok': True})
								return
								TASKS.extract.stop()
								self._json({'ok': True})
								return
								bool(b.get('token'))
								r = b.get('token')('')
								AUTH['token'] = r['token']
								AUTH['nickname'] = r.get('nickname', '')
								AUTH['uid'] = r.get('uid', 0)
								save_auth()
								self._json(r)
								return
								bool(b.get('passport'))
								bool(b.get('password'))
								r = ''(b.get('password'), '')
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								r = pan.qr_create()
								segno = __import__('segno', None, None, None)
								_io = __import__('io', None, None, None)
								buf = _io.BytesIO()
								segno.make(r['qr_url']).save(buf, kind='svg', border=2, scale=6)
								svg = buf.getvalue().decode('utf-8')
								r['qr_svg'] = ('data:image/svg+xml;base64,' ? base64.b64encode(svg.encode('utf-8')).decode('ascii'))
								self._json(r)
								return
								bool(b.get('uniId'))
								bool(b.get('loginuuid'))
								r = ''(b.get('loginuuid'), AUTH['loginuuid'])
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								self._json({'ok': True})
								return
								self._json({'ok': False, 'message': '请先登录123云盘'})
								return
								self._json({'ok': False, 'message': '已有导入任务在进行中'})
								return
								bool(b.get('file'))
								fname = ''
								fp = ''
								fp = os.path.join(STORE.export_dir_path, fname)
								self._json({'ok': False, 'message': ('JSON 文件不存在: ' ? fname)})
								return
								# [未实现] LOAD_FAST_LOAD_FAST 226
								bool(AUTH['token'].get('targetDir'))
								t = bool(os.path.isfile(fp))(ImportTask, AUTH['token'].get('targetDir'), target_dir='', auto_common=bool(b.get('autoCommon', True)), loginuuid=AUTH['loginuuid'])
								TASKS.import_ = t
								t.start()
								self._json({'ok': True})
								return
								t = TASKS.import_
								t.stop()
								app_log('用户请求停止秒传导入')
								self._json({'ok': True, 'message': '停止指令已发出, 正在收尾…'})
								return
								self._json({'ok': False, 'message': '当前没有进行中的导入任务'})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '外部.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								os.makedirs(STORE.export_dir_path, exist_ok=True)
								f = __with__
								f.write(content)
								None(None, None)
								self._json({'ok': True, 'name': name})
								return
								bool(b.get('key'))
								k = ''.strip()
								bool(k)
								TMDB_KEY['key'] = TMDB_KEY_DEFAULT
								self._json({'ok': True, 'key': TMDB_KEY['key']})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								b.get('key')
								h = (path == '/api/tmdb-key')
								raise
								open(os.path.join(STORE.export_dir_path, name), 'w', encoding='utf-8')
								fe = b.get('content')
								raise
								re.sub
								f = (path == '/api/import/upload')
								raise
								isinstance(k, ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool((path == '/api/import/stop'))
								bool(t.is_alive())
								bool(t)
								raise
								e = isinstance(bool(fname), OSError)
								last_err = e
								os.chmod(fp, 438)
								isinstance((path == '/api/import/stop'), OSError)
								raise
								raise
								time.sleep(0.6)
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
								isinstance(bool(fname), OSError)
								raise
								raise
								e = isinstance(bool(fname), OSError)
								app_log(f'{'追加写入 '}{str(name)}{' 失败: '}{str(e)}', exc=True)
								self._json({'ok': False, 'message': ('写入文件失败: %s' ? e)})
								e = None
								del e
								return
								e = None
								del e
								raise
								raise
								raise
								isinstance(bool(fname), Exception)
								r['qr_svg'] = ''
								raise
								raise
								isinstance(bool(fname), ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool(bool(fname))
								b.get('file')
								bool(fname)
								raise
						else:
							pass
					for fe in msg.files:
						# [控制流] JUMP_BACKWARD 1052
						# [控制流] END_FOR None
						[] + [{'path': fe['path'], 'size': fe['size'], 'etag': fe['etag']}]
						files = fe
						fe = False
						for f in files:
							# [控制流] JUMP_BACKWARD 1205
							# [控制流] END_FOR None
							[] + [os.path.basename(f['path'])]
							f = detect_versions
							bool(TASKS.import_.is_alive())({'files': self._json, 'versions': files(f)})
							return
							if (path == '/api/export/dir'):
								bool(b.get('dirName'))
								bool(b.get('parentPath'))
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
							else:
								pass
							{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
							return
							if (path == '/api/export/category'):
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
							else:
								pass
							{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
							return
							if (path == '/api/export/merge'):
								bool(b.get('cats'))
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
							else:
								pass
							{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
							return
							if (path == '/api/export/selected'):
								bool(b.get('dirName'))
								bool(b.get('parentPath'))
								bool(b.get('paths'))
								# [未实现] STORE_FAST_STORE_FAST 171
								# [未实现] LOAD_FAST_LOAD_FAST 171
							else:
								pass
							{'ok': self._json, 'file': bool(r), 'message': bool(r)}({'ok': False, 'message': msg})
							return
							if (path == '/api/client-log'):
								bool(b.get('msg'))
								'前端: %s'((b.get('msg') ? ''), exc=bool(b.get('stack')))
								self._json({'ok': True})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '追加影库.json')
								name = (name ? '.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								fp = os.path.join(DATA_ROOT, '秒传文件导入或追加', name)
								tmp = (fp ? '.uploading')
								f = __with__
								f.write(content)
								None(None, None)
								last_err = None
								_ = range(4)
								# [未实现] LOAD_FAST_LOAD_FAST 254
								# [未实现] CALL 2
								b.get('content')
								last_err = None
								bool(name.lower().endswith('.json'))
							else:
								# [控制流] END_FOR None
							re.sub
							if (last_err is not None):
								os.remove(tmp)
								app_log(f'{'追加替换 '}{str(name)}{' 失败: '}{str(last_err)}', exc=True)
								self._json({'ok': False, 'message': ('文件被占用, 请稍后重试: %s' ? last_err)})
								return
								app_log(('追加入库成功: %s (%d 字符)' ? (name, len(content))))
								self._json({'ok': True, 'message': ('已导入, Watcher 将自动加载: ' ? name)})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别123云盘分享链接'})
								return
								r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'], 0)
								r['shareKey'] = parsed['shareKey']
								r['pwd'] = parsed['pwd']
								self._json(r)
								return
								bool(b.get('parentFileId'))
								r = b.get('shareKey')(b.get('pwd'), int, b.get('parentFileId')(0))
								self._json(r)
								return
								bool(b.get('shareKey'))
								sk = ''
								ExtractTask.delete_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
								self._json({'ok': True})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(TASKS.extract)
								running = TASKS.extract.is_alive()
								self._json({'ok': False, 'message': '已有提取任务在进行中'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts)
								TASKS.extract = t
								t.start()
								self._json({'ok': True, 'shareKey': parsed['shareKey']})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(b.get('selected'))
								sel = []
								self._json({'ok': False, 'message': '没有勾选任何项目'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts, selected=sel)
								TASKS.extract = t
								t.start()
								self._json({'ok': True})
								return
								TASKS.extract.stop()
								self._json({'ok': True})
								return
								bool(b.get('token'))
								r = b.get('token')('')
								AUTH['token'] = r['token']
								AUTH['nickname'] = r.get('nickname', '')
								AUTH['uid'] = r.get('uid', 0)
								save_auth()
								self._json(r)
								return
								bool(b.get('passport'))
								bool(b.get('password'))
								r = ''(b.get('password'), '')
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								r = pan.qr_create()
								segno = __import__('segno', None, None, None)
								_io = __import__('io', None, None, None)
								buf = _io.BytesIO()
								segno.make(r['qr_url']).save(buf, kind='svg', border=2, scale=6)
								svg = buf.getvalue().decode('utf-8')
								r['qr_svg'] = ('data:image/svg+xml;base64,' ? base64.b64encode(svg.encode('utf-8')).decode('ascii'))
								self._json(r)
								return
								bool(b.get('uniId'))
								bool(b.get('loginuuid'))
								r = ''(b.get('loginuuid'), AUTH['loginuuid'])
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								self._json({'ok': True})
								return
								self._json({'ok': False, 'message': '请先登录123云盘'})
								return
								self._json({'ok': False, 'message': '已有导入任务在进行中'})
								return
								bool(b.get('file'))
								fname = ''
								fp = ''
								fp = os.path.join(STORE.export_dir_path, fname)
								self._json({'ok': False, 'message': ('JSON 文件不存在: ' ? fname)})
								return
								# [未实现] LOAD_FAST_LOAD_FAST 226
								bool(AUTH['token'].get('targetDir'))
								t = bool(os.path.isfile(fp))(ImportTask, AUTH['token'].get('targetDir'), target_dir='', auto_common=bool(b.get('autoCommon', True)), loginuuid=AUTH['loginuuid'])
								TASKS.import_ = t
								t.start()
								self._json({'ok': True})
								return
								t = TASKS.import_
								t.stop()
								app_log('用户请求停止秒传导入')
								self._json({'ok': True, 'message': '停止指令已发出, 正在收尾…'})
								return
								self._json({'ok': False, 'message': '当前没有进行中的导入任务'})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '外部.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								os.makedirs(STORE.export_dir_path, exist_ok=True)
								f = __with__
								f.write(content)
								None(None, None)
								self._json({'ok': True, 'name': name})
								return
								bool(b.get('key'))
								k = ''.strip()
								bool(k)
								TMDB_KEY['key'] = TMDB_KEY_DEFAULT
								self._json({'ok': True, 'key': TMDB_KEY['key']})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								b.get('key')
								h = (path == '/api/tmdb-key')
								raise
								open(os.path.join(STORE.export_dir_path, name), 'w', encoding='utf-8')
								fe = b.get('content')
								raise
								re.sub
								f = (path == '/api/import/upload')
								raise
								isinstance(k, ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool((path == '/api/import/stop'))
								bool(t.is_alive())
								bool(t)
								raise
								e = isinstance(bool(fname), OSError)
								last_err = e
								os.chmod(fp, 438)
							# [控制流] JUMP_FORWARD 9640
							if isinstance((path == '/api/import/stop'), OSError):
								bool(fname)
							else:
								raise
							raise
							time.sleep(0.6)
							try:
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
								isinstance(b.get('file'), OSError)
								raise
								raise
							except OSError:
								e = b.get('file')
								app_log(f'{'追加写入 '}{str(name)}{' 失败: '}{str(e)}', exc=True)
							e = None
							del e
							return
							try:
								e = None
								del e
								raise
								raise
							except Exception:
								r['qr_svg'] = ''
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 11390
							try:
								raise
							except ValueError:
								pass
							return
							raise
							raise
							if not (bool(bool(TASKS.import_.is_alive()))):
								raise
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								self._json({'ok': False, 'message': ('写入文件失败: %s' ? e)})
								bool(TASKS.import_.is_alive())
								raise
				else:
					pass
				bool(TASKS.import_.is_alive())({'ok': False, 'message': msg})
				return
				if (path == '/api/export/category'):
					# [未实现] STORE_FAST_STORE_FAST 171
					if bool(r):
						pass
					# [未实现] LOAD_FAST_LOAD_FAST 171
				else:
					pass
				{'ok': __unpack1_of_2(STORE.export_category(b.get('cat1', ''), b.get('cat2', ''), b.get('libIds'))), 'file': self._json, 'message': bool(r)}({'ok': False, 'message': msg})
				return
				if (path == '/api/export/merge'):
					if not (bool(b.get('cats'))):
						pass
					b.get('cats')
					# [未实现] STORE_FAST_STORE_FAST 171
					if bool(r):
						pass
					# [未实现] LOAD_FAST_LOAD_FAST 171
				else:
					pass
				{'ok': __unpack1_of_2(STORE.export_merge([], b.get('libIds'))), 'file': self._json, 'message': bool(r)}({'ok': False, 'message': msg})
				return
				if (path == '/api/export/selected'):
					if not (bool(b.get('dirName'))):
						pass
					b.get('dirName')
					if not (bool(b.get('parentPath'))):
						pass
					b.get('parentPath')
					if not (bool(b.get('paths'))):
						pass
					b.get('paths')
					# [未实现] STORE_FAST_STORE_FAST 171
					if bool(r):
						pass
					# [未实现] LOAD_FAST_LOAD_FAST 171
				else:
					pass
				{'ok': __unpack1_of_2(STORE.export_selected(b.get('libId'), '', '', [])), 'file': self._json, 'message': bool(r)}({'ok': False, 'message': msg})
				return
				if (path == '/api/client-log'):
					if not (bool(b.get('msg'))):
						pass
					b.get('msg')
					app_log(('前端: %s' ? ''), exc=bool(b.get('stack')))
					self._json({'ok': True})
					return
					if (path == '/api/append-import'):
						if not (bool(b.get('name'))):
							pass
						b.get('name')
						name = re.sub('[\\\\/:*?|><"]', '-', '追加影库.json')
						if not (bool(name.lower().endswith('.json'))):
							name = (name ? '.json')
							if not (bool(b.get('content'))):
								pass
							b.get('content')
							content = ''
							try:
								json.loads(content)
								fp = os.path.join(DATA_ROOT, '秒传文件导入或追加', name)
								tmp = (fp ? '.uploading')
								f = __with__
								f.write(content)
								None(None, None)
								last_err = None
								_ = range(4)
								# [未实现] LOAD_FAST_LOAD_FAST 254
								# [未实现] CALL 2
								__unpack0_of_2(STORE.export_selected(b.get('libId'), '', '', []))
								last_err = None
								__unpack0_of_2(STORE.export_merge([], b.get('libIds')))
								# [控制流] END_FOR None
								__unpack0_of_2(STORE.export_category(b.get('cat1', ''), b.get('cat2', ''), b.get('libIds')))
								os.remove(tmp)
								app_log(f'{'追加替换 '}{str(name)}{' 失败: '}{str(last_err)}', exc=True)
								self._json({'ok': False, 'message': ('文件被占用, 请稍后重试: %s' ? last_err)})
								return
								app_log(('追加入库成功: %s (%d 字符)' ? (name, len(content))))
								self._json({'ok': True, 'message': ('已导入, Watcher 将自动加载: ' ? name)})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别123云盘分享链接'})
								return
								r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'], 0)
								r['shareKey'] = parsed['shareKey']
								r['pwd'] = parsed['pwd']
								self._json(r)
								return
								bool(b.get('parentFileId'))
								r = b.get('shareKey')(b.get('pwd'), int, b.get('parentFileId')(0))
								self._json(r)
								return
								bool(b.get('shareKey'))
								sk = ''
								ExtractTask.delete_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
								self._json({'ok': True})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(TASKS.extract)
								running = TASKS.extract.is_alive()
								self._json({'ok': False, 'message': '已有提取任务在进行中'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts)
								TASKS.extract = t
								t.start()
								self._json({'ok': True, 'shareKey': parsed['shareKey']})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(b.get('selected'))
								sel = []
								self._json({'ok': False, 'message': '没有勾选任何项目'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts, selected=sel)
								TASKS.extract = t
								t.start()
								self._json({'ok': True})
								return
								TASKS.extract.stop()
								self._json({'ok': True})
								return
								bool(b.get('token'))
								r = b.get('token')('')
								AUTH['token'] = r['token']
								AUTH['nickname'] = r.get('nickname', '')
								AUTH['uid'] = r.get('uid', 0)
								save_auth()
								self._json(r)
								return
								bool(b.get('passport'))
								bool(b.get('password'))
								r = ''(b.get('password'), '')
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								r = pan.qr_create()
								segno = __import__('segno', None, None, None)
								_io = __import__('io', None, None, None)
								buf = _io.BytesIO()
								segno.make(r['qr_url']).save(buf, kind='svg', border=2, scale=6)
								svg = buf.getvalue().decode('utf-8')
								r['qr_svg'] = ('data:image/svg+xml;base64,' ? base64.b64encode(svg.encode('utf-8')).decode('ascii'))
								self._json(r)
								return
								bool(b.get('uniId'))
								bool(b.get('loginuuid'))
								r = ''(b.get('loginuuid'), AUTH['loginuuid'])
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								self._json({'ok': True})
								return
								self._json({'ok': False, 'message': '请先登录123云盘'})
								return
								self._json({'ok': False, 'message': '已有导入任务在进行中'})
								return
								bool(b.get('file'))
								fname = ''
								fp = ''
								fp = os.path.join(STORE.export_dir_path, fname)
								self._json({'ok': False, 'message': ('JSON 文件不存在: ' ? fname)})
								return
								# [未实现] LOAD_FAST_LOAD_FAST 226
								bool(AUTH['token'].get('targetDir'))
								t = bool(os.path.isfile(fp))(ImportTask, AUTH['token'].get('targetDir'), target_dir='', auto_common=bool(b.get('autoCommon', True)), loginuuid=AUTH['loginuuid'])
								TASKS.import_ = t
								t.start()
								self._json({'ok': True})
								return
								t = TASKS.import_
								t.stop()
								app_log('用户请求停止秒传导入')
								self._json({'ok': True, 'message': '停止指令已发出, 正在收尾…'})
								return
								self._json({'ok': False, 'message': '当前没有进行中的导入任务'})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '外部.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								os.makedirs(STORE.export_dir_path, exist_ok=True)
								f = __with__
								f.write(content)
								None(None, None)
								self._json({'ok': True, 'name': name})
								return
								bool(b.get('key'))
								k = ''.strip()
								bool(k)
								TMDB_KEY['key'] = TMDB_KEY_DEFAULT
								self._json({'ok': True, 'key': TMDB_KEY['key']})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								b.get('key')
								h = (path == '/api/tmdb-key')
								raise
								open(os.path.join(STORE.export_dir_path, name), 'w', encoding='utf-8')
								fe = b.get('content')
								raise
								re.sub
								f = (path == '/api/import/upload')
								raise
							except ValueError:
								pass
						else:
							# [控制流] END_FOR None
					else:
						# [控制流] END_FOR None
				else:
					# [控制流] END_FOR None
				k
				if (last_err is not None):
					try:
						os.remove(tmp)
						try:
							app_log(f'{'追加替换 '}{str(name)}{' 失败: '}{str(last_err)}', exc=True)
							self._json({'ok': False, 'message': ('文件被占用, 请稍后重试: %s' ? last_err)})
							return
							app_log(('追加入库成功: %s (%d 字符)' ? (name, len(content))))
							self._json({'ok': True, 'message': ('已导入, Watcher 将自动加载: ' ? name)})
							return
							if (path == '/api/extract/parse'):
								bool(b.get('link'))
								parsed = b.get('link')('')
							self._json({'ok': False, 'message': '无法识别123云盘分享链接'})
							return
							r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'], 0)
							r['shareKey'] = parsed['shareKey']
							r['pwd'] = parsed['pwd']
							self._json(r)
							return
							if (path == '/api/extract/list'):
								bool(b.get('parentFileId'))
								r = b.get('shareKey')(b.get('pwd'), int, b.get('parentFileId')(0))
								self._json(r)
								return
								bool(b.get('shareKey'))
								sk = ''
								ExtractTask.delete_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
								self._json({'ok': True})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(TASKS.extract)
								running = TASKS.extract.is_alive()
								self._json({'ok': False, 'message': '已有提取任务在进行中'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts)
								TASKS.extract = t
								t.start()
								self._json({'ok': True, 'shareKey': parsed['shareKey']})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(b.get('selected'))
								sel = []
								self._json({'ok': False, 'message': '没有勾选任何项目'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts, selected=sel)
								TASKS.extract = t
								t.start()
								self._json({'ok': True})
								return
								TASKS.extract.stop()
								self._json({'ok': True})
								return
								bool(b.get('token'))
								r = b.get('token')('')
								AUTH['token'] = r['token']
								AUTH['nickname'] = r.get('nickname', '')
								AUTH['uid'] = r.get('uid', 0)
								save_auth()
								self._json(r)
								return
								bool(b.get('passport'))
								bool(b.get('password'))
								r = ''(b.get('password'), '')
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								r = pan.qr_create()
								segno = __import__('segno', None, None, None)
								_io = __import__('io', None, None, None)
								buf = _io.BytesIO()
								segno.make(r['qr_url']).save(buf, kind='svg', border=2, scale=6)
								svg = buf.getvalue().decode('utf-8')
								r['qr_svg'] = ('data:image/svg+xml;base64,' ? base64.b64encode(svg.encode('utf-8')).decode('ascii'))
								self._json(r)
								return
								bool(b.get('uniId'))
								bool(b.get('loginuuid'))
								r = ''(b.get('loginuuid'), AUTH['loginuuid'])
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								self._json({'ok': True})
								return
								self._json({'ok': False, 'message': '请先登录123云盘'})
								return
								self._json({'ok': False, 'message': '已有导入任务在进行中'})
								return
								bool(b.get('file'))
								fname = ''
								fp = ''
								fp = os.path.join(STORE.export_dir_path, fname)
								self._json({'ok': False, 'message': ('JSON 文件不存在: ' ? fname)})
								return
								# [未实现] LOAD_FAST_LOAD_FAST 226
								bool(AUTH['token'].get('targetDir'))
								t = bool(os.path.isfile(fp))(ImportTask, AUTH['token'].get('targetDir'), target_dir='', auto_common=bool(b.get('autoCommon', True)), loginuuid=AUTH['loginuuid'])
								TASKS.import_ = t
								t.start()
								self._json({'ok': True})
								return
								t = TASKS.import_
								t.stop()
								app_log('用户请求停止秒传导入')
								self._json({'ok': True, 'message': '停止指令已发出, 正在收尾…'})
								return
								self._json({'ok': False, 'message': '当前没有进行中的导入任务'})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '外部.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								os.makedirs(STORE.export_dir_path, exist_ok=True)
								f = __with__
								f.write(content)
								None(None, None)
								self._json({'ok': True, 'name': name})
								return
								bool(b.get('key'))
								k = ''.strip()
								bool(k)
								TMDB_KEY['key'] = TMDB_KEY_DEFAULT
								self._json({'ok': True, 'key': TMDB_KEY['key']})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								b.get('key')
								h = (path == '/api/tmdb-key')
								raise
								open(os.path.join(STORE.export_dir_path, name), 'w', encoding='utf-8')
								fe = b.get('content')
								raise
								re.sub
								f = (path == '/api/import/upload')
								raise
								isinstance(k, ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool((path == '/api/import/stop'))
								bool(t.is_alive())
								bool(t)
								raise
								e = isinstance(bool(fname), OSError)
								last_err = e
								os.chmod(fp, 438)
							# [控制流] JUMP_FORWARD 9640
							if isinstance((path == '/api/import/stop'), OSError):
								bool(fname)
							else:
								raise
							raise
							time.sleep(0.6)
							try:
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
								isinstance(b.get('file'), OSError)
								raise
								raise
							except OSError:
								pass
						except OSError:
							pass
					except OSError:
						pass
				# [控制流] JUMP_FORWARD 9640
				if isinstance(b.get('file'), OSError):
					bool(TASKS.import_.is_alive())
				else:
					raise
				raise
				time.sleep(0.6)
				try:
					e = None
					del e
					# [控制流] JUMP_BACKWARD 13114
					try:
						e = None
						del e
						raise
						raise
					except OSError:
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 13121
					try:
						raise
					except OSError:
						pass
				except OSError:
					e = b.get('file')
					app_log(f'{'追加写入 '}{str(name)}{' 失败: '}{str(e)}', exc=True)
				e = None
				del e
				return
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					r['qr_svg'] = ''
				# [控制流] JUMP_BACKWARD_NO_INTERRUPT 11390
				try:
					raise
				except ValueError:
					pass
				return
				raise
				raise
				if not (bool(bool(TASKS.import_.is_alive()))):
					raise
					self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
					self._json({'ok': False, 'message': ('写入文件失败: %s' ? e)})
					bool(TASKS.import_.is_alive())
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 10487
					raise
		else:
			pass
		bool(TASKS.import_.is_alive())({'ok': False, 'message': msg})
		return
		if (path == '/api/export/category'):
			# [未实现] STORE_FAST_STORE_FAST 171
			if bool(r):
				pass
			# [未实现] LOAD_FAST_LOAD_FAST 171
		else:
			pass
		{'ok': __unpack1_of_2(STORE.export_category(b.get('cat1', ''), b.get('cat2', ''), b.get('libIds'))), 'file': self._json, 'message': bool(r)}({'ok': False, 'message': msg})
		return
		if (path == '/api/export/merge'):
			if not (bool(b.get('cats'))):
				pass
			b.get('cats')
			# [未实现] STORE_FAST_STORE_FAST 171
			if bool(r):
				pass
			# [未实现] LOAD_FAST_LOAD_FAST 171
		else:
			pass
		{'ok': __unpack1_of_2(STORE.export_merge([], b.get('libIds'))), 'file': self._json, 'message': bool(r)}({'ok': False, 'message': msg})
		return
		if (path == '/api/export/selected'):
			if not (bool(b.get('dirName'))):
				pass
			b.get('dirName')
			if not (bool(b.get('parentPath'))):
				pass
			b.get('parentPath')
			if not (bool(b.get('paths'))):
				pass
			b.get('paths')
			# [未实现] STORE_FAST_STORE_FAST 171
			if bool(r):
				pass
			# [未实现] LOAD_FAST_LOAD_FAST 171
		else:
			pass
		{'ok': __unpack1_of_2(STORE.export_selected(b.get('libId'), '', '', [])), 'file': self._json, 'message': bool(r)}({'ok': False, 'message': msg})
		return
		if (path == '/api/client-log'):
			if not (bool(b.get('msg'))):
				pass
			b.get('msg')
			app_log(('前端: %s' ? ''), exc=bool(b.get('stack')))
			self._json({'ok': True})
			return
			if (path == '/api/append-import'):
				if not (bool(b.get('name'))):
					pass
				b.get('name')
				name = re.sub('[\\\\/:*?|><"]', '-', '追加影库.json')
				if not (bool(name.lower().endswith('.json'))):
					name = (name ? '.json')
					if not (bool(b.get('content'))):
						pass
					b.get('content')
					content = ''
					try:
						json.loads(content)
						fp = os.path.join(DATA_ROOT, '秒传文件导入或追加', name)
						tmp = (fp ? '.uploading')
						with open(tmp, 'w', encoding='utf-8') as f:
							f.write(content)
						try:
							None(None, None)
							last_err = None
							for _ in range(4):
								# [未实现] LOAD_FAST_LOAD_FAST 254
								# [未实现] CALL 2
								__unpack0_of_2(STORE.export_merge([], b.get('libIds')))
								last_err = None
								__unpack0_of_2(STORE.export_category(b.get('cat1', ''), b.get('cat2', ''), b.get('libIds')))
								# [控制流] END_FOR None
								bool(fname)
								os.remove(tmp)
								app_log(f'{'追加替换 '}{str(name)}{' 失败: '}{str(last_err)}', exc=True)
								self._json({'ok': False, 'message': ('文件被占用, 请稍后重试: %s' ? last_err)})
								return
								app_log(('追加入库成功: %s (%d 字符)' ? (name, len(content))))
								self._json({'ok': True, 'message': ('已导入, Watcher 将自动加载: ' ? name)})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别123云盘分享链接'})
								return
								r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'], 0)
								r['shareKey'] = parsed['shareKey']
								r['pwd'] = parsed['pwd']
								self._json(r)
								return
								bool(b.get('parentFileId'))
								r = b.get('shareKey')(b.get('pwd'), int, b.get('parentFileId')(0))
								self._json(r)
								return
								bool(b.get('shareKey'))
								sk = ''
								ExtractTask.delete_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
								self._json({'ok': True})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(TASKS.extract)
								running = TASKS.extract.is_alive()
								self._json({'ok': False, 'message': '已有提取任务在进行中'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts)
								TASKS.extract = t
								t.start()
								self._json({'ok': True, 'shareKey': parsed['shareKey']})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(b.get('selected'))
								sel = []
								self._json({'ok': False, 'message': '没有勾选任何项目'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts, selected=sel)
								TASKS.extract = t
								t.start()
								self._json({'ok': True})
								return
								TASKS.extract.stop()
								self._json({'ok': True})
								return
								bool(b.get('token'))
								r = b.get('token')('')
								AUTH['token'] = r['token']
								AUTH['nickname'] = r.get('nickname', '')
								AUTH['uid'] = r.get('uid', 0)
								save_auth()
								self._json(r)
								return
								bool(b.get('passport'))
								bool(b.get('password'))
								r = ''(b.get('password'), '')
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								r = pan.qr_create()
								segno = __import__('segno', None, None, None)
								_io = __import__('io', None, None, None)
								buf = _io.BytesIO()
								segno.make(r['qr_url']).save(buf, kind='svg', border=2, scale=6)
								svg = buf.getvalue().decode('utf-8')
								r['qr_svg'] = ('data:image/svg+xml;base64,' ? base64.b64encode(svg.encode('utf-8')).decode('ascii'))
								self._json(r)
								return
								bool(b.get('uniId'))
								bool(b.get('loginuuid'))
								r = ''(b.get('loginuuid'), AUTH['loginuuid'])
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								self._json({'ok': True})
								return
								self._json({'ok': False, 'message': '请先登录123云盘'})
								return
								self._json({'ok': False, 'message': '已有导入任务在进行中'})
								return
								bool(b.get('file'))
								fname = ''
								fp = ''
								fp = os.path.join(STORE.export_dir_path, fname)
								self._json({'ok': False, 'message': ('JSON 文件不存在: ' ? fname)})
								return
								# [未实现] LOAD_FAST_LOAD_FAST 226
								bool(AUTH['token'].get('targetDir'))
								t = bool(os.path.isfile(fp))(ImportTask, AUTH['token'].get('targetDir'), target_dir='', auto_common=bool(b.get('autoCommon', True)), loginuuid=AUTH['loginuuid'])
								TASKS.import_ = t
								t.start()
								self._json({'ok': True})
								return
								t = TASKS.import_
								t.stop()
								app_log('用户请求停止秒传导入')
								self._json({'ok': True, 'message': '停止指令已发出, 正在收尾…'})
								return
								self._json({'ok': False, 'message': '当前没有进行中的导入任务'})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '外部.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								os.makedirs(STORE.export_dir_path, exist_ok=True)
								f = __with__
								f.write(content)
								None(None, None)
								self._json({'ok': True, 'name': name})
								return
								bool(b.get('key'))
								k = ''.strip()
								bool(k)
								TMDB_KEY['key'] = TMDB_KEY_DEFAULT
								self._json({'ok': True, 'key': TMDB_KEY['key']})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								b.get('key')
								h = (path == '/api/tmdb-key')
								raise
								open(os.path.join(STORE.export_dir_path, name), 'w', encoding='utf-8')
								fe = b.get('content')
								raise
								re.sub
								f = (path == '/api/import/upload')
								raise
								isinstance(k, ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool((path == '/api/import/stop'))
								bool(t.is_alive())
								bool(t)
								raise
								e = isinstance(bool(fname), OSError)
								last_err = e
								os.chmod(fp, 438)
								isinstance((path == '/api/import/stop'), OSError)
								raise
								raise
								time.sleep(0.6)
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
								isinstance(bool(fname), OSError)
								raise
								raise
								e = isinstance(bool(fname), OSError)
								app_log(f'{'追加写入 '}{str(name)}{' 失败: '}{str(e)}', exc=True)
								self._json({'ok': False, 'message': ('写入文件失败: %s' ? e)})
								e = None
								del e
								return
								e = None
								del e
								raise
								raise
								raise
								isinstance(bool(fname), Exception)
								r['qr_svg'] = ''
								raise
								raise
								isinstance(bool(fname), ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool(bool(fname))
								b.get('file')
								bool(fname)
								raise
						except OSError:
							pass
					except ValueError:
						pass
				else:
					# [控制流] END_FOR None
			else:
				# [控制流] END_FOR None
		else:
			# [控制流] END_FOR None
		bool(TASKS.import_.is_alive())
		if (last_err is not None):
			try:
				os.remove(tmp)
				try:
					app_log(f'{'追加替换 '}{str(name)}{' 失败: '}{str(last_err)}', exc=True)
					self._json({'ok': False, 'message': ('文件被占用, 请稍后重试: %s' ? last_err)})
					return
					app_log(('追加入库成功: %s (%d 字符)' ? (name, len(content))))
					self._json({'ok': True, 'message': ('已导入, Watcher 将自动加载: ' ? name)})
					return
					if (path == '/api/extract/parse'):
						if not (bool(b.get('link'))):
							pass
						b.get('link')
						parsed = pan.parse_share_text('')
						if not (bool(parsed)):
							self._json({'ok': False, 'message': '无法识别123云盘分享链接'})
							return
							r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'], 0)
							r['shareKey'] = parsed['shareKey']
							r['pwd'] = parsed['pwd']
							self._json(r)
							return
							if (path == '/api/extract/list'):
								bool(b.get('parentFileId'))
								r = b.get('shareKey')(b.get('pwd'), int, b.get('parentFileId')(0))
								self._json(r)
								return
								bool(b.get('shareKey'))
								sk = ''
								ExtractTask.delete_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
								self._json({'ok': True})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(TASKS.extract)
								running = TASKS.extract.is_alive()
								self._json({'ok': False, 'message': '已有提取任务在进行中'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts)
								TASKS.extract = t
								t.start()
								self._json({'ok': True, 'shareKey': parsed['shareKey']})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(b.get('selected'))
								sel = []
								self._json({'ok': False, 'message': '没有勾选任何项目'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts, selected=sel)
								TASKS.extract = t
								t.start()
								self._json({'ok': True})
								return
								TASKS.extract.stop()
								self._json({'ok': True})
								return
								bool(b.get('token'))
								r = b.get('token')('')
								AUTH['token'] = r['token']
								AUTH['nickname'] = r.get('nickname', '')
								AUTH['uid'] = r.get('uid', 0)
								save_auth()
								self._json(r)
								return
								bool(b.get('passport'))
								bool(b.get('password'))
								r = ''(b.get('password'), '')
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								r = pan.qr_create()
								segno = __import__('segno', None, None, None)
								_io = __import__('io', None, None, None)
								buf = _io.BytesIO()
								segno.make(r['qr_url']).save(buf, kind='svg', border=2, scale=6)
								svg = buf.getvalue().decode('utf-8')
								r['qr_svg'] = ('data:image/svg+xml;base64,' ? base64.b64encode(svg.encode('utf-8')).decode('ascii'))
								self._json(r)
								return
								bool(b.get('uniId'))
								bool(b.get('loginuuid'))
								r = ''(b.get('loginuuid'), AUTH['loginuuid'])
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								self._json({'ok': True})
								return
								self._json({'ok': False, 'message': '请先登录123云盘'})
								return
								self._json({'ok': False, 'message': '已有导入任务在进行中'})
								return
								bool(b.get('file'))
								fname = ''
								fp = ''
								fp = os.path.join(STORE.export_dir_path, fname)
								self._json({'ok': False, 'message': ('JSON 文件不存在: ' ? fname)})
								return
								# [未实现] LOAD_FAST_LOAD_FAST 226
								bool(AUTH['token'].get('targetDir'))
								t = bool(os.path.isfile(fp))(ImportTask, AUTH['token'].get('targetDir'), target_dir='', auto_common=bool(b.get('autoCommon', True)), loginuuid=AUTH['loginuuid'])
								TASKS.import_ = t
								t.start()
								self._json({'ok': True})
								return
								t = TASKS.import_
								t.stop()
								app_log('用户请求停止秒传导入')
								self._json({'ok': True, 'message': '停止指令已发出, 正在收尾…'})
								return
								self._json({'ok': False, 'message': '当前没有进行中的导入任务'})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '外部.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								os.makedirs(STORE.export_dir_path, exist_ok=True)
								f = __with__
								f.write(content)
								None(None, None)
								self._json({'ok': True, 'name': name})
								return
								bool(b.get('key'))
								k = ''.strip()
								bool(k)
								TMDB_KEY['key'] = TMDB_KEY_DEFAULT
								self._json({'ok': True, 'key': TMDB_KEY['key']})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								b.get('key')
								h = (path == '/api/tmdb-key')
								raise
								open(os.path.join(STORE.export_dir_path, name), 'w', encoding='utf-8')
								fe = b.get('content')
								raise
								re.sub
								f = (path == '/api/import/upload')
								raise
								isinstance(k, ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool((path == '/api/import/stop'))
								bool(t.is_alive())
								bool(t)
								raise
								e = isinstance(bool(fname), OSError)
								last_err = e
								os.chmod(fp, 438)
					bool(fname)((path == '/api/import/stop'))
					return
					r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'], 0)
					r['shareKey'] = parsed['shareKey']
					r['pwd'] = parsed['pwd']
					self._json(r)
					return
					if (path == '/api/extract/list'):
						if not (bool(b.get('parentFileId'))):
							pass
						b.get('parentFileId')
						r = pan.share_browse_dir(b.get('shareKey'), b.get('pwd'), int(0))
						self._json(r)
						return
						if (path == '/api/extract/checkpoint/delete'):
							if not (bool(b.get('shareKey'))):
								pass
							b.get('shareKey')
							sk = ''
							ExtractTask.delete_checkpoint(os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints'), sk)
							self._json({'ok': True})
							return
							if (path == '/api/extract/start'):
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(TASKS.extract)
								running = TASKS.extract.is_alive()
								self._json({'ok': False, 'message': '已有提取任务在进行中'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts)
								TASKS.extract = t
								t.start()
								self._json({'ok': True, 'shareKey': parsed['shareKey']})
								return
								bool(b.get('link'))
								parsed = b.get('link')('')
								self._json({'ok': False, 'message': '无法识别分享链接'})
								return
								bool(b.get('selected'))
								sel = []
								self._json({'ok': False, 'message': '没有勾选任何项目'})
								return
								ft = b.get('fileTypes')
								exts = None
								exts = set()
								g = ft
								exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
								# [控制流] END_FOR None
								ft
								bool(b.get('title'))
								bool(b.get('cat1'))
								bool(b.get('cat2'))
								t = os.path.join(DATA_ROOT, '秒传文件导入或追加')(b.get('title'), '', b.get('cat1'), title='', cat1=b.get('cat2'), cat2='', file_types=exts, selected=sel)
								TASKS.extract = t
								t.start()
								self._json({'ok': True})
								return
								TASKS.extract.stop()
								self._json({'ok': True})
								return
								bool(b.get('token'))
								r = b.get('token')('')
								AUTH['token'] = r['token']
								AUTH['nickname'] = r.get('nickname', '')
								AUTH['uid'] = r.get('uid', 0)
								save_auth()
								self._json(r)
								return
								bool(b.get('passport'))
								bool(b.get('password'))
								r = ''(b.get('password'), '')
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								r = pan.qr_create()
								segno = __import__('segno', None, None, None)
								_io = __import__('io', None, None, None)
								buf = _io.BytesIO()
								segno.make(r['qr_url']).save(buf, kind='svg', border=2, scale=6)
								svg = buf.getvalue().decode('utf-8')
								r['qr_svg'] = ('data:image/svg+xml;base64,' ? base64.b64encode(svg.encode('utf-8')).decode('ascii'))
								self._json(r)
								return
								bool(b.get('uniId'))
								bool(b.get('loginuuid'))
								r = ''(b.get('loginuuid'), AUTH['loginuuid'])
								AUTH['token'] = r['token']
								info = pan.user_info_from_token(r['token'])
								AUTH['nickname'] = info.get('nickname', '')
								AUTH['uid'] = info.get('uid', 0)
								save_auth()
								r.update(info)
								self._json(r)
								return
								AUTH['token'] = ''
								AUTH['nickname'] = ''
								AUTH['uid'] = 0
								save_auth()
								self._json({'ok': True})
								return
								self._json({'ok': False, 'message': '请先登录123云盘'})
								return
								self._json({'ok': False, 'message': '已有导入任务在进行中'})
								return
								bool(b.get('file'))
								fname = ''
								fp = ''
								fp = os.path.join(STORE.export_dir_path, fname)
								self._json({'ok': False, 'message': ('JSON 文件不存在: ' ? fname)})
								return
								# [未实现] LOAD_FAST_LOAD_FAST 226
								bool(AUTH['token'].get('targetDir'))
								t = bool(os.path.isfile(fp))(ImportTask, AUTH['token'].get('targetDir'), target_dir='', auto_common=bool(b.get('autoCommon', True)), loginuuid=AUTH['loginuuid'])
								TASKS.import_ = t
								t.start()
								self._json({'ok': True})
								return
								t = TASKS.import_
								t.stop()
								app_log('用户请求停止秒传导入')
								self._json({'ok': True, 'message': '停止指令已发出, 正在收尾…'})
								return
								self._json({'ok': False, 'message': '当前没有进行中的导入任务'})
								return
								bool(b.get('name'))
								name = '[\\\\/:*?|><"]'('-', b.get('name'), '外部.json')
								bool(b.get('content'))
								content = ''
								json.loads(content)
								os.makedirs(STORE.export_dir_path, exist_ok=True)
								f = __with__
								f.write(content)
								None(None, None)
								self._json({'ok': True, 'name': name})
								return
								bool(b.get('key'))
								k = ''.strip()
								bool(k)
								TMDB_KEY['key'] = TMDB_KEY_DEFAULT
								self._json({'ok': True, 'key': TMDB_KEY['key']})
								return
								self._json({'error': 'unknown endpoint'}, 404)
								return
								b.get('key')
								h = (path == '/api/tmdb-key')
								raise
								open(os.path.join(STORE.export_dir_path, name), 'w', encoding='utf-8')
								fe = b.get('content')
								raise
								re.sub
								f = (path == '/api/import/upload')
								raise
								isinstance(k, ValueError)
								self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
								return
								raise
								raise
								raise
								bool((path == '/api/import/stop'))
								bool(t.is_alive())
								bool(t)
								raise
								e = isinstance(bool(fname), OSError)
								last_err = e
								os.chmod(fp, 438)
					# [控制流] JUMP_FORWARD 9640
					if isinstance((path == '/api/import/stop'), OSError):
						bool(fname)
					else:
						raise
					raise
					time.sleep(0.6)
					try:
						e = None
						del e
						# [控制流] JUMP_BACKWARD 13114
						try:
							e = None
							del e
							raise
							raise
						except OSError:
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 13121
						try:
							raise
						except OSError:
							pass
					except OSError:
						pass
				except OSError:
					pass
			except OSError:
				pass
		# [控制流] JUMP_FORWARD 9640
		if isinstance(b.get('file'), OSError):
			bool(TASKS.import_.is_alive())
		else:
			raise
		raise
		time.sleep(0.6)
		try:
			e = None
			del e
			# [控制流] JUMP_BACKWARD 13114
			try:
				e = None
				del e
				raise
				raise
			except OSError:
				# [控制流] JUMP_BACKWARD_NO_INTERRUPT 13121
			try:
				raise
			except OSError:
				pass
		except OSError:
			e = b.get('file')
			app_log(f'{'追加写入 '}{str(name)}{' 失败: '}{str(e)}', exc=True)
		e = None
		del e
		return
		try:
			e = None
			del e
			raise
			raise
		except Exception:
			r['qr_svg'] = ''
		# [控制流] JUMP_BACKWARD_NO_INTERRUPT 11390
		try:
			raise
		except ValueError:
			pass
		return
		raise
		raise
		if not (bool(bool(TASKS.import_.is_alive()))):
			raise
			self._json({'ok': False, 'message': '不是有效的 JSON 文件'})
			self._json({'ok': False, 'message': ('写入文件失败: %s' ? e)})
			bool(TASKS.import_.is_alive())
			# [控制流] JUMP_BACKWARD_NO_INTERRUPT 10487
			raise
	__static_attributes__ = ()
	return

Handler = (False,)
def _now():
	datetime = __import__('datetime', None, None, ('datetime',)).datetime
	__import__('datetime', None, None, ('datetime',))
	return datetime.now().strftime('%m-%d %H:%M')

def detect_versions(names):
	rules = [] + list((('2160P HDR H265', ('2160', '4k', 'hdr', '265')), ('2160P', ('2160', '4k')), ('1080P HDR', ('1080', 'hdr')), ('1080P', ('1080',)), ('720P', ('720',)), ('DV', ('dovi', 'dolby vision', 'dv ')), ('H265', ('265', 'hevc')), ('H264', ('264', 'avc')), ('AV1', ('av1',))))
	groups = {}
	for n in names:
		ln = n.lower().replace('.', ' ')
		tags = []
		for ? in rules:
			# [未实现] STORE_FAST_STORE_FAST 103
			for k in keys:
				# [未实现] LOAD_FAST_LOAD_FAST 132
				if not ((__unpack0_of_2(<栈空>) not in __unpack1_of_2(<栈空>))):
					pass
				# [控制流] JUMP_BACKWARD 138
				tags.append(label)
				<栈空>
				# [控制流] JUMP_BACKWARD 205
				# [控制流] END_FOR None
				<栈空>
				# [控制流] JUMP_BACKWARD 217
				# [控制流] END_FOR None
				<栈空>
				if bool(tags):
					pass
				# [控制流] JUMP_FORWARD 267
				key = '其他'
				groups.setdefault(key, []).append(n)
				# [控制流] JUMP_BACKWARD 499
				# [控制流] END_FOR None
				' '.join(sorted(set(tags)))
				if (len(groups) == 1):
					pass
				return []
				for ? in groups.items():
					# [未实现] STORE_FAST_STORE_FAST 138
					# [控制流] JUMP_BACKWARD 486
					# [控制流] END_FOR None
					__unpack1_of_2([]) + [{'label': k, 'count': len(v), 'names': v}]
					out = __unpack0_of_2([])
					k = k
					v = v
					out.sort(key=<code object <lambda> at 0x000002384EC9E410, file "server.py", line 817>)
					return out
					<栈空>
					v = <栈空>
					k = <栈空>
					raise

def find_free_port(start):
	p = start
	for _ in range(50):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			try:
				s.bind(('127.0.0.1', p))
				None(None, None)
				p
				return <栈空>
				# [控制流] END_FOR None
				<栈空>
				return start
			except OSError:
				pass
		None(None, None)
		<栈空>
		return <栈空>
		# [控制流] END_FOR None
		<栈空>
		return start
		if isinstance(<栈空>, OSError):
			<栈空>
		p = (p ? 1)
		# [控制流] JUMP_FORWARD 250
		raise
		raise
		None(None, None)
		# [控制流] JUMP_BACKWARD 398
		if not (bool(<栈空>)):
			raise
			<栈空>
			<栈空>
			<栈空>
			# [控制流] JUMP_BACKWARD 443
			raise

def run_server():
	find_free_port = find_free_port(5890)
	srv = ThreadingHTTPServer(('127.0.0.1', HTTP_PORT), Handler)
	srv.serve_forever()
	return

def main():
	init_data_root()
	url = ('http://127.0.0.1:%d/' ? 0)
	t = threading.Thread(target=run_server, daemon=True)
	t.start()
	_t = __import__('time', None, None, None)
	for _ in range(50):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			if (s.connect_ex(('127.0.0.1', HTTP_PORT)) == 0):
				None(None, None)
				<栈空>
		None(None, None)
		<栈空>
		# [控制流] JUMP_FORWARD 360
		None(None, None)
		_t.sleep(0.1)
		# [控制流] JUMP_BACKWARD 505
		# [控制流] END_FOR None
		<栈空>
		url = ('http://127.0.0.1:%d/' ? HTTP_PORT)
		print(f'{str(APP_NAME)}{' '}{str(APP_VERSION)}{'  数据目录: '}{str(DATA_ROOT)}{'  '}{str(url)}')
		exe_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
		if not (bool(('浏览器版' not in exe_name))):
			('浏览器版' not in exe_name)
			if not (bool(('--browser' not in sys.argv))):
				('--browser' not in sys.argv)
			browser_mode = (os.environ.get('LB_BROWSER') == '1')
			if not (bool(browser_mode)):
				if not (bool(_try_webview(url))):
					webbrowser.open(url)
					print('浏览器模式运行中, 关闭此窗口或按 Ctrl+C 退出')
					_t.sleep(3600)
					# [控制流] JUMP_BACKWARD 959
					return
					try:
						if not (bool(<栈空>)):
							raise
							<栈空>
							<栈空>
							<栈空>
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1285
							raise
							if isinstance(None, KeyboardInterrupt):
								<栈空>
								return
								raise
								raise
					except KeyboardInterrupt:
						return
					raise

def _try_webview(url):
	try:
		webview = __import__('webview', None, None, None)
		try:
			webview.create_window(APP_NAME, url, width=1560, height=900, min_size=(1024, 600))
			webview.start()
			return True
			try:
				if isinstance(<栈空>, ImportError):
					<栈空>
					return False
					try:
						raise
					except Exception:
						return False
					raise
			except Exception:
				pass
		except Exception:
			pass
	except ImportError:
		return False
	raise
	if isinstance(None, Exception):
		return False
		raise
		raise

# [控制流] POP_JUMP_IF_FALSE 674
main()
return
return
