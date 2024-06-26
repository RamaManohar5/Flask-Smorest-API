from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from restapi.constants.status_codes import HTTP_200_OK

sample_page = Blueprint("sampole_page", __name__, template_folder="templates")

@sample_page.route("/", defaults={"page" :"home"})
@sample_page.route("/<page>")
def show(page):
    try:
        page_title = page.capitalize()
        welcome_note = f"Flask Blueprint Simple Page -{page}.html - change5"
        return render_template(f"{page}.html", welcome_note=welcome_note, page_title=page_title)
    except TemplateNotFound:
        abort(404, description=f"Template {page.capitalize()}.html not found")