from typing import Callable


class Observable:
    """ 一个简单的观察者模式 """

    def __init__(self):
        self._callbacks = []

    def register_callback(self, callback: Callable):
        self._callbacks.append(callback)

    def unregister_callback(self, callback: Callable):
        self._callbacks.remove(callback)

    def notify_callbacks(self):
        for callback in self._callbacks:
            callback()
