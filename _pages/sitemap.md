---
layout: refonte
title: "Plan du site"
permalink: /sitemap/
lang: fr
---
<div class="pagehead"><div class="eyebrow">Navigation</div><h2>Plan du site</h2></div>

<div class="prose">
<p>Toutes les pages du site. Une version <a href="/sitemap.xml">XML</a> est disponible pour les moteurs de recherche.</p>
<ul>
<li><a href="/fr/">Accueil</a> · <a href="/en/">Home (EN)</a></li>
{% for link in site.data.navigation.main %}<li><a href="{{ link.url }}">{{ link.title }}</a></li>
{% endfor %}<li><a href="/rien-de-cache/">Rien de caché</a></li>
<li><a href="/terms/">Terms and Privacy Policy</a></li>
</ul>
</div>
