---
permalink: /
title: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">

<style>
.home-wrap { font-family: 'Source Serif 4', Georgia, serif; color: #1a1a1a; max-width: 680px; }
.home-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 2rem; align-items: center; justify-content: space-between; padding-bottom: 1.4rem; border-bottom: 1px solid #ddd; }
.home-taglist { display: flex; flex-wrap: wrap; gap: 0.45rem; }
.home-tag { font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-family: 'Source Serif 4', serif; font-weight: 300; }
.home-tag::after { content: "·"; margin-left: 0.45rem; color: #ddd; }
.home-tag:last-child::after { content: ""; }
.home-lang-btn { background: none; border: 1px solid #ccc; border-radius: 3px; padding: 0.15rem 0.6rem; cursor: pointer; font-size: 0.72rem; color: #888; font-family: 'Source Serif 4', serif; white-space: nowrap; }
.home-body { font-size: 0.97rem; line-height: 1.8; font-weight: 300; color: #1a1a1a; }
.home-body p { margin-bottom: 1.2rem; }
.home-body a { color: #1a1a1a; text-decoration: none; border-bottom: 1px solid #ccc; transition: border-color 0.15s; }
.home-body a:hover { border-color: #1a1a1a; }
.home-logos { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 3rem; padding-top: 1.8rem; border-top: 1px solid #ddd; }
</style>

<script>
function toggleLang() {
  var enEls = document.querySelectorAll('.lang-en');
  var frEls = document.querySelectorAll('.lang-fr');
  var btn = document.getElementById('lang-toggle');
  var isEn = btn.textContent.indexOf('EN') !== -1;
  for (var i = 0; i < enEls.length; i++) { enEls[i].style.display = isEn ? '' : 'none'; }
  for (var i = 0; i < frEls.length; i++) { frEls[i].style.display = isEn ? 'none' : ''; }
  btn.textContent = isEn ? '🌐 FR' : '🌐 EN';
}
</script>

<div class="home-wrap">
<div class="home-tags">
<div class="home-taglist">
<span class="home-tag lang-fr">Croyances</span><span class="home-tag lang-fr">Philosophie & Théologie</span><span class="home-tag lang-fr">Identité</span><span class="home-tag lang-fr">Épistémologie des sciences des religions</span><span class="home-tag lang-en" style="display:none">Beliefs</span><span class="home-tag lang-en" style="display:none">Philosophy & Theology</span><span class="home-tag lang-en" style="display:none">Identity</span><span class="home-tag lang-en" style="display:none">Epistemology of Religious Studies</span>
</div>
<button id="lang-toggle" onclick="toggleLang()" class="home-lang-btn">🌐 EN</button>
</div>
<div class="home-body lang-fr">
<p>Je suis maître de conférences à l'Université de Lorraine (France), où j'enseigne la théologie systématique et la philosophie contemporaine. Mes recherches portent sur le langage théologique, l'épistémologie de la croyance et les relations entre théologie contemporaine et sciences sociales. J'ai soutenu ma thèse en 2013 (sur l'expérience religieuse chez Karl Barth et Henri Bergson) et mon habilitation en 2020. Je m'intéresse également à la construction de l'identité, que j'explore à travers les prismes philosophique et théologique du problème de l'identité personnelle, et via l'expérimentation littéraire (<a href="/rien-de-cache/"><em>Rien de caché</em></a>, 2026).</p>
<p>Je suis cofondateur et directeur de publication de la revue <a href="https://journals.openedition.org/theoremes/"><em>Théo</em>Rèmes</a>.</p>
<p>Je travaille actuellement dans le cadre d'une <a href="https://www.iufrance.fr/les-membres-de-liuf/membre/2850-anthony-feneuil.html">chaire de l'IUF</a> sur les enjeux politiques des sciences sociales de la croyance.</p>
<p>Pour plus de détails, voir mon <a href="/cv/">CV</a> et mes <a href="/publications/">publications</a>.</p>
</div>
<div class="home-body lang-en" style="display:none">
<p>I am an Associate Professor at the University of Lorraine (France), where I teach systematic theology and contemporary philosophy. My research focuses on theological language, the epistemology of belief, and the relationships between contemporary theology and the social sciences. I completed my PhD in 2013 (on religious experience in Karl Barth and Henri Bergson) and obtained my habilitation in 2020. I am also interested in the construction of identity, which I explore through the philosophical and theological lenses of the personal identity problem, and through literary experimentation (<a href="/rien-de-cache/"><em>Rien de caché</em></a>, 2026).</p>
<p>I am a founder and publishing director of the journal <a href="https://journals.openedition.org/theoremes/"><em>Théo</em>Rèmes</a>.</p>
<p>I am currently conducting research as an <a href="https://www.iufrance.fr/les-membres-de-liuf/membre/2850-anthony-feneuil.html">IUF fellow</a> on the political consequences of the social sciences of belief.</p>
<p>For more details, see my <a href="/cv/">CV</a> and <a href="/publications/">publications</a>.</p>
</div>
<div class="home-logos">
<a href="https://ecritures.univ-lorraine.fr/"><img src="/images/logoEcritransp.png" alt="Écritures, Université de Lorraine" style="height: 72px;"></a>
<a href="https://www.iufrance.fr/les-membres-de-liuf/membre/2850-anthony-feneuil.html"><img src="/images/LogoIUF.png" alt="Institut Universitaire de France" style="height: 72px;"></a>
</div>
</div>
