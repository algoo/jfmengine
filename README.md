# JFM-Engine

Today, it's a django app that can generate a static website with Vite & Typescript integration.

## Bootstrap

```shell
$ git clone https://github.com/algoo/jssg.git
$ cd jssg
$ python3.12 -m venv env/
$ source env/bin/activate
$ direnv allow
$ npm install
$ pip install -Ur requirements.txt
```

## Dev

You need to run BOTH npm and the django server. Npm will transpile the typescript code on the fly and provide hot reloading.

Note: if you use `direnv`, the environment variable `DJANGO_DEBUG` is set to `true`. No need to prefix the commands with `DJANGO_DEBUG=true`.

```shell
$ DJANGO_DEBUG=true npm run dev
```

```shell
$ DJANGO_DEBUG=true ./manage.py runserver
```
Then you can acess the dev server at `localhost:8000`.

## Prod

Note: if you use `direnv`, the environment variable `DJANGO_DEBUG` is set to `true`. You must then prefix tho following commands with `DJANGO_DEBUG=false`.

```shell
$ npm run build
$ ./manage.py distill-local --collectstatic --force dist
```
Then the static site will be available in `dist/`.

Or, if you prefer docker:

```shell
$ sudo docker build -t jssg .
$ sudo docker network create traefik_public
$ sudo docker compose up
```
With docker the server is accessible at `localhost:8003`

## Config

### `settings.py` :
For django settings, see https://docs.djangoproject.com/en/5.0/ref/settings/

#### Otherwise, you have to configure the following settings :
- `JFME_DOMAIN` : the domain name of your website, for instance `"https://www.example.com"` (used in sitemap file)
- `JFME_CONTENT_DIRS` : a list of directories where to look for the site content. Add yours to the list `[BASE_DIR / "content"]`. \
Example : `JFME_CONTENT_DIRS = [BASE_DIR / "content"] + [Path("/home/me/my-content")]`
- `JFME_PAGE_INDEX` : the page that will be printed at url `"/"`, for instance `"fr/index/accueil"` will be the page in `pages/fr/index/` with the slug `accueil`

#### Other useful settings :
- **Default metadata :** `JFME_DEFAULT_METADATA_DICT` and `JFME_DEFAULT_METADATA_FILEPATH` allow to set default metadata for pages and posts. The first one is a python dictionary and the second one is a Path to a file having the same format as metadata section in pages.
The order, from less to most priority is : `JFME_DEFAULT_METADATA_DICT` then `JFME_DEFAULT_METADATA_FILEPATH` then page metadata.
- **Required metadata :** `JFME_REQUIRED_METADATA` allow to set metadata that are checked with `check-metadata` command. If some of them are missing or empty, the commend will print it in verbose mode (`--verbose`)
- **Date format in `sitemap.xml` :** the `JFME_SITEMAP_LASTMOD_DATETIME_FORMAT` setting allow to give a format for the `<lastmod>` tag in sitemap. The [allowed format](https://www.sitemaps.org/protocol.html#lastmoddef) are given in Python [`strftime` format](https://docs.python.org/fr/3.6/library/datetime.html#strftime-and-strptime-behavior).
- **Posts pagination :** `JFME_NUMBER_OF_POSTS_BY_PAGE` give the maximum number of posts in a posts list page. If set to 0 or -1, all posts will be in the first page.
- **`JFME_ADDITIONAL_JINJA2_FUNCTIONS` :** a dict of function name as key and string of python module as value, to add Jinja2 functions. \
For instance `{"base64encode": "jssg.templatetags.base_64.base64encode", "md_readtime": "readtime.of_markdown"}` will add :
    -  the `base64encode` function in `jssg/templatetags/base_64.py`
    - `of_markdown` function of `readtime` module as `md_readtime` Jinja2 function
- **`JFME_ADDITIONAL_JINJA2_FILTERS`** same as `JFME_ADDITIONAL_JINJA2_FUNCTIONS`, but for Jinja2 filters

### `Dockerfile` :
- In the `# Copy source dir` section, add `COPY <content-dir>/ <content-dir>/` for each content directory in `JFME_CONTENT_DIRS`

## Usage

Each directory defined in `JFME_CONTENT_DIRS` has the following structure :
```
Content-dir/
    |-- templates/
    |   |-- django/
    |   |   |-- blocks/
    |   |   |-- widgets/
    |   |-- jinja2/
    |       |-- blocks/
    |       |-- widgets/
    |-- pages/
    |-- posts/
    |-- static/
```

### Templates :
For Django engine, see https://docs.djangoproject.com/en/5.0/ref/templates/language/ \
For Jinja2 engine, see https://jinja.palletsprojects.com/en/2.11.x/templates/ \
**Jinja2 templates are recommended**

`page.html` and `post.html` are the firsts templates called to render a page or a post. By default, they extend the `base.html` template.\
You can override default templates by placing your content directories before `content/` in `JFME_CONTENT_DIRS`

#### In Jinja2 templates, you can use :
- `static()` function to reach a static content \
example: `{{ static('css/styles.css') }}` will be replaced by the url for the stylesheet : `'/static/css/styles.css'`
- `url_for_slug()` function to reach an url of a page with his slug \
example: `{{ url_for_slug('accueil') }}` will be replaced by `'/fr/acceuil'` 
- `url_for_slug_path()` function to reach an url of a page with his slug path (used when a slug is duplicated in two different folders) \
example: `{{ url_for_slug_path('/fr/accueil') }}` will be replaced by `'/fr/acceuil'`
- `filter_opengraph_metadata` to filter all open-graphe metadata in metadata \
example: `{% for key, value in object.metadata.items() | filter_opengraph_metadata %}` will browse all open-graph metadata
- `markdown` tag or function, to write content in markdown \
examples: `{% markdown %}**This is strong**{% endmarkdown %}`, `{{ markdown('# this is title') }}` \
The tag allow you to write multiline markdown easily, but the function can be given in parameter, for instance in a widget. 

For `url_for_slug()` and `url_for_slug_path()`, see doc in `jssg/templatetags/functions_url.py`

### Pages :
Pages contain the content of each web page of the site at url `pages/<page-path>/<slug>.html`. They are `.md` files and are structured in 3 sections separated by a line starting with `---` :

- **Metadata** provide some informartion about the page (description, language...). Each metadata is a key, some spaces, and a value. The `title` metadata is required for all pages. Some other metadata can be useful, like `slug`, `lang`, `template_engine` or `og:<key>` (open graph). Metadata are accessible by a dictionary in `object.metadata` in templates.
- **Data** is a section which contains a JSON text. It is accessible by `object.data` in templates.
- **Body** : It is the concrete content of the page, that can be html or template content. For instance, it is possible to use widgets or blocks in this section. It is accessible by `object.content` in templates.

### Posts :
Like pages, they contain the content of each post at url `posts/<slug>.html`. They require an additional metadata `date` in ISO format.
The default templates also use `abstract`, `author`, and `category` metadata.

### Static :
This directory is for the static content, like images, CSS and JavaScript files ... \
It is accessible in templates by the Jinja or Django `static` function. \
See the [Django doc](https://docs.djangoproject.com/en/5.0/howto/static-files/#configuring-static-files) for static files, or the [Jinja2 version](https://docs.djangoproject.com/en/5.0/topics/templates/#module-django.template.backends.django).

### Blocks or widgets
**Widgets** are reusable templates used to factor some content in pages. Widgets will be searched in the templates directories, in `<django|jinja2>/widgets/`.\
They are generally Jinja2 macros, and if so, are automatically imported in pages and posts (see `EXAMPLES.md`).

**Blocks** are parts of content that can have multiple versions.
They have no parameter as they use widgets when necessary.
It is possible to use the macro `block(NAME, [VERSION], [DEFAULT_NAME])`, to include a bloc and specify its version. In this case, the block will be searched in the templates directories, in `<django|jinja2>/blocks/<block-version>/` .\
The `VERSION` and `DEFAULT_NAME` arguments of `block()` are optionnal. If no `VERSION` is given, the block will be searched directly in `blocks/`. For `VERSION`, you can use page metadata, jinja variables, or just strings.
For examples, see `EXAMPLES.md`.

## CLI
For each command, the option `-h` give u some help.

- `./manage.py runserver` to run the dev server, see [Dev](#dev) for usage
- `./manage.py distill-local` to make the static website, see [Prod](#prod) for usage
- `./manage.py check-metadata` to check if metadata set in `JFME_REQUIRED_METADATA` are missing or empty in pages
- `./manage.py list-widgets` to list all widgets found in content directories. See an example in `EXAMPLES.md`.
- `./manage.py format-html <action>` to minify or beautify the html content (`<action>` being `minify` or `beautify`)

## Others

JFM-Engine is a friendly fork of [JSSG](https://github.com/jtremesay/jssg/) made in agreement with the JSSG developer Jonathan Tremesaygues because of different goals. \
See the [issue #21](https://github.com/jtremesay/jssg/issues/21).
