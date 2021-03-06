---
title: Integrating Bootstrap into my Website
categories: [projects, homepage]
tags: [html, css, js, bootstrap]
---
Bootstrap is a CSS and JS library that makes it a lot faster to build websites.
Similar to how python packages reduce code redundancy and allow for more complexity
in less time, Bootstrap packages functionality into a set of class namespaces.
This post documents the integration of Bootstrap into my website.

#### Dec 30, 2018
## Rationale
I figure some of the boilerplate that I'm writing in SASS right now is almost certainly included in Bootstrap.
Now that I understand SASS and CSS better, I'm going to switch over to Bootstrap and try
 to refactor my code to take advantage of the Bootstrap formatting.

#### Jan 3, 2018
## Library CDN {% include refc-small commit="3cad96569b964c415cd98a3b66aed73c01d87113" %}
I'm using the bootstrap CDN, so I made the files `bootstrap/bootstrap.css.html`
and `bootstrap/bootstrap.js.html`, which contain the code to load the bootstrap assets from the CDN.

```html
<!-- src/_includes/bootstrap/bootstrap.css.html -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

<!-- src/_includes/bootstrap/bootstrap.js.html -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
```

These files are included in the layout `base.html` and the include `head.html`, which are used by all pages in the site:
```html
<!-- head.html -->
<head>{% raw %}
    ...
    {% include bootstrap/bootstrap.css.html %}
    ...
</head>

<!-- base.html-->
<body>
    ...
    {% include bootstrap/bootstrap.js.html %}
</body>{% endraw %}
```

#### January 5, 2018
## Rewriting HTML & CSS {% include refc-small commit="67e067a2bbc12b836652552137c1eb8a3889c7c9" %}
I used the [Bootstrap Grid Documentation][bs-grid-docs] and [a tutorial by sentdex][sentdex-bootstrap]
to help me refactor my original HTML based on Bootstrap standards. The whole page is
put in a `container-fill` div with `style="height:100%"`, which represents the container for everything,
including the header and footer.

[bs-grid-docs]: https://getbootstrap.com/docs/4.0/layout/grid/
[sentdex-bootstrap]: https://pythonprogramming.net/design-bootstrap-django-python-tutorial/

Within this container, the site is laid out in 3 rows:

{% raw %}
```html
<div class="container-fill" style="height:100%;">
    <div class="row header" id="header">
        <!-- Header content -->
    </div>
    <div class="row main {{ page-title }} {{ extra }}" id="main-content">
        {{ content }}
    </div>
    <div class="row footer" id="footer">
        <!-- Footer content -->
    </div>
</div>
```
{% endraw %}
{% raw %}
The values in `{{curly brackets}}` get filled according to page attributes.
{% endraw %}

* **`extra`** - If the page has the `short` keyword set to `true`, then this evaluates to ` short-page`,
a class which has been styled with `height: 100%;` to cause shorter pages to fill the whole screen.
* **`page-title`** - equivalent to a lowercase, hyphenated version of the page title with `-page` appended to the end.
* **`content`** - Content of the page.

Additionally, the formatting of the content row div element changes based on attributes of the page.
Unless the page has the `raw` keyword set to `true` (or another truthy value),
the main row renders a little differently:

{% raw %}
```html
<div class="row {{ extra }}" id="main-content">
        <div class="col" id="left-col">
            {% include {{ page.left }} %}
        </div>

        <div class="col-8 main {{ page-title }}" id="main-col">
            {{ content }}
        </div>

        <div class="col" id="right-col">
            {% include {{ page.right }} %}
        </div>
</div>
```
{% endraw %}
The new variables evaluate to include file names:

* **`page.left`** - the file name to an include to insert at the left of the site.
Actual source also includes error catching.
* **`page.right`** - the file name to an include to insert at the right of the site.
Actual source also includes error catching.

Regardless of whether `raw: true` is set, the page object's CSS styles are applied to the div element
that its content is inserted into.

#### Rewriting SASS {% include refc-small commit="67e067a2bbc12b836652552137c1eb8a3889c7c9" %}
This stuff is pretty minimal. For the most part I just removed lines that are covered by the bootstrap formatting.
In addition though, I changed the shadow mixin: now it doesn't have a `$code` argument.
Besides that, it shouldn't be much more complicated.
