function toggleLang() {
  const current = localStorage.getItem('lang') || 'fr';
  const next = current === 'fr' ? 'en' : 'fr';
  setLang(next);
}

function setLang(lang) {
  localStorage.setItem('lang', lang);
  document.querySelectorAll('[data-lang]').forEach(el => {
    el.style.display = el.dataset.lang === lang ? '' : 'none';
  });
  const btn = document.getElementById('lang-toggle');
  if (btn) btn.textContent = '🌐 ' + (lang === 'fr' ? 'EN' : 'FR');
}

document.addEventListener('DOMContentLoaded', () => {
  setLang(localStorage.getItem('lang') || 'fr');
});
