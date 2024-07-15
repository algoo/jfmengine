---
title Another page
slug page2
template_engine jinja2
---
{

}

---

<h2> Page 2 </h2>

<p>Go to <a href="{{ url_for_slug('page1') }}">page 1</a> </p>
