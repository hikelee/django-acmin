import hashlib
import logging
from collections import Iterable
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.db.models.sql.compiler import SQLCompiler
from django.utils.six import wraps

from acmin.utils import attr, memorize

logger = logging.getLogger(__name__)

_cacheable_models = set()


def cacheable(cls):
    _cacheable_models.add(cls)
    return cls


@memorize
def _get_cache_tables():
    return [attr(model, "_meta.db_table").lower() for model in _cacheable_models]


_keywords = ['update', 'insert', 'delete', 'alter', 'create', 'drop']


def _table_names(sql):
    all_tables = _get_cache_tables()
    sql = sql.lower().replace("\t", " ")
    if any([True for keyword in _keywords if f"{keyword} " in sql]):
        return []

    return [name for name in all_tables if name in sql]


def clear(cls):
    if cls in _cacheable_models:
        cache.clear()


def patch():
    if attr(settings, "ACMIN_ENABLE_CACHE"):
        def unset_raw_connection(original):
            def inner(compiler, *args, **kwargs):
                compiler.connection.raw = False
                try:
                    return original(compiler, *args, **kwargs)
                finally:
                    compiler.connection.raw = True

            return inner

        def patch_compiler(original):
            @wraps(original)
            @unset_raw_connection
            def inner(compiler, *args, **kwargs):
                try:
                    s = f"{compiler.as_sql()}"
                    table_names = _table_names(s)
                    md5 = hashlib.md5(bytes(s, "utf-8")).hexdigest()
                    # print(table_names)
                    if table_names:
                        cached_result = cache.get(md5)
                        if cached_result is not None:
                            if attr(settings, "ACMIN_SHOW_CACHE_INFO"):
                                logger.info(f"acmin-cache:{cached_result}")
                            return cached_result

                    result = original(compiler, *args, **kwargs)
                    if table_names:
                        if result.__class__ not in {tuple, list, frozenset, set} and isinstance(result, Iterable):
                            result = list(result)
                        cache.set_many({md5: result})

                    return result
                finally:
                    pass

            return inner

        SQLCompiler.execute_sql = patch_compiler(SQLCompiler.execute_sql)
