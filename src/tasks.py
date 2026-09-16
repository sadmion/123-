# -*- coding: utf-8 -*-
"""后台任务：分享链接提取（断点续传）+ 123云盘秒传导入"""
import json
import os
import threading
import time
import traceback

import pan123_api as pan

_log_sink = None


def set_log_sink(fn):
    global _log_sink
    _log_sink = fn


def _write_log(msg, exc=None):
    if _log_sink:
        try:
            _log_sink(msg, exc=exc)
        except Exception:
            pass


class TaskState(object):
    """全局任务状态（同一时间各一个提取/导入任务）"""

    def __init__(self):
        self.lock = threading.Lock()
        self.extract = None
        self.import_ = None

    def snapshot_extract(self):
        with self.lock:
            return self.extract.snapshot() if self.extract else {'running': False}

    def snapshot_import(self):
        with self.lock:
            return self.import_.snapshot() if self.import_ else {'running': False}


TASKS = TaskState()


class ExtractTask(threading.Thread):
    """分享链接提取入库（支持断点续传/文件类型过滤/浏览选择性提取）"""

    def __init__(self, share_key, pwd, import_dir, title=None, cat1=None,
                 cat2=None, file_types=None, selected=None, tag_suffix=None):
        super().__init__(daemon=True)
        self.share_key = share_key
        self.pwd = pwd
        self.import_dir = import_dir
        self.title = (title or '').strip()
        self.cat1 = (cat1 or '').strip()
        self.cat2 = (cat2 or '').strip()
        self.file_types = file_types
        self.selected = selected
        self.ck_dir = os.path.join(import_dir, '_checkpoints')
        self.ck_file = os.path.join(self.ck_dir, 'extract_%s.json' % share_key)
        self.temp_file = self.ck_file + '.temp'
        self.state = {
            'running': True,
            'step': '准备中',
            'scanned': 0,
            'skipped': 0,
            'found': 0,
            'done': False,
            'ok': False,
            'message': '',
            'result_file': '',
            'checkpoint': False,
        }
        self._stop = False

    def snapshot(self):
        return dict(self.state)

    def stop(self):
        self._stop = True

    def _set(self, **kw):
        self.state.update(kw)

    def _save_checkpoint(self, files, scanned, skipped, done_dirs):
        if self._stop:
            return
        os.makedirs(self.ck_dir, exist_ok=True)
        try:
            with open(self.temp_file, 'w', encoding='utf-8') as f:
                for fe in files:
                    f.write(json.dumps(fe, ensure_ascii=False) + '\n')
        except OSError:
            return
        ck = {
            'shareKey': self.share_key,
            'total_files': len(files),
            'scanned': scanned,
            'skipped': skipped,
            'done_dirs': done_dirs[:5000],
            'file_filters': sorted(self.file_types) if self.file_types else None,
            'ts': time.time(),
        }
        try:
            with open(self.ck_file, 'w', encoding='utf-8') as f:
                json.dump(ck, f, ensure_ascii=False)
        except OSError:
            pass

    @staticmethod
    def load_checkpoint(ck_dir, share_key):
        """读取未完成检查点, 返回 dict 或 None（损坏自动删除）"""
        ck_file = os.path.join(ck_dir, 'extract_%s.json' % share_key)
        if not os.path.exists(ck_file):
            return None
        try:
            with open(ck_file, 'r', encoding='utf-8') as f:
                ck = json.load(f)
            temp = ck_file + '.temp'
            n = 0
            if os.path.exists(temp):
                try:
                    with open(temp, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                n += 1
                except OSError:
                    n = -1
            if n != ck.get('total_files', -1):
                os.remove(ck_file)
                return None
            ck['ck_file'] = ck_file
            ck['temp_file'] = temp
            return ck
        except Exception:
            try:
                os.remove(ck_file)
            except OSError:
                pass
            return None

    @staticmethod
    def delete_checkpoint(ck_dir, share_key):
        ck_file = os.path.join(ck_dir, 'extract_%s.json' % share_key)
        for p in (ck_file, ck_file + '.temp'):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass

    def run(self):
        try:
            self._run()
        except Exception as e:
            self._set(running=False, done=True, ok=False,
                      message='提取失败: %s' % e, step='失败')
            _write_log('提取任务异常 [%s]: %s' % (self.share_key, e), exc=True)
            traceback.print_exc()

    def _run(self):
        resume_files = []
        resume_done = []
        ck = None
        if self.selected is None:
            ck = ExtractTask.load_checkpoint(self.ck_dir, self.share_key)
            if ck:
                old_filters = (set(ck.get('file_filters'))
                               if ck.get('file_filters') else None)
                new_filters = set(self.file_types) if self.file_types else None
                if old_filters != new_filters:
                    ExtractTask.delete_checkpoint(self.ck_dir, self.share_key)
                    ck = None
                else:
                    try:
                        with open(ck['temp_file'], 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.strip():
                                    resume_files.append(json.loads(line))
                    except (OSError, ValueError):
                        resume_files = []
                    resume_done = ck.get('done_dirs') or []
                    self._set(checkpoint=True,
                              message='检测到未完成的提取, 续传已扫描 %d 个文件'
                                      % len(resume_files))

        if self.selected is not None:
            self._set(step='提取选中项')
            files = []
            for it in self.selected:
                if it.get('isDir'):
                    sub, _sc, _sk = pan.share_walk(
                        self.share_key, self.pwd, self.file_types,
                        progress_cb=lambda *a: None,
                        resume_offset={'done_dirs': set()})
                    prefix = it.get('path') or it.get('name')
                    for fe in sub:
                        if fe['path'].startswith(prefix + '/'):
                            fe2 = dict(fe)
                            fe2['path'] = fe['path']
                            files.append(fe2)
                else:
                    files.append({
                        'path': it.get('path') or it.get('name'),
                        'etag': it.get('etag') or '',
                        'size': it.get('size') or 0,
                    })
            files = [f for f in files if f.get('etag')]
            self._set(found=len(files))
            self._save_result(files)
            return

        self._set(step='扫描分享目录')
        progress = [time.time()]

        def cb(scanned, skipped, cur):
            if self._stop:
                raise RuntimeError('已取消')
            if time.time() - progress[0] >= 0.5:
                progress[0] = time.time()
                self._set(scanned=scanned, skipped=skipped,
                          step='扫描: %s' % ((cur or '')[:40]))

        offset = {'done_dirs': set(resume_done), 'scanned': len(resume_files)}
        files, scanned, skipped = pan.share_walk(
            self.share_key, self.pwd, self.file_types, cb,
            checkpoint_cb=lambda files, scanned, skipped, done_dirs:
                self._save_checkpoint(files, scanned, skipped, done_dirs),
            resume_files=resume_files, resume_offset=offset)
        self._set(scanned=scanned, skipped=skipped, found=len(files),
                  step='生成入库文件')
        ExtractTask.delete_checkpoint(self.ck_dir, self.share_key)
        self._save_result(files)

    def _save_result(self, files):
        if not files:
            self._set(running=False, done=True, ok=False,
                      message='没有提取到任何文件（可能没有可秒传的 ETag）')
            return
        if self.title:
            work = self.title
        else:
            infos, _t, _m = pan.share_list_page(self.share_key, self.pwd, 0, 1, 10)
            work = ''
            if infos:
                d0 = [i for i in infos if i.get('Type') == 1]
                work = (d0[0].get('FileName') if d0 else '')
                if not work:
                    work = infos[0].get('FileName') or '分享提取'
            if not work:
                work = '分享提取'

        cat_prefix = ''
        if self.cat1:
            cat_prefix = self.cat1 + ('/' + self.cat2 if self.cat2 else '') + '/'

        out = []
        for fe in files:
            p = fe['path']
            if cat_prefix:
                if not p.startswith(cat_prefix):
                    p = cat_prefix + p
            out.append({'path': p, 'etag': fe['etag'], 'size': fe['size']})

        data = {
            'scriptVersion': '3.2.0',
            'exportVersion': '1.0',
            'usesBase62EtagsInExport': True,
            'commonPath': '',
            'totalFilesCount': len(out),
            'totalSize': sum(f['size'] for f in out),
            'files': out,
        }
        data['formattedTotalSize'] = _fmt(data['totalSize'])

        safe = _safe(work) or '分享提取'
        fname = '%s.123fastlink.json' % safe
        fp = os.path.join(self.import_dir, fname)
        n = 1
        while os.path.exists(fp):
            n += 1
            fname = '%s-%d.123fastlink.json' % (safe, n)
            fp = os.path.join(self.import_dir, fname)
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        self._set(running=False, done=True, ok=True, result_file=fname,
                  message='提取完成: %d 个文件已入库（跳过 %d 个）'
                          % (len(out), self.state.get('skipped', 0)))


class ImportTask(threading.Thread):
    """123云盘秒传导入任务"""

    def __init__(self, token, json_path, target_dir=None, auto_common=True,
                 loginuuid=None):
        super().__init__(daemon=True)
        self.token = token
        self.loginuuid = loginuuid if loginuuid else pan.gen_login_uuid()
        self.json_path = json_path
        self.target_dir = (target_dir or '').strip()
        self.auto_common = auto_common
        self.state = {
            'running': True,
            'total': 0,
            'processed': 0,
            'success': 0,
            'exists': 0,
            'failed': 0,
            'step': '准备中',
            'done': False,
            'ok': False,
            'message': '',
            'logs': [],
        }
        self._stop = False

    def snapshot(self):
        s = dict(self.state)
        s['logs'] = self.state['logs'][-30:]
        return s

    def stop(self):
        self._stop = True

    def _log(self, msg):
        self.state['logs'].append(msg)
        if len(self.state['logs']) > 300:
            del self.state['logs'][:-300]
        _write_log('导入: ' + msg)

    def run(self):
        try:
            self._run()
        except Exception as e:
            self._set(done=True, ok=False, running=False,
                      message='导入失败: %s' % e, step='失败')
            _write_log('导入任务异常 [%s]: %s' % (self.json_path, e), exc=True)
            traceback.print_exc()

    def _set(self, **kw):
        self.state.update(kw)

    def _run(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        entries = []
        common = ''
        if isinstance(data, dict):
            if isinstance(data.get('libraries'), list):
                for lb in data['libraries']:
                    c = lb.get('commonPath') or ''
                    for fe in lb.get('files') or []:
                        entries.append((c, fe))
            elif isinstance(data, dict):
                common = data.get('commonPath') or ''
                for fe in data.get('files') or []:
                    entries.append((common, fe))
        elif isinstance(data, list):
            for fe in data:
                entries.append(('', fe))
        self._set(total=len(entries))
        if not entries:
            self._set(done=True, ok=False, running=False,
                      message='JSON 中没有文件')
            return

        root_id = 0
        if self.target_dir:
            parts = [x for x in self.target_dir.strip('/').split('/') if x]
            root_id = pan.ensure_dir_path(self.token, 0, parts, {},
                                          self.loginuuid,
                                          log_cb=self._log)
            self._log('目标目录已就绪 (id=%s)' % root_id)

        dir_cache = {}
        ok = exists = failed = 0
        i = 0
        for i, (cp, fe) in enumerate(entries, 1):
            if self._stop:
                self._set(message='已手动停止')
                break
            name = fe.get('fileName') or os.path.basename(fe.get('path') or '')
            etag = (fe.get('etag') or '').strip()
            size = fe.get('size') or 0
            if name:
                if not etag:
                    failed += 1
                    continue
            else:
                failed += 1
                continue
            parent = root_id
            if self.auto_common:
                rel = fe.get('path') or ''
                if cp and rel.startswith(cp):
                    rel = rel[len(cp):]
                rel_parts = [x for x in rel.split('/')[:-1] if x]
                try:
                    if self.target_dir:
                        parent = pan.ensure_dir_path(
                            self.token, root_id, rel_parts, dir_cache,
                            self.loginuuid)
                    else:
                        parent = pan.ensure_dir_path(
                            self.token, 0, rel_parts, dir_cache,
                            self.loginuuid)
                except Exception as e:
                    failed += 1
                    self._log('建立目录失败: %s' % e)
                    continue
            r = pan.fast_upload(self.token, etag, name, size, parent,
                                self.loginuuid)
            if r.get('ok'):
                if r.get('reuse'):
                    exists += 1
                else:
                    ok += 1
            else:
                failed += 1
                if failed <= 10:
                    self._log(f'失败: {name[:50]} → {r.get("message", "")}')
            self._set(processed=i, success=ok, exists=exists, failed=failed,
                      step='秒传中 %d/%d' % (i, len(entries)))
            if i % 20 == 0:
                time.sleep(0.4)

        manual_stop = self._stop
        _pre = '已手动停止' if manual_stop else '导入完成'
        self._set(done=True, ok=(failed == 0 and not manual_stop),
                  running=False,
                  step='已停止' if manual_stop else '完成',
                  message=('%s: 成功 %d · 已存在 %d · 失败 %d / 共 %d '
                           '(处理到第 %d 条)')
                          % (_pre, ok, exists, failed, len(entries),
                             min(i, len(entries))))
        self._log(self.state['message'])
        if manual_stop:
            _write_log('导入被用户手动停止: 已处理 %d/%d, 成功 %d, 失败 %d'
                       % (min(i, len(entries)), len(entries), ok, failed))


def _fmt(n):
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024:
            return '%.2f %s' % (n, unit)
        n = n / 1024.0
    return '%.2f PB' % n


def _safe(s):
    import re
    return re.sub(r'[\\/:*?|><"]', '-', s).strip()[:80]
