from django.shortcuts import render, redirect
import markdown2
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page '{title}' was not found."
        })
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    for entry_name in entries:
        if query.lower() == entry_name.lower():
            return redirect('entry', title=entry_name)
    results = [entry_name for entry_name in entries if query.lower() in entry_name.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": f"An encyclopedia entry with the title '{title}' already exists."
            })
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        util.save_entry(title, content)
        return redirect('entry', title=title)

    # For a GET request, pre-populate the text area
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page '{title}' was not found."
        })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect('entry', title=random_title)

def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": f"An encyclopedia entry with the title '{title}' already exists."
            })
            
        # THE FIX: Automatically prepend the title as a Markdown heading if the user didn't type one
        if not content.startswith("#"):
            content = f"# {title}\n\n{content}"

        util.save_entry(title, content)
        return redirect('entry', title=title)
        
    return render(request, "encyclopedia/create.html")