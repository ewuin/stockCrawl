import sys
import os
#from .sqlite import JsonSqliteDict
from subprocess import Popen, PIPE
import six
from six import iteritems
from six.moves.configparser import NoSectionError
import json
from twisted.web import resource

from scrapyd.spiderqueue import SqliteSpiderQueue
from scrapyd.config import Config

import sqlite3
try:
    import cPickle as pickle
except:
    import pickle
import json
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping
import six


class JsonSqliteDict(MutableMapping):
    """SQLite-backed dictionary"""

    def __init__(self, database=None, table="dict"):
        self.database = database or ':memory:'
        self.table = table
        # about check_same_thread: http://twistedmatrix.com/trac/ticket/4040
        self.conn = sqlite3.connect(self.database, check_same_thread=False)
        q = "create table if not exists %s (key blob primary key, value blob)" \
            % table
        self.conn.execute(q)

    def __getitem__(self, key):
        key = self.encode(key)
        q = "select value from %s where key=?" % self.table
        value = self.conn.execute(q, (key,)).fetchone()
        if value:
            return self.decode(value[0])
        raise KeyError(key)

    def __setitem__(self, key, value):
        key, value = self.encode(key), self.encode(value)
        q = "insert or replace into %s (key, value) values (?,?)" % self.table
        self.conn.execute(q, (key, value))
        self.conn.commit()

    def __delitem__(self, key):
        key = self.encode(key)
        q = "delete from %s where key=?" % self.table
        self.conn.execute(q, (key,))
        self.conn.commit()

    def __len__(self):
        q = "select count(*) from %s" % self.table
        return self.conn.execute(q).fetchone()[0]

    def __iter__(self):
        for k in self.iterkeys():
            yield k

    def iterkeys(self):
        q = "select key from %s" % self.table
        return (self.decode(x[0]) for x in self.conn.execute(q))

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        q = "select value from %s" % self.table
        return (self.decode(x[0]) for x in self.conn.execute(q))

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        q = "select key, value from %s" % self.table
        return ((self.decode(x[0]), self.decode(x[1])) for x in self.conn.execute(q))

    def items(self):
        return list(self.iteritems())

    def encode(self, obj):
        return sqlite3.Binary(json.dumps(obj).encode('ascii'))

    def decode(self, obj):
        return json.loads(bytes(obj).decode('ascii'))



class UtilsCache:
    # array of project name that need to be invalided
    invalid_cached_projects = []

    def __init__(self):
        self.cache_manager = JsonSqliteDict(table="utils_cache_manager")

    # Invalid the spider's list's cache of a given project (by name)
    @staticmethod
    def invalid_cache(project):
        UtilsCache.invalid_cached_projects.append(project)

    def __getitem__(self, key):
        for p in UtilsCache.invalid_cached_projects:
            if p in self.cache_manager:
                del self.cache_manager[p]
        UtilsCache.invalid_cached_projects[:] = []
        return self.cache_manager[key]

    def __setitem__(self, key, value):
        self.cache_manager[key] = value


def get_project_list(config):
    """Get list of projects by inspecting the eggs dir and the ones defined in
    the scrapyd.conf [settings] section
    """
    eggs_dir = config.get('eggs_dir', 'eggs')
    if os.path.exists(eggs_dir):
        projects = os.listdir(eggs_dir)
    else:
        projects = []
    try:
        projects += [x[0] for x in config.cp.items('settings')]
    except NoSectionError:
        pass
    return projects

def get_spider_list(project, runner=None, pythonpath=None, version=''):
    """Return the spider list from the given project, using the given runner"""
    if "cache" not in get_spider_list.__dict__:
        get_spider_list.cache = UtilsCache()
    try:
        return get_spider_list.cache[project][version]
    except KeyError:
        pass
    if runner is None:
        runner = Config().get('runner')
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'UTF-8'
    #env['SCRAPY_PROJECT'] = project   change to:   because encoding is utf-8, this would not be necessary in python 3?
    env['SCRAPY_PROJECT'] = str(project.decode('utf8'))
    print "type of env [scrapy_prokject]: ", type(env['SCRAPY_PROJECT'])
    #print env
    if pythonpath:
        env['PYTHONPATH'] = pythonpath
        print pythonpath
        #env['PYTHONPATH'] = str(pythonpath.decode('utf8'))
    if version:
        env['SCRAPY_EGG_VERSION'] = version
        print version
        #env['SCRAPY_EGG_VERSION'] = str(version.decode('utf8'))
        #env['SCRAPY_EGG_VERSION'] = version change to ^   because encoding is utf-8
    print
    pargs = [sys.executable, '-m', runner, 'list']
    proc = Popen(pargs, stdout=PIPE, stderr=PIPE, env=env)
    out, err = proc.communicate()
    #if proc.returncode:
    #    msg = err or out or ''
    #    msg = msg.decode('utf8')
    #    raise RuntimeError(msg.encode('unicode_escape') if six.PY2 else msg)
    # FIXME: can we reliably decode as UTF-8?
    # scrapy list does `print(list)`
    tmp = out.decode('utf-8').splitlines();
    print tmp
    try:
        project_cache = get_spider_list.cache[project]
        project_cache[version] = tmp
    except KeyError:
        project_cache = {version: tmp}
    get_spider_list.cache[project] = project_cache
    return tmp

sList=get_spider_list('stockBot')
print sList
