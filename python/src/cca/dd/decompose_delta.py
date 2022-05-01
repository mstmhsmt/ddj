#!/usr/bin/env python3

'''
  decompose_delta.py

  Copyright 2018-2022 Chiba Institute of Technology

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
'''

__author__ = 'Masatomo Hashimoto <m.hashimoto@stair.center>'

import os
import sys
import networkx as nx
import xml.etree.cElementTree as et
import copy
import random
import logging

from .common import VIRTUOSO_PW, VIRTUOSO_PORT

from cca.ccautil import project, sparql
from cca.ccautil.sparql import get_localname
from cca.ccautil.ns import PREFIX_TBL
from cca.ccautil.common import setup_logger

from cca.factutil.const import SEP
from cca.factutil.entity import SourceCodeEntity

from .queries import K_INS, K_DEL, K_REL, K_MOV, KINDS
from .queries import QUERY_TBL, QUERY_LIST, REF_QUERY_TBL
from .queries import OTH_QUERY_TBL, OTH_DIR_QUERY_TBL
from .queries import STMT_QUERY, MODIFIED_STMT_QUERY, FILE_LOC_QUERY
from .queries import CONTAINING_FILE_QUERY, MAPPED_FILE_QUERY
from .queries import REMOVED_FILE_QUERY, ADDED_FILE_QUERY
from .queries import CONTAINING_METH_QUERY, REMOVED_METH_QUERY
from .queries import ADDED_METH_QUERY, CONTAINING_STMT_QUERY
from .queries import MAPPED_STMT_QUERY, REMOVED_STMT_QUERY
from .queries import ADDED_STMT_QUERY, VER_PAIR_QUERY, Q_DELTA_XML
from .queries import Q_MODIFIED_PATH, VER_QUERY, MAPPED_METH_QUERY

logger = logging.getLogger()

MAX_STMT_LEVEL = 8
MODIFIED_STMT_RATE_THRESH = 0.05

CHGINST_PREFIX = PREFIX_TBL['chginst']
ENT_PREFIX = PREFIX_TBL['ent']

XDD_NS = 'http://codinuum.com/diffts/delta/'

XML_HEAD = '<?xml version="1.0" encoding="UTF-8"?>'

DELTA_BUNDLE_HEAD = '<xdd:bundle xmlns:xdd="%s">' % XDD_NS
DELTA_BUNDLE_TAIL = '</xdd:bundle>'

DELTA_HEAD = '<xdd:delta xdd:lang="%(lang)s" xdd:location="%(loc)s">'
DIR_DELTA_HEAD = '<xdd:delta xdd:lang="%(lang)s">'
DELTA_TAIL = '</xdd:delta>'

et.register_namespace('xdd', XDD_NS)


def make_make_query_id(lang):
    def f(n):
        return 'Q_%s_%s' % (n.upper(), lang.upper())
    return f


def make_query_id(n):
    return 'Q_%s' % n.upper()


def cids_to_string(cids):
    return ','.join([str(x) for x in sorted(list(cids), key=getnum)])


def mkgid(i):
    return 'G%d' % i


def mktmpgid(i):
    return 'g%d' % i


def isgid(x):
    b = False
    if isinstance(x, str):
        b = x.startswith('G')
    return b


def getnum(x):
    n = None
    if isinstance(x, str):
        if x.startswith('G'):
            n = int(x.lstrip('G'))
        elif x.startswith('g'):
            n = int(x.lstrip('g'))
        else:
            n = int(x)
    elif isinstance(x, int):
        n = x
    return n


def insert_attrs(xml, attrs):
    s = xml
    if attrs:
        root = et.fromstring(DELTA_BUNDLE_HEAD+xml+DELTA_BUNDLE_TAIL)
        e = root[0]
        for k, v in attrs:
            e.set(k, v)
        sl = et.tostringlist(root[0], encoding='unicode')
        s = ''.join(filter(lambda x: not x.lstrip().startswith('xmlns'), sl))
    return s


def tbl_add(tbl, key, value):
    try:
        vl = tbl[key]
        if value not in vl:
            vl.append(value)
    except KeyError:
        tbl[key] = [value]


def set_tbl_add(tbl, key, value):
    try:
        s = tbl[key]
        if isinstance(value, set):
            s |= value
        elif value not in s:
            s.add(value)
    except KeyError:
        if isinstance(value, set):
            tbl[key] = value
        else:
            tbl[key] = set([value])


def add_suffix(path, suffix):
    (root, ext) = os.path.splitext(path)
    r = root+suffix+ext
    return r


def vp_to_str(vp):
    (v, v_) = vp
    return '%s-%s' % (get_localname(v), get_localname(v_))


def add_vp_suffix(path, vp):
    suffix = '_%s' % vp_to_str(vp)
    r = add_suffix(path, suffix)
    return r


def capitalize(s):
    if s.isupper():
        return s
    else:
        return s.capitalize()


class Edit(object):
    def __init__(self, kind, ent, ent_, loc, loc_, cat):
        self.kind = kind
        self.ent = ent
        self.ent_ = ent_
        self.loc = loc
        self.loc_ = loc_

        self.key = (kind, (ent, ent_))

        self.cat = None
        self.cats = []
        if cat:
            self.cat = get_localname(cat)
            self.cats = self.cat.split('|')

        self.ent_obj = SourceCodeEntity(uri=ent)
        self.ent_obj_ = SourceCodeEntity(uri=ent_)

        r = None
        self.sl = None
        self.sc = None
        self.el = None
        self.ec = None
        self.so = None
        self.eo = None
        try:
            r = self.ent_obj.get_range()
        except Exception:
            pass
        if r:
            self.sl = r.get_start_line()
            self.el = r.get_end_line()
            self.sc = r.get_start_col()
            self.ec = r.get_end_col()
            self.so = r.get_start_offset()
            self.eo = r.get_end_offset()

        r_ = None
        self.sl_ = None
        self.sc_ = None
        self.el_ = None
        self.ec_ = None
        self.so_ = None
        self.eo_ = None
        try:
            r_ = self.ent_obj_.get_range()
        except Exception:
            pass
        if r_:
            self.sl_ = r_.get_start_line()
            self.el_ = r_.get_end_line()
            self.sc_ = r_.get_start_col()
            self.ec_ = r_.get_end_col()
            self.so_ = r_.get_start_offset()
            self.eo_ = r_.get_end_offset()

        self.xkey = (kind, self.sl, self.sc, self.el, self.ec, loc,
                     self.sl_, self.sc_, self.el_, self.ec_, loc_)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        b = False
        if isinstance(other, Edit):
            b = self.key == other.key
        return b

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_string(self, short=True):
        if short:
            if self.cat == 'File':
                s = '%s %s [%s]' % (self.kind, self.cat, self.loc)
            else:
                p = (self.kind, self.cat,
                     self.sl, self.sc, self.el, self.ec, self.loc)
                if self.kind == K_INS:
                    p = (self.kind, self.cat,
                         self.sl_, self.sc_, self.el_, self.ec_, self.loc_)
                s = '%s %s [%d:%d-%d:%d %s]' % p
        else:
            if self.cat == 'File':
                s = '%s %s [%s]-[%s]' % (self.kind,
                                         self.cat,
                                         self.loc,
                                         self.loc_)
            else:
                s = ('{} {} [{}:{}-{}:{} {}]-[{}:{}-{}:{} {}]'
                     .format(self.kind,
                             self.cat,
                             self.sl, self.sc,
                             self.el, self.ec,
                             self.loc,
                             self.sl_, self.sc_,
                             self.el_, self.ec_,
                             self.loc_))
        return s

    def to_html(self):
        kind = self.kind
        if kind == 'DEL':
            kind = f'<span class="del">{kind}</span>'
        elif kind == 'INS':
            kind = f'<span class="ins">{kind}</span>'
        elif kind == 'REL':
            kind = f'<span class="rel">{kind}</span>'
        elif kind == 'MOV':
            kind = f'<span class="mov">{kind}</span>'
        elif kind == 'MOVREL':
            kind = f'<span class="movrel">{kind}</span>'

        if self.cat == 'File':
            loc_ = '-[{}]'.format(self.loc_) if self.loc != self.loc_ else ''
            s = '{} <span class="name">{}</span> [{}]{}'.format(self.kind,
                                                                self.cat,
                                                                self.loc,
                                                                loc_)
        else:
            loc_ = ' '+self.loc_ if self.loc != self.loc_ else ''
            s = ('{} <span class="name">{}</span> [{}:{}-{}:{} {}]-[{}:{}-{}:{}{}]'
                 .format(kind,
                         self.cat,
                         self.sl, self.sc,
                         self.el, self.ec,
                         self.loc,
                         self.sl_, self.sc_,
                         self.el_, self.ec_,
                         loc_))
        return s

    def __str__(self):
        return self.to_string(short=False)

    def mkchginst(self):
        uri = CHGINST_PREFIX+SEP.join([get_localname(self.ent),
                                       get_localname(self.ent_),
                                       self.kind])
        return uri

    @classmethod
    def of_chginst(cls, inst):
        s = inst.replace(CHGINST_PREFIX, '')
        sl = s.split(SEP)
        kind = sl[6]
        ent = ENT_PREFIX+SEP.join(sl[0:3])
        ent_ = ENT_PREFIX+SEP.join(sl[3:6])
        edit = Edit(kind, ent, ent_, None, None, None)
        return edit


class Hunk(object):
    def __init__(self, root):
        self.root = root

        self.key = root.key

        self.sort_key = (root.ent, root.ent_, root.kind)

        if root is None:
            logger.warning('invalid root')

        self.members = set()

        self._parent = None

        self.parent = None
        self.children = set()

    def add_member(self, mem):
        self.members.add(mem)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        b = False
        if isinstance(other, Hunk):
            b = self.key == other.key
        return b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.key > other.key

    def __lt__(self, other):
        return self.key < other.key

    def to_html(self):
        s = 'HUNK ({}) {}'.format(len(self.members), self.root.to_html())
        return s

    def __str__(self):
        s = 'HUNK (%d) %s' % (len(self.members), self.root)
        return s

    def get_chginst(self):
        return self.root.mkchginst()

    @classmethod
    def of_chginst(cls, inst):
        edit = Edit.of_chginst(inst)
        return Hunk(edit)

    def get_kind(self):
        return self.root.kind

    def get_loc(self):
        return self.root.loc

    def get_loc_(self):
        return self.root.loc_


class Ref(object):
    def __init__(self, ref, sig):
        self.ref = ref
        self.sig = sig
        self.refname = get_localname(ref).split(SEP)[-1]
        self.key = ref

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        b = False
        if isinstance(other, Ref):
            b = self.key == other.key
        return b

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_html(self):
        refname = ' '.join([capitalize(w) for w in self.refname.split('_')])
        s = ('<span class="ref">{}</span> <span class="code">{}</span>'
             .format(refname, self.sig))
        return s

    def __str__(self):
        s = 'REF %s %s' % (self.refname, self.sig)
        return s


class Chg(object):
    def __init__(self, key, key_, kind, name):
        self.key = (key, key_, kind)
        self.name = name

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        b = False
        if isinstance(other, Chg):
            b = self.key == other.key
        return b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        s = 'CHG %s' % self.name
        return s


def get_paths(loc):
    return loc.split('|')


class Graph(object):
    def __init__(self):
        self._graph = nx.Graph()
        self._node_id = 0

    def gen_nid(self):
        i = self._node_id
        self._node_id += 1
        return i

    def num_vertices(self):
        return nx.number_of_nodes(self._graph)

    def add_vertex(self, prop=None):
        v = self.gen_nid()
        self._graph.add_node(v)
        if prop:
            self._graph.nodes[v]['prop'] = prop
        return v

    def set_vprop(self, v, s):
        self._graph.nodes[v]['prop'] = s

    def add_edge(self, v0, v1, prop=None):
        if v0 and v1:
            e = (v0, v1)
            self._graph.add_edge(v0, v1)
            if prop:
                self._graph.edges[e]['prop'] = prop
            return e
        else:
            return None

    def set_eprop(self, e, s):
        self._graph.edges[e]['prop'] = s

    def label_components(self):
        tbl = {}
        for i, cs in enumerate(nx.connected_components(self._graph)):
            for c in cs:
                tbl[c] = i
        return tbl

    def save(self, outfile):
        nx.write_gml(self._graph, outfile)


class DependencyCheckFailedException(Exception):
    pass


class Decomposer(object):
    def __init__(self, proj_id, conf=None, lang=None, vers=None,
                 max_stmt_level=MAX_STMT_LEVEL,
                 modified_stmt_rate_thresh=MODIFIED_STMT_RATE_THRESH,
                 method='odbc', pw=VIRTUOSO_PW, port=VIRTUOSO_PORT):

        self._proj_id = proj_id

        if conf is None:
            conf = project.get_conf(proj_id)

        self._selected_vers = None
        if vers is not None:
            self._selected_vers = set()
            for v in vers:
                self._selected_vers.add(conf.versionNS+v)

        if conf.vpairs:
            self._vpairs = [(conf.versionNS+v, conf.versionNS+v_)
                            for (v, v_) in conf.vpairs]

        self._vp_optout_tbl = {}
        if conf.optout_tbl:
            for ((v, v_), l) in conf.optout_tbl.items():
                k = (conf.versionNS+v, conf.versionNS+v_)
                self._vp_optout_tbl[k] = l

        self._vp_optout_compos_tbl = {}

        if lang:
            self._lang = lang
        else:
            self._lang = conf.lang

        self.make_query_id = make_make_query_id(self._lang)

        self._conf = conf

        self._sparql = sparql.get_driver(method, pw=pw, port=port)

        self._max_stmt_level = max_stmt_level
        self._modified_stmt_rate_thresh = modified_stmt_rate_thresh

        self.init()

    def init(self):

        self._vp_vertex_tbl = {}  # ver * ver -> hunk -> vertex
        self._vp_rev_vertex_tbl = {}  # ver * ver -> vertex -> hunk

        self._graph_tbl = {}  # ver * ver -> graph

        self._vp_compo_tbl = {}  # ver * ver -> component_id -> hunk list

        self._hunk_tbl = {  # kind -> (uri * uri) -> hunk
            K_INS: {},
            K_DEL: {},
            K_REL: {},
            K_MOV: {},
        }

        self._move_tbl = {}  # mov_hunk -> del_hunk * ins_hunk
        self._del_tbl = {}  # del_hunk -> mov_hunk
        self._ins_tbl = {}  # ins_hunk -> mov_hunk

        self._movrel_tbl = {}  # mov_hunk -> rel_hunk set

        self._complete_moves = set()  # inst set

        self._ref_hunks = set()

        self._xml_tbl = {}
        self._modified_path_tbl = {}
        self._rev_modified_path_tbl = {}

        self.__version_cache = {}

        self.__version_pairs_cache = {}
        self._version_pairs_cache = {}

        self._vp_dep_tbl = {}  # ver * ver -> vertex -> vertex set
        self._vp_cid_dep_tbl = {}  # ver * ver -> cid -> cid set

        self._target_fid_tbl = {}

        self.setup_target_fid_tbl()
#
        self._containing_stmt_tbl = {}
        self._mapped_stmt_tbl = {}
        self._removed_stmts = {}
        self._added_stmts = {}

        for lv in range(self._max_stmt_level+1):
            self.setup_mapped_stmt_tbl(lv)
            self.setup_containing_stmt_tbl(lv)
            self.setup_removed_stmts(lv)
            self.setup_added_stmts(lv)
#
        self._containing_meth_tbl = {}
        self._mapped_meth_tbl = {}

        self.setup_mapped_meth_tbl()
        self.setup_containing_meth_tbl()

        self._removed_meths = set()
        self._added_meths = set()

        self.setup_removed_meths()
        self.setup_added_meths()
#
        self._containing_file_tbl = {}
        self._mapped_file_tbl = {}

        self.setup_containing_file_tbl()
        self.setup_mapped_file_tbl()

        self._removed_files = set()
        self._added_files = set()

        self.setup_removed_files()
        self.setup_added_files()
#
        self._vp_group_tbl = {}  # ver * ver -> gid -> cid set
        self._vp_rev_group_tbl = {}  # ver * ver -> cid -> gid

        self._lv_vp_stmt_group_tbl = {}  # lv -> ver * ver -> gid -> cid set
        self._lv_vp_rev_stmt_group_tbl = {}  # lv -> ver * ver -> cid -> gid
        for lv in range(self._max_stmt_level+1):
            self._lv_vp_stmt_group_tbl[lv] = {}
            self._lv_vp_rev_stmt_group_tbl[lv] = {}

        self._vp_meth_group_tbl = {}  # ver * ver -> gid -> cid set
        self._vp_rev_meth_group_tbl = {}  # ver * ver -> cid -> gid

        self._vp_file_group_tbl = {}  # ver * ver -> gid -> cid set
        self._vp_rev_file_group_tbl = {}  # ver * ver -> cid -> gid

        self._vp_id_list_tbl = {}

        self._stmt_tbl = {}  # ver -> ent set
        self._modified_stmt_pair_tbl = {}  # (ver * ver) -> (ent * ent) set
        self._max_stmt_level_tbl = {}  # (ver * ver) -> level

        self.setup_stmt_tbl()
        self.setup_modified_stmt_pair_tbl()
        self.setup_max_stmt_level_tbl()

        self._ref_vphtbl = None

    def get_max_stmt_level(self, v, v_):
        lv = self._max_stmt_level_tbl.get((v, v_), 0)
        return lv

    def clear_group_tbl(self, vp):
        self._vp_group_tbl[vp] = {}
        self._vp_rev_group_tbl[vp] = {}

    def setup_stmt_tbl(self):
        q = STMT_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            stmt = row['stmt']
            ent = SourceCodeEntity(uri=stmt)
            for v in self._get_version(ent):
                set_tbl_add(self._stmt_tbl, v, ent)

    def setup_modified_stmt_pair_tbl(self):
        q = MODIFIED_STMT_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            stmt = row['stmt']
            stmt_ = row['stmt_']
            ent = SourceCodeEntity(uri=stmt)
            ent_ = SourceCodeEntity(uri=stmt_)
            for vp in self._get_version_pairs(ent, ent_):
                set_tbl_add(self._modified_stmt_pair_tbl, vp, (ent, ent_))

    def _get_modified_stmt_rate(self, v, v_):
        ent_pairs = self._modified_stmt_pair_tbl.get((v, v_), [])
        ents = self._stmt_tbl.get(v, [])
        len_ents = len(ents)
        r = 0.0
        if len_ents > 0:
            len_ent_pairs = len(ent_pairs)
            r = float(len_ent_pairs) / float(len_ents)
            logger.info('%s -> %f' % (vp_to_str((v, v_)), r))
        return r

    def setup_max_stmt_level_tbl(self):
        for vp in self._modified_stmt_pair_tbl.keys():
            (v, v_) = vp
            r = self._get_modified_stmt_rate(v, v_)
            if r < self._modified_stmt_rate_thresh:
                self._max_stmt_level_tbl[vp] = 0
            else:
                self._max_stmt_level_tbl[vp] = self._max_stmt_level

    def setup_target_fid_tbl(self):
        q = FILE_LOC_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            ver = row['ver']
            f = row['f']
            loc = row['loc']

            if self.check_loc(loc):
                if all(not loc.startswith(x) for x in self._conf.exclude):
                    fent = SourceCodeEntity(uri=f)
                    set_tbl_add(self._target_fid_tbl, ver, fent.get_file_id())

        for v in self._target_fid_tbl.keys():
            logger.info('{} files selected for {}'
                        .format(len(self._target_fid_tbl[v]), v))

    def setup_containing_file_tbl(self):
        q = CONTAINING_FILE_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            ent = row['ent']
            f = row['f']
            loc = row['loc']
            if self.check_loc(loc):
                self._containing_file_tbl[ent] = f

    def get_containing_file(self, ent):
        return self._containing_file_tbl[ent]

    def check_loc(self, loc):
        ok = False
        if self._conf.include == [] or any(loc.startswith(x)
                                           for x in self._conf.include):
            if all(not loc.startswith(x) for x in self._conf.exclude):
                ok = True
        return ok

    def setup_mapped_file_tbl(self):
        q = MAPPED_FILE_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            f = row['f']
            f_ = row['f_']
            loc = row['loc']
            loc_ = row['loc_']
            if self.check_loc(loc) and self.check_loc(loc_):
                self._mapped_file_tbl[f] = f_
        logger.info('{} mapped files found'
                    .format(len(self._mapped_file_tbl.keys())))

    def get_mapped_file(self, f):
        return self._mapped_file_tbl[f]

    def has_mapped_file(self, f):
        return f in self._mapped_file_tbl

    def setup_removed_files(self):
        q = REMOVED_FILE_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            f = row['f']
            loc = row['loc']
            if self.check_loc(loc):
                self._removed_files.add(f)
        logger.info('%d removed files found' % len(self._removed_files))

    def setup_added_files(self):
        q = ADDED_FILE_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            f_ = row['f_']
            loc_ = row['loc_']
            if self.check_loc(loc_):
                self._added_files.add(f_)
        logger.info('%d added files found' % len(self._added_files))

    def is_removed_file(self, ent):
        return ent in self._removed_files

    def is_added_file(self, ent):
        return ent in self._added_files

    def is_compatible_file_keys(self, k0, k1):
        if k0 is not None and k1 is not None:
            (e0, e0_) = k0
            (e1, e1_) = k1
            b = e0 == e1 or e0 is None or e1 is None
            b_ = e0_ == e1_ or e0_ is None or e1_ is None
            return (b and b_)
        else:
            return False

    def get_file_key(self, hunk):
        fkey = None
        rt = hunk.root

        if self.is_removed_file(rt.ent):
            fkey = (rt.ent, None)
        elif self.is_added_file(rt.ent_):
            fkey = (None, rt.ent_)
        else:
            f = None
            try:
                f = self.get_containing_file(rt.ent)
                if self.is_removed_file(f) and not self.has_mapped_file(f):
                    fkey = (f, None)
            except KeyError:
                pass

            try:
                f_ = self.get_containing_file(rt.ent_)
                if f is None:
                    if self.is_added_file(f_):
                        fkey = (None, f_)
                elif f_ == self.get_mapped_file(f):
                    fkey = (f, f_)
            except KeyError:
                pass

        return fkey

    def setup_containing_meth_tbl(self):
        q = CONTAINING_METH_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            ent = row['ent']
            meth = row['meth']
            loc = row['loc']
            if self.check_loc(loc):
                self._containing_meth_tbl[ent] = meth

    def get_containing_meth(self, ent):
        return self._containing_meth_tbl[ent]

    def setup_mapped_meth_tbl(self):
        q = MAPPED_METH_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            meth = row['meth']
            meth_ = row['meth_']
            loc = row['loc']
            loc_ = row['loc_']
            if self.check_loc(loc) and self.check_loc(loc_):
                self._mapped_meth_tbl[meth] = meth_
        logger.info('%d mapped methods found' % len(self._mapped_meth_tbl.keys()))

    def get_mapped_meth(self, meth):
        return self._mapped_meth_tbl[meth]

    def has_mapped_meth(self, meth):
        return meth in self._mapped_meth_tbl

    def setup_removed_meths(self):
        q = REMOVED_METH_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            meth = row['meth']
            loc = row['loc']
            if self.check_loc(loc):
                self._removed_meths.add(meth)
        logger.info('%d removed methods found' % len(self._removed_meths))

    def setup_added_meths(self):
        q = ADDED_METH_QUERY % {'proj_id': self._proj_id}
        for qvs, row in self._sparql.query(q):
            meth_ = row['meth_']
            loc_ = row['loc_']
            if self.check_loc(loc_):
                self._added_meths.add(meth_)
        logger.info('%d added methods found' % len(self._added_meths))

    def is_removed_meth(self, ent):
        return ent in self._removed_meths

    def is_added_meth(self, ent):
        return ent in self._added_meths

    def get_meth_key(self, hunk):
        mkey = None
        rt = hunk.root

        if self.is_removed_meth(rt.ent):
            mkey = (rt.ent, None)
        elif self.is_added_meth(rt.ent_):
            mkey = (None, rt.ent_)
        else:
            m = None
            try:
                m = self.get_containing_meth(rt.ent)
                if self.is_removed_meth(m) and not self.has_mapped_meth(m):
                    mkey = (m, None)
            except KeyError:
                pass

            try:
                m_ = self.get_containing_meth(rt.ent_)
                if m is None:
                    if self.is_added_meth(m_):
                        mkey = (None, m_)
                elif m_ == self.get_mapped_meth(m):
                    mkey = (m, m_)
            except KeyError:
                pass

        return mkey

    def setup_containing_stmt_tbl(self, lv):
        q = CONTAINING_STMT_QUERY % {'proj_id': self._proj_id, 'lv': lv}
        for qvs, row in self._sparql.query(q):
            ent = row['ent']
            stmt = row['stmt']
            loc = row['loc']
            if self.check_loc(loc):
                try:
                    d = self._containing_stmt_tbl[lv]
                except KeyError:
                    d = {}
                    self._containing_stmt_tbl[lv] = d
                d[ent] = stmt

    def get_containing_stmt(self, lv, ent):
        return self._containing_stmt_tbl[lv][ent]

    def setup_mapped_stmt_tbl(self, lv):
        q = MAPPED_STMT_QUERY % {'proj_id': self._proj_id, 'lv': lv}
        try:
            d = self._mapped_stmt_tbl[lv]
        except KeyError:
            d = {}
            self._mapped_stmt_tbl[lv] = d
        for qvs, row in self._sparql.query(q):
            stmt = row['stmt']
            stmt_ = row['stmt_']
            loc = row['loc']
            loc_ = row['loc_']
            if self.check_loc(loc) and self.check_loc(loc_):
                d[stmt] = stmt_
        logger.info('%d mapped statements found' % len(d.keys()))

    def get_mapped_stmt(self, lv, stmt):
        return self._mapped_stmt_tbl[lv][stmt]

    def has_mapped_stmt(self, lv, stmt):
        return stmt in self._mapped_stmt_tbl[lv]

    def setup_removed_stmts(self, lv):
        q = REMOVED_STMT_QUERY % {'proj_id': self._proj_id, 'lv': lv}
        try:
            s = self._removed_stmts[lv]
        except KeyError:
            s = set()
            self._removed_stmts[lv] = s

        for qvs, row in self._sparql.query(q):
            stmt = row['stmt']
            loc = row['loc']
            if self.check_loc(loc):
                s.add(stmt)
        logger.info('%d removed statements found' % len(s))

    def setup_added_stmts(self, lv):
        q = ADDED_STMT_QUERY % {'proj_id': self._proj_id, 'lv': lv}
        try:
            s = self._added_stmts[lv]
        except KeyError:
            s = set()
            self._added_stmts[lv] = s

        for qvs, row in self._sparql.query(q):
            stmt_ = row['stmt_']
            loc_ = row['loc_']
            if self.check_loc(loc_):
                s.add(stmt_)
        logger.info('%d added statements found' % len(s))

    def is_removed_stmt(self, lv, ent):
        return ent in self._removed_stmts.get(lv, set())

    def is_added_stmt(self, lv, ent):
        return ent in self._added_stmts.get(lv, set())

    def get_stmt_key(self, lv, hunk):
        skey = None
        rt = hunk.root

        if self.is_removed_stmt(lv, rt.ent):
            skey = (rt.ent, None)
        elif self.is_added_stmt(lv, rt.ent_):
            skey = (None, rt.ent_)
        else:
            s = None
            try:
                s = self.get_containing_stmt(lv, rt.ent)
                if self.is_removed_stmt(lv, s) and not self.has_mapped_stmt(lv, s):
                    skey = (s, None)
            except KeyError:
                pass

            try:
                s_ = self.get_containing_stmt(lv, rt.ent_)
                if s is None:
                    if self.is_added_stmt(lv, s_):
                        skey = (None, s_)
                elif s_ == self.get_mapped_stmt(lv, s):
                    skey = (s, s_)
            except KeyError:
                pass

        return skey

    def _get_version(self, ent):
        fent = ent

        if not ent.is_file():
            fent = SourceCodeEntity(file_id=ent.get_file_id())

        try:
            return self.__version_cache[fent]
        except KeyError:
            pass

        q = VER_QUERY % {'fent': fent.get_uri(),
                         'proj_id': self._proj_id,
                         }

        vers = set()

        for qvs, row in self._sparql.query(q):
            vers.add(row['v'])

        if len(vers) == 0:
            logger.warning('cannot get version for "%s"' % ent)
        else:
            self.__version_cache[fent] = vers

        return vers

    def _get_version_pairs(self, ent0, ent1):
        fent0 = ent0
        fent1 = ent1

        if not ent0.is_file():
            fent0 = SourceCodeEntity(file_id=ent0.get_file_id())

        if not ent1.is_file():
            fent1 = SourceCodeEntity(file_id=ent1.get_file_id())

        try:
            return self.__version_pairs_cache[(fent0, fent1)]
        except KeyError:
            pass

        q = VER_PAIR_QUERY % {'fent0': fent0.get_uri(),
                              'fent1': fent1.get_uri(),
                              'proj_id': self._proj_id,
                              }

        pairs = set()

        for qvs, row in self._sparql.query(q):
            pairs.add((row['v'], row['v_']))

        if len(pairs) == 0:
            logger.warning('cannot get version pair'
                           f' for "{ent0}" and "{ent1}"')
        else:
            self.__version_pairs_cache[(fent0, fent1)] = pairs

        return pairs

    def get_version_pairs(self, _h):
        h = self.get_hunk(*_h.root.key)
        try:
            vps = self._version_pairs_cache[h]
        except KeyError:
            vps = self._get_version_pairs(h.root.ent_obj, h.root.ent_obj_)
            self._version_pairs_cache[h] = vps
        return vps

    def classify_hunk_list(self, hunk_list):
        tbl = {}
        for hunk in hunk_list:
            vps = self.get_version_pairs(hunk)
            for vp in vps:
                tbl_add(tbl, vp, hunk)

        return tbl

    def classify_hunk_pair_list(self, hunk_pair_list):
        tbl = {}
        for hunk_pair in hunk_pair_list:
            (h0, h1) = hunk_pair
            vps0 = self.get_version_pairs(h0)
            vps1 = self.get_version_pairs(h1)
            for vp in vps0 & vps1:
                tbl_add(tbl, vp, hunk_pair)

        return tbl

    def classify_hunk_set_list(self, hunk_set_list):
        tbl = {}
        for hunk_set in hunk_set_list:
            vps = set()
            for h in hunk_set:
                vps &= self.get_version_pairs(h)

            for vp in vps:
                tbl_add(tbl, vp, hunk_set)

        return tbl

    def vpmkv(self, vp, _h):
        g = self._graph_tbl[vp]
        h = self.get_hunk(*_h.root.key)

        if not self.check_hunk(vp, h):
            return None

        try:
            vertex_tbl = self._vp_vertex_tbl[vp]
        except KeyError:
            vertex_tbl = {}
            self._vp_vertex_tbl[vp] = vertex_tbl

        try:
            v = vertex_tbl[h]
        except KeyError:
            v = g.add_vertex()
            g.set_vprop(v, str(h))
            vertex_tbl[h] = v
            try:
                rev_vertex_tbl = self._vp_rev_vertex_tbl[vp]
            except KeyError:
                rev_vertex_tbl = {}
                self._vp_rev_vertex_tbl[vp] = rev_vertex_tbl

            rev_vertex_tbl[v] = h

        return v

    def reg_hunk(self, kind, key, hunk):
        tbl = self._hunk_tbl[kind]
        tbl[key] = hunk

    def get_hunk(self, kind, key):
        h = None
        try:
            h = self._hunk_tbl[kind][key]
        except KeyError:
            pass
        return h

    def get_hunks(self, kind):
        hs = set(self._hunk_tbl[kind].values())
        return hs

    def is_selected_vp(self, v_v_):
        v, v_ = v_v_
        b = True
        if self._selected_vers is not None:
            b = v in self._selected_vers or v_ in self._selected_vers
        return b

    def get_selected_vps(self, vps):
        return set(filter(self.is_selected_vp, vps))

    def check_hunk(self, vp, hunk):
        b = True
        if self._target_fid_tbl != {}:
            (v, v_) = vp
            ed = hunk.root
            if ed.loc is not None and ed.loc_ is None:
                fid = ed.ent_obj.get_file_id()
                try:
                    b = fid in self._target_fid_tbl[v]
                except KeyError:
                    logger.warning('"%s" is not in target_fid_tbl' % v)
                    b = False

            elif ed.loc is None and ed.loc_ is not None:
                fid_ = ed.ent_obj_.get_file_id()
                try:
                    b = fid_ in self._target_fid_tbl[v_]
                except KeyError:
                    logger.warning('"%s" is not in target_fid_tbl' % v_)
                    b = False

            elif ed.loc is not None and ed.loc_ is not None:
                fid = ed.ent_obj.get_file_id()
                fid_ = ed.ent_obj_.get_file_id()
                try:
                    b = fid in self._target_fid_tbl[v] and fid_ in self._target_fid_tbl[v_]
                except KeyError:
                    logger.warning('"%s" or "%s" are not in target_fid_tbl' % (v, v_))
                    b = False

        if not b:
            logger.debug('to be filtered: %s' % hunk)
            # logger.warning('to be filtered: %s' % hunk)

        return b

    def id_to_string(self, vp, x):
        s = '???'
        if isgid(x):
            cids = self.get_cids1(vp, x)
            s = '%s(%d)' % (x, len(cids))
        else:
            s = str(x)
        return s

    def get_strong_group_tbl(self, vp, gtbl):
        tmp_group_tbl = {}
        rev_tmp_group_tbl = {}
        compo_ids = set(self.get_compo_ids(vp))

        logger.info('|compo_ids|=%d' % len(compo_ids))

        gid_count = 0

        for (key, cids) in gtbl.items():
            if len(cids) > 1:
                gid = mktmpgid(gid_count)
                gid_count += 1
                tmp_group_tbl[gid] = list(cids)
                logger.info('%s: [%s]' % (gid, cids_to_string(cids)))
                for c in cids:
                    if c in compo_ids:
                        compo_ids.remove(c)
                    set_tbl_add(rev_tmp_group_tbl, c, gid)

        group_group_list = []

        for (gid, cids) in tmp_group_tbl.items():
            ggs = set([gid])
            for c in cids:
                for g in rev_tmp_group_tbl[c]:
                    ggs.add(g)

            if group_group_list:
                disjoint_ggl = list(filter(ggs.isdisjoint, group_group_list))
                connected_ggl = list(filter((lambda x: not ggs.isdisjoint(x)), group_group_list))
                ggs.update(*connected_ggl)
                disjoint_ggl.append(ggs)
                group_group_list = disjoint_ggl
            else:
                group_group_list.append(ggs)

        group_tbl = {}
        rev_group_tbl = {}
        group_ids = set()

        count = 0

        for ggs in group_group_list:
            ggl = list(ggs)
            ggl.sort(key=getnum)
            logger.info('[%s]' % (cids_to_string(ggl)))
            cs = set()
            for g in ggs:
                cs.update(set(tmp_group_tbl[g]))

            gid = mkgid(min(cs))

            group_ids.add(gid)

            for c in cs:
                rev_group_tbl[c] = gid
                count += 1

            group_tbl[gid] = list(cs)

            logger.info('gid=%s (size=%d)' % (gid, len(cs)))

        logger.info('%d components' % (count + len(compo_ids)))

        return (group_tbl, rev_group_tbl, compo_ids, group_ids)

    def get_weak_group_tbl(self, vp, gtbl):
        group_tbl = {}
        rev_group_tbl = {}
        compo_ids = set(self.get_compo_ids(vp))
        group_ids = set()
        count = 0
        for (key, cids) in gtbl.items():
            if len(cids) > 1:
                gid = mkgid(min(cids))
                group_ids.add(gid)
                group_tbl[gid] = list(cids)
                count += len(cids)
                logger.info('%s: [%s]' % (gid, cids_to_string(cids)))
                for c in cids:
                    compo_ids.remove(c)
                    rev_group_tbl[c] = gid

        logger.info('%d components' % (count + len(compo_ids)))

        return (group_tbl, rev_group_tbl, compo_ids, group_ids)

    def has_stmt_group(self, lv, vp):
        b = False
        try:
            if len(self._lv_vp_stmt_group_tbl[lv][vp]) > 0:
                b = True
        except KeyError:
            pass
        logger.info('%s (level=%d)' % (b, lv))
        return b

    def fuse_compos_and_groups_by_change_dep(self, vp,
                                             group_tbl, rev_group_tbl,
                                             compo_ids, group_ids,
                                             restrict=True):

        _cid_dep_tbl = self._vp_cid_dep_tbl[vp]
        if restrict:
            logger.info('restricting dependencies...')
            domain = set(rev_group_tbl.keys()) | set(compo_ids)
            cid_dep_tbl = {}
            for _cids in sorted(_cid_dep_tbl.keys()):
                if set(_cids) <= domain:
                    cids = _cid_dep_tbl[_cids] & domain
                    if cids:
                        logger.debug('  {%s} depends on {%s}' % (cids_to_string(_cids),
                                                                 cids_to_string(cids)))
                        cid_dep_tbl[_cids] = cids
        else:
            cid_dep_tbl = _cid_dep_tbl

        for _cids in sorted(cid_dep_tbl.keys()):
            mems = set()
            cids = cid_dep_tbl[_cids]  # _cids depend on cids
            cs = list(cids)+list(_cids)
            for c in cs:
                if c in compo_ids:
                    mems.add(c)
                else:
                    try:
                        g = rev_group_tbl[c]
                        mems.add(g)
                    except KeyError:
                        pass
                        # logger.warning('%s is dangling?' % c)

            gs = list(filter(isgid, list(mems)))
            if gs:
                gs.sort(key=getnum)
                g0 = gs[0]
                cs0 = mems - set(gs)
                group_tbl[g0] += cs0
                for c in cs0:
                    logger.debug('%s --> %s' % (c, g0))
                    rev_group_tbl[c] = g0
                    if c in compo_ids:
                        compo_ids.remove(c)
                for g1 in gs[1:]:
                    logger.debug('%s --> %s' % (g1, g0))
                    cs1 = group_tbl[g1]
                    del group_tbl[g1]
                    if g1 in group_ids:
                        group_ids.remove(g1)
                    group_tbl[g0] += cs1
                    for c1 in cs1:
                        rev_group_tbl[c1] = g0
            else:
                gid = mkgid(min(cs))
                group_ids.add(gid)
                group_tbl[gid] = cs
                logger.info('%s (by dep): [%s]' % (gid, cids_to_string(cs)))
                for c in cs:
                    if c in compo_ids:
                        compo_ids.remove(c)
                    rev_group_tbl[c] = gid

        id_list = list(compo_ids | group_ids)
        id_list.sort(key=getnum)

        logger.info('{} ids: [{}]'.format(len(id_list),
                                          ','.join([self.id_to_string(vp, x)
                                                    for x in id_list])))

        return id_list

    def decompose(self, use_syn=True, use_ref=True, use_other=True,
                  outfile=None, staged=False, shuffle=0, optout=False):

        qtbl = dict([(n, eval(self.make_query_id(n)))
                     for n in QUERY_TBL.get(self._lang, [])])
        for n in QUERY_LIST:
            qtbl[n] = eval(make_query_id(n))

        if not qtbl:
            logger.warning('unsupported language: %s' % self._lang)
            return

        root_ins_hunks = []
        root_del_hunks = []
        root_mov_hunks = []
        root_chg_hunks = []

        ins_hunks = []
        del_hunks = []

        insrtbl = {}  # mem -> hunk
        delrtbl = {}  # mem -> hunk
        # movrtbl = {} # mem -> hunk

        del_ins_list = []
        ins_mov_list = []
        ins_rel_list = []
        del_mov_list = []
        del_rel_list = []
        del_del_list = []
        # mov__del_or_ins_list = []
        rel_del_set = set()
        rel_ins_set = set()
        rel_rel_set = set()

        sibling_tbl = {}

        # for insertion
        logger.info('finding insertions...')
        _query = qtbl.get('ins', None)
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x_ = row['x_']
                ctx = row['ctx']
                px_ = row.get('px_', None)
                pctx = row.get('pctx', None)
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row.get('cat', None)
                s_ = row.get('s_', None)

                key = (ctx, x_)
                hunk = self.get_hunk(K_INS, key)

                if hunk:
                    if hunk.root.loc != loc or hunk.root.loc_ != loc_:
                        logger.warning('{} != root:{} ({})'
                                       .format(loc_, hunk.root.loc_, cat))
                        return

                if hunk is None:
                    root = Edit(K_INS, ctx, x_, loc, loc_, cat)
                    hunk = Hunk(root)
                    insrtbl[root] = hunk
                    self.reg_hunk(K_INS, key, hunk)

                if s_:
                    set_tbl_add(sibling_tbl, s_, hunk)

                if px_ and pctx and use_syn:
                    hunk._parent = Edit(K_INS, pctx, px_, loc, loc_, cat)

        _query = qtbl.get('ins_c', None)
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x_ = row['x_']
                ctx = row['ctx']
                cx_ = row['cx_']
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row.get('cat', None)

                key = (ctx, x_)
                hunk = self.get_hunk(K_INS, key)

                child = Edit(K_INS, ctx, cx_, loc, loc_, cat)
                hunk.add_member(child)
                insrtbl[child] = hunk
                self.reg_hunk(K_INS, (ctx, cx_), hunk)

        ins_hunks = self.get_hunks(K_INS)

        for hunk in ins_hunks:
            if hunk._parent:
                ph = insrtbl.get(hunk._parent, None)
                if ph:
                    hunk.parent = ph
                    ph.children.add(hunk)

        root_ins_hunks = list(filter(lambda h: h.parent is None, ins_hunks))
        logger.info('%d ins hunks' % len(ins_hunks))
        logger.info('%d root ins hunks' % len(root_ins_hunks))

        # for file insertion
        logger.info('finding file insertions...')
        _query = qtbl.get('ins_file', None)
        file_ins_hunks = set()
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                file_ = row['file_']
                ctx = row['ctx']
                loc_ = row['loc_']

                x_ = row.get('x_', None)
                cx_ = row.get('cx_', None)
                xcat = row.get('xcat', None)
                cxcat = row.get('cxcat', None)

                key = (ctx, file_)
                hunk = self.get_hunk(K_INS, key)

                if hunk is None:
                    root = Edit(K_INS, ctx, file_, None, loc_, "File")
                    hunk = Hunk(root)
                    self.reg_hunk(K_INS, key, hunk)

                    if x_:
                        hunk.add_member(Edit(K_INS, ctx, x_, None, loc_, xcat))
                        self.reg_hunk(K_INS, (ctx, x_), hunk)

                    root_ins_hunks.append(hunk)

                file_ins_hunks.add(hunk)

                if cx_:
                    child = Edit(K_INS, ctx, cx_, None, loc_, cxcat)
                    hunk.add_member(child)
                    self.reg_hunk(K_INS, (ctx, cx_), hunk)

            logger.info('%d file ins hunks' % len(file_ins_hunks))
            # for h in file_ins_hunks:
            #     print('  %s' % h)
            #     for e in h.members:
            #         print('    %s' % e)

        # for deletion
        logger.info('finding deletions...')
        _query = qtbl.get('del', None)
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                ctx_ = row['ctx_']
                px = row.get('px', None)
                pctx_ = row.get('pctx_', None)
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row.get('cat', None)
                s = row.get('s', None)

                key = (x, ctx_)
                hunk = self.get_hunk(K_DEL, key)

                if hunk:
                    if hunk.root.loc != loc or hunk.root.loc_ != loc_:
                        logger.warning('%s != root:%s (%s)' % (loc, hunk.root.loc, cat))
                        return

                if hunk is None:
                    root = Edit(K_DEL, x, ctx_, loc, loc_, cat)
                    hunk = Hunk(root)
                    delrtbl[root] = hunk
                    self.reg_hunk(K_DEL, key, hunk)

                if s:
                    set_tbl_add(sibling_tbl, s, hunk)

                if px and pctx_ and use_syn:
                    hunk._parent = Edit(K_DEL, px, pctx_, loc, loc_, cat)

        _query = qtbl.get('del_c', None)
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                ctx_ = row['ctx_']
                cx = row['cx']
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row.get('cat', None)

                key = (x, ctx_)
                hunk = self.get_hunk(K_DEL, key)

                child = Edit(K_DEL, cx, ctx_, loc, loc_, cat)
                hunk.add_member(child)
                delrtbl[child] = hunk
                self.reg_hunk(K_DEL, (cx, ctx_), hunk)

        del_hunks = self.get_hunks(K_DEL)

        for hunk in del_hunks:
            if hunk._parent:
                ph = delrtbl.get(hunk._parent, None)
                if ph:
                    hunk.parent = ph
                    ph.children.add(hunk)

        root_del_hunks = list(filter(lambda h: h.parent is None, del_hunks))
        logger.info('%d del hunks' % len(del_hunks))
        logger.info('%d root del hunks' % len(root_del_hunks))

        # for file deletion
        logger.info('finding file deletions...')
        _query = qtbl.get('del_file', None)
        file_del_hunks = set()
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                _file = row['file']
                ctx_ = row['ctx_']
                loc = row['loc']

                x = row.get('x', None)
                cx = row.get('cx', None)
                xcat = row.get('xcat', None)
                cxcat = row.get('cxcat', None)

                key = (_file, ctx_)
                hunk = self.get_hunk(K_DEL, key)

                if hunk is None:
                    root = Edit(K_DEL, _file, ctx_, loc, None, "File")
                    hunk = Hunk(root)
                    self.reg_hunk(K_DEL, key, hunk)
                    if x:
                        hunk.add_member(Edit(K_DEL, x, ctx_, loc, None, xcat))
                        self.reg_hunk(K_DEL, (x, ctx_), hunk)

                    root_del_hunks.append(hunk)

                file_del_hunks.add(hunk)

                if cx:
                    child = Edit(K_DEL, cx, ctx_, loc, None, cxcat)
                    hunk.add_member(child)
                    self.reg_hunk(K_DEL, (cx, ctx_), hunk)

            logger.info('%d file del hunks' % len(file_del_hunks))
            # for h in file_del_hunks:
            #     print('  %s' % h)
            #     for e in h.members:
            #         print('    %s' % e)

        # for file move
        logger.info('finding file moves...')
        _query = qtbl.get('mov_file', None)
        file_mov_hunks = set()
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                _file = row['file']
                file_ = row['file_']
                loc = row['loc']
                loc_ = row['loc_']

                key = (_file, file_)
                hunk = self.get_hunk(K_MOV, key)

                if hunk is None:
                    root = Edit(K_MOV, _file, file_, loc, loc_, "File")
                    hunk = Hunk(root)
                    self.reg_hunk(K_MOV, key, hunk)

                    root_mov_hunks.append(hunk)

                file_mov_hunks.add(hunk)

            logger.info('%d file mov hunks' % len(file_mov_hunks))

        # for auxfile modification
        logger.info('finding auxfile modifications...')
        _query = qtbl.get('chg_file', None)
        file_chg_hunks = set()
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                _file = row['file']
                file_ = row['file_']
                loc = row['loc']
                loc_ = row['loc_']

                key = (_file, file_)
                hunk = self.get_hunk(K_REL, key)

                if hunk is None:
                    root = Edit(K_REL, _file, file_, loc, loc_, "Auxfile")
                    hunk = Hunk(root)
                    self.reg_hunk(K_REL, key, hunk)

                    root_chg_hunks.append(hunk)

                file_chg_hunks.add(hunk)

            logger.info('%d file mod hunks' % len(file_chg_hunks))

        # for relabel
        logger.info('finding relabelings...')
        _query = qtbl.get('rel', None)
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                x_ = row['x_']
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row['cat']
                cx = row.get('cx', None)
                cx_ = row.get('cx_', None)
                cat_cx = row.get('cat_cx', None)

                key = (x, x_)
                hunk = self.get_hunk(K_REL, key)

                if hunk is None:
                    root = Edit(K_REL, x, x_, loc, loc_, cat)
                    hunk = Hunk(root)
                    self.reg_hunk(K_REL, key, hunk)

                if cx and cx_ and use_syn:
                    ckey = (cx, cx_)
                    chunk = self.get_hunk(K_REL, ckey)
                    if chunk is None:
                        chunk = Hunk(Edit(K_REL, cx, cx_, loc, loc_, cat_cx))
                        self.reg_hunk(K_REL, ckey, chunk)

                    rel_rel_set.add((hunk, chunk))

            rel_hunks = self.get_hunks(K_REL)
            logger.info('%d rel hunks' % len(rel_hunks))
            logger.info('%d rel-rel couplings' % len(rel_rel_set))

        # for rel-del couplings
        logger.info('finding relabeling-deletion couplings...')
        _query = qtbl.get('rel_del', None)
        if _query and use_syn:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                x_ = row['x_']
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row['cat']

                cx = row['cx']
                ctx_ = row['ctx_']

                key = (x, x_)
                hunk = self.get_hunk(K_REL, key)

                if hunk is None:
                    root = Edit(K_REL, x, x_, loc, loc_, cat)
                    hunk = Hunk(root)
                    self.reg_hunk(K_REL, key, hunk)

                dh = self.get_hunk(K_DEL, (cx, ctx_))
                if dh:
                    rel_del_set.add((hunk, dh))
                else:
                    logger.warning('del_hunk not found')
                    logger.debug('! %s %s' % (cx, ctx_))

            logger.info('%d rel-del couplings' % len(rel_del_set))

        # for rel-ins couplings
        logger.info('finding relabeling-insertion couplings...')
        _query = qtbl.get('rel_ins', None)
        if _query and use_syn:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                x_ = row['x_']
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row['cat']

                cx_ = row.get('cx_', None)
                ctx = row.get('ctx', None)

                key = (x, x_)
                hunk = self.get_hunk(K_REL, key)

                if hunk is None:
                    root = Edit(K_REL, x, x_, loc, loc_, cat)
                    hunk = Hunk(root)
                    self.reg_hunk(K_REL, key, hunk)

                ih = self.get_hunk(K_INS, (ctx, cx_))
                if ih:
                    rel_ins_set.add((hunk, ih))
                else:
                    logger.warning('ins_hunk not found')
                    logger.debug('! %s %s' % (ctx, cx_))

            logger.info('%d rel-ins couplings' % len(rel_ins_set))

        # for move
        logger.info('finding moves...')
        _query = qtbl.get('mov', None)
        if _query:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                x_ = row['x_']
                ctx = row['ctx']
                ctx_ = row['ctx_']
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row['cat']
                cat_ = row['cat_']
                cx = row.get('cx', None)
                cx_ = row.get('cx_', None)
                cat_cx = row.get('cat_cx', None)
                cat_cx_ = row.get('cat_cx_', None)

                key = (x, x_)
                hunk = self.get_hunk(K_MOV, key)

                if hunk is None:
                    root = Edit(K_MOV, x, x_, loc, loc_, cat)
                    hunk = Hunk(root)
                    # movrtbl[root] = hunk
                    self.reg_hunk(K_MOV, key, hunk)

                if hunk not in self._move_tbl:
                    del_key = (x, ctx_)
                    del_hunk = self.get_hunk(K_DEL, del_key)
                    if del_hunk is None:
                        logger.warning('del_hunk not found')

                    ins_key = (ctx, x_)
                    ins_hunk = self.get_hunk(K_INS, ins_key)
                    if ins_hunk is None:
                        logger.warning('ins_hunk not found')

                    if ins_hunk is None or del_hunk is None:
                        if del_hunk is None:
                            logger.warning(f'!!! x={x}')
                            logger.warning(f'!!! ctx_={ctx_}')
                        if ins_hunk is None:
                            logger.warning(f'!!! x_={x_}')
                            logger.warning(f'!!! ctx={ctx}')
                        exit(1)

                    if root.ent != del_hunk.root.ent:
                        # logger.warning('entity mismatch: %s and %s' % (hunk, del_hunk))
                        d = Edit(K_DEL, x, ctx_, loc, loc_, cat)
                        del_hunk = Hunk(d)

                    if root.ent_ != ins_hunk.root.ent_:
                        # logger.warning('entity mismatch: %s and %s' % (hunk, ins_hunk))
                        i = Edit(K_INS, ctx, x_, loc, loc_, cat_)
                        ins_hunk = Hunk(i)

                    self._move_tbl[hunk] = (del_hunk, ins_hunk)
                    logger.debug('hunk:\n{}\ndel_hunk:\n{}\nins_hunk:\n{}'
                                 .format(hunk, del_hunk, ins_hunk))

                if cx and cx_:
                    child = Edit(K_MOV, cx, cx_, loc, loc_, cat_cx)
                    hunk.add_member(child)
                    # movrtbl[child] = hunk
                    self.reg_hunk(K_MOV, (cx, cx_), hunk)

            mov_hunks = self.get_hunks(K_MOV)

            # for hunk in mov_hunks:
            #     if hunk._parent:
            #         ph = movrtbl.get(hunk._parent, None)
            #         if ph:
            #             hunk.parent = ph
            #             ph.children.add(hunk)

            # root_mov_hunks = list(filter(lambda h: h.parent is None, mov_hunks))
            logger.info('%d mov hunks' % len(mov_hunks))
            # logger.info('%d root mov hunks' % len(root_mov_hunks))

        # for movrel
        logger.info('finding movrels...')
        _query = qtbl.get('movrel', None)
        movrels = set()
        if _query:
            movrel_cache = {}
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                x_ = row['x_']
                # ctx = row['ctx']
                # ctx_ = row['ctx_']
                loc = row.get('loc', None)
                loc_ = row.get('loc_', None)
                cat = row['cat']
                cat_ = row['cat_']

                key = (x, x_)

                movrels.add(key)

                mhunk = self.get_hunk(K_MOV, key)
                rhunk = movrel_cache.get(key, None)

                if mhunk is None:
                    root = Edit(K_MOV, x, x_, loc, loc_, cat)
                    mhunk = Hunk(root)
                    self.reg_hunk(K_MOV, key, mhunk)

                if rhunk is None:
                    root = Edit(K_REL, x, x_, loc, loc_, cat)
                    rhunk = Hunk(root)
                    movrel_cache[key] = rhunk

                try:
                    s = self._movrel_tbl[mhunk]
                except KeyError:
                    s = set()
                    self._movrel_tbl[mhunk] = s

                s.add(rhunk)

            logger.info('%d movrels' % len(movrels))

        # for del-ins coupling
        logger.info('finding deletion-insertion couplings...')
        for qn in ['del_ins_u', 'del_ins_l', 'del_ins_ln', 'del_ins_mov']:
            _query = qtbl.get(qn, None)
            if _query and use_syn:
                query = _query % {'proj_id': self._proj_id}
                for qvs, row in self._sparql.query(query):
                    x = row['x']
                    ctx_ = row['ctx_']
                    x_ = row['x_']
                    ctx = row['ctx']
                    cat = row['cat']
                    cat_ = row['cat_']
                    loc = row.get('loc', None)
                    loc_ = row.get('loc_', None)

                    del_hunk = self.get_hunk(K_DEL, (x, ctx_))
                    if del_hunk is None:
                        logger.warning('del_hunk not found')
                        del_hunk = Hunk(Edit(K_DEL, x, ctx_, loc, loc_, cat))
                        logger.warning(f'! {x} {ctx_}')

                    ins_hunk = self.get_hunk(K_INS, (ctx, x_))
                    if ins_hunk is None:
                        logger.warning('ins_hunk not found')
                        ins_hunk = Hunk(Edit(K_INS, ctx, x_, loc, loc_, cat_))
                        logger.warning(f'! {ctx} {x_}' % (ctx, x_))

                    del_ins_list.append((del_hunk, ins_hunk))

                logger.info('{} del-ins couplings ({})'
                            .format(len(del_ins_list), qn))

        #####

        root_del_hunk_vtbl = self.classify_hunk_list(root_del_hunks)
        root_ins_hunk_vtbl = self.classify_hunk_list(root_ins_hunks)
        root_mov_hunk_vtbl = self.classify_hunk_list(root_mov_hunks)
        root_chg_hunk_vtbl = self.classify_hunk_list(root_chg_hunks)
        del_ins_vtbl = self.classify_hunk_pair_list(del_ins_list)
        rel_hunk_vtbl = self.classify_hunk_list(rel_hunks)
        rel_del_vtbl = self.classify_hunk_pair_list(rel_del_set)
        rel_ins_vtbl = self.classify_hunk_pair_list(rel_ins_set)
        rel_rel_vtbl = self.classify_hunk_pair_list(rel_rel_set)
        sibling_vtbl = self.classify_hunk_set_list(sibling_tbl.values())

        vps = set()
        vps |= set(root_del_hunk_vtbl.keys())
        vps |= set(root_ins_hunk_vtbl.keys())
        vps |= set(root_mov_hunk_vtbl.keys())
        vps |= set(root_chg_hunk_vtbl.keys())
        vps |= set(del_ins_vtbl.keys())
        vps |= set(rel_hunk_vtbl.keys())
        vps |= set(rel_del_vtbl.keys())
        vps |= set(rel_ins_vtbl.keys())
        vps |= set(rel_rel_vtbl.keys())
        vps |= set(sibling_vtbl.keys())

        for vp in vps:
            if not self.is_selected_vp(vp):
                continue

            logger.info('%s - %s' % vp)

            g = Graph()
            self._graph_tbl[vp] = g

            def scan_hunk_tree(hunk):
                if hunk:
                    v = self.vpmkv(vp, hunk)
                    for child in hunk.children:
                        cv = self.vpmkv(vp, child)
                        g.add_edge(v, cv)
                        scan_hunk_tree(child)

            for root in root_del_hunk_vtbl.get(vp, []):
                scan_hunk_tree(root)

            for root in root_ins_hunk_vtbl.get(vp, []):
                scan_hunk_tree(root)

            for root in root_mov_hunk_vtbl.get(vp, []):
                scan_hunk_tree(root)

            for root in root_chg_hunk_vtbl.get(vp, []):
                scan_hunk_tree(root)

            for (d, i) in del_ins_vtbl.get(vp, []):
                dv = self.vpmkv(vp, d)
                iv = self.vpmkv(vp, i)
                g.add_edge(dv, iv, prop='del-ins')

            for rh in rel_hunk_vtbl.get(vp, []):
                v = self.vpmkv(vp, rh)

            for (r, d) in rel_del_vtbl.get(vp, []):
                rv = self.vpmkv(vp, r)
                dv = self.vpmkv(vp, d)
                g.add_edge(rv, dv, prop='rel-del')

            for (r, i) in rel_ins_vtbl.get(vp, []):
                rv = self.vpmkv(vp, r)
                iv = self.vpmkv(vp, i)
                g.add_edge(rv, iv, prop='rel-ins')

            for (r0, r1) in rel_rel_vtbl.get(vp, []):
                rv0 = self.vpmkv(vp, r0)
                rv1 = self.vpmkv(vp, r1)
                g.add_edge(rv0, rv1, prop='rel-rel')

            for hs in sibling_vtbl.get(vp, []):
                vs = [self.vpmkv(vp, h) for h in hs]
                for (v0, v1) in zip(vs[0:-1], vs[1:]):
                    g.add_edge(v0, v1, prop='sibling')

            logger.info('%d vertices' % g.num_vertices())

        if use_ref:
            # coupling by refactoring

            vpvtbl = {}  # ver * ver -> Ref -> vertex
            vphtbl = {}  # ver * ver -> Ref -> hunk list

            def vpmkv_ref(vp, ref):
                try:
                    vtbl = vpvtbl[vp]
                except KeyError:
                    vtbl = {}
                    vpvtbl[vp] = vtbl
                try:
                    v = vtbl[ref]
                except KeyError:
                    g = self._graph_tbl[vp]
                    v = g.add_vertex(prop=str(ref))
                    vtbl[ref] = v
                return v

            logger.info('finding couplings by refactorings...')
            print('finding couplings by refactorings...')

            qcount = 0
            for (query_name, kind) in REF_QUERY_TBL.get(self._lang, []):
                _query = eval(self.make_query_id(query_name))
                qcount += 1
                sys.stdout.write('[%d] %s' % (qcount, query_name))
                sys.stdout.flush()
                query = _query % {'proj_id': self._proj_id}
                hit = 0
                for qvs, row in self._sparql.query(query):
                    hit += 1
                    ref = row['ref']
                    sig_ = row['sig_']
                    ent = row['ent']
                    ent_ = row['ent_']

                    eo = SourceCodeEntity(uri=ent)
                    eo_ = SourceCodeEntity(uri=ent_)

                    vps0 = self._get_version_pairs(eo, eo_)

                    selected_vps = self.get_selected_vps(vps0)

                    if len(selected_vps) == 0:
                        continue

                    r = Ref(ref, sig_)

                    hunk = self.get_hunk(kind, (ent, ent_))

                    for vp in selected_vps:
                        try:
                            htbl = vphtbl[vp]
                        except KeyError:
                            htbl = {}
                            vphtbl[vp] = htbl

                        v = vpmkv_ref(vp, r)

                        if hunk:
                            if kind == K_MOV:
                                try:
                                    (dhunk, ihunk) = self._move_tbl[hunk]
                                    tbl_add(htbl, r, dhunk)
                                    tbl_add(htbl, r, ihunk)

                                    g = self._graph_tbl[vp]
                                    g.add_edge(v, self.vpmkv(vp, dhunk),
                                               prop=str(r))
                                    g.add_edge(v, self.vpmkv(vp, ihunk),
                                               prop=str(r))

                                except KeyError:
                                    pass
                            else:
                                tbl_add(htbl, r, hunk)
                                g = self._graph_tbl[vp]
                                g.add_edge(v, self.vpmkv(vp, hunk),
                                           prop=str(r))
                        else:
                            logger.warning('[{}][{}][{}] hunk not found for {} {} {}'
                                           .format(qcount,
                                                   query_name,
                                                   vp_to_str(vp),
                                                   kind,
                                                   get_localname(ent),
                                                   get_localname(ent_)))
                sys.stdout.write(': %d\n' % hit)
                sys.stdout.flush()

            for vp, htbl in vphtbl.items():
                logger.debug('{}: {} refactorings:'.format(vp_to_str(vp), len(htbl)))
                for ref, hs in htbl.items():
                    logger.debug('{} ({})'.format(ref, len(hs)))
                    for h in hs:
                        logger.debug('  {}'.format(h))
                        self._ref_hunks.add(h)

            self._ref_vphtbl = vphtbl

        if use_other:
            # coupling by other changes

            vpvtbl = {}  # ver * ver -> Chg -> vertex
            vphtbl = {}  # ver * ver -> Chg -> hunk list

            def vpmkv_chg(vp, chg):
                try:
                    vtbl = vpvtbl[vp]
                except KeyError:
                    vtbl = {}
                    vpvtbl[vp] = vtbl
                try:
                    v = vtbl[chg]
                except KeyError:
                    g = self._graph_tbl[vp]
                    v = g.add_vertex(prop=str(chg))
                    vtbl[chg] = v
                    try:
                        rev_vertex_tbl = self._vp_rev_vertex_tbl[vp]
                    except KeyError:
                        rev_vertex_tbl = {}
                        self._vp_rev_vertex_tbl[vp] = rev_vertex_tbl
                    rev_vertex_tbl[v] = chg
                return v

            logger.info('finding couplings by other changes...')
            print('finding couplings by other changes...')

            qcount = 0
            for (query_name, key_kind, kind) in OTH_QUERY_TBL.get(self._lang, []):
                _query = eval(self.make_query_id(query_name))
                qcount += 1
                sys.stdout.write('[%d] %s' % (qcount, query_name))
                sys.stdout.flush()
                query = _query % {'proj_id': self._proj_id}
                hit = 0
                for qvs, row in self._sparql.query(query):
                    hit += 1
                    key = row['key']
                    key_ = row['key_']
                    name = row.get('name', '')
                    ent = row['ent']
                    ent_ = row['ent_']

                    ko = SourceCodeEntity(uri=key)
                    ko_ = SourceCodeEntity(uri=key_)

                    eo = SourceCodeEntity(uri=ent)
                    eo_ = SourceCodeEntity(uri=ent_)

                    vps0 = self._get_version_pairs(ko, ko_)
                    vps1 = self._get_version_pairs(eo, eo_)

                    selected_vps = self.get_selected_vps(vps0 & vps1)

                    if len(selected_vps) == 0:
                        continue

                    chg = Chg(key, key_, key_kind, name)

                    hunk = self.get_hunk(kind, (ent, ent_))
                    logger.debug('[{}] hunk:\n{}'.format(qcount, hunk))

                    for vp in selected_vps:
                        try:
                            vtbl = vpvtbl[vp]
                        except KeyError:
                            vtbl = {}
                            vpvtbl[vp] = vtbl
                        try:
                            htbl = vphtbl[vp]
                        except KeyError:
                            htbl = {}
                            vphtbl[vp] = htbl

                        registered = chg in vtbl
                        logger.debug(f'[{qcount}] registered={registered}')

                        v = vpmkv_chg(vp, chg)

                        if not registered:
                            key_hunk = self.get_hunk(key_kind, (key, key_))
                            logger.debug(f'[{qcount}] key_hunk:\n{key_hunk}')

                            if key_hunk:
                                tbl_add(htbl, chg, key_hunk)
                                g = self._graph_tbl[vp]
                                w = self.vpmkv(vp, key_hunk)
                                g.add_edge(v, w, prop=str(chg))
                                # if key_hunk.root.cat == 'File':
                                #     print('key_hunk: (%s:%s) %s' % (v, w, chg.key))

                            else:
                                logger.warning('[{}][{}][{}] key hunk not found for {} {} {}'
                                               .format(qcount,
                                                       query_name,
                                                       vp_to_str(vp),
                                                       key_kind,
                                                       get_localname(key),
                                                       get_localname(key_)))
                        if hunk:
                            tbl_add(htbl, chg, hunk)
                            g = self._graph_tbl[vp]
                            w = self.vpmkv(vp, hunk)
                            g.add_edge(v, w, prop=str(chg))
                            # if hunk.root.cat == 'File':
                            #     print('hunk: (%s:%s) %s' % (v, w, chg.key))
                        else:
                            logger.warning('[{}][{}][{}] hunk not found for {} {} {}'
                                           .format(qcount,
                                                   query_name,
                                                   vp_to_str(vp),
                                                   kind,
                                                   get_localname(ent),
                                                   get_localname(ent_)))
                sys.stdout.write(': %d\n' % hit)
                sys.stdout.flush()
                logger.info('[{}] {}: {}'.format(qcount, query_name, hit))

            for (vp, htbl) in vphtbl.items():
                logger.debug('%s: %d other changes' % (vp_to_str(vp), len(htbl)))
                # for (chg, hs) in htbl.items():
                #     logger.debug('%s (%d)' % (chg, len(hs)))

            # directed coupling by other changes

            logger.info('finding directed couplings by other changes...')
            print('finding directed couplings by other changes...')

            qcount = 0
            for (query_name, dep_kind, kinds) in OTH_DIR_QUERY_TBL.get(self._lang, []):
                _query = eval(self.make_query_id(query_name))
                nkinds = len(kinds)

                if nkinds == 0:
                    continue

                qcount += 1
                sys.stdout.write(f'[{qcount}] {query_name}')
                sys.stdout.flush()
                query = _query % {'proj_id': self._proj_id}
                hit = 0
                for qvs, row in self._sparql.query(query):
                    hit += 1
                    dep = row['dep']
                    dep_ = row['dep_']

                    ents = []
                    ents_ = []

                    if nkinds == 1:
                        ents.append(row['ent'])
                        ents_.append(row['ent_'])
                    else:
                        for i in range(nkinds):
                            ents.append(row['ent%d' % i])
                            ents_.append(row['ent%d_' % i])

                    do = SourceCodeEntity(uri=dep)
                    do_ = SourceCodeEntity(uri=dep_)

                    eos = [SourceCodeEntity(uri=ent) for ent in ents]
                    eos_ = [SourceCodeEntity(uri=ent_) for ent_ in ents_]

                    vps0 = self._get_version_pairs(do, do_)
                    vps1 = self._get_version_pairs(eos[0], eos_[0])

                    selected_vps = self.get_selected_vps(vps0 & vps1)

                    if len(selected_vps) == 0:
                        continue

                    hunks = []
                    for i in range(nkinds):
                        kind = kinds[i]
                        ent = ents[i]
                        ent_ = ents_[i]
                        hunk = self.get_hunk(kind, (ent, ent_))
                        logger.debug('hunk:\n{}'.format(hunk))

                        if hunk is None:
                            logger.warning('[{}][{}] hunk not found for {} {} {}'
                                           .format(qcount,
                                                   query_name,
                                                   kind,
                                                   get_localname(ent),
                                                   get_localname(ent_)))
                        else:
                            hunks.append(hunk)

                    hunks.sort(key=lambda x: x.key)

                    dep_hunk = self.get_hunk(dep_kind, (dep, dep_))
                    logger.debug(f'dep_hunk:\n{dep_hunk}')

                    if dep_hunk is None:
                        logger.warning('[{}][{}] dep hunk not found for {} {} {}'
                                       .format(qcount,
                                               query_name,
                                               dep_kind,
                                               get_localname(dep),
                                               get_localname(dep_)))
                    if not all(hunks) or dep_hunk is None:
                        continue

                    for vp in selected_vps:
                        try:
                            dtbl = self._vp_dep_tbl[vp]
                        except KeyError:
                            dtbl = {}
                            self._vp_dep_tbl[vp] = dtbl

                        vs = [self.vpmkv(vp, hunk) for hunk in hunks]
                        if all(vs):
                            dv = self.vpmkv(vp, dep_hunk)
                            if dv:
                                set_tbl_add(dtbl, tuple(vs), dv)

                sys.stdout.write(f': {hit}\n')
                sys.stdout.flush()
                logger.info(f'[{qcount}] {query_name}: {hit}')

        # # for ins-mov coupling
        # logger.info('finding insertion-move couplings...')
        # _query = qtbl.get('ins_mov', None)
        # if _query and use_syn:
        #     query = _query % {'proj_id': self._proj_id}
        #     for qvs, row in self._sparql.query(query):
        #         x_ = row['x_']
        #         ctx = row['ctx']
        #         cx = row['cx']
        #         cx_ = row['cx_']
        #         loc = row['loc']
        #         loc_ = row['loc_']
        #         cat_ = row.get('cat_', None)
        #         cat_cx_ = row.get('cat_cx_', None)

        #         ins_hunk = self.get_hunk(K_INS, (ctx, x_))
        #         if ins_hunk is None:
        #             logger.warning('null ins_hunk')
        #             ins_hunk = Hunk(Edit(K_INS, ctx, x_, loc, loc_, cat_))

        #         mov_key = (cx, cx_)
        #         mov_hunk = self.get_hunk(K_MOV, mov_key)
        #         if mov_hunk is None:
        #             mov_hunk = Hunk(Edit(K_MOV, cx, cx_, loc, loc_, cat_cx_))
        #             self.reg_hunk(K_MOV, mov_key, mov_hunk)

        #         ins_mov_list.append((ins_hunk, mov_hunk))

        #         if mov_hunk in self._move_tbl:
        #             self._complete_moves.add(mov_hunk)

        #     logger.info('%d ins-mov couplings' % len(ins_mov_list))

        # for ins-rel coupling
        logger.info('finding insertion-relabel couplings...')
        _query = qtbl.get('ins_rel', None)
        if _query and use_syn:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x_ = row['x_']
                ctx = row['ctx']
                cx = row['cx']
                cx_ = row['cx_']
                loc = row['loc']
                loc_ = row['loc_']
                cat_ = row.get('cat_', None)
                cat_cx_ = row.get('cat_cx_', None)

                ins_hunk = self.get_hunk(K_INS, (ctx, x_))
                if ins_hunk is None:
                    logger.warning('null ins_hunk')
                    ins_hunk = Hunk(Edit(K_INS, ctx, x_, loc, loc_, cat_))

                rel_key = (cx, cx_)
                rel_hunk = self.get_hunk(K_REL, rel_key)
                if rel_hunk is None:
                    rel_hunk = Hunk(Edit(K_REL, cx, cx_, loc, loc_, cat_cx_))
                    self.reg_hunk(K_REL, rel_key, rel_hunk)

                ins_rel_list.append((ins_hunk, rel_hunk))

            logger.info('%d ins-rel couplings' % len(ins_rel_list))

        # # for del-mov coupling
        # logger.info('finding deletion-move couplings...')
        # _query = qtbl.get('del_mov', None)
        # if _query and use_syn:
        #     query = _query % {'proj_id': self._proj_id}
        #     for qvs, row in self._sparql.query(query):
        #         x = row['x']
        #         ctx_ = row['ctx_']
        #         cx = row['cx']
        #         cx_ = row['cx_']
        #         loc = row['loc']
        #         loc_ = row['loc_']
        #         cat = row.get('cat', None)
        #         cat_cx = row.get('cat_cx', None)

        #         del_hunk = self.get_hunk(K_DEL, (x, ctx_))
        #         if del_hunk is None:
        #             logger.warning('null del_hunk')
        #             del_hunk = Hunk(Edit(K_DEL, x, ctx_, loc, loc_, cat))

        #         mov_key = (cx, cx_)
        #         mov_hunk = self.get_hunk(K_MOV, mov_key)
        #         if mov_hunk is None:
        #             mov_hunk = Hunk(Edit(K_MOV, cx, cx_, loc, loc_, cat_cx))
        #             self.reg_hunk(K_MOV, mov_key, mov_hunk)

        #         del_mov_list.append((del_hunk, mov_hunk))

        #         if mov_hunk in self._move_tbl:
        #             self._complete_moves.add(mov_hunk)

        #     logger.info('%d del-mov couplings' % len(del_mov_list))

        # for del-rel coupling
        logger.info('finding deletion-relabel couplings...')
        _query = qtbl.get('del_rel', None)
        if _query and use_syn:
            query = _query % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                ctx_ = row['ctx_']
                cx = row['cx']
                cx_ = row['cx_']
                loc = row['loc']
                loc_ = row['loc_']
                cat = row.get('cat', None)
                cat_cx = row.get('cat_cx', None)

                del_hunk = self.get_hunk(K_DEL, (x, ctx_))
                if del_hunk is None:
                    logger.warning('null del_hunk')
                    del_hunk = Hunk(Edit(K_DEL, x, ctx_, loc, loc_, cat))

                rel_key = (cx, cx_)
                rel_hunk = self.get_hunk(K_REL, rel_key)
                if rel_hunk is None:
                    rel_hunk = Hunk(Edit(K_REL, cx, cx_, loc, loc_, cat_cx))
                    self.reg_hunk(K_REL, rel_key, rel_hunk)

                del_rel_list.append((del_hunk, rel_hunk))

            logger.info('%d del-rel couplings' % len(del_rel_list))

        # for mov-rel coupling
        logger.info('finding move-relabel couplings...')
        for mov_rel in ('mov_rel', 'mov_rel_ex', 'mov_rel_ex2'):
            _query = qtbl.get(mov_rel, None)
            if _query and use_syn:
                query = _query % {'proj_id': self._proj_id}
                mov_rel_count = 0
                for qvs, row in self._sparql.query(query):
                    x = row['x']
                    x_ = row['x_']
                    ctx = row['ctx']
                    ctx_ = row['ctx_']
                    loc = row['loc']
                    loc_ = row['loc_']
                    cat = row.get('cat', None)

                    del_hunk = self.get_hunk(K_DEL, (x, ctx_))
                    if del_hunk is None:
                        logger.warning('null del_hunk')
                        del_hunk = Hunk(Edit(K_DEL, x, ctx_, loc, loc_, cat))

                    ins_hunk = self.get_hunk(K_INS, (ctx, x_))
                    if ins_hunk is None:
                        logger.warning('null ins_hunk')
                        ins_hunk = Hunk(Edit(K_INS, ctx, x_, loc, loc_, cat))

                    rel_key = (x, x_)
                    rel_hunk = self.get_hunk(K_REL, rel_key)
                    if rel_hunk is None:
                        rel_hunk = Hunk(Edit(K_REL, x, x_, loc, loc_, cat))
                        self.reg_hunk(K_REL, rel_key, rel_hunk)

                    del_rel_list.append((del_hunk, rel_hunk))
                    ins_rel_list.append((ins_hunk, rel_hunk))

                    mov_rel_count += 1

                logger.info('%d %s couplings' % (mov_rel_count, mov_rel))

        # for del-del coupling
        logger.info('finding deletion-deletion couplings...')
        _query = qtbl.get('del_del', None)
        if _query and use_syn:
            query = _query % {'proj_id': self._proj_id}
            mov_rel_count = 0
            for qvs, row in self._sparql.query(query):
                x = row['x']
                y = row['y']
                ctxx_ = row['ctxx_']
                ctxy_ = row['ctxy_']
                loc = row['loc']
                loc_ = row['loc_']
                catx = row.get('catxx', None)
                caty = row.get('catyy', None)

                del_hunk_x = self.get_hunk(K_DEL, (x, ctxx_))
                if del_hunk_x is None:
                    logger.warning('null del_hunk')
                    del_hunk_x = Hunk(Edit(K_DEL, x, ctxx_, loc, loc_, catx))

                del_hunk_y = self.get_hunk(K_DEL, (y, ctxy_))
                if del_hunk_y is None:
                    logger.warning('null del_hunk')
                    del_hunk_y = Hunk(Edit(K_DEL, y, ctxy_, loc, loc_, caty))

                del_del_list.append((del_hunk_x, del_hunk_y))

            logger.info('%d del-del couplings' % len(del_del_list))

        # # for mov-(del|ins) coupling
        # logger.info('finding move-(deletion|insertion) couplings...')
        # _query = qtbl.get('mov__del_or_ins', None)
        # if _query and use_syn:
        #     query = _query % {'proj_id': self._proj_id}
        #     for qvs, row in self._sparql.query(query):
        #         x = row['x']
        #         x_ = row['x_']
        #         loc = row['loc']
        #         loc_ = row['loc_']
        #         cat = row.get('cat', None)
        #         cat_ = row.get('cat_', None)
        #         cat_cx = row.get('cat_cx', None)
        #         cat_cx_ = row.get('cat_cx_', None)
        #         cx = row.get('cx', None)
        #         cx_ = row.get('cx_', None)
        #         ctx = row.get('ctx', None)
        #         ctx_ = row.get('ctx_', None)

        #         if cx or cx_:
        #             mov_key = (x, x_)
        #             mov_hunk = self.get_hunk(K_MOV, mov_key)
        #             if mov_hunk is None:
        #                 mov_hunk = Hunk(Edit(K_MOV, x, x_, loc, loc_, cat))
        #                 self.reg_hunk(K_MOV, mov_key, mov_hunk)

        #             if cx and ctx_:
        #                 del_hunk = self.get_hunk(K_DEL, (cx, ctx_))
        #                 if del_hunk is None:
        #                     logger.warning('null del_hunk')
        #                     del_hunk = Hunk(Edit(K_DEL, cx, ctx_, loc, loc_, cat_cx))

        #                 mov__del_or_ins_list.append((mov_hunk, del_hunk))

        #             if cx_ and ctx:
        #                 ins_hunk = self.get_hunk(K_INS, (ctx, cx_))
        #                 if ins_hunk is None:
        #                     logger.warning('null ins_hunk')
        #                     ins_hunk = Hunk(Edit(K_INS, ctx, cx_, loc, loc_, cat_cx_))

        #                 mov__del_or_ins_list.append((mov_hunk, ins_hunk))

        #             if mov_hunk in self._move_tbl:
        #                 self._complete_moves.add(mov_hunk)

        #     logger.info('%d mov-(del|ins) couplings' % len(mov__del_or_ins_list))

        ins_mov_vtbl = self.classify_hunk_pair_list(ins_mov_list)
        del_mov_vtbl = self.classify_hunk_pair_list(del_mov_list)
        ins_rel_vtbl = self.classify_hunk_pair_list(ins_rel_list)
        del_rel_vtbl = self.classify_hunk_pair_list(del_rel_list)
        del_del_vtbl = self.classify_hunk_pair_list(del_del_list)
        # mov__del_or_ins_vtbl = self.classify_hunk_pair_list(mov__del_or_ins_list)

        for vp in vps:
            if not self.is_selected_vp(vp):
                continue

            logger.info('%s - %s' % vp)

            g = self._graph_tbl[vp]

            for (i, m) in ins_mov_vtbl.get(vp, []):
                iv = self.vpmkv(vp, i)
                mv = self.vpmkv(vp, m)
                g.add_edge(iv, mv, prop='ins-mov')

            for (d, m) in del_mov_vtbl.get(vp, []):
                dv = self.vpmkv(vp, d)
                mv = self.vpmkv(vp, m)
                g.add_edge(dv, mv, prop='del-mov')

            for (i, r) in ins_rel_vtbl.get(vp, []):
                iv = self.vpmkv(vp, i)
                rv = self.vpmkv(vp, r)
                g.add_edge(iv, rv, prop='ins-rel')

            for (d, r) in del_rel_vtbl.get(vp, []):
                dv = self.vpmkv(vp, d)
                rv = self.vpmkv(vp, r)
                g.add_edge(dv, rv, prop='del-rel')

            for (d0, d1) in del_del_vtbl.get(vp, []):
                dv0 = self.vpmkv(vp, d0)
                dv1 = self.vpmkv(vp, d1)
                g.add_edge(dv0, dv1, prop='del-del')

            # for (m, di) in mov__del_or_ins_vtbl.get(vp, []):
            #     mv = self.vpmkv(vp, m)
            #     div = self.vpmkv(vp, di)
            #     g.add_edge(mv, div, prop='mov-(del|ins)')

            for m in self._complete_moves:

                if vp not in self._get_version_pairs(m.root.ent_obj,
                                                     m.root.ent_obj_):
                    continue

                try:
                    (d, i) = self._move_tbl[m]
                    mv = self.vpmkv(vp, m)
                    dv = self.vpmkv(vp, d)
                    iv = self.vpmkv(vp, i)
                    g.add_edge(mv, dv, prop='movdel')
                    g.add_edge(mv, iv, prop='movins')
                except KeyError:
                    pass

            ###

            compo = g.label_components()

            try:
                compo_tbl = self._vp_compo_tbl[vp]
            except KeyError:
                compo_tbl = {}
                self._vp_compo_tbl[vp] = compo_tbl

            for hunk, vertex in self._vp_vertex_tbl[vp].items():
                compo_id = compo[vertex]
                tbl_add(compo_tbl, compo_id, hunk)

            # normalize compo_tbl
            cid_compo_list = list(compo_tbl.items())
            for (i, c) in cid_compo_list:
                c.sort(key=lambda h: h.sort_key)
            cid_compo_list.sort(key=lambda i_c: i_c[1][0].sort_key)

            if shuffle:
                for i in range(shuffle):
                    random.shuffle(cid_compo_list)

            [_permutation, compos] = zip(*cid_compo_list)
            permutation = dict([(o, i) for (i, o) in enumerate(_permutation)])

            compo_tbl = dict(enumerate(compos))

            vp_str = vp_to_str(vp)

            print('{}: decomposed into {} components'
                  .format(vp_str, len(compos)))
            logger.info('{}: decomposed into {} components'
                        .format(vp_str, len(compos)))

            if optout:
                xl = self._vp_optout_tbl.get(vp, [])
                optout_compos = set()
                for (i, c) in compo_tbl.items():
                    ok = False
                    for h in c:
                        for x in xl:
                            if h.root.xkey == x:
                                optout_compos.add(i)
                                ok = True
                                break
                        if ok:
                            break
                self._vp_optout_compos_tbl[vp] = optout_compos

                print(f'{vp_str}: components opted out: {optout_compos}')

                for i in optout_compos:
                    hs = compo_tbl[i]
                    print('%d (%d):' % (i, len(hs)))
                    for h in hs:
                        print('%s' % h)
                    del compo_tbl[i]

            self._vp_compo_tbl[vp] = compo_tbl

            if optout:
                optout_compos_bak = optout_compos.copy()

            try:
                cid_dep_tbl = self._vp_cid_dep_tbl[vp]
            except KeyError:
                cid_dep_tbl = {}
                self._vp_cid_dep_tbl[vp] = cid_dep_tbl

            cids_pair_list = []

            for vs, dvs in self._vp_dep_tbl.get(vp, {}).items():
                _cids = [permutation[compo[v]] for v in vs]
                _cids_set = set(_cids)
                cids = set([permutation[compo[dv]] for dv in dvs])
                cids -= _cids_set

                dep_add = True

                if optout:
                    if _cids_set & optout_compos:
                        dep_add = False
                    else:
                        if cids & optout_compos:
                            optout_compos |= _cids_set
                            dep_add = False

                if dep_add and cids:
                    cids_pair_list.append((_cids, cids))

            if optout:
                prev_cids_pair_list = []
                changed = True
                while changed:
                    prev_cids_pair_list = cids_pair_list
                    cids_pair_list = []
                    changed = False
                    for (_cids, cids) in prev_cids_pair_list:
                        _cids_set = set(_cids)
                        dep_add = True

                        if _cids_set & optout_compos:
                            dep_add = False
                        else:
                            if cids & optout_compos:
                                optout_compos |= _cids_set
                                dep_add = False
                                changed = True

                        if dep_add and cids:
                            cids_pair_list.append((_cids, cids))

                extra_optout_compos = optout_compos - optout_compos_bak
                if extra_optout_compos:
                    print(f'{vp_str}: further components opted out: {extra_optout_compos}')
                    for i in extra_optout_compos:
                        hs = compo_tbl[i]
                        print('{} ({}):'.format(i, len(hs)))
                        for h in hs:
                            print(f'{h}')
                        del compo_tbl[i]

            for (_cids, cids) in cids_pair_list:
                set_tbl_add(cid_dep_tbl, tuple(_cids), cids)

            for _cids in sorted(cid_dep_tbl.keys()):
                cids = cid_dep_tbl[_cids]
                logger.debug('{%s} depends on {%s}' % (cids_to_string(_cids),
                                                       cids_to_string(cids)))

            lv_wsgtbl = {}  # for statement groups (weak)
            wmgtbl = {}  # for method groups (weak)
            wfgtbl = {}  # for file groups (weak)
            lv_ssgtbl = {}  # for statement groups (strong)
            smgtbl = {}  # for method groups (strong)
            sfgtbl = {}  # for file groups (strong)
            htbl = {}

            for lv in range(self._max_stmt_level+1):
                lv_wsgtbl[lv] = {}
                lv_ssgtbl[lv] = {}

            for cid in sorted(self.get_compo_ids(vp)):
                hs = self.get_compo_hunks(vp, cid)
                len_hs = len(hs)

                if staged:
                    for lv in range(self._max_stmt_level+1):
                        sks = [self.get_stmt_key(lv, h) for h in hs]
                        if sks:
                            skey = sks[0]
                            if skey is not None and all([k == skey for k in sks]):
                                set_tbl_add(lv_wsgtbl[lv], skey, cid)
                            for sk in set(sks):
                                if sk is not None:
                                    set_tbl_add(lv_ssgtbl[lv], sk, cid)

                    mks = [self.get_meth_key(h) for h in hs]
                    if mks:
                        mkey = mks[0]
                        if mkey is not None and all([k == mkey for k in mks]):
                            set_tbl_add(wmgtbl, mkey, cid)
                        for mk in set(mks):
                            if mk is not None:
                                set_tbl_add(smgtbl, mk, cid)

                    fks = [self.get_file_key(h) for h in hs]
                    fkey = fks[0]
                    if fkey is not None and\
                       all([self.is_compatible_file_keys(k, fkey)
                            for k in fks]):

                        set_tbl_add(wfgtbl, fkey, cid)
                    for fk in set(fks):
                        if fk is not None:
                            set_tbl_add(sfgtbl, fk, cid)

                logger.debug(f'{cid} ({len_hs}):')
                for h in hs:
                    logger.debug(h)

                if len_hs > 1:
                    try:
                        cl = htbl[len_hs]
                    except KeyError:
                        cl = []
                        htbl[len_hs] = cl
                    cl.append(cid)

            for n in sorted(htbl.keys()):
                logger.info('%d: %s' % (n, cids_to_string(htbl[n])))

            if staged:
                logger.info('setting up stmt groups...')
                for lv in range(self._max_stmt_level+1):
                    logger.info('stmt level: %d' % lv)
                    # (group_tbl, rev_group_tbl,
                    # compo_ids, group_ids) = self.get_weak_group_tbl(vp, lv_wsgtbl[lv])
                    (group_tbl, rev_group_tbl, compo_ids, group_ids) =\
                        self.get_strong_group_tbl(vp, lv_ssgtbl[lv])

                    self._lv_vp_stmt_group_tbl[lv][vp] = group_tbl
                    self._lv_vp_rev_stmt_group_tbl[lv][vp] = rev_group_tbl

                logger.info('setting up method groups...')
                # (group_tbl, rev_group_tbl,
                #  compo_ids, group_ids) = self.get_weak_group_tbl(vp, wmgtbl)
                (group_tbl, rev_group_tbl, compo_ids, group_ids) =\
                    self.get_strong_group_tbl(vp, smgtbl)

                self._vp_meth_group_tbl[vp] = group_tbl
                self._vp_rev_meth_group_tbl[vp] = rev_group_tbl

                logger.info('setting up file groups...')
                # (group_tbl, rev_group_tbl,
                #  compo_ids, group_ids) = self.get_weak_group_tbl(vp, wfgtbl)
                (group_tbl, rev_group_tbl, compo_ids, group_ids) =\
                    self.get_strong_group_tbl(vp, sfgtbl)

                self._vp_file_group_tbl[vp] = group_tbl
                self._vp_rev_file_group_tbl[vp] = rev_group_tbl

                # setup current group table (grouping by file)
                self._vp_group_tbl[vp] = copy.deepcopy(group_tbl)
                self._vp_rev_group_tbl[vp] = copy.deepcopy(rev_group_tbl)
                group_tbl = self._vp_group_tbl[vp]
                rev_group_tbl = self._vp_rev_group_tbl[vp]

                # fuse compos and groups based on change dep.
                id_list =\
                    self.fuse_compos_and_groups_by_change_dep(vp,
                                                              group_tbl,
                                                              rev_group_tbl,
                                                              compo_ids,
                                                              group_ids,
                                                              restrict=False)
                # id_list = list(compo_ids | group_ids)
                # id_list.sort(key=getnum)

                self._vp_id_list_tbl[vp] = id_list

            else:  # if not staged
                id_list = self.get_compo_ids(vp)
                id_list.sort(key=getnum)
                self._vp_id_list_tbl[vp] = id_list

            if outfile:
                g.save(add_vp_suffix(outfile, vp))

        for (mhunk, (dhunk, ihunk)) in self._move_tbl.items():
            self._del_tbl[dhunk] = mhunk
            self._ins_tbl[ihunk] = mhunk

    def regroup(self, vpgtbl, vprgtbl, vp, _cids, by_dep=False):
        cids = self.get_cids(vp, _cids)

        logger.info('{} cids: [{}]'
                    .format(len(cids), ','.join([str(x) for x in cids])))

        gtbl = vpgtbl[vp]
        group_tbl = {}
        for k in gtbl.keys():
            cs = list(filter((lambda c: c in cids), gtbl[k]))
            group_tbl[k] = cs

        rgtbl = vprgtbl[vp]
        rev_group_tbl = {}
        for k in rgtbl.keys():
            if k in cids:
                rev_group_tbl[k] = rgtbl[k]

        self._vp_group_tbl[vp] = group_tbl
        self._vp_rev_group_tbl[vp] = rev_group_tbl

        compo_ids = set()
        group_ids = set()

        for cid in cids:
            try:
                gid = rev_group_tbl[cid]
                group_ids.add(gid)
            except KeyError:
                compo_ids.add(cid)

        if by_dep:
            id_list = self.fuse_compos_and_groups_by_change_dep(vp,
                                                                group_tbl,
                                                                rev_group_tbl,
                                                                compo_ids,
                                                                group_ids)
        else:
            id_list = list(compo_ids | group_ids)

        id_list.sort(key=getnum)

        self._vp_id_list_tbl[vp] = id_list

        logger.info('{} ids: [{}]'
                    .format(len(id_list),
                            ','.join([self.id_to_string(vp, x)
                                      for x in id_list])))

        return id_list

    def regroup_by_file(self, vp, _cids, by_dep=False):
        return self.regroup(self._vp_file_group_tbl,
                            self._vp_rev_file_group_tbl,
                            vp, _cids, by_dep=by_dep)

    def regroup_by_meth(self, vp, _cids, by_dep=False):
        return self.regroup(self._vp_meth_group_tbl,
                            self._vp_rev_meth_group_tbl,
                            vp, _cids, by_dep=by_dep)

    def regroup_by_stmt(self, lv, vp, _cids, by_dep=False):
        return self.regroup(self._lv_vp_stmt_group_tbl[lv],
                            self._lv_vp_rev_stmt_group_tbl[lv],
                            vp, _cids, by_dep=by_dep)

    def get_id_list_tbl(self):
        return self._vp_id_list_tbl

    def get_optout_compo_ids(self, vp):
        return self._vp_optout_compos_tbl.get(vp, set())

    def get_compo_ids_tbl(self):
        return self._vp_compo_tbl

    def get_ref_tbl(self, vp):
        return self._ref_vphtbl.get(vp, {})

    def show_compo_ids_tbl(self, out=None):
        if out:
            outf = open(out, 'w')
        else:
            outf = sys.stdout

        for (vp, compo_tbl) in self._vp_compo_tbl.items():
            outf.write('*** {}\n'.format(vp_to_str(vp)))
            for cid, hunks in compo_tbl.items():
                outf.write(f'Component-{cid}\n')
                for hunk in hunks:
                    outf.write(f' {hunk}\n')

        if out:
            outf.close()

    def get_compo_ids(self, vp):
        return list(self._vp_compo_tbl[vp].keys())

    def get_compo_hunks(self, vp, cid):
        return self._vp_compo_tbl[vp][cid]

    def get_gid(self, vp, cid):
        return self._vp_rev_group_tbl[vp][cid]

    def get_cids1(self, vp, x):
        cids = None
        if isgid(x):
            cids = self._vp_group_tbl[vp][x]
        else:
            cids = [x]
        return cids

    def get_cids(self, vp, xs):
        cids = []
        for x in xs:
            cids += self.get_cids1(vp, x)
        return cids

    def get_compo_hunks_g(self, vp, x):
        cids = self.get_cids1(vp, x)
        hunks = []
        if cids:
            for cid in cids:
                hunks += self._vp_compo_tbl[vp][cid]
        return hunks

    def group_by_dep_g(self, vp, xs):
        len_xs = len(xs)
        logger.info('components (%d): %s' % (len_xs, sorted(xs, key=getnum)))

        cid_dep_tbl = self._vp_cid_dep_tbl.get(vp, {})
        g = Graph()
        vtbl = {}
        ctbl = {}
        for x in xs:
            v = g.add_vertex()
            vtbl[x] = v
            cs = self.get_cids1(vp, x)
            if cs:
                for c in cs:
                    ctbl[c] = v
        for _cids0, cids0 in cid_dep_tbl.items():
            # if len(_cids0) > 1:
            #     continue
            for _cid0 in _cids0:
                _v0 = ctbl.get(_cid0, None)
                if _v0:
                    for cid0 in cids0:
                        v0 = ctbl.get(cid0, None)
                        if v0:
                            g.add_edge(_v0, v0)
        compo = g.label_components()
        dgtbl = {}
        for x, v in vtbl.items():
            dgid = compo[v]
            set_tbl_add(dgtbl, dgid, x)
        yll = []
        for _, ys in dgtbl.items():
            yll.append(sorted(list(ys), key=getnum))

        return yll

    def add_dependency_g(self, vp, xs):
        len_xs = len(xs)
        logger.info('components ({}): {}'
                    .format(len_xs, sorted(xs, key=getnum)))
        compo_ids = self.get_cids(vp, xs)
        r = self.add_dependency(vp, compo_ids)
        if r is None:
            return None

        ys = None
        count = 0

        while r is not None:
            count += 1
            ys = set()
            for c in r:
                try:
                    gid = self.get_gid(vp, c)
                    ys.add(gid)
                except KeyError:
                    ys.add(c)
            logger.info('[{}] components ({}): {}'
                        .format(count,
                                len(ys),
                                sorted(list(ys), key=getnum)))
            compo_ids = self.get_cids(vp, ys)
            r = self.add_dependency(vp, compo_ids)

        yl = list(ys)
        yl.sort(key=getnum)
        len_yl = len(yl)
        d = len_yl - len_xs
        logger.info(f'augmented components ({len_yl}:+{d}): {yl}')
        if d == 0:
            return None
        return yl

    def add_dependency(self, vp, compo_ids):
        orig_compo_ids = set(compo_ids)
        cid_dep_tbl = self._vp_cid_dep_tbl.get(vp, {})

        def incr(_cids):
            cs = set(_cids)
            for _cids0, cids0 in cid_dep_tbl.items():
                if set(_cids0) <= _cids:
                    # print('incr: {%s} depends on {%s}' % (cids_to_string(_cids0),
                    #                                       cids_to_string(cids0)))
                    cs |= cids0

            # print('incr: %d -> %d' % (len(_cids), len(cs)))

            return cs

        cur_compo_ids = set(compo_ids)
        cids = set()
        while True:
            cids = incr(cur_compo_ids)
            if len(cids) == len(cur_compo_ids):
                break
            else:
                cur_compo_ids = cids

        compo_diff = sorted(list(cids - orig_compo_ids))
        ndiff = len(compo_diff)
        if ndiff > 0:
            result = sorted(list(cids))
            logger.info('augmented components ({}:+{}): {}'
                        .format(len(result), ndiff, result))
            return result
        else:
            logger.info('components ({}): {}'
                        .format(len(compo_ids), compo_ids))
            return None

    def _remove_dependency_g(self, vp, xs):
        # len_xs = len(xs)
        compo_ids = self.get_cids(vp, xs)
        cids = self._remove_dependency(vp, compo_ids)
        ys = set()
        for c in cids:
            try:
                gid = self.get_gid(vp, c)
                ys.add(gid)
            except KeyError:
                ys.add(c)
        return ys

    def _remove_dependency(self, vp, compo_ids):
        cid_dep_tbl = self._vp_cid_dep_tbl.get(vp, {})

        def decr(_cids):
            orig_len = len(_cids)
            cs = set(_cids)
            to_be_removed = set()
            for _cids0, cids0 in cid_dep_tbl.items():
                _cids0_set = set(_cids0)
                if _cids0_set <= cs:
                    # print('decr: {%s} depends on {%s}' % (cids_to_string(_cids0),
                    #                                       cids_to_string(cids0)))
                    if len(cids0 - cs) > 0:
                        to_be_removed |= _cids0_set
                        n = len(to_be_removed)
                        # print('decr: |to_be_removed|=%d' % len(to_be_removed))
                        if orig_len <= n:
                            break

            result = cs - to_be_removed
            # print('decr: %d -> %d' % (len(cs), len(result)))
            return result

        cur_compo_ids = set(compo_ids)
        cids = set()
        while True:
            cids = decr(cur_compo_ids)
            if len(cids) == len(cur_compo_ids):
                break
            else:
                cur_compo_ids = cids

        return cids

    def remove_dependency_g(self, vp, xs):
        len_xs = len(xs)
        logger.info('components ({}): {}'
                    .format(len_xs, sorted(xs, key=getnum)))
        compo_ids = self.get_cids(vp, xs)
        r = self.remove_dependency(vp, compo_ids)
        if r is None:
            return None

        ys = set(xs)
        count = 0

        while r is not None:
            count += 1
            dec = set(compo_ids) - set(r)
            ds = set()
            for c in dec:
                try:
                    gid = self.get_gid(vp, c)
                    ds.add(gid)
                except KeyError:
                    ds.add(c)
            ys.difference_update(ds)
            logger.info('[{}] components ({}): {}'
                        .format(count,
                                len(ys),
                                sorted(list(ys), key=getnum)))

            compo_ids = self.get_cids(vp, ys)
            r = self.remove_dependency(vp, compo_ids)

        yl = list(ys)
        yl.sort(key=getnum)
        len_yl = len(yl)
        d = len_xs - len_yl

        logger.info(f'diminished components ({len_yl}:-{d}): {yl}')

        if d == 0:
            return None

        return yl

    def remove_dependency(self, vp, compo_ids):
        _result = self._remove_dependency(vp, compo_ids)

        if 0 < len(_result) < len(compo_ids):
            result = list(_result)
            result.sort()
            ndiff = len(compo_ids) - len(result)
            logger.info('diminished components ({}:-{}): {}'
                        .format(len(result), ndiff, result))
            return result
        else:
            logger.info('components ({}): {}'
                        .format(len(compo_ids), compo_ids))
            return None

    def dump_delta(self, vp, xs, outfile='a.xddb', ignore_ref=False,
                   no_check=False):
        compo_ids = self.get_cids(vp, xs)
        self._dump_delta(vp, compo_ids, outfile=outfile, ignore_ref=ignore_ref,
                         no_check=no_check)

    def _dump_delta(self, vp, compo_ids, outfile='a.xddb', ignore_ref=False,
                    no_check=False):

        if self._xml_tbl == {}:
            logger.info('creating xml table...')
            query = Q_DELTA_XML % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                x = row['x']
                xml = row['xml']
                set_tbl_add(self._xml_tbl, x, xml)

            logger.info('%d delta keys found' % len(self._xml_tbl))

        if self._modified_path_tbl == {} or self._rev_modified_path_tbl == {}:
            self._modified_path_tbl = {}
            self._rev_modified_path_tbl = {}

            query = Q_MODIFIED_PATH % {'proj_id': self._proj_id}
            for qvs, row in self._sparql.query(query):
                path = row['path']
                path_ = row['path_']
                self._modified_path_tbl[path] = path_
                self._rev_modified_path_tbl[path_] = path

            logger.info('{} modified paths found'
                        .format(len(self._modified_path_tbl)))

        ###

        logger.info('creating hunk table...')

        hunk_tbl = {}  # loc -> hunk list
        ignored_hunks = []

        r = self._remove_dependency(vp, compo_ids)

        compo_diff = sorted(list(set(compo_ids) - r))
        if not no_check and len(compo_diff) > 0:
            raise DependencyCheckFailedException(compo_diff)

        total_compo_ids = sorted(compo_ids)
        # logger.info('total components (%d): %s' % (len(total_compo_ids),
        #                                             total_compo_ids))

        for compo_id in total_compo_ids:
            hs = self.get_compo_hunks(vp, compo_id)
            for h in hs:
                if ignore_ref and h in self._ref_hunks:
                    ignored_hunks.append(h)
                    continue

                if h.get_kind() in KINDS and 'File' in h.root.cats:
                    tbl_add(hunk_tbl, '', h)

                elif h.get_kind() in KINDS and 'Auxfile' in h.root.cats:
                    tbl_add(hunk_tbl, '', h)

                else:
                    loc = h.get_loc()
                    loc_ = h.get_loc_()

                    loc0 = ''
                    loc1 = ''

                    if loc_:

                        # if loc_.find('RowAction.java') >= 0:
                        #     print('%d %s:' % (compo_id, h))
                        #     for x in self._xml_tbl.get(h.get_chginst(), []):
                        #         print('    %s' % x)

                        paths_ = get_paths(loc_)
                        paths = filter(lambda x: x is not None,
                                       [self._rev_modified_path_tbl.get(p_, None)
                                        for p_ in paths_])

                        loc0 = '|'.join(paths)

                    if loc:
                        paths = filter(lambda p: p in self._modified_path_tbl,
                                       get_paths(loc))
                        loc1 = '|'.join(paths)

                    if loc_:
                        tbl_add(hunk_tbl, loc0, h)
                    elif loc:
                        tbl_add(hunk_tbl, loc1, h)

        if ignored_hunks:
            logger.info('{} hunks ignored'.format(len(ignored_hunks)))

        inst_tbl = {}  # loc -> inst set

        movrel_inst_tbl = {}  # inst -> inst list

        del_insts = set()
        ins_insts = set()

        logger.info('creating change instance table...')

        for loc, hunks in hunk_tbl.items():
            for hunk in hunks:
                k = hunk.get_kind()

                dflag = False
                iflag = False

                if k == K_DEL:
                    try:
                        h = self._del_tbl[hunk]
                        dflag = True
                    except KeyError:
                        h = hunk

                elif k == K_INS:
                    try:
                        h = self._ins_tbl[hunk]
                        iflag = True
                    except KeyError:
                        h = hunk
                else:
                    h = hunk

                logger.debug(f'h={h}')

                # if h.root.kind == K_MOV:
                #     flag = False
                #     if h.root.loc:
                #         if h.root.loc.find('RowAction.java') >= 0:
                #             flag = True
                #     elif h.root.loc_:
                #         if h.root.loc_.find('RowAction.java') >= 0:
                #             flag = True
                #     if flag:
                #         print('!!! D:%s I:%s %s' % (dflag, iflag, h))

                inst = h.get_chginst()

                logger.debug('inst={}'.format(inst))

                movrel_hunks = self._movrel_tbl.get(h, None)
                if movrel_hunks:
                    movrel_insts = [mrh.get_chginst() for mrh in movrel_hunks]
                    movrel_inst_tbl[inst] = movrel_insts

                if dflag:
                    del_insts.add(inst)
                if iflag:
                    ins_insts.add(inst)

                set_tbl_add(inst_tbl, loc, inst)

        logger.info(f'dumping into "{outfile}"...')

        with open(outfile, 'w') as f:

            f.write(XML_HEAD)

            f.write(DELTA_BUNDLE_HEAD)

            count = 0
            keys = set(self._xml_tbl.keys())

            complete_move_insts = set([h.get_chginst()
                                       for h in self._complete_moves])

            for loc, insts in inst_tbl.items():
                if loc:
                    f.write(DELTA_HEAD % {'lang': self._lang, 'loc': loc})
                else:
                    f.write(DIR_DELTA_HEAD % {'lang': self._lang})

                for inst in insts:

                    xmls = self._xml_tbl.get(inst, None)

                    if not xmls:
                        logger.warning(f'xml not found: {inst}')
                        continue

                    keys.discard(inst)

                    mctl = []

                    needs_movrel = False

                    if inst not in complete_move_insts:
                        dflag = inst in del_insts
                        iflag = inst in ins_insts
                        logger.debug(f'inst={inst}')
                        logger.debug(f'dflag={dflag} iflag={iflag}')

                        if dflag and not iflag:
                            mctl = [('xdd:mctl', 'D')]
                        elif iflag and not dflag:
                            mctl = [('xdd:mctl', 'I')]
                            needs_movrel = True
                        elif dflag and iflag:
                            needs_movrel = True

                    for xml in xmls:
                        logger.debug(f'xml={xml}')
                        count += 1

                        if mctl:
                            xml = insert_attrs(xml, mctl)

                        f.write(xml)

                    if needs_movrel:
                        movrel_insts = movrel_inst_tbl.get(inst, None)
                        if movrel_insts:
                            for movrel_inst in movrel_insts:
                                mr_xmls = self._xml_tbl.get(movrel_inst, None)
                                if not mr_xmls:
                                    logger.warning(f'xml not found: {movrel_inst}')
                                    continue
                                keys.discard(movrel_inst)
                                for mr_xml in mr_xmls:
                                    count += 1
                                    if mctl:
                                        mr_xml = insert_attrs(mr_xml, mctl)
                                    f.write(mr_xml)

                f.write(DELTA_TAIL)

            f.write(DELTA_BUNDLE_TAIL)

        logger.info('%d delta fragments dumped' % count)

        logger.info('%d keys missed' % len(keys))


def main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(description='decompose delta',
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('proj_id', type=str, help='project id')

    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help='enable debug printing')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='enable verbose printing')

    parser.add_argument('--nosyn', dest='nosyn', default=False,
                        action='store_true',
                        help='disable change coupling based on syntactic structure')

    parser.add_argument('--noref', dest='noref', default=False,
                        action='store_true',
                        help='disable change coupling based on refactoring')

    parser.add_argument('--nochg', dest='nochg', default=False,
                        action='store_true',
                        help='disable change coupling based on change dependency')

    parser.add_argument('--ignoreref', dest='ignoreref', default=False,
                        action='store_true',
                        help='remove refactoring changes from delta')

    parser.add_argument('-g', '--graph-outfile', dest='graph_outfile',
                        default=None,
                        metavar='FILE', type=str, help='dump graph into FILE')

    parser.add_argument('-o', '--outfile', dest='outfile', default=None,
                        metavar='FILE', type=str,
                        help='dump delta bundle into FILE')

    parser.add_argument('-l', '--lang', dest='lang', default='java',
                        metavar='LANG', type=str, help='target language')

    parser.add_argument('--ver', dest='vers', action='append', default=None,
                        metavar='VER', type=str, help='specify versions')

    args = parser.parse_args()

    log_level = logging.WARNING
    if args.verbose:
        log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    setup_logger(logger, log_level)

    decomp = Decomposer(args.proj_id, lang=args.lang, vers=args.vers)

    decomp.decompose(use_syn=(not args.nosyn),
                     use_ref=(not args.noref),
                     use_other=(not args.nochg),
                     outfile=args.graph_outfile)

    compo_ids_tbl = decomp.get_compo_ids_tbl()

    if args.outfile:
        for (vp, compo_tbl) in compo_ids_tbl.items():
            outfile = add_vp_suffix(args.outfile, vp)
            decomp.dump_delta(vp, compo_tbl.keys(), outfile=outfile,
                              ignore_ref=args.ignoreref)

    decomp.show_compo_ids_tbl()


if __name__ == '__main__':
    main()
