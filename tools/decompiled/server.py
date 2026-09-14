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
	if bool(os.environ.get('APPDATA')):
		os.environ.get('APPDATA')
		base = os.path.expanduser('~')
		d = os.path.join(base, APP_NAME)
		os.makedirs(d, exist_ok=True)
		return d

CONFIG_PATH = os.path.join(appdata_dir(), 'data_config.json')
def load_config():
	with ('encoding',) as f:
		pass
	try:
		None(None, None)
		return <栈空>(u=<栈空>, t=<栈空>, f=open, -=CONFIG_PATH, 8='r')
		try:
			# [控制流] PUSH_EXC_INFO None
			# [控制流] WITH_EXCEPT_START None
			if bool(json.load(f)):
				raise
				<栈空>
				try:
					# [控制流] POP_EXCEPT None
					<栈空>
					<栈空>
					return
					try:
						# [控制流] POP_EXCEPT None
						raise
					except Exception:
						pass
				except Exception:
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(None, Exception)):
							<栈空>
							# [控制流] POP_EXCEPT None
							return {}
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						pass
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			try:
				# [控制流] POP_EXCEPT None
				raise
			except Exception:
				pass
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, Exception)):
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def save_config(cfg):
	with ('encoding',) as f:
		# [未实现] LOAD_FAST_LOAD_FAST 'f'
		# [未实现] CALL_KW 4
		<栈空>
	try:
		None(None, None)
		return
		try:
			# [控制流] PUSH_EXC_INFO None
			# [控制流] WITH_EXCEPT_START None
			if bool(<栈空>):
				raise
				<栈空>
				try:
					# [控制流] POP_EXCEPT None
					<栈空>
					<栈空>
					return
					try:
						# [控制流] POP_EXCEPT None
						raise
					except Exception:
						pass
				except Exception:
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(None, OSError)):
							<栈空>
							# [控制流] POP_EXCEPT None
							return
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						pass
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			try:
				# [控制流] POP_EXCEPT None
				raise
			except Exception:
				pass
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, OSError)):
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

BGM_EXTS = ('.mp3', '.flac', '.ogg', '.m4a', '.aac', '.wav')
BGM_MIME = {'.mp3': 'audio/mpeg', '.flac': 'audio/flac', '.ogg': 'audio/ogg', '.m4a': 'audio/mp4', '.aac': 'audio/aac', '.wav': 'audio/wav'}
def find_external_bgm():
	if not (bool(getattr(sys, 'frozen', False))):
		pass
	# [控制流] JUMP_FORWARD 199
	bases = [os.path.dirname(os.path.abspath(__file__))]
	if not (bool(DATA_ROOT)):
		bases.append(DATA_ROOT)
		for base in bases:
			if not (bool(base)):
				if bool(os.path.isdir(base)):
					pass
				# [控制流] JUMP_BACKWARD 476
				try:
					for fn in sorted(os.listdir(base)):
						# [未实现] UNPACK_SEQUENCE 2
						# [未实现] STORE_FAST_STORE_FAST 52
						if (stem.lower() == 'bgm'):
							pass
					try:
						if (ext.lower() not in BGM_EXTS):
							pass
						# [控制流] JUMP_BACKWARD 744
						try:
							# [未实现] LOAD_FAST_LOAD_FAST 18
							(os.path.dirname(sys.executable)(os.path.splitext(fn), os.path.join), BGM_MIME[ext.lower()])
							<栈空>
							return <栈空>
							try:
								# [控制流] END_FOR None
								<栈空>
								# [控制流] JUMP_BACKWARD 1010
								# [控制流] END_FOR None
								<栈空>
								return
							except Exception:
								pass
						except Exception:
							pass
					except Exception:
						pass
				except Exception:
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(<栈空>, OSError)):
							<栈空>
						# [控制流] POP_EXCEPT None
						# [控制流] JUMP_BACKWARD 1058
						try:
							raise
						except Exception:
							pass
					except Exception:
						pass
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		try:
			for fn in sorted(os.listdir(base)):
				# [未实现] UNPACK_SEQUENCE 2
				# [未实现] STORE_FAST_STORE_FAST 52
				if (stem.lower() == 'bgm'):
					pass
			try:
				if (ext.lower() not in BGM_EXTS):
					pass
				# [控制流] JUMP_BACKWARD 744
				try:
					# [未实现] LOAD_FAST_LOAD_FAST 18
					(<栈空>(os.path.splitext(fn), os.path.join), BGM_MIME[ext.lower()])
					<栈空>
					return <栈空>
					try:
						# [控制流] END_FOR None
						<栈空>
						# [控制流] JUMP_BACKWARD 1010
						# [控制流] END_FOR None
						<栈空>
						return
					except Exception:
						pass
				except Exception:
					pass
			except Exception:
				pass
		except Exception:
			try:
				# [控制流] PUSH_EXC_INFO None
				if not (isinstance(<栈空>, OSError)):
					<栈空>
				# [控制流] POP_EXCEPT None
				# [控制流] JUMP_BACKWARD 1058
				try:
					raise
				except Exception:
					pass
			except Exception:
				pass
		try:
			raise
		except Exception:
			# [控制流] POP_EXCEPT None
			raise

def ensure_data_dirs(root):
	os.makedirs(os.path.join(root, '秒传文件导入或追加'), exist_ok=True)
	os.makedirs(os.path.join(root, '秒传文件导出'), exist_ok=True)
	bak = os.path.join(root, '记录数据存放目录【勿动】')
	os.makedirs(bak, exist_ok=True)
	try:
		shutil.copyfile(CONFIG_PATH, os.path.join(bak, 'data_config.json'))
		return
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, OSError)):
				<栈空>
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
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
		if bool(path):
			pass
		path
		return ''
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, Exception)):
				<栈空>
				# [控制流] POP_EXCEPT None
				return ''
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def init_data_root():
	cfg = load_config()
	# [未实现] BINARY_SLICE None
	args = None
	root = ''
	# [控制流] MAKE_FUNCTION None
	if not (bool(<code object <genexpr> at 0x00000282E5289630, file "server.py", line 129>(args()))):
		pass
	# [控制流] JUMP_FORWARD 243
	for a in args:
		if bool(a.startswith('--dir=')):
			pass
	# [未实现] BINARY_SLICE None
	root = None.strip('"')
	# [控制流] JUMP_BACKWARD 261
	# [控制流] END_FOR None
	6
	if bool(root):
		pass
	if bool(cfg.get('data_root')):
		pass
	cfg.get('data_root')
	root = ''
	if not (bool(root)):
		if bool(os.path.isdir(root)):
			pass
		root = ''
		if bool(root):
			root = select_dir_dialog('选择数据存放目录（将自动创建子目录）')
			if bool(root):
				print('未选择数据目录, 退出')
				sys.exit(0)
				if not (bool(getattr(sys, 'frozen', False))):
					pass
	# [控制流] JUMP_FORWARD 689
	exe_dir = os.path.dirname(os.path.abspath(__file__))
	for n in os.listdir(exe_dir):
		if bool(n.lower().endswith('.json')):
			pass
	try:
		# [未实现] LOAD_FAST_LOAD_FAST 69
		# [未实现] CALL 2
		# [未实现] LOAD_FAST_LOAD_FAST 37
		1(any, a(os.path.dirname(sys.executable), os.path.join))
		# [控制流] JUMP_BACKWARD 1171
		# [控制流] END_FOR None
		sys.argv
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
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, OSError)):
				<栈空>
				# [控制流] POP_EXCEPT None
				# [控制流] JUMP_BACKWARD 1835
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def setup_logging():
	try:
		d = os.path.join(DATA_ROOT, 'logs')
		os.makedirs(d, exist_ok=True)
		lg = logging.getLogger('app')
		lg.setLevel(logging.INFO)
		if bool(lg.handlers):
			fh = logging.FileHandler(os.path.join(d, 'server.log'), encoding='utf-8')
			fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
			lg.addHandler(fh)
			setLevel = lg
			return
			try:
				# [控制流] PUSH_EXC_INFO None
				if not (isinstance(<栈空>, Exception)):
					<栈空>
					setLevel = None
					# [控制流] POP_EXCEPT None
					return
					try:
						raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, Exception)):
				setLevel = None
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def app_log(msg, exc):
	if not (bool(LOGGER)):
		try:
			if not (bool(exc)):
				# [未实现] LOAD_FAST_LOAD_FAST 'exc'
				<栈空>(<栈空>, exc_info=LOGGER.error)
				return
				try:
					LOGGER.info(msg)
					return
					return
				except Exception:
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(<栈空>, Exception)):
							<栈空>
							# [控制流] POP_EXCEPT None
							return
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						pass
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	# [未实现] CALL_KW 2
	<栈空>
	return
	try:
		LOGGER.info(msg)
		return
		return
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, Exception)):
				<栈空>
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def load_history():
	try:
		with ('encoding',) as f:
			# [未实现] BINARY_SLICE None
			# [未实现] STORE_SLICE None
		try:
			None(None, None)
			return
			try:
				# [控制流] PUSH_EXC_INFO None
				# [控制流] WITH_EXCEPT_START None
				if bool(None):
					raise
					None
					try:
						# [控制流] POP_EXCEPT None
						HISTORY
						HISTORY_MAX
						return
						try:
							# [控制流] POP_EXCEPT None
							raise
						except Exception:
							pass
					except Exception:
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(<栈空>(u=<栈空>, t=<栈空>, f=open, -=os.path.join(DATA_ROOT, '.history.json'), 8='r'), Exception)):
								None
								# [未实现] STORE_SLICE None
								# [控制流] POP_EXCEPT None
								return
								try:
									raise
								except Exception:
									# [控制流] POP_EXCEPT None
									raise
						except Exception:
							pass
					try:
						raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
			except Exception:
				try:
					# [控制流] POP_EXCEPT None
					raise
				except Exception:
					pass
		except Exception:
			pass
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, Exception)):
				None
				# [未实现] STORE_SLICE None
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def save_history():
	try:
		with ('encoding',) as f:
			# [未实现] BINARY_SLICE None
			None(HISTORY_MAX, f, ensure_ascii=False)
		try:
			None(None, None)
			return
			try:
				# [控制流] PUSH_EXC_INFO None
				# [控制流] WITH_EXCEPT_START None
				if bool(HISTORY):
					raise
					try:
						# [控制流] POP_EXCEPT None
						json.dump
						<栈空>(u=<栈空>, t=<栈空>, f=open, -=os.path.join(DATA_ROOT, '.history.json'), 8='w')
						return
						try:
							# [控制流] POP_EXCEPT None
							raise
						except Exception:
							pass
					except Exception:
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(None, OSError)):
								<栈空>
								# [控制流] POP_EXCEPT None
								return
								try:
									raise
								except Exception:
									# [控制流] POP_EXCEPT None
									raise
						except Exception:
							pass
					try:
						raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
			except Exception:
				try:
					# [控制流] POP_EXCEPT None
					raise
				except Exception:
					pass
		except Exception:
			pass
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, OSError)):
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def _auth_file():
	return os.path.join(DATA_ROOT, '.login.json')

def save_auth():
	try:
		if not (bool(AUTH['token'])):
			with ('encoding',) as f:
				json.dump({'token': AUTH['token'], 'nickname': AUTH['nickname'], 'uid': AUTH['uid']}, f, ensure_ascii=False)
			try:
				None(None, None)
				return
				try:
					os.remove(_auth_file())
					return
					try:
						# [控制流] PUSH_EXC_INFO None
						# [控制流] WITH_EXCEPT_START None
						if bool(<栈空>(u=<栈空>, t=<栈空>, f=open, -=_auth_file(), 8='w')):
							raise
							<栈空>
							try:
								# [控制流] POP_EXCEPT None
								<栈空>
								<栈空>
								return
								try:
									# [控制流] POP_EXCEPT None
									raise
									try:
										# [控制流] PUSH_EXC_INFO None
										if not (isinstance(None, OSError)):
											<栈空>
											try:
												# [控制流] POP_EXCEPT None
												return
												try:
													raise
												except Exception:
													try:
														# [控制流] POP_EXCEPT None
														raise
													except Exception:
														pass
											except Exception:
												try:
													# [控制流] PUSH_EXC_INFO None
													if not (isinstance(None, OSError)):
														<栈空>
														# [控制流] POP_EXCEPT None
														return
														try:
															raise
														except Exception:
															# [控制流] POP_EXCEPT None
															raise
												except Exception:
													pass
											try:
												raise
											except Exception:
												# [控制流] POP_EXCEPT None
												raise
									except Exception:
										try:
											# [控制流] POP_EXCEPT None
											raise
										except Exception:
											pass
								except Exception:
									pass
							except Exception:
								try:
									# [控制流] PUSH_EXC_INFO None
									if not (isinstance(None, OSError)):
										# [控制流] POP_EXCEPT None
										return
										try:
											raise
										except Exception:
											# [控制流] POP_EXCEPT None
											raise
								except Exception:
									pass
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						try:
							# [控制流] POP_EXCEPT None
							raise
							try:
								# [控制流] PUSH_EXC_INFO None
								if not (isinstance(None, OSError)):
									try:
										# [控制流] POP_EXCEPT None
										return
										try:
											raise
										except Exception:
											try:
												# [控制流] POP_EXCEPT None
												raise
											except Exception:
												pass
									except Exception:
										try:
											# [控制流] PUSH_EXC_INFO None
											if not (isinstance(None, OSError)):
												# [控制流] POP_EXCEPT None
												return
												try:
													raise
												except Exception:
													# [控制流] POP_EXCEPT None
													raise
										except Exception:
											pass
									try:
										raise
									except Exception:
										# [控制流] POP_EXCEPT None
										raise
							except Exception:
								try:
									# [控制流] POP_EXCEPT None
									raise
								except Exception:
									pass
						except Exception:
							pass
				except Exception:
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(None, OSError)):
							try:
								# [控制流] POP_EXCEPT None
								return
								try:
									raise
								except Exception:
									try:
										# [控制流] POP_EXCEPT None
										raise
									except Exception:
										pass
							except Exception:
								try:
									# [控制流] PUSH_EXC_INFO None
									if not (isinstance(None, OSError)):
										# [控制流] POP_EXCEPT None
										return
										try:
											raise
										except Exception:
											# [控制流] POP_EXCEPT None
											raise
								except Exception:
									pass
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						pass
				try:
					# [控制流] POP_EXCEPT None
					return
					try:
						raise
					except Exception:
						try:
							# [控制流] POP_EXCEPT None
							raise
						except Exception:
							pass
				except Exception:
					pass
			except Exception:
				try:
					# [控制流] PUSH_EXC_INFO None
					if not (isinstance(None, OSError)):
						# [控制流] POP_EXCEPT None
						return
						try:
							raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
				except Exception:
					pass
			try:
				raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, OSError)):
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def load_auth():
	# [控制流] MAKE_CELL 3
	with ('encoding',) as f:
		d = json.load(f)
	try:
		None(None, None)
		if bool(d.get('token')):
			pass
		d.get('token')
		3 = ''
		if bool(3):
			return
			try:
				AUTH['token'] = 3
				AUTH['nickname'] = d.get('nickname', '')
				AUTH['uid'] = d.get('uid', 0)
				# [未实现] BUILD_TUPLE 1
				# [控制流] MAKE_FUNCTION None
				# [控制流] SET_FUNCTION_ATTRIBUTE 8
				_verify = <code object _verify at 0x00000282E528E030, file "server.py", line 242>
				threading.Thread(target=_verify, daemon=True).start()
				return
				try:
					# [控制流] PUSH_EXC_INFO None
					# [控制流] WITH_EXCEPT_START None
					if bool(<栈空>(u=<栈空>, t=<栈空>, f=open, -=_auth_file(), 8='r')):
						raise
						<栈空>
						try:
							# [控制流] POP_EXCEPT None
							<栈空>
							<栈空>
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 553
							# [控制流] POP_EXCEPT None
							raise
						except Exception:
							try:
								# [控制流] PUSH_EXC_INFO None
								if not (isinstance(None, Exception)):
									<栈空>
									# [控制流] POP_EXCEPT None
									return
									try:
										raise
									except Exception:
										# [控制流] POP_EXCEPT None
										raise
							except Exception:
								pass
						try:
							raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
			except Exception:
				try:
					# [控制流] PUSH_EXC_INFO None
					if not (isinstance(None, Exception)):
						# [控制流] POP_EXCEPT None
						return
						try:
							raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
				except Exception:
					pass
			try:
				raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, Exception)):
				# [控制流] POP_EXCEPT None
				return
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
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
			if not (bool(year)):
				# [未实现] LOAD_FAST_LOAD_FAST 22
			if not ((mtype == 'movie')):
				pass
			# [控制流] JUMP_FORWARD 97
			'year'['first_air_date_year'] = <栈空>
			# [未实现] FORMAT_SIMPLE None
			# [未实现] FORMAT_SIMPLE None
			url = f'{<栈空>}{<栈空>}{'https://api.themoviedb.org/3/search/'}{'?'}'
			req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
			# [未实现] CALL_KW 2
			with ('timeout',) as r:
				data = json.loads(r.read().decode('utf-8'))
			try:
				None(None, None)
				if bool(data.get('results')):
					pass
				data.get('results')
				for res in []:
					score = 0
					if bool(res.get('title')):
						res.get('title')
					if bool(res.get('name')):
						pass
					res.get('name')
					name = ''
					if (title.lower() not in name.lower()):
						pass
					if not ((name.lower() not in title.lower())):
						score = (score ? 2)
						if bool(res.get('release_date')):
							res.get('release_date')
						if bool(res.get('first_air_date')):
							pass
						res.get('first_air_date')
						# [未实现] BINARY_SLICE None
						y = 4
						if not (bool(year)):
							# [未实现] LOAD_FAST_LOAD_FAST 225
							if not (('' == None)):
								score = (score ? 1)
								if (score == 2):
									pass
								# [控制流] JUMP_BACKWARD 1071
								try:
									# [未实现] LOAD_FAST_LOAD_FAST 203
									if bool(req.get('popularity')):
										pass
									req.get('popularity')
									if not (bool(res.get('poster_path'))):
										pass
									# [控制流] JUMP_FORWARD 995
									# [未实现] LOAD_FAST_LOAD_FAST 222
									cand = {'score': <栈空>, 'poster': (urllib.request.urlopen ? (0 ? 1000.0)), 'title': (TMDB_IMG ? res['poster_path']), 'year': '', 'type': mtype}
									if (best is None):
										if (cand['score'] == best['score']):
											# [控制流] JUMP_BACKWARD 1333
											try:
												best = cand
												# [控制流] JUMP_BACKWARD 1348
												# [控制流] END_FOR None
												<栈空>
												# [控制流] JUMP_BACKWARD 1567
												# [控制流] END_FOR None
												<栈空>
												return best
												try:
													# [控制流] PUSH_EXC_INFO None
													# [控制流] WITH_EXCEPT_START None
													if bool(<栈空>):
														raise
														<栈空>
														try:
															# [控制流] POP_EXCEPT None
															<栈空>
															<栈空>
															# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1448
															# [控制流] POP_EXCEPT None
															raise
														except Exception:
															try:
																# [控制流] PUSH_EXC_INFO None
																if not (isinstance(None, Exception)):
																	<栈空>
																	# [控制流] POP_EXCEPT None
																	# [控制流] JUMP_BACKWARD 1675
																	try:
																		raise
																	except Exception:
																		# [控制流] POP_EXCEPT None
																		raise
															except Exception:
																pass
														try:
															raise
														except Exception:
															# [控制流] POP_EXCEPT None
															raise
												except Exception:
													# [控制流] POP_EXCEPT None
													raise
											except Exception:
												try:
													# [控制流] PUSH_EXC_INFO None
													if not (isinstance(None, Exception)):
														# [控制流] POP_EXCEPT None
														# [控制流] JUMP_BACKWARD 1675
														try:
															raise
														except Exception:
															# [控制流] POP_EXCEPT None
															raise
												except Exception:
													pass
											try:
												raise
											except Exception:
												# [控制流] POP_EXCEPT None
												raise
								except Exception:
									pass
				try:
					# [未实现] LOAD_FAST_LOAD_FAST 203
					if bool(None.get('popularity')):
						pass
					None.get('popularity')
					if not (bool(res.get('poster_path'))):
						pass
					# [控制流] JUMP_FORWARD 995
					# [未实现] LOAD_FAST_LOAD_FAST 222
					cand = {'score': <栈空>, 'poster': (None ? (0 ? 1000.0)), 'title': (TMDB_IMG ? res['poster_path']), 'year': '', 'type': mtype}
					if (best is None):
						if (cand['score'] == best['score']):
							# [控制流] JUMP_BACKWARD 1333
							try:
								best = cand
								# [控制流] JUMP_BACKWARD 1348
								# [控制流] END_FOR None
								<栈空>
								# [控制流] JUMP_BACKWARD 1567
								# [控制流] END_FOR None
								<栈空>
								return best
								try:
									# [控制流] PUSH_EXC_INFO None
									# [控制流] WITH_EXCEPT_START None
									if bool(<栈空>):
										raise
										<栈空>
										try:
											# [控制流] POP_EXCEPT None
											<栈空>
											<栈空>
											# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1448
											# [控制流] POP_EXCEPT None
											raise
										except Exception:
											try:
												# [控制流] PUSH_EXC_INFO None
												if not (isinstance(None, Exception)):
													<栈空>
													# [控制流] POP_EXCEPT None
													# [控制流] JUMP_BACKWARD 1675
													try:
														raise
													except Exception:
														# [控制流] POP_EXCEPT None
														raise
											except Exception:
												pass
										try:
											raise
										except Exception:
											# [控制流] POP_EXCEPT None
											raise
								except Exception:
									# [控制流] POP_EXCEPT None
									raise
							except Exception:
								try:
									# [控制流] PUSH_EXC_INFO None
									if not (isinstance(None, Exception)):
										# [控制流] POP_EXCEPT None
										# [控制流] JUMP_BACKWARD 1675
										try:
											raise
										except Exception:
											# [控制流] POP_EXCEPT None
											raise
								except Exception:
									pass
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
				except Exception:
					pass
			except Exception:
				pass
		except Exception:
			pass
	try:
		# [未实现] LOAD_FAST_LOAD_FAST 203
		if bool(None.get('popularity')):
			pass
		None.get('popularity')
		if not (bool(res.get('poster_path'))):
			pass
		# [控制流] JUMP_FORWARD 995
		# [未实现] LOAD_FAST_LOAD_FAST 222
		cand = {'score': <栈空>, 'poster': (None ? (0 ? 1000.0)), 'title': (TMDB_IMG ? res['poster_path']), 'year': '', 'type': mtype}
		if (best is None):
			if (cand['score'] == best['score']):
				# [控制流] JUMP_BACKWARD 1333
				try:
					best = cand
					# [控制流] JUMP_BACKWARD 1348
					# [控制流] END_FOR None
					<栈空>
					# [控制流] JUMP_BACKWARD 1567
					# [控制流] END_FOR None
					<栈空>
					return best
					try:
						# [控制流] PUSH_EXC_INFO None
						# [控制流] WITH_EXCEPT_START None
						if bool(<栈空>):
							raise
							<栈空>
							try:
								# [控制流] POP_EXCEPT None
								<栈空>
								<栈空>
								# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1448
								# [控制流] POP_EXCEPT None
								raise
							except Exception:
								try:
									# [控制流] PUSH_EXC_INFO None
									if not (isinstance(None, Exception)):
										<栈空>
										# [控制流] POP_EXCEPT None
										# [控制流] JUMP_BACKWARD 1675
										try:
											raise
										except Exception:
											# [控制流] POP_EXCEPT None
											raise
								except Exception:
									pass
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
				except Exception:
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(None, Exception)):
							# [控制流] POP_EXCEPT None
							# [控制流] JUMP_BACKWARD 1675
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						pass
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, Exception)):
				# [控制流] POP_EXCEPT None
				# [控制流] JUMP_BACKWARD 1675
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

class Handler(BaseHTTPRequestHandler):
	protocol_version = 'HTTP/1.1'
	server_version = ('LibraryServer/' ? APP_VERSION)
	# [控制流] MAKE_FUNCTION None
	log_message = <code object log_message at 0x00000282E519C100, file "server.py", line 298>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	_json = <code object _json at 0x00000282E4AD22E0, file "server.py", line 302>
	# [控制流] MAKE_FUNCTION None
	_body = <code object _body at 0x00000282E528E630, file "server.py", line 314>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	_static = <code object _static at 0x00000282E47381A0, file "server.py", line 327>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	_static_abs = <code object _static_abs at 0x00000282E4B490D0, file "server.py", line 344>
	# [控制流] MAKE_FUNCTION None
	_qs = <code object _qs at 0x00000282E51668B0, file "server.py", line 366>
	# [控制流] MAKE_FUNCTION None
	_libs_param = <code object _libs_param at 0x00000282E4C2AD30, file "server.py", line 371>
	# [控制流] MAKE_FUNCTION None
	do_GET = <code object do_GET at 0x00000282E4C53C00, file "server.py", line 381>
	# [控制流] MAKE_FUNCTION None
	do_POST = <code object do_POST at 0x00000282E4C53DD0, file "server.py", line 391>
	# [控制流] MAKE_FUNCTION None
	_safe_traceback = <code object _safe_traceback at 0x00000282E5248270, file "server.py", line 401>()
	# [控制流] MAKE_FUNCTION None
	_route_get = <code object _route_get at 0x00000282E4F3B230, file "server.py", line 409>
	# [控制流] MAKE_FUNCTION None
	_route_post = <code object _route_post at 0x00000282E4CF4020, file "server.py", line 508>
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
			# [未实现] UNPACK_SEQUENCE 2
			# [未实现] STORE_FAST_STORE_FAST 103
			for k in keys:
				# [未实现] LOAD_FAST_LOAD_FAST 132
				if (<栈空> not in <栈空>):
					pass
	tags.append(label)
	<栈空>
	# [控制流] JUMP_BACKWARD 205
	# [控制流] END_FOR None
	<栈空>
	# [控制流] JUMP_BACKWARD 217
	# [控制流] END_FOR None
	<栈空>
	if not (bool(tags)):
		pass
	# [控制流] JUMP_FORWARD 267
	key = '其他'
	groups.setdefault(key, []).append(n)
	# [控制流] JUMP_BACKWARD 499
	# [控制流] END_FOR None
	' '.join(sorted(set(tags)))
	if not ((len(groups) == 1)):
		pass
	return []
	try:
		for ? in groups.items():
			# [未实现] UNPACK_SEQUENCE 2
			# [未实现] STORE_FAST_STORE_FAST 138
		out = [] + [{'label': k, 'count': len(v), 'names': v}]
		k = k
		v = v
		# [控制流] MAKE_FUNCTION None
		out.sort(key=<code object <lambda> at 0x00000282E5236E90, file "server.py", line 817>)
		return out
	except Exception:
		<栈空>
		v = <栈空>
		k = <栈空>
		raise

def find_free_port(start):
	p = start
	for _ in range(50):
		# [未实现] CALL 2
		with socket.SOCK_STREAM as s:
			try:
				s.bind(('127.0.0.1', p))
				None(None, None)
				p
				return <栈空>
				# [控制流] END_FOR None
				<栈空>
				return start
			except Exception:
				pass
		None(None, None)
		<栈空>
		return <栈空>
		# [控制流] END_FOR None
		<栈空>
		return start
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, OSError)):
				<栈空>
			p = (p ? 1)
			try:
				# [控制流] POP_EXCEPT None
				# [控制流] JUMP_FORWARD 250
				try:
					raise
				except Exception:
					try:
						# [控制流] POP_EXCEPT None
						raise
						None(None, None)
						# [控制流] JUMP_BACKWARD 398
					except Exception:
						pass
			except Exception:
				pass
		except Exception:
			try:
				# [控制流] POP_EXCEPT None
				raise
				None(None, None)
				# [控制流] JUMP_BACKWARD 398
			except Exception:
				pass
	try:
		# [控制流] PUSH_EXC_INFO None
		# [控制流] WITH_EXCEPT_START None
		if bool(<栈空>):
			raise
			<栈空>
			# [控制流] POP_EXCEPT None
			<栈空>
			<栈空>
			# [控制流] JUMP_BACKWARD 443
			# [控制流] POP_EXCEPT None
			raise
	except Exception:
		# [控制流] POP_EXCEPT None
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
		# [未实现] CALL 2
		with socket.SOCK_STREAM as s:
			if not ((s.connect_ex(('127.0.0.1', HTTP_PORT)) == 0)):
				None(None, None)
				<栈空>
		None(None, None)
		<栈空>
		# [控制流] JUMP_FORWARD 360
		None(None, None)
		_t.sleep(0.1)
	url = ('http://127.0.0.1:%d/' ? HTTP_PORT)
	# [未实现] FORMAT_SIMPLE None
	# [未实现] FORMAT_SIMPLE None
	# [未实现] FORMAT_SIMPLE None
	# [未实现] FORMAT_SIMPLE None
	<栈空>(f'{<栈空>}{<栈空>}{<栈空>}{print}{' '}{'  数据目录: '}{'  '}')
	exe_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
	if bool(('浏览器版' not in exe_name)):
		('浏览器版' not in exe_name)
		if bool(('--browser' not in sys.argv)):
			('--browser' not in sys.argv)
		browser_mode = (os.environ.get('LB_BROWSER') == '1')
		if bool(browser_mode):
			if bool(_try_webview(url)):
				webbrowser.open(url)
				print('浏览器模式运行中, 关闭此窗口或按 Ctrl+C 退出')
				_t.sleep(3600)
				# [控制流] JUMP_BACKWARD 959
				return
				try:
					# [控制流] PUSH_EXC_INFO None
					# [控制流] WITH_EXCEPT_START None
					if bool(<栈空>):
						raise
						<栈空>
						# [控制流] POP_EXCEPT None
						<栈空>
						<栈空>
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1285
						# [控制流] POP_EXCEPT None
						raise
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(None, KeyboardInterrupt)):
								<栈空>
								# [控制流] POP_EXCEPT None
								return
								try:
									raise
								except Exception:
									# [控制流] POP_EXCEPT None
									raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
				try:
					# [控制流] PUSH_EXC_INFO None
					if not (isinstance(None, KeyboardInterrupt)):
						# [控制流] POP_EXCEPT None
						return
						try:
							raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise

def _try_webview(url):
	try:
		webview = __import__('webview', None, None, None)
		try:
			webview.create_window(APP_NAME, url, width=1560, height=900, min_size=(1024, 600))
			webview.start()
			return True
			try:
				# [控制流] PUSH_EXC_INFO None
				if not (isinstance(<栈空>, ImportError)):
					<栈空>
					# [控制流] POP_EXCEPT None
					return False
					try:
						raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(None, Exception)):
							<栈空>
							# [控制流] POP_EXCEPT None
							return False
							try:
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise
		except Exception:
			pass
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, ImportError)):
				# [控制流] POP_EXCEPT None
				return False
				try:
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
				try:
					# [控制流] PUSH_EXC_INFO None
					if not (isinstance(None, Exception)):
						# [控制流] POP_EXCEPT None
						return False
						try:
							raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise
	try:
		# [控制流] PUSH_EXC_INFO None
		if not (isinstance(None, Exception)):
			# [控制流] POP_EXCEPT None
			return False
			try:
				raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

# [控制流] POP_JUMP_IF_FALSE 674
main()
return
return
