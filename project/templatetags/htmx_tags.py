from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def htmx_cdn():
    url = "https://unpkg.com/htmx.org@1.9.0"
    sha = "sha384-aOxz9UdWG0yBiyrTwPeMibmaoq07/d3a96GCbb9x60f3mOt5zwkjdbcHFnKH8qls"
    return mark_safe(
        '<script src="%(url)s" integrity="%(sha)s" crossorigin="anonymous"></script>'
        % {"url": url, "sha": sha}
    )


@register.simple_tag
def htmx_csrf(token):
    return mark_safe('hx-headers=\'{"X-CSRFToken": "%(token)s"}\'' % {"token": token})


METHODS = ["post", "POST"]
SWAP = ["innerHTML", "outerHTML", "none"]


@register.simple_tag
def htmx_request(link_dict):
    output = ""
    if "method" in link_dict and link_dict["method"] in METHODS:
        method = link_dict["method"].lower()
        output += 'hx-%(method)s="%(url)s" ' % {
            "method": method,
            "url": link_dict["url"],
        }
    else:
        output += 'hx-get="%(url)s" ' % {"url": link_dict["url"]}
    if "target" in link_dict:
        if not link_dict["target"].startswith("#"):
            link_dict["target"] = "#" + link_dict["target"]
        output += 'hx-target="%(target)s" ' % {"target": link_dict["target"]}
    if "swap" in link_dict and link_dict["swap"] in SWAP:
        output += 'hx-swap="%(swap)s" ' % {"swap": link_dict["swap"]}
    if "push" in link_dict:
        output += 'hx-push-url="%(push)s" ' % {"push": link_dict["push"]}
    if "trigger" in link_dict:
        output += 'hx-trigger="%(trigger)s" ' % {"trigger": link_dict["trigger"]}
    return mark_safe(output)
