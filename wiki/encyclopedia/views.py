from django.shortcuts import render
import markdown2

from . import util

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
            

    


