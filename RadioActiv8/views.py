from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from .forms import *
from random import randrange


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


def valid_intelligence_options(request):
    #patrol = Patrol.objects.get(name = request.GET.get('patrol'))
    patrol = request.GET['patrol']
    current_location = request.GET['current_location']

    intelligence_options = Intelligence.objects.all()
    if current_location:
        intelligence_options = intelligence_options.filter(base=current_location)

    # FIXME: Should we bother limiting based on location here?
    if patrol:
        patrol_answers = [e.intelligence_request for e in
                        Event.objects.filter(patrol=patrol,
                        intelligence_answered_correctly=True).order_by('timestamp')]

        # FIXME: Can this be done as a DB query instead?
        unused_options = list(set(intelligence_options.order_by('question')) - set(patrol_answers))
    else:
        unused_options = []

    # FIXME: Use a proper template for this; possibly inherit from
    # 'django/forms/widgets/select.html' or
    # 'django/forms/widgets/select_option.html'
    # Or at least use render() instead of HttpResponse()
    #
    # See https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    html = '<option value="">---------</option>\n'
    unused_option_count = len(unused_options)
    random_option = randrange(unused_option_count)
    for option in range(unused_option_count):
        if option == random_option:
            selected=' selected=""'
        else:
            selected=''
        html += f'<option value="{unused_options[option].id}"{selected}>{unused_options[option]}</option>\n'
    return HttpResponse(html)

    # field-intelligence_request