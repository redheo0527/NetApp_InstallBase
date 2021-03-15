from django.shortcuts import render
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q
from .forms import *
from django.shortcuts import redirect
from .models import *

class part_list(ListView):
    model = ics_part
    template_name = 'ics/list.html'
    context_object_name = 'part_list'

    def get_queryset(self):
        global search_part_list
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        order = self.request.GET.get('order', '')
        part_list = ics_part.objects.order_by('-id')
        inout_list = ics_inout.objects.order_by('-ics_update')

        if order:
            if order == 'id':
                part_list = ics_part.objects.order_by('-id')
            elif order == 'part_num':
                part_list = ics_part.objects.order_by('-part_num')
            elif order == 'part_description':
                part_list = ics_part.objects.order_by('-part_description')
            elif order == 'ea':
                part_list = ics_part.objects.order_by('-ea')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_part_list = part_list.filter(
                        Q(part_num__icontains=search_keyword) | Q(part_description__icontains=search_keyword))
                elif search_type == 'part_num':
                    search_part_list = part_list.filter(part_num__icontains=search_keyword)
                elif search_type == 'part_description':
                    search_part_list = part_list.filter(part_description__icontains=search_keyword)
                ics = {
                    'part_list': search_part_list,
                    'inout_list': inout_list,
                }
                return ics
            else:
                messages.error(self.request, "검색어는 2글자 이상 입력해주세요.")

        ics = {
            'part_list': part_list,
            'inout_list': inout_list,
        }
        return ics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
            context['type'] = search_type


        return context


def part_create(request):
    if request.method == 'POST':
        form = ics_part_form(request.POST)
        if form.is_valid():
            part_list = form.save(commit=False)
            part_list.save()
            return redirect('/ics')
    else:
        form = ics_part_form()
    context = {'form': form}
    return render(request, 'ics/upload.html', context)

def inout_create(request, pk):
    part = ics_part.objects.filter(id=pk)[0]
    part_id = part.id
    part_number = part.part_num
    part_ea = part.ea
    if request.method == 'POST':
        form = ics_inout_form(request.POST)
        if form.is_valid():
            part_list = form.save(commit=False)
            inout = part_list.inout
            if inout == 0:
                part.ea = int(part_ea) + int(part_list.ea)
            else:
                part.ea = int(part_ea) - int(part_list.ea)
            part.save()
            part_list.save()
            return redirect('/ics')
    else:
        form = ics_inout_form()
    context = {
        'form': form,
        'part_id': part_id,
        'part_number': part_number,
    }
    return render(request, 'ics/inout.html', context)

def inout_delete(request, pk, inoutid):
    part = ics_part.objects.filter(id=pk)[0]
    part_ea = part.ea
    inout = ics_inout.objects.filter(id=inoutid)[0]
    if request.method == 'POST':
        part_inout = inout.inout
        if part_inout == 0:
            part.ea = int(part_ea) - int(inout.ea)
        else:
            part.ea = int(part_ea) + int(inout.ea)
        inout.delete()
        part.save()
        return redirect('/ics')
    else:
        form = ics_inout_form()
    return render(request, 'ics/inout_del.html')