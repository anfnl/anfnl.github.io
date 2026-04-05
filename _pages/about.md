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
.home-body { font-size: 0.97rem; line-height: 1.8; font-weight: 300; color: #1a1a1a; font-family: 'Source Serif 4', Georgia, serif; }
.home-body p { margin-bottom: 1.2rem; }
.home-body a { color: #1a1a1a; text-decoration: none; border-bottom: 1px solid #ccc; transition: border-color 0.15s; }
.home-body a:hover { border-color: #1a1a1a; }
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

function adjustTags() {
  var inner = document.getElementById('home-tags-inner');
  if (!inner) return;
  var mobile = window.innerWidth <= 600;
  inner.style.flexWrap = mobile ? 'wrap' : 'nowrap';
  inner.style.overflow = mobile ? 'visible' : 'hidden';
  var spans = inner.querySelectorAll('span');
  for (var i = 0; i < spans.length; i++) {
    spans[i].style.whiteSpace = mobile ? 'normal' : 'nowrap';
    spans[i].style.overflow = mobile ? 'visible' : 'hidden';
    spans[i].style.textOverflow = mobile ? 'unset' : 'ellipsis';
  }
}

window.addEventListener('load', adjustTags);
window.addEventListener('resize', adjustTags);
</script>

<div style="font-family: 'Source Serif 4', Georgia, serif; color: #1a1a1a; max-width: 680px;">
<div style="display: flex; align-items: center; margin-bottom: 2rem; padding-bottom: 1.4rem; border-bottom: 1px solid #ddd;">
<div id="home-tags-inner" style="flex: 1; min-width: 0; overflow: hidden; display: flex; flex-wrap: nowrap; gap: 0.2rem; align-items: center;">
<span class="lang-fr" style="font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Croyances ·</span>
<span class="lang-fr" style="font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Philosophie & Théologie ·</span>
<span class="lang-fr" style="font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Identité ·</span>
<span class="lang-fr" style="font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Épistémologie des sciences des religions</span>
<span class="lang-en" style="display:none; font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Beliefs ·</span>
<span class="lang-en" style="display:none; font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Philosophy & Theology ·</span>
<span class="lang-en" style="display:none; font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Identity ·</span>
<span class="lang-en" style="display:none; font-size: 0.72rem; letter-spacing: 0.06em; color: #999; font-weight: 300; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;">Epistemology of Religious Studies</span>
</div>
<button id="lang-toggle" onclick="toggleLang()" style="flex-shrink: 0; margin-left: 0.8rem; background: none; border: 1px solid #ccc; border-radius: 3px; padding: 0.15rem 0.6rem; cursor: pointer; font-size: 0.65rem; color: #aaa; font-family: 'Source Serif 4', Georgia, serif; white-space: nowrap;">🌐 EN</button>
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
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 3rem; padding-top: 1.8rem; border-top: 1px solid #ddd;">
<a href="https://ecritures.univ-lorraine.fr/"><img src="/images/logoEcritransp.png" alt="Écritures, Université de Lorraine" style="height: 72px;"></a>
<a href="https://www.iufrance.fr/les-membres-de-liuf/membre/2850-anthony-feneuil.html"><img src="/images/LogoIUF.png" alt="Institut Universitaire de France" style="height: 72px;"></a>
</div>
</div>
