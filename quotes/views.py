from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .models import Quote
from .forms import QuoteForm
from pages.models import Page
from pages.views import log_entry
from .utils.file_application import find_application
IP_FILES_PATH = ''


@login_required(login_url=reverse_lazy('login'))
def QuoteList(request):
    documents = []
    typ = []

    documents_full = Quote.objects.all()

    for d in documents_full:
        fn = str(d.jobfile.name)
        fn2, file_extension = os.path.splitext(fn)
        temp = [d.id, d.type, d.title, d.meetingdate, d.submitted, d.jobfile, fn, file_extension]
        documents.append(temp)
        if d.type not in typ:
            typ.append(d.type)

    typ.sort(key=lambda tup: tup[0])
    documents.sort(key=lambda tup: tup[3], reverse=True)

    filename = request.GET.get('filename')

    if not filename:
        # log_entry(request, "Document List Viewed")
        return render(request, 'quotes/quote_list.html', {'data': documents, 'types': typ, 'Page_list': Page.objects.all()})

    fpath = os.path.join(IP_FILES_PATH, filename)
    log_entry(request, "File Downloaded - " + filename, category='Download', importance='Low')
    application = find_application(filename)

    return HttpResponse(
        open(fpath, 'rb'),
        content_type=application,
        headers={
            'Content-Disposition': f"attachment; filename={filename}",
            'Cache-Control': 'no-cache'
        }
    )


@login_required(login_url=reverse_lazy('login'))
def QuoteType(request, pk):
    # print(pk)
    documents = []
    documents_full = Quote.objects.all().filter(type=pk)

    for d in documents_full:
        fn2, file_extension = os.path.splitext(str(d.jobfile))
        temp = [d.id, d.type, d.title, d.meetingdate, d.submitted, d.jobfile, file_extension]
        documents.append(temp)

    documents.sort(key=lambda tup: tup[3], reverse=True)

    filename = request.GET.get('filename')

    if not filename:
        return render(request, 'quotes/quote_type.html', {'data': documents, 'Page_list': Page.objects.all()})

    fpath = os.path.join(IP_FILES_PATH, filename)
    log_entry(request, "File Download - " + filename, category='Download', importance='Low')
    application = find_application(filename)

    return HttpResponse(
        open(fpath, 'rb'),
        content_type=application,
        headers={
            'Content-Disposition': f"attachment; filename={filename}",
            'Cache-Control': 'no-cache'  # files are dynamic, prevent caching
        }
    )


@login_required(login_url=reverse_lazy('login'))
def QuoteDelete(request, pk):
    # print('in quote delete - document id = ', pk)
    data = []
    doc = Quote.objects.all().filter(id=pk)
    if len(doc) > 1:
        log_entry(request, 'document delete returned more than one document', category='System', importance='High')
        return render(request, '404.html', {'Page_list': Page.objects.all()})
    for d in doc:
        # print(d.id, d.type, d.meetingdate, d.jobfile, d.username, len(doc))
        line = [d.id, d.type, d.meetingdate, d.jobfile, d.username]
        data.append(line)
        # print(data)
    return render(request, 'quotes/quote_delete.html', {'data': data, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def delete_file(request, pk):
    file_set = Quote.objects.all().filter(id=pk)
    for f in file_set:
        ftype = f.type
        fname = f.jobfile

        try:
            deleted_count, _ = Quote.objects.filter(id=pk).delete()
            if deleted_count == 0:
                log_entry(request, "No record found on Quotes with ID" + str(pk), category='System', importance='High')
            else:
                os.remove(str(fname))
                log_entry(request, "File Deleted - " + str(fname), category='Delete', importance='Low')

        except Exception as e:
            log_entry(request, "Quote delete exception - " + str(e), category='System', importance='High')

    documents = []
    documents_full = Quote.objects.all().filter(type=ftype)

    for d in documents_full:
        fn2, file_extension = os.path.splitext(str(d.jobfile))
        temp = [d.id, d.type, d.title, d.meetingdate, d.submitted, d.jobfile, file_extension]
        documents.append(temp)

    documents.sort(key=lambda tup: tup[3], reverse=True)

    return render(request, 'quotes/quote_type.html', {'data': documents, 'Page_list': Page.objects.all()})


# Check this out as the possible start of a user admin setup - would need a separate project app
class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


# This is now part of the document upload
@login_required(login_url=reverse_lazy('login'))
def quote_req(request):
    submitted = False
    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            try:
                quote.username = request.user
            except Exception:
                pass
            quote.save()
            log_entry(request, "File Upload" + str(quote.jobfile), category='Upload', importance='Low')

            return HttpResponseRedirect('/quote/?submitted=True')
    else:
        form = QuoteForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'quotes/quote.html', {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})
