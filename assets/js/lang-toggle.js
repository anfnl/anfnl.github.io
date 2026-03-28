function toggleLang() {
  const current = localStorage.getItem('lang') || 'en';
  const next = current === 'en' ? 'fr' : 'en';
  setLang(next);
}

function setLang(lang) {
  localStorage.setItem('lang', lang);
  document.querySelectorAll('[data-lang]').forEach(el => {
    el.style.display = el.dataset.lang === lang ? '' : 'none';
  });
  const btn = document.getElementById('lang-toggle');
  if (btn) btn.textContent = '🌐 ' + (lang === 'en' ? 'FR' : 'EN');
}

document.addEventListener('DOMContentLoaded', () => {
  setLang(localStorage.getItem('lang') || 'en');
});
