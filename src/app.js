/* 123云盘影库搜索工具（复刻版）— 前端逻辑 */
"use strict";
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));

async function api(path, opts) {
  const r = await fetch(path, opts);
  let j;
  try { j = await r.json(); } catch (e) { j = {}; }
  // 服务器 500 等返回 {error}, 统一透出到 message 以便 toast 显示具体原因
  if (j.error && !j.message) j.message = j.error;
  if (!r.ok && j.ok === undefined) j.ok = false;
  return j;
}
async function post(path, data) {
  return api(path, { method: "POST", headers: { "Content-Type": "application/json" },
                     body: JSON.stringify(data || {}) });
}
function fmtSize(n) {
  if (n == null || isNaN(n)) return "-";
  n = Number(n);
  const u = ["B","KB","MB","GB","TB","PB"]; let i = 0;
  while (n >= 1024 && i < u.length - 1) { n /= 1024; i++; }
  return (i === 0 ? n.toFixed(0) : n.toFixed(2)) + " " + u[i];
}
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g,
    c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
function toast(msg, ok) {
  let t = $("#toast");
  if (!t) {
    t = document.createElement("div"); t.id = "toast";
    t.style.cssText = "position:fixed;top:66px;left:50%;transform:translateX(-50%);z-index:999;padding:9px 20px;border-radius:8px;font-size:13px;box-shadow:0 6px 20px rgba(15,23,42,.2);background:#1e293b;color:#fff;transition:opacity .3s;opacity:0;pointer-events:none";
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.background = ok === false ? "#ef4444" : (ok === true ? "#059669" : "#1e293b");
  t.style.opacity = "1";
  clearTimeout(t._h);
  t._h = setTimeout(() => (t.style.opacity = "0"), 2600);
}

/* ══════════════ 全局状态 ══════════════ */
const S = {
  libs: [], selLibs: JSON.parse(localStorage.getItem("selLibs") || "null"),
  cats: [], cat1: "", cat2: "", year: "",
  page: 1, pageSize: 20, total: 0,
  multiMode: false, multiSel: [],
  lastSearch: { kw: "", cat1: "", cat2: "" },
  ver: -1, retry: 0,
  ftSel: null,
  browse: { shareKey: "", pwd: "", dir: 0, sel: new Map(), stack: [] },
};

/* ══════════════ 影库 ══════════════ */
async function loadLibs(silent) {
  const r = await api("/api/libs");
  S.libs = r.libs || [];
  if (r.errors && r.errors.length && !silent) toast(r.errors[r.errors.length - 1], false);
  const valid = new Set(S.libs.map(l => l.id));
  if (!S.selLibs) S.selLibs = S.libs.map(l => l.id);
  else S.selLibs = S.selLibs.filter(id => valid.has(id));
  renderLibDropdown();
  const totalF = S.libs.reduce((a, l) => a + l.fileCount, 0);
  const totalS = S.libs.reduce((a, l) => a + l.size, 0);
  $("#libSummary").textContent = S.libs.length ?
    "已加载 " + S.libs.length + " 个影库 · " + totalF.toLocaleString() + " 个文件 · " + fmtSize(totalS) :
    "尚未加载影库";
  if (!silent) { await loadCategories(); }
  return S.libs;
}
function renderLibDropdown() {
  const dd = $("#libDropdown");
  dd.innerHTML = S.libs.length ? S.libs.map(l => `
    <div class="li" data-id="${l.id}">
      <input type="checkbox" ${S.selLibs.includes(l.id) ? "checked" : ""}>
      <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(l.name)}</span>
      <span class="tag ${l.tag === "原库" ? "blue" : "orange"}">${l.tag === "原库" ? "原库" : "追加·" + esc(l.importDate || "")}</span>
      <span class="muted">${l.fileCount.toLocaleString()}</span>
    </div>`).join("") : '<div class="li muted">暂无影库</div>';
  $$("#libDropdown .li").forEach(li => {
    li.onclick = (e) => {
      if (e.target.tagName === "INPUT" && !S.libs.length) return;
      const id = +li.dataset.id;
      const i = S.selLibs.indexOf(id);
      if (i >= 0) S.selLibs.splice(i, 1); else S.selLibs.push(id);
      localStorage.setItem("selLibs", JSON.stringify(S.selLibs));
      renderLibDropdown();
      refreshAll();
    };
  });
  $("#libSelCount").textContent = S.selLibs.length ? "(" + S.selLibs.length + ")" : "";
}
$("#btnLibDrop").onclick = (e) => { e.stopPropagation(); $("#libDropdown").classList.toggle("open"); };
document.addEventListener("click", (e) => {
  if (!e.target.closest(".lib-select")) $("#libDropdown").classList.remove("open");
});

/* ══════════════ 分类 ══════════════ */
async function loadCategories() {
  const qs = S.selLibs.length ? "?libs=" + S.selLibs.join(",") : "";
  const r = await api("/api/categories" + qs);
  S.cats = r.categories || [];
  renderCats();
  renderStorage();
  renderCatOptions();
  if (!S.cats.length && S.retry < 6) {   // 大文件加载中, 自动重试
    S.retry++;
    setTimeout(loadCategories, 1500 + S.retry * 500);
  } else S.retry = 0;
}
function catTag(c, level, checked, active) {
  const dl = level === 1 && !S.multiMode ?
    '<span class="dl" data-dl1="' + esc(c.name) + '" title="导出该分类秒传">⬇</span>' : "";
  const chk = S.multiMode ?
    '<input type="checkbox" style="accent-color:#2563eb" ' + (checked ? "checked" : "") + ">" : "";
  return '<span class="cat-tag ' + (checked ? "checked " : "") + (active ? "active" : "") +
    '" data-lv="' + level + '" data-name="' + esc(c.name) +
    '" title="' + esc(c.name) + " · " + c.works + ' 部作品 · ' + fmtSize(c.size) + '">' +
    chk + esc(c.name) + '<span class="cnt">' + c.works + "部·" + fmtSize(c.size) + "</span>" + dl + "</span>";
}
function renderCats() {
  const box = $("#catLines");
  if (!S.cats.length) { box.innerHTML = '<span class="muted" style="padding:8px">暂无分类</span>'; updateFold(); return; }
  let html = "";
  for (const c of S.cats) {
    const checked = S.multiSel.some(m => m.cat1 === c.name);
    html += catTag(c, 1, checked, S.cat1 === c.name && !S.multiMode);
  }
  box.innerHTML = html;
  bindCatTags();
  updateFold();
}
function bindCatTags() {
  $$("#catLines .cat-tag").forEach(tag => {
    tag.onclick = (e) => {
      if (e.target.classList.contains("dl")) {
        exportCategory(e.target.dataset.dl1, ""); e.stopPropagation(); return;
      }
      const name = tag.dataset.name;
      if (S.multiMode) {
        const i = S.multiSel.findIndex(m => m.cat1 === name);
        if (i >= 0) S.multiSel.splice(i, 1); else S.multiSel.push({ cat1: name });
        renderCats(); renderMultiBar(); return;
      }
      if (S.cat1 === name) { S.cat1 = ""; S.cat2 = ""; }
      else { S.cat1 = name; S.cat2 = ""; }
      S.year = ""; S.page = 1;
      renderCats(); renderSubcats(); doSearch();
    };
  });
}
function renderSubcats() {
  const zone = $("#subcatZone");
  const c = S.cats.find(x => x.name === S.cat1);
  if (!c || !c.children || !c.children.length) { zone.classList.remove("show"); return; }
  zone.classList.add("show");
  zone.innerHTML = '<div class="muted" style="margin-bottom:5px">' + esc(c.name) + " 的子分类（点击筛选）：</div>" +
    '<div class="cat-lines">' + c.children.map(cc =>
      '<span class="cat-tag ' + (S.cat2 === cc.name ? "active" : "") + '" data-name="' + esc(cc.name) + '">' +
      esc(cc.name) + '<span class="cnt">' + cc.works + "部</span></span>").join("") + "</div>";
  $$("#subcatZone .cat-tag").forEach(tag => {
    tag.onclick = () => {
      S.cat2 = S.cat2 === tag.dataset.name ? "" : tag.dataset.name;
      S.year = ""; S.page = 1;
      renderSubcats(); doSearch();
    };
  });
}
function updateFold() {
  const wrap = $("#catWrap"), btn = $("#btnExpandMore");
  if (!wrap) return;
  const lines = $("#catLines").getBoundingClientRect().height;
  if (lines > 200) { wrap.classList.add("folded"); btn.classList.add("show"); }
  else { btn.classList.remove("show"); wrap.classList.remove("folded"); }
}
$("#btnExpandMore").onclick = () => {
  const wrap = $("#catWrap");
  wrap.classList.toggle("expanded");
  $("#btnExpandMore").textContent = wrap.classList.contains("expanded") ? "收起 ▴" : "展开更多 ▾";
};
$("#btnSubcat").onclick = () => {
  const zone = $("#subcatZone");
  if (S.cat2) { S.cat2 = ""; renderSubcats(); doSearch(); }
  else if (zone.classList.contains("show") && S.cat1) { /* 已显示 */ }
  else if (S.cat1) renderSubcats();
  else toast("请先选择一个一级分类");
};
/* 合并导出多选 */
$("#btnMulti").onclick = () => {
  S.multiMode = !S.multiMode;
  if (S.multiMode) { S.multiSel = []; S.cat1 = ""; S.cat2 = ""; }
  $("#btnMulti").textContent = S.multiMode ? "☑ 退出多选" : "☑ 合并导出";
  $("#multiBar").style.display = S.multiMode ? "flex" : "none";
  renderCats(); renderMultiBar();
};
function renderMultiBar() { $("#multiCount").textContent = "已选 " + S.multiSel.length + " 个分类"; }
$("#btnMultiClear").onclick = () => { S.multiSel = []; renderCats(); renderMultiBar(); };
$("#btnMultiExit").onclick = () => $("#btnMulti").onclick();
$("#btnMergeGo").onclick = async () => {
  if (!S.multiSel.length) return toast("请先勾选分类", false);
  toast("合并导出中…");
  const r = await post("/api/export/merge", { cats: S.multiSel, libIds: S.selLibs });
  toast(r.message || (r.ok ? "导出成功" : "导出失败"), r.ok);
};

/* ══════════════ 搜索与结果 ══════════════ */
async function doSearch() {
  const kw = $("#searchInput").value.trim();
  if (kw && kw.length < 2) return toast("关键词至少 2 个字", false);
  const qs = new URLSearchParams({
    keyword: kw, cat1: S.cat1, cat2: S.cat2, page: S.page, pageSize: S.pageSize,
  });
  if (S.selLibs.length) qs.set("libs", S.selLibs.join(","));
  const r = await api("/api/search?" + qs);
  S.total = r.total;
  S.lastSearch = { kw: kw, cat1: S.cat1, cat2: S.cat2 };
  renderResults(r);
  if (kw || S.cat1 || S.cat2) {
    post("/api/history/add", { keyword: kw, cat1: S.cat1, cat2: S.cat2, results: r.total });
    loadHistory();
  }
}
function renderResults(r) {
  const list = $("#workList"), meta = $("#resultMeta");
  const ls = S.lastSearch;
  const mode = ls.kw && (ls.cat1 || ls.cat2) ? "混合搜索" :
    ls.kw ? "片名搜索" : (ls.cat1 ? "分类浏览" : "全部作品");
  meta.innerHTML = '<span class="tag blue">' + mode + "</span> 共 <b>" +
    r.total.toLocaleString() + "</b> 部作品";
  $("#emptyTip").style.display = r.total ? "none" : "block";
  $("#emptyText").textContent = r.total ? "" :
    (S.libs.length ? "没有找到匹配的作品" : "请将 *.json 放入「秒传文件导入或追加/」目录");
  const yf = $("#yearFilter");
  if (!ls.kw && ls.cat1 && r.works.length) {
    const years = [...new Set(r.works.map(w => w.year).filter(Boolean))].sort().reverse();
    yf.innerHTML = years.map(y =>
      '<span class="year-tag ' + (S.year === y ? "active" : "") + '" data-y="' + y + '">' + y + "</span>").join("");
    $$("#yearFilter .year-tag").forEach(t => t.onclick = () => {
      S.year = S.year === t.dataset.y ? "" : t.dataset.y;
      $$("#yearFilter .year-tag").forEach(x => x.classList.toggle("active", x.dataset.y === S.year));
      list.innerHTML = r.works.filter(w => !S.year || w.year === S.year).map(workCard).join("");
      bindWorkCards(r.works.filter(w => !S.year || w.year === S.year));
    });
  } else yf.innerHTML = "";
  const works = r.works;
  list.innerHTML = works.map(workCard).join("");
  bindWorkCards(works);
  renderPager(r);
}
function workCard(w, idx) {
  return '<div class="work-card" data-idx="' + idx + '">' +
    '<div class="poster" data-title="' + esc(w.title) + '" data-year="' + (w.year || "") + '">🎞️</div>' +
    '<div class="work-main">' +
    '<div class="work-title" title="' + esc(w.title) + '">' + esc(w.title) + "</div>" +
    '<div class="work-meta"><span>📅 ' + (w.year || "未知") + "</span>" +
    "<span>🎬 " + w.videoCount + " 个视频</span><span>📄 " + w.fileCount + " 个文件</span>" +
    "<span>💾 " + fmtSize(w.size) + "</span>" +
    (w.libName ? '<span class="tag blue">' + esc(w.libName) + "</span>" : "") +
    (w.cat1 && w.cat1 !== "全部文件" ?
      '<span class="tag" style="background:#ede9fe;color:#6d28d9">' + esc(w.cat1) + (w.cat2 ? "/" + esc(w.cat2) : "") + "</span>" : "") +
    "</div>" +
    '<div class="work-ops"><button class="btn sm" data-act="expand">展开文件</button>' +
    '<button class="btn sm" data-act="expdir">导出目录</button></div>' +
    '<div class="file-list"></div></div></div>';
}
function bindWorkCards(works) {
  const q = $$("#workList .poster").slice();
  const loadOne = () => {
    if (!q.length) return;
    const el = q.shift();
    api("/api/tmdb?title=" + encodeURIComponent(el.dataset.title) + "&year=" + encodeURIComponent(el.dataset.year))
      .then(r => { if (r && r.poster) el.innerHTML = '<img src="' + r.poster + '" loading="lazy">'; })
      .catch(() => {}).finally(loadOne);
  };
  loadOne(); loadOne(); loadOne();
  $$("#workList .work-card").forEach((card) => {
    const w = works[+card.dataset.idx];
    if (!w) return;
    card.querySelector(".work-title").onclick = () => toggleFiles(card, w);
    card.querySelector('[data-act="expand"]').onclick = () => toggleFiles(card, w);
    card.querySelector('[data-act="expdir"]').onclick = async (e) => {
      const btn = e.target;
      btn.disabled = true; btn.textContent = "导出中…";
      const r = await post("/api/export/dir", { libId: w.libId, dirName: w.dirName, parentPath: w.parentPath });
      toast(r.message || "导出失败", r.ok);
      if (r.ok) btn.textContent = "已导出 " + r.file.count + " 个 ✓";
      else { btn.disabled = false; btn.textContent = "导出目录"; }
    };
  });
}
async function toggleFiles(card, w) {
  const fl = card.querySelector(".file-list");
  if (fl.classList.contains("open")) { fl.classList.remove("open"); return; }
  if (!fl.dataset.loaded) {
    fl.innerHTML = '<div class="muted" style="padding:8px">加载中…</div>';
    const r = await post("/api/work/files", { libId: w.libId, dirName: w.dirName, parentPath: w.parentPath });
    if (r.error) { fl.innerHTML = '<div class="err-text" style="padding:8px">' + esc(r.error) + "</div>"; fl.classList.add("open"); return; }
    renderFileList(fl, w, r);
    fl.dataset.loaded = "1";
  }
  fl.classList.add("open");
}
function renderFileList(fl, w, r) {
  const versions = r.versions || [];
  const all = r.files;
  const selected = new Set();
  let curVer = "全部";
  const head = versions.length ?
    '<div class="ver-tabs"><span class="ver-tab active" data-v="全部">全部(' + all.length + ")</span>" +
    versions.map(v => '<span class="ver-tab" data-v="' + esc(v.label) + '">' + esc(v.label) + "(" + v.count + ")</span>").join("") + "</div>" : "";
  const ops = '<div class="row" style="margin-bottom:7px;flex-wrap:wrap">' +
    '<button class="btn sm" data-a="all">全选</button>' +
    '<button class="btn sm" data-a="verall">全选当前版本</button>' +
    '<button class="btn sm" data-a="none">取消全选</button>' +
    '<button class="btn sm primary" data-a="export" disabled>导出选中 (<span id="selN">0</span>)</button></div>';
  fl.innerHTML = head + ops + '<div class="file-rows"></div>';
  const rows = fl.querySelector(".file-rows");
  const filesOf = () => curVer === "全部" ? all :
    all.filter(f => { const v = versions.find(x => x.label === curVer); return v && v.names.includes(f.path.split("/").pop()); });
  const upd = () => {
    fl.querySelector("#selN").textContent = selected.size;
    fl.querySelector('[data-a="export"]').disabled = !selected.size;
  };
  const draw = () => {
    const files = filesOf();
    rows.innerHTML = files.map(f => {
      const nm = f.path.split("/").pop();
      return '<div class="file-row" data-p="' + esc(f.path) + '">' +
        '<input type="checkbox" ' + (selected.has(f.path) ? "checked" : "") + ' style="accent-color:#2563eb">' +
        '<span class="fname" title="' + esc(f.path) + '">' + esc(nm) + "</span>" +
        '<span class="fsize">' + fmtSize(f.size) + "</span></div>";
    }).join("");
    rows.querySelectorAll(".file-row").forEach(row => {
      row.onclick = (e) => {
        const cb = row.querySelector("input");
        if (e.target !== cb) cb.checked = !cb.checked;
        const p = row.dataset.p;
        if (cb.checked) selected.add(p); else selected.delete(p);
        upd();
      };
    });
  };
  fl.querySelectorAll(".ver-tab").forEach(t => t.onclick = () => {
    curVer = t.dataset.v;
    fl.querySelectorAll(".ver-tab").forEach(x => x.classList.toggle("active", x === t));
    draw();
  });
  fl.querySelector('[data-a="all"]').onclick = () => { all.forEach(f => selected.add(f.path)); draw(); upd(); };
  fl.querySelector('[data-a="none"]').onclick = () => { selected.clear(); draw(); upd(); };
  fl.querySelector('[data-a="verall"]').onclick = () => { filesOf().forEach(f => selected.add(f.path)); draw(); upd(); };
  fl.querySelector('[data-a="export"]').onclick = async () => {
    toast("导出选中文件中…");
    const rr = await post("/api/export/selected", {
      libId: w.libId, dirName: w.dirName, parentPath: w.parentPath, paths: [...selected] });
    toast(rr.message || "导出失败", rr.ok);
  };
  draw();
}
function renderPager(r) {
  const pg = $("#pager");
  const pages = Math.ceil(r.total / r.pageSize) || 1;
  if (pages <= 1 && r.total <= 20) { pg.innerHTML = ""; return; }
  pg.innerHTML = '<button class="btn sm" id="pgPrev" ' + (r.page <= 1 ? "disabled" : "") + ">◀ 上一页</button>" +
    '<span class="pg-info">第 ' + r.page + " / " + pages + " 页</span>" +
    '<button class="btn sm" id="pgNext" ' + (r.page >= pages ? "disabled" : "") + ">下一页 ▶</button>" +
    '<select class="input" id="pgSize" style="width:auto;padding:4px 8px">' +
    [20, 50, 100].map(n => '<option ' + (n === r.pageSize ? "selected" : "") + ">" + n + "</option>").join("") +
    '</select><span class="pg-info">条/页</span>';
  $("#pgPrev").onclick = () => { S.page--; doSearch(); };
  $("#pgNext").onclick = () => { S.page++; doSearch(); };
  $("#pgSize").onchange = (e) => { S.pageSize = +e.target.value; S.page = 1; doSearch(); };
}
$("#btnSearch").onclick = () => { S.page = 1; S.cat1 = ""; S.cat2 = ""; S.year = ""; renderCats(); doSearch(); };
$("#searchInput").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#btnSearch").onclick(); });
async function exportCategory(cat1, cat2) {
  toast("导出分类中（大分类需要十几秒）…");
  const r = await post("/api/export/category", { cat1: cat1, cat2: cat2, libIds: S.selLibs });
  toast(r.message || "导出失败", r.ok);
}

/* ══════════════ 存储分析图表 ══════════════ */
const PALETTE = ["#2563eb","#7c3aed","#10b981","#f59e0b","#ef4444","#06b6d4","#8b5cf6","#f97316","#14b8a6","#ec4899","#84cc16","#64748b"];
let donutSegs = [], hlIdx = -1;
function renderStorage() {
  const cats = S.cats.filter(c => c.size > 0).slice(0, 12);
  if (!cats.length) {
    $("#donutLegend").innerHTML = '<div class="muted">暂无数据</div>';
    $("#barChart").innerHTML = "";
    const ctx = $("#donut").getContext("2d");
    ctx.clearRect(0, 0, 190, 190);
    return;
  }
  const total = cats.reduce((a, c) => a + c.size, 0) || 1;
  donutSegs = cats.map((c, i) => ({ name: c.name, size: c.size, color: PALETTE[i % PALETTE.length], pct: c.size / total * 100 }));
  drawDonut();
  $("#donutLegend").innerHTML = donutSegs.map((c, i) =>
    '<div class="lg" data-i="' + i + '"><span class="dot" style="background:' + c.color + '"></span>' +
    '<span class="nm">' + esc(c.name) + '</span><span class="pv">' + c.pct.toFixed(1) + "%</span></div>").join("");
  const max = Math.max(...cats.map(c => c.size), 1);
  $("#barChart").innerHTML = cats.map((c, i) =>
    '<div class="brow" data-i="' + i + '"><span class="bnm" title="' + esc(c.name) + '">' + esc(c.name) + "</span>" +
    '<div class="btrack"><div class="bfill" style="background:' + c.color + '" data-w="' + (c.size / max * 100).toFixed(1) + '"></div></div>' +
    '<span class="bpv">' + fmtSize(c.size) + "</span></div>").join("");
  setTimeout(() => $$("#barChart .bfill").forEach(b => b.style.width = b.dataset.w + "%"), 60);
  $$("#donutLegend .lg, #barChart .brow").forEach(el => {
    el.onmouseenter = () => { hlIdx = +el.dataset.i; drawDonut(); syncHL(true); };
    el.onmouseleave = () => { hlIdx = -1; drawDonut(); syncHL(false); };
  });
}
function syncHL(on) {
  $$("#donutLegend .lg").forEach(el => el.classList.toggle("hl", on && +el.dataset.i === hlIdx));
  $$("#barChart .brow").forEach(el => el.classList.toggle("hl", on && +el.dataset.i === hlIdx));
}
function drawDonut() {
  const cv = $("#donut"), ctx = cv.getContext("2d");
  const cx = 95, cy = 95, R = 80, r = 54;
  ctx.clearRect(0, 0, cv.width, cv.height);
  const total = donutSegs.reduce((a, s) => a + s.size, 0) || 1;
  let a0 = -Math.PI / 2;
  for (const seg of donutSegs) {
    const a1 = a0 + (seg.size / total) * Math.PI * 2;
    const hl = donutSegs[hlIdx] === seg;
    if (a1 > a0) {
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a0) * R, cy + Math.sin(a0) * R);
      ctx.arc(cx, cy, R, a0, a1);
      ctx.arc(cx, cy, r, a1, a0, true);
      ctx.closePath();
      ctx.fillStyle = seg.color;
      ctx.globalAlpha = hl ? 1 : (hlIdx >= 0 ? .35 : .92);
      ctx.fill();
      if (seg.pct >= 0.7 && (a1 - a0) / (Math.PI * 2) > 0.02) {
        const mid = (a0 + a1) / 2;
        ctx.save(); ctx.globalAlpha = 1; ctx.fillStyle = "#fff";
        ctx.font = "600 10px 'Microsoft YaHei UI'";
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(seg.pct.toFixed(0) + "%", cx + Math.cos(mid) * (R + r) / 2, cy + Math.sin(mid) * (R + r) / 2);
        ctx.restore();
      }
    }
    a0 = a1;
  }
  ctx.globalAlpha = 1;
  ctx.fillStyle = "#1e293b"; ctx.textAlign = "center";
  ctx.font = "800 14px 'Microsoft YaHei UI'";
  ctx.fillText(fmtSize(donutSegs.reduce((a, s) => a + s.size, 0)), cx, cy - 6);
  ctx.font = "11px 'Microsoft YaHei UI'"; ctx.fillStyle = "#64748b";
  ctx.fillText(S.total ? "共 " + S.total.toLocaleString() + " 部作品" : donutSegs.length + " 个分类", cx, cy + 14);
}

/* ══════════════ 搜索历史 ══════════════ */
async function loadHistory() {
  const r = await api("/api/history");
  const box = $("#histList");
  box.innerHTML = (r.history || []).map(h =>
    '<div class="hitem" data-kw="' + esc(h.keyword) + '" data-c1="' + esc(h.cat1) + '" data-c2="' + esc(h.cat2) + '">' +
    "<span>🔍</span><span class=\"hk\">" + esc(h.keyword || h.cat1 || "—") + (h.cat2 ? "/" + esc(h.cat2) : "") +
    '</span><span class="hn">' + h.results + "条</span></div>").join("") ||
    '<div class="muted" style="padding:6px">暂无历史</div>';
  $$("#histList .hitem").forEach(el => el.onclick = () => {
    $("#searchInput").value = el.dataset.kw;
    S.cat1 = el.dataset.c1; S.cat2 = el.dataset.c2; S.page = 1;
    renderCats(); renderSubcats(); doSearch();
  });
}
$("#btnHistClear").onclick = async () => { await post("/api/history/clear"); loadHistory(); toast("已清空历史"); };

/* ══════════════ 分类下拉(提取入库用) ══════════════ */
function renderCatOptions() {
  const s1 = $("#shareCat1");
  const cur = s1.value;
  s1.innerHTML = '<option value="">保持原结构</option>' +
    S.cats.filter(c => c.name !== "全部文件").slice(0, 60)
      .map(c => '<option value="' + esc(c.name) + '">' + esc(c.name) + "</option>").join("");
  s1.value = cur;
  $("#shareCat1").onchange();
}
$("#shareCat1").onchange = () => {
  const c = S.cats.find(x => x.name === $("#shareCat1").value);
  $("#shareCat2").innerHTML = '<option value="">无</option>' +
    (c ? c.children.map(cc => '<option value="' + esc(cc.name) + '">' + esc(cc.name) + "</option>").join("") : "");
};

/* ══════════════ 分享提取 ══════════════ */
function getShareParsed() {
  const link = $("#shareLink").value.trim();
  if (!link) { toast("请先粘贴分享链接", false); return null; }
  return { link: link };
}
$("#btnExtract").onclick = async () => {
  const p = getShareParsed(); if (!p) return;
  const body = Object.assign(p, {
    title: $("#shareTitle").value.trim(),
    cat1: $("#shareCat1").value, cat2: $("#shareCat2").value,
    fileTypes: S.ftSel,
  });
  const r = await post("/api/extract/start", body);
  if (!r.ok) return toast(r.message || "启动失败", false);
  toast("提取任务已启动");
  $("#extractProgress").classList.add("show");
  pollExtract();
};
$("#btnExtractStop").onclick = () => post("/api/extract/stop");
async function pollExtract() {
  const r = await api("/api/extract/progress");
  $("#extractStep").textContent = r.step || "";
  const total = Math.max(r.scanned || 0, 1);
  $("#extractBar").style.width = r.done ? "100%" : Math.min(95, ((r.found || 0) / total * 100 + 20)).toFixed(0) + "%";
  $("#extractNums").textContent = "已扫描 " + (r.scanned || 0).toLocaleString() +
    " · 跳过 " + (r.skipped || 0).toLocaleString() +
    " · 提取 " + (r.found || 0).toLocaleString() + " 个" +
    (r.checkpoint ? " · 断点续传" : "");
  if (r.running) setTimeout(pollExtract, 1200);
  else if (r.done) {
    toast(r.message || "提取结束", r.ok);
    $("#extractStep").textContent = r.message || "";
    $("#extractBar").style.width = r.ok ? "100%" : "0%";
    setTimeout(() => $("#extractProgress").classList.remove("show"), 4000);
    await loadLibs();
  }
}
/* 文件类型过滤弹窗 */
function openFtModal() {
  api("/api/file-types").then(r => {
    const grid = $("#ftGrid");
    grid.innerHTML = Object.keys(r.groups).map(g =>
      '<span class="ft-item ' + (S.ftSel === null || S.ftSel.includes(g) ? "on" : "") + '" data-g="' + g + '">' +
      '<input type="checkbox" style="accent-color:#2563eb" ' +
      (S.ftSel === null || S.ftSel.includes(g) ? "checked" : "") + ">" + g + "</span>").join("");
    grid.querySelectorAll(".ft-item").forEach(el => el.onclick = (e) => {
      if (e.target !== el.querySelector("input")) {
        const cb = el.querySelector("input"); cb.checked = !cb.checked;
      }
      el.classList.toggle("on", el.querySelector("input").checked);
    });
    $("#ftMask").classList.add("open");
    $("#ftMask")._cb = null;
  });
}
$("#btnFtVideo").onclick = () => {
  $$("#ftGrid .ft-item").forEach(el => {
    const on = el.dataset.g === "视频";
    el.querySelector("input").checked = on; el.classList.toggle("on", on);
  });
};
$("#btnFtAll").onclick = () => $$("#ftGrid .ft-item").forEach(el => {
  el.querySelector("input").checked = true; el.classList.add("on");
});
$("#btnFtNone").onclick = () => $$("#ftGrid .ft-item").forEach(el => {
  el.querySelector("input").checked = false; el.classList.remove("on");
});
$("#btnFtOk").onclick = () => {
  const sel = $$("#ftGrid .ft-item").filter(el => el.querySelector("input").checked).map(el => el.dataset.g);
  S.ftSel = sel.length === Object.keys((window._ftGroups || {})).length ? null : sel;
  $("#ftMask").classList.remove("open");
  toast("类型过滤已保存: " + (S.ftSel ? S.ftSel.join("/") : "全部类型"));
};
$$(".modal-close").forEach(b => b.onclick = () => $("#" + b.dataset.close).classList.remove("open"));
$$(".modal-mask").forEach(m => m.onclick = (e) => { if (e.target === m) m.classList.remove("open"); });

/* 浏览分享（目录树选择提取） */
$("#btnBrowseShare").onclick = async () => {
  const p = getShareParsed(); if (!p) return;
  toast("解析分享链接…");
  const r = await post("/api/extract/parse", p);
  if (!r.ok) return toast(r.message || "解析失败", false);
  S.browse = { shareKey: r.shareKey, pwd: r.pwd, dir: 0, sel: new Map(), stack: [] };
  S.browse.rootName = (r.items && r.items.length && r.items[0].isDir) ? "" : "根目录";
  $("#browseMask").classList.add("open");
  showBrowseDir(0, []);
};
async function showBrowseDir(fid, stack) {
  S.browse.dir = fid; S.browse.stack = stack || [];
  $("#crumb").innerHTML = '<a data-d="0">根目录</a>' +
    (S.browse.stack || []).map((nm, i) =>
      ' <span>/</span> <a data-d="' + (i >= 0 ? "s" + i : "") + '" data-si="' + i + '">' + esc(nm) + "</a>").join("");
  $$("#crumb a").forEach(a => a.onclick = () => {
    const si = a.dataset.si;
    if (si === undefined) showBrowseDir(0, []);
    else showBrowseDir(S.browse.stackIds[+si], S.browse.stack.slice(0, +si + 1));
  });
  $("#browseList").innerHTML = '<div class="muted" style="padding:10px">加载中…</div>';
  const r = await post("/api/extract/list", { shareKey: S.browse.shareKey, pwd: S.browse.pwd, parentFileId: fid });
  if (!r.ok) { $("#browseList").innerHTML = '<div class="err-text" style="padding:10px">' + esc(r.message) + "</div>"; return; }
  window._browseItems = r.items;
  const selAll = r.items.length && r.items.every(it => S.browse.sel.has(it.fileId));
  $("#browseList").innerHTML = r.items.map(it => {
    const checked = S.browse.sel.has(it.fileId);
    return '<div class="browse-row" data-fid="' + it.fileId + '">' +
      '<input type="checkbox" ' + (checked ? "checked" : "") + ' style="accent-color:#2563eb">' +
      (it.isDir ? '<span class="barr">▸</span>' : "<span>📄</span>") +
      '<span class="bname" title="' + esc(it.name) + '">' + esc(it.name) + "</span>" +
      '<span class="bsize">' + (it.isDir ? "文件夹" : fmtSize(it.size)) + "</span></div>";
  }).join("");
  updateBrowseStat();
  $("#browseList").querySelectorAll(".browse-row").forEach(row => {
    row.onclick = (e) => {
      const it = window._browseItems.find(x => String(x.fileId) === row.dataset.fid);
      const cb = row.querySelector("input");
      if (e.target !== cb && !e.target.classList.contains("barr")) {
        cb.checked = !cb.checked;
        toggleSel(it, cb.checked); updateBrowseStat(); return;
      }
      if (e.target.classList.contains("barr")) {
        S.browse.stackIds = S.browse.stackIds || [];
        showBrowseDir(it.fileId, (S.browse.stack || []).concat([it.name])).then(() => {
          S.browse.stackIds = (S.browse.stack || []).map((n, i) => S.browse._ids ? S.browse._ids[i] : 0);
        });
        S.browse._ids = (S.browse._ids || []).slice(0, (S.browse.stack || []).length).concat([it.fileId]);
      }
    };
    row.ondblclick = () => {
      const it = window._browseItems.find(x => String(x.fileId) === row.dataset.fid);
      if (it && it.isDir) {
        S.browse._ids = (S.browse._ids || []).slice(0, (S.browse.stack || []).length).concat([it.fileId]);
        showBrowseDir(it.fileId, (S.browse.stack || []).concat([it.name]));
      }
    };
  });
}
function toggleSel(it, on) {
  if (on) S.browse.sel.set(it.fileId, it);
  else S.browse.sel.delete(it.fileId);
}
function updateBrowseStat() {
  let n = 0, sz = 0;
  S.browse.sel.forEach(it => { n++; sz += it.size || 0; });
  $("#browseStat").textContent = "已选 " + n + " 项 · " + fmtSize(sz);
}
$("#btnSelAll").onclick = () => {
  const items = window._browseItems || [];
  const allSel = items.length && items.every(it => S.browse.sel.has(it.fileId));
  items.forEach(it => allSel ? S.browse.sel.delete(it.fileId) : S.browse.sel.set(it.fileId, it));
  $$("#browseList .browse-row").forEach(row => {
    const it = items.find(x => String(x.fileId) === row.dataset.fid);
    row.querySelector("input").checked = !allSel && !!it;
  });
  updateBrowseStat();
};
$("#btnFileTypeSet").onclick = () => openFtModal();
$("#btnExtractSel").onclick = async () => {
  if (!S.browse.sel.size) return toast("请先勾选文件或文件夹", false);
  const sel = [];
  S.browse.sel.forEach(it => sel.push(it));
  const r = await post("/api/extract/selected", {
    link: $("#shareLink").value.trim(), title: $("#shareTitle").value.trim(),
    cat1: $("#shareCat1").value, cat2: $("#shareCat2").value,
    fileTypes: S.ftSel, selected: sel });
  $("#browseMask").classList.remove("open");
  if (!r.ok) return toast(r.message || "启动失败", false);
  toast("提取任务已启动");
  $("#extractProgress").classList.add("show");
  pollExtract();
};
$("#btnExtractAll").onclick = () => { $("#browseMask").classList.remove("open"); $("#btnExtract").onclick(); };

/* ══════════════ 123云盘登录 ══════════════ */
$("#btnQrLogin").onclick = async () => {
  $("#qrBox").style.display = "block"; $("#tokenBox").style.display = "none"; $("#pwdBox").style.display = "none";
  await refreshQr();
};
async function refreshQr() {
  $("#qrStatus").textContent = "获取二维码…";
  const r = await post("/api/login/qrcode");
  if (!r.ok) { $("#qrStatus").textContent = r.message || "获取失败"; return; }
  if (r.qr_svg) $("#qrImg").src = r.qr_svg;
  window._qrUni = r.uni_id; window._qrUuid = r.loginuuid;
  window._qrUrl = r.qr_url;
  pollQr();
}
$("#btnQrRefresh").onclick = () => refreshQr();
$("#btnCopyQr").onclick = () => {
  if (window._qrUrl) { navigator.clipboard.writeText(window._qrUrl); toast("登录链接已复制"); }
};
let _qrPolling = false;
async function pollQr() {
  if (_qrPolling) return; _qrPolling = true;
  const st = $("#qrStatus");
  try {
    while (true) {
      const r = await post("/api/login/qrcode/status", { uniId: window._qrUni, loginuuid: window._qrUuid });
      if (!r.ok) { st.textContent = "轮询失败"; break; }
      const s = r.status;
      if (r.token) {                       // 任何状态拿到 token 都算成功(含"过期后最后一搏")
        st.textContent = "✅ 登录成功";
        showUser(r.nickname, r.uid);
        toast("登录成功: " + (r.nickname || ""), true);
        break;
      }
      if (s === 0) st.textContent = "等待扫码…";
      else if (s === 1) st.textContent = "已扫码，请在手机上确认";
      else if (s === 2) st.textContent = "已确认，正在获取登录凭据…";
      else if (s === 3) { st.textContent = "二维码已过期，请刷新重试"; break; }
      else if (s === 4) { st.textContent = "会话失效，请刷新"; break; }
      // 已扫码/确认后服务端凭据就绪很快, 缩短间隔快速轮询
      await new Promise(res => setTimeout(res, (s >= 1 && s <= 3 || r.wx_pending) ? 800 : 2000));
    }
  } finally { _qrPolling = false; }
}
$("#btnTokenLogin").onclick = () => {
  $("#tokenBox").style.display = "block"; $("#qrBox").style.display = "none"; $("#pwdBox").style.display = "none";
};
$("#btnTokenGo").onclick = async () => {
  const r = await post("/api/login/token", { token: $("#tokenInput").value.trim() });
  if (r.ok) { showUser(r.nickname, r.uid); toast("Token 登录成功", true); }
  else toast(r.message || "Token 无效", false);
};
$("#btnPwdLogin").onclick = () => {
  $("#pwdBox").style.display = "block"; $("#qrBox").style.display = "none"; $("#tokenBox").style.display = "none";
};
$("#btnPwdGo").onclick = async () => {
  const r = await post("/api/login/password", {
    passport: $("#pwdUser").value.trim(), password: $("#pwdPass").value });
  if (r.ok) { showUser(r.nickname, r.uid); toast("登录成功", true); }
  else toast(r.message || "登录失败", false);
};
function showUser(nick, uid) {
  $("#loginArea").style.display = "none";
  $("#userArea").style.display = "block";
  $("#nickShow").textContent = nick || "用户";
  $("#uidShow").textContent = uid ? "UID:" + uid : "";
}
$("#btnLogout").onclick = async () => {
  await post("/api/logout");
  $("#loginArea").style.display = "block";
  $("#userArea").style.display = "none";
  toast("已退出登录");
};
async function checkLogin() {
  const r = await api("/api/login/status");
  if (r.logged) showUser(r.nickname, r.uid);
}

/* ══════════════ 秒传导入 ══════════════ */
async function loadImportFiles() {
  const r = await api("/api/import/files");
  const sel = $("#importFile");
  const cur = sel.value;
  sel.innerHTML = (r.files || []).map(f => '<option value="' + esc(f) + '">' + esc(f) + "</option>").join("");
  if (cur && r.files && r.files.includes(cur)) sel.value = cur;
}
$("#btnUploadJson").onclick = () => {
  const inp = $("#jsonFileInput");
  inp.onchange = async () => {
    const f = inp.files[0]; if (!f) return;
    const content = await f.text();
    const r = await post("/api/import/upload", { name: f.name, content: content });
    toast(r.ok ? "已上传: " + r.name : (r.message || "上传失败"), r.ok);
    if (r.ok) { await loadImportFiles(); $("#importFile").value = r.name || $("#importFile").value; }
    inp.value = "";
  };
  inp.click();
};
$("#btnAppend").onclick = () => {
  const inp = $("#jsonFileInput");
  inp.onchange = async () => {
    const f = inp.files[0]; if (!f) return;
    const content = await f.text();
    const r = await post("/api/append-import", { name: f.name, content: content });
    toast(r.ok ? "已入库, Watcher 自动加载: " + (r.message || "") : (r.message || "导入失败"), r.ok);
    if (r.ok) await loadLibs();
    inp.value = "";
  };
  inp.click();
};
$("#btnImport").onclick = async () => {
  const f = $("#importFile").value;
  if (!f) return toast("请先选择秒传 JSON 文件", false);
  const r = await post("/api/import/start", {
    file: f, targetDir: $("#importTarget").value.trim(),
    autoCommon: $("#autoCommon").checked });
  if (!r.ok) return toast(r.message || "启动失败", false);
  toast("导入任务已启动");
  $("#importProgress").classList.add("show");
  $("#btnImportStop").style.display = "block";
  pollImport();
};
$("#btnImportStop").onclick = async () => {
  const r = await post("/api/import/stop", {});
  toast(r.message || (r.ok ? "停止指令已发出" : "当前没有进行中的任务"), r.ok);
  if (r.ok) { $("#btnImportStop").disabled = true; $("#btnImportStop").textContent = "⏹ 正在停止…"; }
};
async function pollImport() {
  const r = await api("/api/import/progress");
  $("#importStep").textContent = r.step || "";
  $("#importBar").style.width = (r.total ? (r.processed / r.total * 100) : 0).toFixed(1) + "%";
  $("#importNums").textContent = (r.processed || 0) + " / " + (r.total || 0) +
    " · 成功 " + (r.success || 0) + " · 已存在 " + (r.exists || 0) + " · 失败 " + (r.failed || 0);
  $("#importLog").innerHTML = (r.logs || []).map(l => "<div>" + esc(l) + "</div>").join("");
  if (r.running) setTimeout(pollImport, 1000);
  else {
    $("#btnImportStop").style.display = "none";
    $("#btnImportStop").disabled = false;
    $("#btnImportStop").textContent = "⏹ 停止导入";
    if (r.done) { toast(r.message || "导入结束", r.ok); $("#importStep").textContent = r.message || ""; }
  }
}

/* ══════════════ 杂项按钮 ══════════════ */
$("#btnOpenDir").onclick = () => post("/api/open-dir");
$("#btnRefresh").onclick = () => refreshAll();
$("#btnRefreshL").onclick = () => refreshAll();
async function refreshAll() {
  await loadLibs();
  S.page = 1;
  doSearch();
  toast("已刷新", true);
}
/* TMDB Key */
$("#tmdbKey").value = localStorage.getItem("tmdbKey") || "";
$("#btnTmdbSave").onclick = async () => {
  const k = $("#tmdbKey").value.trim();
  localStorage.setItem("tmdbKey", k);
  const r = await post("/api/tmdb-key", { key: k });
  toast(r.ok ? (k ? "已保存自定义 Key" : "已恢复内置 Key") : "保存失败", r.ok);
};
/* 功能说明 */
const HELP = [
  ["🔍 片名搜索", "输入关键词（至少2字）+ Enter 搜索，配合影库多选与分类过滤。片名搜索按视频数排序，分类浏览按年份排序。"],
  ["📚 影库管理", "搜索栏左侧「影库」下拉可勾选多个影库，搜索与分类仅限选中范围。追加库显示导入日期。"],
  ["📂 分类浏览", "点击一级分类浏览，右上角展开二级分类；分类超过 6 行自动折叠，可「展开更多」。标签旁 ⬇ 一键导出该分类。"],
  ["📤 导出", "作品卡片「导出目录」导出整部作品；展开文件后可按版本（4K/HDR/H265…）过滤、勾选文件、按集数命名导出选中。"],
  ["☑ 合并导出", "进入多选模式勾选多个分类，合并为单个秒传 JSON，保留完整目录结构并去重。"],
  ["🔗 分享提取", "粘贴分享链接（可含提取码）自动遍历提取入库；「浏览分享」可勾选部分文件夹/文件提取；支持文件类型过滤与断点续传。"],
  ["☁️ 秒传导入", "登录 123 云盘（扫码/Token/账密）后选择 JSON，自动按 commonPath 建目录并逐条秒传。"],
  ["📊 存储分析", "右侧甜甜圈图与柱状图展示各分类容量占比，悬停联动高亮。"],
  ["🎬 TMDB 海报", "自动按标题+年份匹配海报；内置公开 Key，失效时可填入自己的 Key。"],
  ["🔄 自动加载", "后台每 3 秒扫描导入目录，新增/修改 JSON 自动加载，无需重启。"],
  ["🕘 搜索历史", "自动记录最近 30 条搜索，点击条目一键恢复。"],
  ["🎵 背景音乐", "左上角播放器，自动循环播放，可暂停/继续。"],
];
$("#btnHelp").onclick = () => {
  $("#helpBody").innerHTML = HELP.map(h =>
    '<div style="margin-bottom:10px"><b>' + h[0] + "</b><div class='muted' style='margin-top:2px'>" + h[1] + "</div></div>").join("");
  $("#helpMask").classList.add("open");
};

/* ══════════════ 背景音乐 ══════════════ */
(function initMusic() {
  const bgm = $("#bgm"), panel = $("#musicPanel"), btn = $("#musicBtn");
  let wantPlay = true;
  bgm.volume = 0.35;
  const tryPlay = () => {
    if (!wantPlay) return;
    bgm.play().then(() => { panel.classList.add("playing"); btn.textContent = "❚❚"; })
      .catch(() => {});
  };
  tryPlay();
  document.addEventListener("click", tryPlay, { once: true });
  btn.onclick = (e) => {
    e.stopPropagation();
    if (bgm.paused) { wantPlay = true; tryPlay(); }
    else { wantPlay = false; bgm.pause(); panel.classList.remove("playing"); btn.textContent = "▶"; }
  };
})();

/* ══════════════ Watcher: 数据版本轮询 ══════════════ */
async function watchVersion() {
  try {
    const r = await api("/api/libs");
    if (r.version !== S.ver) {
      const first = S.ver === -1;
      S.ver = r.version;
      if (!first) {
        await loadLibs();
        doSearch();
        toast("影库数据已自动更新", true);
      }
    }
  } catch (e) { /* 服务未就绪时忽略 */ }
  setTimeout(watchVersion, 3000);
}

/* ══════════════ 初始化 ══════════════ */
window.addEventListener("error", e => {
  post("/api/client-log", {msg: "JS error: " + e.message + " @" + (e.filename||"") + ":" + e.lineno}).catch(() => {});
});
window.addEventListener("unhandledrejection", e => {
  post("/api/client-log", {msg: "Promise reject: " + (e.reason && (e.reason.stack || e.reason.message) || String(e.reason))}).catch(() => {});
});

(async function init() {
  try {
    const ping = await api("/api/ping");
    $("#verInfo").textContent = ping.version || "";
  } catch (e) {}
  await loadLibs();
  await doSearch();
  loadHistory();
  checkLogin();
  loadImportFiles();
  watchVersion();
  setInterval(loadImportFiles, 30000);
  // 若导入仍在后台进行（如页面刷新后），自动恢复进度面板与停止按钮
  try {
    const p = await api("/api/import/progress");
    if (p && p.running) {
      $("#importProgress").classList.add("show");
      $("#btnImportStop").style.display = "block";
      pollImport();
    }
  } catch (e) {}
})();

