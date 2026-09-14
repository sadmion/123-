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
	if not (bool(_log_sink)):
		try:
			# [未实现] LOAD_FAST_LOAD_FAST 'exc'
			<栈空>(<栈空>, exc=_log_sink)
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

class TaskState(object):
	__doc__ = '全局任务状态（同一时间各一个提取/导入任务）'
	# [控制流] MAKE_FUNCTION None
	__init__ = <code object __init__ at 0x00000282E52485D0, file "tasks.py", line 30>
	# [控制流] MAKE_FUNCTION None
	snapshot_extract = <code object snapshot_extract at 0x00000282E5166A30, file "tasks.py", line 35>
	# [控制流] MAKE_FUNCTION None
	snapshot_import = <code object snapshot_import at 0x00000282E5166BB0, file "tasks.py", line 39>
	__static_attributes__ = ('extract', 'import_', 'lock')
	return

TaskState = (False,)
TASKS = TaskState()
class ExtractTask(threading):
	# [控制流] MAKE_CELL '__class__'
	__doc__ = '分享链接提取入库（支持断点续传/文件类型过滤/浏览选择性提取）'
	# [未实现] BUILD_TUPLE 1
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 8
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	__init__ = <code object __init__ at 0x00000282E499AEC0, file "tasks.py", line 50>
	# [控制流] MAKE_FUNCTION None
	snapshot = <code object snapshot at 0x00000282E5289E30, file "tasks.py", line 70>
	# [控制流] MAKE_FUNCTION None
	stop = <code object stop at 0x00000282E5237130, file "tasks.py", line 73>
	# [控制流] MAKE_FUNCTION None
	_set = <code object _set at 0x00000282E5286230, file "tasks.py", line 76>
	# [控制流] MAKE_FUNCTION None
	_save_checkpoint = <code object _save_checkpoint at 0x00000282E4E309A0, file "tasks.py", line 80>
	# [控制流] MAKE_FUNCTION None
	load_checkpoint = <code object load_checkpoint at 0x00000282E49C9B70, file "tasks.py", line 98>()
	# [控制流] MAKE_FUNCTION None
	delete_checkpoint = <code object delete_checkpoint at 0x00000282E4C53690, file "tasks.py", line 134>()
	# [控制流] MAKE_FUNCTION None
	run = <code object run at 0x00000282E4C2F120, file "tasks.py", line 145>
	# [控制流] MAKE_FUNCTION None
	_run = <code object _run at 0x00000282E4D95E80, file "tasks.py", line 154>
	# [控制流] MAKE_FUNCTION None
	_save_result = <code object _save_result at 0x00000282E4DEA250, file "tasks.py", line 228>
	__static_attributes__ = ('_stop', 'cat1', 'cat2', 'ck_dir', 'ck_file', 'file_types', 'import_dir', 'pwd', 'selected', 'share_key', 'state', 'temp_file', 'title')
	__classcell__ = 0
	return 0

ExtractTask = <栈空>
class ImportTask(threading):
	# [控制流] MAKE_CELL '__class__'
	__doc__ = '123云盘秒传导入任务'
	# [未实现] BUILD_TUPLE 1
	# [控制流] MAKE_FUNCTION None
	# [控制流] SET_FUNCTION_ATTRIBUTE 8
	# [控制流] SET_FUNCTION_ATTRIBUTE 1
	__init__ = <code object __init__ at 0x00000282E52F0030, file "tasks.py", line 281>
	# [控制流] MAKE_FUNCTION None
	snapshot = <code object snapshot at 0x00000282E5286670, file "tasks.py", line 293>
	# [控制流] MAKE_FUNCTION None
	stop = <code object stop at 0x00000282E5236A30, file "tasks.py", line 298>
	# [控制流] MAKE_FUNCTION None
	_log = <code object _log at 0x00000282E52B0030, file "tasks.py", line 301>
	# [控制流] MAKE_FUNCTION None
	run = <code object run at 0x00000282E4C2F2D0, file "tasks.py", line 307>
	# [控制流] MAKE_FUNCTION None
	_set = <code object _set at 0x00000282E5286890, file "tasks.py", line 316>
	# [控制流] MAKE_FUNCTION None
	_run = <code object _run at 0x00000282E4DD2110, file "tasks.py", line 319>
	__static_attributes__ = ('_stop', 'auto_common', 'json_path', 'loginuuid', 'state', 'target_dir', 'token')
	__classcell__ = 0
	return 0

ImportTask = <栈空>
def _fmt(n):
	for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
		if not ((n == 1024)):
			# [未实现] LOAD_FAST_LOAD_FAST 'unit'
		(<栈空> ? (<栈空>, '%.2f %s'))
		return <栈空>
		n = (n ? 1024.0)
	return ('%.2f PB' ? n)

def _safe(s):
	re = __import__('re', None, None, None)
	# [未实现] BINARY_SLICE None
	return 80

return
