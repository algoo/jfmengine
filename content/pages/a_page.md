---
title Page1
slug page1
engine jinja2
---
{

}

---

<h2>Page 1</h2>

<p>Go to <a href="{{ url('page', args=['page2']) }}">page 2</a> </p>

