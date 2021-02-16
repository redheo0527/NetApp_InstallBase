from django.shortcuts import render
from django.views.generic import ListView
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse
import csv
from installbase.forms import *
from .models import installbase
import urllib
from urllib.parse import urlparse
import os
from django.http import Http404
import mimetypes
from django.shortcuts import get_object_or_404
from django.conf import settings
import json


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
                        Q(customer__icontains=search_keyword) | Q(project_name__icontains=search_keyword) | Q(model__icontains=search_keyword) | Q(osversion__icontains=search_keyword) | Q(serialnumber__icontains=search_keyword) | Q(hostname__icontains=search_keyword) | Q(ipslist__icontains=search_keyword) | Q(diskmodel__icontains=search_keyword) | Q(addlist__icontains=search_keyword) | Q(licensed__icontains=search_keyword) | Q(engineername__icontains=search_keyword))
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
                elif search_type == 'engineername':
                    search_installbase_list = installbase_list.filter(engineername__icontains=search_keyword)
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

def InstallBase_Rack_view(request, pk):
    Installbase = installbase.objects.get(id=pk)
    unit1 = Installbase.unit1_42, Installbase.unit1_41, Installbase.unit1_40, Installbase.unit1_39, Installbase.unit1_38, Installbase.unit1_37, Installbase.unit1_36, Installbase.unit1_35, Installbase.unit1_34, Installbase.unit1_33, Installbase.unit1_32, Installbase.unit1_31, Installbase.unit1_30, Installbase.unit1_29, Installbase.unit1_28, Installbase.unit1_27, Installbase.unit1_26, Installbase.unit1_25, Installbase.unit1_24, Installbase.unit1_23, Installbase.unit1_22, Installbase.unit1_21, Installbase.unit1_20, Installbase.unit1_19, Installbase.unit1_18, Installbase.unit1_17, Installbase.unit1_16, Installbase.unit1_15, Installbase.unit1_14, Installbase.unit1_13, Installbase.unit1_12, Installbase.unit1_11, Installbase.unit1_10, Installbase.unit1_9, Installbase.unit1_8, Installbase.unit1_7, Installbase.unit1_6, Installbase.unit1_5, Installbase.unit1_4, Installbase.unit1_3, Installbase.unit1_2, Installbase.unit1_1
    unit1_desc = Installbase.unit1_42_description, Installbase.unit1_41_description, Installbase.unit1_40_description, Installbase.unit1_39_description, Installbase.unit1_38_description, Installbase.unit1_37_description, Installbase.unit1_36_description, Installbase.unit1_35_description, Installbase.unit1_34_description, Installbase.unit1_33_description, Installbase.unit1_32_description, Installbase.unit1_31_description, Installbase.unit1_30_description, Installbase.unit1_29_description, Installbase.unit1_28_description, Installbase.unit1_27_description, Installbase.unit1_26_description, Installbase.unit1_25_description, Installbase.unit1_24_description, Installbase.unit1_23_description, Installbase.unit1_22_description, Installbase.unit1_21_description, Installbase.unit1_20_description, Installbase.unit1_19_description, Installbase.unit1_18_description, Installbase.unit1_17_description, Installbase.unit1_16_description, Installbase.unit1_15_description, Installbase.unit1_14_description, Installbase.unit1_13_description, Installbase.unit1_12_description, Installbase.unit1_11_description, Installbase.unit1_10_description, Installbase.unit1_9_description, Installbase.unit1_8_description,                              Installbase.unit1_7_description, Installbase.unit1_6_description, Installbase.unit1_5_description, Installbase.unit1_4_description, Installbase.unit1_3_description, Installbase.unit1_2_description, Installbase.unit1_1_description
    unit1_context = zip(unit1, unit1_desc)
    unit2 = Installbase.unit2_42, Installbase.unit2_41, Installbase.unit2_40, Installbase.unit2_39, Installbase.unit2_38, Installbase.unit2_37, Installbase.unit2_36, Installbase.unit2_35, Installbase.unit2_34, Installbase.unit2_33, Installbase.unit2_32, Installbase.unit2_31, Installbase.unit2_30, Installbase.unit2_29, Installbase.unit2_28, Installbase.unit2_27, Installbase.unit2_26, Installbase.unit2_25, Installbase.unit2_24, Installbase.unit2_23, Installbase.unit2_22, Installbase.unit2_21, Installbase.unit2_20, Installbase.unit2_19, Installbase.unit2_18, Installbase.unit2_17, Installbase.unit2_16, Installbase.unit2_15, Installbase.unit2_14, Installbase.unit2_13, Installbase.unit2_12, Installbase.unit2_11, Installbase.unit2_10, Installbase.unit2_9, Installbase.unit2_8, Installbase.unit2_7, Installbase.unit2_6, Installbase.unit2_5, Installbase.unit2_4, Installbase.unit2_3, Installbase.unit2_2, Installbase.unit2_1
    unit2_desc = Installbase.unit2_42_description, Installbase.unit2_41_description, Installbase.unit2_40_description, Installbase.unit2_39_description, Installbase.unit2_38_description, Installbase.unit2_37_description, Installbase.unit2_36_description, Installbase.unit2_35_description, Installbase.unit2_34_description, Installbase.unit2_33_description, Installbase.unit2_32_description, Installbase.unit2_31_description, Installbase.unit2_30_description, Installbase.unit2_29_description, Installbase.unit2_28_description, Installbase.unit2_27_description, Installbase.unit2_26_description, Installbase.unit2_25_description, Installbase.unit2_24_description, Installbase.unit2_23_description, Installbase.unit2_22_description, Installbase.unit2_21_description, Installbase.unit2_20_description, Installbase.unit2_19_description, Installbase.unit2_18_description, Installbase.unit2_17_description, Installbase.unit2_16_description, Installbase.unit2_15_description, Installbase.unit2_14_description, Installbase.unit2_13_description, Installbase.unit2_12_description, Installbase.unit2_11_description, Installbase.unit2_10_description, Installbase.unit2_9_description, Installbase.unit2_8_description, Installbase.unit2_7_description, Installbase.unit2_6_description, Installbase.unit2_5_description, Installbase.unit2_4_description, Installbase.unit2_3_description, Installbase.unit2_2_description, Installbase.unit2_1_description
    unit2_context = zip(unit2, unit2_desc)
    unit3 = Installbase.unit3_42, Installbase.unit3_41, Installbase.unit3_40, Installbase.unit3_39, Installbase.unit3_38, Installbase.unit3_37, Installbase.unit3_36, Installbase.unit3_35, Installbase.unit3_34, Installbase.unit3_33, Installbase.unit3_32, Installbase.unit3_31, Installbase.unit3_30, Installbase.unit3_29, Installbase.unit3_28, Installbase.unit3_27, Installbase.unit3_26, Installbase.unit3_25, Installbase.unit3_24, Installbase.unit3_23, Installbase.unit3_22, Installbase.unit3_21, Installbase.unit3_20, Installbase.unit3_19, Installbase.unit3_18, Installbase.unit3_17, Installbase.unit3_16, Installbase.unit3_15, Installbase.unit3_14, Installbase.unit3_13, Installbase.unit3_12, Installbase.unit3_11, Installbase.unit3_10, Installbase.unit3_9, Installbase.unit3_8, Installbase.unit3_7, Installbase.unit3_6, Installbase.unit3_5, Installbase.unit3_4, Installbase.unit3_3, Installbase.unit3_2, Installbase.unit3_1
    unit3_desc = Installbase.unit3_42_description, Installbase.unit3_41_description, Installbase.unit3_40_description, Installbase.unit3_39_description, Installbase.unit3_38_description, Installbase.unit3_37_description, Installbase.unit3_36_description, Installbase.unit3_35_description, Installbase.unit3_34_description, Installbase.unit3_33_description, Installbase.unit3_32_description, Installbase.unit3_31_description, Installbase.unit3_30_description, Installbase.unit3_29_description, Installbase.unit3_28_description, Installbase.unit3_27_description, Installbase.unit3_26_description, Installbase.unit3_25_description, Installbase.unit3_24_description, Installbase.unit3_23_description, Installbase.unit3_22_description, Installbase.unit3_21_description, Installbase.unit3_20_description, Installbase.unit3_19_description, Installbase.unit3_18_description, Installbase.unit3_17_description, Installbase.unit3_16_description, Installbase.unit3_15_description, Installbase.unit3_14_description, Installbase.unit3_13_description, Installbase.unit3_12_description, Installbase.unit3_11_description, Installbase.unit3_10_description, Installbase.unit3_9_description, Installbase.unit3_8_description, Installbase.unit3_7_description, Installbase.unit3_6_description, Installbase.unit3_5_description, Installbase.unit3_4_description, Installbase.unit3_3_description, Installbase.unit3_2_description, Installbase.unit3_1_description
    unit3_context = zip(unit3, unit3_desc)
    unit4 = Installbase.unit4_42, Installbase.unit4_41, Installbase.unit4_40, Installbase.unit4_39, Installbase.unit4_38, Installbase.unit4_37, Installbase.unit4_36, Installbase.unit4_35, Installbase.unit4_34, Installbase.unit4_33, Installbase.unit4_32, Installbase.unit4_31, Installbase.unit4_30, Installbase.unit4_29, Installbase.unit4_28, Installbase.unit4_27, Installbase.unit4_26, Installbase.unit4_25, Installbase.unit4_24, Installbase.unit4_23, Installbase.unit4_22, Installbase.unit4_21, Installbase.unit4_20, Installbase.unit4_19, Installbase.unit4_18, Installbase.unit4_17, Installbase.unit4_16, Installbase.unit4_15, Installbase.unit4_14, Installbase.unit4_13, Installbase.unit4_12, Installbase.unit4_11, Installbase.unit4_10, Installbase.unit4_9, Installbase.unit4_8, Installbase.unit4_7, Installbase.unit4_6, Installbase.unit4_5, Installbase.unit4_4, Installbase.unit4_3, Installbase.unit4_2, Installbase.unit4_1
    unit4_desc = Installbase.unit4_42_description, Installbase.unit4_41_description, Installbase.unit4_40_description, Installbase.unit4_39_description, Installbase.unit4_38_description, Installbase.unit4_37_description, Installbase.unit4_36_description, Installbase.unit4_35_description, Installbase.unit4_34_description, Installbase.unit4_33_description, Installbase.unit4_32_description, Installbase.unit4_31_description, Installbase.unit4_30_description, Installbase.unit4_29_description, Installbase.unit4_28_description, Installbase.unit4_27_description, Installbase.unit4_26_description, Installbase.unit4_25_description, Installbase.unit4_24_description, Installbase.unit4_23_description, Installbase.unit4_22_description, Installbase.unit4_21_description, Installbase.unit4_20_description, Installbase.unit4_19_description, Installbase.unit4_18_description, Installbase.unit4_17_description, Installbase.unit4_16_description, Installbase.unit4_15_description, Installbase.unit4_14_description, Installbase.unit4_13_description, Installbase.unit4_12_description, Installbase.unit4_11_description, Installbase.unit4_10_description, Installbase.unit4_9_description, Installbase.unit4_8_description, Installbase.unit4_7_description, Installbase.unit4_6_description, Installbase.unit4_5_description, Installbase.unit4_4_description, Installbase.unit4_3_description, Installbase.unit4_2_description, Installbase.unit4_1_description
    unit4_context = zip(unit4, unit4_desc)
    context = {
        'unit1_context': unit1_context,
        'unit2_context': unit2_context,
        'unit3_context': unit3_context,
        'unit4_context': unit4_context,
        'rack1': Installbase.rack1,
        'rack2': Installbase.rack2,
        'rack3': Installbase.rack3,
        'rack4': Installbase.rack4,
        'id': Installbase.id,
    }
    return render(request, 'installbase/rack_view.html', context)


def InstallBase_Rack_update(request, pk):
    Installbase = installbase.objects.get(id=pk)
    if request.method == "POST":
        form = Rackform(request.POST, instance=Installbase)
        if form.is_valid():
            Installbase.save()
            return redirect('/detail/' + str(pk))
        else:
            print(Installbase)
            return redirect('/detail/' + str(pk))
    else:
        Installbase = installbase.objects.get(id=pk)
        form = Rackform(instance=Installbase)
        return render(request, "installbase/rack_update.html", {'form': form})
