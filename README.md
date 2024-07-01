# JSSG - Jtremesay's Static Site Generator

[![CI/CD](https://github.com/jtremesay/jssg/actions/workflows/main.yaml/badge.svg)](https://github.com/jtremesay/jssg/actions/workflows/main.yaml)

The thing that propulse [jtremesay.org](https://jtremesay.org).

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
$ docker build -t jssg .
$ sudo docker run -p 8080:80 jssg:latest
```

## Config

### `settings.py` :
For django settings, see https://docs.djangoproject.com/en/5.0/ref/settings/

Otherwise, you have to configure the following settings :
- `JSSG_DOMAIN` : the domain name of your website, for example `"https://www.example.com"` (used in sitemap file)
- `JSSG_CONTENT_DIR` : a list of directories where look for the site content

### `Dockerfile` :
- In the `# Copy source dir` section, add `COPY <content-dir>/ <content-dir>/` for each content directory in `JSSG_CONTENT_DIR`

### `views.py` :
- In the `get_object` method of `IndexView`, set the `self.kwargs["slug"]` to the slug of your index page which is sent at the root of your site

## Usage

Each directory defined in `JSSG_CONTENT_DIR` has the following structure :
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
For Django engine : https://docs.djangoproject.com/en/5.0/ref/templates/language/ \
For Jinja2 engine : https://jinja.palletsprojects.com/en/2.11.x/templates/

`page.html` and `post.html` are the firsts templates called to render a page or a post. In these templates, the content of a page is accessible by `object.content`. By default, they extend the `base.html` template.

### Pages :
Pages contain the content of each web page of the site at `pages/<slug>.html`. They are `.md` files and are structured in 3 sections separated by a line starting with `---` :

- **Metadata** provide some informartion about the page (description, language...). Each metadata is a key, some spaces, and a value. The `title` metadata is required for all pages. `slug`, `lang`, `engine` or open graph metadata can also be useful. Metadata are accessible by a dictionary in `object.metadata` in templates.
- **Data** is a section which contains a JSON text. It is accessible by `object.data` in templates.
- **Body** : It is the concrete content of the page, that can be html or template content. For example, it is possible to use widgets or blocks in this section.

### Posts :
Like pages, they contain the content of each post at `posts/<slug>.html`. They require an additional metadata `date` in ISO format.

### Static :
This directory is for the static content, like images, CSS and JavaScript files ...
It is accessible in templates by the `static` function.

## Others

This repo is a fork of https://github.com/jtremesay/jssg.git for algoo websites use cases.
