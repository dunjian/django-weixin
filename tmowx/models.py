#!coding=utf-8
from django.db import models
from tmkit.db.virtualdeletion import VirtualDeletionMixin, VirtualDeletionManagerMixin


FUNC_INFO_LIST = (
    (1, u"消息与菜单"),
    (2, u"用户管理"),
    (3, u"帐号管理"),
    (4, u"网页授权"),
    (5, u"微信小店"),
    (6, u"多客服"),
    (7, u"业务通知"),
    (8, u"微信卡券"),
    (9, u"微信扫一扫"),
)


class Authorizer(VirtualDeletionMixin):
    """
    微信授权方
    """
    authorizer_info = models.CharField(u"授权方昵称", max_length=250)
    head_img = models.CharField(u"授权方头像（资源地址)", max_length=500)
    service_type_info = models.IntegerField(u"公众号类型", choices=((0, u"订阅号"), (1, u"历史订阅号"), (2, u"服务号")))
    verify_type_info = models.IntegerField(u"授权方认证类型", choices=(
        (-1, u"未认证"), (0, u"微信认证"), (1, u"新浪微博认证"), (2, u"腾讯微博认证"),
        (3, u"还未通过名称认证"), (4, u"通过了新浪微博认证"), (5, u"通过了腾讯微博认证")
    ))
    user_name = models.CharField(u"原始ID", max_length=250)
    alias = models.CharField(u"授权方设置的微信号", null=True, blank=True, max_length=250)
    qrcode_url = models.CharField(u"二维码图片url", max_length=500)
    appid = models.CharField(u"授权方appid", max_length=250)
    func_info_list = models.CharField(u"权限集", max_length=100, help_text=u"以分号分隔的字符列表")

    def func_info(self):
        data = self.func_info_list.split(";")
        func_dict = dict(FUNC_INFO_LIST)
        ret = {}
        for k in data:
            k = int(k)
            ret[k] = func_dict[k]
        return ret

    def has_func(self, key_id):
        """
        是否存在该权限
        """
        return self.func_info().get(key_id)

    def __unicode__(self):
        return "%s" % self.user_name

    class Meta:
        verbose_name = u"授权方"
        verbose_name_plural = u"授权方管理"


class AuthorizerMixin(VirtualDeletionMixin):
    authorizer = models.ForeignKey("Authorizer", verbose_name=u"授权方")

    class Meta:
        abstract = True


class WMenu(AuthorizerMixin):
    """
    微信菜单
    """
    MENU_TYPE_CHOICES = (('click', u'点击'), ('view', u'查看',), ('parent', u'父菜单'))
    parent = models.ForeignKey('self', verbose_name=u'父菜单', null=True, blank=True, \
                               related_name='children')
    menu_type = models.CharField(u'菜单类型', max_length=10, choices=MENU_TYPE_CHOICES, \
                                 help_text=u'类型为"父菜单",则必须要有子菜单')
    name = models.CharField(u'菜单名称', max_length=20)
    value = models.CharField(u'值', help_text=u'类型为"点击",则输入键码，如果类型为"查看",则输入url', \
                             max_length=256, null=True, blank=True)
    position = models.IntegerField(u'顺序')

    def __unicode__(self):
        return "%s of %s" % (self.name, self.authorizer)

    class Meta:
        verbose_name = u"微信菜单"
        verbose_name_plural = u"微信菜单管理"


class User(AuthorizerMixin):
    """
    用户
    """
    SEX_CHOICES = (('1', u'男'), ('0', u'女'), ('2', u'未提交'))
    openid = models.CharField(max_length=50, blank=False, primary_key=True)
    nickname = models.CharField(u'昵称', max_length=50, blank=True, null=True)
    sex = models.CharField(u'性别', choices=SEX_CHOICES, default='2', max_length=10, blank=True, null=True)
    telephone = models.CharField(u'手机号', max_length=11, blank=True, null=True)
    is_active = models.BooleanField(u'是否验证', default=False)
    active_at = models.CharField(u'最新手机验证时间', max_length=50, blank=True, null=True)
    latitude = models.CharField(u'经度', max_length=50, blank=True, null=True)
    longitude = models.CharField(u'纬度', max_length=50, blank=True, null=True)
    precision = models.CharField(u'精度', max_length=50, blank=True, null=True)
    modify_at = models.CharField(u'最新经纬度时间', max_length=50, blank=True, null=True)
    city = models.CharField(u'城市', max_length=100, blank=True, null=True)
    province = models.CharField(u'省份', max_length=100, blank=True, null=True)
    headimgurl = models.URLField(u'用户头像图片地址', blank=True, null=True)
    subscribe_time = models.CharField(u'关注公众账号时间', max_length=50, blank=True, null=True)

    def __unicode__(self):
        return '<%s %s[%s]> of %s' % ("tmowx.User", self.openid, self.nickname, self.authorizer)

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = u"用户管理"


