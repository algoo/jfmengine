---
title Page1
slug page1
template_engine jinja2
---
{

}

---
{% from "widgets/page_header.html" import page_header %}


<h2>Page 1</h2>

<p>Go to <a href="{{ url('page', args=['page2']) }}">page 2</a> </p>

<article>
{% markdown %}
```
This is markdown.
```
{% endmarkdown %}
</article>


{{ page_header(
    markdown('
test
**test**
`test`
    ')
) }}
