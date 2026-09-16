# -*- coding: utf-8 -*-
"""
123云盘 API 封装（网页端协议）
- 分享链接提取（免登录）
- 扫码 / Bearer Token / 账号密码 三种登录
- 目录列表 / 建目录 / 秒传上传（Bearer Token 鉴权，2026-07 起无需签名）

本文件由字节码还原（tools/bytecode/pan123_api.pyc），逐函数对照指令重建，
已通过语法检查。还原依据为原始字节码常量/变量名，未做行为猜测。
"""
import base64
import hashlib
import json
import os
import re
import socket
import time
import uuid
import platform as _platform

import requests

WEB_BASE = 'https://www.123pan.cn'
WEB_BASE_ALT = 'https://www.123pan.com'
LOGIN_BASE = 'https://user.123pan.cn'
LOGIN_PAGE_URL = '/centerlogin?redirect_url=https%3A%2F%2Fyun.123pan.cn&source_page=website'

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0')

# 分享链接与提取码
SHARE_URL_RE = re.compile(
    r'https?://(?:www\.)?(?:123pan\.com|123pan\.cn|123684\.com|123865\.com'
    r'|123912\.com|123912\.cn|123865\.cn)/s/([A-Za-z0-9_\-]+)')
PWD_RE = re.compile(
    r'(?:提取码|访问码|密码|提取[:：\s]*|pwd[=:]?)\s*[:：]?\s*([A-Za-z0-9]{4})')

# 扫码状态
QR_WAITING = 0
QR_SCANNED = 1
QR_CONFIRMED = 2
QR_EXPIRED = 3
QR_NO_SESSION = 4

BASE62_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
FAST_BASES = ('https://api.123278.com',)

# 文件类型分组（按扩展名归类，用于提取时过滤/分类）
FILE_TYPE_GROUPS = {
    '视频': ('.mp4', '.mkv', '.avi', '.ts', '.m2ts', '.wmv', '.rmvb', '.mov',
             '.flv', '.iso', '.m4v', '.mpg', '.mpeg', '.3gp', '.webm', '.vob'),
    '字幕': ('.srt', '.ass', '.ssa', '.sub', '.idx', '.sup'),
    '音频': ('.mp3', '.flac', '.wav', '.aac', '.m4a', '.ape', '.ogg', '.wma',
             '.dsf', '.dff'),
    '图片': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.tiff'),
    '文档': ('.txt', '.pdf', '.doc', '.docx', '.nfo', '.md', '.html', '.epub',
             '.xlsx', '.csv'),
    '压缩包': ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.001'),
}


def base62_to_hex(s):
    """123fastlink base62 etag → 32位小写 hex MD5。"""
    num = 0
    for c in s:
        idx = BASE62_CHARS.find(c)
        if idx < 0:
            raise ValueError('非 base62 字符: %r' % c)
        num = num * 62 + idx
    return format(num, 'x').zfill(32)


def normalize_etag(etag):
    """统一成 123pan 秒传 API 需要的 32 位小写 hex MD5。
兼容: 32位hex / base62(123fastlink V2导出,前导零时20~21位) / base64(MD5字节)"""
    e = (etag or '').strip().strip('"')
    if re.fullmatch('[0-9a-fA-F]{32}', e):
        return e.lower()
    if re.fullmatch('[A-Za-z0-9]{15,22}', e):
        try:
            return base62_to_hex(e)
        except ValueError:
            pass
    if re.fullmatch('[A-Za-z0-9+/]{23}=', e):
        try:
            return base64.b64decode(e).hex()
        except Exception:
            pass
    return e.lower()


def gen_login_uuid():
    """生成设备指纹（64位hex），同一台机器保持稳定。"""
    try:
        username = os.getlogin()
    except OSError:
        username = os.environ.get('USERNAME', os.environ.get('USER', 'unknown'))
    raw = f'{socket.gethostname()}:{username}:{_platform.system()}'
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def base_headers(loginuuid=None, token=None):
    h = {
        'User-Agent': UA,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'App-Version': '3',
        'platform': 'web',
        'LoginUuid': loginuuid or gen_login_uuid(),
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    }
    if token:
        if not token.startswith('Bearer '):
            token = 'Bearer ' + token
        h['Authorization'] = token
    return h


def decode_jwt_payload(token):
    """从 JWT token 里解出用户信息（nickname / id）。失败返回空 dict。"""
    try:
        payload = token.split('.')[1]
        payload = payload + '=' * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload.encode()).decode('utf-8', 'ignore'))
        return {
            'nickname': data.get('nickname') or data.get('username') or '',
            'uid': data.get('id') or data.get('ID') or 0,
        }
    except Exception:
        return {}


def parse_share_text(text):
    """从用户粘贴的文本中解析分享链接和提取码。"""
    if not text:
        return None
    text = text.strip()
    m = SHARE_URL_RE.search(text)
    if not m:
        return None
    share_key = m.group(1)
    pwd = ''
    mp = PWD_RE.search(text)
    if mp:
        pwd = mp.group(1)
    else:
        # 正文中没有，尝试从链接后面的尾巴里找 4 位码
        tail = text[m.end():].strip()
        m2 = re.match(r'^[\s:：]*(?:提取码)?[\s:：]*([A-Za-z0-9]{4})$', tail)
        if m2:
            pwd = m2.group(1)
    return {'shareKey': share_key, 'pwd': pwd}


# ---------------------------------------------------------------- 分享浏览

def share_list_page(share_key, pwd, parent_file_id, page, limit):
    """分享目录列表（单页）。返回 (info_list, total, message)。"""
    url = WEB_BASE + '/a/api/share/get'
    params = {
        'limit': limit,
        'next': '1',
        'orderBy': 'file_name',
        'orderDirection': 'asc',
        'shareKey': share_key,
        'SharePwd': pwd,
        'ParentFileId': parent_file_id,
        'Page': page,
        'event': 'homeListFile',
        'operateType': 4,
    }
    last_msg = ''
    for base in (WEB_BASE, WEB_BASE_ALT):
        try:
            r = requests.get(base + '/a/api/share/get', params=params,
                             headers=base_headers(), timeout=15)
            data = r.json()
            if data.get('code') == 0:
                d = data.get('data') or {}
                return (d.get('InfoList') or [],
                        d.get('Total') or 0,
                        '')
            last_msg = data.get('message') or ('code=%s' % data.get('code'))
        except Exception as e:
            last_msg = str(e)
    return (None, 0, last_msg)


def share_browse_dir(share_key, pwd, parent_file_id):
    """浏览分享：返回某个目录的一页内容（limit=100 足够浏览用）。"""
    infos, total, msg = share_list_page(share_key, pwd, parent_file_id, 1, 100)
    if infos is None:
        return {'ok': False, 'message': msg or '获取分享目录失败'}
    items = []
    for it in infos:
        items.append({
            'fileId': it.get('FileId'),
            'name': it.get('FileName'),
            'isDir': it.get('Type') == 1,
            'size': int(it.get('Size') or 0),
            'etag': (it.get('Etag') or '').lower(),
        })
    items.sort(key=lambda x: (0 if x['isDir'] else 1, x['name'] or ''))
    return {'ok': True, 'items': items}


def share_walk(share_key, pwd, file_types, progress_cb, checkpoint_cb,
               resume_files, resume_offset):
    """递归遍历分享目录树，提取全部文件。

file_types: 允许的扩展名集合(set, 小写含点)，None 表示不过滤
progress_cb: (scanned, skipped, current_path)
checkpoint_cb: (files_so_far, scanned, skipped) 每页保存一次检查点
resume_files: 断点续传时已收集的文件列表
返回 files 列表: [{path, etag, size}]
"""
    files = list(resume_files) if resume_files else []
    scanned = resume_offset['scanned'] if resume_offset else len(files)
    skipped = resume_offset['skipped'] if resume_offset else 0
    done_dirs = set(resume_offset.get('done_dirs') or []) if resume_offset else set()

    def _walk(parent_id, path):
        nonlocal scanned, skipped
        page = 1
        while True:
            infos, total, msg = share_list_page(share_key, pwd, parent_id, page, 100)
            if infos is None:
                raise RuntimeError('遍历分享目录失败: %s (位于 %s)' % (msg, path or '根目录'))
            for it in infos:
                name = it.get('FileName') or ''
                item_path = (path + '/' + name) if path else name
                if it.get('Type') == 1:
                    fid = it.get('FileId')
                    if fid in done_dirs:
                        continue
                    _walk(fid, item_path)
                    done_dirs.add(fid)
                    if checkpoint_cb:
                        checkpoint_cb(files, scanned, skipped, list(done_dirs))
                    continue
                # ---- 普通文件 ----
                scanned += 1
                ext = os.path.splitext(name)[1].lower()
                if file_types is not None:
                    if ext not in file_types:
                        skipped += 1
                        continue
                etag = (it.get('Etag') or '').lower()
                if etag:
                    files.append({'path': item_path, 'etag': etag,
                                  'size': int(it.get('Size') or 0)})
                    if len(files) % 500 == 0 and checkpoint_cb:
                        checkpoint_cb(files, scanned, skipped, list(done_dirs))
                    if progress_cb and scanned % 50 == 0:
                        progress_cb(scanned, skipped, item_path)
            # 不足一页 → 本目录遍历结束
            if len(infos) < 100:
                return
            page += 1
            if checkpoint_cb:
                checkpoint_cb(files, scanned, skipped, list(done_dirs))
            if progress_cb:
                progress_cb(scanned, skipped, path or '根目录')

    _walk(0, '')
    if progress_cb:
        progress_cb(scanned, skipped, '完成')
    return files, scanned, skipped


# ---------------------------------------------------------------- 会话管理

_QR_SESSIONS = {}
_QR_ORDER = []


def _qr_session():
    s = requests.Session()
    try:
        s.get(LOGIN_PAGE_URL, headers={'User-Agent': UA}, timeout=10)
    except Exception:
        pass
    return s


def _qr_get_session(uni_id):
    s = _QR_SESSIONS.get(uni_id)
    if s is None:
        s = _qr_session()
        _QR_SESSIONS[uni_id] = s
        _QR_ORDER.append(uni_id)
        while len(_QR_ORDER) > 20:
            old = _QR_ORDER.pop(0)
            _QR_SESSIONS.pop(old, None)
    return s


def _qr_drop_session(uni_id):
    _QR_SESSIONS.pop(uni_id, None)
    try:
        _QR_ORDER.remove(uni_id)
    except ValueError:
        pass


# ---------------------------------------------------------------- 扫码登录

def qr_create():
    """生成扫码登录二维码。返回 {ok, qr_url, uni_id, message}"""
    s = _qr_session()
    loginuuid = gen_login_uuid()
    headers = base_headers(loginuuid)
    headers['Content-Type'] = 'application/json'
    headers['Origin'] = LOGIN_BASE
    headers['Referer'] = LOGIN_PAGE_URL
    headers['app-version'] = '132'
    try:
        r = s.get(LOGIN_BASE + '/api/user/qr-code/generate',
                  params={'uniID': str(uuid.uuid4())},
                  headers=headers, timeout=10)
        data = r.json()
        if data.get('code') != 0:
            return {'ok': False, 'message': data.get('message') or '获取二维码失败'}
        d = data.get('data') or {}
        uni_id = d.get('uniID', '')
        base_url = d.get('url', '')
        if not uni_id or not base_url:
            return {'ok': False, 'message': '二维码响应缺少字段'}
        qr_url = f'{base_url}?uniID={uni_id}&env=production'
        _QR_SESSIONS[uni_id] = s
        _QR_ORDER.append(uni_id)
        return {'ok': True, 'qr_url': qr_url, 'uni_id': uni_id,
                'loginuuid': loginuuid}
    except Exception as e:
        return {'ok': False, 'message': '请求二维码失败: %s' % e}


def _qr_wx_code(s, uni_id, headers):
    try:
        r = s.post(LOGIN_BASE + '/api/user/qr-code/wx_code',
                   headers=headers, json={'uniID': uni_id}, timeout=10)
        data = r.json()
        if data.get('code') != 0:
            return None
        d = data.get('data') or {}
        return d.get('wxCode') or d.get('wechat_code') or None
    except Exception:
        return None


def _sign_in_wechat(s, wx_code, headers):
    headers = dict(headers)
    headers['Content-Type'] = 'application/json'
    payload = {'from': 'web', 'wechat_code': wx_code, 'type': 4,
               'remember': True, 'gray': True}
    try:
        r = s.post(LOGIN_BASE + '/api/user/sign_in',
                   headers=headers, json=payload, timeout=20)
        data = r.json()
        code = data.get('code')
        if code not in (0, 200):
            return {'ok': False,
                    'message': data.get('message') or ('登录失败 code=%s' % code)}
        token = (data.get('data') or {}).get('token') or ''
        if not token:
            try:
                token = r.cookies.get('sso-token') or ''
                if not token:
                    sc = r.headers.get('set-cookie', '') or ''
                    if 'sso-token=' in sc:
                        m = re.search('sso-token=([^;]+)', sc)
                        if m:
                            token = m.group(1)
            except Exception:
                pass
        if not token:
            return {'ok': False, 'message': '登录响应中无 token'}
        if token.startswith('Bearer '):
            token = token[7:]
        return {'ok': True, 'token': token}
    except Exception as e:
        return {'ok': False, 'message': str(e)}

def qr_poll(uni_id, loginuuid):
    """轮询扫码状态。返回 {ok, status, token?, nickname?, uid?, message}"""
    headers = base_headers(loginuuid)
    headers['Referer'] = LOGIN_PAGE_URL
    headers['app-version'] = '132'
    s = _qr_get_session(uni_id)
    try:
        r = s.get(LOGIN_BASE + '/api/user/qr-code/result',
                  params={'uniID': uni_id, 'remember': 'true', 'gray': 'true'},
                  headers=headers, timeout=10)
        data = r.json()
        if data.get('code') != 0:
            return {'ok': False, 'message': data.get('message') or '轮询失败'}
        status = (data.get('data') or {}).get('loginStatus', -1)
        result = {'ok': True, 'status': status}
        if status in (QR_SCANNED, QR_CONFIRMED, QR_EXPIRED):
            wx = _qr_wx_code(s, uni_id, headers)
            if wx:
                login = _sign_in_wechat(s, wx, headers)
                if login.get('ok'):
                    result['token'] = login['token']
                    _qr_drop_session(uni_id)
                    return result
                result['wx_pending'] = True
                return result
            result['wx_pending'] = True
            return result
        return result
    except Exception as e:
        return {'ok': False, 'message': str(e)}


# ---------------------------------------------------------------- 登录

def login_password(passport, password):
    """账号密码登录。"""
    s = _qr_session()
    headers = base_headers()
    headers['Content-Type'] = 'application/json'
    headers['Origin'] = LOGIN_BASE
    headers['Referer'] = LOGIN_PAGE_URL
    payload = {'passport': passport, 'password': password, 'type': 1,
               'remember': True, 'from': 'web', 'gray': True}
    try:
        r = s.post(LOGIN_BASE + '/api/user/sign_in',
                   headers=headers, json=payload, timeout=20)
        data = r.json()
        code = data.get('code')
        if code not in (0, 200):
            return {'ok': False,
                    'message': data.get('message') or ('登录失败 code=%s' % code)}
        token = (data.get('data') or {}).get('token') or ''
        if not token:
            return {'ok': False, 'message': '登录响应中无 token'}
        return {'ok': True, 'token': token}
    except Exception as e:
        return {'ok': False, 'message': '登录请求失败: %s' % e}


def login_token(token):
    """Bearer Token 登录（校验有效性）。"""
    token = token.strip()
    if token.startswith('Bearer '):
        token = token[7:]
    info = _token_verify(token)
    if not info.get('ok'):
        return info
    info = user_info_from_token(token)
    return {'ok': True, 'token': token, **info}


def _token_verify(token):
    headers = base_headers(token=token)
    try:
        r = requests.get(LOGIN_BASE + '/api/user/token/verify',
                         headers=headers, timeout=10)
        data = r.json()
        if data.get('code') in (0, 200):
            return {'ok': True}
        r2 = requests.get(WEB_BASE + '/b/api/user/info',
                          headers=base_headers(token=token), timeout=10)
        d2 = r2.json()
        if d2.get('code') in (0, 200):
            return {'ok': True}
        return {'ok': False, 'message': d2.get('message') or 'Token 校验失败'}
    except Exception as e:
        return {'ok': False, 'message': 'Token 校验请求失败: %s' % e}


def user_info_from_token(token):
    """优先从业务接口取昵称/UID，失败则解 JWT。"""
    info = {}
    try:
        r = requests.get(WEB_BASE + '/b/api/user/info',
                         headers=base_headers(token=token), timeout=10)
        data = r.json()
        if data.get('code') in (0, 200):
            d = data.get('data') or {}
            info = {
                'nickname': (d.get('Nickname') or d.get('nickname') or ''),
                'uid': (d.get('UID') or d.get('uid') or d.get('ID') or 0),
            }
            if not info.get('nickname'):
                info = decode_jwt_payload(token)
            return info
    except Exception:
        pass
    return info


# ---------------------------------------------------------------- 云盘操作

def file_list_dir(token, parent_file_id, loginuuid):
    """列出一个目录的全部内容（自动翻页）。失败返回 (None, msg)。"""
    headers = base_headers(loginuuid, token)
    items = []
    page = 1
    total = -1
    while total < 0 or len(items) < total:
        params = {
            'driveId': 0,
            'limit': 100,
            'next': 0,
            'orderBy': 'file_name',
            'orderDirection': 'asc',
            'parentFileId': str(parent_file_id),
            'trashed': 'false',
            'SearchData': '',
            'Page': str(page),
            'OnlyLookAbnormalFile': 0,
        }
        try:
            r = requests.get(WEB_BASE + '/b/api/file/list/new',
                             params=params, headers=headers, timeout=20)
            data = r.json()
            if data.get('code') != 0:
                try:
                    r = requests.get(WEB_BASE_ALT + '/b/api/file/list/new',
                                     params=params, headers=headers, timeout=20)
                    data = r.json()
                    if data.get('code') != 0:
                        return (None,
                                data.get('message') or ('code=%s' % data.get('code')))
                except Exception as e:
                    return (None, str(e))
            d = data.get('data') or {}
            infos = d.get('InfoList') or []
            items.extend(infos)
            total = d.get('Total') or 0
            if not infos:
                return (items, '')
            if len(items) >= total:
                return (items, '')
            page += 1
        except Exception as e2:
            return (None, data.get('message') or str(e2))
    return (items, '')


def _mkdir(token, parent_id, name, loginuuid):
    headers = base_headers(loginuuid, token)
    headers['Content-Type'] = 'application/json;charset=UTF-8'
    payload = {
        'driveId': 0,
        'etag': '',
        'fileName': name,
        'parentFileId': parent_id,
        'size': 0,
        'type': 1,
        'duplicate': 1,
        'NotReuse': True,
        'event': 'newCreateFolder',
        'operateType': 1,
    }
    last_msg = ''
    for base in (WEB_BASE, WEB_BASE_ALT):
        try:
            r = requests.post(base + '/a/api/file/upload_request',
                              headers=headers, data=json.dumps(payload),
                              timeout=20)
            data = r.json()
            if data.get('code') == 0:
                d = data.get('data') or {}
                info = d.get('Info') or {}
                return info.get('FileId') or d.get('FileId')
            last_msg = data.get('message') or ('code=%s' % data.get('code'))
        except Exception as e:
            last_msg = str(e)
    raise RuntimeError(f'创建目录失败 [{name}]: {last_msg}')


def ensure_dir_path(token, root_id, parts, dir_cache, loginuuid, log_cb):
    """逐级查找/创建目录，返回最终 FileId。dir_cache 缓存已解析目录。"""
    cur = root_id
    for name in parts:
        if not name:
            continue
        key = (cur, name)
        if key in dir_cache:
            cur = dir_cache[key]
            continue
        items, msg = file_list_dir(token, cur, loginuuid)
        if items is None:
            raise RuntimeError('读取目录失败: %s' % msg)
        found = None
        for it in items:
            if it.get('FileName') == name:
                if it.get('Type') == 1:
                    found = it.get('FileId')
                    break
        if found is None:
            found = _mkdir(token, cur, name, loginuuid)
            if log_cb:
                log_cb(f'创建目录: {name} (id={found})')
        dir_cache[key] = found
        cur = found
    return cur


def fast_upload(token, etag, filename, size, parent_id, loginuuid):
    """秒传一个文件。返回 {ok, reuse, file_id, message}
etag 自动兼容 base62(123fastlink V2) / hex / base64 格式。"""
    headers = base_headers(loginuuid, token)
    headers['Content-Type'] = 'application/json;charset=UTF-8'
    safe_name = re.sub(r'[\\/:*?|><"]', '-', filename)
    if len(safe_name) > 250:
        root, ext = os.path.splitext(safe_name)
        safe_name = root[:250 - len(ext)] + ext
    etag = normalize_etag(etag)
    payload = {
        'driveId': 0,
        'etag': etag,
        'fileName': safe_name,
        'parentFileId': parent_id,
        'size': int(size),
        'type': 0,
        'RequestSource': None,
        'duplicate': 0,
    }
    last_msg = ''
    for base in FAST_BASES:
        try:
            r = requests.post(base + '/b/api/file/upload_request',
                              headers=headers, data=json.dumps(payload),
                              timeout=30)
            data = r.json()
            if data.get('code') == 1:
                d = data.get('data') or {}
                info = d.get('Info') or {}
                return {'ok': True, 'reuse': bool(info.get('Reuse')),
                        'file_id': info.get('FileId')}
            last_msg = data.get('message') or ('code=%s' % data.get('code'))
            if data.get('code') in (401, 10006, 10002):
                continue
        except Exception as e:
            last_msg = str(e)
            time.sleep(1)
    return {'ok': False, 'reuse': False, 'message': last_msg}


def get_all_known_exts():
    exts = set()
    for v in FILE_TYPE_GROUPS.values():
        exts.update(v)
    return exts
