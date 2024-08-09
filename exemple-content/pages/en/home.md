---
title Welcome on my site !
slug home
lang en
description Home page 

page_header_h1 Welcome !
page_header_h2 This is a example site for JFME
---
{

}
---

{% markdown %}
**Here an image of tux :**
{% endmarkdown%}

{{
    page_widgets.image(
        IMAGE_PATH = static("images/tux.png"),
    )
}}