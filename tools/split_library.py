# -*- coding: utf-8 -*-
"""影库拆分工具 —— 把大影库按目录/条数拆成多个小库。

用途：降低**单次加载峰值**，避免在小内存环境（NAS/容器）加载时被 OOM 杀掉。

注意：拆分不能降低**常驻内存总量**（记录总数不变），
      要降常驻内存需要加内存或改加载实现。

用法：
    # 查看影库规模与内存预估
    python tools/split_library.py "影库.json" --info

    # 按分类目录拆，每个子库最多 5 万条
    python tools/split_library.py "影库.json" --by-dir 50000

    # 按条数顺序切块
    python tools/split_library.py "影库.json" --split 50000

    # 只留某类
    python tools/split_library.py "影库.json" --filter "电影/" --by-dir 50000

    # 预览不落盘
    python tools/split_library.py "影库.json" --by-dir 50000 --dry-run
"""
import argparse
import json
import os
import sys

OUT_DEFAULT = '瘦身输出'


def human(n):
    for u in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024:
            return '%d %s' % (n, u) if u == 'B' else '%.2f %s' % (n, u)
        n /= 1024.0
    return '%.2f PB' % n


def load_raw(path):
    """读出 (元数据 dict, files 列表)。兼容三种格式。"""
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    meta = {}
    files = []
    if isinstance(data, dict):
        if isinstance(data.get('libraries'), list):
            for lib in data['libraries']:
                cp = lib.get('commonPath') or ''
                for fe in lib.get('files') or []:
                    files.append(dict(fe, _cp=cp))
        else:
            cp = data.get('commonPath') or ''
            for fe in data.get('files') or []:
                files.append(dict(fe, _cp=cp))
            for k, v in data.items():
                if k != 'files':
                    meta[k] = v
    elif isinstance(data, list):
        for fe in data:
            files.append(dict(fe, _cp=''))
    return meta, files


def est_peak_mb(path):
    size = os.path.getsize(path)
    return size / 1048576 * 7.8


def cmd_info(path):
    meta, files = load_raw(path)
    size = os.path.getsize(path)
    print('=' * 60)
    print('影库: %s' % os.path.basename(path))
    print('=' * 60)
    print('  体积      : %s' % human(size))
    print('  记录数    : %d' % len(files))
    peak = est_peak_mb(path)
    print('  加载峰值  : ≈ %.0f MB' % peak)
    if peak > 1200:
        print('  ⚠ 峰值较高，小内存环境（<2GB）导入时会崩，建议拆分')
    elif peak > 700:
        print('  ⚠ 峰值偏高，建议容器给足 2GB 以上内存')
    else:
        print('  ✓ 峰值安全')
    print()
    # 顶级分组分布
    dist = {}
    for fe in files:
        p = (fe.get('path') or '').replace('\\', '/').lstrip('/')
        top = p.split('/')[0] if '/' in p else '(根目录)'
        dist[top] = dist.get(top, 0) + 1
    print('  顶级分组（前 15）:')
    for k, v in sorted(dist.items(), key=lambda x: -x[1])[:15]:
        print('    %-24s %8d 条' % (k[:24], v))
    return 0


def split(path, out_dir, by_dir=0, by_count=0, filt='', dry=False):
    meta, files = load_raw(path)
    name0 = os.path.basename(path)
    for suf in ('.123fastlink.json', '.json'):
        if name0.endswith(suf):
            name0 = name0[:-len(suf)]
            break

    if filt:
        files = [f for f in files
                 if (f.get('path') or '').replace('\\', '/').lstrip('/')
                 .startswith(filt)]
        print('  过滤 "%s" 后剩 %d 条' % (filt, len(files)))

    # 分组
    groups = {}
    if by_dir:
        for fe in files:
            p = (fe.get('path') or '').replace('\\', '/').lstrip('/')
            top = p.split('/')[0] if '/' in p else '(根目录)'
            groups.setdefault(top, []).append(fe)
        # 超限的组再按条数切块
        final = {}
        for gname, items in groups.items():
            if len(items) <= by_dir:
                final['%s' % gname] = items
            else:
                for i in range(0, len(items), by_dir):
                    final['%s_part%02d' % (gname, i // by_dir + 1)] = \
                        items[i:i + by_dir]
        groups = final
    elif by_count:
        for i in range(0, len(files), by_count):
            groups['part%02d' % (i // by_count + 1)] = files[i:i + by_count]
    else:
        groups['all'] = files

    if not dry:
        os.makedirs(out_dir, exist_ok=True)

    print('=' * 66)
    print('拆分为 %d 个子库' % len(groups))
    print('=' * 66)
    total = 0
    for gname, items in sorted(groups.items()):
        safe = gname.replace('/', '_').replace('\\', '_')[:60]
        fn = '%s_%s.123fastlink.json' % (name0, safe)
        body = {
            'scriptVersion': meta.get('scriptVersion', '3.2.0'),
            'exportVersion': meta.get('exportVersion', '1.0'),
            'usesBase62EtagsInExport': meta.get('usesBase62EtagsInExport', True),
            'commonPath': (items[0].get('_cp') if items else '') or '',
            'totalFilesCount': len(items),
            'files': [{k: v for k, v in fe.items() if k != '_cp'}
                      for fe in items],
        }
        txt = json.dumps(body, ensure_ascii=False)
        nbytes = len(txt.encode('utf-8'))
        total += nbytes
        peak = nbytes / 1048576 * 7.8
        flag = '⚠' if peak > 700 else '✓'
        print('  %s %-46s %7d 条  %8s  峰值≈%4.0f MB'
              % (flag, fn[:46], len(items), human(nbytes), peak))
        if not dry:
            with open(os.path.join(out_dir, fn), 'w', encoding='utf-8') as f:
                f.write(txt)
    print('-' * 66)
    print('  合计 %d 条 / %s' % (len(files), human(total)))
    if dry:
        print('  （--dry-run 预览，未写入文件）')
    else:
        print('  已写入: %s' % os.path.abspath(out_dir))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path', help='影库 JSON 路径')
    ap.add_argument('--info', action='store_true', help='只看规模与预估')
    ap.add_argument('--by-dir', type=int, default=0, metavar='N',
                    help='按分类目录拆，每库最多 N 条')
    ap.add_argument('--split', type=int, default=0, metavar='N',
                    help='按条数顺序切块，每块 N 条')
    ap.add_argument('--filter', default='', help='只保留此前缀的路径')
    ap.add_argument('-o', '--out', default=OUT_DEFAULT, help='输出目录')
    ap.add_argument('--dry-run', action='store_true', help='只预览不写文件')
    args = ap.parse_args()

    if not os.path.isfile(args.path):
        print('找不到文件: %s' % args.path)
        return 2
    if args.info:
        return cmd_info(args.path)
    if not args.by_dir and not args.split:
        print('请指定 --by-dir N 或 --split N（或 --info 查看规模）')
        return 2
    return split(args.path, args.out, args.by_dir, args.split,
                 args.filter, args.dry_run)


if __name__ == '__main__':
    sys.exit(main())
