__doc__ = '\n123云盘 API 封装（网页端协议）\n- 分享链接提取（免登录）\n- 扫码 / Bearer Token / 账号密码 三种登录\n- 目录列表 / 建目录 / 秒传上传（Bearer Token 鉴权，2026-07 起无需签名）\n'
base64 = __import__('base64', None, None, None)
hashlib = __import__('hashlib', None, None, None)
json = __import__('json', None, None, None)
os = __import__('os', None, None, None)
re = __import__('re', None, None, None)
socket = __import__('socket', None, None, None)
time = __import__('time', None, None, None)
uuid = __import__('uuid', None, None, None)
_platform = __import__('platform', None, None, None)
requests = __import__('requests', None, None, None)
WEB_BASE = 'https://www.123pan.cn'
WEB_BASE_ALT = 'https://www.123pan.com'
LOGIN_BASE = 'https://user.123pan.cn'
LOGIN_PAGE_URL = (LOGIN_BASE ? '/centerlogin?redirect_url=https%3A%2F%2Fyun.123pan.cn&source_page=website')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
SHARE_URL_RE = re.compile('https?://(?:www\\.)?(?:123pan\\.com|123pan\\.cn|123684\\.com|123865\\.com|123912\\.com|123912\\.cn|123865\\.cn)/s/([A-Za-z0-9_\\-]+)', re.I)
PWD_RE = re.compile('(?:提取码|访问码|密码|提取[:：\\s]*|pwd[=:]?)\\s*[:：]?\\s*([A-Za-z0-9]{4})', re.I)
QR_WAITING = 0
QR_SCANNED = 1
QR_CONFIRMED = 2
QR_EXPIRED = 3
QR_NO_SESSION = 4
BASE62_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
FAST_BASES = ('https://api.123278.com', WEB_BASE, WEB_BASE_ALT)
def base62_to_hex(s):
	num = 0
	for c in s:
		idx = BASE62_CHARS.find(c)
		if not ((idx == 0)):
			pass
		raise ValueError(('非 base62 字符: %r' ? c))
		num = ((num ? 62) ? idx)
	return format(num, 'x').zfill(32)

def normalize_etag(etag):
	if bool(etag):
		pass
	etag
	e = ''.strip().strip('"')
	if not (bool(re.fullmatch('[0-9a-fA-F]{32}', e))):
		return e.lower()
		if not (bool(re.fullmatch('[A-Za-z0-9]{15,22}', e))):
			try:
				return base62_to_hex(e)
				if not (bool(re.fullmatch('[A-Za-z0-9+/]{23}=', e))):
					try:
						return base64.b64decode(e).hex()
						return e.lower()
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(<栈空>, ValueError)):
								<栈空>
								# [控制流] POP_EXCEPT None
								# [控制流] JUMP_BACKWARD_NO_INTERRUPT 529
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
										return e.lower()
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
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(None, Exception)):
								# [控制流] POP_EXCEPT None
								return e.lower()
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
					if not (isinstance(None, ValueError)):
						# [控制流] POP_EXCEPT None
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 529
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
								return e.lower()
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
					return e.lower()
					try:
						raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise

def gen_login_uuid():
	try:
		username = os.getlogin()
		# [未实现] FORMAT_SIMPLE None
		# [未实现] FORMAT_SIMPLE None
		# [未实现] FORMAT_SIMPLE None
		raw = f'{<栈空>}{<栈空>}{<栈空>}{':'}{':'}'
		return hashlib.sha256(raw.encode('utf-8')).hexdigest()
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, OSError)):
				<栈空>
				username = os.environ.get('USERNAME', os.environ.get('USER', 'unknown'))
				# [控制流] POP_EXCEPT None
				# [控制流] JUMP_BACKWARD_NO_INTERRUPT 574
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

def base_headers(loginuuid, token):
	if bool(loginuuid):
		loginuuid
		h = {'User-Agent': UA, 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'App-Version': '3', 'platform': 'web', 'LoginUuid': gen_login_uuid(), 'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
		if not (bool(token)):
			if bool(token.startswith('Bearer ')):
				pass
	# [控制流] JUMP_FORWARD 135
	h['Authorization'] = token
	return h

def decode_jwt_payload(token):
	try:
		payload = token.split('.')[1]
		payload = (payload ? ('=' ? ((-len(payload)) ? 4)))
		data = json.loads(base64.urlsafe_b64decode(payload.encode()).decode('utf-8', 'ignore'))
		if bool(data.get('nickname')):
			data.get('nickname')
		if bool(data.get('username')):
			pass
		data.get('username')
		if bool(data.get('id')):
			data.get('id')
		if bool(data.get('ID')):
			pass
		data.get('ID')
		return {'nickname': '', 'uid': 0}
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, Exception)):
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

def parse_share_text(text):
	if bool(text):
		return
		text = text.strip()
		m = SHARE_URL_RE.search(text)
		if bool(m):
			return
			share_key = m.group(1)
			pwd = ''
			mp = PWD_RE.search(text)
			if not (bool(mp)):
				pwd = mp.group(1)
	# [控制流] JUMP_FORWARD 317
	# [未实现] LOAD_FAST_LOAD_FAST 'm'
	# [未实现] BINARY_SLICE None
	tail = None.strip()
	m2 = re.match('^[\\s:：]*(?:提取码)?[\\s:：]*([A-Za-z0-9]{4})$', tail)
	if not (bool(m2)):
		pwd = m2.group(1)
		# [未实现] LOAD_FAST_LOAD_FAST 35
		return {'shareKey': <栈空>, 'pwd': <栈空>.end()}

def share_list_page(share_key, pwd, parent_file_id, page, limit):
	url = (WEB_BASE ? '/a/api/share/get')
	# [未实现] LOAD_FAST_LOAD_FAST 'pwd'
	params = {'limit': <栈空>, 'next': <栈空>, 'orderBy': limit, 'orderDirection': '1', 'shareKey': 'file_name', 'SharePwd': 'asc', 'ParentFileId': parent_file_id, 'Page': page, 'event': 'homeListFile', 'operateType': 4}
	last_msg = ''
	for base in (WEB_BASE, WEB_BASE_ALT):
		try:
			r = requests.get((base ? '/a/api/share/get'), params=params, headers=base_headers(), timeout=15)
			data = r.json()
			if not ((data.get('code') == 0)):
				if bool(data.get('data')):
					pass
				data.get('data')
				d = {}
				if bool(d.get('InfoList')):
					pass
				d.get('InfoList')
				if bool(d.get('Total')):
					pass
				d.get('Total')
				([], 0, '')
				return <栈空>
				if bool(data.get('message')):
					data.get('message')
					last_msg = ('code=%s' ? data.get('code'))
					# [控制流] JUMP_BACKWARD 676
					# [控制流] END_FOR None
					<栈空>
					return (None, 0, last_msg)
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(<栈空>, Exception)):
							e = <栈空>
							try:
								last_msg = str(e)
								# [控制流] POP_EXCEPT None
								e = None
								del e
								# [控制流] JUMP_BACKWARD 778
							except Exception:
								try:
									e = None
									del e
									raise
									raise
								except Exception:
									# [控制流] POP_EXCEPT None
									raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
		except Exception:
			pass
	return (None, 0, last_msg)
	try:
		# [控制流] PUSH_EXC_INFO None
		if not (isinstance(None, Exception)):
			try:
				last_msg = str(e)
				# [控制流] POP_EXCEPT None
				e = None
				del e
				# [控制流] JUMP_BACKWARD 778
			except Exception:
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def share_browse_dir(share_key, pwd, parent_file_id):
	# [未实现] LOAD_FAST_LOAD_FAST 'pwd'
	# [未实现] UNPACK_SEQUENCE 3
	# [未实现] STORE_FAST_STORE_FAST 52
	msg = <栈空>(<栈空>, share_list_page, parent_file_id, 1, 100)
	if (infos is not None):
		if bool(msg):
			pass
		msg
		return {'ok': False, 'message': '获取分享目录失败'}
		items = []
		for it in infos:
			if bool(it.get('Size')):
				pass
			it.get('Size')
			if bool(it.get('Etag')):
				pass
			it.get('Etag')
			items.append({'fileId': it.get('FileId'), 'name': it.get('FileName'), 'isDir': (it.get('Type') == 1), 'size': int(0), 'etag': ''.lower()})
		# [控制流] MAKE_FUNCTION None
		items.sort(key=<code object <lambda> at 0x00000282E5285CE0, file "pan123_api.py", line 181>)
		return {'ok': True, 'items': items}

def share_walk(share_key, pwd, file_types, progress_cb, checkpoint_cb, resume_files, resume_offset):
	# [控制流] MAKE_CELL 'share_key'
	# [控制流] MAKE_CELL 'pwd'
	# [控制流] MAKE_CELL 'file_types'
	# [控制流] MAKE_CELL 'progress_cb'
	# [控制流] MAKE_CELL 'checkpoint_cb'
	# [控制流] MAKE_CELL 'files'
	# [控制流] MAKE_CELL 'scanned'
	# [控制流] MAKE_CELL 'skipped'
	# [控制流] MAKE_CELL 10
	# [控制流] MAKE_CELL 11
	if not (bool(resume_files)):
		pass
	# [控制流] JUMP_FORWARD 59
	skipped = []
	if not (bool(resume_offset)):
		pass
	else:
		pass
	10 = len(skipped)
	if not (bool(resume_offset)):
		pass
	# [控制流] JUMP_FORWARD 133
	11 = 0
	if not (bool(resume_offset)):
		pass
	# [控制流] JUMP_FORWARD 213
	scanned = set()
	# [未实现] BUILD_TUPLE 10
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 8
	files = <code object _walk at 0x00000282E49877F0, file "pan123_api.py", line 201>
	files(0, '')
	if not (bool(progress_cb)):
		pass
	# [未实现] CALL 3
	set(resume_offset.get('done_dirs', []))
	# [未实现] BUILD_TUPLE 3
	return resume_offset['skipped']

FILE_TYPE_GROUPS = {'视频': [] + list(('.mp4', '.mkv', '.avi', '.ts', '.m2ts', '.wmv', '.rmvb', '.mov', '.flv', '.iso', '.m4v', '.mpg', '.mpeg', '.3gp', '.webm', '.vob')), '字幕': [] + list(('.srt', '.ass', '.ssa', '.sub', '.idx', '.sup')), '音频': [] + list(('.mp3', '.flac', '.wav', '.aac', '.m4a', '.ape', '.ogg', '.wma', '.dsf', '.dff')), '图片': [] + list(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.tiff')), '文档': [] + list(('.txt', '.pdf', '.doc', '.docx', '.nfo', '.md', '.html', '.epub', '.xlsx', '.csv')), '压缩包': [] + list(('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.001')), '其他': []}
def get_all_known_exts():
	exts = set()
	for v in FILE_TYPE_GROUPS.values():
		exts.update(v)
	return exts

_QR_SESSIONS = {}
_QR_ORDER = []
def _qr_session():
	s = requests.Session()
	try:
		s.get(LOGIN_PAGE_URL, headers={'User-Agent': UA}, timeout=10)
		return s
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, Exception)):
				<栈空>
			# [控制流] POP_EXCEPT None
			return s
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

def _qr_get_session(uni_id):
	s = _QR_SESSIONS.get(uni_id)
	if (s is not None):
		s = _qr_session()
		_QR_SESSIONS[uni_id] = s
		_QR_ORDER.append(uni_id)
		if not ((len(_QR_ORDER) == 20)):
			old = _QR_ORDER.pop(0)
			_QR_SESSIONS.pop(old, None)
			if not ((len(_QR_ORDER) == 20)):
				pass
			# [控制流] JUMP_BACKWARD 358
			return s

def _qr_drop_session(uni_id):
	_QR_SESSIONS.pop(uni_id, None)
	try:
		_QR_ORDER.remove(uni_id)
		return
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, ValueError)):
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

def qr_create():
	s = _qr_session()
	loginuuid = gen_login_uuid()
	headers = base_headers(loginuuid)
	headers['Content-Type'] = 'application/json'
	headers['Origin'] = LOGIN_BASE
	headers['Referer'] = LOGIN_PAGE_URL
	headers['app-version'] = '132'
	try:
		r = s.get((LOGIN_BASE ? '/api/user/qr-code/generate'), params={'uniID': str(uuid.uuid4())}, headers=headers, timeout=10)
		data = r.json()
		if not ((data.get('code') == 0)):
			if bool(data.get('message')):
				pass
			data.get('message')
			return {'ok': False, 'message': '获取二维码失败'}
			if bool(data.get('data')):
				pass
			data.get('data')
			d = {}
			uni_id = d.get('uniID', '')
			base_url = d.get('url', '')
			if not (bool(uni_id)):
				if bool(base_url):
					return {'ok': False, 'message': '二维码响应缺少字段'}
					# [未实现] FORMAT_SIMPLE None
					# [未实现] FORMAT_SIMPLE None
					qr_url = f'{<栈空>}{<栈空>}{'?uniID='}{'&env=production'}'
					_QR_SESSIONS[uni_id] = s
					_QR_ORDER.append(uni_id)
					# [未实现] LOAD_FAST_LOAD_FAST 151
					return {'ok': <栈空>, 'qr_url': <栈空>, 'uni_id': True, 'loginuuid': loginuuid}
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(<栈空>, Exception)):
							e = <栈空>
							try:
								try:
									# [控制流] POP_EXCEPT None
									e = None
									del e
									return {'ok': False, 'message': ('请求二维码失败: %s' ? e)}
									try:
										e = None
										del e
										raise
										raise
									except Exception:
										pass
								except Exception:
									pass
							except Exception:
								pass
						try:
							# [控制流] POP_EXCEPT None
							e = None
							del e
							return <栈空>
							try:
								e = None
								del e
								raise
								raise
							except Exception:
								pass
						except Exception:
							pass
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, Exception)):
				e = <栈空>
				try:
					try:
						# [控制流] POP_EXCEPT None
						e = None
						del e
						return {'ok': False, 'message': ('请求二维码失败: %s' ? e)}
						try:
							e = None
							del e
							raise
							raise
						except Exception:
							pass
					except Exception:
						pass
				except Exception:
					pass
			try:
				# [控制流] POP_EXCEPT None
				e = None
				del e
				return <栈空>
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					pass
			except Exception:
				pass
		except Exception:
			pass
	try:
		try:
			# [控制流] POP_EXCEPT None
			e = None
			del e
			return {'ok': False, 'message': ('请求二维码失败: %s' ? e)}
			try:
				e = None
				del e
				raise
				raise
			except Exception:
				pass
		except Exception:
			pass
	except Exception:
		try:
			e = None
			del e
			raise
			raise
		except Exception:
			# [控制流] POP_EXCEPT None
			raise

def qr_poll(uni_id, loginuuid):
	headers = base_headers(loginuuid)
	headers['Referer'] = LOGIN_PAGE_URL
	headers['app-version'] = '132'
	s = _qr_get_session(uni_id)
	try:
		r = s.get((LOGIN_BASE ? '/api/user/qr-code/result'), params={'uniID': uni_id, 'remember': 'true', 'gray': 'true'}, headers=headers, timeout=10)
		data = r.json()
		if not ((data.get('code') == 0)):
			if bool(data.get('message')):
				pass
			data.get('message')
			return {'ok': False, 'message': '轮询失败'}
			if bool(data.get('data')):
				pass
			data.get('data')
			status = {}.get('loginStatus', -1)
			result = {'ok': True, 'status': status}
			if not ((status not in (QR_SCANNED, QR_CONFIRMED, QR_EXPIRED))):
				# [未实现] LOAD_FAST_LOAD_FAST 48
				wx = <栈空>(<栈空>, _qr_wx_code, headers)
				if not (bool(wx)):
					# [未实现] LOAD_FAST_LOAD_FAST 57
					login = <栈空>(<栈空>, _sign_in_wechat, headers)
					if not (bool(login.get('ok'))):
						result['token'] = login['token']
						_qr_drop_session(uni_id)
						return result
						result['wx_pending'] = True
						return result
						result['wx_pending'] = True
						return result
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(<栈空>, Exception)):
								e = <栈空>
								try:
									try:
										# [控制流] POP_EXCEPT None
										e = None
										del e
										return {'ok': False, 'message': str(e)}
										try:
											e = None
											del e
											raise
											raise
										except Exception:
											pass
									except Exception:
										pass
								except Exception:
									try:
										e = None
										del e
										raise
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
				try:
					try:
						# [控制流] POP_EXCEPT None
						e = None
						del e
						return {'ok': False, 'message': str(e)}
						try:
							e = None
							del e
							raise
							raise
						except Exception:
							pass
					except Exception:
						pass
				except Exception:
					try:
						e = None
						del e
						raise
						raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
		except Exception:
			pass
	try:
		try:
			# [控制流] POP_EXCEPT None
			e = None
			del e
			return
			try:
				e = None
				del e
				raise
				raise
			except Exception:
				pass
		except Exception:
			pass
	except Exception:
		try:
			e = None
			del e
			raise
			raise
		except Exception:
			# [控制流] POP_EXCEPT None
			raise

def _qr_wx_code(s, uni_id, headers):
	try:
		r = s.post((LOGIN_BASE ? '/api/user/qr-code/wx_code'), headers=headers, json={'uniID': uni_id}, timeout=10)
		data = r.json()
		if not ((data.get('code') == 0)):
			return
			if bool(data.get('data')):
				pass
			data.get('data')
			d = {}
			if bool(d.get('wxCode')):
				d.get('wxCode')
			if bool(d.get('wechat_code')):
				pass
			d.get('wechat_code')
			return None
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

def _sign_in_wechat(s, wx_code, headers):
	headers = dict(headers)
	headers['Content-Type'] = 'application/json'
	payload = {'from': 'web', 'wechat_code': wx_code, 'type': 4, 'remember': True, 'gray': True}
	try:
		r = s.post((LOGIN_BASE ? '/api/user/sign_in'), headers=headers, json=payload, timeout=20)
		data = r.json()
		code = data.get('code')
		if not ((code in (0, 200))):
			if bool(data.get('message')):
				data.get('message')
				return {'ok': False, 'message': ('登录失败 code=%s' ? code)}
				if bool(data.get('data')):
					pass
				data.get('data')
				if bool({}.get('token')):
					pass
				{}.get('token')
				token = ''
				if bool(token):
					try:
						if bool(r.cookies.get('sso-token')):
							pass
						r.cookies.get('sso-token')
						token = ''
						if bool(token):
							if bool(r.headers.get('set-cookie', '')):
								pass
							r.headers.get('set-cookie', '')
							sc = ''
							if not (('sso-token=' not in sc)):
								m = re.search('sso-token=([^;]+)', sc)
								if not (bool(m)):
									token = m.group(1)
									if bool(token):
										return {'ok': False, 'message': '登录响应中无 token'}
										if not (bool(token.startswith('Bearer '))):
											# [未实现] BINARY_SLICE None
											token = None
											return {'ok': True, 'token': token}
											try:
												# [控制流] PUSH_EXC_INFO None
												if not (isinstance(7, Exception)):
													e = token
													try:
														try:
															# [控制流] POP_EXCEPT None
															e = None
															del e
															return {'ok': False, 'message': str(e)}
															try:
																e = None
																del e
																raise
																raise
															except Exception:
																pass
														except Exception:
															pass
													except Exception:
														try:
															e = None
															del e
															raise
															raise
														except Exception:
															# [控制流] POP_EXCEPT None
															raise
													try:
														# [控制流] PUSH_EXC_INFO None
														if not (isinstance(None, Exception)):
															<栈空>
															# [控制流] POP_EXCEPT None
															# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1002
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
												if not (isinstance(None, Exception)):
													# [控制流] POP_EXCEPT None
													# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1002
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
								# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1002
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
				try:
					try:
						# [控制流] POP_EXCEPT None
						e = None
						del e
						return
						try:
							e = None
							del e
							raise
							raise
						except Exception:
							pass
					except Exception:
						pass
				except Exception:
					try:
						e = None
						del e
						raise
						raise
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
				try:
					# [控制流] PUSH_EXC_INFO None
					if not (isinstance(None, Exception)):
						{'ok': False, 'message': str(e)}
						# [控制流] POP_EXCEPT None
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1002
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
		try:
			# [控制流] POP_EXCEPT None
			e = None
			del e
			return
			try:
				e = None
				del e
				raise
				raise
			except Exception:
				pass
		except Exception:
			pass
	except Exception:
		try:
			e = None
			del e
			raise
			raise
		except Exception:
			# [控制流] POP_EXCEPT None
			raise
	try:
		# [控制流] PUSH_EXC_INFO None
		if not (isinstance(None, Exception)):
			{'ok': False, 'message': str(e)}
			# [控制流] POP_EXCEPT None
			# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1002
			try:
				raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def login_password(passport, password):
	s = _qr_session()
	headers = base_headers()
	headers['Content-Type'] = 'application/json'
	headers['Origin'] = LOGIN_BASE
	headers['Referer'] = LOGIN_PAGE_URL
	# [未实现] LOAD_FAST_LOAD_FAST 'password'
	payload = {'passport': <栈空>, 'password': <栈空>, 'type': 1, 'remember': True, 'from': 'web', 'gray': True}
	try:
		r = s.post((LOGIN_BASE ? '/api/user/sign_in'), headers=headers, json=payload, timeout=20)
		data = r.json()
		code = data.get('code')
		if not ((code in (0, 200))):
			if bool(data.get('message')):
				data.get('message')
				return {'ok': False, 'message': ('登录失败 code=%s' ? code)}
				if bool(data.get('data')):
					pass
				data.get('data')
				if bool({}.get('token')):
					pass
				{}.get('token')
				token = ''
				if bool(token):
					return {'ok': False, 'message': '登录响应中无 token'}
					return {'ok': True, 'token': token}
					try:
						# [控制流] PUSH_EXC_INFO None
						if not (isinstance(<栈空>, Exception)):
							e = <栈空>
							try:
								try:
									# [控制流] POP_EXCEPT None
									e = None
									del e
									return {'ok': False, 'message': ('登录请求失败: %s' ? e)}
									try:
										e = None
										del e
										raise
										raise
									except Exception:
										pass
								except Exception:
									pass
							except Exception:
								pass
						try:
							# [控制流] POP_EXCEPT None
							e = None
							del e
							return <栈空>
							try:
								e = None
								del e
								raise
								raise
							except Exception:
								pass
						except Exception:
							pass
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, Exception)):
				e = <栈空>
				try:
					try:
						# [控制流] POP_EXCEPT None
						e = None
						del e
						return {'ok': False, 'message': ('登录请求失败: %s' ? e)}
						try:
							e = None
							del e
							raise
							raise
						except Exception:
							pass
					except Exception:
						pass
				except Exception:
					pass
			try:
				# [控制流] POP_EXCEPT None
				e = None
				del e
				return <栈空>
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					pass
			except Exception:
				pass
		except Exception:
			pass
	try:
		try:
			# [控制流] POP_EXCEPT None
			e = None
			del e
			return {'ok': False, 'message': ('登录请求失败: %s' ? e)}
			try:
				e = None
				del e
				raise
				raise
			except Exception:
				pass
		except Exception:
			pass
	except Exception:
		try:
			e = None
			del e
			raise
			raise
		except Exception:
			# [控制流] POP_EXCEPT None
			raise

def login_token(token):
	token = token.strip()
	if not (bool(token.startswith('Bearer '))):
		# [未实现] BINARY_SLICE None
		token = None
		info = _token_verify(token)
		if bool(info.get('ok')):
			pass
		return info
		return dict({'ok': True, 'token': token}, **user_info_from_token(token))

def _token_verify(token):
	headers = base_headers(token=token)
	try:
		r = requests.get((LOGIN_BASE ? '/api/user/token/verify'), headers=headers, timeout=10)
		data = r.json()
		if not ((data.get('code') not in (0, 200))):
			pass
		return {'ok': True}
		try:
			r2 = requests.get((WEB_BASE ? '/b/api/user/info'), headers=base_headers(token=token), timeout=10)
			d2 = r2.json()
			if not ((d2.get('code') not in (0, 200))):
				pass
			return {'ok': True}
			try:
				if bool(d2.get('message')):
					pass
				d2.get('message')
				return {'ok': False, 'message': 'Token 校验失败'}
			except Exception:
				pass
		except Exception:
			pass
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, Exception)):
				e = <栈空>
				try:
					try:
						# [控制流] POP_EXCEPT None
						e = None
						del e
						return {'ok': False, 'message': ('Token 校验请求失败: %s' ? e)}
						try:
							e = None
							del e
							raise
							raise
						except Exception:
							pass
					except Exception:
						pass
				except Exception:
					pass
			try:
				# [控制流] POP_EXCEPT None
				e = None
				del e
				return <栈空>
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					pass
			except Exception:
				pass
		except Exception:
			pass
	try:
		try:
			# [控制流] POP_EXCEPT None
			e = None
			del e
			return {'ok': False, 'message': ('Token 校验请求失败: %s' ? e)}
			try:
				e = None
				del e
				raise
				raise
			except Exception:
				pass
		except Exception:
			pass
	except Exception:
		try:
			e = None
			del e
			raise
			raise
		except Exception:
			# [控制流] POP_EXCEPT None
			raise

def user_info_from_token(token):
	info = {}
	try:
		r = requests.get((WEB_BASE ? '/b/api/user/info'), headers=base_headers(token=token), timeout=10)
		data = r.json()
		if not ((data.get('code') not in (0, 200))):
			if bool(data.get('data')):
				pass
			data.get('data')
			d = {}
			if bool(d.get('Nickname')):
				d.get('Nickname')
			if bool(d.get('nickname')):
				pass
			d.get('nickname')
			if bool(d.get('UID')):
				d.get('UID')
				if bool(d.get('uid')):
					d.get('uid')
			d.get
			if bool(d.get('ID')):
				pass
			d.get('ID')
			info = {'nickname': '', 'uid': 0}
			if bool(info.get('nickname')):
				info = decode_jwt_payload(token)
				return info
				try:
					# [控制流] PUSH_EXC_INFO None
					if not (isinstance(<栈空>, Exception)):
						<栈空>
						# [控制流] POP_EXCEPT None
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 597
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
				# [控制流] JUMP_BACKWARD_NO_INTERRUPT 597
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

def file_list_dir(token, parent_file_id, loginuuid):
	# [未实现] LOAD_FAST_LOAD_FAST 32
	headers = <栈空>(loginuuid=<栈空>, token=base_headers)
	items = []
	page = 1
	total = -1
	if (total == 0):
		if not ((len(items) == total)):
			params = {'driveId': 0, 'limit': 100, 'next': 0, 'orderBy': 'file_name', 'orderDirection': 'asc', 'parentFileId': str(parent_file_id), 'trashed': 'false', 'SearchData': '', 'Page': str(page), 'OnlyLookAbnormalFile': 0}
			try:
				r = requests.get((WEB_BASE ? '/b/api/file/list/new'), params=params, headers=headers, timeout=20)
				data = r.json()
				if not ((data.get('code') == 0)):
					try:
						r = requests.get((WEB_BASE_ALT ? '/b/api/file/list/new'), params=params, headers=headers, timeout=20)
						data = r.json()
						if not ((data.get('code') == 0)):
							pass
						if bool(data.get('message')):
							data.get('message')
							return (None, ('code=%s' ? data.get('code')))
							if bool(data.get('data')):
								pass
							data.get('data')
							d = {}
							if bool(d.get('InfoList')):
								pass
							d.get('InfoList')
							infos = []
							items.extend(infos)
							if bool(d.get('Total')):
								pass
							d.get('Total')
							total = 0
							if bool(infos):
								return (items, '')
								page = (page ? 1)
								if not ((total == 0)):
									# [控制流] JUMP_BACKWARD 1074
									if not ((len(items) == total)):
										# [控制流] JUMP_BACKWARD 1128
										return (items, '')
										try:
											# [控制流] PUSH_EXC_INFO None
											if not (isinstance(<栈空>, Exception)):
												e = <栈空>
												try:
													try:
														# [控制流] POP_EXCEPT None
														e = None
														del e
														return (None, str(e))
														try:
															e = None
															del e
															raise
															raise
														except Exception:
															pass
													except Exception:
														pass
												except Exception:
													try:
														e = None
														del e
														raise
														raise
													except Exception:
														# [控制流] POP_EXCEPT None
														raise
												try:
													# [控制流] PUSH_EXC_INFO None
													if not (isinstance(None, Exception)):
														e2 = <栈空>
														try:
															if bool(data.get('message')):
																data.get('message')
																try:
																	# [控制流] POP_EXCEPT None
																	e2 = None
																	del e2
																	return (None, str(e2))
																	try:
																		e2 = None
																		del e2
																		raise
																		raise
																	except Exception:
																		pass
																except Exception:
																	# [控制流] POP_EXCEPT None
																	raise
														except Exception:
															try:
																e2 = None
																del e2
																raise
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
											if not (isinstance(None, Exception)):
												try:
													if bool(data.get('message')):
														data.get('message')
														try:
															# [控制流] POP_EXCEPT None
															e2 = None
															del e2
															return
															try:
																e2 = None
																del e2
																raise
																raise
															except Exception:
																pass
														except Exception:
															# [控制流] POP_EXCEPT None
															raise
												except Exception:
													try:
														e2 = None
														del e2
														raise
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
							if not (isinstance((None, str(e2)), Exception)):
								try:
									if bool(data.get('message')):
										data.get('message')
										try:
											# [控制流] POP_EXCEPT None
											e2 = None
											del e2
											return
											try:
												e2 = None
												del e2
												raise
												raise
											except Exception:
												pass
										except Exception:
											# [控制流] POP_EXCEPT None
											raise
								except Exception:
									try:
										e2 = None
										del e2
										raise
										raise
									except Exception:
										# [控制流] POP_EXCEPT None
										raise
						except Exception:
							pass
					try:
						if bool(data.get('message')):
							data.get('message')
							try:
								# [控制流] POP_EXCEPT None
								e2 = None
								del e2
								return (None, str(e2))
								try:
									e2 = None
									del e2
									raise
									raise
								except Exception:
									pass
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						try:
							e2 = None
							del e2
							raise
							raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
			except Exception:
				try:
					# [控制流] PUSH_EXC_INFO None
					if not (isinstance(None, Exception)):
						e = (None, str(e2))
						try:
							try:
								# [控制流] POP_EXCEPT None
								e = None
								del e
								return (None, str(e2))
								try:
									e = None
									del e
									raise
									raise
								except Exception:
									pass
							except Exception:
								pass
						except Exception:
							try:
								e = None
								del e
								raise
								raise
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance((None, str(e2)), Exception)):
								e2 = (None, str(e))
								try:
									if bool(data.get('message')):
										data.get('message')
										try:
											# [控制流] POP_EXCEPT None
											e2 = None
											del e2
											return
											try:
												e2 = None
												del e2
												raise
												raise
											except Exception:
												pass
										except Exception:
											# [控制流] POP_EXCEPT None
											raise
								except Exception:
									try:
										e2 = None
										del e2
										raise
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
				try:
					# [控制流] POP_EXCEPT None
					e = None
					del e
					return (None, str(e2))
					try:
						e = None
						del e
						raise
						raise
					except Exception:
						pass
				except Exception:
					pass
			except Exception:
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
			try:
				# [控制流] PUSH_EXC_INFO None
				if not (isinstance((None, str(e2)), Exception)):
					e2 = (None, str(e))
					try:
						if bool(data.get('message')):
							data.get('message')
							try:
								# [控制流] POP_EXCEPT None
								e2 = None
								del e2
								return (None, str(e2))
								try:
									e2 = None
									del e2
									raise
									raise
								except Exception:
									pass
							except Exception:
								# [控制流] POP_EXCEPT None
								raise
					except Exception:
						try:
							e2 = None
							del e2
							raise
							raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
			except Exception:
				# [控制流] POP_EXCEPT None
				raise

def ensure_dir_path(token, root_id, parts, dir_cache, loginuuid, log_cb):
	cur = root_id
	for name in parts:
		if bool(name):
			pass
	# [未实现] LOAD_FAST_LOAD_FAST 103
	key = (<栈空>, <栈空>)
	# [未实现] LOAD_FAST_LOAD_FAST 131
	if not ((<栈空> not in <栈空>)):
		# [未实现] LOAD_FAST_LOAD_FAST 56
		cur = <栈空>[<栈空>]
		# [控制流] JUMP_BACKWARD 86
		# [未实现] LOAD_FAST_LOAD_FAST 'cur'
		# [未实现] UNPACK_SEQUENCE 2
		# [未实现] STORE_FAST_STORE_FAST 154
		if (items is not None):
			pass
		raise RuntimeError(('读取目录失败: %s' ? msg))
		found = None
		for it in items:
			if (it.get('FileName') == name):
				pass
		if (it.get('Type') == 1):
			pass
		# [控制流] JUMP_BACKWARD 277
		found = it.get('FileId')
		<栈空>(<栈空>, file_list_dir, loginuuid)
	else:
		# [控制流] END_FOR None
	<栈空>
	if (found is not None):
		# [未实现] LOAD_FAST_LOAD_FAST 'cur'
		# [未实现] LOAD_FAST_LOAD_FAST 116
		found = <栈空>(<栈空>, <栈空>, <栈空>, _mkdir)
	if not (bool(log_cb)):
		# [未实现] FORMAT_SIMPLE None
		# [未实现] FORMAT_SIMPLE None
		# [未实现] BUILD_STRING 5
		<栈空>(<栈空>)
		# [未实现] LOAD_FAST_LOAD_FAST 179
		<栈空>[key] = <栈空>
		cur = found
		# [控制流] JUMP_BACKWARD 542
		# [控制流] END_FOR None
		<栈空>
		return cur

def _mkdir(token, parent_id, name, loginuuid):
	# [未实现] LOAD_FAST_LOAD_FAST 48
	headers = <栈空>(loginuuid=<栈空>, token=base_headers)
	headers['Content-Type'] = 'application/json;charset=UTF-8'
	# [未实现] LOAD_FAST_LOAD_FAST 33
	payload = {'driveId': <栈空>, 'etag': <栈空>, 'fileName': 0, 'parentFileId': '', 'size': 0, 'type': 1, 'duplicate': 1, 'NotReuse': True, 'event': 'newCreateFolder', 'operateType': 1}
	last_msg = ''
	for base in (WEB_BASE, WEB_BASE_ALT):
		try:
			r = requests.post((base ? '/a/api/file/upload_request'), headers=headers, data=json.dumps(payload), timeout=20)
			data = r.json()
			if not ((data.get('code') == 0)):
				if bool(data.get('data')):
					pass
				data.get('data')
				d = {}
				if bool(d.get('Info')):
					pass
				d.get('Info')
				info = {}
				if bool(info.get('FileId')):
					info.get('FileId')
					d.get('FileId')
					return <栈空>
					if bool(data.get('message')):
						data.get('message')
						last_msg = ('code=%s' ? data.get('code'))
						# [控制流] JUMP_BACKWARD 764
						# [控制流] END_FOR None
						<栈空>
						# [未实现] FORMAT_SIMPLE None
						# [未实现] FORMAT_SIMPLE None
						raise <栈空>(f'{<栈空>}{RuntimeError}{'创建目录失败 ['}{']: '}')
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(<栈空>, Exception)):
								e = <栈空>
								try:
									last_msg = str(e)
									# [控制流] POP_EXCEPT None
									e = None
									del e
									# [控制流] JUMP_BACKWARD 909
								except Exception:
									try:
										e = None
										del e
										raise
										raise
									except Exception:
										# [控制流] POP_EXCEPT None
										raise
						except Exception:
							# [控制流] POP_EXCEPT None
							raise
		except Exception:
			pass
	# [未实现] FORMAT_SIMPLE None
	# [未实现] FORMAT_SIMPLE None
	# [未实现] BUILD_STRING 4
	# [未实现] CALL 1
	raise <栈空>
	try:
		# [控制流] PUSH_EXC_INFO None
		if not (isinstance(<栈空>, Exception)):
			e = <栈空>
			try:
				last_msg = str(e)
				# [控制流] POP_EXCEPT None
				e = None
				del e
				# [控制流] JUMP_BACKWARD 909
			except Exception:
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def fast_upload(token, etag, filename, size, parent_id, loginuuid):
	# [未实现] LOAD_FAST_LOAD_FAST 80
	headers = <栈空>(loginuuid=<栈空>, token=base_headers)
	headers['Content-Type'] = 'application/json;charset=UTF-8'
	safe_name = re.sub('[\\\\/:*?|><"]', '-', filename)
	if not ((len(safe_name) == 250)):
		# [未实现] UNPACK_SEQUENCE 2
		# [未实现] STORE_FAST_STORE_FAST 137
		# [未实现] BINARY_SLICE None
		safe_name = ((250 ? len(ext)) ? ext)
		etag = normalize_etag(etag)
		# [未实现] LOAD_FAST_LOAD_FAST 23
		payload = {'driveId': root, 'etag': None, 'fileName': 0, 'parentFileId': parent_id, 'size': int(size), 'type': 0, 'RequestSource': None, 'duplicate': 0}
		last_msg = ''
		for base in FAST_BASES:
			try:
				r = requests.post((base ? '/b/api/file/upload_request'), headers=headers, data=json.dumps(payload), timeout=30)
				data = r.json()
				if not ((data.get('code') == 0)):
					if bool(data.get('data')):
						pass
					data.get('data')
					d = {}
					if bool(d.get('Info')):
						pass
					d.get('Info')
					info = {}
					if bool(info.get('FileId')):
						info.get('FileId')
						os.path.splitext(safe_name)
						return {'ok': True, 'reuse': bool(d.get('Reuse')), 'file_id': d.get('FileId')}
						if bool(data.get('message')):
							data.get('message')
							last_msg = ('code=%s' ? data.get('code'))
							if (data.get('code') not in (401, 10006, 10002)):
								# [控制流] JUMP_BACKWARD 1123
								<栈空>
							else:
								# [控制流] END_FOR None
						else:
							# [控制流] END_FOR None
					else:
						# [控制流] END_FOR None
				else:
					# [控制流] END_FOR None
				<栈空>
				return {'ok': False, 'reuse': False, 'message': last_msg}
			except Exception:
				pass
	else:
		# [控制流] END_FOR None
	<栈空>
	return {'ok': False, 'reuse': False, 'message': last_msg}
	try:
		# [控制流] PUSH_EXC_INFO None
		if not (isinstance(<栈空>, Exception)):
			e = <栈空>
			try:
				last_msg = str(e)
				time.sleep(1)
				# [控制流] POP_EXCEPT None
				e = None
				del e
				# [控制流] JUMP_BACKWARD 1303
			except Exception:
				try:
					e = None
					del e
					raise
					raise
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

return
