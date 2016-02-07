# coding:utf-8
from spyne import srpc, Integer, Unicode, Iterable, Date, Boolean

from .models import Institution, Person


# curl "http://localhost:8000/wsfactory/api/DemoService/GetInstitutions" | tidy -q -xml -indent -wrap 0
@srpc(_returns=Iterable(Unicode, member_name="Institution"), _out_variable_name="Institutions")
def get_institutions():
    return {"%s/%s" % (i[0], i[1]) for i in Institution.objects.filter(children__isnull=True).values_list("id", "name")}


# curl "http://localhost:8000/wsfactory/api/DemoService/AddPerson?name=name&surname=surname&patronymic=patronymi&date_of_birth=1979-09-20&institution=9" | tidy -q -xml -indent -wrap 0
@srpc(
    Unicode,
    Unicode,
    Unicode,
    Date,
    Integer,
    _returns=Boolean)
def add_person(name, surname, patronymic, date_of_birth, institution):
    try:
        i = Institution.objects.filter(pk=institution, children__isnull=True).values("id")[0].get("id", None)
        o = Person()
        o.name = name
        o.surname = surname
        o.patronymic = patronymic
        o.date_of_birth = date_of_birth
        o.institution_id = i
        o.save()
        return True
    except Exception, e:
        print 'error: %s' % e
        return False
