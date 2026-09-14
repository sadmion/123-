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
		if (idx == 0):
			pass
		raise ValueError(('非 base62 字符: %r' ? c))
		num = ((num ? 62) ? idx)
		# [控制流] JUMP_BACKWARD 170
		# [控制流] END_FOR None
		<栈空>
		return format(num, 'x').zfill(32)

def normalize_etag(etag):
	if not (bool(etag)):
		pass
	etag
	e = ''.strip().strip('"')
	if bool(re.fullmatch('[0-9a-fA-F]{32}', e)):
		return e.lower()
		if bool(re.fullmatch('[A-Za-z0-9]{15,22}', e)):
			try:
				return base62_to_hex(e)
				if bool(re.fullmatch('[A-Za-z0-9+/]{23}=', e)):
					try:
						return base64.b64decode(e).hex()
						return e.lower()
						try:
							if isinstance(<栈空>, ValueError):
								<栈空>
								raise
								raise
								isinstance(None, Exception)
								return e.lower()
								raise
								raise
						except Exception:
							pass
					except Exception:
						return e.lower()
					raise
			except ValueError:
				# [控制流] JUMP_BACKWARD_NO_INTERRUPT 529
			raise
			if isinstance(None, Exception):
				return e.lower()
				raise
				raise

def gen_login_uuid():
	try:
		username = os.getlogin()
		raw = f'{str(socket.gethostname())}{':'}{str(username)}{':'}{str(_platform.system())}'
		return hashlib.sha256(raw.encode('utf-8')).hexdigest()
	except OSError:
		username = os.environ.get('USERNAME', os.environ.get('USER', 'unknown'))
	# [控制流] JUMP_BACKWARD_NO_INTERRUPT 574
	raise
	raise

def base_headers(loginuuid, token):
	if not (bool(loginuuid)):
		loginuuid
		h = {'User-Agent': UA, 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'App-Version': '3', 'platform': 'web', 'LoginUuid': gen_login_uuid(), 'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
		if bool(token):
			if not (bool(token.startswith('Bearer '))):
				pass
	# [控制流] JUMP_FORWARD 135
	h['Authorization'] = token
	return h

def decode_jwt_payload(token):
	try:
		payload = token.split('.')[1]
		payload = (payload ? ('=' ? ((-len(payload)) ? 4)))
		data = json.loads(base64.urlsafe_b64decode(payload.encode()).decode('utf-8', 'ignore'))
		if not (bool(data.get('nickname'))):
			data.get('nickname')
		if not (bool(data.get('username'))):
			pass
		data.get('username')
		if not (bool(data.get('id'))):
			data.get('id')
		if not (bool(data.get('ID'))):
			pass
		data.get('ID')
		return {'nickname': '', 'uid': 0}
	except Exception:
		pass
	return {}
	raise
	raise

def parse_share_text(text):
	if not (bool(text)):
		return
		text = text.strip()
		m = SHARE_URL_RE.search(text)
		if not (bool(m)):
			return
			share_key = m.group(1)
			pwd = ''
			mp = PWD_RE.search(text)
			if bool(mp):
				pwd = mp.group(1)
	# [控制流] JUMP_FORWARD 317
	# [未实现] LOAD_FAST_LOAD_FAST 'm'
	tail = <栈空>[<栈空>.end():None].strip()
	m2 = re.match('^[\\s:：]*(?:提取码)?[\\s:：]*([A-Za-z0-9]{4})$', tail)
	if bool(m2):
		pwd = m2.group(1)
		# [未实现] LOAD_FAST_LOAD_FAST 35
		return {'shareKey': <栈空>, 'pwd': <栈空>}

def share_list_page(share_key, pwd, parent_file_id, page, limit):
	url = (WEB_BASE ? '/a/api/share/get')
	# [未实现] LOAD_FAST_LOAD_FAST 'pwd'
	params = {'limit': <栈空>, 'next': <栈空>, 'orderBy': limit, 'orderDirection': '1', 'shareKey': 'file_name', 'SharePwd': 'asc', 'ParentFileId': parent_file_id, 'Page': page, 'event': 'homeListFile', 'operateType': 4}
	last_msg = ''
	for base in (WEB_BASE, WEB_BASE_ALT):
		try:
			r = requests.get((base ? '/a/api/share/get'), params=params, headers=base_headers(), timeout=15)
			data = r.json()
			if (data.get('code') == 0):
				if not (bool(data.get('data'))):
					pass
				data.get('data')
				d = {}
				if not (bool(d.get('InfoList'))):
					pass
				d.get('InfoList')
				if not (bool(d.get('Total'))):
					pass
				d.get('Total')
				([], 0, '')
				return <栈空>
				if not (bool(data.get('message'))):
					data.get('message')
					last_msg = ('code=%s' ? data.get('code'))
					# [控制流] JUMP_BACKWARD 676
					# [控制流] END_FOR None
					<栈空>
					return (None, 0, last_msg)
					if isinstance(<栈空>, Exception):
						e = <栈空>
						last_msg = str(e)
						e = None
						del e
						# [控制流] JUMP_BACKWARD 778
						e = None
						del e
						raise
						raise
						raise
		except Exception:
			last_msg = str(e)
		e = None
		del e
		# [控制流] JUMP_BACKWARD 778
		e = None
		del e
		raise
		raise
		raise

def share_browse_dir(share_key, pwd, parent_file_id):
	# [未实现] LOAD_FAST_LOAD_FAST 'pwd'
	# [未实现] STORE_FAST_STORE_FAST 52
	msg = __unpack2_of_3(<栈空>(<栈空>, share_list_page, parent_file_id, 1, 100))
	if (infos is None):
		if not (bool(msg)):
			pass
		msg
		return {'ok': False, 'message': '获取分享目录失败'}
		items = []
		for it in infos:
			if not (bool(it.get('Size'))):
				pass
			it.get('Size')
			if not (bool(it.get('Etag'))):
				pass
			it.get('Etag')
			items.append({'fileId': it.get('FileId'), 'name': it.get('FileName'), 'isDir': (it.get('Type') == 1), 'size': int(0), 'etag': ''.lower()})
			# [控制流] JUMP_BACKWARD 517
			# [控制流] END_FOR None
			__unpack1_of_3(<栈空>(<栈空>, share_list_page, parent_file_id, 1, 100))
			items.sort(key=<code object <lambda> at 0x000002384EC75F00, file "pan123_api.py", line 181>)
			return {'ok': True, 'items': items}

def share_walk(share_key, pwd, file_types, progress_cb, checkpoint_cb, resume_files, resume_offset):
	if bool(resume_files):
		pass
	# [控制流] JUMP_FORWARD 59
	file_types = []
	if bool(resume_offset):
		pass
	else:
		pass
	progress_cb = len(file_types)
	if bool(resume_offset):
		pass
	# [控制流] JUMP_FORWARD 133
	checkpoint_cb = 0
	if bool(resume_offset):
		pass
	# [控制流] JUMP_FORWARD 213
	pwd = set()
	# [未实现] BUILD_TUPLE 10
	def share_key(parent_id, path):
		page = 1
		# [未实现] LOAD_FAST_LOAD_FAST 'page'
		# [未实现] STORE_FAST_STORE_FAST 52
		msg = __unpack2_of_3(<栈空>(<栈空>, share_list_page, share_key, pwd, 100))
		if (infos is None):
			if not (bool(path)):
				pass
			path
			raise RuntimeError(f'{'遍历分享目录失败: '}{str(msg)}{' (位于 '}{str('根目录')}{')'}')
			for it in infos:
				if not (bool(it.get('FileName'))):
					pass
				it.get('FileName')
				name = ''
				if bool(path):
					pass
				# [控制流] JUMP_FORWARD 203
				item_path = name
				if (it.get('Type') == 1):
					fid = it.get('FileId')
					if (fid not in done_dirs):
						pass
					# [控制流] JUMP_BACKWARD 389
					# [未实现] LOAD_FAST_LOAD_FAST 152
					# [未实现] CALL 2
					__unpack1_of_3(<栈空>(<栈空>, share_list_page, share_key, pwd, 100))
					done_dirs.add(fid)
					if bool(checkpoint_cb):
						pass
					checkpoint_cb(files, scanned, skipped, list(done_dirs))
					# [控制流] JUMP_BACKWARD 551
					# [控制流] JUMP_BACKWARD 557
					scanned = (scanned ? 1)
					ext = os.path.splitext(name)[1].lower()
					if (file_types is not None):
						if (ext in file_types):
							skipped = (skipped ? 1)
							# [控制流] JUMP_BACKWARD 764
							if not (bool(it.get('Etag'))):
								pass
							it.get('Etag')
							etag = ''.lower()
							if bool(etag):
								# [未实现] LOAD_FAST_LOAD_FAST 139
								bool(it.get('Size'))
							__unpack0_of_3(<栈空>(<栈空>, share_list_page, share_key, pwd, 100))({'path': files.append, 'etag': int, 'size': it.get('Size')(0)})
							if ((len(files) ? 500) == 0):
								checkpoint_cb(files, scanned, skipped, list(done_dirs))
								progress_cb(scanned, skipped, item_path)
								# [控制流] END_FOR None
								((scanned ? 50) == 0)
								return
								page = (page ? 1)
								checkpoint_cb(files, scanned, skipped, list(done_dirs))
								bool(path)
								scanned(skipped, path, '根目录')
		# [控制流] JUMP_FORWARD 203
		item_path = name
		if (it.get('Type') == 1):
			fid = it.get('FileId')
			if (fid not in done_dirs):
				pass
			# [控制流] JUMP_BACKWARD 389
			# [未实现] LOAD_FAST_LOAD_FAST 152
			# [未实现] CALL 2
			bool(progress_cb)
			done_dirs.add(fid)
			if bool(checkpoint_cb):
				pass
			checkpoint_cb(files, scanned, skipped, list(done_dirs))
			# [控制流] JUMP_BACKWARD 551
			# [控制流] JUMP_BACKWARD 557
			scanned = (scanned ? 1)
			ext = os.path.splitext(name)[1].lower()
			if (file_types is not None):
				if (ext in file_types):
					skipped = (skipped ? 1)
					# [控制流] JUMP_BACKWARD 764
					if not (bool(it.get('Etag'))):
						pass
					it.get('Etag')
					etag = ''.lower()
					if bool(etag):
						# [未实现] LOAD_FAST_LOAD_FAST 139
						if not (bool(it.get('Size'))):
							pass
						it.get('Size')
					(len(infos) == 100)({'path': bool(checkpoint_cb), 'etag': files.append, 'size': int(0)})
					if ((len(files) ? 500) == 0):
						if bool(checkpoint_cb):
							checkpoint_cb(files, scanned, skipped, list(done_dirs))
							if not (bool(progress_cb)):
								progress_cb(scanned, skipped, item_path)
								# [控制流] END_FOR None
								((scanned ? 50) == 0)
								return
								page = (page ? 1)
								checkpoint_cb(files, scanned, skipped, list(done_dirs))
								bool(path)
								scanned(skipped, path, '根目录')
	share_key(0, '')
	if bool(progress_cb):
		pass
	progress_cb(progress_cb, checkpoint_cb, '完成')
	return (file_types, progress_cb, checkpoint_cb)

FILE_TYPE_GROUPS = {'视频': [] + list(('.mp4', '.mkv', '.avi', '.ts', '.m2ts', '.wmv', '.rmvb', '.mov', '.flv', '.iso', '.m4v', '.mpg', '.mpeg', '.3gp', '.webm', '.vob')), '字幕': [] + list(('.srt', '.ass', '.ssa', '.sub', '.idx', '.sup')), '音频': [] + list(('.mp3', '.flac', '.wav', '.aac', '.m4a', '.ape', '.ogg', '.wma', '.dsf', '.dff')), '图片': [] + list(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.tiff')), '文档': [] + list(('.txt', '.pdf', '.doc', '.docx', '.nfo', '.md', '.html', '.epub', '.xlsx', '.csv')), '压缩包': [] + list(('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.001')), '其他': []}
def get_all_known_exts():
	exts = set()
	for v in FILE_TYPE_GROUPS.values():
		exts.update(v)
		# [控制流] JUMP_BACKWARD 126
		# [控制流] END_FOR None
		<栈空>
		return exts

_QR_SESSIONS = {}
_QR_ORDER = []
def _qr_session():
	s = requests.Session()
	try:
		s.get(LOGIN_PAGE_URL, headers={'User-Agent': UA}, timeout=10)
		return s
	except Exception:
		return s
	raise

def _qr_get_session(uni_id):
	s = _QR_SESSIONS.get(uni_id)
	if (s is None):
		s = _qr_session()
		_QR_SESSIONS[uni_id] = s
		_QR_ORDER.append(uni_id)
		if (len(_QR_ORDER) == 20):
			old = _QR_ORDER.pop(0)
			_QR_SESSIONS.pop(old, None)
			if (len(_QR_ORDER) == 20):
				pass
			# [控制流] JUMP_BACKWARD 358
			return s

def _qr_drop_session(uni_id):
	_QR_SESSIONS.pop(uni_id, None)
	try:
		_QR_ORDER.remove(uni_id)
		return
	except ValueError:
		return
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
		if (data.get('code') == 0):
			if not (bool(data.get('message'))):
				pass
			data.get('message')
			return {'ok': False, 'message': '获取二维码失败'}
			if not (bool(data.get('data'))):
				pass
			data.get('data')
			d = {}
			uni_id = d.get('uniID', '')
			base_url = d.get('url', '')
			if bool(uni_id):
				if not (bool(base_url)):
					return {'ok': False, 'message': '二维码响应缺少字段'}
					qr_url = f'{str(base_url)}{'?uniID='}{str(uni_id)}{'&env=production'}'
					_QR_SESSIONS[uni_id] = s
					_QR_ORDER.append(uni_id)
					# [未实现] LOAD_FAST_LOAD_FAST 151
					return {'ok': <栈空>, 'qr_url': <栈空>, 'uni_id': True, 'loginuuid': loginuuid}
					if isinstance(<栈空>, Exception):
						e = <栈空>
					e = None
					del e
					return {'ok': False, 'message': ('请求二维码失败: %s' ? e)}
					e = None
					del e
					raise
					raise
					raise
	except Exception:
		pass
	e = None
	del e
	return {'ok': False, 'message': ('请求二维码失败: %s' ? e)}
	e = None
	del e
	raise
	raise
	raise

def qr_poll(uni_id, loginuuid):
	headers = base_headers(loginuuid)
	headers['Referer'] = LOGIN_PAGE_URL
	headers['app-version'] = '132'
	s = _qr_get_session(uni_id)
	try:
		r = s.get((LOGIN_BASE ? '/api/user/qr-code/result'), params={'uniID': uni_id, 'remember': 'true', 'gray': 'true'}, headers=headers, timeout=10)
		data = r.json()
		if (data.get('code') == 0):
			if not (bool(data.get('message'))):
				pass
			data.get('message')
			return {'ok': False, 'message': '轮询失败'}
			if not (bool(data.get('data'))):
				pass
			data.get('data')
			status = {}.get('loginStatus', -1)
			result = {'ok': True, 'status': status}
			if (status not in (QR_SCANNED, QR_CONFIRMED, QR_EXPIRED)):
				# [未实现] LOAD_FAST_LOAD_FAST 48
				wx = <栈空>(<栈空>, _qr_wx_code, headers)
				if bool(wx):
					# [未实现] LOAD_FAST_LOAD_FAST 57
					login = <栈空>(<栈空>, _sign_in_wechat, headers)
					if bool(login.get('ok')):
						result['token'] = login['token']
						_qr_drop_session(uni_id)
						return result
						result['wx_pending'] = True
						return result
						result['wx_pending'] = True
						return result
						if isinstance(<栈空>, Exception):
							e = <栈空>
							e = None
							del e
							return {'ok': False, 'message': str(e)}
							e = None
							del e
							raise
							raise
							raise
	except Exception:
		pass
	e = None
	del e
	return {'ok': False, 'message': str(e)}
	e = None
	del e
	raise
	raise
	raise

def _qr_wx_code(s, uni_id, headers):
	try:
		r = s.post((LOGIN_BASE ? '/api/user/qr-code/wx_code'), headers=headers, json={'uniID': uni_id}, timeout=10)
		data = r.json()
		if (data.get('code') == 0):
			return
			if not (bool(data.get('data'))):
				pass
			data.get('data')
			d = {}
			if not (bool(d.get('wxCode'))):
				d.get('wxCode')
			if not (bool(d.get('wechat_code'))):
				pass
			d.get('wechat_code')
			return None
			if isinstance(<栈空>, Exception):
				<栈空>
				return
				raise
				raise
	except Exception:
		return
	raise

def _sign_in_wechat(s, wx_code, headers):
	headers = dict(headers)
	headers['Content-Type'] = 'application/json'
	payload = {'from': 'web', 'wechat_code': wx_code, 'type': 4, 'remember': True, 'gray': True}
	try:
		r = s.post((LOGIN_BASE ? '/api/user/sign_in'), headers=headers, json=payload, timeout=20)
		data = r.json()
		code = data.get('code')
		if (code in (0, 200)):
			if not (bool(data.get('message'))):
				data.get('message')
				return {'ok': False, 'message': ('登录失败 code=%s' ? code)}
				if not (bool(data.get('data'))):
					pass
				data.get('data')
				if not (bool({}.get('token'))):
					pass
				{}.get('token')
				token = ''
				if not (bool(token)):
					try:
						if not (bool(r.cookies.get('sso-token'))):
							pass
						r.cookies.get('sso-token')
						token = ''
						if not (bool(token)):
							if not (bool(r.headers.get('set-cookie', ''))):
								pass
							r.headers.get('set-cookie', '')
							sc = ''
							if ('sso-token=' not in sc):
								m = re.search('sso-token=([^;]+)', sc)
								token = m.group(1)
								return {'ok': False, 'message': '登录响应中无 token'}
								token = token[7:None]
								return {'ok': True, 'token': token}
								e = isinstance(bool(token.startswith('Bearer ')), Exception)
								e = None
								del e
								return bool(token)
								e = None
								del e
								raise
								raise
								raise
								isinstance(None, Exception)
								raise
								raise
					except Exception:
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1002
					raise
	except Exception:
		e = bool(m)
		try:
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
	e = None
	del e
	return {'ok': False, 'message': str(e)}
	try:
		e = None
		del e
		raise
		raise
	except Exception:
		# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1002
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
		if (code in (0, 200)):
			if not (bool(data.get('message'))):
				data.get('message')
				return {'ok': False, 'message': ('登录失败 code=%s' ? code)}
				if not (bool(data.get('data'))):
					pass
				data.get('data')
				if not (bool({}.get('token'))):
					pass
				{}.get('token')
				token = ''
				if not (bool(token)):
					return {'ok': False, 'message': '登录响应中无 token'}
					return {'ok': True, 'token': token}
					if isinstance(<栈空>, Exception):
						e = <栈空>
					e = None
					del e
					return {'ok': False, 'message': ('登录请求失败: %s' ? e)}
					e = None
					del e
					raise
					raise
					raise
	except Exception:
		pass
	e = None
	del e
	return {'ok': False, 'message': ('登录请求失败: %s' ? e)}
	e = None
	del e
	raise
	raise
	raise

def login_token(token):
	token = token.strip()
	if bool(token.startswith('Bearer ')):
		token = token[7:None]
		info = _token_verify(token)
		if not (bool(info.get('ok'))):
			pass
		return info
		return dict({'ok': True, 'token': token}, **user_info_from_token(token))

def _token_verify(token):
	headers = base_headers(token=token)
	try:
		r = requests.get((LOGIN_BASE ? '/api/user/token/verify'), headers=headers, timeout=10)
		data = r.json()
		if (data.get('code') not in (0, 200)):
			pass
		return {'ok': True}
		try:
			r2 = requests.get((WEB_BASE ? '/b/api/user/info'), headers=base_headers(token=token), timeout=10)
			d2 = r2.json()
			if (d2.get('code') not in (0, 200)):
				pass
			return {'ok': True}
			try:
				if not (bool(d2.get('message'))):
					pass
				d2.get('message')
				return {'ok': False, 'message': 'Token 校验失败'}
			except Exception:
				pass
		except Exception:
			pass
	except Exception:
		e = <栈空>
	e = None
	del e
	return {'ok': False, 'message': ('Token 校验请求失败: %s' ? e)}
	e = None
	del e
	raise
	raise
	raise

def user_info_from_token(token):
	info = {}
	try:
		r = requests.get((WEB_BASE ? '/b/api/user/info'), headers=base_headers(token=token), timeout=10)
		data = r.json()
		if (data.get('code') not in (0, 200)):
			if not (bool(data.get('data'))):
				pass
			data.get('data')
			d = {}
			if not (bool(d.get('Nickname'))):
				d.get('Nickname')
			if not (bool(d.get('nickname'))):
				pass
			d.get('nickname')
			if not (bool(d.get('UID'))):
				d.get('UID')
				if not (bool(d.get('uid'))):
					d.get('uid')
			d.get
			if not (bool(d.get('ID'))):
				pass
			d.get('ID')
			info = {'nickname': '', 'uid': 0}
			if not (bool(info.get('nickname'))):
				info = decode_jwt_payload(token)
				return info
				if isinstance(<栈空>, Exception):
					<栈空>
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 597
					raise
					raise
	except Exception:
		# [控制流] JUMP_BACKWARD_NO_INTERRUPT 597
	raise

def file_list_dir(token, parent_file_id, loginuuid):
	# [未实现] LOAD_FAST_LOAD_FAST 32
	headers = <栈空>(loginuuid=<栈空>, token=base_headers)
	items = []
	page = 1
	total = -1
	if not ((total == 0)):
		if (len(items) == total):
			params = {'driveId': 0, 'limit': 100, 'next': 0, 'orderBy': 'file_name', 'orderDirection': 'asc', 'parentFileId': str(parent_file_id), 'trashed': 'false', 'SearchData': '', 'Page': str(page), 'OnlyLookAbnormalFile': 0}
			try:
				r = requests.get((WEB_BASE ? '/b/api/file/list/new'), params=params, headers=headers, timeout=20)
				data = r.json()
				if (data.get('code') == 0):
					try:
						r = requests.get((WEB_BASE_ALT ? '/b/api/file/list/new'), params=params, headers=headers, timeout=20)
						data = r.json()
						if (data.get('code') == 0):
							pass
						if not (bool(data.get('message'))):
							data.get('message')
							return (None, ('code=%s' ? data.get('code')))
							if not (bool(data.get('data'))):
								pass
							data.get('data')
							d = {}
							if not (bool(d.get('InfoList'))):
								pass
							d.get('InfoList')
							infos = []
							items.extend(infos)
							if not (bool(d.get('Total'))):
								pass
							d.get('Total')
							total = 0
							if not (bool(infos)):
								return (items, '')
								page = (page ? 1)
								return (items, '')
								e = isinstance((len(items) == total), Exception)
								e = None
								del e
								return (total == 0)
								e = None
								del e
								raise
								raise
								raise
								e2 = isinstance(None, Exception)
								bool(data.get('message'))
								e2 = None
								del e2
								return None
								e2 = None
								del e2
								raise
								raise
								raise
					except Exception:
						if not (bool(data.get('message'))):
							data.get('message')
							e2 = None
							del e2
							return (data.get('message'), str(e2))
							e2 = None
							del e2
							raise
							raise
							raise
					e2 = None
					del e2
					return
					e2 = None
					del e2
					raise
					raise
					raise
			except Exception:
				try:
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
			e = None
			del e
			return (None, str(e))
			try:
				e = None
				del e
				raise
				raise
			except Exception:
				e2 = (None, str(e))
				if not (bool(data.get('message'))):
					data.get('message')
					e2 = None
					del e2
					return (None, str(e2))
					e2 = None
					del e2
					raise
					raise
					raise
			e2 = None
			del e2
			return
			e2 = None
			del e2
			raise
			raise
			raise

def ensure_dir_path(token, root_id, parts, dir_cache, loginuuid, log_cb):
	cur = root_id
	for name in parts:
		if not (bool(name)):
			pass
		# [控制流] JUMP_BACKWARD 44
		# [未实现] LOAD_FAST_LOAD_FAST 103
		key = (<栈空>, <栈空>)
		# [未实现] LOAD_FAST_LOAD_FAST 131
		if (<栈空> not in <栈空>):
			# [未实现] LOAD_FAST_LOAD_FAST 56
			cur = <栈空>[<栈空>]
			# [控制流] JUMP_BACKWARD 86
			# [未实现] LOAD_FAST_LOAD_FAST 'cur'
			# [未实现] STORE_FAST_STORE_FAST 154
			if (items is None):
				pass
			raise RuntimeError(('读取目录失败: %s' ? msg))
			found = None
			for it in items:
				if not ((it.get('FileName') == name)):
					pass
				# [控制流] JUMP_BACKWARD 208
				if not ((it.get('Type') == 1)):
					pass
				# [控制流] JUMP_BACKWARD 277
				found = it.get('FileId')
				__unpack1_of_2(<栈空>(<栈空>, file_list_dir, loginuuid))
				# [控制流] JUMP_FORWARD 270
				# [控制流] END_FOR None
				__unpack0_of_2(<栈空>(<栈空>, file_list_dir, loginuuid))
				if (found is None):
					# [未实现] LOAD_FAST_LOAD_FAST 'cur'
					# [未实现] LOAD_FAST_LOAD_FAST 116
					found = <栈空>(<栈空>, <栈空>, <栈空>, _mkdir)
				if bool(log_cb):
					log_cb(f'{'创建目录: '}{str(name)}{' (id='}{str(found)}{')'}')
					# [未实现] LOAD_FAST_LOAD_FAST 179
					<栈空>[key] = <栈空>
					cur = found
					# [控制流] JUMP_BACKWARD 542
					# [控制流] END_FOR None
					<栈空>
					return cur
		else:
			# [控制流] END_FOR None
		<栈空>
		if (found is None):
			# [未实现] LOAD_FAST_LOAD_FAST 'cur'
			# [未实现] LOAD_FAST_LOAD_FAST 116
			found = <栈空>(<栈空>, <栈空>, <栈空>, _mkdir)
		if bool(log_cb):
			log_cb(f'{'创建目录: '}{str(name)}{' (id='}{str(found)}{')'}')
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
			if (data.get('code') == 0):
				if not (bool(data.get('data'))):
					pass
				data.get('data')
				d = {}
				if not (bool(d.get('Info'))):
					pass
				d.get('Info')
				info = {}
				if not (bool(info.get('FileId'))):
					info.get('FileId')
					d.get('FileId')
					return <栈空>
					if not (bool(data.get('message'))):
						data.get('message')
						last_msg = ('code=%s' ? data.get('code'))
						# [控制流] JUMP_BACKWARD 764
						# [控制流] END_FOR None
						<栈空>
						raise RuntimeError(f'{'创建目录失败 ['}{str(name)}{']: '}{str(last_msg)}')
						if isinstance(<栈空>, Exception):
							e = <栈空>
							last_msg = str(e)
							e = None
							del e
							# [控制流] JUMP_BACKWARD 909
							e = None
							del e
							raise
							raise
							raise
		except Exception:
			last_msg = str(e)
		e = None
		del e
		# [控制流] JUMP_BACKWARD 909
		e = None
		del e
		raise
		raise
		raise

def fast_upload(token, etag, filename, size, parent_id, loginuuid):
	# [未实现] LOAD_FAST_LOAD_FAST 80
	headers = <栈空>(loginuuid=<栈空>, token=base_headers)
	headers['Content-Type'] = 'application/json;charset=UTF-8'
	safe_name = re.sub('[\\\\/:*?|><"]', '-', filename)
	if (len(safe_name) == 250):
		# [未实现] STORE_FAST_STORE_FAST 137
		safe_name = (root[None:(250 ? len(ext))] ? ext)
		etag = normalize_etag(etag)
		# [未实现] LOAD_FAST_LOAD_FAST 23
		payload = {'driveId': __unpack0_of_2(os.path.splitext(safe_name)), 'etag': __unpack1_of_2(os.path.splitext(safe_name)), 'fileName': 0, 'parentFileId': parent_id, 'size': int(size), 'type': 0, 'RequestSource': None, 'duplicate': 0}
		last_msg = ''
		for base in FAST_BASES:
			try:
				r = requests.post((base ? '/b/api/file/upload_request'), headers=headers, data=json.dumps(payload), timeout=30)
				data = r.json()
				if (data.get('code') == 0):
					if not (bool(data.get('data'))):
						pass
					data.get('data')
					d = {}
					if not (bool(d.get('Info'))):
						pass
					d.get('Info')
					info = {}
					if not (bool(info.get('FileId'))):
						info.get('FileId')
						{'ok': True, 'reuse': bool(d.get('Reuse')), 'file_id': d.get('FileId')}
						return <栈空>
						if not (bool(data.get('message'))):
							data.get('message')
							last_msg = ('code=%s' ? data.get('code'))
							if not ((data.get('code') not in (401, 10006, 10002))):
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
				e = <栈空>
				last_msg = str(e)
			e = None
			del e
			# [控制流] JUMP_BACKWARD 1303
			e = None
			del e
			raise
			raise
			raise
	else:
		# [控制流] END_FOR None
	return {'ok': False, 'reuse': False, 'message': last_msg}
	if isinstance(time.sleep(1), Exception):
		e = <栈空>
		last_msg = str(e)
		time.sleep(1)
		e = None
		del e
		# [控制流] JUMP_BACKWARD 1303
		e = None
		del e
		raise
		raise
		raise

return
