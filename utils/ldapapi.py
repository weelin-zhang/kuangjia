# coding: utf-8
import os
import base64
import hashlib
import logging
from contextlib import contextmanager

import ldap
import ldap.modlist
from ldap.filter import escape_filter_chars

from django.conf import settings

from utils.base import to_bytes, to_string


_log = logging.getLogger(__name__)


class LDAPException(Exception):
    """重写定义自己的异常内容"""
    def __init__(self, message):
        self.message = message


def escape(s):
    """ 转义特殊字符
    """
    if isinstance(s, bytes):
        s = escape_filter_chars(to_string(s))
        return to_bytes(s)
    elif isinstance(s, str):
        return escape_filter_chars(s)
    elif isinstance(s, list):
        return [escape(i) for i in s]
    else:
        return s


class LDAPClient(object):

    @staticmethod
    @contextmanager
    def connect(host=None, port=None, basedn=None, user=None, password=None):
        host = host or settings.LDAP["host"]
        port = port or settings.LDAP["port"]
        basedn = basedn or settings.LDAP["basedn"]
        user = user or settings.LDAP["user"]
        password = password or settings.LDAP["password"]

        ldap_client = LDAPClient(host, port, basedn, user, password)
        try:
            yield ldap_client
        finally:
            ldap_client.close()

    def __init__(self, host, port, basedn, user, password):
        self.basedn = basedn
        self.userdn = settings.LDAP['userdn']
        self.groupdn = settings.LDAP['groupdn']
        self.appdn = settings.LDAP['appdn']

        self.ldap_conn = ldap.initialize("ldap://%s:%s" % (host, port), trace_level=1)
        self.ldap_conn.simple_bind_s(user, password)

    def close(self):
        self.ldap_conn.unbind_s()

    def make_password(self, password, salt=None):
        if not salt:
            salt = os.urandom(4)

        sha = hashlib.sha1(to_bytes(password))
        sha.update(salt)
        digest_salt_b64 = base64.standard_b64encode(to_bytes('{}{}'.format(sha.digest(), salt))).strip()
        tagged_digest_salt = '{{SSHA}}{}'.format(to_string(digest_salt_b64))

        return to_bytes(tagged_digest_salt)

    def check_password(self, tagged_digest_salt, password):
        digest_salt = base64.standard_b64decode(tagged_digest_salt[6:])

        digest = digest_salt[:20]
        salt = digest_salt[20:]

        sha = hashlib.sha1(password)
        sha.update(salt)
        return digest == sha.digest()

    def find_group(self, groupname):
        groupname = escape(groupname)

        entry_list = self.ldap_conn.search_s(self.groupdn,
                                             ldap.SCOPE_SUBTREE,
                                             filterstr=('cn={}'.format(groupname)),
                                             attrlist=["cn", "displayName", "description"],)
        if entry_list:
            return entry_list[0]
        return None

    def create_group(self, name, name_zh, dn=None):
        name = escape(name)
        name_zh = escape(name_zh)
        dn = escape(dn)
        if not dn:
            dn = "cn={},{}".format(name, self.groupdn)

        ou = [("objectclass", (b"group")),
              ("cn", to_bytes(name)),
              ("displayName", to_bytes(name_zh)),
              ("description", to_bytes(name_zh))]
        try:
            self.ldap_conn.add_s(dn, ou)
        except ldap.ALREADY_EXISTS as exc:
            _log.exception(exc)
            raise LDAPException('组名已被占用')

    def update_group(self, name, name_zh, dn=None):
        name = escape(name)
        name_zh = escape(name_zh)
        dn = escape(dn)
        if not dn:
            dn = "cn={}, {}".format(name, self.groupdn)

        ou = [(ldap.MOD_REPLACE, "description", to_bytes(name_zh)),
              (ldap.MOD_REPLACE, "displayName", to_bytes(name_zh)), ]
        self.ldap_conn.modify_s(dn, ou)

    def add_user_to_group(self, user_dn, group_dn):
        user_dn = escape(user_dn)
        group_dn = escape(group_dn)
        if not isinstance(user_dn, list):
            user_dn = [user_dn]

        mod_attrs = [(ldap.MOD_ADD, "Member", [to_bytes(dn) for dn in user_dn])]
        try:
            self.ldap_conn.modify_s(group_dn, mod_attrs)
        except ldap.ALREADY_EXISTS as exc:
            _log.exception(exc)
            raise LDAPException('成员已经存在组里')

    def del_user_from_group(self, user_dn, group_dn):
        user_dn = escape(user_dn)
        group_dn = escape(group_dn)
        if not isinstance(user_dn, list):
            user_dn = [user_dn]

        mod_attrs = [(ldap.MOD_DELETE, "Member", [to_bytes(dn) for dn in user_dn])]
        self.ldap_conn.modify_s(group_dn, mod_attrs)

    def find_user(self, username):
        username = escape(username)
        entry_list = self.ldap_conn.search_s("cn={},{}".format(username, self.userdn),
                                             ldap.SCOPE_BASE,
                                             attrlist=["cn", "displayName", "mail", "description"],)
        if entry_list:
            return entry_list[0]
        return None

    def find_users(self, username_list):
        username_list = escape(username_list)
        filterstr = "(|{})".format(''.join(['(cn={})'.format(u) for u in username_list]))
        return self.ldap_conn.search_s(self.userdn,
                                       ldap.SCOPE_ONELEVEL,
                                       filterstr=filterstr,
                                       attrlist=["cn", "displayName", "mail", "description"],)

    def create_user(self, username, name_zh, email, password, dn=None):
        username = escape(username)
        name_zh = escape(name_zh)
        email = escape(email)
        dn = escape(dn)
        if not dn:
            dn = "cn={},{}".format(username, self.userdn)

        ou = [("Objectclass", (b"inetOrgPerson")),
              ("cn", to_bytes(username)),
              ("userPassword", self.make_password(password)), ]
        if name_zh:
            ou += [("sn", to_bytes(name_zh[0])),
                   ("givenName", to_bytes(name_zh[1:])),
                   ("displayName", to_bytes(name_zh)), ]
        if email:
            ou.append(("mail", to_bytes(email)))
        try:
            self.ldap_conn.add_s(dn, ou)
        except ldap.ALREADY_EXISTS as exc:
            _log.exception(exc)
            raise LDAPException('用户名已被占用')

    def update_user(self, username, name_zh, email, password, dn=None):
        username = escape(username)
        name_zh = escape(name_zh)
        email = escape(email)
        dn = escape(dn)
        if not dn:
            dn = "cn={}, {}".format(username, self.userdn)

        ou = []
        if password:
            ou.append((ldap.MOD_REPLACE, "userPassword", self.make_password(password)))
        if name_zh:
            ou += [(ldap.MOD_REPLACE, "sn", to_bytes(name_zh[0])),
                   (ldap.MOD_REPLACE, "givenName", to_bytes(name_zh[1:])),
                   (ldap.MOD_REPLACE, "displayName", to_bytes(name_zh)), ]
        if email:
            ou.append((ldap.MOD_REPLACE, "mail", to_bytes(email)))
        if not ou:
            return
        try:
            self.ldap_conn.modify_s(dn, ou)
        except ldap.ALREADY_EXISTS as exc:
            _log.exception(exc)
            raise LDAPException('用户名已被占用')

    def add_user_to_app(self, user_dn, app_dn=None):
        """ 先默认只添加到cloud
        """
        user_dn = escape(user_dn)
        app_dn = escape(app_dn)
        if not isinstance(user_dn, list):
            user_dn = [user_dn]
        if not app_dn:
            app_dn = "cn=cloud,{}".format(self.appdn)

        mod_attrs = [(ldap.MOD_ADD, "Member", [to_bytes(dn) for dn in user_dn])]
        try:
            self.ldap_conn.modify_s(app_dn, mod_attrs)
        except ldap.ALREADY_EXISTS as exc:
            _log.exception(exc)
            raise LDAPException('成员已经存在cloud应用里')

    def ola(self):
        pass
