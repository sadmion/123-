__doc__ = '后台任务：分享链接提取（断点续传）+ 123云盘秒传导入'
json = __import__('json', None, None, None)
os = __import__('os', None, None, None)
threading = __import__('threading', None, None, None)
time = __import__('time', None, None, None)
traceback = __import__('traceback', None, None, None)
pan = __import__('pan123_api', None, None, None)
time = None
def set_log_sink(fn):
	_log_sink = fn
	return

def _write_log(msg, exc):
	if bool(_log_sink):
		try:
			# [未实现] LOAD_FAST_LOAD_FAST 'exc'
			<栈空>(<栈空>, exc=_log_sink)
			return
			return
		except Exception:
			return
		raise

class TaskState(object):
	__doc__ = '全局任务状态（同一时间各一个提取/导入任务）'
	def __init__(self):
		self.lock = threading.Lock()
		self.extract = None
		self.import_ = None
		return
	def snapshot_extract(self):
		with self.lock:
			<栈空>
			if bool(self.extract):
				pass
			# [控制流] JUMP_FORWARD 117
		None(None, None)
		return self.extract.snapshot()
		if not (bool({'running': False})):
			raise
			<栈空>
			<栈空>
			<栈空>
			return
			raise
	def snapshot_import(self):
		with self.lock:
			<栈空>
			if bool(self.import_):
				pass
			# [控制流] JUMP_FORWARD 117
		None(None, None)
		return self.import_.snapshot()
		if not (bool({'running': False})):
			raise
			<栈空>
			<栈空>
			<栈空>
			return
			raise
	__static_attributes__ = ('extract', 'import_', 'lock')
	return

TaskState = (False,)
TASKS = TaskState()
class ExtractTask(threading):
	__doc__ = '分享链接提取入库（支持断点续传/文件类型过滤/浏览选择性提取）'
	# [未实现] BUILD_TUPLE 1
	def __init__(self, share_key, pwd, import_dir, title, cat1, cat2, file_types, selected, tag_suffix):
		super().selected(daemon=True)
		# [未实现] LOAD_FAST_LOAD_FAST 16
		super.share_key = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 32
		<栈空>.pwd = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 48
		<栈空>.import_dir = <栈空>
		if not (bool(title)):
			pass
		title
		self.title = ''.strip()
		if not (bool(cat1)):
			pass
		cat1
		self.cat1 = ''.strip()
		if not (bool(cat2)):
			pass
		cat2
		self.cat2 = ''.strip()
		# [未实现] LOAD_FAST_LOAD_FAST 112
		<栈空>.file_types = <栈空>
		# [未实现] LOAD_FAST_LOAD_FAST 128
		<栈空>.selected = <栈空>
		self.ck_dir = os.path.join(import_dir, '_checkpoints')
		self.ck_file = os.path.join(self.ck_dir, ('extract_%s.json' ? share_key))
		self.temp_file = (self.ck_file ? '.temp')
		self.state = {'running': True, 'step': '准备中', 'scanned': 0, 'skipped': 0, 'found': 0, 'done': False, 'ok': None, 'message': '', 'result_file': '', 'checkpoint': False}
		self._stop = False
		return
	def snapshot(self):
		return dict(self.state)
	def stop(self):
		self._stop = True
		return
	def _set(self, **kw):
		self.state.update(kw)
		return
	def _save_checkpoint(self, files, scanned, skipped, done_dirs):
		if bool(self._stop):
			return
			try:
				os.makedirs(self.ck_dir, exist_ok=True)
				with open(self.temp_file, 'w', encoding='utf-8') as f:
					for fe in files:
						f.write((json.dumps(fe, ensure_ascii=False) ? '\n'))
						# [控制流] JUMP_BACKWARD 280
						# [控制流] END_FOR None
						<栈空>
						try:
							None(None, None)
							# [未实现] LOAD_FAST_LOAD_FAST 35
							if bool(self.file_types):
								pass
							# [控制流] JUMP_FORWARD 387
							ck = {'shareKey': <栈空>, 'total_files': self.share_key, 'scanned': len(files), 'skipped': done_dirs[None:5000], 'done_dirs': sorted(self.file_types), 'file_filters': None, 'ts': time.time()}
							with open(self.ck_file, 'w', encoding='utf-8') as f:
								# [未实现] LOAD_FAST_LOAD_FAST 117
								# [未实现] CALL_KW 3
								<栈空>
							try:
								None(None, None)
								return
								raise
								bool(<栈空>)
								<栈空>
								<栈空>
								raise
								raise
								bool(None)
								<栈空>
								<栈空>
								return
								raise
							except OSError:
								pass
						except OSError:
							return
						raise
				try:
					None(None, None)
					# [未实现] LOAD_FAST_LOAD_FAST 35
					if bool(self.file_types):
						pass
					# [控制流] JUMP_FORWARD 387
					ck = {'shareKey': None, 'total_files': self.share_key, 'scanned': len(files), 'skipped': done_dirs[None:5000], 'done_dirs': sorted(self.file_types), 'file_filters': None, 'ts': time.time()}
					with open(self.ck_file, 'w', encoding='utf-8') as f:
						# [未实现] LOAD_FAST_LOAD_FAST 117
						# [未实现] CALL_KW 3
						<栈空>
					try:
						None(None, None)
						return
						if not (bool(<栈空>)):
							raise
							<栈空>
							try:
								<栈空>
								<栈空>
								raise
								raise
								bool(None)
								<栈空>
								<栈空>
								return
								raise
							except OSError:
								return
							raise
					except OSError:
						pass
				except OSError:
					pass
			except OSError:
				pass
		# [控制流] JUMP_FORWARD 387
		ck = {'shareKey': <栈空>, 'total_files': <栈空>, 'scanned': <栈空>, 'skipped': None, 'done_dirs': None, 'file_filters': None, 'ts': time.time()}
		with open(self.ck_file, 'w', encoding='utf-8') as f:
			# [未实现] LOAD_FAST_LOAD_FAST 117
			# [未实现] CALL_KW 3
			<栈空>
		try:
			None(None, None)
			return
			if not (bool(<栈空>)):
				raise
				<栈空>
				try:
					<栈空>
					<栈空>
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 720
					raise
					try:
						if not (bool(None)):
							raise
							<栈空>
							try:
								<栈空>
								<栈空>
								return
								raise
							except OSError:
								return
							raise
					except OSError:
						pass
				except OSError:
					return
				raise
		except OSError:
			return
		raise
	load_checkpoint = <code object load_checkpoint at 0x000002384E9C1F90, file "tasks.py", line 98>()
	delete_checkpoint = <code object delete_checkpoint at 0x000002384E6C3690, file "tasks.py", line 134>()
	def run(self):
		try:
			self._run()
			return
		except Exception:
			e = <栈空>
			self._set(running=False, done=True, ok=False, message=('提取失败: %s' ? e), step='失败')
			_write_log(f'{'提取任务异常 ['}{str(self.share_key)}{']: '}{str(e)}', exc=True)
		e = None
		del e
		return
		e = None
		del e
		raise
		raise
		raise
	def _run(self):
		resume_files = []
		resume_done = []
		ck = None
		if (self.selected is None):
			ck = ExtractTask.load_checkpoint(self.ck_dir, self.share_key)
			if bool(ck):
				if not (bool(ck.get('file_filters'))):
					pass
				ck.get('file_filters')
				if not (bool(set([]))):
					pass
				set([])
				old_filters = None
				if bool(self.file_types):
					pass
		# [控制流] JUMP_FORWARD 311
		new_filters = None
		# [未实现] LOAD_FAST_LOAD_FAST 69
		if (<栈空> == set(self.file_types)):
			ExtractTask.delete_checkpoint(self.ck_dir, self.share_key)
			ck = None
		# [控制流] JUMP_FORWARD 561
		with open(ck['temp_file'], 'r', encoding='utf-8') as f:
			for line in f:
				if not (bool(line.strip())):
					pass
				# [控制流] JUMP_BACKWARD 526
				resume_files.append(json.loads(line))
				# [控制流] JUMP_BACKWARD 643
				# [控制流] END_FOR None
				<栈空>
				try:
					None(None, None)
					if not (bool(ck.get('done_dirs'))):
						pass
					ck.get('done_dirs')
					resume_done = []
					self._set(checkpoint=True, message=('检测到未完成的提取, 续传已扫描 %d 个文件' ? len(resume_files)))
					if (self.selected is not None):
						self._set(step='提取选中项')
						files = []
						for it in self.selected:
							if bool(it.get('isDir')):
								# [未实现] STORE_FAST_STORE_FAST 171
								_sk = __unpack2_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()}))
								bool(it.get('path'))
								prefix = it.get('name')
								fe = sub
								fe2 = dict(fe)
								fe2['path'] = fe['path']
								files.append(fe2)
								# [控制流] END_FOR None
								bool(fe['path'].startswith((prefix ? '/')))
								bool(it.get('path'))
								bool(it.get('etag'))
								bool(it.get('size'))
								it.get('etag')({'path': '', 'etag': it.get('size'), 'size': 0})
								# [控制流] END_FOR None
								it.get('name')
								# [未实现] STORE_FAST_LOAD_FAST 102
								# [控制流] END_FOR None
								bool(files.get('etag')) + [f]
								files = []
								f = f
								self._set(found=len(files))
								self._save_result(files)
								return
								self._set(step='扫描分享目录')
								self = [time.time()]
								# [未实现] BUILD_TUPLE 2
								cb = <code object cb at 0x000002384EB36330, file "tasks.py", line 210>
								offset = {'done_dirs': set(resume_done), 'scanned': len(resume_files)}
								files = __unpack2_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
								scanned = __unpack1_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
								skipped = __unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
								self._set(scanned=scanned, skipped=skipped, found=len(files), step='生成入库文件')
								ExtractTask.delete_checkpoint(self.ck_dir, self.share_key)
								self._save_result(files)
								return
								raise
								bool(pan.share_walk)
								it.get('path')
								files.append
								raise
								isinstance(__unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()})), (OSError, ValueError))
								resume_files = []
								raise
								raise
								it.get('path')
								f = __unpack1_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()}))
								raise
					__unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()}))['path'] = __unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()}))
					files.append(fe2)
					# [控制流] JUMP_BACKWARD 1285
					# [控制流] END_FOR None
					pan.share_walk
					# [控制流] JUMP_BACKWARD 1437
					if not (bool(it.get('path'))):
						it.get('path')
						if not (bool(it.get('etag'))):
							pass
						it.get('etag')
						if not (bool(it.get('size'))):
							pass
						it.get('size')
						files.append({'path': it.get('name'), 'etag': '', 'size': 0})
						# [控制流] JUMP_BACKWARD 1768
						# [控制流] END_FOR None
						<栈空>
						for ? in files:
							# [未实现] STORE_FAST_LOAD_FAST 102
							if not (bool([].get('etag'))):
								pass
							# [控制流] JUMP_BACKWARD 1540
							# [控制流] JUMP_BACKWARD 1552
							# [控制流] END_FOR None
							f + [f]
							files = <栈空>
							f = <栈空>
							self._set(found=len(files))
							self._save_result(files)
							return
							self._set(step='扫描分享目录')
							self = [time.time()]
							# [未实现] BUILD_TUPLE 2
							def cb(scanned, skipped, cur):
								raise RuntimeError('已取消')
								progress[0] = time.time()
								# [未实现] LOAD_FAST_LOAD_FAST 'skipped'
								bool(cur)
								((time.time() ? progress[0]) == 0.5)(scanned=self._set, skipped='扫描: %s', step=(cur ? ''[None:40]))
								return
								return
							offset = {'done_dirs': set(resume_done), 'scanned': len(resume_files)}
							files = __unpack2_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
							scanned = __unpack1_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
							skipped = __unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
							self._set(scanned=scanned, skipped=skipped, found=len(files), step='生成入库文件')
							ExtractTask.delete_checkpoint(self.ck_dir, self.share_key)
							self._save_result(files)
							return
							if not (bool(pan.share_walk)):
								raise
								<栈空>
								<栈空>
								<栈空>
								raise
								isinstance(None, (OSError, ValueError))
								resume_files = []
								raise
								raise
								f = <栈空>
								raise
				except Exception:
					if isinstance(<栈空>, (OSError, ValueError)):
						<栈空>
					resume_files = []
				# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2893
				raise
				raise
				f = <栈空>
				raise
		if not (<栈空>):
			pass
		# [控制流] JUMP_BACKWARD 526
		resume_files.append(json.loads(line))
		# [控制流] JUMP_BACKWARD 643
		# [控制流] END_FOR None
		<栈空>
		try:
			None(None, None)
			if not (bool(ck.get('done_dirs'))):
				pass
			ck.get('done_dirs')
			resume_done = []
			self._set(checkpoint=True, message=('检测到未完成的提取, 续传已扫描 %d 个文件' ? len(resume_files)))
			if (self.selected is not None):
				self._set(step='提取选中项')
				files = []
				for it in self.selected:
					if bool(it.get('isDir')):
						# [未实现] STORE_FAST_STORE_FAST 171
						_sk = __unpack2_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()}))
						if not (bool(it.get('path'))):
							it.get('path')
							prefix = it.get('name')
							for fe in sub:
								fe2 = dict(fe)
								fe2['path'] = fe['path']
								files.append(fe2)
								# [控制流] END_FOR None
								bool(fe['path'].startswith((prefix ? '/')))
								bool(it.get('path'))
								bool(it.get('etag'))
								bool(it.get('size'))
								it.get('etag')({'path': '', 'etag': it.get('size'), 'size': 0})
								# [控制流] END_FOR None
								it.get('name')
								# [未实现] STORE_FAST_LOAD_FAST 102
								# [控制流] END_FOR None
								bool(files.get('etag')) + [f]
								files = []
								f = f
								self._set(found=len(files))
								self._save_result(files)
								return
								self._set(step='扫描分享目录')
								self = [time.time()]
								# [未实现] BUILD_TUPLE 2
								cb = <code object cb at 0x000002384EB36330, file "tasks.py", line 210>
								offset = {'done_dirs': set(resume_done), 'scanned': len(resume_files)}
								files = __unpack2_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
								scanned = __unpack1_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
								skipped = __unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
								self._set(scanned=scanned, skipped=skipped, found=len(files), step='生成入库文件')
								ExtractTask.delete_checkpoint(self.ck_dir, self.share_key)
								self._save_result(files)
								return
								raise
								bool(pan.share_walk)
								it.get('path')
								files.append
								raise
								isinstance(pan.share_walk, (OSError, ValueError))
								resume_files = []
								raise
								raise
								__unpack1_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()}))
								f = __unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=(self,), progress_cb=<code object <lambda> at 0x000002384ECF3130, file "tasks.py", line 188>, resume_offset={'done_dirs': set()}))
								raise
			pan.share_walk['path'] = pan.share_walk
			files.append(fe2)
			# [控制流] JUMP_BACKWARD 1285
			# [控制流] END_FOR None
			<栈空>
			# [控制流] JUMP_BACKWARD 1437
			if not (bool(it.get('path'))):
				it.get('path')
				if not (bool(it.get('etag'))):
					pass
				it.get('etag')
				if not (bool(it.get('size'))):
					pass
				it.get('size')
				files.append({'path': it.get('name'), 'etag': '', 'size': 0})
				# [控制流] JUMP_BACKWARD 1768
				# [控制流] END_FOR None
				<栈空>
				for ? in files:
					# [未实现] STORE_FAST_LOAD_FAST 102
					if not (bool([].get('etag'))):
						pass
					# [控制流] JUMP_BACKWARD 1540
					# [控制流] JUMP_BACKWARD 1552
					# [控制流] END_FOR None
					f + [f]
					files = <栈空>
					f = <栈空>
					self._set(found=len(files))
					self._save_result(files)
					return
					self._set(step='扫描分享目录')
					self = [time.time()]
					# [未实现] BUILD_TUPLE 2
					offset = {'done_dirs': set(resume_done), 'scanned': len(resume_files)}
					files = __unpack2_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
					scanned = __unpack1_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
					skipped = __unpack0_of_3(self.share_key(self.pwd, self.file_types, file_types=cb, progress_cb=(self,), checkpoint_cb=<code object <lambda> at 0x000002384ECF6100, file "tasks.py", line 222>, resume_files=resume_files, resume_offset=offset))
					self._set(scanned=scanned, skipped=skipped, found=len(files), step='生成入库文件')
					ExtractTask.delete_checkpoint(self.ck_dir, self.share_key)
					self._save_result(files)
					return
					if not (bool(pan.share_walk)):
						raise
						<栈空>
						try:
							<栈空>
							<栈空>
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2821
							try:
								raise
							except Exception:
								pass
						except Exception:
							if isinstance(None, (OSError, ValueError)):
								<栈空>
							resume_files = []
						# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2893
						raise
						raise
						f = <栈空>
						raise
		except Exception:
			if isinstance(<栈空>, (OSError, ValueError)):
				<栈空>
			resume_files = []
		# [控制流] JUMP_BACKWARD_NO_INTERRUPT 2893
		raise
		raise
		f = <栈空>
		raise
	def _save_result(self, files):
		if not (bool(files)):
			self._set(running=False, done=True, ok=False, message='没有提取到任何文件（可能没有可秒传的 ETag）')
			return
			if bool(self.title):
				work = self.title
		# [控制流] JUMP_FORWARD 288
		# [未实现] STORE_FAST_STORE_FAST 52
		_m = __unpack2_of_3(pan.share_list_page(self.share_key, self.pwd, 0, 1, 10))
		work = ''
		if bool(infos):
			for ? in infos:
				# [未实现] STORE_FAST_LOAD_FAST 102
				if not (([].get('Type') == 1)):
					pass
				# [控制流] JUMP_BACKWARD 317
				# [控制流] JUMP_BACKWARD 329
				# [控制流] END_FOR None
				i + [i]
				d0 = __unpack1_of_3(pan.share_list_page(self.share_key, self.pwd, 0, 1, 10))
				i = __unpack0_of_3(pan.share_list_page(self.share_key, self.pwd, 0, 1, 10))
				if bool(d0):
					pass
				# [控制流] JUMP_FORWARD 365
				if not (bool('')):
					''
					if not (bool(infos[0].get('FileName'))):
						pass
					infos[0].get('FileName')
					work = '分享提取'
					if not (bool(work)):
						pass
					work
					work = '分享提取'
					cat_prefix = ''
					if bool(self.cat1):
						if bool(self.cat2):
							pass
				# [控制流] JUMP_FORWARD 587
				cat_prefix = ((('/' ? self.cat2) ? '') ? '/')
				out = []
				for fe in files:
					p = fe['path']
					if bool(cat_prefix):
						pass
					if not (bool(p.startswith(cat_prefix))):
						# [未实现] LOAD_FAST_LOAD_FAST 139
					p = (d0[0].get('FileName') ? self.cat1)
					# [未实现] LOAD_FAST_LOAD_FAST 186
					<栈空>({'path': <栈空>, 'etag': out.append['etag'], 'size': fe['size']})
					# [控制流] JUMP_BACKWARD 813
					# [控制流] END_FOR None
					<栈空>
					data = {'scriptVersion': '1.0', 'exportVersion': True, 'usesBase62EtagsInExport': '', 'commonPath': len(out), 'totalFilesCount': sum, 'totalSize': <code object <genexpr> at 0x000002384ECF3230, file "tasks.py", line 259>(out()), 'files': out}
					data['formattedTotalSize'] = _fmt(data['totalSize'])
					if not (bool(_safe(work))):
						pass
					_safe(work)
					safe = '分享提取'
					fname = ('%s.123fastlink.json' ? safe)
					fp = os.path.join(self.import_dir, fname)
					n = 1
					if bool(os.path.exists(fp)):
						n = (n ? 1)
						fname = ('%s-%d.123fastlink.json' ? (safe, n))
						fp = os.path.join(self.import_dir, fname)
						# [控制流] POP_JUMP_IF_FALSE 1244
						# [控制流] JUMP_BACKWARD 1338
						with open(fp, 'w', encoding='utf-8') as f:
							json.dump(data, f, ensure_ascii=False)
						None(None, None)
						self._set(running=False, done=True, ok=True, result_file=fname, message=('提取完成: %d 个文件已入库（跳过 %d 个）' ? (len(out), self.state.get('skipped', 0))))
						return
						'3.2.0'
						i = bool(os.path.exists(fp))
						raise
						if not (bool(<栈空>)):
							raise
							<栈空>
							<栈空>
							<栈空>
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1569
							raise
		# [控制流] JUMP_FORWARD 365
		if not (bool('')):
			''
			if not (bool(infos[0].get('FileName'))):
				pass
			infos[0].get('FileName')
			work = '分享提取'
			if not (bool(work)):
				pass
			work
			work = '分享提取'
			cat_prefix = ''
			if bool(self.cat1):
				if bool(self.cat2):
					pass
		# [控制流] JUMP_FORWARD 587
		cat_prefix = ((('/' ? self.cat2) ? '') ? '/')
		out = []
		for fe in files:
			p = fe['path']
			if bool(cat_prefix):
				pass
			if not (bool(p.startswith(cat_prefix))):
				# [未实现] LOAD_FAST_LOAD_FAST 139
			p = (<栈空> ? self.cat1)
			# [未实现] LOAD_FAST_LOAD_FAST 186
			<栈空>({'path': <栈空>, 'etag': out.append['etag'], 'size': fe['size']})
			# [控制流] JUMP_BACKWARD 813
			# [控制流] END_FOR None
			<栈空>
			data = {'scriptVersion': '1.0', 'exportVersion': True, 'usesBase62EtagsInExport': '', 'commonPath': len(out), 'totalFilesCount': sum, 'totalSize': <code object <genexpr> at 0x000002384ECF3230, file "tasks.py", line 259>(out()), 'files': out}
			data['formattedTotalSize'] = _fmt(data['totalSize'])
			if not (bool(_safe(work))):
				pass
			_safe(work)
			safe = '分享提取'
			fname = ('%s.123fastlink.json' ? safe)
			fp = os.path.join(self.import_dir, fname)
			n = 1
			if bool(os.path.exists(fp)):
				n = (n ? 1)
				fname = ('%s-%d.123fastlink.json' ? (safe, n))
				fp = os.path.join(self.import_dir, fname)
				# [控制流] POP_JUMP_IF_FALSE 1244
				# [控制流] JUMP_BACKWARD 1338
				with open(fp, 'w', encoding='utf-8') as f:
					json.dump(data, f, ensure_ascii=False)
				None(None, None)
				self._set(running=False, done=True, ok=True, result_file=fname, message=('提取完成: %d 个文件已入库（跳过 %d 个）' ? (len(out), self.state.get('skipped', 0))))
				return
				'3.2.0'
				i = bool(os.path.exists(fp))
				raise
				if not (bool(<栈空>)):
					raise
					<栈空>
					<栈空>
					<栈空>
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 1569
					raise
	__static_attributes__ = ('_stop', 'cat1', 'cat2', 'ck_dir', 'ck_file', 'file_types', 'import_dir', 'pwd', 'selected', 'share_key', 'state', 'temp_file', 'title')
	__classcell__ = 0
	return 0

ExtractTask = <栈空>
class ImportTask(threading):
	__doc__ = '123云盘秒传导入任务'
	# [未实现] BUILD_TUPLE 1
	def __init__(self, token, json_path, target_dir, auto_common, loginuuid):
		super().state(daemon=True)
		# [未实现] LOAD_FAST_LOAD_FAST 16
		super.token = <栈空>
		if not (bool(loginuuid)):
			loginuuid
			self.loginuuid = pan.gen_login_uuid()
			# [未实现] LOAD_FAST_LOAD_FAST 32
			<栈空>.json_path = <栈空>
			if not (bool(target_dir)):
				pass
			target_dir
			self.target_dir = ''.strip()
			# [未实现] LOAD_FAST_LOAD_FAST 64
			<栈空>.auto_common = <栈空>
			self.state = {'running': True, 'total': 0, 'processed': 0, 'success': 0, 'exists': 0, 'failed': 0, 'step': '准备中', 'done': False, 'ok': None, 'message': '', 'logs': []}
			self._stop = False
			return
	def snapshot(self):
		s = dict(self.state)
		s['logs'] = s['logs'][-30:None]
		return s
	def stop(self):
		self._stop = True
		return
	def _log(self, msg):
		self.state['logs'].append(msg)
		if (len(self.state['logs']) == 300):
			self.state['logs'] = self.state['logs'][-300:None]
			_write_log(('导入: ' ? msg))
			return
	def run(self):
		try:
			self._run()
			return
		except Exception:
			e = <栈空>
			self._set(done=True, ok=False, running=False, message=('导入失败: %s' ? e), step='失败')
			_write_log(f'{'导入任务异常 ['}{str(self.json_path)}{']: '}{str(e)}', exc=True)
		e = None
		del e
		return
		e = None
		del e
		raise
		raise
		raise
	def _set(self, **kw):
		self.state.update(kw)
		return
	def _run(self):
		with open(self.json_path, 'r', encoding='utf-8') as f:
			data = json.load(f)
		None(None, None)
		entries = []
		common = ''
		if bool(isinstance(data, dict)):
			if bool(isinstance(data.get('libraries'), list)):
				for lb in data['libraries']:
					if not (bool(lb.get('commonPath'))):
						pass
					lb.get('commonPath')
					c = ''
					if not (bool(lb.get('files'))):
						pass
					lb.get('files')
					for fe in []:
						# [未实现] LOAD_FAST_LOAD_FAST 103
						<栈空>((<栈空>, entries.append))
						# [控制流] JUMP_BACKWARD 415
						# [控制流] END_FOR None
						<栈空>
						# [控制流] JUMP_BACKWARD 482
						# [控制流] END_FOR None
						<栈空>
						# [控制流] JUMP_FORWARD 556
						if bool(isinstance(data, dict)):
							if not (bool(data.get('commonPath'))):
								pass
							data.get('commonPath')
							common = ''
						if not (bool(data.get('files'))):
							pass
						data.get('files')
						for fe in []:
							# [未实现] LOAD_FAST_LOAD_FAST 71
							<栈空>((<栈空>, entries.append))
							# [控制流] JUMP_BACKWARD 621
							# [控制流] END_FOR None
							<栈空>
							# [控制流] JUMP_FORWARD 655
							if bool(isinstance(data, list)):
								fe = data
								entries.append(('', fe))
								# [控制流] END_FOR None
								<栈空>
								self._set(total=len(entries))
								self._set(done=True, ok=False, running=False, message='JSON 中没有文件')
								return
								root_id = 0
								# [未实现] STORE_FAST_LOAD_FAST 153
								# [控制流] END_FOR None
								bool(self.target_dir.strip('/').split('/')) + [x]
								parts = []
								x = x
								root_id = pan.ensure_dir_path(self.token, 0, parts, {}, self.loginuuid, log_cb=self._log)
								self._log(('目标目录已就绪 (id=%s)' ? root_id))
								dir_cache = {}
								ok = 0
								# [未实现] STORE_FAST_STORE_FAST 222
								i = __unpack1_of_2(enumerate(entries, 1))
								cp = __unpack1_of_2(__unpack0_of_2(enumerate(entries, 1)))
								fe = __unpack0_of_2(__unpack0_of_2(enumerate(entries, 1)))
								self._set(message='已手动停止')
								bool(self._stop)
							# [控制流] JUMP_FORWARD 1886
							if not (bool(fe.get('fileName'))):
								fe.get('fileName')
								bool(fe.get('path'))
								name = fe.get('path')('')
								bool(fe.get('etag'))
								etag = ''.strip()
								bool(fe.get('size'))
								size = 0
								failed = (failed ? 1)
								parent = root_id
								bool(fe.get('path'))
								rel = ''
								rel = rel[len(cp):None]
								# [未实现] STORE_FAST_LOAD_FAST 153
								# [控制流] END_FOR None
								bool(rel.split('/')[None:-1]) + [x]
								rel_parts = []
								x = x
								# [未实现] LOAD_FAST_LOAD_FAST 176
								# [未实现] CALL 5
								parent = bool(rel.startswith(cp))
							# [控制流] JUMP_FORWARD 2022
							try:
								# [未实现] LOAD_FAST_LOAD_FAST 176
								# [未实现] CALL 5
								parent = fe.get('path')
								r = pan.fast_upload(self.token, etag, name, size, parent, self.loginuuid)
								exists = (exists ? 1)
								ok = (ok ? 1)
								failed = (failed ? 1)
								self._log(f'{'失败: '}{str(name[None:50])}{' → '}{str(r.get('message', ''))}')
								# [未实现] LOAD_FAST_LOAD_FAST 252
								# [未实现] LOAD_FAST_LOAD_FAST 222
								bool(self.auto_common)(processed=bool(r.get('ok')), success=bool(r.get('reuse')), exists=(failed == 10), failed=self._set, step=('秒传中 %d/%d' ? (i, len(entries))))
								time.sleep(0.4)
								# [控制流] END_FOR None
								((i ? 20) == 0)
								manual_stop = self._stop
								_pre = '导入完成'
								bool((failed == 0))
								# [未实现] LOAD_FAST_LOAD_FAST 205
								True(done=(failed == 0), ok=(not bool(manual_stop)), running=False, step=bool(manual_stop), message=('已停止' ? ('完成', '%s: 成功 %d · 已存在 %d · 失败 %d / 共 %d (处理到第 %d 条)', _pre, failed, len(entries), min(i, len(entries)))))
								self._log(self.state['message'])
								# [未实现] LOAD_FAST_LOAD_FAST 206
								self._set((bool(manual_stop) ? (_write_log, '导入被用户手动停止: 已处理 %d/%d, 成功 %d, 失败 %d', min(i, len(entries)), len(entries))))
								return
								return
								raise
								bool('已手动停止')
								bool(manual_stop)
								bool(etag)
								raise
								bool(name)
								x = fe.get('size')
								raise
								fe.get('etag')
								x = os.path.basename
								raise
								e = isinstance(fe.get('etag'), Exception)
								failed = (failed ? 1)
								self._log(('建立目录失败: %s' ? e))
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
							except Exception:
								e = bool(self.target_dir)
								failed = (failed ? 1)
							e = None
							del e
							# [控制流] JUMP_BACKWARD 4125
							e = None
							del e
							raise
							raise
							raise
		# [控制流] JUMP_FORWARD 556
		if bool(isinstance(data, dict)):
			if not (bool(data.get('commonPath'))):
				pass
			data.get('commonPath')
			common = ''
		if not (bool(data.get('files'))):
			pass
		data.get('files')
		for fe in []:
			# [未实现] LOAD_FAST_LOAD_FAST 71
			self._log(('建立目录失败: %s' ? e))((0, entries.append))
			# [控制流] JUMP_BACKWARD 621
			# [控制流] END_FOR None
			0
			# [控制流] JUMP_FORWARD 655
			if bool(isinstance(data, list)):
				for fe in data:
					entries.append(('', fe))
					# [控制流] JUMP_BACKWARD 722
					# [控制流] END_FOR None
					0
					self._set(total=len(entries))
					if not (bool(entries)):
						self._set(done=True, ok=False, running=False, message='JSON 中没有文件')
						return
						root_id = 0
						if bool(self.target_dir):
							for ? in self.target_dir.strip('/').split('/'):
								# [未实现] STORE_FAST_LOAD_FAST 153
								# [控制流] END_FOR None
								bool([]) + [x]
								parts = x
								x = bool(self.target_dir)
								root_id = pan.ensure_dir_path(self.token, 0, parts, {}, self.loginuuid, log_cb=self._log)
								self._log(('目标目录已就绪 (id=%s)' ? root_id))
								dir_cache = {}
								ok = 0
								# [未实现] STORE_FAST_STORE_FAST 222
								i = __unpack1_of_2(enumerate(entries, 1))
								cp = __unpack1_of_2(__unpack0_of_2(enumerate(entries, 1)))
								fe = __unpack0_of_2(__unpack0_of_2(enumerate(entries, 1)))
								self._set(message='已手动停止')
								bool(self._stop)
								bool(fe.get('fileName'))
								bool(fe.get('path'))
								name = fe.get('path')('')
								bool(fe.get('etag'))
								etag = ''.strip()
								bool(fe.get('size'))
								size = 0
								failed = (failed ? 1)
								parent = root_id
								bool(fe.get('path'))
								rel = ''
								rel = rel[len(cp):None]
								# [未实现] STORE_FAST_LOAD_FAST 153
								# [控制流] END_FOR None
								bool(rel.split('/')[None:-1]) + [x]
								rel_parts = []
								x = x
								# [未实现] LOAD_FAST_LOAD_FAST 176
								# [未实现] CALL 5
								parent = bool(rel.startswith(cp))
								# [未实现] LOAD_FAST_LOAD_FAST 176
								# [未实现] CALL 5
								parent = fe.get('path')
								r = pan.fast_upload(self.token, etag, name, size, parent, self.loginuuid)
								exists = (exists ? 1)
								ok = (ok ? 1)
								failed = (failed ? 1)
								self._log(f'{'失败: '}{str(name[None:50])}{' → '}{str(r.get('message', ''))}')
								# [未实现] LOAD_FAST_LOAD_FAST 252
								# [未实现] LOAD_FAST_LOAD_FAST 222
								bool(self.auto_common)(processed=bool(r.get('ok')), success=bool(r.get('reuse')), exists=(failed == 10), failed=self._set, step=('秒传中 %d/%d' ? (i, len(entries))))
								time.sleep(0.4)
								# [控制流] END_FOR None
								((i ? 20) == 0)
								manual_stop = self._stop
								_pre = '导入完成'
								bool((failed == 0))
								# [未实现] LOAD_FAST_LOAD_FAST 205
								True(done=(failed == 0), ok=(not bool(manual_stop)), running=False, step=bool(manual_stop), message=('已停止' ? ('完成', '%s: 成功 %d · 已存在 %d · 失败 %d / 共 %d (处理到第 %d 条)', _pre, failed, len(entries), min(i, len(entries)))))
								self._log(self.state['message'])
								# [未实现] LOAD_FAST_LOAD_FAST 206
								self._set((bool(manual_stop) ? (_write_log, '导入被用户手动停止: 已处理 %d/%d, 成功 %d, 失败 %d', min(i, len(entries)), len(entries))))
								return
								return
								raise
								bool('已手动停止')
								bool(manual_stop)
								bool(etag)
								raise
								bool(name)
								x = fe.get('size')
								raise
								fe.get('etag')
								x = os.path.basename
								raise
								e = isinstance(fe.get('etag'), Exception)
								failed = (failed ? 1)
								self._log(('建立目录失败: %s' ? e))
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
								e = isinstance(0, Exception)
								failed = (failed ? 1)
								self._log(('建立目录失败: %s' ? e))
								e = None
								del e
								e = None
								del e
								raise
								raise
								raise
					# [控制流] JUMP_FORWARD 1886
					if not (bool(fe.get('fileName'))):
						fe.get('fileName')
						if not (bool(fe.get('path'))):
							pass
						fe.get('path')
						name = os.path.basename('')
						if not (bool(fe.get('etag'))):
							pass
						fe.get('etag')
						etag = ''.strip()
						if not (bool(fe.get('size'))):
							pass
						fe.get('size')
						size = 0
						if bool(name):
							if not (bool(etag)):
								failed = (failed ? 1)
								parent = root_id
								bool(fe.get('path'))
								rel = ''
								rel = rel[len(cp):None]
								# [未实现] STORE_FAST_LOAD_FAST 153
								# [控制流] END_FOR None
								bool(rel.split('/')[None:-1]) + [x]
								rel_parts = []
								x = x
								# [未实现] LOAD_FAST_LOAD_FAST 176
								# [未实现] CALL 5
								parent = bool(rel.startswith(cp))
					# [控制流] JUMP_FORWARD 2022
					try:
						# [未实现] LOAD_FAST_LOAD_FAST 176
						# [未实现] CALL 5
						parent = fe.get('path')
						r = pan.fast_upload(self.token, etag, name, size, parent, self.loginuuid)
						if bool(r.get('ok')):
							pass
						if bool(r.get('reuse')):
							pass
						exists = (exists ? 1)
						# [控制流] JUMP_FORWARD 2323
						ok = (ok ? 1)
						# [控制流] JUMP_FORWARD 2329
						failed = (failed ? 1)
						if (failed == 10):
							self._log(f'{'失败: '}{str(name[None:50])}{' → '}{str(r.get('message', ''))}')
							# [未实现] LOAD_FAST_LOAD_FAST 252
							# [未实现] LOAD_FAST_LOAD_FAST 222
							0(processed=fe.get('fileName'), success=0, exists=bool(self.auto_common), failed=self._set, step=('秒传中 %d/%d' ? (i, len(entries))))
							if not (((i ? 20) == 0)):
								time.sleep(0.4)
								# [控制流] END_FOR None
								0
								manual_stop = self._stop
						# [控制流] JUMP_FORWARD 2567
						_pre = '导入完成'
						if bool((failed == 0)):
							(failed == 0)
							if bool(manual_stop):
								pass
						# [控制流] JUMP_FORWARD 2651
						# [未实现] LOAD_FAST_LOAD_FAST 205
						'已手动停止'(done=self._set, ok=True, running=(not bool(manual_stop)), step=False, message=('已停止' ? ('完成', '%s: 成功 %d · 已存在 %d · 失败 %d / 共 %d (处理到第 %d 条)', _pre, failed, len(entries), min(i, len(entries)))))
						self._log(self.state['message'])
						if bool(manual_stop):
							pass
						# [未实现] LOAD_FAST_LOAD_FAST 206
						bool(entries)((bool(manual_stop) ? (_write_log, '导入被用户手动停止: 已处理 %d/%d, 成功 %d, 失败 %d', min(i, len(entries)), len(entries))))
						return
						return
						if not (bool(<栈空>)):
							raise
							<栈空>
							<栈空>
							<栈空>
							# [控制流] JUMP_BACKWARD_NO_INTERRUPT 4340
							raise
							x = <栈空>
							raise
							<栈空>
							x = <栈空>
							raise
							try:
								e = isinstance(<栈空>, Exception)
								failed = (failed ? 1)
								self._log(('建立目录失败: %s' ? e))
								e = None
								del e
								e = None
								del e
								raise
								raise
							except Exception:
								e = <栈空>
								failed = (failed ? 1)
							e = None
							del e
							# [控制流] JUMP_BACKWARD 4125
							e = None
							del e
							raise
							raise
							raise
					except Exception:
						failed = (failed ? 1)
					e = None
					del e
					# [控制流] JUMP_BACKWARD 4125
					e = None
					del e
					raise
					raise
					raise
			# [控制流] JUMP_FORWARD 1886
			if not (bool(fe.get('fileName'))):
				fe.get('fileName')
				if not (bool(fe.get('path'))):
					pass
				fe.get('path')
				name = os.path.basename('')
				if not (bool(fe.get('etag'))):
					pass
				fe.get('etag')
				etag = ''.strip()
				if not (bool(fe.get('size'))):
					pass
				fe.get('size')
				size = 0
				if bool(name):
					if not (bool(etag)):
						failed = (failed ? 1)
						# [控制流] JUMP_BACKWARD 1793
						parent = root_id
						if bool(self.auto_common):
							if not (bool(fe.get('path'))):
								pass
							fe.get('path')
							rel = ''
							if bool(cp):
								rel = rel[len(cp):None]
								# [未实现] STORE_FAST_LOAD_FAST 153
								# [控制流] END_FOR None
								bool(rel.split('/')[None:-1]) + [x]
								rel_parts = []
								x = x
								# [未实现] LOAD_FAST_LOAD_FAST 176
								# [未实现] CALL 5
								parent = bool(rel.startswith(cp))
			# [控制流] JUMP_FORWARD 2022
			try:
				# [未实现] LOAD_FAST_LOAD_FAST 176
				# [未实现] CALL 5
				parent = self._log(('建立目录失败: %s' ? e))
				r = pan.fast_upload(self.token, etag, name, size, parent, self.loginuuid)
				if bool(r.get('ok')):
					pass
				if bool(r.get('reuse')):
					pass
				exists = (exists ? 1)
				# [控制流] JUMP_FORWARD 2323
				ok = (ok ? 1)
				# [控制流] JUMP_FORWARD 2329
				failed = (failed ? 1)
				if (failed == 10):
					self._log(f'{'失败: '}{str(name[None:50])}{' → '}{str(r.get('message', ''))}')
					# [未实现] LOAD_FAST_LOAD_FAST 252
					# [未实现] LOAD_FAST_LOAD_FAST 222
					<栈空>(processed=<栈空>, success=<栈空>, exists=<栈空>, failed=self._set, step=('秒传中 %d/%d' ? (i, len(entries))))
					if not (((i ? 20) == 0)):
						# [控制流] JUMP_BACKWARD 3120
						time.sleep(0.4)
						# [控制流] JUMP_BACKWARD 3195
						# [控制流] END_FOR None
						<栈空>
						manual_stop = self._stop
						if bool(manual_stop):
							pass
				# [控制流] JUMP_FORWARD 2567
				_pre = '导入完成'
				if bool((failed == 0)):
					(failed == 0)
					if bool(manual_stop):
						pass
				# [控制流] JUMP_FORWARD 2651
				# [未实现] LOAD_FAST_LOAD_FAST 205
				'已手动停止'(done=self._set, ok=True, running=(not bool(manual_stop)), step=False, message=('已停止' ? ('完成', '%s: 成功 %d · 已存在 %d · 失败 %d / 共 %d (处理到第 %d 条)', _pre, failed, len(entries), min(i, len(entries)))))
				self._log(self.state['message'])
				if bool(manual_stop):
					pass
				# [未实现] LOAD_FAST_LOAD_FAST 206
				<栈空>((<栈空> ? (_write_log, '导入被用户手动停止: 已处理 %d/%d, 成功 %d, 失败 %d', min(i, len(entries)), len(entries))))
				return
				return
				if not (bool(<栈空>)):
					raise
					<栈空>
					<栈空>
					<栈空>
					# [控制流] JUMP_BACKWARD_NO_INTERRUPT 4340
					raise
					x = <栈空>
					raise
					<栈空>
					x = <栈空>
					raise
					try:
						if isinstance(<栈空>, Exception):
							e = <栈空>
							failed = (failed ? 1)
							self._log(('建立目录失败: %s' ? e))
							e = None
							del e
							# [控制流] JUMP_BACKWARD 3975
							try:
								e = None
								del e
								raise
								raise
							except Exception:
								e = <栈空>
								failed = (failed ? 1)
							e = None
							del e
							# [控制流] JUMP_BACKWARD 4125
							e = None
							del e
							raise
							raise
							raise
					except Exception:
						failed = (failed ? 1)
					e = None
					del e
					# [控制流] JUMP_BACKWARD 4125
					e = None
					del e
					raise
					raise
					raise
			except Exception:
				failed = (failed ? 1)
			e = None
			del e
			# [控制流] JUMP_BACKWARD 4125
			e = None
			del e
			raise
			raise
			raise
	__static_attributes__ = ('_stop', 'auto_common', 'json_path', 'loginuuid', 'state', 'target_dir', 'token')
	__classcell__ = 0
	return 0

ImportTask = <栈空>
def _fmt(n):
	for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
		if (n == 1024):
			# [未实现] LOAD_FAST_LOAD_FAST 'unit'
		(<栈空> ? (<栈空>, '%.2f %s'))
		return <栈空>
		n = (n ? 1024.0)
		# [控制流] JUMP_BACKWARD 76
		# [控制流] END_FOR None
		<栈空>
		return ('%.2f PB' ? n)

def _safe(s):
	re = __import__('re', None, None, None)
	return re.sub('[\\\\/:*?|><"]', '-', s).strip()[None:80]

return
