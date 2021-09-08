from django.shortcuts import redirect, render
from .models import Document
from .form import DocumentForm
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.http import HttpResponse


gauth = GoogleAuth()

def my_view(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save() 
            global doc,fname
            doc = newdoc.docfile.path
            fname = newdoc.docfile.name
            fname = fname.split('/')[1]
            url=gauth.GetAuthUrl()
            documents = Document.objects.all()
            context = {'documents': documents, 'form': form,'link':url}
            return render(request, 'home.html', context)
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form}
    return render(request, 'home.html', context)

def callback(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        if code == None:
            return render(request,'callback.html')
        try:
            gauth.Auth(code)
            gauth.SaveCredentialsFile('creds.json')
            drive = GoogleDrive(gauth)
            file1 = drive.CreateFile({'title': fname})
            file1.SetContentFile(doc)
            file1.Upload()
        except pydrive.auth.AuthenticationError:
            messages.error(request, "Authentication Error")
            return redirect('/')
        return redirect('/callback')   
    return render(request,'callback.html')

    