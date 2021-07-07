from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from random import randrange
import re
from . import util


def search(request):
    entries = util.list_entries()   # list of the existing entries
    results = []                    # list of matched entry from search

    # check if user searched an entry (from sidebar)
    if request.method == "POST":
        # get the user's input
        q = request.POST.get('q').lower()

        # check if q is empty
        if not q:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

        # user searched an entry
        else:
            # loop through the list of existing entries
            for entry in entries:
                # if input matches exactly to an entry,
                # redirect to the entry
                if q == entry.lower():
                    return HttpResponseRedirect(f'/wiki/{entry}')
                # if input is a substring of an entry,
                # add to results
                elif q in entry.lower():
                    results.append(entry)

            # No Match
            if len(results) == 0:
                return render(request, "encyclopedia/search.html", {
                    'title': "No Match",
                    'entries': results,
                    'q': request.POST.get('q')
                })
            
            # display the result
            return render(request, "encyclopedia/search.html", {
                'title': "Search Results",
                'entries': results,
                'q': request.POST.get('q')
            })
    
    # request.method = "GET
    # just bring the user to index
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


# Index Page
def index(request):
    if request.method == "POST":
        # check if user searched an entry from sidebar
        if request.POST.get('q'):
            return search(request)
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Encyclopedia Page
# Entry
def wiki(request, title=""):
    if request.method == "POST":
        # check if user searched an entry from sidebar
        if request.POST.get('q'):
            return search(request)

    # wiki/   => No other path
    if not title:
        return HttpResponseRedirect('/')
        # return render(request, "encyclopedia/wiki.html", {
        #     "title": "Wiki",
        #     "entry": "Welcome to Wiki!"
        # })

    # check if wiki/path is valid
    try:
        markdown(util.get_entry(title))
    except:
        return render(request, "encyclopedia/wiki.html")

    # display the entry
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })


def edit(request, title=""):

    content = util.get_entry(title)
    
    if content == None:
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': content, 
            "errormsg": "Invalid Page"
        })

    if request.method == "POST":
        # check if user searched an entry from sidebar
        if request.POST.get('q'):
            return search(request)

        new_title = request.POST.get('edited_title')
        new_content = request.POST.get('edited_content')
        if  new_title and new_content:
            print(new_title)
            util.save_entry(new_title, new_content)
            return HttpResponseRedirect(reverse('wiki', args=[new_title]))


    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'content': content,
        "errormsg": ""
    })



class CreateForm(forms.Form):   # used to create forms for 'create new' page
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}), label="")
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content'}), label="")



# Create New Page
def new(request):
    errormsg = ""

    # check if user submitted the form
    if request.method == "POST":
        # check if user searched an entry from sidebar
        if request.POST.get('q'):
            return search(request)

        # takes the values from the form
        form = CreateForm(request.POST)
        
        # check if form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            # check if title exists
            if util.get_entry(title) != None:
                errormsg = "Title already exists!"
                return render(request, "encyclopedia/new.html", {
                    "form": CreateForm(),
                    "errormsg": errormsg
                })
            
            # save and display the entry
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')
        
        else:
            errormsg = "Must include valid title and/or content"
            return render(request, "encyclopedia/new.html", {
                "form": CreateForm(),
                "errormsg": errormsg
            })

    # render the 'create new' page 
    return render(request, "encyclopedia/new.html", {
        "form": CreateForm(),
        "errormsg": errormsg
    })


def random(request):
    if request.method == "POST":
        # check if user searched an entry from sidebar
        if request.POST.get('q'):
            return search(request)

    # generate random entry included in entries/
    entriescount = len(util.list_entries())
    randnum = randrange(entriescount)
    title = util.list_entries()[randnum]

    # redirect to the randomly selected entry
    return HttpResponseRedirect(f'/wiki/{title}')



