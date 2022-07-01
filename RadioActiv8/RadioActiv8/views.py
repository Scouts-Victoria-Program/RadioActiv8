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

def healthcheck(request):
    context = {}
    template_name = 'RadioActiv8/'

    # Do a database request to test DB is working
    x = Session.objects.count()

    #return render(request, template_name, context)
    return HttpResponse('healthy')


@login_required
def index(request):
    context = {}

    ra8_session = request.session.get('ra8_session')

    context['session_set_form'] = SessionListForm(initial={'session_list_field': ra8_session})

    return render(request, 'RadioActiv8/master/home.html', context)


@login_required
def map(request):
    template_name = 'RadioActiv8/master/map.html'
    ra8_session = request.session.get('ra8_session')
    available_bases = [b for b in Base.objects.filter(session=ra8_session) if not b.is_full()]
    busy_patrols = [p for p in Patrol.objects.filter(session=ra8_session) if p.current_base]
    full_bases = [b for b in Base.objects.filter(session=ra8_session) if b.is_full()]

    context = {
        "available_bases": available_bases,
        "busy_patrols": busy_patrols,
        "full_bases": full_bases,
        "bases_geojson" : serialize('geojson', Location.objects.filter(session=ra8_session)),
        "base_locations": Base.objects.filter(session=ra8_session)
    }
    return render(request, template_name, context)


@login_required
def play(request):
    #template_name = 'RadioActiv8/event/create.html'
    template_name = 'RadioActiv8/master/play.html'
    form_class = EventForm
    success_url = reverse_lazy('RadioActiv8:EventCreate')
    initial = {}
    context = {}

    ra8_session = request.session.get('ra8_session')
    initial['session'] = ra8_session

    if (request.method == "POST"):
        event_form = EventForm(request.POST)

        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        if event_form.is_valid():

            session = event_form.cleaned_data["session"]
            patrol = event_form.cleaned_data["patrol"]
            location = event_form.cleaned_data["location"]
            intelligence_request = event_form.cleaned_data["intelligence_request"]
            intelligence_answered_correctly = event_form.cleaned_data["intelligence_answered_correctly"]
            destination = event_form.cleaned_data["destination"]
            comment = event_form.cleaned_data["comment"]

            # process the data in form.cleaned_data as required
            event = Event(session=session,
                         patrol=patrol,
                         location=location,
                         intelligence_request=intelligence_request,
                         intelligence_answered_correctly=intelligence_answered_correctly,
                         destination=destination,
                         comment=comment
                         )
            if session.id != ra8_session:
                request.session['ra8_session'] = session.id
            event.save()
            messages.success(request, f"{event} was created successfully.")

            # redirect to a new URL:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context['form'] = event_form
            return render(request, template_name, context)

    form = EventForm(initial=initial)

    submit_action = reverse("RadioActiv8:play")
    patrols = Patrol.objects.filter(session=ra8_session)
    bases = Base.objects.filter(session=ra8_session)
    available_bases = [b for b in Base.objects.filter(session=ra8_session) if not b.is_full()]
    busy_patrols = [p for p in Patrol.objects.filter(session=ra8_session) if p.current_base]
    full_bases = [b for b in Base.objects.filter(session=ra8_session) if b.is_full()]
    context = {
        "submit_action": submit_action,
        "patrols": patrols,
        "bases": bases,
        "available_bases": available_bases,
        "busy_patrols": busy_patrols,
        "full_bases": full_bases,
        "form": form,
    }
    return render(request, template_name, context)


class PatrolList(LoginRequiredMixin, generic.ListView):
    template_name = 'RadioActiv8/patrol/index.html'

    def get_queryset(self):
        """Return a list of Patrols."""
        return Patrol.objects.all()


@login_required
def PatrolDetail(request, pk):
    template_name = 'RadioActiv8/patrol/detail.html'
    #form_class = EventForm
    #success_url = reverse_lazy('RadioActiv8:EventCreate')
    success_url = request.META.get('HTTP_REFERER')
    context = {}

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        pass
        # create a form instance and populate it with data from the request:
        form = BonusPointsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            patrol = form.cleaned_data['patrol']
            bonus_points = form.cleaned_data['bonus_points']
            if 'subtract' in request.POST:
                patrol.bonus_points -= bonus_points
            else:
                patrol.bonus_points += bonus_points

            patrol.save()

            # redirect to a new URL:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    patrol = Patrol.objects.get(id=pk)
    context['patrol'] = patrol
    form = BonusPointsForm(initial={'patrol': patrol })
    context['form'] = form

    return render(request, template_name, context)


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

    event_list= Event.objects.all().order_by('-timestamp')
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


@login_required
def CurrentSessionDetail(request, path=None):
    ra8_session = request.session.get('ra8_session')
    redirect = reverse('RadioActiv8:SessionDetail', args=(ra8_session,))
    if path:
        redirect += path
    return HttpResponseRedirect(redirect)


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
        if form.is_valid():
            if current_patrol:
                current_patrol.gps_tracker = None
                current_patrol.current_base = None
                current_patrol.save()
            if request.POST['patrol']:
                patrol = Patrol.objects.get(id=request.POST['patrol'])
                patrol.gps_tracker = GPSTracker.objects.get(id=request.POST['gpstracker'])
                patrol.save()
                messages.success(request, f'Assigned tracker {gpstracker} to patrol {patrol}')
            else:
                messages.success(request, f'Unassigned tracker {gpstracker} from patrol {current_patrol}')
            return HttpResponseRedirect(reverse('RadioActiv8:GPSTrackerList'))
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
    response['location_options'] = []
    for b in Base.objects.all():
        this_base = {'id': b.id, 'name': b.name }
        # FIXME: Is this the best way to see if a Base exists in the Session?
        if session.location_set.filter(id=b.id).exists():
            this_base['current_session'] = True
        else:
            this_base['current_session'] = False
        response['location_options'].append(this_base)

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
        # create a form instance and populate it with data from the request:
        session_form = SessionAddPatrolForm(request.POST, session=this_session)
        # check whether it's valid:
        if session_form.is_valid():
            # process the data in form.cleaned_data as required
            session = Session.objects.get(id=request.POST['ra8_session'])
            patrol = Patrol.objects.get(id=request.POST['patrol'])
            gps_tracker = GPSTracker.objects.get(id=request.POST['gps_tracker'])
            base = Base.objects.get(id=request.POST['base'])

            patrol.session.add(session)
            patrol.gps_tracker = gps_tracker
            patrol.save()

            event = Event(session=session, patrol=patrol, location=session.home_base, intelligence_answered_correctly=False, destination=base, comment=f"Assigned tracker {gps_tracker}")
            event.save()
            messages.success(request, f'Patrol {patrol} added to session {session} allocated tracker {gps_tracker}, sent to base {base}')
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('RadioActiv8:SessionAddPatrol', args=[pk]))
    # if a GET (or any other method) we'll create a blank form
    else:
        session_add_patrol_form = SessionAddPatrolForm(session=this_session, initial={'ra8_session': pk})
        context['session_add_patrol_form'] = session_add_patrol_form

        return render(request, template_name, context)


def participant_homepage(request):
    return HttpResponseRedirect('/static/RadioActiv8/img/participant_map.png')
    template_name = 'RadioActiv8/master/participant_homepage.html'
    context = {}

    if request.method == 'POST':
        form = PatrolForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('RadioActiv8:participant_base_list', args=(request.POST['patrol'],)))
        else:
            context['form'] = form

            return render(request, template_name, context)
    else:
        form = PatrolForm()
        context['form'] = form

        return render(request, template_name, context)


def participant_base_list(request, pk):
    template_name = 'RadioActiv8/master/participant_base_list.html'
    context = {}

    patrol = Patrol.objects.get(id=pk)

    context['patrol'] = patrol
    #context['bases'] = [ base for base in Base.objects.filter(starts_session=None).filter(session__in=patrol.session.all()).exclude(activity_type='F') ]
    context['bases'] = Base.objects.filter(is_home_base=None).filter(session__in=patrol.session.all()).exclude(activity_type='F')

    return render(request, template_name, context)


def participant_base_detail(request, patrol_pk, base_pk):
    template_name = 'RadioActiv8/master/participant_base_detail.html'
    context = {}

    patrol = Patrol.objects.get(id=patrol_pk)
    base = Base.objects.get(id=base_pk)

    intelligence = base.get_random_intelligence(patrol)
    context['intelligence'] = intelligence

    return render(request, template_name, context)

@login_required
def SessionClock(request, pk):
    template_name = 'RadioActiv8/session/clock.html'
    context = {}

    ra8_session = Session.objects.get(id=pk)

    context['ra8_session'] = ra8_session

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
    response = {'bases': [], 'home_base': None}

    visited_bases_list = list(patrol.visited_bases())
    session_bases = Base.objects.filter(session=session)
    if session.home_base:
        session_bases = session_bases.exclude(id=session.home_base.id)
        response['home_base'] = {'id': session.home_base.id, 'name': session.home_base.name}
    if current_location: visited_bases_list.append(current_location)

    visited_bases = session_bases.filter(id__in = [ b.id for b in visited_bases_list ])
    eligible_bases = session_bases.filter(mission__member_classes__in = patrol.member_classes.all()).distinct()

    for b in session_bases:
        base = {
            'id': b.id,
            'name': b.name,
            'type': b.activity_type,
            'num_patrols': b.get_patrols_count(),
            'max_patrols': b.max_patrols,
            'visited': b in visited_bases,
            'eligible': b in eligible_bases,
            'preferred': b in patrol.preferred_bases.all(),
            'repeatable': b.repeatable,
        }
        response['bases'].append(base)

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

