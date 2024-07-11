# Exemple for automatic widget inclusion

First you can verify that all widgets are found with the `listwidget` command.\
Then the `makewidget` command will create a file `content/templates/<engine>/allwidgets.html`, that groups all the widgets found, and is automatically imported as `widgets` in all pages.\

The line `{% import 'allwidgets.html' as widgets %}` is added at the beginning of each `Body` section of pages.

For instance, if we have 3 widgets : `navbar.html`, `header.html` and `footer.html` we can use them in pages :

```jinja
{{ widgets.navbar(...) }}
{{ widgets.header(...) }}
{{ widgets.footer(...) }}
```