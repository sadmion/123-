# -*- coding: utf-8 -*-
"""影库内存测试 —— 在本地复现「追加影库崩溃」，不依赖 Docker。

用法：
    # 1) 看当前数据目录里各影库的加载内存
    python tools/mem_test.py

    # 2) 指定数据目录
    python tools/mem_test.py --dir ./data

    # 3) 模拟「追加」：先加载已有的，再逐个追加
    python tools/mem_test.py --append

    # 4) 测试拆分方案（对比大库 vs 小库）
    python tools/mem_test.py --compare ./瘦身输出

    # 5) 设定内存上限（MB），超过就报"会崩"
    python tools/mem_test.py --limit 2048

说明：
    崩溃的本质是进程内存被系统杀掉，表现为"点追加后闪退、日志无记录"。
    本脚本用 step-by-step 采样，在真正 OOM 之前就能看出趋势。
"""
import argparse
import gc
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'src'))

PID = os.getpid()


def rss_mb():
    """当前进程工作集（MB）。Windows 用 tasklist，Linux 用 /proc。"""
    if sys.platform == 'win32':
        try:
            out = subprocess.run(
                ['tasklist', '/FI', 'PID eq %d' % PID, '/FO', 'CSV', '/NH'],
                capture_output=True, text=True, timeout=10).stdout
            last = out.strip().split('","')[-1]
            return int(last.replace('"', '').replace(' K', '')
                       .replace(',', '')) / 1024
        except Exception:
            return -1.0
    try:
        with open('/proc/%d/status' % PID) as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    return int(line.split()[1]) / 1024
    except Exception:
        pass
    return -1.0


def sys_avail_mb():
    """系统可用内存（MB）。"""
    if sys.platform == 'win32':
        try:
            import ctypes

            class M(ctypes.Structure):
                _fields_ = [('dwLength', ctypes.c_ulong),
                            ('dwMemoryLoad', ctypes.c_ulong),
                            ('ullTotalPhys', ctypes.c_ulonglong),
                            ('ullAvailPhys', ctypes.c_ulonglong),
                            ('ullTotalPageFile', ctypes.c_ulonglong),
                            ('ullAvailPageFile', ctypes.c_ulonglong),
                            ('ullTotalVirtual', ctypes.c_ulonglong),
                            ('ullAvailVirtual', ctypes.c_ulonglong),
                            ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
            m = M()
            m.dwLength = ctypes.sizeof(M)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.ullAvailPhys / 1048576
        except Exception:
            pass
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                if line.startswith('MemAvailable:'):
                    return int(line.split()[1]) / 1024
    except Exception:
        pass
    return -1.0


def load_one(fp):
    """加载单个影库，返回 (Library, 耗时秒)。"""
    import library_store as L
    t0 = time.time()
    lib = L.Library(fp, tag='测试')
    lib.load()
    return lib, time.time() - t0


def fmt(mb):
    return '--' if mb < 0 else '%.1f' % mb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default=os.path.join(ROOT, 'data'))
    ap.add_argument('--append', action='store_true',
                    help='模拟追加：先加载全部已有影库，逐个追加')
    ap.add_argument('--compare', metavar='DESC_DIR',
                    help='对比：把该目录下所有 json 当成「拆分后的小库」加载')
    ap.add_argument('--limit', type=float, default=0,
                    help='内存上限(MB)，超出则判定为会崩')
    ap.add_argument('--plan', action='store_true',
                    help='粗筛预估（不加载，毫秒级）。'
                         '注意：只按体积估算，系数因字段完整度而异（实测 3~4.4），'
                         '偏保守，用于快速识别明显超标的库；'
                         '要准确判断请用 --append 实测')
    ap.add_argument('--json', action='store_true', help='输出 JSON')
    args = ap.parse_args()

    import library_store  # noqa: F401

    results = []

    def report(title, rows, base):
        print()
        print(title)
        print('%-46s %9s %11s %11s' % ('文件', '体积MB', '内存增量MB', '耗时s'))
        print('-' * 82)
        for name, size_mb, delta, dt, note in rows:
            print('%-46s %9.1f %11s %11.1f  %s'
                  % (name[:46], size_mb, fmt(delta), dt, note))
        cur = rss_mb()
        print('-' * 82)
        print('  当前进程内存: %s MB   系统可用: %s MB'
              % (fmt(cur), fmt(sys_avail_mb())))
        return cur

    # 数据目录里的影库
    imp = os.path.join(args.dir, '秒传文件导入或追加')
    if not os.path.isdir(imp):
        imp = args.dir

    files = sorted(n for n in os.listdir(imp)
                   if n.lower().endswith('.json')
                   and not n.startswith('.'))
    if not files:
        print('  在 %s 里没找到 json 影库文件' % imp)
        return 1

    print('=' * 82)
    print('影库内存测试')
    print('=' * 82)
    print('  数据目录  : %s' % imp)
    print('  影库数量  : %d' % len(files))
    print('  系统可用  : %s MB' % fmt(sys_avail_mb()))
    print('  进程起始  : %s MB' % fmt(rss_mb()))
    if args.limit:
        print('  内存上限  : %.0f MB（超出判定为会崩）' % args.limit)

    kept = []

    if args.plan:
        # 粗筛：不加载，只按体积估。系数实测在 3~4.4 之间（取决于记录里
        # 带多少可选字段），这里取 4.4 偏保守，用于快速识别明显超标的库。
        # 峰值另加一次加载峰值（待加载库之间不会叠加峰值）。
        K_RES = 4.4       # 常驻系数（偏保守）
        K_PEAK = 7.8      # 单库加载峰值系数
        print()
        print('=== 粗筛预估（不加载，偏保守）===')
        print('%-44s %9s %11s' % ('文件', '体积MB', '常驻估算MB'))
        print('-' * 68)
        sizes = []
        for n in files:
            sz = os.path.getsize(os.path.join(imp, n)) / 1048576
            sizes.append((n, sz))
            flag = '⚠' if sz * K_RES > 700 else ' '
            print('%-44s %9.1f %11.1f %s'
                  % (n[:44], sz, sz * K_RES, flag))
        print('-' * 68)
        tot_sz = sum(s for _, s in sizes)
        tot_res = tot_sz * K_RES
        biggest = max((s for _, s in sizes), default=0)
        peak_est = tot_res - biggest * K_RES + biggest * K_PEAK
        print('%-44s %9.1f %11.1f' % ('合计', tot_sz, tot_res))
        print()
        print('  常驻合计   : %.0f MB' % tot_res)
        print('  峰值估算   : %.0f MB  （常驻 + 最大单库的加载瞬时增量）'
              % peak_est)
        print('  ⚠ 体积系数因字段完整度而异（实测 3.0~4.4），此估算偏保守。')
        print('     准确判断请跑：python tools/mem_test.py --append')
        print()
        avail = sys_avail_mb()
        print('  本机可用内存: %s MB' % fmt(avail))
        if args.limit:
            print('  容器内存上限: %.0f MB' % args.limit)
            print()
            print('  提醒：目录里的库会在**启动时全部加载**'
                  '（LibraryStore.__init__ 调 scan(initial=True)），')
            print('        watcher 每 3 秒扫一次，新增文件会立即加载 ——'
                  ' 这就是「放进目录就崩」的原因。')
            print()
            ratio = peak_est / args.limit
            if ratio > 1.0:
                print('  ★ 判定：⚠⚠ 很可能崩（估算峰值 %.0f > 上限 %.0f）'
                      % (peak_est, args.limit))
                print('      建议：上限提到 %.0f MB 以上，'
                      '或用 tools/split_library.py 拆分' % (peak_est * 1.3))
            elif ratio > 0.7:
                print('  ★ 判定：⚠ 风险偏高（估算峰值占上限 %.0f%%）'
                      % (ratio * 100))
                print('      运行期再加库可能就会崩')
            else:
                print('  ★ 判定：✓ 看起来安全（估算峰值占上限 %.0f%%）'
                      % (ratio * 100))
        return 0

    if args.compare:
        # 拆分方案对比
        cdir = args.compare
        cfs = sorted(n for n in os.listdir(cdir)
                     if n.lower().endswith('.json'))
        print()
        print('=== 加载拆分后的小库（%d 个）===' % len(cfs))
        tot = sum(os.path.getsize(os.path.join(cdir, n)) for n in cfs)
        gc.collect()
        b = rss_mb()
        t0 = time.time()
        libs = []
        for n in cfs:
            lib, _ = load_one(os.path.join(cdir, n))
            libs.append(lib)
        dt = time.time() - t0
        a = rss_mb()
        rec = sum(len(l.files) for l in libs)
        print('  合计体积   : %.1f MB' % (tot / 1048576))
        print('  记录数     : %d' % rec)
        print('  加载后内存 : %s MB   (增量 %s MB)'
              % (fmt(a), fmt(a - b)))
        print('  总耗时     : %.1f s' % dt)
        verdict = '安全'
        if args.limit and a > args.limit:
            verdict = '⚠ 超限，会崩'
        print('  判定       : %s' % verdict)
        print()
        print('  结论：拆分后共 %d 个小库，常驻内存 %s MB'
              % (len(cfs), fmt(a)))
        del libs
        gc.collect()
        return 0

    rows = []
    for n in files:
        fp = os.path.join(imp, n)
        size_mb = os.path.getsize(fp) / 1048576
        gc.collect()
        b = rss_mb()
        try:
            lib, dt = load_one(fp)
        except Exception as e:
            rows.append((n, size_mb, -1, 0, '加载失败: %s' % e))
            continue
        a = rss_mb()
        rec = len(lib.files)
        note = '%d 条' % rec
        rows.append((n, size_mb, a - b, dt, note))
        if args.append:
            kept.append(lib)          # 故意保留 → 模拟追加时的内存累加
        else:
            del lib
            gc.collect()

        # 每加载一个就看一眼余量，提前预警
        avail = sys_avail_mb()
        if avail > 0 and avail < size_mb * 6:
            print('  ⚠ 加载 %s 后系统仅剩 %s MB，风险高'
                  % (n[:30], fmt(avail)))

    cur = report('=== 逐个加载（%s）===' % ('累加，不释放' if args.append else '每个加载后释放'),
                 rows, 0)

    if kept:
        print()
        print('  ★ 追加完成：%d 个影库同时常驻，进程内存 %s MB'
              % (len(kept), fmt(rss_mb())))
        if args.limit and cur > args.limit:
            print('  ★ 判定：⚠ 超过 %.0f MB 上限 —— 真实环境会被 OOM 杀掉'
                  % args.limit)
        else:
            print('  ★ 判定：未超限')

    return 0


if __name__ == '__main__':
    sys.exit(main())
