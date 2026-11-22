/* Portfolio site behaviour: theme toggle, mobile nav, project filters, scroll reveal. */
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');

  function store(key, value) {
    try {
      if (value === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, value);
    } catch (e) { return null; }
  }

  /* Theme toggle */
  var toggle = document.getElementById('theme-toggle');
  function paintIcon() {
    if (!toggle) return;
    var light = root.getAttribute('data-theme') === 'light';
    toggle.innerHTML = light ? '<i class="bi bi-moon-stars"></i>' : '<i class="bi bi-sun"></i>';
    toggle.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
  }
  if (toggle) {
    paintIcon();
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      store('theme', next);
      paintIcon();
    });
  }

  /* Mobile navigation */
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.innerHTML = open ? '<i class="bi bi-x-lg"></i>' : '<i class="bi bi-list"></i>';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
        menuBtn.innerHTML = '<i class="bi bi-list"></i>';
      }
    });
  }

  /* Project filters */
  var filterBar = document.querySelector('.filters');
  if (filterBar) {
    var items = document.querySelectorAll('[data-tags]');
    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-filter]');
      if (!btn) return;
      var f = btn.getAttribute('data-filter');
      filterBar.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      items.forEach(function (el) {
        var tags = el.getAttribute('data-tags').split(' ');
        el.classList.toggle('is-hidden', f !== 'all' && tags.indexOf(f) === -1);
      });
    });
  }

  /* Scroll reveal */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* Print resume */
  var printBtn = document.getElementById('print-resume');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });
})();
