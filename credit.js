/* Shared chrome: header, desktop sidebar, mobile drawer, quick pills, footer, GoatCounter. */
(function () {
  if (document.querySelector('meta[http-equiv="refresh"]')) return;
  if (window.__ptkShell) return;
  window.__ptkShell = true;

  var PAGES = [
    { href: 'index.html', icon: '🏠', label: 'หน้าหลัก' },
    { group: '💰 การเงิน' },
    { href: 'planfin_dashboard.html', icon: '📈', label: 'Planfin / การเงิน' },
    { href: 'uc_transfer_dashboard.html', icon: '🏦', label: 'เงินโอน UC / สปสช.' },
    { href: 'sso_dashboard.html', icon: '🛡️', label: 'ประกันสังคมจากแม่ข่าย' },
    { href: 'ppfs_dashboard.html', icon: '📑', label: 'PPFS NHSO' },
    { href: 'nhso_mis.html', icon: '🏥', label: 'NHSO-MIS' },
    { href: 'opwalkin.html', icon: '💰', label: 'OP-Walkin' },
    { href: 'ar_aging.html', icon: '🧾', label: 'อายุลูกหนี้' },
    { group: '📊 KPI และแผนงาน' },
    { href: 'kpi_dashboard.html', icon: '📊', label: 'KPI Dashboard' },
    { href: 'plan2570.html', icon: '📋', label: 'แผนงานโครงการ 2570' },
    { group: '⏱ บริการ' },
    { href: 'compare.html', icon: '⏱', label: 'ระยะเวลารอคอย' },
    { href: 'bottleneck_dashboard.html', icon: '🔎', label: 'วิเคราะห์คอขวด', sub: true },
    { group: '🩺 คุณภาพเวชระเบียน' },
    { href: 'chart_audit.html', icon: '🩺', label: 'Audit ชาร์ต' },
    { group: '💊 รพ.สต.' },
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
      '#ptk-sidebar a{display:flex;align-items:center;gap:10px;padding:10px 18px;margin:2px 10px;border-radius:8px;color:#334155;text-decoration:none;font-weight:600;font-size:14.5px}',
      '#ptk-sidebar .ptk-group{margin:18px 20px 6px;padding-top:14px;border-top:1px solid #EEF2F6;font-size:11px;font-weight:700;letter-spacing:.6px;color:#6B8BA4;text-transform:uppercase;cursor:default;user-select:none}',
      '#ptk-sidebar .ptk-group:first-of-type{border-top:0;padding-top:0;margin-top:12px}',
      '#ptk-sidebar a.sub{position:relative;font-size:13px;font-weight:500;color:#94A3B8;padding:7px 14px 7px 18px;margin:0 10px 2px 38px;border-radius:0 8px 8px 0;border-left:2px solid #E2E8F0}',
      '#ptk-sidebar a:hover,#ptk-sidebar a.active{background:rgba(29,111,164,.08);color:#1D6FA4}',
      '#ptk-sidebar a.sub:hover,#ptk-sidebar a.sub.active{border-left-color:#1D6FA4}',
      '#ptk-dim{display:none;position:fixed;inset:0;top:64px;background:rgba(15,23,42,.35);z-index:10030}',
      '#ptk-quick{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px;font-family:Sarabun,"IBM Plex Sans Thai",Tahoma,sans-serif}',
      '#ptk-quick a{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:999px;border:1px solid #E2E8F0;background:#fff;color:#1A2332;text-decoration:none;font-weight:700;font-size:13px}',
      '#ptk-quick a:hover,#ptk-quick a.active{background:#1D6FA4;color:#fff;border-color:#1D6FA4}',
      'body.ptk-has-shell{padding-top:64px !important}',
      'body.ptk-has-shell nav.top-nav,body.ptk-has-shell .top-nav,body.ptk-has-shell aside.sidebar:not(#ptk-sidebar),body.ptk-has-shell #sidebar:not(#ptk-sidebar){display:none !important}',
      'body.ptk-has-shell .quick:not(#ptk-quick){display:none !important}',
      'body.ptk-has-shell .main-content,body.ptk-has-shell .main,body.ptk-has-shell .wrap{margin-left:0}',
      '.page-byline{margin:28px auto 12px;padding:16px 8px;text-align:center;color:#64748B;font-size:13px;font-family:Sarabun,Tahoma,sans-serif;border-top:1px solid rgba(148,163,184,.35)}',
      '@media(min-width:901px){body.ptk-has-shell{margin-left:260px}#ptk-burger{visibility:hidden}}',
      /* full-width content: lift max-width caps on main page wrappers (desktop) */
      '@media(min-width:901px){body.ptk-has-shell > .wrap,body.ptk-has-shell > main,body.ptk-has-shell > .main,body.ptk-has-shell > .main-content,body.ptk-has-shell > .max-w-6xl,body.ptk-has-shell > .max-w-7xl{max-width:none !important;margin-left:0 !important;margin-right:0 !important;padding-left:24px !important;padding-right:24px !important;box-sizing:border-box}}',
      '@media(max-width:900px){#ptk-sidebar{transform:translateX(-100%);box-shadow:8px 0 24px rgba(0,0,0,.12)}#ptk-sidebar.open{transform:translateX(0)}#ptk-dim.show{display:block}body.ptk-has-shell{margin-left:0 !important}#ptk-header .ptk-left{flex:1}#ptk-header .ptk-left>div:last-child{min-width:0}#ptk-header .ptk-title{font-size:12.5px;white-space:normal;line-height:1.25;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}#ptk-header .ptk-sub{font-size:11px}#ptk-header .ptk-clock{display:none}}',
      '.kpi-row{grid-template-columns:1.3fr 1.3fr .85fr !important;gap:14px !important}',
      '@media(max-width:900px){.kpi-row{grid-template-columns:1fr !important}}',
      '.kpi.kpi-prog,.kpi.net{border-radius:16px !important;border:1px solid transparent !important;border-left:5px solid !important;padding:15px 16px 13px !important;box-shadow:0 6px 18px rgba(15,23,42,.05) !important}',
      '.kpi.pay.kpi-prog{background:linear-gradient(180deg,#fff 0%,#fff6f6 100%) !important;border-color:#fecaca !important;border-left-color:#dc2626 !important}',
      '.kpi.rec.kpi-prog{background:linear-gradient(180deg,#fff 0%,#f4fdf7 100%) !important;border-color:#bbf7d0 !important;border-left-color:#16a34a !important}',
      '.kpi.net{background:linear-gradient(180deg,#fff 0%,#f5f9ff 100%) !important;border-color:#dbeafe !important;border-left-color:#2563eb !important}',
      '.kpi-head{display:flex;align-items:center;justify-content:space-between;gap:8px}',
      '.kpi-prog .kpi-lbl{font-size:12.5px !important;font-weight:700 !important;color:#64748B !important;margin:0 !important}',
      '.kpi-pill{font-size:12px;font-weight:800;padding:3px 9px;border-radius:999px;white-space:nowrap}',
      '.kpi.pay .kpi-pill{background:#fee2e2;color:#b91c1c}',
      '.kpi.rec .kpi-pill{background:#dcfce7;color:#15803d}',
      '.kpi-prog .kpi-val,.kpi.net .kpi-val{font-size:1.55rem !important;font-weight:800 !important;letter-spacing:-.3px;margin:7px 0 2px !important;line-height:1.1}',
      '.kpi-prog .kpi-sub{font-size:12px !important;color:#94a3b8 !important;margin:0 0 2px !important}',
      '.kpi-bar{height:11px;border-radius:99px;margin-top:12px;overflow:hidden}',
      '.kpi.pay .kpi-bar{background:#fecaca}',
      '.kpi.rec .kpi-bar{background:#dcfce7}',
      '.kpi.pay .kpi-bar span{display:block;height:100%;background:linear-gradient(90deg,#f87171,#b91c1c);border-radius:99px}',
      '.kpi.rec .kpi-bar span{display:block;height:100%;background:linear-gradient(90deg,#4ade80,#15803d);border-radius:99px}',
      '.kpi-split{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}',
      '.kpi-chip{border-radius:11px;padding:8px 10px}',
      '.kpi.pay .kpi-chip.done{background:#fee2e2}',
      '.kpi.pay .kpi-chip.left{background:#fff1f2}',
      '.kpi.rec .kpi-chip.done{background:#dcfce7}',
      '.kpi.rec .kpi-chip.left{background:#f0fdf4}',
      '.kpi-chip span{display:block;font-size:11px;color:#64748B;font-weight:700}',
      '.kpi-chip b{display:block;font-size:14.5px;font-weight:800;margin-top:1px}',
      '.kpi.pay .kpi-chip.done b{color:#b91c1c}',
      '.kpi.pay .kpi-chip.left b{color:#fca5a5}',
      '.kpi.rec .kpi-chip.done b{color:#15803d}',
      '.kpi.rec .kpi-chip.left b{color:#86efac}',
      '.kpi-tag{display:inline-block;background:#dbeafe;color:#1d4ed8;border-radius:99px;padding:5px 12px;font-size:12.5px;font-weight:800;margin-top:14px}',
    ].join('\n');
    document.head.appendChild(s);
  }

  function buildHeader() {
    var h = document.createElement('header');
    h.id = 'ptk-header';
    h.innerHTML = '<div class="ptk-left">'
      + '<button type="button" id="ptk-burger" aria-label="เมนู">☰</button>'
      + '<div class="ptk-mark">🏥</div>'
      + '<div><div class="ptk-title" title="โรงพยาบาลพระทองคำเฉลิมพระเกียรติ 80 พรรษา">โรงพยาบาลพระทองคำเฉลิมพระเกียรติ 80 พรรษา</div>'
      + '<div class="ptk-sub">ระบบติดตามข้อมูลโรงพยาบาล</div></div></div>'
      + '<div class="ptk-clock"><div class="ptk-time" id="ptk-clock">--:--</div>'
      + '<div class="ptk-date" id="ptk-date"></div></div>';
    document.body.insertBefore(h, document.body.firstChild);
  }

  function buildSidebar() {
    var a = document.createElement('aside');
    a.id = 'ptk-sidebar';
    a.innerHTML = PAGES.map(function (p) {
      if (p.group) return '<div class="ptk-group">' + p.group + '</div>';
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
    box.innerHTML = PAGES.filter(function (p) { return !p.group; }).map(function (p) {
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

  function enhanceOpWalkinCharts() {
    if (file !== 'opwalkin.html') return;
    if (typeof renderTopCharts !== 'function') return;
    var recTitle = document.querySelector('#cTopRec') && document.getElementById('cTopRec').closest('.card');
    var payTitle = document.querySelector('#cTopPay') && document.getElementById('cTopPay').closest('.card');
    if (recTitle) {
      var t = recTitle.querySelector('.card-ttl');
      if (t) t.lastChild.textContent = 'Top 10 แหล่งพึงรับ — รับแล้ว vs คงค้าง';
    }
    if (payTitle) {
      var t2 = payTitle.querySelector('.card-ttl');
      if (t2) t2.lastChild.textContent = 'Top 10 รายจ่าย — จ่ายแล้ว vs คงค้าง';
    }
    window.counterpartSettled = function (name, kind) {
      var months = getAllMonthsForHosp(state.currentHosp);
      var total = 0, settled = 0;
      months.forEach(function (m) {
        var map = kind === 'rec' ? (m.rd || {}) : (m.pd || {});
        Object.entries(map).forEach(function (pair) {
          var h = pair[0], v = pair[1];
          if (kind === 'rec' && String(h).indexOf('รวม') === 0) return;
          var c = resolveHospName(h);
          if (c !== name) return;
          total += v;
          var done = kind === 'rec' ? isRec(c, m.month) : isPaid(c, m.month);
          if (done) settled += v;
        });
      });
      return { total: total, settled: settled, remain: Math.max(0, total - settled) };
    };
    window.renderTopCharts = function (hosp) {
      var months = getAllMonthsForHosp(hosp);
      var recMap = {};
      months.forEach(function (m) {
        Object.entries(m.rd || {}).forEach(function (pair) {
          if (String(pair[0]).indexOf('รวม') === 0) return;
          var c = resolveHospName(pair[0]);
          recMap[c] = (recMap[c] || 0) + pair[1];
        });
      });
      var topRec = Object.entries(recMap).filter(function (e) { return e[1] > 0; }).sort(function (a, b) { return b[1] - a[1]; }).slice(0, 10);
      var recSettled = topRec.map(function (e) { return counterpartSettled(e[0], 'rec'); });
      dc('cTopRec');
      charts.cTopRec = new Chart(document.getElementById('cTopRec'), {
        type: 'bar',
        data: {
          labels: topRec.map(function (e) { return e[0]; }),
          datasets: [
            { label: 'รับแล้ว', data: recSettled.map(function (s) { return s.settled; }), backgroundColor: '#B8860B', borderRadius: 3, stack: 's' },
            { label: 'คงค้างรับ', data: recSettled.map(function (s) { return s.remain; }), backgroundColor: '#1A7A4A', borderRadius: 3, stack: 's' }
          ]
        },
        options: {
          indexAxis: 'y', responsive: true, maintainAspectRatio: false,
          plugins: {
            legend: { display: true, position: 'top', labels: { font: FONT, boxWidth: 12 } },
            tooltip: { callbacks: { afterBody: function (items) {
              var s = recSettled[items[0].dataIndex];
              var pct = s.total ? Math.round(s.settled / s.total * 100) : 0;
              return 'รวมพึงรับ ' + fmt(s.total) + ' · รับแล้ว ' + pct + '%';
            } } }
          },
          scales: {
            x: { stacked: true, ticks: { callback: function (v) { return fmtK(v); }, font: FONT }, grid: { color: '#E8EFF7' } },
            y: { stacked: true, ticks: { font: Object.assign({}, FONT, { size: 10 }) }, grid: { display: false } }
          }
        }
      });
      var payMap = {};
      months.forEach(function (m) {
        Object.entries(m.pd || {}).forEach(function (pair) {
          var c = resolveHospName(pair[0]);
          payMap[c] = (payMap[c] || 0) + pair[1];
        });
      });
      var topPay = Object.entries(payMap).filter(function (e) { return e[1] > 0; }).sort(function (a, b) { return b[1] - a[1]; }).slice(0, 10);
      var paySettled = topPay.map(function (e) { return counterpartSettled(e[0], 'pay'); });
      dc('cTopPay');
      charts.cTopPay = new Chart(document.getElementById('cTopPay'), {
        type: 'bar',
        data: {
          labels: topPay.map(function (e) { return e[0]; }),
          datasets: [
            { label: 'จ่ายแล้ว', data: paySettled.map(function (s) { return s.settled; }), backgroundColor: '#B8860B', borderRadius: 3, stack: 's' },
            { label: 'คงค้างจ่าย', data: paySettled.map(function (s) { return s.remain; }), backgroundColor: '#C0392B', borderRadius: 3, stack: 's' }
          ]
        },
        options: {
          indexAxis: 'y', responsive: true, maintainAspectRatio: false,
          plugins: {
            legend: { display: true, position: 'top', labels: { font: FONT, boxWidth: 12 } },
            tooltip: { callbacks: { afterBody: function (items) {
              var s = paySettled[items[0].dataIndex];
              var pct = s.total ? Math.round(s.settled / s.total * 100) : 0;
              return 'รวมพึงจ่าย ' + fmt(s.total) + ' · จ่ายแล้ว ' + pct + '%';
            } } }
          },
          scales: {
            x: { stacked: true, ticks: { callback: function (v) { return fmtK(v); }, font: FONT }, grid: { color: '#E8EFF7' } },
            y: { stacked: true, ticks: { font: Object.assign({}, FONT, { size: 10 }) }, grid: { display: false } }
          }
        }
      });
    };
    var ovTitle = document.querySelector('#cOverview') && document.getElementById('cOverview').closest('.card');
    if (ovTitle) {
      var t3 = ovTitle.querySelector('.card-ttl');
      if (t3) t3.lastChild.textContent = 'พึงรับ vs พึงจ่าย รายเดือน — ส่วนที่เคลียรแล้ว';
    }
    window.monthSettled = function (m) {
      var recDone = 0, payDone = 0;
      Object.entries(m.rd || {}).forEach(function (pair) {
        if (String(pair[0]).indexOf('รวม') === 0) return;
        if (isRec(resolveHospName(pair[0]), m.month)) recDone += pair[1];
      });
      Object.entries(m.pd || {}).forEach(function (pair) {
        if (isPaid(resolveHospName(pair[0]), m.month)) payDone += pair[1];
      });
      var rec = m.receivable || 0, pay = m.payable || 0;
      return {
        recDone: Math.min(recDone, rec),
        recRemain: Math.max(0, rec - recDone),
        payDone: Math.min(payDone, pay),
        payRemain: Math.max(0, pay - payDone)
      };
    };
    window.renderOverviewChart = function (months) {
      dc('cOverview');
      var settled = months.map(monthSettled);
      charts.cOverview = new Chart(document.getElementById('cOverview'), {
        type: 'bar',
        data: {
          labels: months.map(function (m) { return m.month; }),
          datasets: [
            { label: 'รับแล้ว', data: settled.map(function (s) { return s.recDone; }), backgroundColor: '#CA8A04', borderRadius: 4, stack: 'rec' },
            { label: 'คงค้างรับ', data: settled.map(function (s) { return s.recRemain; }), backgroundColor: '#1A7A4A', borderRadius: 4, stack: 'rec' },
            { label: 'จ่ายแล้ว', data: settled.map(function (s) { return s.payDone; }), backgroundColor: '#B45309', borderRadius: 4, stack: 'pay' },
            { label: 'คงค้างจ่าย', data: settled.map(function (s) { return s.payRemain; }), backgroundColor: '#C0392B', borderRadius: 4, stack: 'pay' }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: {
            legend: { labels: { font: FONT, boxWidth: 12 } },
            tooltip: { callbacks: { afterBody: function (items) {
              var s = settled[items[0].dataIndex];
              var rec = s.recDone + s.recRemain, pay = s.payDone + s.payRemain;
              var rp = rec ? Math.round(s.recDone / rec * 100) : 0;
              var pp = pay ? Math.round(s.payDone / pay * 100) : 0;
              return 'รับแล้ว ' + rp + '% · จ่ายแล้ว ' + pp + '%';
            } } }
          },
          scales: {
            y: { stacked: true, ticks: { callback: function (v) { return fmtK(v); }, font: FONT }, grid: { color: '#E8EFF7' } },
            x: { stacked: true, ticks: { font: FONT }, grid: { display: false } }
          }
        }
      });
    };
    try { renderTopCharts(state.currentHosp); } catch (e) {}
    try { renderOverviewChart(getAllMonthsForHosp(state.currentHosp)); } catch (e) {}
  }


  function enhanceOpWalkinKpis() {
    if (file !== 'opwalkin.html') return;
    if (typeof renderKPIs !== 'function' || typeof getPaidFromCells !== 'function') return;
    window.renderKPIs = function (months) {
      var totalRec = months.reduce(function (s, m) { return s + (m.receivable || 0); }, 0);
      var totalPay = months.reduce(function (s, m) { return s + (m.payable || 0); }, 0);
      var net = totalRec - totalPay;
      var paidPay = getPaidFromCells(state.currentHosp) + state.payments.filter(function (p) {
        return p.hosp === state.currentHosp && p.type === 'payable';
      }).reduce(function (s, p) { return s + p.amount; }, 0);
      var recPaid = getRecFromCells(state.currentHosp);
      var outstanding = Math.max(0, totalPay - paidPay);
      var recOut = Math.max(0, totalRec - recPaid);
      var payPct = totalPay ? Math.round(paidPay / totalPay * 1000) / 10 : 0;
      var recPct = totalRec ? Math.round(recPaid / totalRec * 1000) / 10 : 0;
      var last = months[months.length - 1] || {};
      var lastLbl = last.month || '';
      var netTag = net >= 0 ? '▲ รับมากกว่าจ่าย' : '▼ จ่ายมากกว่ากัน';
      function card(kind, title, pill, total, lastAmt, settledLbl, settled, leftLbl, left) {
        return '<div class="kpi ' + kind + ' kpi-prog">'
          + '<div class="kpi-head"><div class="kpi-lbl">' + title + '</div><div class="kpi-pill">' + pill + '</div></div>'
          + '<div class="kpi-val">' + fmt(total) + '</div>'
          + '<div class="kpi-sub">เดือนล่าสุด ' + lastLbl + ' · ' + fmt(lastAmt) + '</div>'
          + '<div class="kpi-bar"><span style="width:' + pill.replace('%','') + '%"></span></div>'
          + '<div class="kpi-split">'
          + '<div class="kpi-chip done"><span>' + settledLbl + '</span><b>' + fmt(settled) + '</b></div>'
          + '<div class="kpi-chip left"><span>' + leftLbl + '</span><b>' + fmt(left) + '</b></div>'
          + '</div></div>';
      }
      document.getElementById('kpiRow').innerHTML =
        card('pay', 'พึงจ่ายรวม', payPct + '%', totalPay, last.payable || 0, 'จ่ายแล้ว', paidPay, 'ค้างจ่าย', outstanding)
        + card('rec', 'พึงรับรวม', recPct + '%', totalRec, last.receivable || 0, 'รับแล้ว', recPaid, 'ค้างรับ', recOut)
        + '<div class="kpi net">'
        + '<div class="kpi-lbl">ยอดสุทธิสะสม</div>'
        + '<div class="kpi-val">' + fmt(net) + '</div>'
        + '<div class="kpi-sub">รับ ' + fmt(totalRec) + ' − จ่าย ' + fmt(totalPay) + '</div>'
        + '<div class="kpi-tag">' + netTag + '</div>'
        + '</div>';
    };
    try { renderKPIs(getAllMonthsForHosp(state.currentHosp)); } catch (e) {}
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
    enhanceOpWalkinCharts();
    enhanceOpWalkinKpis();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
