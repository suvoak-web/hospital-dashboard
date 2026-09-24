/* Shared footer + lightweight analytics (GoatCounter).
   Stats: https://ptk80dash.goatcounter.com
   Create that site code at https://www.goatcounter.com/signup if it is not yours yet. */
(function () {
  var s = document.createElement('script');
  s.setAttribute('data-goatcounter', 'https://ptk80dash.goatcounter.com/count');
  s.async = true;
  s.src = 'https://gc.zgo.at/count.js';
  document.head.appendChild(s);
})();

document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelector('.page-byline')) return;
  var d = document.createElement('div');
  d.className = 'page-byline';
  d.innerHTML = '\u0e42\u0e23\u0e07\u0e1e\u0e22\u0e32\u0e1a\u0e32\u0e25\u0e1e\u0e23\u0e30\u0e17\u0e2d\u0e07\u0e04\u0e33\u0e40\u0e09\u0e25\u0e34\u0e21\u0e1e\u0e23\u0e30\u0e40\u0e01\u0e35\u0e22\u0e23\u0e15\u0e34 80 \u0e1e\u0e23\u0e23\u0e29\u0e32<br>by <b>Suweerasak Riwlord, M.D.</b>';
  d.style.cssText = 'margin:28px auto 12px;padding:16px 8px;text-align:center;color:#64748B;font-size:13px;font-family:Sarabun,Tahoma,sans-serif;border-top:1px solid rgba(148,163,184,.35);';
  document.body.appendChild(d);
});
