---
title Bienvenue sur mon site !
slug accueil
lang fr

page_header_h1 Bienvenue !
page_header_h2 Un exemple de site pour JFME
---
{

}
---

{% markdown %}
**Voilà une image de Tux :**
{% endmarkdown%}

{{
    page_widgets.image(
        IMAGE_PATH = static("images/tux.png"),
    )
}}