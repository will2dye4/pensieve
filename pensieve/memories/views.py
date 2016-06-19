from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Memory


class IndexView(generic.ListView):
    template_name = 'memories/index.html'
    context_object_name = 'recent_memories'

    def get_queryset(self):
        return Memory.objects.order_by('-created')[:10]


class MemoryDetailView(generic.DetailView):
    model = Memory
    template_name = 'memories/detail.html'

    def post(self, request, **kwargs):
        memory = self.get_object()
        memory.title = request.POST['title']
        memory.save()
        return HttpResponseRedirect(reverse('memories:detail', args=(kwargs['pk'],)))


def detail(request, memory_id):
    memory = get_object_or_404(Memory, pk=memory_id)
    if request.method == 'POST':
        memory.title = request.POST['title']
        memory.save()
        return HttpResponseRedirect(reverse('memories:detail', args=(memory_id,)))
    else:
        return render(request, 'memories/detail.html', {'memory': memory})
