from django.shortcuts import render
from django.utils.text import slugify
from lxml import html, etree

from pages.models import HelpPages

def get_left_menu(current_page=None):
    left_menu = HelpPages.objects.filter(parent_page=None, status=1).values()
    for page in left_menu:
        page['has_subs'] = HelpPages.objects.filter(parent_page_id=page['id'], status=1).exists()
        page['opened'] = True if current_page and current_page.id is page['id'] else False
        page['is_selected'] = True if current_page and current_page.id is page['id'] else False
        page['subs'] = HelpPages.objects.filter(parent_page_id=page['id'], status=1).values()
        for sub_page in page['subs']:
            sub_page['has_subs'] = HelpPages.objects.filter(parent_page_id=sub_page['id'], status=1).exists()
            if current_page and current_page.id is sub_page['id']:
                sub_page['is_selected'] = True
                page['opened'] = True
            else:
                sub_page['is_selected'] = False
    return left_menu

def home(request):
    my_list = []
    left_menu = get_left_menu()
    page_title = "Помощь"
    next_page = HelpPages.objects.filter(parent_page=None, status=1)[0]

    all_pages = HelpPages.objects.filter(parent_page=None, status=1).values()
    for page in all_pages:
        page['has_subs'] = HelpPages.objects.filter(parent_page_id=page['id'], status=1).exists()
        page['subs'] = HelpPages.objects.filter(parent_page_id=page['id'], status=1).values()
    return render(request, "home/index.html", locals())


def page(request, slug):
    my_list = []
    page = HelpPages.objects.get(slug=slug)
    left_menu = get_left_menu(page)
    page_title = page.title

    anchors = None
    if page.content:
        content_html = html.document_fromstring(page.content)
        anchors = content_html.cssselect("h2")
        setted_anchors = []
        for anchor in anchors:
            if anchor.text and anchor.text != "":
                anchor_link = slugify(anchor.text, allow_unicode=True)
                if anchor_link in setted_anchors:
                    anchor_link = "{}_".format(anchor_link)

                anchor.attrib['id'] = anchor_link
                anchor.insert(0, etree.XML('<a href="#{}" class="anchor">#</a>'.format(anchor_link)))
                setted_anchors.append(anchor_link)

        page.content = html.tostring(content_html,encoding='unicode', pretty_print=True,)

    sub_pages = HelpPages.objects.filter(parent_page=page)

    # Next Page
    if HelpPages.objects.filter(parent_page_id=page.parent_page_id, status=1, tree_id__gt=page.tree_id).exists():
        next_page = HelpPages.objects.filter(parent_page_id=page.parent_page_id, status=1, tree_id__gt=page.tree_id)[0]
    elif page.parent_page and HelpPages.objects.filter(parent_page=None, status=1, tree_id__gt=page.parent_page.tree_id).exists():
        next_page = HelpPages.objects.filter(parent_page=None, status=1, tree_id__gt=page.parent_page.tree_id)[0]
    if HelpPages.objects.filter(parent_page_id=page.id, status=1).exists():
        next_page = HelpPages.objects.filter(parent_page_id=page.id, status=1)[0]
    # Previous Page
    if HelpPages.objects.filter(parent_page_id=page.parent_page_id, status=1, tree_id__lt=page.tree_id).exists():
        prev_page = HelpPages.objects.filter(parent_page_id=page.parent_page_id, status=1, tree_id__lt=page.tree_id).last()
        if HelpPages.objects.filter(parent_page_id=prev_page.id, status=1).exists():
            prev_page = HelpPages.objects.filter(parent_page_id=prev_page.id, status=1).last()
    elif page.parent_page:
        prev_page = page.parent_page
    else:
        prev_page = {'title':"Помощь"}

    return render(request, "page/index.html", locals())