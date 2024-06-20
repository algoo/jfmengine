---
title Another page
slug page2
engine jinja2
---
{

}

---

<h2> Page 2 </h2>

<p>Go to <a href="{{ url('page', args=['page1']) }}">page 1</a> </p>
