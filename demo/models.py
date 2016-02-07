# coding: utf-8
import datetime

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Person(models.Model):
    GENDERS = (
        (0, u'Женский'),
        (1, u'Мужской')
    )

    name = models.CharField(
        u'Имя', max_length=50)
    surname = models.CharField(
        u'Фамилия', max_length=50)
    patronymic = models.CharField(
        u'Отчество', max_length=50)
    date_of_birth = models.DateField(
        u'Дата рождения',
        null=True,
        default=datetime.date.today
    )
    gender = models.SmallIntegerField(
        u'Пол',
        choices=GENDERS,
        default=GENDERS[1][0]
    )
    institution = models.ForeignKey(
        'Institution', verbose_name=u'Учреждение',
        related_name='institution_set',
        null=True, blank=True,
    )

    @property
    def fullname(self):
        return u' '.join((self.name, self.surname, self.patronymic))

    def __unicode__(self):
        return self.fullname

    class Meta:
        verbose_name = u'Физическое лицо'
        verbose_name_plural = u'Физические лица'


class Institution(MPTTModel):
    name = models.CharField(
        u'Наименование', max_length=50)
    inn = models.CharField(
        u'Инн', max_length=50, null=True, blank=True)
    kpp = models.CharField(
        u'Кпп', max_length=50, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name=u'Министерство')

    def __unicode__(self):
        return self.name

    def safe_delete(self):
        if not self.get_children():
            self.delete()
            return True

    class Meta:
        verbose_name = u'Учреждение'
        verbose_name_plural = u'Учреждения'
