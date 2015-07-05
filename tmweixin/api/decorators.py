#!coding: utf-8
__author__ = 'zkchen'


def pull_cache_api(api_klass, api_url, data_key, cache_time, cache_key, success_key=None, **kwargs):
    if success_key is None:
        success_key = (data_key, )
    api = api_klass(api_url=api_url, data_key=data_key, cache_key=cache_key,
                    success_key=success_key, cache_time=cache_time, **kwargs)

    def wraper(func):
        def inner(self):
            ret = func(self, api.get_data())
            return ret

        return inner

    return wraper
