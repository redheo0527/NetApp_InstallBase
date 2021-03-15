from django import forms
from .models import ics_part,ics_inout
from bootstrap_datepicker_plus import DatePickerInput


class ics_part_form(forms.ModelForm):
    class Meta:
        model = ics_part
        fields = ['part_num', 'part_description', 'ea']
        widgets = {
            'part_num': forms.TextInput(attrs={'class': 'form-control'}),
            'part_description': forms.TextInput(attrs={'class': 'form-control'}),
            'ea': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'part_num': 'Part Number',
            'part_description': 'Part Description',
            'ea': '초기 수량',
        }

class ics_inout_form(forms.ModelForm):
    class Meta:
        model = ics_inout
        fields = ['inout_id','part_num', 'inout', 'project_name', 'user', 'ea', 'ics_update']
        widgets = {
            'inout_id': forms.TextInput(attrs={'class': 'form-control', 'style': 'display :none'}),
            'part_num': forms.TextInput(attrs={'class': 'form-control'}),
            'ea': forms.TextInput(attrs={'class': 'form-control'}),
            'ics_update': DatePickerInput(format='%Y/%m/%d'),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'inout': forms.Select(choices=((0, '반입'), (1, '반출'))),
        }
        labels = {
            'part_num': 'Part Number',
            'inout': '반입/반출',
            'project_name': '프로젝트명',
            'user': '사용자',
            'ea': '수량',
            'ics_update': '반입/반출 일자',
        }
