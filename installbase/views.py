from django.shortcuts import render
from django.views.generic import ListView
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse
import csv
from installbase.forms import InstallBaseform
from .models import installbase

class InstallBase_list(ListView):
    model = installbase
    template_name = 'installbase/list.html'
    context_object_name = 'installbase_list'

    def get_queryset(self):
        global search_installbase_list
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        installbase_list = installbase.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_installbase_list = installbase_list.filter(
                        Q(customer__icontains=search_keyword) | Q(project_name__icontains=search_keyword) | Q(
                            model__icontains=search_keyword) | Q(osversion__icontains=search_keyword) | Q(
                            serialnumber__icontains=search_keyword) | Q(hostname__icontains=search_keyword) | Q(
                            ipslist__icontains=search_keyword) | Q(diskmodel__icontains=search_keyword) | Q(
                            addlist__icontains=search_keyword) | Q(licensed__icontains=search_keyword))
                elif search_type == 'customer':
                    search_installbase_list = installbase_list.filter(customer__icontains=search_keyword)
                elif search_type == 'project_name':
                    search_installbase_list = installbase_list.filter(project_name__icontains=search_keyword)
                elif search_type == 'model':
                    search_installbase_list = installbase_list.filter(model__icontains=search_keyword)
                elif search_type == 'osversion':
                    search_installbase_list = installbase_list.filter(osversion__icontains=search_keyword)
                elif search_type == 'serialnumber':
                    search_installbase_list = installbase_list.filter(serialnumber__icontains=search_keyword)
                elif search_type == 'hostname':
                    search_installbase_list = installbase_list.filter(hostname__icontains=search_keyword)
                elif search_type == 'ipslist':
                    search_installbase_list = installbase_list.filter(ipslist__icontains=search_keyword)
                elif search_type == 'diskmodel':
                    search_installbase_list = installbase_list.filter(diskmodel__icontains=search_keyword)
                elif search_type == 'addlist':
                    search_installbase_list = installbase_list.filter(addlist__icontains=search_keyword)
                elif search_type == 'licensed':
                    search_installbase_list = installbase_list.filter(licensed__icontains=search_keyword)
                return search_installbase_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')

        return installbase_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
            context['type'] = search_type

        return context

class InstallBaseUpdateView(UpdateView):
    model = installbase
    form_class = InstallBaseform
    template_name = 'installbase/update.html'

def InstallBase_create(request):
    if request.method == 'POST':
        form = InstallBaseform(request.POST)
        if form.is_valid():
            installbase = form.save(commit=False)
            installbase.save()
            return redirect('/')
    else:
        form = InstallBaseform()
    context = {'form': form}
    return render(request, 'installbase/upload.html', context)

class InstallBase_delete(UpdateView):
    model = installbase
    fields = ['deleted']
    template_name = 'installbase/delete.html'

    def form_valid(self, form):
        form.instance.deleted = True
        if form.is_valid():
            # 데이터가 올바르다면
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})

class InstallBase_undelete(UpdateView):
    model = installbase
    fields = ['deleted']
    template_name = 'installbase/undelete.html'

    def form_valid(self, form):
        form.instance.deleted = False
        if form.is_valid():
            # 데이터가 올바르다면
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})

class InstallBaseClearView(DeleteView):
    model = installbase
    success_url = '/'
    template_name = 'installbase/clear.html'

def InstallBase_export(request):
    response = HttpResponse(content_type='text/csv')

    response.write(u'\ufeff' .encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['customer', 'installedat', 'project_name', 'model', 'osversion', 'serialnumber', 'hostname', 'ipslist', 'shelfmodel' ,'disk', 'diskmodel', 'shelfemptyslot', 'slotinfo', 'engineername', 'addlist', 'installedate', 'warrantydate', 'controllereoa', 'controllereos'])

    for installbases in installbase.objects.all().values_list('customer', 'installedat', 'project_name', 'model', 'osversion', 'serialnumber', 'hostname', 'ipslist', 'shelfmodel', 'disk', 'diskmodel', 'shelfemptyslot', 'slotinfo', 'engineername', 'addlist', 'installedate', 'warrantydate', 'controllereoa', 'controllereos'):
        writer.writerow(installbases)

        response['Content-Disposition'] = 'attachment; filename="installbase.csv"'
    return response
