from django.shortcuts import render,redirect
import markdown
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,name):
    entry=util.get_entry(name)
    if entry is None:
        return render(request, "encyclopedia/error.html" ,{
            "message":f"Entry with the name of '{name.capitalize()}' not found"
        })
    entry_content=markdown.markdown(entry)
    return render(request, "encyclopedia/entry.html",{
        "name":name,
        "content":entry_content
    })

def search(request):
    q = request.GET.get('q', '')
    entry=util.get_entry(q)
    if entry:
        return redirect('entry',name=q)

    entries=util.list_entries()
    matching_entries=[entry for entry in entries if q.lower() in entry.lower()]


    return render(request, "encyclopedia/search.html" ,{
        "name":q,
        "content": matching_entries
    })
def create(request):
    if request.method=="GET":
        return render(request, "encyclopedia/create.html")
    else:
        title=request.POST['title']
        content=request.POST['content']
        allenteries=util.list_entries()
        enterieslower=[]
        for entry in allenteries:
            enterieslower.append(entry.lower())
        if title.lower() in enterieslower:
            return render (request, "encyclopedia/error.html",{
                "message":"File name already exists"
            })
        else:
            util.save_entry(title,content)
            dcontent=markdown.markdown(content)
            return render(request,"encyclopedia/entry.html",{
                "name":title,
                "content":dcontent
            })

def edit(request):
    if request.method=="POST":
        title=request.POST['title']
        entry=util.get_entry(title)
        return render(request, "encyclopedia/edit.html" ,{
            "title":title,
            "content":entry
        })
def save_edit(request):
    if request.method=="POST":
        title=request.POST['title']
        content=request.POST['content']
        util.save_entry(title,content)
        dcontent=markdown.markdown(content)
        return render(request,"encyclopedia/entry.html",{
            "name":title,
            "content":dcontent
            })
def random_entry(request):
    title=util.list_entries()
    utitle=random.choice(title)
    ucontent=util.get_entry(utitle)
    content=markdown.markdown(ucontent)
    return render(request, "encyclopedia/entry.html", {
        "name":utitle,
        "content":content
    })

