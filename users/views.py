# coding=utf8
from smtplib import SMTPException

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from locations.models import Location
from links.models import Link
from users.models import Contact, Participation

def current_profile(request):
    """ Show profile of the currently logged in user """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    return profile(request, request.user.username)

def fill_columns(user):
    return {
        'links': list(Link.objects.filter(user=user).select_related()),
        'contacts': list(Contact.objects.filter(user=user)) if user.is_authenticated() else [],
        'have_in_contacts': list(Contact.objects.filter(contact=user)),
        }

def profile(request, username):
    user = get_object_or_404(User, username=username)

    activities = {}
    for participation in Participation.objects.filter(user=user).select_related():
        activities[participation.type] = {'user': participation.user, 'location': participation.location}

    context = {
        'profile_user': user,
        'profile': user.get_profile(),
        'activities': activities,
        'locations': list(Location.objects.filter(parent_1=None).order_by('name')),
    }
    context.update(fill_columns(user))
    return render_to_response('users/profile.html', context_instance=RequestContext(request, context))

def become_voter(request):
    if request.method=='POST' and request.is_ajax() and request.user.is_authenticated():
        for name in ('region_3', 'region_2', 'region_1'):
            try:
                location_id = int(request.POST.get(name, ''))
            except ValueError:
                continue

            try:
                participation, created = Participation.objects.get_or_create(
                        type='voter', user=request.user, defaults={'location_id': location_id})
            except IntegrityError:
                return HttpResponse(u'Ошибка базы данных')

            if not created:
                participation.location_id = location_id
                participation.save()

            return HttpResponse('ok')

    return HttpResponse(u'Ошибка')

def add_to_contacts(request):
    if request.method=='POST' and request.is_ajax() and request.user.is_authenticated():
        try:
            contact = User.objects.get(username=request.POST.get('username', ''))
        except User.DoesNotExist:
            return HttpResponse(u'Пользователь не существует')

        try:
            Contact.objects.create(user=request.user, contact=contact)
        except IntegrityError:
            return HttpResponse(u'Пользователь уже добавлен в контакты')

        return HttpResponse('ok')

    return HttpResponse(u'Ошибка')

def remove_from_contacts(request):
    if request.method=='POST' and request.is_ajax() and request.user.is_authenticated():
        try:
            contact = User.objects.get(username=request.POST.get('username', ''))
        except User.DoesNotExist:
            return HttpResponse(u'Пользователь не существует')

        Contact.objects.filter(user=request.user, contact=contact).delete()
        return HttpResponse('ok')

    return HttpResponse(u'Ошибка')

def send_message(request):
    if request.method=='POST' and request.is_ajax() and request.user.is_authenticated():
        try:
            user = User.objects.get(username=request.POST.get('username', ''))
        except User.DoesNotExist:
            return HttpResponse(u'Пользователь не существует')

        title = request.POST.get('message_title', '')
        if title == '':
            return HttpResponse(u'Введите тему сообщения')

        message_body = request.POST.get('message_body', '')
        if message_body == '':
            return HttpResponse(u'Введите текст сообщения')

        try:
            send_mail(title, message_body, request.user.email, [user.email], fail_silently=False)
        except SMTPException:
            return HttpResponse(u'Не удалось отправить сообщение')

        return HttpResponse('ok')

    return HttpResponse(u'Ошибка')

def edit_profile(request):
    from forms import EditProfileForm
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    user = get_object_or_404(User, username=request.user.username)
    profile = user.get_profile()
    context = {
        'user': user,
        'profile': profile,
    }
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.session['profile_saved'] = 'saved'
            return redirect(reverse("edit_profile"))
    elif request.method == "GET":
        form = EditProfileForm(instance=profile)
        context.update({'profile_saved':request.session.get('profile_saved', None)})
        try:
            del request.session['profile_saved']
        except KeyError:
            pass
    
    context.update({'form':form,})
    context.update(fill_columns(user))
    return render_to_response('users/edit_profile.html', context_instance=RequestContext(request, context))
