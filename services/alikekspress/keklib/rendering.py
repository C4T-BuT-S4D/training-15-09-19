from flask import render_template_string


def render_template(template_name, **kwargs):
    with open('templates/' + template_name) as f:
        template = f.read()
    return render_template_string(template.format(**kwargs), **kwargs)
