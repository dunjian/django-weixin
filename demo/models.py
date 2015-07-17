#!coding:utf-8
__author__ = 'akun'
from django.db import models
from django.dispatch import Signal
from django.db.models.manager import BaseManager


sig_virtual_deletion = Signal(providing_args=["obj"])
sig_virtual_rollback = Signal(providing_args=["obj"])


class VirtualDeletionManagerMixin(BaseManager):
    def all(self, is_deleted=False):
        """
        :param is_deleted: False(调出所有没标记为“删除"的数据）, True(得到所有标记为“删除"的数据）， None（所有数据)
        """
        if is_deleted not in [False, True, None]:
            raise AttributeError(u"is_deleted can only set as False True None")
        q = super(VirtualDeletionManagerMixin, self).all()
        if is_deleted is None:
            return q
        else:
            return q.filter(is_deleted=is_deleted)

    ######################################
    #   影响filter, exclude 的结果
    ######################################
    def _filter_or_exclude(self, negate, *args, **kwargs):
        """
        如果没有在关键字参数中指定is_deleted,则默认is_deleted为False，即只查询没有被标记为"删除"的数据
        """
        try:
            is_deleted = kwargs.pop("is_deleted")
            if is_deleted not in [None, True, False]:
                raise AttributeError(u"is_deleted can only set as False True None")

            # is_deleted 为None则不作限制
            if is_deleted is not None:
                kwargs.update({
                    "is_deleted": is_deleted,
                })
        except KeyError:
            # 未设定is_deleted关键字参数则默认设定为False
            kwargs.update({
                "is_deleted": False
            })

        clone = super(VirtualDeletionManagerMixin, self)._filter_or_exclude(negate, *args, **kwargs)
        return clone


class VirtualDeletionMixin(models.Model):
    is_deleted = models.BigIntegerField(u"已删除", default=False)

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
        sig_virtual_deletion.send(sender=self, obj=self)

    class Meta:
        abstract = True


class Blog(VirtualDeletionMixin):
    name = models.CharField(u"名字", max_length=250)

    class Meta(VirtualDeletionMixin.Meta):
        abstract = False
        verbose_name_plural = u"博客管理"
        verbose_name = u"博客"

    def __unicode__(self):
        return self.name


class Entry(VirtualDeletionMixin):
    blog = models.ForeignKey("Blog", verbose_name=u"所属博客")
    title = models.CharField(u"标题", max_length=250)
    content = models.TextField(u"内容", blank=True, null=True)

    def __unicode__(self):
        return "%s [%s]" % (self.title, self.blog.name)

    class Meta:
        abstract = False
        verbose_name_plural = u"文章管理"
        verbose_name = u"文章"

