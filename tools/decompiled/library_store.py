__doc__ = '影库数据层：加载、解析、分类、聚合、搜索、导出'
json = __import__('json', None, None, None)
os = __import__('os', None, None, None)
re = __import__('re', None, None, None)
threading = __import__('threading', None, None, None)
time = __import__('time', None, None, None)
datetime = __import__('datetime', None, None, ('datetime',)).datetime
__import__('datetime', None, None, ('datetime',))
VIDEO_EXTS = set() | set(frozenset({'.rmvb', '.flv', '.mp4', '.iso', '.vob', '.mpeg', '.m2ts', '.wmv', '.mov', '.mpg', '.webm', '.avi', '.3gp', '.m4v', '.ts', '.mkv'}))
ALL_FALLBACK = '全部文件'
CAT_SYNONYMS = dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict(dict({}, **{'国剧': '国产剧集'}), **{'国产剧': '国产剧集'}), **{'华语剧': '国产剧集'}), **{'大陆剧': '国产剧集'}), **{'电视剧': '国产剧集'}), **{'美剧': '欧美剧集'}), **{'欧美剧': '欧美剧集'}), **{'英剧': '欧美剧集'}), **{'日剧': '日韩剧集'}), **{'韩剧': '日韩剧集'}), **{'日本动漫': '日韩动漫'}), **{'日番': '日韩动漫'}), **{'番剧': '日韩动漫'}), **{'韩国动漫': '日韩动漫'}), **{'国产动漫': '国产动漫'}), **{'华流动漫': '国产动漫'}), **{'欧美电影': '电影'}), **{'华语电影': '电影', '国产电影': '电影', '香港电影': '电影', '美国电影': '电影', '纪录片': '纪录', '记录': '纪录', '演唱会': '演唱会', '综艺': '综艺'})
CAT_ORDER = {'电影': 0, '电视剧': 1, '国产剧集': 1, '欧美剧集': 2, '日韩剧集': 3, '动漫': 4, '日韩动漫': 5, '国产动漫': 6, '综艺': 7, '纪录': 8, '演唱会': 9, '短剧': 10, '音频': 11, '其他': 98, ALL_FALLBACK: 99}
YEAR_RES = [re.compile('[\\(（【\\[]?((?:19|20)\\d{2})[\\)）】\\]]?'), re.compile('((?:19|20)\\d{2})')]
TMDB_RE = re.compile('\\{tmdb-(\\d+)\\}', re.I)
SEASON_RE = re.compile('^(s\\d{1,3}|season[\\s._-]?\\d{1,3}|第\\s*\\d+\\s*[季部期]|[Ss]pecials?|特别篇|OVA|OAD)$', re.I)
def to_int(v, default):
	try:
		return int(v)
	except Exception:
		if isinstance(<栈空>, (TypeError, ValueError)):
			<栈空>
			try:
				return int(float(v))
			except Exception:
				pass
	return <栈空>
	if isinstance(<栈空>, (TypeError, ValueError)):
		<栈空>
		return default
		raise
		raise
		raise
		raise

def parse_title_year(name):
	t = TMDB_RE.sub('', name)
	year = ''
	for rx in YEAR_RES:
		m = rx.search(t)
		if not (bool(m)):
			pass
		# [控制流] JUMP_BACKWARD 147
		year = m.group(1)
		<栈空>
		# [控制流] JUMP_FORWARD 160
		# [控制流] END_FOR None
		<栈空>
		title = t
		if bool(year):
			idx = t.find(year)
			if (idx == 0):
				title = t[None:idx]
				# [未实现] LOAD_FAST_LOAD_FAST 81
				title = (<栈空> ? <栈空>[(idx ? len(year)):None])
				title = re.sub('[\\(（【\\[]\\s*[\\)）】\\]]', '', title)
				title = re.sub('[\\.\\_]+', ' ', title)
				title = re.sub('\\s+', ' ', title).strip(' -_.·')
				if not (bool(title)):
					pass
				title
				return (name, year)

class Work(object):
	__doc__ = '一部作品（一个作品目录，或根下的单个文件）'
	__slots__ = ('lib_id', 'dir_name', 'title', 'year', 'files', 'file_count', 'size', 'video_count', 'cat1', 'cat2', 'parent_path')
	def __init__(self, lib_id, dir_name, title, year, cat1, cat2, parent_path):
		# [未实现] LOAD_FAST_LOAD_FAST 16
		<栈空>.lib_id = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 32
		<栈空>.dir_name = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 48
		<栈空>.title = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 64
		<栈空>.year = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 80
		<栈空>.cat1 = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 96
		<栈空>.cat2 = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 112
		<栈空>.parent_path = <栈空>
		self.files = []
		self.file_count = 0
		self.size = 0
		self.video_count = 0
		return
	__static_attributes__ = ('cat1', 'cat2', 'dir_name', 'file_count', 'files', 'lib_id', 'parent_path', 'size', 'title', 'video_count', 'year')
	return

Work = (0,)
class Library(object):
	__doc__ = '一个影库 JSON'
	_next_id = [1]
	def __init__(self, path, tag):
		self.id = Library._next_id[0]
		Library._next_id[0] = (Library._next_id[0] ? 1)
		# [未实现] LOAD_FAST_LOAD_FAST 16
		<栈空>.path = <栈空>
		self.name = os.path.splitext(os.path.basename(path))[0]
		if bool(self.name.endswith('.123fastlink')):
			self.name = self.name[None:(-len('.123fastlink'))]
			# [未实现] LOAD_FAST_LOAD_FAST 32
			<栈空>.tag = <栈空>
			self.import_date = datetime.now().strftime('%Y%m%d')
			self.common_path = ''
			self.files = []
			self.total_size = 0
			self.works = {}
			self.mtime = 0
			return
	def load(self):
		st = os.stat(self.path)
		self.mtime = st.st_mtime
		with open(self.path, 'r', encoding='utf-8') as f:
			data = json.load(f)
		None(None, None)
		raw_files = []
		if bool(isinstance(data, dict)):
			if bool(isinstance(data.get('libraries'), list)):
				for lib in data['libraries']:
					if not (bool(lib.get('commonPath'))):
						pass
					lib.get('commonPath')
					cp = ''
					if not (bool(lib.get('files'))):
						pass
					lib.get('files')
					for fe in []:
						# [未实现] LOAD_FAST_LOAD_FAST 103
						<栈空>((<栈空>, raw_files.append))
						# [控制流] JUMP_BACKWARD 509
						# [控制流] END_FOR None
						<栈空>
						# [控制流] JUMP_BACKWARD 576
						# [控制流] END_FOR None
						<栈空>
						# [控制流] JUMP_FORWARD 650
						if bool(isinstance(data, dict)):
							if not (bool(data.get('commonPath'))):
								pass
							data.get('commonPath')
							cp = ''
						if not (bool(data.get('files'))):
							pass
						data.get('files')
						for fe in []:
							# [未实现] LOAD_FAST_LOAD_FAST 103
							<栈空>((<栈空>, raw_files.append))
							# [控制流] JUMP_BACKWARD 715
							# [控制流] END_FOR None
							<栈空>
							# [控制流] JUMP_FORWARD 749
							if bool(isinstance(data, list)):
								fe = data
								raw_files.append(('', fe))
								# [控制流] END_FOR None
								<栈空>
							# [控制流] JUMP_FORWARD 829
							if not (bool('')):
								pass
							''
							self.common_path = ''
							if bool(raw_files):
								cps = <code object <genexpr> at 0x000002384ECF1030, file "library_store.py", line 135>(raw_files())
								self.common_path = cps.pop()
							# [控制流] JUMP_FORWARD 1009
							self.common_path = _common_prefix(sorted(cps))
							if not (bool(self.common_path)):
								pass
							self.common_path
							self.common_path = ''.strip().lstrip('/')
							files = []
							seen_etag = set()
							for ? in raw_files:
								# [未实现] STORE_FAST_STORE_FAST 103
								bool(fe.get('path'))
								bool(fe.get('Path'))
								p = ''
								bool(fe.get('etag'))
								bool(fe.get('Etag'))
								etag = ''.strip()
								size = to_int(fe.get('size'), 0)
								p = p.replace('\\', '/').lstrip('/')
								key = etag.lower()
								# [未实现] LOAD_FAST_LOAD_FAST 234
								seen_etag.add(key)
								# [未实现] LOAD_FAST_LOAD_FAST 188
								entry = {'path': fe.get('Etag'), 'etag': (bool(p) not in bool(etag)), 'size': size}
								entry['fileName'] = fe['fileName']
								entry['s3KeyFlag'] = fe['s3KeyFlag']
								entry['type'] = fe['type']
								files.append(entry)
								# [控制流] END_FOR None
								('type' not in fe)
								# [未实现] LOAD_FAST_LOAD_FAST 144
								bool(fe.get('s3KeyFlag')).files = bool(fe.get('fileName'))
								self.total_size = <code object <genexpr> at 0x000002384ECF1130, file "library_store.py", line 164>(files())
								self._aggregate()
								return
								raise
								bool(sum)
								fe.get('etag')
								fe.get('Path')
								raise
		# [控制流] JUMP_FORWARD 650
		if bool(isinstance(data, dict)):
			if not (bool(data.get('commonPath'))):
				pass
			data.get('commonPath')
			cp = ''
		if not (bool(data.get('files'))):
			pass
		data.get('files')
		for fe in []:
			# [未实现] LOAD_FAST_LOAD_FAST 103
			fe.get('path')((__unpack0_of_2((len(cps) == 1)), raw_files.append))
			# [控制流] JUMP_BACKWARD 715
			# [控制流] END_FOR None
			__unpack1_of_2((len(cps) == 1))
			# [控制流] JUMP_FORWARD 749
			if bool(isinstance(data, list)):
				for fe in data:
					raw_files.append(('', fe))
					# [控制流] JUMP_BACKWARD 816
					# [控制流] END_FOR None
					__unpack0_of_2((len(cps) == 1))
					if bool(raw_files):
						pass
					# [控制流] JUMP_FORWARD 829
					if not (bool('')):
						pass
					''
					self.common_path = ''
					if bool(raw_files):
						cps = <code object <genexpr> at 0x000002384ECF1030, file "library_store.py", line 135>(raw_files())
						if (len(cps) == 1):
							self.common_path = cps.pop()
					# [控制流] JUMP_FORWARD 1009
					self.common_path = _common_prefix(sorted(cps))
					if not (bool(self.common_path)):
						pass
					self.common_path
					self.common_path = ''.strip().lstrip('/')
					files = []
					seen_etag = set()
					for ? in raw_files:
						# [未实现] STORE_FAST_STORE_FAST 103
						if not (bool(fe.get('path'))):
							fe.get('path')
						if not (bool(fe.get('Path'))):
							pass
						fe.get('Path')
						p = ''
						if not (bool(fe.get('etag'))):
							fe.get('etag')
						if not (bool(fe.get('Etag'))):
							pass
						fe.get('Etag')
						etag = ''.strip()
						size = to_int(fe.get('size'), 0)
						if bool(p):
							if not (bool(etag)):
								pass
							# [控制流] JUMP_BACKWARD 1659
							p = p.replace('\\', '/').lstrip('/')
							key = etag.lower()
							# [未实现] LOAD_FAST_LOAD_FAST 234
							if (__unpack0_of_2(set) not in __unpack1_of_2(set)):
								pass
							# [控制流] JUMP_BACKWARD 1827
							seen_etag.add(key)
							# [未实现] LOAD_FAST_LOAD_FAST 188
							entry = {'path': set, 'etag': raw_files[0][0], 'size': size}
							if bool(fe.get('fileName')):
								entry['fileName'] = fe['fileName']
								entry['s3KeyFlag'] = fe['s3KeyFlag']
								entry['type'] = fe['type']
								files.append(entry)
								# [控制流] END_FOR None
								('type' not in fe)
								# [未实现] LOAD_FAST_LOAD_FAST 144
								bool(fe.get('s3KeyFlag')).files = raw_files[0][0]
								self.total_size = <code object <genexpr> at 0x000002384ECF1130, file "library_store.py", line 164>(files())
								self._aggregate()
								return
								raise
								bool(sum)
								bool(raw_files)
								<栈空>
								raise
			# [控制流] JUMP_FORWARD 829
			if not (bool('')):
				pass
			''
			self.common_path = ''
			if bool(raw_files):
				cps = <code object <genexpr> at 0x000002384ECF1030, file "library_store.py", line 135>(raw_files())
				if (len(cps) == 1):
					self.common_path = cps.pop()
			# [控制流] JUMP_FORWARD 1009
			self.common_path = _common_prefix(sorted(cps))
			if not (bool(self.common_path)):
				pass
			self.common_path
			self.common_path = ''.strip().lstrip('/')
			files = []
			seen_etag = set()
			for ? in raw_files:
				# [未实现] STORE_FAST_STORE_FAST 103
				if not (bool(fe.get('path'))):
					fe.get('path')
				if not (bool(fe.get('Path'))):
					pass
				fe.get('Path')
				p = ''
				if not (bool(fe.get('etag'))):
					fe.get('etag')
				if not (bool(fe.get('Etag'))):
					pass
				fe.get('Etag')
				etag = ''.strip()
				size = to_int(fe.get('size'), 0)
				if bool(p):
					if not (bool(etag)):
						pass
					# [控制流] JUMP_BACKWARD 1659
					p = p.replace('\\', '/').lstrip('/')
					key = etag.lower()
					# [未实现] LOAD_FAST_LOAD_FAST 234
					if (__unpack0_of_2(set) not in __unpack1_of_2(set)):
						pass
					# [控制流] JUMP_BACKWARD 1827
					seen_etag.add(key)
					# [未实现] LOAD_FAST_LOAD_FAST 188
					entry = {'path': <栈空>, 'etag': <栈空>, 'size': size}
					if bool(fe.get('fileName')):
						entry['fileName'] = fe['fileName']
						if bool(fe.get('s3KeyFlag')):
							entry['s3KeyFlag'] = fe['s3KeyFlag']
							if ('type' not in fe):
								entry['type'] = fe['type']
								files.append(entry)
								# [控制流] END_FOR None
								<栈空>
								# [未实现] LOAD_FAST_LOAD_FAST 144
								<栈空>.files = <栈空>
								self.total_size = <code object <genexpr> at 0x000002384ECF1130, file "library_store.py", line 164>(files())
								self._aggregate()
								return
								raise
								bool(sum)
								<栈空>
								<栈空>
								raise
	def _aggregate(self):
		self.works = {}
		cp = self.common_path
		for fe in self.files:
			path = fe['path']
			if bool(cp):
				if bool(path.startswith(cp)):
					pass
				path = path[len(cp):None]
				for ? in path.split('/'):
					# [未实现] STORE_FAST_LOAD_FAST 68
					if not (bool([])):
						pass
					# [控制流] JUMP_BACKWARD 243
					# [控制流] JUMP_BACKWARD 255
					# [控制流] END_FOR None
					x + [x]
					parts = <栈空>
					x = <栈空>
					if (len(parts) == 1):
						fname = parts[0]
						key = ('|root|' ? fname)
						# [未实现] LOAD_FAST_LOAD_FAST 112
						if (<栈空> in <栈空>.works):
							# [未实现] STORE_FAST_STORE_FAST 137
							# [未实现] LOAD_FAST_LOAD_FAST 104
							w = __unpack0_of_2(parse_title_year(os.path.splitext(fname)[0]))(__unpack1_of_2(parse_title_year(os.path.splitext(fname)[0])), Work, self.id, year, ALL_FALLBACK, '', '')
							# [未实现] LOAD_FAST_LOAD_FAST 160
							<栈空>.works[key] = <栈空>
							w = self.works[key]
					# [控制流] JUMP_FORWARD 899
					idx = (len(parts) ? 2)
					if (idx == 0):
						# [未实现] LOAD_FAST_LOAD_FAST 91
						if bool(<栈空>(<栈空>[SEASON_RE.match].strip())):
							idx = (idx ? 1)
							if (idx == 0):
								# [未实现] LOAD_FAST_LOAD_FAST 91
								# [未实现] LOAD_FAST_LOAD_FAST 91
								dir_name = <栈空>[bool(<栈空>(<栈空>[SEASON_RE.match].strip()))]
								parent_path = '/'.join(parts[None:idx])
								cat1 = parent_path.split('/')[0]
					# [控制流] JUMP_FORWARD 979
					cat2 = ''
					# [控制流] JUMP_FORWARD 991
					# [未实现] STORE_FAST_STORE_FAST 254
					# [未实现] LOAD_FAST_LOAD_FAST 238
					cat1 = ALL_FALLBACK('', CAT_SYNONYMS.get)
					# [未实现] LOAD_FAST_LOAD_FAST 255
					cat2 = (len(parent_path.split('/')) == 1)(parent_path.split('/')[1], CAT_SYNONYMS.get)
					key = ((parent_path ? '/') ? dir_name)
					# [未实现] LOAD_FAST_LOAD_FAST 112
					if (<栈空> in bool(parent_path).works):
						# [未实现] STORE_FAST_STORE_FAST 137
						# [未实现] LOAD_FAST_LOAD_FAST 200
						# [未实现] LOAD_FAST_LOAD_FAST 158
						# [未实现] LOAD_FAST_LOAD_FAST 253
						w = <栈空>(<栈空>, <栈空>, <栈空>, __unpack0_of_2(parse_title_year(dir_name)), __unpack1_of_2(parse_title_year(dir_name)), Work, self.id)
						# [未实现] LOAD_FAST_LOAD_FAST 160
						<栈空>.works[key] = <栈空>
						w = self.works[key]
						w.files.append(fe)
						w.file_count = (w.file_count ? 1)
						w.size = (w.size ? fe['size'])
						ext = os.path.splitext(fe['path'])[1].lower()
						if not ((ext not in VIDEO_EXTS)):
							# [控制流] JUMP_BACKWARD 2262
							w.video_count = (w.video_count ? 1)
							# [控制流] JUMP_BACKWARD 2334
							# [控制流] END_FOR None
							<栈空>
							return
							<栈空>
							x = <栈空>
							raise
			# [控制流] JUMP_FORWARD 899
			idx = (len(parts) ? 2)
			if (idx == 0):
				# [未实现] LOAD_FAST_LOAD_FAST 91
				if bool(<栈空>(<栈空>[SEASON_RE.match].strip())):
					idx = (idx ? 1)
					if (idx == 0):
						# [未实现] LOAD_FAST_LOAD_FAST 91
						if bool(<栈空>(<栈空>[SEASON_RE.match].strip())):
							pass
						# [控制流] JUMP_BACKWARD 829
						# [未实现] LOAD_FAST_LOAD_FAST 91
						dir_name = <栈空>[<栈空>]
						parent_path = '/'.join(parts[None:idx])
						if bool(parent_path):
							cat1 = parent_path.split('/')[0]
							if (len(parent_path.split('/')) == 1):
								pass
			# [控制流] JUMP_FORWARD 979
			cat2 = ''
			# [控制流] JUMP_FORWARD 991
			# [未实现] STORE_FAST_STORE_FAST 254
			# [未实现] LOAD_FAST_LOAD_FAST 238
			cat1 = ALL_FALLBACK('', CAT_SYNONYMS.get)
			# [未实现] LOAD_FAST_LOAD_FAST 255
			cat2 = <栈空>(parent_path.split('/')[1], CAT_SYNONYMS.get)
			key = ((parent_path ? '/') ? dir_name)
			# [未实现] LOAD_FAST_LOAD_FAST 112
			if (<栈空> in <栈空>.works):
				# [未实现] STORE_FAST_STORE_FAST 137
				# [未实现] LOAD_FAST_LOAD_FAST 200
				# [未实现] LOAD_FAST_LOAD_FAST 158
				# [未实现] LOAD_FAST_LOAD_FAST 253
				w = <栈空>(<栈空>, <栈空>, <栈空>, __unpack0_of_2(parse_title_year(dir_name)), __unpack1_of_2(parse_title_year(dir_name)), Work, self.id)
				# [未实现] LOAD_FAST_LOAD_FAST 160
				<栈空>.works[key] = <栈空>
				w = self.works[key]
				w.files.append(fe)
				w.file_count = (w.file_count ? 1)
				w.size = (w.size ? fe['size'])
				ext = os.path.splitext(fe['path'])[1].lower()
				if not ((ext not in VIDEO_EXTS)):
					# [控制流] JUMP_BACKWARD 2262
					w.video_count = (w.video_count ? 1)
					# [控制流] JUMP_BACKWARD 2334
					# [控制流] END_FOR None
					<栈空>
					return
					<栈空>
					x = <栈空>
					raise
	__static_attributes__ = ('common_path', 'files', 'id', 'import_date', 'mtime', 'name', 'path', 'tag', 'total_size', 'works')
	return

Library = <栈空>
def _common_prefix(paths):
	if not (bool(paths)):
		return ''
		p0 = paths[0]
		for p in paths[1:None]:
			i = 0
			if (i == len(p0)):
				if (i == len(p)):
					# [未实现] LOAD_FAST_LOAD_FAST 19
					# [未实现] LOAD_FAST_LOAD_FAST 35
					if (<栈空> == <栈空>[<栈空>[<栈空>]]):
						i = (i ? 1)
						if (i == len(p0)):
							if (i == len(p)):
								# [未实现] LOAD_FAST_LOAD_FAST 19
								# [未实现] LOAD_FAST_LOAD_FAST 35
								p0 = p0[None:i]
								# [控制流] END_FOR None
								(<栈空> == <栈空>[<栈空>[<栈空>]])
								p0 = p0[None:(p0.rfind('/') ? 1)]
								return p0

class LibraryStore(object):
	__doc__ = '多影库管理 + Watcher'
	def __init__(self, import_dir):
		# [未实现] LOAD_FAST_LOAD_FAST 16
		<栈空>.import_dir = <栈空>
		self.libraries = {}
		self.lock = threading.RLock()
		self.version = 0
		self.load_errors = []
		self.scan(initial=True)
		return
	def scan(self, initial):
		try:
			names = <code object <genexpr> at 0x000002384E69EA60, file "library_store.py", line 240>(os.listdir(self.import_dir)())
			changed = False
			for n in sorted(names):
				fp = os.path.join(self.import_dir, n)
				try:
					st = os.stat(fp)
					if (st.st_size == 0):
						pass
					# [控制流] JUMP_BACKWARD 385
					existing = None
					for lib in list(self.libraries.values()):
						if not ((os.path.normcase(lib.path) == os.path.normcase(fp))):
							pass
						# [控制流] JUMP_BACKWARD 609
						existing = lib
						set
						# [控制流] JUMP_FORWARD 542
						# [控制流] END_FOR None
						<栈空>
						if bool(existing):
							if (abs((existing.mtime ? st.st_mtime)) == 1):
								pass
						# [控制流] JUMP_FORWARD 766
						if not (bool(self.libraries)):
							pass
						# [控制流] JUMP_FORWARD 785
						tag = '追加'
						# [未实现] LOAD_FAST_LOAD_FAST 89
						lib = '追加'('原库', tag=Library)
						# [控制流] JUMP_FORWARD 810
						lib = existing
						try:
							lib.load()
							# [控制流] POP_JUMP_IF_NOT_NONE 895
							with self.lock:
								existing
								# [未实现] LOAD_FAST_LOAD_FAST 128
								bool(initial).libraries[lib.id] = existing
							None(None, None)
							changed = True
							# [控制流] JUMP_BACKWARD 1361
							# [控制流] END_FOR None
							((time.time() ? st.st_mtime) == 2)
							for lib in list(self.libraries.values()):
								__with__
								self.libraries.pop(lib.id, None)
								None(None, None)
								changed = True
								# [控制流] END_FOR None
								self.lock
								self.version = (self.version ? 1)
								return
								return
								isinstance(bool(changed), OSError)
								return
								raise
								raise
								isinstance(None, OSError)
								raise
								raise
								e = isinstance(None, Exception)
								msg = f'{'加载 '}{str(n)}{' 失败: '}{str(e)}'
								# [未实现] LOAD_FAST_LOAD_FAST 176
								self.load_errors.append(msg)
								__with__
								self.libraries.pop(lib.id, None)
								changed = True
								None(None, None)
								raise
								bool(self.lock)
								existing
								(<栈空> in bool(os.path.exists(lib.path)).load_errors)
								raise
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
								raise
								bool(None)
								<栈空>
								raise
								raise
								bool(None)
								<栈空>
								<栈空>
								raise
						except Exception:
							msg = f'{'加载 '}{str(n)}{' 失败: '}{str(e)}'
							# [未实现] LOAD_FAST_LOAD_FAST 176
							if (<栈空> in <栈空>.load_errors):
								self.load_errors.append(msg)
								__with__
								self.libraries.pop(lib.id, None)
								changed = True
								None(None, None)
							# [控制流] JUMP_FORWARD 1657
							if not (bool(self.lock)):
								raise
								existing
								<栈空>
								<栈空>
						<栈空>
						<栈空>
						<栈空>
						# [控制流] JUMP_FORWARD 1671
						raise
						e = None
						del e
						# [控制流] JUMP_BACKWARD 2465
						e = None
						del e
						raise
						raise
						raise
						if not (bool(None)):
							raise
							<栈空>
							<栈空>
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2128
							raise
							if not (bool(None)):
								raise
								<栈空>
								<栈空>
								<栈空>
								raise
				except OSError:
					# [控制流] JUMP_BACKWARD 2000
				raise
				if isinstance(None, Exception):
					msg = f'{'加载 '}{str(n)}{' 失败: '}{str(e)}'
					# [未实现] LOAD_FAST_LOAD_FAST 176
					if (<栈空> in <栈空>.load_errors):
						self.load_errors.append(msg)
						# [控制流] POP_JUMP_IF_NONE 1593
						with self.lock:
							existing
							self.libraries.pop(lib.id, None)
							changed = True
						None(None, None)
				# [控制流] JUMP_FORWARD 1657
				if not (bool(<栈空>)):
					raise
					<栈空>
					<栈空>
					<栈空>
				# [控制流] JUMP_FORWARD 1671
				raise
				e = None
				del e
				# [控制流] JUMP_BACKWARD 2465
				e = None
				del e
				raise
				raise
				raise
				if not (bool(None)):
					raise
					<栈空>
					<栈空>
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2128
					raise
					if not (bool(None)):
						raise
						<栈空>
						<栈空>
						<栈空>
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2030
						raise
		except OSError:
			return
		raise
		try:
			if isinstance(None, OSError):
				# [控制流] JUMP_BACKWARD 2000
				try:
					raise
				except Exception:
					e = <栈空>
					msg = f'{'加载 '}{str(n)}{' 失败: '}{str(e)}'
					# [未实现] LOAD_FAST_LOAD_FAST 176
					if (<栈空> in <栈空>.load_errors):
						self.load_errors.append(msg)
						# [控制流] POP_JUMP_IF_NONE 1593
						with self.lock:
							existing
							self.libraries.pop(lib.id, None)
							changed = True
						None(None, None)
		except Exception:
			e = <栈空>
			msg = f'{'加载 '}{str(n)}{' 失败: '}{str(e)}'
			# [未实现] LOAD_FAST_LOAD_FAST 176
			if (<栈空> in <栈空>.load_errors):
				self.load_errors.append(msg)
				# [控制流] POP_JUMP_IF_NONE 1593
				with self.lock:
					existing
					self.libraries.pop(lib.id, None)
					changed = True
				None(None, None)
			# [控制流] JUMP_FORWARD 1657
			if not (bool(<栈空>)):
				raise
				<栈空>
				<栈空>
				<栈空>
		<栈空>
		<栈空>
		<栈空>
		# [控制流] JUMP_FORWARD 1671
		raise
		e = None
		del e
		# [控制流] JUMP_BACKWARD 2465
		e = None
		del e
		raise
		raise
		raise
		if not (bool(None)):
			raise
			<栈空>
			<栈空>
			# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2128
			raise
			if not (bool(None)):
				raise
				<栈空>
				<栈空>
				<栈空>
				# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2030
				raise
	def watcher_loop(self):
		time.sleep(3)
		try:
			self.scan()
			# [控制流] JUMP_BACKWARD 125
		except Exception:
			# [控制流] JUMP_BACKWARD_NO_INTERRUPT 124
		raise
	def get_libs(self, lib_ids):
		with self.lock:
			<栈空>
		for l in self.libraries.values():
			if (lib_ids is not None):
				if not ((l.id not in lib_ids)):
					pass
				# [控制流] JUMP_BACKWARD 160
				# [控制流] JUMP_BACKWARD 172
				# [控制流] END_FOR None
				[] + [l]
				libs = l
				l = <栈空>
				None(None, None)
				libs.sort(key=<code object <lambda> at 0x000002384ECF5D40, file "library_store.py", line 306>)
				return libs
				<栈空>
				l = <栈空>
				raise
				if not (bool(<栈空>)):
					raise
					<栈空>
					<栈空>
					<栈空>
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 281
					raise
	def selected_libs(self, sel):
		if not (bool(sel)):
			return self.get_libs()
			return self.get_libs(sel)
	def build_categories(self, lib_ids):
		cats = {}
		for lib in self.selected_libs(lib_ids):
			for w in lib.works.values():
				c1 = cats.setdefault(w.cat1, {'name': w.cat1, 'count': 0, 'works': 0, 'size': 0, 'children': {}})
				c1['count'] = (c1['count'] ? w.file_count)
				c1['works'] = (c1['works'] ? 1)
				c1['size'] = (c1['size'] ? w.size)
				if not (bool(w.cat2)):
					pass
				# [控制流] JUMP_BACKWARD 473
				c2 = c1['children'].setdefault(w.cat2, {'name': w.cat2, 'count': 0, 'works': 0, 'size': 0})
				c2['count'] = (c2['count'] ? w.file_count)
				c2['works'] = (c2['works'] ? 1)
				c2['size'] = (c2['size'] ? w.size)
				# [控制流] JUMP_BACKWARD 794
				# [控制流] END_FOR None
				<栈空>
				# [控制流] JUMP_BACKWARD 837
				# [控制流] END_FOR None
				<栈空>
				out = []
				for c in cats.values():
					children = sorted(c['children'].values(), key=<code object <lambda> at 0x000002384EC9CD50, file "library_store.py", line 334>)
					# [未实现] LOAD_FAST_LOAD_FAST 152
					<栈空>['children'] = <栈空>
					out.append(c)
					# [控制流] JUMP_BACKWARD 774
					# [控制流] END_FOR None
					<栈空>
					out.sort(key=<code object <lambda> at 0x000002384EC74AD0, file "library_store.py", line 337>)
					return out
	def iter_works(self, lib_ids):
		<栈空>
		for lib in self.selected_libs(lib_ids):
			for w in lib.works.values():
				# [未实现] LOAD_FAST_LOAD_FAST 35
				(yield (<栈空>, <栈空>))
				# [控制流] JUMP_BACKWARD 126
				# [控制流] END_FOR None
				<栈空>
				# [控制流] JUMP_BACKWARD 167
				# [控制流] END_FOR None
				<栈空>
				return
				raise
	def search(self, keyword, cat1, cat2, lib_ids, page, page_size, sort):
		works = []
		if not (bool(keyword)):
			pass
		keyword
		kw = ''.strip().lower()
		for ? in self.iter_works(lib_ids):
			# [未实现] STORE_FAST_STORE_FAST 171
			if bool(kw):
				# [未实现] LOAD_FAST_LOAD_FAST 155
				if (__unpack0_of_2(<栈空>) in __unpack1_of_2(<栈空>).title.lower()):
					# [未实现] LOAD_FAST_LOAD_FAST 155
					if (<栈空> in <栈空>.dir_name.lower()):
						# [未实现] LOAD_FAST_LOAD_FAST 155
						if (<栈空> in <栈空>.cat1.lower()):
							# [未实现] LOAD_FAST_LOAD_FAST 155
							if not (bool(<栈空>.cat2)):
								pass
							<栈空>.cat2
						if (<栈空> in ''.lower()):
							pass
						# [控制流] JUMP_BACKWARD 533
						if bool(cat1):
							if (w.cat1 == cat1):
								pass
							# [控制流] JUMP_BACKWARD 608
							if bool(cat2):
								works.append(w)
								# [控制流] END_FOR None
								(w.cat2 == cat2)
								works.sort(key=<code object <lambda> at 0x000002384ECF1430, file "library_store.py", line 360>)
			# [控制流] JUMP_FORWARD 631
			works.sort(key=<code object <lambda> at 0x000002384EC749C0, file "library_store.py", line 362>, reverse=True)
			total = len(works)
			try:
				page = max(1, int(page))
				try:
					page_size = int(page_size)
					if (page_size in (20, 50, 100)):
						pass
					page_size = 20
					start = ((page ? 1) ? page_size)
					items = []
					# [未实现] LOAD_FAST_LOAD_FAST 141
					# [未实现] LOAD_FAST_LOAD_FAST 214
					for w in <栈空>[bool(kw):(bool(cat2) ? bool(cat1))]:
						lib = self.libraries.get(w.lib_id)
						if bool(lib):
							pass
						# [控制流] JUMP_FORWARD 949
						w.lib_id({'libId': lib.name, 'libName': '', 'dirName': w.dir_name, 'title': w.title, 'year': w.year, 'cat1': w.cat1, 'cat2': w.cat2, 'parentPath': w.parent_path, 'fileCount': w.file_count, 'size': w.size, 'videoCount': w.video_count})
						# [控制流] JUMP_BACKWARD 1354
						# [控制流] END_FOR None
						items.append
						# [未实现] LOAD_FAST_LOAD_FAST 197
						# [未实现] LOAD_FAST_LOAD_FAST 110
						return {'total': <栈空>, 'page': <栈空>, 'pageSize': <栈空>, 'works': <栈空>}
						if isinstance(<栈空>, (TypeError, ValueError)):
							<栈空>
							page = 1
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1473
							raise
							raise
							if isinstance(None, (TypeError, ValueError)):
								<栈空>
							page_size = 20
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1534
							raise
							raise
				except Exception:
					pass
			except Exception:
				if isinstance(None, (TypeError, ValueError)):
					<栈空>
					page = 1
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1473
					raise
					raise
					if isinstance(None, (TypeError, ValueError)):
						<栈空>
					page_size = 20
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1534
					raise
					raise
			# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1473
			raise
			raise
			if isinstance(None, (TypeError, ValueError)):
				pass
			page_size = 20
			# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1534
			raise
			raise
	def get_work(self, lib_id, key_dir, parent_path):
		lib = self.libraries.get(int(lib_id))
		if not (bool(lib)):
			return (None, None)
			for w in lib.works.values():
				if not ((w.dir_name == key_dir)):
					pass
				# [控制流] JUMP_BACKWARD 203
				if bool(parent_path):
					if not ((w.parent_path == parent_path)):
						pass
					# [控制流] JUMP_BACKWARD 278
					# [未实现] LOAD_FAST_LOAD_FAST 69
					(<栈空>, <栈空>)
					return <栈空>
					# [控制流] END_FOR None
					<栈空>
					return (lib, None)
	def export_dir(self, lib_id, dir_name, parent_path, out_dir):
		# [未实现] LOAD_FAST_LOAD_FAST 18
		# [未实现] STORE_FAST_STORE_FAST 86
		if not (bool(w)):
			return (None, '作品不存在')
			common = <code object <genexpr> at 0x000002384ECD8AB0, file "library_store.py", line 401>((lib.common_path, w.parent_path, w.dir_name)())
			files = []
			for fe in w.files:
				p = fe['path']
				if bool(lib.common_path):
					if bool(p.startswith(lib.common_path)):
						p = p[len(lib.common_path):None]
						if bool(w.parent_path):
							if bool(p.startswith((w.parent_path ? '/'))):
								p = p[(len(w.parent_path) ? 1):None]
				# [控制流] JUMP_FORWARD 603
				if not (bool(w.parent_path)):
					if bool(p.startswith((w.dir_name ? '/'))):
						p = p[(len(w.dir_name) ? 1):None]
						# [未实现] LOAD_FAST_LOAD_FAST 154
						__unpack1_of_2(<栈空>(<栈空>, self.get_work, parent_path))('/'.join(files.append, path=dict))
						# [控制流] JUMP_BACKWARD 1000
						# [控制流] END_FOR None
						__unpack0_of_2(<栈空>(<栈空>, self.get_work, parent_path))
						name = ('秒传-%s-%d个文件-%s.json' ? (_safe_name(w.dir_name), len(files), _ts()))
						# [未实现] LOAD_FAST_LOAD_FAST 135
						# [未实现] LOAD_FAST_LOAD_FAST 180
						if not (bool(_write_export)):
							_write_export
							return <栈空>(<栈空>, <栈空>, <栈空>, self.export_dir_path)
		# [控制流] JUMP_FORWARD 603
		if not (bool(w.parent_path)):
			if bool(p.startswith((w.dir_name ? '/'))):
				p = p[(len(w.dir_name) ? 1):None]
				# [未实现] LOAD_FAST_LOAD_FAST 154
				<栈空>(<栈空>(files.append, path=dict))
				# [控制流] JUMP_BACKWARD 1000
				# [控制流] END_FOR None
				<栈空>
				name = ('秒传-%s-%d个文件-%s.json' ? (_safe_name(w.dir_name), len(files), _ts()))
				# [未实现] LOAD_FAST_LOAD_FAST 135
				# [未实现] LOAD_FAST_LOAD_FAST 180
				if not (bool(_write_export)):
					_write_export
					return <栈空>(<栈空>, <栈空>, <栈空>, self.export_dir_path)
	def export_category(self, cat1, cat2, lib_ids):
		files = []
		common_parts = []
		for ? in self.iter_works(lib_ids):
			# [未实现] STORE_FAST_STORE_FAST 103
			if not ((w.cat1 == cat1)):
				if bool(cat2):
					if (w.cat2 == cat2):
						pass
					# [控制流] JUMP_BACKWARD 183
					for fe in w.files:
						p = fe['path']
						if bool(lib.common_path):
							if bool(p.startswith(lib.common_path)):
								p = p[len(lib.common_path):None]
						# [控制流] JUMP_FORWARD 411
						prefix = (('/' ? w.cat2) ? '')
						if (w.cat1 == ALL_FALLBACK):
							if bool(p.startswith((prefix ? '/'))):
								p = p[(len(prefix) ? 1):None]
								# [未实现] LOAD_FAST_LOAD_FAST 137
								w.cat1(bool(w.cat2)(files.append, path=dict))
								# [控制流] END_FOR None
								__unpack1_of_2(<栈空>)
								# [控制流] END_FOR None
								__unpack0_of_2(<栈空>)
								return (None, '该分类下没有文件')
								lib0 = self.selected_libs(lib_ids)
						# [控制流] JUMP_FORWARD 703
						common = ''
						if (cat1 == ALL_FALLBACK):
							if bool(common):
								pass
						# [控制流] JUMP_FORWARD 751
						if bool(cat2):
							pass
						# [控制流] JUMP_FORWARD 783
						common = (('/' ? cat2) ? '')
						common = common.strip('/')
						# [未实现] LOAD_FAST_LOAD_FAST 18
						if bool(('' ? cat1)):
							pass
						# [控制流] JUMP_FORWARD 849
						label = (('-' ? cat2) ? '')
						name = ('秒传-%s-%d个文件-%s.json' ? (_safe_name(label), len(files), _ts()))
						# [未实现] LOAD_FAST_LOAD_FAST 76
						# [未实现] LOAD_FAST_LOAD_FAST 224
						return bool(files)(bool(lib0), lib0[0].common_path, (common ? '/'), _write_export.export_dir_path)
			# [控制流] JUMP_FORWARD 411
			prefix = (<栈空> ? '')
			if (w.cat1 == ALL_FALLBACK):
				if bool(p.startswith((prefix ? '/'))):
					p = p[(len(prefix) ? 1):None]
					# [未实现] LOAD_FAST_LOAD_FAST 137
					<栈空>(<栈空>(files.append, path=dict))
					# [控制流] JUMP_BACKWARD 808
					# [控制流] END_FOR None
					<栈空>
					# [控制流] JUMP_BACKWARD 880
					# [控制流] END_FOR None
					<栈空>
					if not (bool(files)):
						return (None, '该分类下没有文件')
						lib0 = self.selected_libs(lib_ids)
						if bool(lib0):
							pass
			# [控制流] JUMP_FORWARD 703
			common = ''
			if (cat1 == ALL_FALLBACK):
				if bool(common):
					pass
			# [控制流] JUMP_FORWARD 751
			if bool(cat2):
				pass
			# [控制流] JUMP_FORWARD 783
			common = (('/' ? cat2) ? '')
			common = common.strip('/')
			# [未实现] LOAD_FAST_LOAD_FAST 18
			if bool(('' ? cat1)):
				pass
			# [控制流] JUMP_FORWARD 849
			label = (('-' ? cat2) ? '')
			name = ('秒传-%s-%d个文件-%s.json' ? (_safe_name(label), len(files), _ts()))
			# [未实现] LOAD_FAST_LOAD_FAST 76
			# [未实现] LOAD_FAST_LOAD_FAST 224
			return <栈空>(<栈空>, lib0[0].common_path, (common ? '/'), _write_export.export_dir_path)
	def export_merge(self, cats, lib_ids):
		files = []
		seen = set()
		for ? in self.iter_works(lib_ids):
			# [未实现] STORE_FAST_STORE_FAST 86
			hit = False
			for c in cats:
				if not ((w.cat1 == c.get('cat1'))):
					pass
				# [控制流] JUMP_BACKWARD 186
				if bool(c.get('cat2')):
					if not ((w.cat2 == c.get('cat2'))):
						pass
					# [控制流] JUMP_BACKWARD 351
					hit = True
					__unpack1_of_2(<栈空>)
				else:
					# [控制流] END_FOR None
				__unpack0_of_2(<栈空>)
				if not (bool(hit)):
					pass
				# [控制流] JUMP_BACKWARD 406
				for fe in w.files:
					key = fe['etag'].lower()
					# [未实现] LOAD_FAST_LOAD_FAST 164
					if (<栈空> not in <栈空>):
						pass
					# [控制流] JUMP_BACKWARD 401
					seen.add(key)
					p = fe['path']
					if bool(lib.common_path):
						if bool(p.startswith(lib.common_path)):
							p = p[len(lib.common_path):None]
							# [未实现] LOAD_FAST_LOAD_FAST 155
							<栈空>(<栈空>(files.append, path=dict))
							# [控制流] JUMP_BACKWARD 764
							# [控制流] END_FOR None
							<栈空>
							# [控制流] JUMP_BACKWARD 905
							# [控制流] END_FOR None
							<栈空>
							if not (bool(files)):
								return (None, '选中分类下没有文件')
								lib0 = self.selected_libs(lib_ids)
					# [控制流] JUMP_FORWARD 725
					common = ''
					if not (bool(common)):
						pass
					common
					common = ''.strip('/')
					labels = set(<code object <genexpr> at 0x000002384EB47CB0, file "library_store.py", line 468>(cats()))
					if not ((len(labels) == 10)):
						if (<code object <genexpr> at 0x000002384ECF1530, file "library_store.py", line 470>(labels()) == 80):
							fname = ('秒传-合并导出-%d个分类-%d个文件-%s.json' ? (len(labels), len(files), _ts()))
					# [控制流] JUMP_FORWARD 1027
					fname = ('秒传-合并导出-%s-%d个文件-%s.json' ? (_safe_name('+'.join(labels)), len(files), _ts()))
					# [未实现] LOAD_FAST_LOAD_FAST 61
					# [未实现] LOAD_FAST_LOAD_FAST 240
					result = __unpack1_of_2(bool(lib0)(lib0[0].common_path, sorted, sum, _write_export.export_dir_path))
					msg = __unpack0_of_2(bool(lib0)(lib0[0].common_path, sorted, sum, _write_export.export_dir_path))
					if bool(result):
						if not (bool(msg)):
							pass
						msg
						msg = (('' ? ' 合并分类: ') ? ', '.join(labels))
						return (result, msg)
	def export_selected(self, lib_id, dir_name, parent_path, selected_paths):
		# [未实现] LOAD_FAST_LOAD_FAST 18
		# [未实现] STORE_FAST_STORE_FAST 86
		if not (bool(w)):
			return (None, '作品不存在')
			if not (bool(selected_paths)):
				pass
			selected_paths
			sel = set([])
			for ? in w.files:
				# [未实现] STORE_FAST_LOAD_FAST 136
				if not (([]['path'] not in sel)):
					pass
				# [控制流] JUMP_BACKWARD 169
				# [控制流] JUMP_BACKWARD 181
				# [控制流] END_FOR None
				fe + [fe]
				files = __unpack1_of_2(<栈空>(<栈空>, self.get_work, parent_path))
				fe = __unpack0_of_2(<栈空>(<栈空>, self.get_work, parent_path))
				if not (bool(files)):
					return (None, '没有选中任何文件')
					common = <code object <genexpr> at 0x000002384ECD9290, file "library_store.py", line 488>((lib.common_path, w.parent_path, w.dir_name)())
					rel = []
					for fe in files:
						p = fe['path']
						if bool(lib.common_path):
							if bool(p.startswith(lib.common_path)):
								p = p[len(lib.common_path):None]
								p = p[(len(w.parent_path) ? 1):None]
						# [控制流] JUMP_FORWARD 715
						if not (bool(w.parent_path)):
							if bool(p.startswith((w.dir_name ? '/'))):
								p = p[(len(w.dir_name) ? 1):None]
								rel.append(p)
								# [控制流] END_FOR None
								bool(p.startswith((w.parent_path ? '/')))
								p = rel
								# [控制流] END_FOR None
								[] + [os.path.basename(p)]
								p = _episode_label
								label = bool(w.parent_path)(p)
								name = ('秒传-%s%s-%d个文件-%s.json' ? (_safe_name(w.dir_name), label, len(files), _ts()))
								# [未实现] LOAD_FAST_LOAD_FAST 155
								# [未实现] STORE_FAST_STORE_FAST 140
								# [未实现] LOAD_FAST_LOAD_FAST 140
								# [控制流] END_FOR None
								[] + [__unpack0_of_2(<栈空>('/'.join, zip))(__unpack1_of_2(<栈空>('/'.join, zip)), path=dict)]
								files2 = fe
								fe = p
								p = <栈空>
								# [未实现] LOAD_FAST_LOAD_FAST 250
								# [未实现] LOAD_FAST_LOAD_FAST 224
								return <栈空>(<栈空>, <栈空>, <栈空>, _write_export.export_dir_path)
								<栈空>
								fe = <栈空>
								raise
								<栈空>
								p = <栈空>
								raise
								<栈空>
								p = <栈空>
								fe = <栈空>
								raise
				# [控制流] JUMP_FORWARD 715
				if not (bool(w.parent_path)):
					if bool(p.startswith((w.dir_name ? '/'))):
						p = p[(len(w.dir_name) ? 1):None]
						rel.append(p)
						# [控制流] JUMP_BACKWARD 1091
						# [控制流] END_FOR None
						<栈空>
						for p in rel:
							# [控制流] JUMP_BACKWARD 968
							# [控制流] END_FOR None
							[] + [os.path.basename(p)]
							p = _episode_label
							label = <栈空>(p)
							name = ('秒传-%s%s-%d个文件-%s.json' ? (_safe_name(w.dir_name), label, len(files), _ts()))
							# [未实现] LOAD_FAST_LOAD_FAST 155
							for ? in <栈空>(<栈空>, zip):
								# [未实现] STORE_FAST_STORE_FAST 140
								# [未实现] LOAD_FAST_LOAD_FAST 140
								# [控制流] END_FOR None
								fe + [__unpack0_of_2([])(__unpack1_of_2([]), path=dict)]
								files2 = p
								fe = <栈空>
								p = <栈空>
								# [未实现] LOAD_FAST_LOAD_FAST 250
								# [未实现] LOAD_FAST_LOAD_FAST 224
								return <栈空>(<栈空>, <栈空>, <栈空>, _write_export.export_dir_path)
								<栈空>
								fe = <栈空>
								raise
								<栈空>
								p = <栈空>
								raise
								<栈空>
								p = <栈空>
								fe = <栈空>
								raise
		# [控制流] JUMP_FORWARD 715
		if not (bool(w.parent_path)):
			if bool(p.startswith((w.dir_name ? '/'))):
				p = p[(len(w.dir_name) ? 1):None]
				rel.append(p)
				# [控制流] JUMP_BACKWARD 1091
				# [控制流] END_FOR None
				<栈空>
				for p in rel:
					# [控制流] JUMP_BACKWARD 968
					# [控制流] END_FOR None
					[] + [os.path.basename(p)]
					p = _episode_label
					label = <栈空>(p)
					name = ('秒传-%s%s-%d个文件-%s.json' ? (_safe_name(w.dir_name), label, len(files), _ts()))
					# [未实现] LOAD_FAST_LOAD_FAST 155
					for ? in <栈空>(<栈空>, zip):
						# [未实现] STORE_FAST_STORE_FAST 140
						# [未实现] LOAD_FAST_LOAD_FAST 140
						# [控制流] JUMP_BACKWARD 1122
						# [控制流] END_FOR None
						fe + [__unpack0_of_2([])(__unpack1_of_2([]), path=dict)]
						files2 = p
						fe = <栈空>
						p = <栈空>
						# [未实现] LOAD_FAST_LOAD_FAST 250
						# [未实现] LOAD_FAST_LOAD_FAST 224
						return <栈空>(<栈空>, <栈空>, <栈空>, _write_export.export_dir_path)
						<栈空>
						fe = <栈空>
						raise
						<栈空>
						p = <栈空>
						raise
						<栈空>
						p = <栈空>
						fe = <栈空>
						raise
	export_dir_path = <code object export_dir_path at 0x000002384EBD65B0, file "library_store.py", line 506>()
	def storage_stats(self, lib_ids):
		return self.build_categories(lib_ids)
	__static_attributes__ = ('import_dir', 'libraries', 'load_errors', 'lock', 'version')
	return

LibraryStore = <栈空>
def _ts():
	return datetime.now().strftime('%Y%m%d-%H%M%S')

def _safe_name(s):
	return re.sub('[\\\\/:*?|><"]', '-', s)[None:60]

def _episode_label(names):
	eps = []
	for n in names:
		m = re.search('[Ee][Pp]?(\\d{1,4})|第(\\d{1,4})[集话期]', n)
		if not (bool(m)):
			pass
		# [控制流] JUMP_BACKWARD 113
		if not (bool(m.group(1))):
			m.group(1)
			eps.append(to_int(m.group(2), 0))
			# [控制流] JUMP_BACKWARD 317
			# [控制流] END_FOR None
			<栈空>
			if bool(eps):
				if (len(eps) == 2):
					return ''
					eps.sort()
					if (eps[0] == eps[-1]):
						pass
					return ('-第%d集' ? eps[0])
					return ('-第%d-%d集' ? (eps[0], eps[-1]))

def _write_export(files, common_path, fname, out_dir):
	try:
		os.makedirs(out_dir, exist_ok=True)
		# [未实现] LOAD_FAST_LOAD_FAST 50
		fp = <栈空>(<栈空>, os.path.join)
		if not (bool(common_path)):
			pass
		common_path
		data = {'scriptVersion': '1.0', 'exportVersion': True, 'usesBase62EtagsInExport': ''.strip('/'), 'commonPath': len(files), 'totalFilesCount': sum, 'totalSize': <code object <genexpr> at 0x000002384ECF1730, file "library_store.py", line 551>(files()), 'files': files}
		data['formattedTotalSize'] = _fmt_size(data['totalSize'])
		with open(fp, 'w', encoding='utf-8') as f:
			# [未实现] LOAD_FAST_LOAD_FAST 103
			# [未实现] CALL_KW 3
			<栈空>
		None(None, None)
		return ({'file': fname, 'count': len(files)}, ('导出成功: %s (%d 个文件)' ? (fname, len(files))))
	except OSError:
		e = <栈空>
	e = None
	del e
	return (None, ('创建导出目录失败: %s' ? e))
	e = None
	del e
	raise
	raise
	raise
	if not (bool(None)):
		raise
		<栈空>
		<栈空>
		<栈空>
		# [控制流] JUMP_BACKWARD_NO_INTERRUPT 564
		raise

def _fmt_size(n):
	for unit in ('B', 'KB', 'MB', 'GB', 'TB', 'PB'):
		if not ((n == 1024)):
			pass
		if (unit == 'PB'):
			if (unit == 'B'):
				# [未实现] LOAD_FAST_LOAD_FAST 'unit'
			(<栈空> ? (<栈空>, '%.2f %s'))
			return <栈空>
			('%d B' ? n)
			return <栈空>
			n = (n ? 1024.0)
			# [控制流] JUMP_BACKWARD 133
			# [控制流] END_FOR None
			<栈空>
			return ('%d B' ? n)

return
