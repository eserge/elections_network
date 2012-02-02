# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from locations.models import Location
from links.models import Link
from users.models import Participation

from django.core import serializers
json_serializer = serializers.get_serializer("json")()

# TODO: restructure it and take only one parameter
def goto_location(request):
    try:
        location_id = int(request.GET.get('tik_pk', ''))
    except ValueError:
        return HttpResponseRedirect(reverse('main'))
    return HttpResponseRedirect(reverse('location', args=[location_id]))

# TODO: mark links previously reported by user
def location(request, loc_id):
    try:
        id = int(loc_id)
    except ValueError:
        raise Http404

    try:
        location = Location.objects.select_related().get(id=id)
    except Location.DoesNotExist:
        raise Http404

    # Get the list of participants
    participants = {} # {participation_type: [users]}
    query = Q(location=location)

    if not location.parent_2:
        query |= Q(location__parent_2=location) if location.parent_1 else Q(location__parent_1=location)

    for participation in Participation.objects.filter(query).select_related():
        participants.setdefault(participation.type, []).append(participation.user)

    # Get sub-regions
    if location.parent_2:
        sub_regions = []
    elif location.parent_1:
        sub_regions = list(Location.objects.filter(parent_2=location))
    else:
        sub_regions = list(Location.objects.filter(parent_1=location, parent_2=None))

    context = {
        'current_location': location,
        'participants': participants,
        'links': list(Link.objects.filter(location=location)),
        'locations': list(Location.objects.filter(parent_1=None).order_by('name')),
        'is_voter_here': request.user.is_authenticated() and any(request.user==voter for voter in participants.get('voter', [])),
        'sub_regions': sub_regions,
    }
    return render_to_response('location.html', context_instance=RequestContext(request, context))

def get_sub_regions(request):
    if request.is_ajax():
        try:
            location_id = int(request.GET.get('location', ''))
        except ValueError:
            return HttpResponse('[]')

        try:
            location = Location.objects.select_related().get(id=location_id)
        except Location.DoesNotExist:
            return HttpResponse('[]')

        if location.parent_2: # 3rd level location
            return HttpResponse('[]') # 3rd level locations have no children
        elif location.parent_1: # 2nd level location
            res = []
            for loc in Location.objects.filter(parent_2=location).order_by('name'):
                res.append({'name': loc.name, 'id': loc.id})
            return HttpResponse(json.dumps(res))
        else: # 1st level location
            res = []
            for loc in Location.objects.filter(parent_1=location, parent_2=None).order_by('name'):
                res.append({'name': loc.name, 'id': loc.id})
            return HttpResponse(json.dumps(res))

    return HttpResponse('[]')

def search_locations_by_name(request):
    if request.is_ajax():
        search_string = request.REQUEST.get("search_string")
        locations = Location.objects.filter(name__icontains=search_string)
        # first select third level 
        # 
        # next select second level
        # if there are some select their children (see F)
        # selecting children exclude these from first query
        #
        # then first level locations  and make the same as with second
        # exclude from result all occurences of already selected first and second level locations 
        # 
        for location in locations:
            location.name = (location.parent_1 and (location.parent_1.name + ", ") or "") + \
                        (location.parent_2 and (location.parent_2.name + ", ") or "") + \
                        unicode(location.name)
        locations_list = json_serializer.serialize(locations, ensure_ascii=False)
        return HttpResponse(json.dumps(locations_list.encode("utf8")))
    return HttpResponse('[]')
