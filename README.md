# dj-hx-patterns
Some patterns I use with Django and HTMX (Python 3.10 and Django 4.2)
## Purpose
Experiment some patterns using [HTMX](https://htmx.org/) along with Django. Build reusable apps with typical `CRUD` interactions (see below).
## Installation
If you are on Windows like me, copy the `launch_dj_hx_patterns.ps1` to your computer, modify first three lines to your directory of choice and run the routine. I have `pre-commit` systemwide, if you are not interested delete the line. You can easily convert the file to your favourite command shell.
The routine sets a python virtual environment, downloads the libraries, clones the repository, sets the environment, migrates
the database tables, creates a superuser, populates the tables and runs the server. Enjoy!
## Warning, CBVs!
All views except in the `Box list` app are `Class Based` (this is not mainstream, I'm still wondering if I have to stick to this rule). I have about three `HTMX  Mixins`, mostly controlling if `HTMX` headers are in the request.
## Apps
### Box list
Most simple. Add items to a list, modify them inline, change their position with [Sortable.js](https://sortablejs.github.io/Sortable/). Suitable for related objects. This app unlike the others uses `Function Based Views`, that I'm starting to appreciate: view workflow is clear, views can perform more tasks.
### Bulk table
Long list with pagination. Modify or delete in bulk. Here an `EventEmitter TemplateView` is used: you have a `hx-post` call for an `UpdateView` with swapping set to `none`. On success `UpdateView` redirects (with parameters) to the `EventEmitterView` that has a void template (nothing to swap, but here I control if `HTMX` headers are in the request) and a `dispatch` method that sends multiple `HX-Trigger` events back to the client.
### Hierarchy
Tree of hierarchical items. Based on fabulous lightweight [django-tree-queries](https://django-tree-queries.readthedocs.io/en/latest/).
### Timeline
A timeline of hierarchical items. Items may have start date or follow parent item.
## Tests
Coverage 99%.
## Template Tags
HTMX is great, but it adds a slight complexity: you can swap just chunks of your `DOM`, targeting a specific element (use tag `hx-target="#<DOM element>"`). This info normally is found in your `Template`, so to get the whole picture of an interaction you have to track both `View` and `Template` content. To bring all logic into the `View`, my first workaround  used `HX-Retarget` header in the `dispatch` method (see also [django-htmx Response Modifying Functions](https://django-htmx.readthedocs.io/en/latest/http.html#response-modifying-functions)), but the approach has debatable results!
### htmx_request tag (not used)
Second approach uses `Templatetags`: first, add `{% load htmx_tags %}` in your template, then use tag `{% htmx_request <request_name> %}` in the element where you want HTMX in action (i.e. `<a {% htmx_request click_me %}>Click me!</a>`). Go to your `View` and add some context data (I use `get_context_data` method because I stick to CBVs), i.e. `context["click_me"] = {"method": "POST", "url": "click/me/", "target": "some-DOM-element"}`. The tag accepts values for `url`, `method` (if blank defaults to `GET`), `target`, `include`, `swap` (swapping method), `push` (if url must be pushed in navigation history, use "true" instead of True), `trigger`, `sync`, `confirm`, `headers` and `vals` (not in evaluate mode), but I'll try to tackle all attributes in the future. The template tag transforms your dictionary into HTMX attributes (as in previous example: `hx-post="click/me/"` and `hx-target="#some-DOM-element"`). All the logic is moved from `Template` to `View`, but this is slightly against Django's architecture: you can leave `url` in template, without adding it in context data (`<a hx-post="click/me/" {% htmx_request click_me %}>Click me!</a>`), as links are normally found in templates.
### htmx_cdn / static tag
Add `{% load htmx_tags %}` in your base template, then use tag `{% htmx_cdn %}` in the `<HEAD>` section. Latest `htmx.min.js` will be downloaded via `CDN` (not recommended for privacy, performance, and security reasons, but it's ok as a first approach). Alternatively use `{% static "project/js/htmx.min.js" %}`, or `{% htmx_static %}`.
### htmx_csrf tag
Always in base template, add the templatetag inside your `<BODY>` tag (`<body {% htmx_csrf %}>`). This will ensure that all requests will carry `CSRFToken` in the header (see [here](https://django-htmx.readthedocs.io/en/latest/tips.html#make-htmx-pass-the-csrf-token) for explanation).
