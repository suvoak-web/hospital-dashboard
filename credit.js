/* Shared chrome: header, desktop sidebar, mobile drawer, quick pills, footer, GoatCounter. */
(function () {
  if (document.querySelector('meta[http-equiv="refresh"]')) return;
  if (window.__ptkShell) return;
  window.__ptkShell = true;

  var PAGES = [
    { href: 'index.html', icon: '🏠', label: 'หน้าหลัก' },
    { href: 'kpi_dashboard.html', icon: '📊', label: 'KPI Dashboard' },
    { href: 'planfin_dashboard.html', icon: '📈', label: 'Planfin / การเงิน' },
    { href: 'uc_transfer_dashboard.html', icon: '🏦', label: 'เงินโอน UC / สปสช.' },
    { href: 'opwalkin.html', icon: '💰', label: 'พึงรับ-พึงจ่าย' },
    { href: 'compare.html', icon: '⏱', label: 'ระยะเวลารอคอย' },
    { href: 'bottleneck_dashboard.html', icon: '🔎', label: 'วิเคราะห์คอขวด', sub: true },
    { href: 'pcupayment.html', icon: '💊', label: 'ยาและเวชภัณฑ์ รพ.สต.' }
  ];

  var file = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  if (!file || file.indexOf('.') === -1) file = 'index.html';
  if (file === 'fin_dashboard.html' || file === 'fin_projection.html') file = 'planfin_dashboard.html';

  function isActive(href) {
    return file === href.toLowerCase();
  }

  function css() {
    var s = document.createElement('style');
    s.id = 'ptk-shell-css';
    s.textContent = [
      '#ptk-header{position:fixed;top:0;left:0;right:0;z-index:10050;height:64px;background:#1D6FA4;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 16px 0 10px;box-shadow:0 2px 10px rgba(0,0,0,.12);font-family:Sarabun,"IBM Plex Sans Thai",Tahoma,sans-serif}',
      '#ptk-header .ptk-left{display:flex;align-items:center;gap:10px;min-width:0}',
      '#ptk-burger{background:none;border:none;color:#fff;font-size:26px;cursor:pointer;padding:6px 10px;line-height:1}',
      '#ptk-header .ptk-mark{width:40px;height:40px;border-radius:10px;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}',
      '#ptk-header .ptk-title{font-weight:700;font-size:15.5px;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
      '#ptk-header .ptk-sub{font-size:12px;opacity:.88}',
      '#ptk-header .ptk-clock{text-align:right;font-family:"IBM Plex Mono",ui-monospace,monospace}',
      '#ptk-header .ptk-time{font-size:20px;font-weight:700}',
      '#ptk-header .ptk-date{font-size:12px;opacity:.9}',
      '#ptk-sidebar{position:fixed;top:64px;left:0;bottom:0;width:260px;background:#fff;border-right:1px solid #E2E8F0;overflow-y:auto;padding:14px 0 24px;z-index:10040;transform:translateX(0);transition:transform .2s ease;font-family:Sarabun,"IBM Plex Sans Thai",Tahoma,sans-serif}',
      '#ptk-sidebar a{display:flex;align-items:center;gap:10px;padding:11px 18px;margin:3px 10px;border-radius:8px;color:#64748B;text-decoration:none;font-weight:600;font-size:14.5px}',
      '#ptk-sidebar a.sub{font-size:13.5px;font-weight:500;padding-left:36px}',
      '#ptk-sidebar a:hover,#ptk-sidebar a.active{background:rgba(29,111,164,.08);color:#1D6FA4}',
      '#ptk-dim{display:none;position:fixed;inset:0;top:64px;background:rgba(15,23,42,.35);z-index:10030}',
      '#ptk-quick{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px;font-family:Sarabun,"IBM Plex Sans Thai",Tahoma,sans-serif}',
      '#ptk-quick a{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:999px;border:1px solid #E2E8F0;background:#fff;color:#1A2332;text-decoration:none;font-weight:700;font-size:13px}',
      '#ptk-quick a:hover,#ptk-quick a.active{background:#1D6FA4;color:#fff;border-color:#1D6FA4}',
      'body.ptk-has-shell{padding-top:64px !important}',
      'body.ptk-has-shell nav.top-nav,body.ptk-has-shell .top-nav,body.ptk-has-shell aside.sidebar:not(#ptk-sidebar),body.ptk-has-shell #sidebar:not(#ptk-sidebar),body.ptk-has-shell > header:not(#ptk-header){display:none !important}',
      'body.ptk-has-shell .quick:not(#ptk-quick){display:none !important}',
      'body.ptk-has-shell .main-content,body.ptk-has-shell .main,body.ptk-has-shell .wrap{margin-left:0}',
      '.page-byline{margin:28px auto 12px;padding:16px 8px;text-align:center;color:#64748B;font-size:13px;font-family:Sarabun,Tahoma,sans-serif;border-top:1px solid rgba(148,163,184,.35)}',
      '@media(min-width:901px){body.ptk-has-shell{margin-left:260px}}',
      '@media(max-width:900px){#ptk-sidebar{transform:translateX(-100%);box-shadow:8px 0 24px rgba(0,0,0,.12)}#ptk-sidebar.open{transform:translateX(0)}#ptk-dim.show{display:block}body.ptk-has-shell{margin-left:0 !important}#ptk-header .ptk-title{font-size:13.5px}#ptk-header .ptk-clock{display:none}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  function buildHeader() {
    var h = document.createElement('header');
    h.id = 'ptk-header';
    h.innerHTML = '<div class="ptk-left">'
      + '<button type="button" id="ptk-burger" aria-label="เมนู">☰</button>'
      + '<div class="ptk-mark">🏥</div>'
      + '<div><div class="ptk-title">โรงพยาบาลพระทองคำเฉลิมพระเกียรติ 80 พรรษา</div>'
      + '<div class="ptk-sub">ระบบติดตามข้อมูลโรงพยาบาล</div></div></div>'
      + '<div class="ptk-clock"><div class="ptk-time" id="ptk-clock">--:--</div>'
      + '<div class="ptk-date" id="ptk-date"></div></div>';
    document.body.insertBefore(h, document.body.firstChild);
  }

  function buildSidebar() {
    var a = document.createElement('aside');
    a.id = 'ptk-sidebar';
    a.innerHTML = PAGES.map(function (p) {
      return '<a href="' + p.href + '" class="'
        + (isActive(p.href) ? 'active' : '')
        + (p.sub ? ' sub' : '') + '">' + p.icon + ' ' + p.label + '</a>';
    }).join('');
    document.body.insertBefore(a, document.body.firstChild.nextSibling);
    var dim = document.createElement('div');
    dim.id = 'ptk-dim';
    document.body.appendChild(dim);
  }

  function buildQuick() {
    var box = document.createElement('div');
    box.id = 'ptk-quick';
    box.innerHTML = PAGES.map(function (p) {
      return '<a href="' + p.href + '"' + (isActive(p.href) ? ' class="active"' : '') + '>'
        + p.icon + ' ' + p.label.replace(' / การเงิน', '').replace(' / สปสช.', '') + '</a>';
    }).join('');
    var host = document.querySelector('.main-content, .main, .wrap, main');
    if (host) host.insertBefore(box, host.firstChild);
    else document.body.insertBefore(box, document.getElementById('ptk-sidebar').nextSibling);
  }

  function tick() {
    var now = new Date();
    var el = document.getElementById('ptk-clock');
    var ed = document.getElementById('ptk-date');
    if (!el) return;
    el.textContent = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
    var days = ['อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์'];
    var months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
    if (ed) ed.textContent = days[now.getDay()] + ' ' + now.getDate() + ' ' + months[now.getMonth()] + ' ' + (now.getFullYear() + 543);
  }

  function bind() {
    var side = document.getElementById('ptk-sidebar');
    var dim = document.getElementById('ptk-dim');
    function close() { side.classList.remove('open'); dim.classList.remove('show'); }
    function toggle() {
      if (window.innerWidth > 900) return;
      var on = side.classList.toggle('open');
      dim.classList.toggle('show', on);
    }
    document.getElementById('ptk-burger').addEventListener('click', toggle);
    dim.addEventListener('click', close);
    window.addEventListener('resize', function () { if (window.innerWidth > 900) close(); });
  }

  function footer() {
    if (document.querySelector('.page-byline')) return;
    var d = document.createElement('div');
    d.className = 'page-byline';
    d.innerHTML = 'โรงพยาบาลพระทองคำเฉลิมพระเกียรติ 80 พรรษา<br>by <b>Suweerasak Riwlord, M.D.</b>';
    document.body.appendChild(d);
  }

  function analytics() {
    if (document.querySelector('script[data-goatcounter]')) return;
    var s = document.createElement('script');
    s.setAttribute('data-goatcounter', 'https://ptk80dash.goatcounter.com/count');
    s.async = true;
    s.src = 'https://gc.zgo.at/count.js';
    document.head.appendChild(s);
  }

  function boot() {
    css();
    document.body.classList.add('ptk-has-shell');
    buildHeader();
    buildSidebar();
    buildQuick();
    bind();
    tick();
    setInterval(tick, 10000);
    footer();
    analytics();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
