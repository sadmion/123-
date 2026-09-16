# -*- coding: utf-8 -*-
"""HTTP 服务 + API 路由 + 数据目录管理 + 程序入口"""
import base64
import json
import logging
import mimetypes
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pan123_api as pan
import tasks as _tasks
from tasks import TASKS, ExtractTask, ImportTask
from library_store import LibraryStore

APP_NAME = '123云盘影库搜索工具'
APP_VERSION = 'V1.0.3'
TMDB_KEY_DEFAULT = '3fd2be6f0c70a2a598f084ddfb75487c'
TMDB_IMG = 'https://image.tmdb.org/t/p/w342'

gen_login_uuid = pan.gen_login_uuid
AUTH = {'token': '', 'nickname': '', 'uid': 0, 'loginuuid': gen_login_uuid()}
TMDB_KEY = {'key': TMDB_KEY_DEFAULT}
HISTORY = []
HISTORY_MAX = 30
STORE = None
DATA_ROOT = ''
HTTP_PORT = 5890


def _get_base_dir():
    if getattr(sys, '_MEIPASS', None):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = _get_base_dir()
LOGGER = logging.getLogger(APP_NAME)


def appdata_dir():
    base = os.environ.get('APPDATA') or os.path.expanduser('~')
    d = os.path.join(base, APP_NAME)
    os.makedirs(d, exist_ok=True)
    return d


CONFIG_PATH = os.path.join(appdata_dir(), 'data_config.json')


def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(cfg):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


BGM_EXTS = ('.mp3', '.flac', '.ogg', '.m4a', '.aac', '.wav')
BGM_MIME = {
    '.mp3': 'audio/mpeg',
    '.flac': 'audio/flac',
    '.ogg': 'audio/ogg',
    '.m4a': 'audio/mp4',
    '.aac': 'audio/aac',
    '.wav': 'audio/wav',
}


def find_external_bgm():
    """实时扫描外部 BGM 文件, 找到返回 (绝对路径, MIME), 没有返回 None"""
    exe_dir = (os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)
               else os.path.dirname(os.path.abspath(__file__)))
    bases = [exe_dir]
    if DATA_ROOT:
        bases.append(DATA_ROOT)
    for base in bases:
        if not base:
            continue
        try:
            if not os.path.isdir(base):
                continue
            for fn in sorted(os.listdir(base)):
                stem, ext = os.path.splitext(fn)
                if stem.lower() != 'bgm':
                    continue
                if ext.lower() not in BGM_EXTS:
                    continue
                return (os.path.join(base, fn), BGM_MIME[ext.lower()])
        except OSError:
            continue
    return None


def ensure_data_dirs(root):
    os.makedirs(os.path.join(root, '秒传文件导入或追加'), exist_ok=True)
    os.makedirs(os.path.join(root, '秒传文件导出'), exist_ok=True)
    bak = os.path.join(root, '记录数据存放目录【勿动】')
    os.makedirs(bak, exist_ok=True)
    try:
        shutil.copyfile(CONFIG_PATH, os.path.join(bak, 'data_config.json'))
    except OSError:
        pass


def select_dir_dialog(title):
    """弹目录选择对话框（tkinter）"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askdirectory(
            title=title, initialdir=os.path.expanduser('~'))
        root.destroy()
        return path or ''
    except Exception:
        return ''


def init_data_root():
    global DATA_ROOT, STORE
    cfg = load_config()
    args = sys.argv[1:]
    root = ''
    if any(a == '--select' for a in args):
        pass
    else:
        for a in args:
            if a.startswith('--dir='):
                root = a[6:].strip('"')
                break
    if not root:
        root = cfg.get('data_root') or ''
    if root:
        if not os.path.isdir(root):
            root = ''
    if not root:
        root = select_dir_dialog('选择数据存放目录（将自动创建子目录）')
        if not root:
            print('未选择数据目录, 退出')
            sys.exit(0)
    # 从 exe 同目录搬移影库 json（首次运行时）
    exe_dir = (os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)
               else os.path.dirname(os.path.abspath(__file__)))
    if os.path.isdir(exe_dir):
        for n in os.listdir(exe_dir):
            if n.lower().endswith('.json'):
                try:
                    shutil.copyfile(os.path.join(exe_dir, n),
                                    os.path.join(root, n))
                except OSError:
                    pass
    root = os.path.abspath(root)
    ensure_data_dirs(root)
    cfg['data_root'] = root
    save_config(cfg)
    DATA_ROOT = root
    setup_logging()
    _tasks.set_log_sink(app_log)
    STORE = LibraryStore(os.path.join(root, '秒传文件导入或追加'))
    threading.Thread(target=STORE.watcher_loop, daemon=True).start()
    load_history()
    load_auth()


def setup_logging():
    """日志写入 数据目录/logs/server.log, noconsole 打包下也能留痕"""
    global LOGGER
    d = os.path.join(DATA_ROOT, 'logs')
    os.makedirs(d, exist_ok=True)
    lg = logging.getLogger('app')
    lg.setLevel(logging.INFO)
    if not lg.handlers:
        fh = logging.FileHandler(os.path.join(d, 'server.log'),
                                 encoding='utf-8')
        fh.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s'))
        lg.addHandler(fh)
    try:
        LOGGER = lg
    except Exception:
        LOGGER = None


def app_log(msg, exc=False):
    try:
        if LOGGER:
            if exc:
                LOGGER.error(msg, exc_info=exc)
            else:
                LOGGER.info(msg)
    except Exception:
        pass


def load_history():
    try:
        with open(os.path.join(DATA_ROOT, '.history.json'), 'r',
                  encoding='utf-8') as f:
            data = json.load(f)
        HISTORY[:] = data[:HISTORY_MAX]
    except Exception:
        pass


def save_history():
    try:
        with open(os.path.join(DATA_ROOT, '.history.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(HISTORY[:HISTORY_MAX], f, ensure_ascii=False)
    except OSError:
        pass


def _auth_file():
    return os.path.join(DATA_ROOT, '.login.json')


def save_auth():
    """登录成功后持久化, 重启免登录"""
    if AUTH['token']:
        try:
            with open(_auth_file(), 'w', encoding='utf-8') as f:
                json.dump({'token': AUTH['token'],
                           'nickname': AUTH['nickname'],
                           'uid': AUTH['uid']}, f, ensure_ascii=False)
        except OSError:
            pass
    else:
        try:
            os.remove(_auth_file())
        except OSError:
            pass


def load_auth():
    """启动时恢复登录, 后台校验 token 有效性"""
    try:
        with open(_auth_file(), 'r', encoding='utf-8') as f:
            d = json.load(f)
        t = d.get('token') or ''
        if not t:
            return
        AUTH['token'] = t
        AUTH['nickname'] = d.get('nickname', '')
        AUTH['uid'] = d.get('uid', 0)

        def _verify():
            try:
                info = pan.user_info_from_token(t)
                if info.get('ok') is not False:
                    if not info:
                        raise ValueError('token 失效')
                    app_log('已恢复登录: %s' % AUTH['nickname'])
            except Exception:
                AUTH['token'] = ''
                AUTH['nickname'] = ''
                AUTH['uid'] = 0
                save_auth()
                app_log('已保存的登录已失效, 已清除')

        threading.Thread(target=_verify, daemon=True).start()
    except Exception:
        pass


def tmdb_search(title, year):
    key = TMDB_KEY['key']
    best = None
    import urllib.request
    import urllib.parse
    for mtype in ('movie', 'tv'):
        q = {'api_key': key, 'query': title, 'language': 'zh-CN'}
        if year:
            q['year' if mtype == 'movie' else 'first_air_date_year'] = year
        url = ('https://api.themoviedb.org/3/search/%s?%s'
               % (mtype, urllib.parse.urlencode(q)))
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=4) as r:
                data = json.loads(r.read().decode('utf-8'))
        except Exception:
            continue
        for res in (data.get('results') or []):
            score = 0
            name = res.get('title') or res.get('name') or ''
            if title.lower() in name.lower() or name.lower() in title.lower():
                score += 2
            y = (res.get('release_date') or res.get('first_air_date') or '')[:4]
            if year and y == year:
                score += 1
            if score < 2:
                continue
            cand = {
                'score': score + (res.get('popularity') or 0) / 1000.0,
                'poster': (TMDB_IMG + res['poster_path']
                           if res.get('poster_path') else ''),
                'title': name,
                'year': y,
                'type': mtype,
            }
            if best is None or cand['score'] > best['score']:
                best = cand
    return best


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    server_version = 'LibraryServer/' + APP_VERSION

    def log_message(self, fmt, *args):
        return

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            return

    def _body(self):
        try:
            n = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            n = 0
        if n <= 0:
            return {}
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode('utf-8'))
        except Exception:
            return {}

    def _static(self, rel, mime=None):
        fp = os.path.join(BASE_DIR, rel)
        if not os.path.isfile(fp):
            self._json({'error': 'not found'}, 404)
            return
        try:
            with open(fp, 'rb') as f:
                body = f.read()
        except OSError:
            self._json({'error': 'not found'}, 404)
            return
        if not mime:
            mime = mimetypes.guess_type(fp)[0] or 'application/octet-stream'
        try:
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            return

    def _static_abs(self, fp, mime=None):
        if not os.path.isfile(fp):
            self._json({'error': 'not found'}, 404)
            return
        try:
            with open(fp, 'rb') as f:
                body = f.read()
        except OSError:
            self._json({'error': 'not found'}, 404)
            return
        if not mime:
            mime = mimetypes.guess_type(fp)[0] or 'application/octet-stream'
        try:
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            return

    def _qs(self):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query)
        return {k: v[0] for k, v in q.items()}

    def _libs_param(self, q):
        v = q.get('libs') or ''
        if not v:
            return None
        try:
            return [int(x) for x in v.split(',') if x.strip().isdigit()]
        except ValueError:
            return None

    def do_GET(self):
        try:
            self._route_get()
        except (BrokenPipeError, ConnectionResetError):
            return
        except Exception as e:
            _safe_traceback()
            app_log(f'GET {self.path} 异常: {e}', exc=True)
            self._json({'error': str(e)}, 500)

    def do_POST(self):
        try:
            self._route_post()
        except (BrokenPipeError, ConnectionResetError):
            return
        except Exception as e:
            _safe_traceback()
            app_log(f'POST {self.path} 异常: {e}', exc=True)
            self._json({'error': str(e)}, 500)


    def _route_get(self):
        q = self._qs()
        path = self.path.split('?')[0]

        # ---- 静态资源 ----
        if path in ('/', '/index.html'):
            self._static('index.html', 'text/html; charset=utf-8')
            return
        if path in ('/bgm.mp3', '/bgm.wav'):
            bgm = find_external_bgm()
            if bgm:
                self._static_abs(bgm[0], bgm[1])
                return
            if path == '/bgm.mp3':
                self._static('bgm.mp3', 'audio/mpeg')
            else:
                self._static('bgm.wav', 'audio/wav')
            return
        if path in ('/style.css', '/app.js'):
            if path == '/style.css':
                self._static('style.css', 'text/css; charset=utf-8')
            else:
                self._static('app.js', 'application/javascript; charset=utf-8')
            return
        if path == '/favicon.ico':
            ico = base64.b64decode(
                'AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAADAAAAAAAAAAP'
                'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                'AAAAAAAAAAAAAAAA')
            self.send_response(200)
            self.send_header('Content-Type', 'image/x-icon')
            self.send_header('Content-Length', str(len(ico)))
            self.end_headers()
            self.wfile.write(ico)
            return

        # ---- API ----
        if path == '/api/ping':
            self._json({'ok': True, 'version': APP_VERSION,
                        'dataRoot': DATA_ROOT})
            return
        if path == '/api/libs':
            libs = []
            for l in STORE.get_libs() if STORE else []:
                libs.append({
                    'id': l.id, 'name': l.name, 'tag': l.tag,
                    'importDate': l.import_date,
                    'fileCount': len(l.files), 'size': l.total_size,
                    'commonPath': l.common_path,
                })
            self._json({'libs': libs, 'version': STORE.version if STORE else 0,
                        'errors': (STORE.load_errors[-5:] if STORE else [])})
            return
        if path == '/api/categories':
            self._json({'categories': STORE.build_categories(
                self._libs_param(q)) if STORE else []})
            return
        if path == '/api/search':
            r = STORE.search(
                q.get('keyword', ''), q.get('cat1', ''), q.get('cat2', ''),
                self._libs_param(q), q.get('page', '1'),
                q.get('pageSize', '20'))
            self._json(r)
            return
        if path == '/api/storage':
            self._json({'categories': STORE.build_categories(
                self._libs_param(q)) if STORE else []})
            return
        if path == '/api/history':
            self._json({'history': HISTORY[-12:]})
            return
        if path == '/api/tmdb':
            r = tmdb_search(q.get('title', ''), q.get('year', ''))
            self._json({'poster': (r or {}).get('poster', '')})
            return
        if path == '/api/file-types':
            self._json({'groups': {k: sorted(v) for k, v
                                   in pan.FILE_TYPE_GROUPS.items()}})
            return
        if path == '/api/login/status':
            self._json({'logged': bool(AUTH['token']),
                        'nickname': AUTH['nickname'],
                        'uid': AUTH['uid']})
            return
        if path == '/api/import/files':
            out_dir = ''
            files = []
            try:
                out_dir = STORE.export_dir_path() if STORE else ''
                if out_dir and os.path.isdir(out_dir):
                    for n in sorted(os.listdir(out_dir)):
                        if n.lower().endswith('.json'):
                            files.append(n)
            except OSError:
                pass
            self._json({'files': files, 'dir': out_dir})
            return
        if path == '/api/extract/checkpoint':
            body = self._body()
            sk = q.get('shareKey') or body.get('shareKey') or ''
            link = (q.get('link') or body.get('link') or '').strip()
            if link and not sk:
                parsed = pan.parse_share_text(link)
                sk = (parsed or {}).get('shareKey', '')
            if not sk:
                self._json({'exists': False})
                return
            ck_dir = os.path.join(DATA_ROOT, '秒传文件导入或追加', '_checkpoints')
            ck = ExtractTask.load_checkpoint(ck_dir, sk)
            if not ck:
                self._json({'exists': False})
                return
            self._json({
                'exists': True,
                'totalFiles': ck.get('total_files', 0),
                'scanned': ck.get('scanned', 0),
                'skipped': ck.get('skipped', 0),
            })
            return
        if path == '/api/extract/progress':
            self._json(TASKS.snapshot_extract())
            return
        if path == '/api/import/progress':
            self._json(TASKS.snapshot_import())
            return
        if path == '/api/open-dir':
            out_dir = STORE.export_dir_path() if STORE else DATA_ROOT
            try:
                subprocess.Popen(['explorer.exe', os.path.normpath(out_dir)])
                self._json({'ok': True})
            except Exception as e:
                self._json({'ok': False, 'error': str(e)})
            return

        self._json({'error': 'unknown endpoint'}, 404)

    def _route_post(self):
        path = self.path.split('?')[0]
        b = self._body()

        # ---- 搜索历史 ----
        if path == '/api/history/add':
            item = {
                'keyword': b.get('keyword', ''),
                'cat1': b.get('cat1', ''),
                'cat2': b.get('cat2', ''),
                'results': b.get('results', 0),
                'ts': _now(),
            }
            HISTORY[:] = [h for h in HISTORY
                          if not (h.get('keyword') == item['keyword']
                                  and h.get('cat1') == item['cat1']
                                  and h.get('cat2') == item['cat2'])]
            HISTORY.append(item)
            del HISTORY[:-HISTORY_MAX]
            save_history()
            self._json({'ok': True})
            return
        if path == '/api/history/clear':
            HISTORY.clear()
            save_history()
            self._json({'ok': True})
            return

        # ---- 作品文件列表 ----
        if path == '/api/work/files':
            lib, w = STORE.get_work(b.get('libId'), b.get('dirName') or '',
                                    b.get('parentPath') or '')
            if not w:
                self._json({'error': '作品不存在'}, 404)
                return
            files = [{'path': fe['path'], 'size': fe['size'],
                      'etag': fe['etag']} for fe in w.files]
            self._json({'files': files,
                        'versions': detect_versions(
                            [os.path.basename(f['path']) for f in files])})
            return

        # ---- 导出 ----
        if path == '/api/export/dir':
            r, msg = STORE.export_dir(b.get('libId'), b.get('dirName') or '',
                                      b.get('parentPath') or '')
            self._json({'ok': bool(r), 'file': r, 'message': msg}
                       if r else {'ok': False, 'message': msg})
            return
        if path == '/api/export/category':
            r, msg = STORE.export_category(b.get('cat1', ''),
                                           b.get('cat2', ''),
                                           b.get('libIds'))
            self._json({'ok': bool(r), 'file': r, 'message': msg}
                       if r else {'ok': False, 'message': msg})
            return
        if path == '/api/export/merge':
            r, msg = STORE.export_merge(b.get('cats') or [], b.get('libIds'))
            self._json({'ok': bool(r), 'file': r, 'message': msg}
                       if r else {'ok': False, 'message': msg})
            return
        if path == '/api/export/selected':
            r, msg = STORE.export_selected(
                b.get('libId'), b.get('dirName') or '',
                b.get('parentPath') or '', b.get('paths') or [])
            self._json({'ok': bool(r), 'file': r, 'message': msg}
                       if r else {'ok': False, 'message': msg})
            return

        # ---- 前端日志 ----
        if path == '/api/client-log':
            app_log('前端: %s' % (b.get('msg') or ''), exc=bool(b.get('stack')))
            self._json({'ok': True})
            return

        # ---- 追加影库 ----
        if path == '/api/append-import':
            name = re.sub(r'[\\/:*?|><"]', '-',
                          b.get('name') or '追加影库.json')
            if not name.lower().endswith('.json'):
                name += '.json'
            content = b.get('content')
            try:
                json.loads(content)
            except ValueError as e:
                self._json({'ok': False, 'message': 'JSON 格式错误: %s' % e})
                return
            fp = os.path.join(DATA_ROOT, '秒传文件导入或追加', name)
            tmp = fp + '.uploading'
            last_err = None
            try:
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(tmp, 'w', encoding='utf-8') as f:
                    f.write(content)
                for _ in range(4):
                    try:
                        os.replace(tmp, fp)
                        last_err = None
                        break
                    except OSError as e:
                        last_err = e
                        time.sleep(0.3)
                if last_err is not None:
                    try:
                        os.remove(tmp)
                    except OSError:
                        pass
                    app_log('追加替换 %s 失败: %s' % (name, last_err), exc=True)
                    self._json({'ok': False,
                                'message': '文件被占用, 请稍后重试: %s'
                                           % last_err})
                    return
                app_log('追加入库成功: %s (%d 字符)' % (name, len(content)))
                self._json({'ok': True, 'file': name})
            except OSError as e:
                self._json({'ok': False, 'message': str(e)})
            return

        # ---- 分享提取 ----
        if path == '/api/extract/parse':
            parsed = pan.parse_share_text(b.get('link') or '')
            if not parsed:
                self._json({'ok': False, 'message': '无法识别分享链接'})
                return
            self._json({'ok': True, 'shareKey': parsed['shareKey'],
                        'pwd': parsed['pwd']})
            return
        if path == '/api/extract/list':
            parsed = pan.parse_share_text(b.get('link') or '')
            if not parsed:
                self._json({'ok': False, 'message': '无法识别分享链接'})
                return
            r = pan.share_browse_dir(parsed['shareKey'], parsed['pwd'],
                                     b.get('fileId') or 0)
            self._json(r)
            return
        if path == '/api/extract/checkpoint/delete':
            parsed = pan.parse_share_text(b.get('link') or '')
            sk = (parsed or {}).get('shareKey') or b.get('shareKey') or ''
            if sk:
                ck_dir = os.path.join(DATA_ROOT, '秒传文件导入或追加',
                                      '_checkpoints')
                ExtractTask.delete_checkpoint(ck_dir, sk)
            self._json({'ok': True})
            return
        if path == '/api/extract/start':
            parsed = pan.parse_share_text(b.get('link') or '')
            if not parsed:
                self._json({'ok': False, 'message': '无法识别分享链接'})
                return
            running = False
            if TASKS.extract:
                running = TASKS.extract.is_alive()
            if running:
                self._json({'ok': False, 'message': '已有提取任务在进行中'})
                return
            ft = b.get('fileTypes')
            exts = None
            if ft is not None:
                exts = set()
                for g in ft:
                    exts.update(pan.FILE_TYPE_GROUPS.get(g, []))
            t = ExtractTask(parsed['shareKey'], parsed['pwd'],
                            os.path.join(DATA_ROOT, '秒传文件导入或追加'),
                            b.get('title') or '', b.get('cat1') or '',
                            b.get('cat2') or '', exts,
                            title=b.get('title') or '',
                            cat1=b.get('cat1') or '',
                            cat2=b.get('cat2') or '',
                            file_types=exts)
            TASKS.extract = t
            t.start()
            self._json({'ok': True})
            return
        if path == '/api/extract/selected':
            parsed = pan.parse_share_text(b.get('link') or '')
            if not parsed:
                self._json({'ok': False, 'message': '无法识别分享链接'})
                return
            running = bool(TASKS.extract and TASKS.extract.is_alive())
            if running:
                self._json({'ok': False, 'message': '已有提取任务在进行中'})
                return
            t = ExtractTask(
                parsed['shareKey'], parsed['pwd'],
                os.path.join(DATA_ROOT, '秒传文件导入或追加'),
                b.get('title') or '', b.get('cat1') or '',
                b.get('cat2') or '', None,
                selected=b.get('selected') or [])
            TASKS.extract = t
            t.start()
            self._json({'ok': True})
            return
        if path == '/api/extract/stop':
            if TASKS.extract:
                TASKS.extract.stop()
            self._json({'ok': True})
            return

        # ---- 登录 ----
        if path == '/api/login/token':
            r = pan.login_token(b.get('token') or '')
            if r.get('ok'):
                AUTH['token'] = r['token']
                AUTH['nickname'] = r.get('nickname', '')
                AUTH['uid'] = r.get('uid', 0)
                save_auth()
            self._json(r)
            return
        if path == '/api/login/password':
            r = pan.login_password(b.get('passport') or '',
                                   b.get('password') or '')
            if r.get('ok'):
                AUTH['token'] = r['token']
                info = pan.user_info_from_token(r['token'])
                AUTH['nickname'] = info.get('nickname', '')
                AUTH['uid'] = info.get('uid', 0)
                save_auth()
                r.update(info)
            self._json(r)
            return
        if path == '/api/login/qrcode':
            r = pan.qr_create()
            self._json(r)
            return
        if path == '/api/login/qrcode/status':
            r = pan.qr_poll(b.get('uniId') or b.get('uniID') or '',
                            b.get('loginuuid') or AUTH['loginuuid'])
            tok = r.get('token')
            if tok:
                AUTH['token'] = tok
                info = pan.user_info_from_token(tok)
                AUTH['nickname'] = info.get('nickname', '')
                AUTH['uid'] = info.get('uid', 0)
                save_auth()
                r.update(info)
            self._json(r)
            return
        if path == '/api/logout':
            AUTH['token'] = ''
            AUTH['nickname'] = ''
            AUTH['uid'] = 0
            save_auth()
            self._json({'ok': True})
            return

        # ---- 秒传导入 ----
        if path == '/api/import/start':
            running = bool(TASKS.import_ and TASKS.import_.is_alive())
            if running:
                self._json({'ok': False, 'message': '已有导入任务在进行中'})
                return
            jp = b.get('file') or ''
            if not jp:
                self._json({'ok': False, 'message': '未指定影库文件'})
                return
            if not os.path.isabs(jp):
                jp = os.path.join(STORE.export_dir_path(), jp)
            if not os.path.isfile(jp):
                self._json({'ok': False, 'message': '影库文件不存在: %s' % jp})
                return
            if not AUTH['token']:
                self._json({'ok': False, 'message': '未登录'})
                return
            t = ImportTask(AUTH['token'], jp, b.get('targetDir') or '',
                           b.get('autoCommon', True), AUTH['loginuuid'])
            TASKS.import_ = t
            t.start()
            self._json({'ok': True})
            return
        if path == '/api/import/stop':
            if TASKS.import_:
                TASKS.import_.stop()
            self._json({'ok': True})
            return
        if path == '/api/import/upload':
            name = re.sub(r'[\\/:*?|><"]', '-',
                          b.get('name') or '影库.json')
            if not name.lower().endswith('.json'):
                name += '.json'
            content = b.get('content')
            try:
                json.loads(content)
            except ValueError as e:
                self._json({'ok': False, 'message': 'JSON 格式错误: %s' % e})
                return
            out_dir = STORE.export_dir_path() if STORE else DATA_ROOT
            try:
                os.makedirs(out_dir, exist_ok=True)
            except OSError as e:
                self._json({'ok': False, 'message': str(e)})
                return
            fp = os.path.join(out_dir, name)
            last_err = None
            try:
                for _ in range(4):
                    try:
                        with open(fp, 'w', encoding='utf-8') as f:
                            f.write(content)
                        last_err = None
                        break
                    except OSError as e:
                        last_err = e
                        time.sleep(0.3)
                if last_err is not None:
                    self._json({'ok': False, 'message': str(last_err)})
                    return
                app_log('影库上传成功: %s (%d 字符)' % (name, len(content)))
                self._json({'ok': True, 'file': name})
            except OSError as e:
                self._json({'ok': False, 'message': str(e)})
            return

        # ---- TMDB Key ----
        if path == '/api/tmdb-key':
            k = (b.get('key') or '').strip()
            if k:
                globals()['TMDB_KEY'] = {'key': k}
                cfg = load_config()
                cfg['tmdb_key'] = k
                save_config(cfg)
                self._json({'ok': True, 'key': k})
            else:
                globals()['TMDB_KEY'] = {'key': TMDB_KEY_DEFAULT}
                self._json({'ok': True, 'key': TMDB_KEY_DEFAULT})
            return

        self._json({'error': 'unknown endpoint'}, 404)


def _safe_traceback():
    try:
        traceback.print_exc()
    except Exception:
        pass


def _now():
    from datetime import datetime
    return datetime.now().strftime('%m-%d %H:%M')


def detect_versions(names):
    """按文件名识别版本标签: 4K/HDR/SDR/DV/H265/H264/AV1"""
    rules = [
        ('2160P HDR H265', ('2160', '4k', 'hdr', '265')),
        ('2160P', ('2160', '4k')),
        ('1080P HDR', ('1080', 'hdr')),
        ('1080P', ('1080',)),
        ('720P', ('720',)),
        ('DV', ('dovi', 'dolby vision', 'dv ')),
        ('H265', ('265', 'hevc')),
        ('H264', ('264', 'avc')),
        ('AV1', ('av1',)),
    ]
    groups = {}
    for n in names:
        ln = n.lower().replace('.', ' ')
        tags = []
        for label, keys in rules:
            for k in keys:
                if k in ln:
                    tags.append(label)
                    break
        key = ' '.join(sorted(set(tags))) if tags else '其他'
        groups.setdefault(key, []).append(n)
    if len(groups) <= 1:
        return []
    return [{'label': k, 'count': len(v), 'names': v}
            for k, v in sorted(groups.items(), key=lambda x: -len(x[1]))]


def find_free_port(start=5890):
    p = start
    for _ in range(50):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', p))
                return p
        except OSError:
            p += 1
    return start


def run_server():
    global HTTP_PORT
    HTTP_PORT = find_free_port(5890)
    srv = ThreadingHTTPServer(('127.0.0.1', HTTP_PORT), Handler)
    srv.serve_forever()


def main():
    init_data_root()
    url = 'http://127.0.0.1:%d/' % 0
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    import time as _t
    for _ in range(50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', HTTP_PORT)) == 0:
                break
        _t.sleep(0.1)
    url = 'http://127.0.0.1:%d/' % HTTP_PORT
    print(f'{APP_NAME} {APP_VERSION}  数据目录: {DATA_ROOT}  {url}')
    exe_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    browser_mode = ('浏览器版' in exe_name
                    or '--browser' in sys.argv
                    or os.environ.get('LB_BROWSER') == '1')
    if not browser_mode:
        if not _try_webview(url):
            webbrowser.open(url)
    try:
        print('浏览器模式运行中, 关闭此窗口或按 Ctrl+C 退出')
        while True:
            _t.sleep(3600)
    except KeyboardInterrupt:
        return


def _try_webview(url):
    """尝试 pywebview 桌面窗口（阻塞直到窗口关闭）"""
    try:
        import webview
    except ImportError:
        return False
    try:
        webview.create_window(APP_NAME, url, width=1560, height=900,
                              min_size=(1024, 600))
        webview.start()
        return True
    except Exception:
        return False


if __name__ == '__main__':
    main()
