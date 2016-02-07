# coding:utf-8
from objectpack import observer


obs = observer.Observer()

action_controller = observer.ObservableController(obs, "/controller")

