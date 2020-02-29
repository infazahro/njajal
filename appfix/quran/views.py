from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q   
from .models import Qori, Murotal 
from .forms import QoriForm, MurotalForm, UserForm


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if not request.user.is_authenticated(): 
        return render(request, 'quran/login.html')
    else:
        qoris = Qori.objects.filter(user=request.user)
        murotal_results = Murotal.objects.all()
        query = request.GET.get("q")
        if query:
            qoris = qoris.filter(
                Q(juz__icontains=query) |   
                Q(nama_qori__icontains=query)
            ).distinct()
            murotal_results = murotal_results.filter(
                Q(surah__icontains=query)
            ).distinct()
            return render(request, 'quran/index.html', {
                'qoris': qoris,
                'murotals' : murotal_result,
            })
        else:
            return render(request, 'quran/index.html', {'qoris': qoris})

def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
          if user.is_active:
              login(request, user)
              qoris = Qori.objects.filter(user=request.user)
              return render(request,'quran/index.html',{'qoris': qoris})
          else:
              return render(request, 'quran/login.html', {'error_message': 'Akun Anda telah dinonaktifkan'})
        else:
            return render(request, 'quran/login.html', {'error_message': 'Invalid login'})
    return render(request, 'quran/login.html')

 
def detail(request, qori_id):

    if not request.user.is_authenticated():
        return render(request, 'quran/login.html')
    else:
        user = request.user
        qori = get_object_or_404(Qori, pk=qori_id)
        return render(request, 'quran/detail.html', {'qori': qori, 'user': user})


def favorite(request, murotal_id): 

    murotal = get_object_or_404(Murotal, pk=murotal_id)
    try:
        if murotal.is_favorite:
            murotal.is_favorite = False
        else: 
            murotal.is_favorite = True
        murotal.save()
    except (KeyError, Murotal.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_qori(request, qori_id):

    qori = get_object_or_404(Qori, pk=qori_id)
    try:  
        if qori.is_favorite:
            qori.is_favorite = False
        else: 
            qori.is_favorite = True
        qori.save()
    except (KeyError, Qori.DoesNotExist):
        return JsonResponse({'success': False}) 
    else:
        return JsonResponse({'success': True})


def murotals(request, filter_by):

    if not request.user.is_authenticated():
        return render(request, 'quran/login.html')
    else:
        try:
            murotal_ids = [] 
            for qori in Qori.objects.filter(user=request.user):      
                for murotal in qori.murotal_set.all():    
                    murotal_ids.append(murotal.pk)
            users_murotals = Murotal.objects.filter(pk__in=murotal_ids)
            if filter_by == 'favorites':
                users_murotals = users_murotals.filter(is_favorite=True) 
        except Qori.DoesNotExist:
            users_murotals = []
        return render(request, 'quran/murotals.html', { 
            'murotal_list': users_murotals,
            'filter_by': filter_by,
        })


def logout_user(request):

    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'quran/login.html', context)


def register(request):

    form = UserForm(request.POST or None) 
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                qoris = Qori.objects.filter(user=request.user)
                return render(request, 'quran/index.html', {'qoris': qoris})
    context = {
        "form": form,
    }
    return render(request, 'quran/register.html', context)

 
def create_qori(request):

    if not request.user.is_authenticated():
        return render(request, 'quran/login.html')
    else:
        form = QoriForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            qori = form.save(commit=False)
            qori.user = request.user 
            qori.gambar = request.FILES ['gambar']
            file_type = qori.gambar.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'qori': qori,
                    'form': form,
                    'error_message': 'gambar harus format PNG, JPG or JPEG'
                }
                return render(request, 'quran/create_qori.html', context)
            qori.save()
            return render(request,'quran/detail.html',{'qori': qori})
        context = {
            "form": form
        }
        return render(request, 'quran/create_qori.html', context)

def create_murotal(request, qori_id): 

    form = MurotalForm(request.POST or None, request.FILES or None)
    qori = get_object_or_404(Qori, pk=qori_id)
    if form.is_valid():
        qoris_murotals = qori.murotal_set.all()
        for s in qoris_murotals:
            if s.surah == form.cleaned_data.get("surah"):
                context = {
                    'qori': qori,
                    'form': form,
                    'error_message': 'Anda Telah Menambah Murotal',
                }
                return render(request, 'quran/create_murotal.html', context)
        murotal = form.save(commit=False)
        murotal.qori = qori
        murotal.audio_file = request.FILES['audio_file']
        file_type = murotal.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'qori': qori,
                'form': form,
                'error_message': 'File audio harus format WAV, MP3, or OGG',
            }
            return render(request, 'quran/create_murotal.html', context)

        murotal.save()
        return render(request, 'quran/detail.html', {'qori': qori})
    context = {
        'qori': qori,
        'form': form,
    }
    return render(request, 'quran/create_murotal.html', context)


def delete_qori(request, qori_id):

    qori = Qori.objects.get(pk=qori_id)
    qori.delete()
    qoris = Qori.objects.filter(user=request.user)
    return render(request, 'quran/index.html', {'qoris': qoris})
    

def delete_murotal(request, qori_id, murotal_id):

    qori = get_object_or_404(Qori, pk=qori_id)
    murotal = Murotal.objects.get(pk=murotal_id)
    murotal.delete()
    return render(request, 'quran/detail.html', {'qori': qori})

def ayat(request):

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            ayat_title = request.POST.items()[1][1]
            ayat_address = 'upnplay/ayatdir/' + ayat_title + '.mp3'
            with open(ayat_address, 'wb+' ) as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
                audio = MP3(ayat_address)
                c = Ayat(title = ayat_title, songfile = ayat_address, duration = audio.info.length)
                c.save()
            return HttpResponseRedirect('')
    else:
        form = UploadForm()
    c = {'form': form}
    c.update(csrf(request))
    return render(request, 'index.html', {'form': form})
