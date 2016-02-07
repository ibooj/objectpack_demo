# coding:utf-8
import objectpack
from objectpack import tree_object_pack


from .controller import obs
from . import models


class PersonObjectPack(objectpack.ObjectPack):
    model = models.Person
    add_to_desktop = True
    add_to_menu = True

    edit_window = add_window = objectpack.ui.ModelEditWindow.fabricate(
        model,
        model_register=obs,
        field_list=[
            'name',
            'surname',
            'patronymic',
            'date_of_birth',
            'gender',
            'institution_id'
        ],
    )

    columns = [
        {
            'data_index': 'surname',
            'header': u'Фамилия',
            'sortable': True,
            'sort_fields': ('surname',),
            'filter': {
                'type': 'string',
                'custom_field': ('surname',)
            }
        },
        {
            'data_index': 'name',
            'header': u'Имя',
            'sortable': True,
            'sort_fields': ('name',),
            'filter': {
                'type': 'string',
                'custom_field': ('name',)
            }
        },
        {
            'data_index': 'patronymic',
            'header': u'Отчество',
            'sortable': True,
            'sort_fields': ('patronymic',),
            'filter': {
                'type': 'string',
                'custom_field': ('patronymic',)
            }
        },
        {
            'data_index': 'date_of_birth',
            'header': u'Дата рождения',
            'filter': {
                'type': 'date'
            }
        },
        {
            'data_index': 'gender',
            'header': u'Пол',
            'filter': {
                'type': 'list',
                'options': models.Person.GENDERS
            }
        },
        {
            'data_index': 'institution',
            'header': u'Учреждение'
        }

    ]

    def extend_menu(self, menu):
        return (
            menu.registries(
                menu.Item(u'Физические лица', self)
            )
        )


class InstitutionTreeObjectPack(tree_object_pack.TreeObjectPack):
    model = models.Institution
    add_to_desktop = True
    add_to_menu = True

    add_window = objectpack.ui.ModelEditWindow.fabricate(
        model,
        model_register=obs,
        field_list=[
            'name',
            'inn',
            'kpp'
        ],
    )
    edit_window = objectpack.ui.ModelEditWindow.fabricate(
        model,
        model_register=obs,
        field_list=[
            'name',
            'inn',
            'kpp',
            'parent_id'
        ],
    )

    columns = [
        {
            "data_index": "name",
            "header": u"Наименование"
        },
        {
            "data_index": "inn",
            "header": u"Инн"
        },
        {
            "data_index": "kpp",
            "header": u"Кпп"
        }
    ]

    def extend_menu(self, menu):
        return (
            menu.dicts(
                menu.Item(u'Учреждения', self)
            )
        )

    def save_row(self, obj, create_new, request, context):
        parent_id = getattr(context, 'parent_id', None)
        setattr(obj, 'parent_id', parent_id)
        if not create_new and parent_id:
            # если так не сделать то ругнется что нет атрибута tree_id
            getattr(obj.parent, 'tree_id')

        obj.save()
