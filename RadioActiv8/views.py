from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from random import randrange
from django.core.serializers import serialize


@login_required(login_url='RadioActiv8:login')
def index(request):
    return render(request, 'master/home.html')


@login_required(login_url='RadioActiv8:login')
def map(request):
    ab = [b for b in Base.objects.all() if not b.is_full()]
    bp = [p for p in Patrol.objects.all() if p.base]
    fb = [b for b in Base.objects.all() if b.is_full()]
    context = {
        "available_bases": ab,
        "busy_patrols": bp,
        "full_bases": fb
    }
    return render(request, 'master/map.html', context)


@login_required(login_url='RadioActiv8:login')
def play(request):
    if (request.method == "POST"):
        patrol = Patrol.objects.get(id=request.POST.get("patrol"))
        base = Base.objects.get(id=request.POST.get("base"))
        if (request.POST.get("action") == "check-in"):
            patrol.check_in(base)
        elif (request.POST.get("action") == "check-out"):
            patrol.check_out()
        elif (request.POST.get("action") == "intel"):
            #TODO: Fix passing intel
            patrol.log_intelligence(base, None)
        elif (request.POST.get("action") == "log-event"):
            #TODO: Fix passing the comment
            patrol.log_event(base, None)

    submit_action = reverse("RadioActiv8:play")
    patrols = Patrol.objects.all()
    bases = Base.objects.all()
    ab = [b for b in Base.objects.all() if not b.is_full()]
    bp = [p for p in Patrol.objects.all() if p.base]
    fb = [b for b in Base.objects.all() if b.is_full()]
    context = {
        "submit_action": submit_action,
        "patrols": patrols,
        "bases": bases,
        "available_bases": ab,
        "busy_patrols": bp,
        "full_bases": fb
    }
    return render(request, 'master/play.html', context)


class PatrolList(generic.ListView):
    template_name = 'patrol/index.html'

    def get_queryset(self):
        """Return a list of Patrols."""
        return Patrol.objects.all()


class PatrolDetail(generic.DetailView):
    model = Patrol
    template_name = 'patrol/detail.html'


class BaseList(generic.ListView):
    template_name = 'base/index.html'

    def get_queryset(self):
        """Return a list of Bases."""
        return Base.objects.all()


class BaseDetail(generic.DetailView):
    model = Base
    template_name = 'base/detail.html'


def base_test(request, base_id):
    base = get_object_or_404(Base, pk=base_id)
    if (request.method == 'POST'):
        our_form_data = BaseForm(request.POST, instance=base)
        if our_form_data.is_valid():
            our_form_data.save()
    submit_location = reverse('RadioActiv8:base_test', args=(base.id,))
    form = BaseForm(instance=base)
    patrol_form = PatrolForm()
    return render(request, 'base/detail.html', {'base': base, 'form_test': form, 'patrol_form': patrol_form, 'submit_location': submit_location})


@login_required(login_url='RadioActiv8:login')
def valid_intelligence_options(request):
    patrol_id = request.GET['patrol']
    current_location_id = request.GET['current_location']

    response = {'unused': {}, 'used': {}}
    if not current_location_id or not patrol_id:
        return JsonResponse(response, safe=False)

    current_location = Base.objects.get(id = current_location_id)
    patrol = Patrol.objects.get(id = patrol_id)

    unused_options = current_location.get_intelligence(patrol)
    used_options = current_location.get_intelligence().exclude(id__in=unused_options)

    response['unused'] = [{'id': o.id, 'q': o.question, 'a': o.answer}
                          for o in unused_options]
    response['used'] = [{'id': o.id, 'q': o.question, 'a': o.answer}
                        for o in used_options]

    return JsonResponse(response, safe=False)


@login_required(login_url='RadioActiv8:login')
def valid_next_base_options(request):
    patrol_id = request.GET['patrol']
    current_location_id = request.GET['current_location']

    if not current_location_id or not patrol_id:
        return HttpResponse('<option value="" selected="">---------</option>')

    current_location = Location.objects.get(id=current_location_id)
    patrol = Patrol.objects.get(id=patrol_id)

    # FIXME: Surely there's a better way to do these queries, ideally without the list comprehensions?
    visited_bases = [event.location for event in Event.objects.filter(patrol=patrol_id)]
    visited_bases.append(current_location)
    unvisited_bases = Base.objects.exclude(id__in=[b.id for b in visited_bases]).order_by('location_name')
    # We do this to deduplicate the previous version of the list
    visited_bases = Base.objects.filter(id__in=[b.id for b in visited_bases]).order_by('location_name')

    # FIXME: Use a proper template for this; possibly inherit from
    # 'django/forms/widgets/select.html' or
    # 'django/forms/widgets/select_option.html'
    # Or at least use render() instead of HttpResponse()
    #
    # See https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    html = '<option value="">---------</option>\n'

    # FIXME: Deal with possibility where all bases are visited
    html += '<option value="">--- Unvisitied Bases</option>\n'
    unvisited_bases_count = len(unvisited_bases)
    random_base = None
    if unvisited_bases_count > 0:
        random_base = randrange(unvisited_bases_count)

    for base in range(unvisited_bases_count):
        if base == random_base:
            selected=' selected=""'
        else:
            selected=''
        html += f'<option value="{unvisited_bases[base].id}"{selected}>{unvisited_bases[base]}</option>\n'
    html += '<option value="">--- Visitied Bases</option>\n'
    for base in visited_bases:
        html += f'<option value="{base.id}">{base}</option>\n'

    return HttpResponse(html)

@login_required(login_url='RadioActiv8:login')
def patrol_base_history(request):
    patrol_id = request.GET['patrol']

    if not patrol_id:
        return JsonResponse({'visited_bases': [], 'last_destination': {}})

    visited_bases = [ {'id': event.location.id, 'name': str(event.location)} for event in Event.objects.filter(patrol=patrol_id).order_by('timestamp')]
    events = Event.objects.filter(patrol=patrol_id).order_by('-timestamp')
    last_destination = None
    if events:
        last_destination = events[0].destination
    if last_destination:
        last_destination_response = {'id': last_destination.id, 'name': last_destination.radio.location_name}
    else:
        last_destination_response = {'id': -1, 'name': 'NONE'}


    response = {'visited_bases': visited_bases, 'last_destination': last_destination_response}

    return JsonResponse(response, safe=False)


def base_distance(base_a, base_b):
    '''
    Calculate distance in metres, between two bases
    '''
    a_metres = base_a.gps_location.transform(7855, clone=True)
    b_metres = base_b.gps_location.transform(7855, clone=True)
    return a_metres.distance(b_metres)

def total_distance(patrol):
    '''
    Calculate total distance a patrol has travelled.
    FIXME: Try to optimise so this doesn't take ~1sec to run
    FIXME: Also calculate time between bases and total time taken
    '''
    patrol_events = Event.objects.filter(patrol__id = patrol.id)

    bases = [ e.location for e in patrol_events ]

    number_of_bases_visited = len(bases)
    total_distance = 0

    for i in range(number_of_bases_visited):
        if(i == 0):
            continue
        start = bases[i-1]
        end = bases[i]
        distance = base_distance(start, end)
        print(f'{str(start):10s} to {str(end):10s}: {distance:-8.2f} metres')
        total_distance += distance
    print(f'{patrol} Patrol total distance: {total_distance:.2f} metres')
    return total_distance

#@login_required(login_url='RadioActiv8:login')
def bases_geojson(request):
    all_objects = [*Base.objects.all(), *Radio.objects.all(), *Location.objects.all()]
    response = serialize('geojson', all_objects,
            #geometry_field='gps_location',
            #fields=('location_name',)
            )

    return HttpResponse(response, content_type="application/json")

