# coding: utf-8

from django.conf import urls

from objectpack import desktop

from . import actions
from . import controller


def register_urlpatterns():
    return urls.patterns(
        "",
        controller.action_controller.urlpattern
    )


def register_actions():
    controller.action_controller.packs.extend([
        actions.PersonObjectPack(),
        actions.InstitutionTreeObjectPack(),
    ])


def register_desktop_menu():
    desktop.uificate_the_controller(
        controller.action_controller
    )
