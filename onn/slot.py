# -*- coding: utf-8 -*-
"""One Neural Network-Slot."""


class Slot:
    """Any Class save in Slot."""

    def __init__(self):
        """Init."""
        self._class_table = {}

    def _load(self, cls_name, cls):
        """Load cls to class table."""
        self._class_table[cls_name] = cls

    def push(self):
        """Push cls to class table."""

        def _inner_func(cls):
            cls_name = cls.__module__ + "." + cls.__name__
            self._load(cls_name, cls)
            return cls

        return _inner_func

    def pop(self, cls_name):
        """Pop Class from class table."""
        return self._class_table[cls_name]

    def __str__(self):
        """Return str expr."""
        expr = ""
        for i, cls_name in enumerate(self._class_table.keys()):
            expr += f"[{cls_name}] "
            if i % 20 == 0:
                expr += "\n"
        return expr


TRITON = Slot()
