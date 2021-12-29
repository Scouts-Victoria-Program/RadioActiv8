from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from .forms import *
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# FIXME: Ensure most views require login

@login_required
def index(request):
    context = {}

    ra8_session = request.session.get('ra8_session')

    context['session_set_form'] = SessionListForm(initial={'session_list_field': ra8_session})

    return render(request, 'RadioActiv8/master/home.html', context)


@login_required
def map(request):
    ab = [b for b in Base.objects.all() if not b.is_full()]
    bp = [p for p in Patrol.objects.all() if p.base]
    fb = [b for b in Base.objects.all() if b.is_full()]
    context = {
        "available_bases": ab,
        "busy_patrols": bp,
        "full_bases": fb
    }
    return render(request, 'RadioActiv8/master/map.html', context)


@login_required
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
    bp = [p for p in Patrol.objects.all() if p.current_base]
    fb = [b for b in Base.objects.all() if b.is_full()]
    context = {
        "submit_action": submit_action,
        "patrols": patrols,
        "bases": bases,
        "available_bases": ab,
        "busy_patrols": bp,
        "full_bases": fb
    }
    return render(request, 'RadioActiv8/master/play.html', context)


class PatrolList(LoginRequiredMixin, generic.ListView):
    template_name = 'RadioActiv8/patrol/index.html'

    def get_queryset(self):
        """Return a list of Patrols."""
        return Patrol.objects.all()


class PatrolDetail(LoginRequiredMixin, generic.DetailView):
    model = Patrol
    template_name = 'RadioActiv8/patrol/detail.html'


class BaseList(LoginRequiredMixin, generic.ListView):
    template_name = 'RadioActiv8/base/index.html'

    def get_queryset(self):
        """Return a list of Bases."""
        return Base.objects.all()


class BaseDetail(LoginRequiredMixin, generic.DetailView):
    model = Base
    template_name = 'RadioActiv8/base/detail.html'

@login_required
def SetWorkingSession(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        session_form = SessionListForm(request.POST)
        # check whether it's valid:
        if session_form.is_valid():
            # process the data in form.cleaned_data as required
            request.session['ra8_session'] = session_form.cleaned_data['session_list_field'].id
            # redirect to a new URL:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def EventList(request):
    template_name = 'RadioActiv8/event/index.html'
    context = {}

    ra8_session = request.session.get('ra8_session')

    context['session_set_form'] = SessionListForm(initial={'session_list_field': ra8_session})

    event_list= Event.objects.all()
    if ra8_session:
        event_list = event_list.filter(session__id=ra8_session)
    context['event_list'] = event_list

    return render(request, template_name, context)


class EventCreate(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = Event
    template_name = 'RadioActiv8/event/create.html'
    form_class = EventForm
    success_url = reverse_lazy('RadioActiv8:EventCreate')

    def get(self, request, *args, **kwargs):
        self.initial['session'] = self.request.session['ra8_session']
        return super().get(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return f"{self.object} was created successfully."


class SessionList(LoginRequiredMixin, generic.ListView):
    template_name = 'RadioActiv8/session/index.html'

    def get_queryset(self):
        """Return a list of Sessions."""
        return Session.objects.all()


class SessionDetail(LoginRequiredMixin, generic.DetailView):
    model = Session
    template_name = 'RadioActiv8/session/detail.html'


@login_required
def GPSTrackerList(request):
    template_name = 'RadioActiv8/gpstracker/index.html'
    context = {}


    if request.method == 'POST':
        pass
    else:
        gpstracker_list = GPSTracker.objects.all()
        context['gpstracker_list'] = gpstracker_list

        return render(request, template_name, context)


@login_required
def GPSTrackerDetail(request, pk):
    template_name = 'RadioActiv8/gpstracker/detail.html'
    context = {}
    gpstracker = GPSTracker.objects.get(id=pk)
    form_initial = {'gpstracker': pk}
    current_patrol = None
    if hasattr(gpstracker, 'patrol'):
        current_patrol = gpstracker.patrol

    if request.method == 'POST':
        form = GPSTrackerPatrolForm(request.POST)
        print(request.POST)
        if form.is_valid():
            if current_patrol:
                current_patrol.gps_tracker = None
                current_patrol.save()
            if request.POST['patrol']:
                patrol = Patrol.objects.get(id=request.POST['patrol'])
                patrol.gps_tracker = GPSTracker.objects.get(id=request.POST['gpstracker'])
                patrol.save()
                messages.success(request, f'Assigned tracker {gpstracker} to patrol {patrol}')
            else:
                messages.success(request, f'Unassigned tracker {gpstracker} from patrol {current_patrol}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context['gpstracker'] = gpstracker
            context['form'] = form

            return render(request, template_name, context)
    else:
        form = GPSTrackerPatrolForm(initial = form_initial)

        context['gpstracker'] = gpstracker
        context['form'] = form

        return render(request, template_name, context)

@login_required
def base_test(request, base_id):
    base = get_object_or_404(Base, pk=base_id)
    if (request.method == 'POST'):
        our_form_data = BaseForm(request.POST, instance=base)
        if our_form_data.is_valid():
            our_form_data.save()
    submit_location = reverse('RadioActiv8:base_test', args=(base.id,))
    form = BaseForm(instance=base)
    patrol_form = PatrolForm()
    return render(request, 'RadioActiv8/base/detail.html', {'base': base, 'form_test': form, 'patrol_form': patrol_form, 'submit_location': submit_location})


@login_required
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
    response['base_history'] = patrol_base_history(session, patrol)

    return JsonResponse(response, safe=False)

@login_required
def add_patrol_to_session(request, pk):
    template_name = 'RadioActiv8/session/add_patrol.html'
    context = {}

    this_session = Session.objects.get(id=pk)
    context['session'] = this_session

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print(request.POST)
        # create a form instance and populate it with data from the request:
        session_form = SessionAddPatrolForm(request.POST, session=this_session)
        # check whether it's valid:
        if session_form.is_valid():
            # process the data in form.cleaned_data as required
            session = Session.objects.get(id=request.POST['ra8_session'])
            patrol = Patrol.objects.get(id=request.POST['patrol'])
            gps_tracker = GPSTracker.objects.get(id=request.POST['gps_tracker'])

            patrol.session.add(session)
            patrol.gps_tracker = gps_tracker
            patrol.save()
            messages.success(request, f'Added patrol {patrol} to session {session} and allocated tracker {gps_tracker}')
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('RadioActiv8:SessionAddPatrol', args=[pk]))
    # if a GET (or any other method) we'll create a blank form
    else:
        session_add_patrol_form = SessionAddPatrolForm(session=this_session, initial={'ra8_session': pk})
        context['session_add_patrol_form'] = session_add_patrol_form

        return render(request, template_name, context)

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
    response = {'unvisited': {}, 'visited': {}, 'home_base': None}

    visited_bases_list = list(patrol.visited_bases())
    session_bases = Base.objects.filter(session=session)
    if session.home_base:
        session_bases = session_bases.exclude(id=session.home_base.id)
        response['home_base'] = {'id': session.home_base.id, 'b': session.home_base.name}
    if current_location: visited_bases_list.append(current_location)

    unvisited_bases = session_bases.exclude(id__in = [ b.id for b in visited_bases_list ])
    visited_bases = session_bases.filter(id__in = [ b.id for b in visited_bases_list ])

    response['unvisited'] = [{'id': b.id, 'b': b.name}
                          for b in unvisited_bases]
    response['visited'] = [{'id': b.id, 'b': b.name}
                        for b in visited_bases]

    return response


def patrol_base_history(session, patrol):
    visited_bases = [ {'id': event.location.id, 'name': str(event.location)} for event in Event.objects.filter(session=session).filter(patrol=patrol).order_by('timestamp')]
    events = Event.objects.filter(session=session).filter(patrol=patrol).order_by('-timestamp')
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

#@login_required
def bases_geojson(request):
    all_objects = [*Base.objects.all(), *Radio.objects.all(), *Location.objects.all()]
    response = serialize('geojson', all_objects,
            #geometry_field='gps_location',
            #fields=('name',)
            )

    return HttpResponse(response, content_type="application/json")

