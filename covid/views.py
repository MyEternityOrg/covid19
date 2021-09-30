from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Enterprises, Persons, persons_covid19, TimeSheetPlane, covid19_vtype, covid19_dtype, \
    covid19_reply_codes
from datetime import datetime, date, time, timedelta
from django.db.models import Q
from django.utils import dateformat
from django.contrib import messages
import uuid
from django.contrib.auth.decorators import login_required
from operator import or_, not_, and_
from functools import reduce
from django.db import connection


def person_covid(request):
    if request.method == 'POST':

        if request.POST['close_save'] == "Сохранить":

            for i in range(int(request.POST['len_list'])):
                enterprise = Enterprises.objects.get(guid=request.POST['enterprise'])
                # vaccinated = request.POST['vaccinated' + str(i)]
                # contraindications = request.POST['contraindications' + str(i)]
                # having_qr_code = request.POST['having_qr_code' + str(i)]
                reply_code = request.POST['reply_code' + str(i)]
                person_covid = Persons.objects.get(guid=request.POST['person_guid' + str(i)])
                dts = datetime.today()

                # if vaccinated == '--------' or contraindications == '--------':
                #     messages.warning(request, "ОШИБКА! нет данных! сотрудник: " + str(person_covid))
                #     continue

                find_row = persons_covid19.objects.filter(enterprise_guid=enterprise,
                                                          person_guid=person_covid,
                                                          dts=dts).first()

                # if find_row == None:
                #     persons_covid19.objects.create(
                #         uid=str(uuid.uuid4()),
                #         enterprise_guid=enterprise,
                #         person_guid=person_covid,
                #         dts=dts,
                #         vaccination_type=0 if vaccinated == 'true' else 1,
                #         vaccination_declined=1 if contraindications == 'true' else 0,
                #         having_qr_code=1 if having_qr_code == 'true' else 0,
                #     )
                # else:
                #     find_row.enterprise_guid = enterprise
                #     find_row.person_guid = person_covid
                #     find_row.dts = dts
                #     find_row.vaccination_type = 0 if vaccinated == 'true' else 1
                #     find_row.vaccination_declined = 1 if contraindications == 'true' else 0
                #     find_row.having_qr_code = 1 if having_qr_code == 'true' else 0
                #     find_row.save()

                if find_row == None:
                    persons_covid19.objects.create(
                        uid=str(uuid.uuid4()),
                        enterprise_guid=enterprise,
                        person_guid=person_covid,
                        dts=dts,
                        vaccination_type=0,
                        vaccination_declined=0,
                        having_qr_code=0,
                        reply_code=reply_code,
                    )
                else:
                    find_row.enterprise_guid = enterprise
                    find_row.person_guid = person_covid
                    find_row.dts = dts
                    find_row.vaccination_type = 0
                    find_row.vaccination_declined = 0
                    find_row.having_qr_code = 0
                    find_row.reply_code = reply_code
                    find_row.save()

            return HttpResponse('<h1>Данные отправлены</h1>')

    else:

        this_enterprise = get_enterprise_ip(request)

        this_today = datetime.today()
        list_obj = TimeSheetPlane.objects.filter(enterprise_guid=this_enterprise, dts=this_today, suspicious=0).exclude(
            busy_key_guid='E1916359-15C4-11E9-8112-00155D6DE618').distinct()

        list_codes = covid19_reply_codes.objects.all()

        return render(request, 'covid/person_covid_v2.html', {'list_obj': list_obj,
                                                           'enterprise': this_enterprise,
                                                           'len_list': len(list_obj),
                                                           'list_codes': list_codes})


def get_local_ip_client(request):
    return request.META['REMOTE_ADDR']


def get_enterprise_ip(request):
    ip_adress = get_local_ip_client(request)

    print(ip_adress)
    list_number = ip_adress.split('.')
    number_shop = ('' if list_number[1] == '0' else list_number[1]) + (
        list_number[2] if len(list_number[2]) > 1 else ('0' + list_number[2]))
    print(number_shop)
    shop_number = Enterprises.objects.filter(enterprise_code=number_shop).first()
    print(shop_number)
    if shop_number == None:
        return Enterprises.objects.get(guid='5409EFB9-53D8-11EB-80D4-00155D6DE62E')
    return Enterprises.objects.get(guid=shop_number.guid)
