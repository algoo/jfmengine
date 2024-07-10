# Examples of blocks usage :
## With language as version  
For instance, you could have different version of a widget `jinja2/widgets/navbar.html` :
```jinja
{% macro navbar(
      LINK1 = "", TEXT1 = "",
      LINK2 = "", TEXT2 = "",
      LINK3 = "", TEXT3 = "",
)
%}
<nav>
    <a href="{{ LINK1 }}">{{ TEXT1 }}</a> |
    <a href="{{ LINK2 }}">{{ TEXT2 }}</a> |
    <a href="{{ LINK3 }}">{{ TEXT3 }}</a>
</nav>
{% endmacro %}
```

A block `jinja2/blocks/en/navbar.html` :
```jinja
{% from "widgets/navbar.html" import navbar %}

{{ navbar(
      LINK1 = "/index.html", TEXT1 = "Home",
      LINK2 = "/contact.html", TEXT2 = "Contact us",
      LINK3 = "/login/connect.html", TEXT3 = "Connexion",
  ) }}
```
A block `jinja2/blocks/fr/navbar.html` :
```jinja
{% from "widgets/navbar.html" import navbar %}

{{ navbar(
      LINK1 = "/index.html", TEXT1 = "Accueil",
      LINK2 = "/contact.html", TEXT2 = "Contactez-nous",
      LINK3 = "/login/connect.html", TEXT3 = "Connexion",
  ) }}
```

In `base.html`, we can include a navbar which depends of each page language by :
```jinja
{% from "blocks/block.html" import block %}

{{ block(
    NAME = "navbar",
    VERSION = object.metadata.lang|default(""),
    DEFAULT_NAME = "en/navbar.html"
) }}
```
For all pages, if the page contains the metadata `lang` then the block will be searched as `blocks/<lang>/navbar.html`, and will be `blocks/en/navbar.html` if not found.\
Else, the `default("")` filter allow to overpass the error and the block will be searched as `blocks/navbar.html`, and will be `blocks/en/navbar.html` if not found.\

## With user levels as version :
For this example, we have a widget that prints information about user in `jinja2/widgets/profile.html` :
```jinja
{% macro profile(
      USER_TYPE = "guest", 
)
%}
<div>
    <h2> {{ USER_TYPE }} profile </h2>
    {% if user_type == 'admin' %}
    <p>Status : Administrator</p>
    {% else %}
    <p>Status : Guest user</p>
    {% endif %}
</div>
{% endmacro %}
```
With two version of blocks `jinja2/blocks/admin/profile.html` and `jinja2/blocks/guest/profile.html` :
```jinja
{% from "widgets/profile.html" import profile %}

{{ profile(USER_TYPE = "admin") }}
```
```jinja
{% from "widgets/profile.html" import profile %}

{{ profile() }}
```
And finally we can use this blocks with :
```jinja
{% from "blocks/block.html" import block %}

{{ block(
    NAME = "profile"
    VERSION = "admin"
)}}

{{ block(
    NAME = "profile"
    VERSION = "guest"
)}}
```
