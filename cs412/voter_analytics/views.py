from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go


# Create your views here.


class VoterListView(ListView):
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        voters = Voter.objects.all().order_by('Last_Name', 'First_Name')

        party = self.request.GET.get('party')
        if party:
            voters = voters.filter(Party_Affiliation__iexact=party.strip())

        min_dob = self.request.GET.get('min_dob')
        if min_dob and min_dob.isdigit():
            voters = voters.filter(Date_of_Birth__year__gte=int(min_dob))

        max_dob = self.request.GET.get('max_dob')
        if max_dob and max_dob.isdigit():
            voters = voters.filter(Date_of_Birth__year__lte=int(max_dob))

        voter_score = self.request.GET.get('voter_score')
        if voter_score and voter_score.isdigit():
            voters = voters.filter(voter_score=int(voter_score))

        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for election in elections:
            if self.request.GET.get(election):
                kwargs = {election: True}
                voters = voters.filter(**kwargs)

        return voters
    
class VoterDetailView(DetailView):
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'



class VoterGraphView(ListView):
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        # Same filtering logic as in VoterListView
        qs = super().get_queryset()
        request = self.request.GET

        if 'party' in request and request['party']:
            qs = qs.filter(Party_Affiliation__iexact=request['party'].strip())
        if 'min_dob' in request and request['min_dob']:
            qs = qs.filter(Date_of_Birth__year__gte=int(request['min_dob']))
        if 'max_dob' in request and request['max_dob']:
            qs = qs.filter(Date_of_Birth__year__lte=int(request['max_dob']))
        if 'voter_score' in self.request.GET:
            score = self.request.GET.get('voter_score')
            if score.isdigit():  # ensures it's a number
                voters = voters.filter(voter_score=int(score))
        for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if election in request and request[election] == 'on':
                qs = qs.filter(**{election: True})

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = context['voters']

        # Birth Year Histogram
        byear_counts = qs.values_list('Date_of_Birth', flat=True)
        birth_years = [dob.year for dob in byear_counts if dob]
        birth_fig = go.Figure([go.Histogram(x=birth_years)])
        birth_fig.update_layout(title_text="Distribution of Voters by Year of Birth")
        context['birth_year_graph'] = plotly.offline.plot(birth_fig, auto_open=False, output_type='div')

        # Party Pie Chart
        party_counts = {}
        for voter in qs:
            party = voter.Party_Affiliation.strip()
            party_counts[party] = party_counts.get(party, 0) + 1
        pie_fig = go.Figure([go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))])
        pie_fig.update_layout(title_text="Party Affiliation Breakdown")
        context['party_pie_chart'] = plotly.offline.plot(pie_fig, auto_open=False, output_type='div')

        # Election Participation
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        voted_counts = [qs.filter(**{e: True}).count() for e in elections]
        bar_fig = go.Figure([go.Bar(x=elections, y=voted_counts)])
        bar_fig.update_layout(title_text="Voter Participation in Elections")
        context['voting_histogram'] = plotly.offline.plot(bar_fig, auto_open=False, output_type='div')

        return context
