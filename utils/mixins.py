from dictdiffer import diff
from simple_history.manager import HistoryManager


class SimpleHistoryDiffMixin(object):
    """DjangoSimpleHistory Object Diff"""
    history = None
    diff_ignore_keys = None

    @staticmethod
    def diff(old_obj1, new_obj2, diff_ignore_keys=None):
        obj1_dict = SimpleHistoryDiffMixin.orm_object_as_dict(old_obj1)
        obj2_dict = SimpleHistoryDiffMixin.orm_object_as_dict(new_obj2)

        if diff_ignore_keys:
            return diff(obj1_dict, obj2_dict, ignore=set(diff_ignore_keys))
        return diff(obj1_dict, obj2_dict)

    @staticmethod
    def orm_object_as_dict(obj):
        return dict([(field.attname, getattr(obj, field.attname)) for field in obj._meta.fields])

    def diff_with_all(self):
        if not self.history or not isinstance(self.history, HistoryManager):
            return []

        history = self.history.all()
        diff_element = []
        if history.count() <= 1:
            return diff_element

        hist_prev = history[0]
        diff_element.append(hist_prev)
        for hist in history:
            if hist_prev == hist:
                continue
            if list(self.diff(hist_prev, hist, diff_ignore_keys=self.diff_ignore_keys)):
                diff_element.append(hist)
                hist_prev = hist

        return diff_element
