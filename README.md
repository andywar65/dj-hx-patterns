# dj-hx-patterns
Some patterns I use with Django and HTMX, Python 3.10 and Django 4.1
## Purpose
Experiment some patterns using [HTMX](https://htmx.org/) along with Django. Build reusable apps with typical `CRUD` interactions (see below).
## Installation
If you are on Windows like me, copy the `launch_dj_hx_patterns.ps1` to your computer, modify first three lines to your directory of choice and run the routine. I have `pre-commit` systemwide, if you are not interested delete the line. You can easily convert the file to your favourite command shell.
The routine sets a python virtual environment, downloads the libraries, clones the repository, sets the environment, migrates
the database tables, creates a superuser, populates the tables and runs the server. Enjoy!
## Warning, CBVs!
All views are `Class Based` (this is not mainstream). I have a pair of `HTMX  Mixins`, but I'd like to have more. And maybe template tags.
## Apps
### Box list
Most simple. Add items to a list, modify them inline, change their position. Suitable for related objects.
### Bulk table
Long list with pagination. Modify or delete in bulk.
### Hierarchy
Tree of hierarchical items. Based on fabulous lightweight [django-tree-queries](https://django-tree-queries.readthedocs.io/en/latest/).
### Timeline
A timeline of hierarchical items. Items may have start date or follow parent item.
## TODO
Tests.
