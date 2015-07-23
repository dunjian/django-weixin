#!coding: utf-8
__author__ = 'zkchen'
from django.db import models
from django.db.models.manager import BaseManager, Manager
from .signals import sig_virtual_deletion, sig_virtual_rollback


class VirtualDeletionQuerySet(models.QuerySet):
    """
    改变删除逻辑：删除默认设置is_deleted 为 True
    """
    del_key = "is_deleted"

    def _wrap_kwargs(self, *args, **kwargs):
        try:
            is_deleted = kwargs.pop(self.del_key)
            if is_deleted not in [None, True, False]:
                raise AttributeError(u"is_deleted can only set as False True None")

            # is_deleted 为None则不作限制
            if is_deleted is not None:
                kwargs.update({
                    self.del_key: is_deleted,
                    })
        except KeyError:
            kwargs.update({
                self.del_key: False
            })
        return kwargs

    def get(self, *args, **kwargs):
        kwargs = self._wrap_kwargs(*args, **kwargs)
        return super(VirtualDeletionQuerySet, self).get(*args, **kwargs)


    ######################################
    #   影响filter, exclude 的结果
    ######################################
    def _filter_or_exclude(self, negate, *args, **kwargs):
        """
        如果没有在关键字参数中指定is_deleted,则默认is_deleted为False，即只查询没有被标记为"删除"的数据
        """
        kwargs = self._wrap_kwargs(*args, **kwargs)
        clone = super(VirtualDeletionQuerySet, self)._filter_or_exclude(negate, *args, **kwargs)
        return clone

    def rollback(self):
        """
        设置当前结果集is_deleted False
        """
        return super(VirtualDeletionQuerySet, self).update(is_deleted=False)

    def delete(self, db_delete=False):
        """
        param db_delete: True（从数据库中实际删除), False(只是设置is_deleted True)
        """
        if db_delete is True:
            return super(VirtualDeletionQuerySet, self).delete()
        else:
            return super(VirtualDeletionQuerySet, self).update(is_deleted=True)


class VirtualDeletionBaseManager(BaseManager.from_queryset(VirtualDeletionQuerySet), Manager):
    pass


class VirtualDeletionManagerMixin(VirtualDeletionBaseManager):
    def all(self, is_deleted=False):
        """
        is_deleted: False(调出所有没标记为“删除"的数据）, True(得到所有标记为“删除"的数据）， None（所有数据)
        """
        if is_deleted not in [False, True, None]:
            raise AttributeError(u"is_deleted can only set as False True None")
        q = super(VirtualDeletionManagerMixin, self).all()
        if is_deleted is None:
            return q
        else:
            return q.filter(is_deleted=is_deleted)


class VirtualDeletionMixin(models.Model):
    is_deleted = models.BooleanField(u"已删除", default=False)

    objects = VirtualDeletionManagerMixin()

    def delete(self, using=None):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()
        sig_virtual_deletion.send(sender=self, obj=self)

    def rollback(self):
        if self.is_deleted:
            self.is_deleted = False
            self.save()
        sig_virtual_rollback.send(sender=self, obj=self)

    class Meta:
        abstract = True
