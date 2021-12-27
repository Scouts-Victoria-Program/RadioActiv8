from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from .forms import *
from django.core.serializers import serialize

# FIXME: Ensure most views require login

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


def EventList(request):
    template_name = 'event/index.html'
    context = {}

    ra8_session = None
    if request.session.get('ra8_session'):
        ra8_session = request.session['ra8_session']

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        session_form = SessionListForm(request.POST, initial={'session_list_field': request.session['ra8_session']})
        # check whether it's valid:
        if session_form.is_valid():
            # process the data in form.cleaned_data as required
            request.session['ra8_session'] = session_form.cleaned_data['session_list_field'].id
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('RadioActiv8:EventList'))
    # if a GET (or any other method) we'll create a blank form
    else:
        session_form = SessionListForm(initial={'session_list_field': ra8_session})
        context['session_form'] = session_form

        event_list= Event.objects.all()
        if ra8_session:
            event_list = event_list.filter(session__id=ra8_session)
        context['event_list'] = event_list

        return render(request, template_name, context)


class EventCreate(generic.edit.CreateView):
    model = Event
    template_name = 'event/create.html'
    form_class = EventForm
    success_url = reverse_lazy('RadioActiv8:EventCreate')


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
def event_ajax(request):
    session_id = request.GET['ra8_session']
    patrol_id = request.GET['patrol']
    current_location_id = request.GET['current_location']

    response = {
        'patrol_options': [],
        'location_options': [],
        'intelligence_options': {
            'unused': {},
            'used': {}
        },
        'valid_destinations': {
            'unvisited': {},
            'visited': {}
        },
        'base_history': {
            'visited_bases': [],
            'last_destination': None
        }
    }

    if session_id:
        session = Session.objects.get(id = session_id)
    else:
        return JsonResponse(response, safe=False)

    response['patrol_options'] = [ {'id': p.id, 'name': p.name} for p in Patrol.objects.filter(session=session) ]
    response['location_options'] = [ {'id': b.id, 'name': b.name } for b in Base.objects.filter(session=session) ]

    if patrol_id:
        patrol = Patrol.objects.get(id = patrol_id)
    else:
        return JsonResponse(response, safe=False)

    if current_location_id:
        current_location = Base.objects.get(id = current_location_id)
    else:
        current_location = None
        events = Event.objects.filter(patrol=patrol).order_by('-timestamp')
        if events:
            current_location = events[0].destination
            if not current_location:
                current_location = events[0].location

    response['intelligence_options'] = valid_intelligence_options(patrol, current_location)
    response['valid_destinations'] = valid_next_base_options(session, patrol, current_location)
    response['base_history'] = patrol_base_history(patrol)

    return JsonResponse(response, safe=False)


'''
Only helper functions below this point
'''

def valid_intelligence_options(patrol, current_location):
    response = {'unused': {}, 'used': {}, 'random': False}

    if not current_location:
        return response

    unused_options = current_location.radio.base.get_intelligence(patrol)
    used_options = current_location.radio.base.get_intelligence().exclude(id__in=unused_options)

    response['unused'] = [{'id': o.id, 'q': o.question, 'a': o.answer}
                          for o in unused_options]
    response['used'] = [{'id': o.id, 'q': o.question, 'a': o.answer}
                        for o in used_options]
    if current_location.radio.base.activity_type == 'R':
        response['random'] = True

    return response


def valid_next_base_options(session, patrol, current_location):
    response = {'unvisited': {}, 'visited': {}}

    visited_bases_list = list(patrol.visited_bases())
    session_bases = Base.objects.filter(session=session)
    if current_location: visited_bases_list.append(current_location)

    unvisited_bases = session_bases.exclude(id__in = [ b.id for b in visited_bases_list ]).order_by('name')
    visited_bases = session_bases.filter(id__in = [ b.id for b in visited_bases_list ]).order_by('name')

    response['unvisited'] = [{'id': b.id, 'b': b.name}
                          for b in unvisited_bases]
    response['visited'] = [{'id': b.id, 'b': b.name}
                        for b in visited_bases]

    return response


def patrol_base_history(patrol):
    visited_bases = [ {'id': event.location.id, 'name': str(event.location)} for event in Event.objects.filter(patrol=patrol).order_by('timestamp')]
    events = Event.objects.filter(patrol=patrol).order_by('-timestamp')
    last_destination = None
    if events:
        last_destination = events[0].destination
        if not last_destination:
            last_destination = events[0].location
    if last_destination:
        last_destination_response = {'id': last_destination.id, 'name': last_destination.radio.name}
    else:
        last_destination_response = {'id': -1, 'name': 'NONE'}

    response = {'visited_bases': visited_bases, 'last_destination': last_destination_response}

    return response


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
            #fields=('name',)
            )

    return HttpResponse(response, content_type="application/json")

