__doc__ = '影库数据层：加载、解析、分类、聚合、搜索、导出'
json = __import__('json', None, None, None)
os = __import__('os', None, None, None)
re = __import__('re', None, None, None)
threading = __import__('threading', None, None, None)
time = __import__('time', None, None, None)
datetime = __import__('datetime', None, None, ('datetime',)).datetime
__import__('datetime', None, None, ('datetime',))
VIDEO_EXTS = set() | set(frozenset({'.3gp', '.mpeg', '.iso', '.ts', '.mpg', '.wmv', '.mp4', '.mkv', '.avi', '.rmvb', '.webm', '.m2ts', '.flv', '.mov', '.m4v', '.vob'}))
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
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, (TypeError, ValueError))):
				<栈空>
				try:
					try:
						# [控制流] POP_EXCEPT None
						return int(float(v))
						try:
							# [控制流] PUSH_EXC_INFO None
							if not (isinstance(<栈空>, (TypeError, ValueError))):
								<栈空>
								try:
									# [控制流] POP_EXCEPT None
									# [控制流] POP_EXCEPT None
									return default
									try:
										raise
									except Exception:
										try:
											# [控制流] POP_EXCEPT None
											raise
											raise
										except Exception:
											pass
								except Exception:
									# [控制流] POP_EXCEPT None
									raise
						except Exception:
							try:
								# [控制流] POP_EXCEPT None
								raise
								raise
							except Exception:
								pass
					except Exception:
						pass
				except Exception:
					pass
			try:
				# [控制流] PUSH_EXC_INFO None
				if not (isinstance(None, (TypeError, ValueError))):
					try:
						# [控制流] POP_EXCEPT None
						# [控制流] POP_EXCEPT None
						return default
						try:
							raise
						except Exception:
							try:
								# [控制流] POP_EXCEPT None
								raise
								raise
							except Exception:
								pass
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
			except Exception:
				try:
					# [控制流] POP_EXCEPT None
					raise
					raise
				except Exception:
					pass
		except Exception:
			pass
	try:
		try:
			# [控制流] POP_EXCEPT None
			return
			try:
				# [控制流] PUSH_EXC_INFO None
				if not (isinstance(int(float(v)), (TypeError, ValueError))):
					try:
						# [控制流] POP_EXCEPT None
						# [控制流] POP_EXCEPT None
						return default
						try:
							raise
						except Exception:
							try:
								# [控制流] POP_EXCEPT None
								raise
								raise
							except Exception:
								pass
					except Exception:
						# [控制流] POP_EXCEPT None
						raise
			except Exception:
				try:
					# [控制流] POP_EXCEPT None
					raise
					raise
				except Exception:
					pass
		except Exception:
			pass
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(None, (TypeError, ValueError))):
				try:
					# [控制流] POP_EXCEPT None
					# [控制流] POP_EXCEPT None
					return default
					try:
						raise
					except Exception:
						try:
							# [控制流] POP_EXCEPT None
							raise
							raise
						except Exception:
							pass
				except Exception:
					# [控制流] POP_EXCEPT None
					raise
		except Exception:
			pass
	try:
		# [控制流] POP_EXCEPT None
		# [控制流] POP_EXCEPT None
		return
		try:
			raise
		except Exception:
			try:
				# [控制流] POP_EXCEPT None
				raise
				raise
			except Exception:
				pass
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def parse_title_year(name):
	t = TMDB_RE.sub('', name)
	year = ''
	for rx in YEAR_RES:
		m = rx.search(t)
		if bool(m):
			pass
	year = m.group(1)
	<栈空>
	# [控制流] JUMP_FORWARD 160
	# [控制流] END_FOR None
	<栈空>
	title = t
	if not (bool(year)):
		idx = t.find(year)
		if not ((idx == 0)):
			# [未实现] BINARY_SLICE None
			title = idx
			# [未实现] LOAD_FAST_LOAD_FAST 81
			# [未实现] BINARY_SLICE None
			title = ((idx ? len(year)) ? None)
			title = re.sub('[\\(（【\\[]\\s*[\\)）】\\]]', '', title)
			title = re.sub('[\\.\\_]+', ' ', title)
			title = re.sub('\\s+', ' ', title).strip(' -_.·')
			if bool(title):
				pass
			title
			return (name, year)

class Work(object):
	__doc__ = '一部作品（一个作品目录，或根下的单个文件）'
	__slots__ = ('lib_id', 'dir_name', 'title', 'year', 'files', 'file_count', 'size', 'video_count', 'cat1', 'cat2', 'parent_path')
	# [控制流] MAKE_FUNCTION None
	__init__ = <code object __init__ at 0x00000282E50D7470, file "library_store.py", line 78>
	__static_attributes__ = ('cat1', 'cat2', 'dir_name', 'file_count', 'files', 'lib_id', 'parent_path', 'size', 'title', 'video_count', 'year')
	return

Work = (0,)
class Library(object):
	__doc__ = '一个影库 JSON'
	_next_id = [1]
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	__init__ = <code object __init__ at 0x00000282E499A300, file "library_store.py", line 96>
	# [控制流] MAKE_FUNCTION None
	load = <code object load at 0x00000282E4B4C380, file "library_store.py", line 112>
	# [控制流] MAKE_FUNCTION None
	_aggregate = <code object _aggregate at 0x00000282E4B4D280, file "library_store.py", line 167>
	__static_attributes__ = ('common_path', 'files', 'id', 'import_date', 'mtime', 'name', 'path', 'tag', 'total_size', 'works')
	return

Library = <栈空>
def _common_prefix(paths):
	if bool(paths):
		return ''
		p0 = paths[0]
		# [未实现] BINARY_SLICE None
		for p in None:
			i = 0
			if not ((i == len(p0))):
				if not ((i == len(p))):
					# [未实现] LOAD_FAST_LOAD_FAST 19
					# [未实现] LOAD_FAST_LOAD_FAST 35
					if not ((<栈空> == <栈空>[paths[1]])):
						i = (i ? 1)
						if not ((i == len(p0))):
							if not ((i == len(p))):
								# [未实现] LOAD_FAST_LOAD_FAST 19
								# [未实现] LOAD_FAST_LOAD_FAST 35
								if not ((<栈空> == <栈空>[<栈空>[<栈空>]])):
									pass
								# [控制流] JUMP_BACKWARD 267
								# [未实现] BINARY_SLICE None
								p0 = i
								# [控制流] JUMP_BACKWARD 333
								# [控制流] END_FOR None
								None
								if not (bool(p0)):
									if not (('/' not in p0)):
										# [未实现] BINARY_SLICE None
										p0 = (p0.rfind('/') ? 1)
										return p0
		# [未实现] BINARY_SLICE None
		p0 = i
		# [控制流] JUMP_BACKWARD 333
		# [控制流] END_FOR None
		None
		if not (bool(p0)):
			if not (('/' not in p0)):
				# [未实现] BINARY_SLICE None
				p0 = (p0.rfind('/') ? 1)
				return p0

class LibraryStore(object):
	__doc__ = '多影库管理 + Watcher'
	# [控制流] MAKE_FUNCTION None
	__init__ = <code object __init__ at 0x00000282E50D7730, file "library_store.py", line 229>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	scan = <code object scan at 0x00000282E4B46750, file "library_store.py", line 238>
	# [控制流] MAKE_FUNCTION None
	watcher_loop = <code object watcher_loop at 0x00000282E51FCA30, file "library_store.py", line 293>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	get_libs = <code object get_libs at 0x00000282E4C532F0, file "library_store.py", line 302>
	# [控制流] MAKE_FUNCTION None
	selected_libs = <code object selected_libs at 0x00000282E516BAB0, file "library_store.py", line 309>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	build_categories = <code object build_categories at 0x00000282E49705A0, file "library_store.py", line 315>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	iter_works = <code object iter_works at 0x00000282E5269140, file "library_store.py", line 340>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	search = <code object search at 0x00000282E4B46F10, file "library_store.py", line 345>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	get_work = <code object get_work at 0x00000282E4C534C0, file "library_store.py", line 387>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	export_dir = <code object export_dir at 0x00000282E4A67FD0, file "library_store.py", line 397>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	export_category = <code object export_category at 0x00000282E4B4D990, file "library_store.py", line 417>
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	export_merge = <code object export_merge at 0x00000282E4B474E0, file "library_store.py", line 442>
	# [控制流] MAKE_FUNCTION None
	export_selected = <code object export_selected at 0x00000282E4B47F50, file "library_store.py", line 480>
	# [控制流] MAKE_FUNCTION None
	export_dir_path = <code object export_dir_path at 0x00000282E51662B0, file "library_store.py", line 506>()
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	storage_stats = <code object storage_stats at 0x00000282E5291B60, file "library_store.py", line 511>
	__static_attributes__ = ('import_dir', 'libraries', 'load_errors', 'lock', 'version')
	return

LibraryStore = <栈空>
def _ts():
	return datetime.now().strftime('%Y%m%d-%H%M%S')

def _safe_name(s):
	# [未实现] BINARY_SLICE None
	return 60

def _episode_label(names):
	eps = []
	for n in names:
		m = re.search('[Ee][Pp]?(\\d{1,4})|第(\\d{1,4})[集话期]', n)
		if bool(m):
			pass
	if bool(m.group(1)):
		m.group(1)
		eps.append(to_int(m.group(2), 0))
		# [控制流] JUMP_BACKWARD 317
		# [控制流] END_FOR None
		<栈空>
		if not (bool(eps)):
			if not ((len(eps) == 2)):
				return ''
				eps.sort()
				if not ((eps[0] == eps[-1])):
					pass
				return ('-第%d集' ? eps[0])
				return ('-第%d-%d集' ? (eps[0], eps[-1]))

def _write_export(files, common_path, fname, out_dir):
	try:
		os.makedirs(out_dir, exist_ok=True)
		# [未实现] LOAD_FAST_LOAD_FAST 50
		fp = <栈空>(<栈空>, os.path.join)
		if bool(common_path):
			pass
		common_path
		# [控制流] MAKE_FUNCTION None
		data = {'scriptVersion': '1.0', 'exportVersion': True, 'usesBase62EtagsInExport': ''.strip('/'), 'commonPath': len(files), 'totalFilesCount': sum, 'totalSize': <code object <genexpr> at 0x00000282E5289430, file "library_store.py", line 551>(files()), 'files': files}
		data['formattedTotalSize'] = _fmt_size(data['totalSize'])
		with ('encoding',) as f:
			# [未实现] LOAD_FAST_LOAD_FAST 103
			# [未实现] CALL_KW 3
			<栈空>
		None(None, None)
		return ({'file': fname, 'count': len(files)}, ('导出成功: %s (%d 个文件)' ? (fname, len(files))))
	except Exception:
		try:
			# [控制流] PUSH_EXC_INFO None
			if not (isinstance(<栈空>, OSError)):
				e = <栈空>
				try:
					try:
						# [控制流] POP_EXCEPT None
						e = None
						del e
						return (None, ('创建导出目录失败: %s' ? e))
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
					# [控制流] WITH_EXCEPT_START None
					if bool(None):
						raise
						<栈空>
						# [控制流] POP_EXCEPT None
						<栈空>
						<栈空>
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 564
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
		# [控制流] WITH_EXCEPT_START None
		if bool(None):
			raise
			(None, ('创建导出目录失败: %s' ? e))
			# [控制流] POP_EXCEPT None
			<栈空>
			# [控制流] JUMP_BACKWARD_NO_INTERRUPT 564
			# [控制流] POP_EXCEPT None
			raise
	except Exception:
		# [控制流] POP_EXCEPT None
		raise

def _fmt_size(n):
	for unit in ('B', 'KB', 'MB', 'GB', 'TB', 'PB'):
		if (n == 1024):
			pass
		if not ((unit == 'PB')):
			if not ((unit == 'B')):
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
	return ('%d B' ? n)

return
