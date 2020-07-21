import random
import re

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class PageForm(forms.Form):
    title = forms.CharField(
        label="Title:",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Wiki Page Title",
                "class": "form-control"
            }
        )
    )
    content = forms.CharField(
        label="Content:",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Wiki Page Content",
                "class": "form-control"
            }
        )
    )

def heading_markdown_to_html(match):
    heading_deliminator, heading_text = match.groups()
    heading_num = str(len(heading_deliminator))

    return f"<h{heading_num}>{heading_text}</h{heading_num}>"

def markdown(markdown):
    heading_pattern = re.compile(r"^\s*(#+) (.+?)\s*$", re.MULTILINE)
    markdown = heading_pattern.sub(heading_markdown_to_html, markdown)

    bold_pattern = re.compile(r"\*\*(.+?)\*\*")
    markdown = bold_pattern.sub(r"<strong>\1</strong>", markdown)

    unordered_list_pattern = re.compile(r"(^[*-] .+?)\n[^*-]", re.MULTILINE|re.DOTALL)
    markdown = unordered_list_pattern.sub(r"<ul>\n\1\n</ul>", markdown)

    list_item_pattern = re.compile(r"^\s*[*-] (.+?)\s*$", re.MULTILINE)
    markdown = list_item_pattern.sub(r"<li>\1</li>", markdown)

    link_pattern = re.compile(r"\[(.+?)\]\((\S+?)\)")
    markdown = link_pattern.sub(r"<a href='\2'>\1</a>", markdown)

    paragraph_pattern = re.compile(r"^\s*([^<].*?)\s*$", re.MULTILINE)
    markdown = paragraph_pattern.sub(r"<p>\1</p>", markdown)

    return markdown

def index(request):
    query = ""
    if request.method == "POST":
        query = request.POST.get("q")
        entry = util.get_entry(query)
        if entry is not None:
            return HttpResponseRedirect(reverse("entry", kwargs={"title": query}))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(query)
    })

def entry(request, title):
    markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })   

def create_new_page(request):
    error = False
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        entry = util.get_entry(title)
        if entry is None:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

        error = True

    return render(request, "encyclopedia/create.html", {
        "form": PageForm(), 
        "error": error
    })

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    form = PageForm({
        "title": title,
        "content": util.get_entry(title)
    })
    form.fields["title"].widget.attrs['disabled'] = True

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
