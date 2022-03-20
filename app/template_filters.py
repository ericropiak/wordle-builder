from bs4 import BeautifulSoup

from app.main import app


@app.template_filter('sanitize_html')
def sanitize_html(string_html):
    if not string_html:
        return ''

    soup = BeautifulSoup(string_html, "html.parser")
    safelist = ['a']
    for tag in soup.find_all(True):
        if tag.name not in safelist:
            tag.replaceWith('')
    return soup
