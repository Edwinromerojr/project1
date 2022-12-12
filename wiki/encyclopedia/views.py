from django.shortcuts import render
import markdown2
import random

from . import util

#convertion markdown to html
def converter(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Entry Page
def entry(request, title):
    Converted_html = converter(title)
    if Converted_html == None:
        return render(request, "encyclopedia/warning.html", {
            "error": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": Converted_html
        })

#Search
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        Converted_html = converter(entry_search)
        if Converted_html is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entry_search,
            "content": Converted_html
            })
        else:
            Allentries = util.list_entries()
            recommend = []
            for entry in Allentries:
                if entry_search.lower() in entry.lower():
                    recommend.append(entry)
            return render(request, "encyclopedia/recommendation.html", {
                "recommend": recommend
            })

#Creating New Page            
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newp.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/warning.html", {
                "error": " This page is already exist"
            })
        else:
            util.save_entry(title, content)
            Converted_html = converter(title)
            return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": Converted_html
        })

#Edit Page
def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        Converted_html = converter(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": Converted_html
        })

#Random page
def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    Converted_html = converter(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": Converted_html
    })

    
    

    


