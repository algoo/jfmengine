# JFM-Engine

Today, it's a django app that can generate a static website with Vite & Typescript integration.

## Bootstrap

```shell
$ git clone https://github.com/algoo/jssg.git
$ cd jssg
$ python3.9 -m venv env/
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

## Prod

Note: if you use `direnv`, the environment variable `DJANGO_DEBUG` is set to `true`. You must then prefix tho following commands with `DJANGO_DEBUG=false`.

```shell
$ npm run build
$ ./manage.py distill-local --collectstatic --force dist
```

Or, if you prefer docker:

```shell
$ sudo docker build -t jssg .
$ sudo docker network create traefik_public
$ sudo docker compose up
```

## Config

### `settings.py` :
For django settings, see https://docs.djangoproject.com/en/5.0/ref/settings/

Otherwise, you have to configure the following settings :
- `JFME_DOMAIN` : the domain name of your website, for instance `"https://www.example.com"` (used in sitemap file)
- `JFME_CONTENT_DIRS` : a list of directories where to look for the site content

Other useful settings :
- Default metadata : `JFME_DEFAULT_METADATA_DICT` and `JFME_DEFAULT_METADATA_FILEPATH` allow to set default metadata for pages and posts. The first one is a python dictionary and the second one is a Path to a file having the same format as metadata section in pages.
The order, from less to most priority is : `JFME_DEFAULT_METADATA_DICT` then `JFME_DEFAULT_METADATA_FILEPATH` then page matadata.

### `Dockerfile` :
- In the `# Copy source dir` section, add `COPY <content-dir>/ <content-dir>/` for each content directory in `JFME_CONTENT_DIRS`

### `views.py` :
- In the `get_object` method of `IndexView`, set the `self.kwargs["slug"]` to the slug of your index page which is sent at the root of your site

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
    |       |-- base.html
    |       |-- page.html
    |       |-- post.html
    |       |-- sitemap.html
    |-- pages/
    |-- posts/
    |-- static/
```

### Templates :
For Django engine, see https://docs.djangoproject.com/en/5.0/ref/templates/language/ \
For Jinja2 engine, see https://jinja.palletsprojects.com/en/2.11.x/templates/

`page.html` and `post.html` are the firsts templates called to render a page or a post. By default, they extend the `base.html` template.

### Pages :
Pages contain the content of each web page of the site at url `pages/<slug>.html`. They are `.md` files and are structured in 3 sections separated by a line starting with `---` :

- **Metadata** provide some informartion about the page (description, language...). Each metadata is a key, some spaces, and a value. The `title` metadata is required for all pages. Other metadata can be useful, like `slug`, `lang`, `template_engine` or `og:<key>` (open graph). Metadata are accessible by a dictionary in `object.metadata` in templates.
- **Data** is a section which contains a JSON text. It is accessible by `object.data` in templates.
- **Body** : It is the concrete content of the page, that can be html or template content. For instance, it is possible to use widgets or blocks in this section. It is accessible by `object.content` in templates.

### Posts :
Like pages, they contain the content of each post at url `posts/<slug>.html`. They require an additional metadata `date` in ISO format

### Static :
This directory is for the static content, like images, CSS and JavaScript files ... \
It is accessible in templates by the Jinja or Django `static` function. \
See the [Django doc](https://docs.djangoproject.com/en/5.0/howto/static-files/#configuring-static-files) for static files, or the [Jinja2 version](https://docs.djangoproject.com/en/5.0/topics/templates/#module-django.template.backends.django).

### Blocks or widgets
Widgets are reusable templates used to factor some content in pages. Widgets will be searched in the templates directories, in `<django|jinja2>/widgets/`

Blocks are parts of content that can have multiple versions.
They have no parameter as they use widgets when necessary.
It is possible to use the macro `block(NAME, [VERSION], [DEFAULT_NAME])`, to include a bloc and specify its version. In this case, the block will be searched in the templates directories, in `<django|jinja2>/blocks/<block-version>/` .

The `VERSION` and `DEFAULT_NAME` arguments of `block()` are optionnal.\
If no `VERSION` is given, the block will be searched directly in `blocks/`.

For `VERSION`, you can use page metadata, jinja variables, or just strings.

For examples, see `EXAMPLES.md`.

## CLI
For each command, the option `-h` give u some help.

 `./manage.py runserver` to run the dev server, see [Dev](#dev) for usage

 `./manage.py distill-local` to make the static website, see [Prod](#prod) for usage

 `./manage.py list-widgets` to list all widgets found in content directories

 `./manage.py make-widgets` to make a file that groups all jinja2 widgets macros for easier includes. It is automatically called by `runserver` and `distill-local` commands. \
 See an example in `EXAMPLE.md`

## Others

JFM-Engine is a friendly fork of [JSSG](https://github.com/jtremesay/jssg/) made in agreement with the JSSG developer because of different goals. \
See the [issue #21](https://github.com/jtremesay/jssg/issues/21).
