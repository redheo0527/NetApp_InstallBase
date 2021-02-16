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
import urllib
from urllib.parse import urlparse
import os
from django.http import Http404
import mimetypes
from django.shortcuts import get_object_or_404
from django.conf import settings


class InstallBase_list(ListView):
    model = installbase
    template_name = 'installbase/list.html'
    context_object_name = 'installbase_list'

    def get_queryset(self):
        global search_installbase_list
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        order = self.request.GET.get('order', '')
        installbase_list = installbase.objects.order_by('-id')

        if order:
            if order == 'id':
                installbase_list = installbase.objects.order_by('-id')
            elif order == 'production':
                installbase_list = installbase.objects.order_by('-production')
            elif order == 'customer':
                installbase_list = installbase.objects.order_by('-customer')
            elif order == 'project_name':
                installbase_list = installbase.objects.order_by('-project_name')
            elif order == 'osversion':
                installbase_list = installbase.objects.order_by('-osversion')
            elif order == 'sanswitch':
                installbase_list = installbase.objects.order_by('-sanswitch')
            elif order == 'warrantydate':
                installbase_list = installbase.objects.order_by('-warrantydate')

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
                messages.error(self.request, "검색어는 2글자 이상 입력해주세요.")
        return installbase_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
            context['type'] = search_type

        return context

def InstallBase_create(request):
	if request.method == 'POST':
		form = InstallBaseform(request.POST, request.FILES)
		if form.is_valid():
			installbase = form.save(commit=False)
			if request.FILES:
				if 'upload_files' in request.FILES.keys():
					installbase.filename = request.FILES['upload_files'].name
				installbase.save()
			else:
				installbase.save()
			return redirect('/')
	else:
		form = InstallBaseform()
	context = {'form': form}
	return render(request, 'installbase/upload.html', context)

def InstallBaseUpdateView(request, pk):
    Installbase = installbase.objects.get(id=pk)
    if request.method == "POST":
        file_change_check = request.POST.get('fileChange', False)
        file_check = request.POST.get('upload_files-clear', False)

        if file_check or file_change_check:
            os.remove(os.path.join(settings.MEDIA_ROOT, Installbase.upload_files.path))

        form = InstallBaseform(request.POST, request.FILES, instance=Installbase)
        if form.is_valid():
            Installbase = form.save(commit=False)
            if request.FILES:
                if 'upload_files' in request.FILES.keys():
                    Installbase.filename = request.FILES['upload_files'].name
            Installbase.save()
            messages.success(request, "수정되었습니다.")
            return redirect('/detail/' + str(pk))
    else:
        Installbase = installbase.objects.get(id=pk)
        form = InstallBaseform(instance=Installbase)
        return render(request, "installbase/update.html", {'form': form})



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
            return self.render_to_response({'form': form})


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
            return self.render_to_response({'form': form})


class InstallBaseClearView(DeleteView):
    model = installbase
    success_url = '/'
    template_name = 'installbase/clear.html'


def InstallBase_export(request):
    response = HttpResponse(content_type='text/csv')

    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(
        ['고객사', '설치위치', '프로젝트명', '모델', 'OS버전', '시리얼', '클러스터명', 'IP정보',
         'Shelf 모델', 'Disk', 'Disk 모델', 'Shelf 빈슬롯', '컨트롤러 슬롯정보', '증설 이력', 'SAN Switch 여부', 'SAN Switch 모델', 'SAN Switch 시리얼', 'SAN Switch HostName', 'SAN Switch IP',  'SAN Switch 잔여포트', 'SAN Switch Port License',  '초기 설치일',
         '워런티 종료일', '담당 엔지니어', 'EOA', 'EOS'])

    for installbases in installbase.objects.all().values_list('customer', 'installedat', 'project_name', 'model',
                                                              'osversion', 'serialnumber', 'hostname', 'ipslist',
                                                              'shelfmodel', 'disk', 'diskmodel', 'shelfemptyslot',
                                                              'slotinfo', 'addlist', 'sanswitch', 'sanswitchmodel', 'sanswitchserial', 'sanswitchhostname', 'sanswitchipaddress',  'sanswitchport', 'sanswitchportlicense', 'installedate',
                                                              'warrantydate', 'engineername', 'controllereoa', 'controllereos'):
        writer.writerow(installbases)

        response['Content-Disposition'] = 'attachment; filename="installbase.csv"'
    return response


def InstallBase_download_view(request, pk):
    download = get_object_or_404(installbase, pk=pk)
    url = download.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(download.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404
