# -*- coding: utf-8 -*-
"""影库数据层：加载、解析、分类、聚合、搜索、导出"""
import json
import os
import re
import threading
import time
from datetime import datetime

VIDEO_EXTS = set(frozenset({
    '.mp4', '.mkv', '.avi', '.ts', '.m2ts', '.wmv', '.rmvb', '.mov', '.flv',
    '.iso', '.m4v', '.mpg', '.mpeg', '.3gp', '.webm', '.vob',
}))

ALL_FALLBACK = '全部文件'

# 分类同义词：各种叫法归一到统一分类名
CAT_SYNONYMS = {
    '国剧': '国产剧集',
    '国产剧': '国产剧集',
    '华语剧': '国产剧集',
    '大陆剧': '国产剧集',
    '电视剧': '国产剧集',
    '美剧': '欧美剧集',
    '欧美剧': '欧美剧集',
    '英剧': '欧美剧集',
    '日剧': '日韩剧集',
    '韩剧': '日韩剧集',
    '日本动漫': '日韩动漫',
    '日番': '日韩动漫',
    '番剧': '日韩动漫',
    '韩国动漫': '日韩动漫',
    '国产动漫': '国产动漫',
    '华流动漫': '国产动漫',
    '欧美电影': '电影',
    '电影': '电影',
    '电影': '电影',
    '电影': '电影',
    '纪录': '纪录',
    '演唱会': '综艺',
}
CAT_SYNONYMS.update({
    '华语电影': '电影',
    '国产电影': '电影',
    '香港电影': '电影',
    '美国电影': '电影',
    '纪录片': '纪录',
    '记录': '纪录',
    '演唱会': '综艺',
    '综艺': '综艺',
})

# 分类展示顺序
CAT_ORDER = {
    '电影': 0,
    '电视剧': 1,
    '国产剧集': 1,
    '欧美剧集': 2,
    '日韩剧集': 3,
    '动漫': 4,
    '日韩动漫': 5,
    '国产动漫': 6,
    '综艺': 7,
    '纪录': 8,
    '演唱会': 9,
    '短剧': 10,
    '音频': 11,
    '其他': 98,
    ALL_FALLBACK: 99,
}

YEAR_RES = [
    re.compile(r'[\(（【\[]?((?:19|20)\d{2})[\)）】\]]?'),
    re.compile(r'((?:19|20)\d{2})'),
]
TMDB_RE = re.compile(r'\{tmdb-(\d+)\}', re.I)
SEASON_RE = re.compile(
    r'^(s\d{1,3}|season[\s._-]?\d{1,3}|第\s*\d+\s*[季部期]|[Ss]pecials?'
    r'|特别篇|OVA|OAD)$', re.I)


def to_int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        try:
            return int(float(v))
        except (TypeError, ValueError):
            return default


def parse_title_year(name):
    """从目录名/文件名提取标题与年份"""
    t = TMDB_RE.sub('', name)
    year = ''
    for rx in YEAR_RES:
        m = rx.search(t)
        if m:
            year = m.group(1)
            break
    title = t
    if year:
        idx = t.find(year)
        if idx >= 0:
            title = t[:idx] + t[idx + len(year):]
    title = re.sub(r'[\(（【\[]\s*[\)）】\]]', '', title)
    title = re.sub(r'[\.\_]+', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip(' -_.·')
    if not title:
        return name, year
    return title, year


class Work(object):
    """一部作品（一个作品目录，或根下的单个文件）"""

    __slots__ = ('lib_id', 'dir_name', 'title', 'year', 'files', 'file_count',
                 'size', 'video_count', 'cat1', 'cat2', 'parent_path')

    def __init__(self, lib_id, dir_name, title, year, cat1, cat2, parent_path):
        self.lib_id = lib_id
        self.dir_name = dir_name
        self.title = title
        self.year = year
        self.cat1 = cat1
        self.cat2 = cat2
        self.parent_path = parent_path
        self.files = []
        self.file_count = 0
        self.size = 0
        self.video_count = 0


class Library(object):
    """一个影库 JSON"""

    _next_id = [0]

    def __init__(self, path, tag='原库'):
        self.id = Library._next_id[0]
        Library._next_id[0] += 1
        self.path = path
        self.name = os.path.splitext(os.path.basename(path))[0]
        if self.name.endswith('.123fastlink'):
            self.name = self.name[:-len('.123fastlink')]
        self.tag = tag
        self.import_date = datetime.now().strftime('%Y%m%d')
        self.common_path = ''
        self.files = []
        self.total_size = 0
        self.works = {}
        self.mtime = 0

    def load(self):
        st = os.stat(self.path)
        self.mtime = st.st_mtime
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        raw_files = []
        if isinstance(data, dict):
            if isinstance(data.get('libraries'), list):
                for lib in data['libraries']:
                    cp = lib.get('commonPath') or ''
                    for fe in lib.get('files') or []:
                        raw_files.append((cp, fe))
            elif isinstance(data, dict):
                cp = data.get('commonPath') or ''
                for fe in data.get('files') or []:
                    raw_files.append((cp, fe))
        elif isinstance(data, list):
            for fe in data:
                raw_files.append(('', fe))

        self.common_path = raw_files[0][0] if raw_files else ''
        if not self.common_path:
            self.common_path = ''
        if raw_files:
            cps = set(x[0] for x in raw_files)
            if len(cps) == 1:
                self.common_path = cps.pop()
            else:
                self.common_path = _common_prefix(sorted(cps))
        if not self.common_path:
            self.common_path = ''.strip().lstrip('/')

        files = []
        seen_etag = set()
        for cp, fe in raw_files:
            p = fe.get('path') or fe.get('Path') or ''
            etag = (fe.get('etag') or fe.get('Etag') or '').strip()
            size = to_int(fe.get('size'), 0)
            if not p or not etag:
                continue
            p = p.replace('\\', '/').lstrip('/')
            key = etag.lower()
            if key in seen_etag:
                continue
            seen_etag.add(key)
            entry = {'path': p, 'etag': etag, 'size': size}
            # 透传导出时需要的原始字段
            if fe.get('fileName'):
                entry['fileName'] = fe['fileName']
            if fe.get('s3KeyFlag'):
                entry['s3KeyFlag'] = fe['s3KeyFlag']
            if 'type' in fe:
                entry['type'] = fe['type']
            files.append(entry)

        self.files = files
        self.total_size = sum(f['size'] for f in files)
        self._aggregate()

    def _aggregate(self):
        """按作品目录聚合"""
        self.works = {}
        cp = self.common_path
        for fe in self.files:
            path = fe['path']
            if cp:
                if path.startswith(cp):
                    path = path[len(cp):]
            parts = [x for x in path.split('/') if x]
            if len(parts) == 1:
                # 根目录下的单个文件
                fname = parts[0]
                key = '|root|' + fname
                if key not in self.works:
                    title, year = parse_title_year(os.path.splitext(fname)[0])
                    w = Work(self.id, fname, title, year, ALL_FALLBACK, '',
                             '')
                    self.works[key] = w
                w = self.works[key]
            else:
                idx = len(parts) - 2
                if idx > 0 and SEASON_RE.match(parts[idx].strip()):
                    idx -= 1
                dir_name = parts[idx]
                parent_path = '/'.join(parts[:idx])
                if parent_path:
                    cat1 = parent_path.split('/')[0]
                    if len(parent_path.split('/')) > 1:
                        cat2 = parent_path.split('/')[1]
                    else:
                        cat2 = ''
                else:
                    cat1, cat2 = ALL_FALLBACK, ''
                cat1 = CAT_SYNONYMS.get(cat1, cat1)
                cat2 = CAT_SYNONYMS.get(cat2, cat2)
                key = parent_path + '/' + dir_name
                if key not in self.works:
                    title, year = parse_title_year(dir_name)
                    w = Work(self.id, dir_name, title, year, cat1, cat2,
                             parent_path)
                    self.works[key] = w
                w = self.works[key]
            w.files.append(fe)
            w.file_count += 1
            w.size += fe['size']
            ext = os.path.splitext(fe['path'])[1].lower()
            if ext in VIDEO_EXTS:
                w.video_count += 1


class LibraryStore(object):
    """多影库管理 + Watcher"""

    def __init__(self, import_dir):
        self.import_dir = import_dir
        self.libraries = {}
        self.lock = threading.RLock()
        self.version = 0
        self.load_errors = []
        self.scan(initial=True)

    def scan(self, initial=False):
        try:
            names = set(n for n in os.listdir(self.import_dir)
                        if n.lower().endswith('.json')
                        and not os.path.basename(n).startswith('.'))
        except OSError:
            names = set()
        changed = False
        for n in sorted(names):
            fp = os.path.join(self.import_dir, n)
            try:
                st = os.stat(fp)
                if st.st_size == 0:
                    continue
            except OSError:
                continue
            existing = None
            for lib in list(self.libraries.values()):
                if os.path.normcase(lib.path) == os.path.normcase(fp):
                    existing = lib
                    break
            # 已存在且 mtime 没变 → 跳过
            if existing is not None:
                if abs(existing.mtime - st.st_mtime) < 1:
                    continue
            # 文件还在写入（2 秒内改过）→ 等下轮
            if time.time() - st.st_mtime < 2:
                continue

            if existing is None:
                tag = '追加' if not initial else ('原库' if not self.libraries
                                              else '追加')
                lib = Library(fp, tag=tag)
            else:
                lib = existing
            try:
                lib.load()
            except Exception as e:
                self.load_errors.append('加载 %s 失败: %s' % (n, e))
                continue
            if existing is None:
                with self.lock:
                    self.libraries[lib.id] = lib
                changed = True
        # 清理已删除的文件
        for lib in list(self.libraries.values()):
            if not os.path.exists(lib.path):
                with self.lock:
                    self.libraries.pop(lib.id, None)
                changed = True
        if changed:
            self.version += 1

    def watcher_loop(self):
        while True:
            try:
                time.sleep(3)
                self.scan()
            except Exception:
                pass

    def get_libs(self, lib_ids=None):
        with self.lock:
            libs = [l for l in self.libraries.values()
                    if lib_ids is None or l.id in lib_ids]
        libs.sort(key=lambda l: l.id)
        return libs

    def selected_libs(self, sel):
        """sel: None=全部, 或 [id]"""
        if not sel:
            return self.get_libs()
        return self.get_libs(sel)

    def build_categories(self, lib_ids=None):
        """返回 [{name,count,works,size,children:[{name,count,works,size}]}]"""
        cats = {}
        for lib in self.selected_libs(lib_ids):
            for w in lib.works.values():
                c1 = cats.setdefault(w.cat1, {
                    'name': w.cat1, 'count': 0, 'works': 0, 'size': 0,
                    'children': {}})
                c1['count'] += w.file_count
                c1['works'] += 1
                c1['size'] += w.size
                if w.cat2:
                    c2 = c1['children'].setdefault(w.cat2, {
                        'name': w.cat2, 'count': 0, 'works': 0, 'size': 0})
                    c2['count'] += w.file_count
                    c2['works'] += 1
                    c2['size'] += w.size
        out = []
        for name, c in cats.items():
            c['children'] = sorted(c['children'].values(),
                                   key=lambda x: (-x['works'], x['name']))
            out.append(c)
        out.sort(key=lambda x: (CAT_ORDER.get(x['name'], 50), x['name']))
        return out

    def iter_works(self, lib_ids=None):
        for lib in self.selected_libs(lib_ids):
            for w in lib.works.values():
                yield lib, w

    def search(self, keyword, cat1='', cat2='', lib_ids=None, page=1,
               page_size=20, sort=''):
        """mode 由参数组合决定: 片名搜索/分类浏览/混合搜索"""
        works = []
        kw = (keyword or '').strip().lower()
        for lib, w in self.iter_works(lib_ids):
            if kw:
                if (kw not in w.title.lower()
                        and kw not in w.dir_name.lower()
                        and kw not in w.cat1.lower()
                        and kw not in (w.cat2 or '').lower()):
                    continue
            if cat1:
                if w.cat1 != cat1:
                    continue
            if cat2:
                if w.cat2 != cat2:
                    continue
            works.append(w)
        if kw or cat1 or cat2:
            works.sort(key=lambda w: (w.year or '', w.title))
        else:
            works.sort(key=lambda w: (-w.video_count, w.title))
        total = len(works)
        try:
            page = max(1, int(page))
        except (TypeError, ValueError):
            page = 1
        page_size = int(page_size)
        if page_size not in (20, 50, 100):
            page_size = 20
        start = (page - 1) * page_size
        items = []
        for w in works[start:start + page_size]:
            lib = self.libraries.get(w.lib_id)
            items.append({
                'libId': w.lib_id,
                'libName': lib.name if lib else '',
                'dirName': w.dir_name,
                'title': w.title,
                'year': w.year,
                'cat1': w.cat1,
                'cat2': w.cat2,
                'parentPath': w.parent_path,
                'fileCount': w.file_count,
                'size': w.size,
                'videoCount': w.video_count,
            })
        return {'total': total, 'page': page, 'pageSize': page_size,
                'works': items}

    def get_work(self, lib_id, key_dir, parent_path=''):
        lib = self.libraries.get(int(lib_id))
        if not lib:
            return (None, None)
        for w in lib.works.values():
            if w.dir_name == key_dir:
                if parent_path:
                    if w.parent_path == parent_path:
                        return (lib, w)
                else:
                    return (lib, w)
        return (lib, None)

    def export_dir(self, lib_id, dir_name, parent_path, out_dir=None):
        lib, w = self.get_work(lib_id, dir_name, parent_path)
        if not w:
            return (None, '作品不存在')
        common = '/'.join(x for x in (lib.common_path, w.parent_path,
                                      w.dir_name) if x)
        files = []
        for fe in w.files:
            p = fe['path']
            if lib.common_path:
                if p.startswith(lib.common_path):
                    p = p[len(lib.common_path):]
            if w.parent_path:
                if p.startswith(w.parent_path + '/'):
                    p = p[len(w.parent_path) + 1:]
            else:
                if p.startswith(w.dir_name + '/'):
                    p = p[len(w.dir_name) + 1:]
            files.append(dict(fe, path=p))
        name = '秒传-%s-%d个文件-%s.json' % (_safe_name(w.dir_name),
                                          len(files), _ts())
        return _write_export(files, common, name, out_dir or
                             self.export_dir_path())

    def export_category(self, cat1, cat2='', lib_ids=None):
        files = []
        common_parts = []
        for lib, w in self.iter_works(lib_ids):
            if w.cat1 != cat1:
                continue
            if cat2:
                if w.cat2 != cat2:
                    continue
            for fe in w.files:
                p = fe['path']
                if lib.common_path:
                    if p.startswith(lib.common_path):
                        p = p[len(lib.common_path):]
                prefix = w.cat1 + ('/' + w.cat2 if w.cat2 else '')
                if w.cat1 == ALL_FALLBACK:
                    if p.startswith(prefix + '/'):
                        p = p[len(prefix) + 1:]
                files.append(dict(fe, path=p))
        if not files:
            return (None, '该分类下没有文件')
        lib0 = self.selected_libs(lib_ids)
        common = lib0[0].common_path if lib0 else ''
        common = ((common + '/') if common else '') + cat1 + (
            '/' + cat2 if cat2 else '')
        common = common.strip('/')
        name = '秒传-%s-%d个文件-%s.json' % (_safe_name(common), len(files),
                                          _ts())
        return _write_export(files, common, name, self.export_dir_path())

    def export_merge(self, cats, lib_ids=None):
        """cats: [{"cat1":x,"cat2":y}] 合并导出, 保留完整路径, 去重"""
        files = []
        seen = set()
        for lib, w in self.iter_works(lib_ids):
            hit = False
            for c in cats:
                if w.cat1 != c.get('cat1'):
                    continue
                if c.get('cat2'):
                    if w.cat2 != c.get('cat2'):
                        continue
                hit = True
                break
            if not hit:
                continue
            for fe in w.files:
                key = fe['etag'].lower()
                if key in seen:
                    continue
                seen.add(key)
                p = fe['path']
                if lib.common_path:
                    if p.startswith(lib.common_path):
                        p = p[len(lib.common_path):]
                files.append(dict(fe, path=p))
        if not files:
            return (None, '选中分类下没有文件')
        lib0 = self.selected_libs(lib_ids)
        common = lib0[0].common_path if lib0 else ''
        common = (common or '').strip('/')
        labels = sorted(set(
            '%s/%s' % (c.get('cat1'), c.get('cat2')) if c.get('cat2')
            else c.get('cat1') or '' for c in cats))
        if len(labels) <= 10 and sum(len(x) for x in labels) <= 80:
            fname = '秒传-合并导出-%d个分类-%d个文件-%s.json' % (
                len(labels), len(files), _ts())
        else:
            fname = '秒传-合并导出-%s-%d个文件-%s.json' % (
                _safe_name('+'.join(labels)), len(files), _ts())
        return _write_export(files, common, fname, self.export_dir_path())

    def export_selected(self, lib_id, dir_name, parent_path, selected_paths):
        lib, w = self.get_work(lib_id, dir_name, parent_path)
        if not w:
            return (None, '作品不存在')
        sel = set(selected_paths or [])
        files = [fe for fe in w.files if fe['path'] in sel]
        if not files:
            return (None, '没有选中任何文件')
        common = '/'.join(x for x in (lib.common_path, w.parent_path,
                                      w.dir_name) if x)
        rel = []
        for fe in files:
            p = fe['path']
            if lib.common_path:
                if p.startswith(lib.common_path):
                    p = p[len(lib.common_path):]
            if w.parent_path:
                if p.startswith(w.parent_path + '/'):
                    p = p[len(w.parent_path) + 1:]
            else:
                if p.startswith(w.dir_name + '/'):
                    p = p[len(w.dir_name) + 1:]
            rel.append(p)
        label = _episode_label([os.path.basename(p) for p in rel])
        name = '秒传-%s%s-%d个文件-%s.json' % (_safe_name(w.dir_name), label,
                                          len(files), _ts())
        return _write_export([dict(fe, path=p) for fe, p in zip(files, rel)],
                             common, name, self.export_dir_path())

    def export_dir_path(self):
        return os.path.join(
            os.path.dirname(self.import_dir.rstrip('\\/')),
            '秒传文件导出')

    def storage_stats(self, lib_ids=None):
        return self.build_categories(lib_ids)


def _common_prefix(paths):
    if not paths:
        return ''
    p0 = paths[0]
    for p in paths[1:]:
        i = 0
        while i < len(p0) and i < len(p) and p0[i] == p[i]:
            i += 1
        p0 = p0[:i]
    if p0:
        if '/' in p0:
            p0 = p0[:p0.rfind('/') + 1]
    return p0


def _ts():
    return datetime.now().strftime('%Y%m%d-%H%M%S')


def _safe_name(s):
    return re.sub(r'[\\/:*?|><"]', '-', s)[:60]


def _episode_label(names):
    """按集数范围给导出文件命名, 如 -第1-3集"""
    eps = []
    for n in names:
        m = re.search(r'[Ee][Pp]?(\d{1,4})|第(\d{1,4})[集话期]', n)
        if m:
            eps.append(to_int(m.group(1) or m.group(2)))
    if not eps:
        return ''
    eps.sort()
    if eps[0] == eps[-1]:
        return '-第%d集' % eps[0]
    return '-第%d-%d集' % (eps[0], eps[-1])


def _write_export(files, common_path, fname, out_dir):
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        return (None, '创建导出目录失败: %s' % e)
    fp = os.path.join(out_dir, fname)
    data = {
        'scriptVersion': '3.2.0',
        'exportVersion': '1.0',
        'usesBase62EtagsInExport': True,
        'commonPath': (common_path or '').strip('/'),
        'totalFilesCount': len(files),
        'totalSize': sum(f.get('size') or 0 for f in files),
        'files': files,
    }
    data['formattedTotalSize'] = _fmt_size(data['totalSize'])
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return (fname, '导出成功: %s (%d 个文件)' % (fname, len(files)))


def _fmt_size(n):
    for unit in ('B', 'KB', 'MB', 'GB', 'TB', 'PB'):
        if n < 1024:
            if unit == 'PB':
                return '%.2f %s' % (n, unit)
            if unit == 'B':
                return '%d B' % n
            return '%.2f %s' % (n, unit)
        n = n / 1024.0
    return '%d B' % n
