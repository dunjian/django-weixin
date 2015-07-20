#!coding:utf-8
__author__ = 'akun'
import pickle
from django.db.models import SubfieldBase
from django.db.models import Field


class PythonObjectField(Field):
    __metaclass__ = SubfieldBase
    description = u"python obj pickle str"

    def __init__(self, *args, **kwargs):
        super(PythonObjectField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        value = super(PythonObjectField, self).to_python(value)
        if value is None:
            return value
        try:
            value = pickle.loads(value)
        except Exception as e:
            try:
                value = eval(value)
            except Exception:
                pass
                # raise ValidationError(u"invalid data:%s type:%s" % (value, type(value)))
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        p_value = value
        return pickle.dumps(p_value)

