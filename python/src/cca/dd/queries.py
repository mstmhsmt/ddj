#!/usr/bin/env python3

'''
  queries.py

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

from cca.ccautil.ns import NS_TBL

Q_DELTA_XML = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?xml
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {
  ?x delta:xml ?xml .
}
}
''' % NS_TBL

Q_MODIFIED_PATH = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
SELECT DISTINCT ?path ?path_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {
  ?loc a src:Location ;
       src:path ?path ;
       chg:modified ?loc_ .

  ?loc_ a src:Location ;
        src:path ?path_ .
}
}
''' % NS_TBL

VER_QUERY = '''
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
SELECT DISTINCT ?v
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {
  <%%(fent)s> ver:version ?v .
}
''' % NS_TBL

VER_PAIR_QUERY = '''
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
SELECT DISTINCT ?v ?v_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {
  <%%(fent0)s> ver:version ?v .
  <%%(fent1)s> ver:version ?v_ .
  ?v ver:next ?v_ .
}
''' % NS_TBL

FILE_LOC_QUERY = '''
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX gsrc: <%(gsrc_ns)s>
SELECT DISTINCT ?ver ?f ?loc
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {
  ?f a src:File ;
     src:location ?loc .

  [] ver:version ?ver ;
     gsrc:location ?f ;
     gsrc:location ?loc .

}
''' % NS_TBL

CONTAINING_FILE_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?ent ?f ?loc
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?ent a java:Entity ;
       src:parent*/src:inFile ?f .

  ?f src:location ?loc .

  FILTER (EXISTS {
    ?f0 chg:mappedTo ?f .
  } || EXISTS {
    ?f chg:mappedTo ?f0 .
  })

}
''' % NS_TBL

MAPPED_FILE_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?f ?f_ ?loc ?loc_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?f a src:File ;
     src:location ?loc ;
     chg:mappedTo ?f_ .

  ?f_ a src:File ;
      src:location ?loc_ .

}
''' % NS_TBL

REMOVED_FILE_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?f ?ctx_ ?loc
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?f a src:File ;
     src:location ?loc ;
     chg:genRemoved ?ctx_ .

}
''' % NS_TBL

ADDED_FILE_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?ctx ?f_ ?loc_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?f_ a src:File ;
      src:location ?loc_ ;
      chg:genAdded ?ctx .

}
''' % NS_TBL

STMT_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?stmt
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {
  ?stmt a java:Statement .
}
''' % NS_TBL

MODIFIED_STMT_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?stmt ?stmt_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {
  ?stmt a java:Statement ;
        chg:modified ?stmt_ .
}
''' % NS_TBL

CONTAINING_STMT_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?ent ?stmt ?loc
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?ent a java:Entity ;
       src:parent+ ?stmt .

  ?stmt a java:Statement ;
        java:inTypeDeclaration/src:inFile/src:location ?loc ;
        java:stmtLevel %%(lv)d .

}
''' % NS_TBL

MAPPED_STMT_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?stmt ?stmt_ ?loc ?loc_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?stmt a java:Statement ;
        java:stmtLevel %%(lv)d ;
        java:inTypeDeclaration/src:inFile/src:location ?loc ;
        chg:mappedTo ?stmt_ .

  ?stmt_ a java:Statement ;
         java:stmtLevel %%(lv)d ;
         java:inTypeDeclaration/src:inFile/src:location ?loc_ .

}
''' % NS_TBL

REMOVED_STMT_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?stmt ?ctx_ ?loc
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?stmt a java:Statement ;
        java:stmtLevel %%(lv)d ;
        java:inTypeDeclaration/src:inFile/src:location ?loc ;
        chg:genRemoved ?ctx_ .

}
''' % NS_TBL

ADDED_STMT_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?ctx ?stmt_ ?loc_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?stmt_ a java:Statement ;
         java:stmtLevel %%(lv)d ;
         java:inTypeDeclaration/src:inFile/src:location ?loc_ ;
         chg:genAdded ?ctx .

}
''' % NS_TBL

CONTAINING_METH_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?ent ?meth ?loc
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?ent a java:Entity ;
       java:inMethodOrConstructor ?meth .

  ?meth java:inTypeDeclaration/src:inFile/src:location ?loc .

  FILTER (EXISTS {
    ?meth0 chg:mappedTo ?meth .
  } || EXISTS {
    ?meth chg:mappedTo ?meth0 .
  })

}
''' % NS_TBL

MAPPED_METH_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?meth ?meth_ ?name ?name_ ?loc ?loc_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration/src:inFile/src:location ?loc ;
        java:name ?name ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration/src:inFile/src:location ?loc_ ;
         java:name ?name_ .

}
''' % NS_TBL

REMOVED_METH_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?meth ?ctx_ ?name ?loc
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration/src:inFile/src:location ?loc ;
        java:name ?name ;
        chg:genRemoved ?ctx_ .

}
''' % NS_TBL

ADDED_METH_QUERY = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?ctx ?meth_ ?name_ ?loc_
FROM <%(fb_ns)s%%(proj_id)s>
WHERE {

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration/src:inFile/src:location ?loc_ ;
         java:name ?name_ ;
         chg:genAdded ?ctx .

}
''' % NS_TBL

Q_DEL_INS_U_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?x ?ctx_ ?x_ ?ctx ?loc ?loc_ ?cat ?cat_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x chg:removal ?ctx_ ;
     src:parent ?ctx .

  ?x_ chg:addition ?ctx ;
      src:parent ?ctx_ .

  FILTER NOT EXISTS {#!!!!!NG
    ?ctx a src:ListNode .
  }
  FILTER NOT EXISTS {
    ?ctx_ a src:ListNode .
  }

  OPTIONAL {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

  {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c_), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c_ OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  OPTIONAL {
    ?y src:parent+ ?x .
    ?y chg:mappedStablyTo [] .
    ?ctx a ?ctx_cat OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?ctx_cat rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
      ?p_child rdfs:subPropertyOf src:child .
    }
    ?y a ?child_class .
  }

  OPTIONAL {
    ?y_ src:parent+ ?x_ .
    [] chg:mappedStablyTo ?y_ .
    ?ctx_ a ?ctx_cat_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?ctx_cat_ rdfs:subClassOf* ?ln_ .
       ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
      ?p_child_ rdfs:subPropertyOf src:child .
    }
    ?y_ a ?child_class_ .
  }

  FILTER (!BOUND(?y) || !BOUND(?y_))

  OPTIONAL {
    ?x chg:movedTo ?x0_ .
    FILTER (?x0_ != ?x_)
  }
  FILTER (!BOUND(?x0_) || NOT EXISTS {
    ?x0_ src:parent+ ?x_ .
    ?cx_ src:parent+ ?x0_ .
    ?cx src:parent+ ?x ;
        chg:mappedStablyTo ?cx_ .
  })

  OPTIONAL {
    ?x0 chg:movedTo ?x_ .
    FILTER (?x0 != ?x)
  }
  FILTER (!BOUND(?x0) || NOT EXISTS {
    ?x0 src:parent+ ?x .
    ?cx_ src:parent+ ?x_ .
    ?cx src:parent+ ?x0 ;
        chg:mappedStablyTo ?cx_ .
  })

}
}
''' % NS_TBL

Q_DEL_INS_L_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?ctx_ ?x_ ?ctx ?loc ?loc_ ?cat ?cat_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?ctx ?ctx_ ?catx ?catx_ ?nc
    WHERE {

      ?x a ?catx OPTION (INFERENCE NONE) ;
         src:parent+ ?ctx ;
         chg:removal ?ctx_ .

      ?x_ a ?catx_ OPTION (INFERENCE NONE) ;
          src:parent+ ?ctx_ ;
          chg:addition ?ctx .

      FILTER ((EXISTS {
        [] a chg:Deletion ;
           delta:entity1 ?x ;
           delta:entity2 ?ctx_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x .
      }) && (EXISTS {
        [] a chg:Insertion ;
           delta:entity1 ?ctx ;
           delta:entity2 ?x_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity2 ?x_ .
      }))

      {
        SELECT DISTINCT ?x ?x_ (COUNT(DISTINCT ?cx0) AS ?nc)
        WHERE {
          ?cx0 src:parent+ ?x ;
               chg:mappedStablyTo ?cx0_ .

          ?cx0_ src:parent+ ?x_ .

        } GROUP BY ?x ?x_
      }

    } GROUP BY ?x ?x_ ?ctx ?ctx_ ?catx ?catx_ ?nc
  }

  FILTER (?nc > 0)

  ?bx src:parent* ?x ;
      chg:removal ?ctx_ .

  ?bx_ src:parent* ?x_ ;
       chg:addition ?ctx .

  ?cx src:parent ?bx ;
      chg:mappedStablyTo ?cx_ .

  ?cx_ src:parent ?bx_ .

  FILTER (((?bx != ?x && NOT EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?bx ;
       delta:entity2 ?ctx_ .
  } && NOT EXISTS {
    [] a chg:Move ;
       delta:entity1 ?bx .
  } && NOT EXISTS {
    ?x a [] .
    ?bx src:parent+ ?bx0 .
    ?bx0 src:parent+ ?x ;
         chg:removal ?ctx_ .
    FILTER (EXISTS {
      [] a chg:Deletion ;
         delta:entity1 ?bx0 ;
         delta:entity2 ?ctx_ .
    } || EXISTS {
      [] a chg:Move ;
         delta:entity1 ?bx0 .
    })
  }) || ?bx = ?x )
  ||
  ((?bx_ != ?x_ && NOT EXISTS {
    [] a chg:Insertion ;
       delta:entity1 ?ctx ;
       delta:entity2 ?bx_ .
  } && NOT EXISTS {
    [] a chg:Move ;
       delta:entity2 ?bx_ .
  } && NOT EXISTS {
    ?x_ a [] .
    ?bx_ src:parent+ ?bx0_ .
    ?bx0_ src:parent+ ?x_ ;
          chg:addition ?ctx .
    FILTER (EXISTS {
      [] a chg:Insertion ;
         delta:entity1 ?ctx ;
         delta:entity2 ?bx0_ .
    } || EXISTS {
      [] a chg:Move ;
         delta:entity2 ?bx0_ .
    })
  }) || ?bx_ = ?x_ ))

  OPTIONAL {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

  {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?cat0), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?cat0 OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?cat0_), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?cat0_ OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

}
}
''' % NS_TBL

Q_DEL_INS_LN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?x ?ctx_ ?x_ ?ctx ?loc ?loc_ ?cat ?cat_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a ?cat0 OPTION (INFERENCE NONE) ;
     src:parent ?ctx ;
     chg:removal ?ctx_ .

  ?x_ a ?cat0_ OPTION (INFERENCE NONE) ;
      src:parent ?ctx_ ;
      chg:addition ?ctx .

  ?cx a ?cx_cat OPTION (INFERENCE NONE) ;
      src:parent ?x ;
      chg:mappedStablyTo ?cx_ .

  ?cx_ a ?cx_cat_ OPTION (INFERENCE NONE) ;
       src:parent ?x_ .

  ?ctx a src:ListNode ;
       a ?ctx_cat OPTION (INFERENCE NONE) .

  ?ctx_ a src:ListNode ;
        a ?ctx_cat_ OPTION (INFERENCE NONE) .

  GRAPH <http://codinuum.com/ont/cpi> {
    FILTER NOT EXISTS {
      ?ctx_cat rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty src:child0 ;
         owl:onClass ?lcat .
      ?cx_cat rdfs:subClassOf* ?lcat .
    }
  }

  GRAPH <http://codinuum.com/ont/cpi> {
    FILTER NOT EXISTS {
      ?ctx_cat_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty src:child0 ;
          owl:onClass ?lcat_ .
      ?cx_cat_ rdfs:subClassOf* ?lcat_ .
    }
  }

  OPTIONAL {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

  {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c_), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c_ OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

}
}
''' % NS_TBL

Q_DEL_INS_MOV_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?ctx_ ?x_ ?ctx ?loc ?loc_ ?cat ?cat_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_
    WHERE {
      ?x chg:movedTo ?x_ .

      FILTER EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }

    } GROUP BY ?x ?x_
  }

  ?x chg:genRemoved ?ctx_ .
  ?x_ chg:genAdded ?ctx .

  FILTER (EXISTS {
    ?x a [] .
    ?x_ a [] .
    ?cx_ src:parent+ ?x_ .
    ?cx src:parent+ ?x ;
        chg:mappedStablyTo ?cx_ .

  } || EXISTS {

    ?x a java:ReturnStatement .
    ?x_ a java:ReturnStatement .

    ?b rdf:first ?x ;
       rdf:rest rdf:nil .

    ?body a java:MethodBody ;
          chg:mappedStablyTo ?body_ ;
          src:children/rdf:rest* ?b .

    ?body_ a java:MethodBody ;
           src:children/rdf:rest* ?b_ .

    ?b_ rdf:first ?x_ ;
        rdf:rest rdf:nil .

  } || EXISTS {

    ?x src:parent ?px ;
       chg:orderChanged ?x_ .

    ?x_ src:parent ?px_ .

    ?px a src:ListNode .
    ?px_ a src:ListNode .

    FILTER NOT EXISTS {
      ?x chg:movRelabeled ?x_ .
    }

    FILTER NOT EXISTS {
      ?x a [] .
      ?cx src:parent+ ?x ;
          chg:deletedOrPruned ?ctxc_ .
    }

    FILTER NOT EXISTS {
      ?x a [] .
      ?cx src:parent+ ?x ;
          chg:movRelabeled ?cx_ .
    }

    FILTER NOT EXISTS {
      ?x_ a [] .
      ?cx_ src:parent+ ?x_ ;
           chg:insertedOrGrafted ?ctxc .
    }

  })

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

}
}
''' % NS_TBL

Q_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x_ ?ctx ?px_ ?pctx ?loc ?loc_ ?cat ?s_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x_ ?ctx
    WHERE {
      ?x_ chg:addition ?ctx .

      FILTER (EXISTS {
        [] a chg:Insertion ;
           delta:entity1 ?ctx ;
           delta:entity2 ?x_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity2 ?x_ .
      })

    } GROUP BY ?x_ ?ctx
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
      WHERE {
        ?x_ a ?c OPTION (INFERENCE NONE) .
      } GROUP BY ?x_
    }
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
      WHERE {
        ?x_ (src:parent*/src:inFile/src:location)|src:location ?loc0_ .
      } GROUP BY ?x_
    }
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?ctx (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
      WHERE {
        ?ctx (src:parent*/src:inFile/src:location)|src:location ?loc0 .
      } GROUP BY ?ctx
    }
  }

  OPTIONAL {
    ?x_ src:parent ?s_ .
    FILTER NOT EXISTS {
      ?s_ chg:addition []
    }
    FILTER NOT EXISTS {
      ?s_ a src:ListNode .
    }
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?x_ ?px_ ?pctx ?n
      WHERE {
        ?x_ src:parent+ ?px_ .
        ?px_ chg:addition ?pctx .

        FILTER EXISTS {
          [] a chg:Insertion ;
             delta:entity1 ?pctx ;
             delta:entity2 ?px_ .
        }

        FILTER NOT EXISTS {
          ?px_ a [] .
          ?x_ src:parent+ ?px0_ .
          ?px0_ src:parent+ ?px_ .
          ?px0_ chg:addition ?pctx0 .
          [] a chg:Insertion ;
             delta:entity1 ?pctx0 ;
             delta:entity2 ?px0_ .
        }

        FILTER NOT EXISTS {
          ?px_ a src:ListNode .
        }

        {
          SELECT DISTINCT ?x_ ?px_ (COUNT(DISTINCT ?px1_) AS ?n)
          WHERE {
            OPTIONAL {
              ?x_ src:parent+ ?px1_ .
              ?px1_ src:parent+ ?px_ .
              ?px1_ a src:ListNode .
            }
          } GROUP BY ?x_ ?px_
        }

      } GROUP BY ?x_ ?px_ ?pctx ?n
    }
    FILTER (?n = 0)
  }

}
}
''' % NS_TBL

Q_INS_C_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x_ ?ctx ?cx_ ?loc ?loc_ ?cat
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?cx_ ?ctx ?x_ ?file ?file_
    WHERE {

      {
        SELECT DISTINCT ?cx_ ?ctx ?x_ ?file ?file_
        WHERE {

          {
            SELECT DISTINCT ?file ?file_ ?x_ ?ctx
            WHERE {

              ?x_ a java:Entity ;
                  src:parent*/src:inFile ?file_ ;
                  chg:addition ?ctx .

              ?ctx src:parent*/src:inFile ?file .

#              ?file a src:File .
#              ?file_ a src:File .

              FILTER (EXISTS {
                [] a chg:Insertion ;
                   delta:entity1 ?ctx ;
                   delta:entity2 ?x_ .
              } || EXISTS {
                [] a chg:Move ;
                   delta:entity2 ?x_ .
              })

            } GROUP BY ?file ?file_ ?x_ ?ctx
          }

          ?file a src:File .
          ?file_ a src:File .

          ?cx_ a java:Entity ;
               src:parent+ ?x_ ;
               chg:addition ?ctx .

          FILTER NOT EXISTS {
            [] a chg:Insertion ;
               delta:entity1 ?ctx ;
               delta:entity2 ?cx_ .
          }
          FILTER NOT EXISTS {
            [] a chg:Move ;
               delta:entity1 ?cx ;
               delta:entity2 ?cx_ .
            ?cx src:parent*/src:inFile ?file .
          }

        } GROUP BY ?cx_ ?ctx ?x_ ?file ?file_
      }

      FILTER NOT EXISTS {
        ?x0_ a [] ;
             src:parent+ ?x_ .
        ?cx_ src:parent+ ?x0_ .
        ?x0_ chg:addition ?ctx .
        {
          [] a chg:Insertion ;
             delta:entity1 ?ctx ;
             delta:entity2 ?x0_ .
        } UNION {
          [] a chg:Move ;
             delta:entity2 ?x0_ .
        }
      }

    } GROUP BY ?cx_ ?ctx ?x_ ?file ?file_
  }

  FILTER (EXISTS {
    ?x_ chg:insertedInto ?ctx .
    ?cx_ chg:insertedInto ?ctx .
  } || EXISTS {
    ?x_ chg:graftedOnto ?ctx .
    ?cx_ chg:graftedOnto ?ctx .
  } || EXISTS {
    ?x_ chg:genAdded ?ctx OPTION (INFERENCE NONE) .
    ?cx_ chg:genAdded ?ctx OPTION (INFERENCE NONE) .
  } || EXISTS {
    ?x_ chg:insertedInto ?ctx .
    ?cx_ chg:graftedOnto ?ctx .
  })

  OPTIONAL {
    ?cx_ a java:Entity .
    {
      SELECT DISTINCT ?cx_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
      WHERE {
        ?cx_ a ?c OPTION (INFERENCE NONE) .
      } GROUP BY ?cx_
    }
  }

  {
    SELECT DISTINCT ?file (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?file src:location ?loc0 .
    } GROUP BY ?file
  }
  {
    SELECT DISTINCT ?file_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?file_ src:location ?loc0_ .
    } GROUP BY ?file_
  }

}
}
''' % NS_TBL

Q_INS_MOV_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x_ ?ctx ?cx ?cx_ ?loc ?loc_ ?cat_ ?cat_cx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x_ ?ctx
    WHERE {
      ?x_ chg:addition ?ctx .

      FILTER (EXISTS {
        [] a chg:Insertion ;
           delta:entity1 ?ctx ;
           delta:entity2 ?x_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity2 ?x_ .
      })

    } GROUP BY ?x_ ?ctx
  }

  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

  OPTIONAL {
    SELECT DISTINCT ?ctx (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?ctx src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?ctx
  }

  ?cx chg:movedTo ?cx_ .
  ?cx_ src:parent+ ?x_ .

  FILTER NOT EXISTS {
    ?cx_ src:parent [ a src:ListNode ] .
  }

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }

  FILTER NOT EXISTS {
    ?x0_ a [] ;
         src:parent+ ?x_ .
    ?cx_ src:parent+ ?x0_ .

    [] a chg:Insertion ;
       delta:entity1 ?ctx ;
       delta:entity2 ?x0_ .
  }
  FILTER NOT EXISTS {
    ?x1_ a [] ;
         src:parent+ ?x_ .
    ?cx_ src:parent+ ?x1_ .

    [] a chg:Move ;
       delta:entity2 ?x1_ .
  }

  OPTIONAL {
    SELECT ?cx_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_cx_)
    WHERE {
      ?cx_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?cx_
  }

}
}
''' % NS_TBL

Q_INS_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x_ ?ctx ?cx ?cx_ ?loc ?loc_ ?cat_ ?cat_cx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x_ ?ctx
    WHERE {
      ?x_ chg:addition ?ctx .

      # FILTER (EXISTS {
      #   ?chg a chg:Insertion ;
      #        delta:entity1 ?ctx ;
      #        delta:entity2 ?x_ .
      # } || EXISTS {
      #   ?chg a chg:Move ;
      #        delta:entity2 ?x_ .
      # })
    } GROUP BY ?x_ ?ctx
  }

  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

  OPTIONAL {
    SELECT DISTINCT ?ctx (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?ctx (src:parent*/src:inFile/src:location)|src:location ?loc0 .
    } GROUP BY ?ctx
  }

  ?cx chg:relabeled ?cx_ .
  {
    ?cx chg:mappedStablyTo ?cx_ .
  }
  UNION
  {
    ?cx chg:movedTo ?cx_ ;
        src:parent+ ?px .
    ?x_ src:parent ?px_ .
    ?px chg:movedTo ?px_ .
    FILTER NOT EXISTS {
      [] chg:movedTo ?x_ .
    }
  }
  ?cx_ src:parent ?x_ .

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }

  FILTER (NOT EXISTS {
    ?x_ a src:ListNode .
  } || EXISTS {
    ?x_ a ?catx_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty src:child0 ;
          owl:onClass ?lcat_ .
    }
    ?cx_ a ?lcat_ .
  })

  OPTIONAL {
    SELECT ?cx_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_cx_)
    WHERE {
      ?cx_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?cx_
  }

}
}
''' % NS_TBL

Q_INS_FILE = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?ctx ?file_ ?x_ ?cx_ ?loc_ ?xcat ?cxcat
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    ?file_ a src:File ;
           src:location ?loc_ ;
           chg:graftedOnto ?ctx .

    ?ctx a src:SourceTree .

    FILTER EXISTS {
      [] a chg:Insertion ;
         delta:entity1 ?ctx ;
         delta:entity2 ?file_ .
    }

    ?x_ a ?xcat OPTION (INFERENCE NONE) ;
        src:inFile ?file_ .

    OPTIONAL {
      ?cx_ a ?cxcat OPTION (INFERENCE NONE) ;
           src:parent* ?x_ ;
           chg:addition ?ctx .
    }
  }
  UNION
  {
    ?file_ a src:File ;
           a src:Auxfile ;
           src:location ?loc_ ;
           chg:graftedOnto ?ctx .

    ?ctx a src:SourceTree .

    FILTER EXISTS {
      [] a chg:Insertion ;
         delta:entity1 ?ctx ;
         delta:entity2 ?file_ .
    }
  }

}
}
''' % NS_TBL

Q_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?ctx_ ?px ?pctx_ ?loc ?loc_ ?cat ?s
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?ctx_
    WHERE {
      ?x chg:removal ?ctx_ .

      FILTER (EXISTS {
        [] a chg:Deletion ;
           delta:entity1 ?x ;
           delta:entity2 ?ctx_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x .
      })

    } GROUP BY ?x ?ctx_
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
      WHERE {
        ?x a ?c OPTION (INFERENCE NONE) .
      } GROUP BY ?x
    }
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
      WHERE {
        ?x (src:parent*/src:inFile/src:location)|src:location ?loc0 .
      } GROUP BY ?x
    }
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?ctx_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
      WHERE {
        ?ctx_ (src:parent*/src:inFile/src:location)|src:location ?loc0_ .
      } GROUP BY ?ctx_
    }
  }

  OPTIONAL {
    ?x src:parent ?s .
    FILTER NOT EXISTS {
      ?s chg:removal []
    }
    FILTER NOT EXISTS {
      ?s a src:ListNode .
    }
  }

  OPTIONAL {
    {
      SELECT DISTINCT ?x ?px ?pctx_ ?n
      WHERE {
        ?x src:parent+ ?px .
        ?px chg:removal ?pctx_ .

        FILTER EXISTS {
          [] a chg:Deletion ;
             delta:entity1 ?px ;
             delta:entity2 ?pctx_ .
        }

        FILTER NOT EXISTS {
          ?px a [] .
          ?x src:parent+ ?px0 .
          ?px0 src:parent+ ?px .
          ?px0 chg:removal ?pctx0_ .
          [] a chg:Deletion ;
             delta:entity1 ?px0 ;
             delta:entity2 ?pctx0_ .
        }

        FILTER NOT EXISTS {
          ?px a src:ListNode .
        }

        {
          SELECT DISTINCT ?x ?px (COUNT(DISTINCT ?px1) AS ?n)
          WHERE {
            OPTIONAL {
              ?x src:parent+ ?px1 .
              ?px1 src:parent+ ?px .
              ?px1 a src:ListNode .
            }
          } GROUP BY ?x ?px
        }

      } GROUP BY ?x ?px ?pctx_ ?n
    }
    FILTER (?n = 0)
  }

}
}
''' % NS_TBL

Q_DEL_C_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?ctx_ ?cx ?loc ?loc_ ?cat
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?cx ?ctx_ ?file ?file_
    WHERE {

      {
        SELECT DISTINCT ?x ?cx ?ctx_ ?file ?file_
        WHERE {

          {
            SELECT DISTINCT ?file ?file_ ?x ?ctx_
            WHERE {

              ?x a java:Entity ;
                 src:parent*/src:inFile ?file ;
                 chg:removal ?ctx_ .

              ?ctx_ src:parent*/src:inFile ?file_ .

#              ?file a src:File .
#              ?file_ a src:File .

              FILTER (EXISTS {
                [] a chg:Deletion ;
                     delta:entity1 ?x ;
                     delta:entity2 ?ctx_ .
              } || EXISTS {
                [] a chg:Move ;
                   delta:entity1 ?x .
              })

            } GROUP BY ?file ?file_ ?x ?ctx_
          }

          ?file a src:File .
          ?file_ a src:File .

          ?cx a java:Entity ;
              src:parent+ ?x ;
              chg:removal ?ctx_ .

          FILTER NOT EXISTS {
            [] a chg:Deletion ;
               delta:entity1 ?cx ;
               delta:entity2 ?ctx_ .
          }
          FILTER NOT EXISTS {
            [] a chg:Move ;
               delta:entity1 ?cx ;
               delta:entity2 ?cx_ .
            ?cx_ src:parent*/src:inFile ?file_ .
          }

        } GROUP BY ?x ?cx ?ctx_ ?file ?file_
      }

      FILTER NOT EXISTS {
        ?x0 a [] ;
            src:parent+ ?x .
        ?cx src:parent+ ?x0 .
        ?x0 chg:removal ?ctx_ .
        {
          [] a chg:Deletion ;
             delta:entity1 ?x0 ;
             delta:entity2 ?ctx_ .
        } UNION {
          [] a chg:Move ;
             delta:entity1 ?x0 .
        }

      }

    } GROUP BY ?x ?cx ?ctx_ ?file ?file_
  }

  FILTER (EXISTS {
    ?x chg:deletedFrom ?ctx_ .
    ?cx chg:deletedFrom ?ctx_ .
  } || EXISTS {
    ?x chg:prunedFrom ?ctx_ .
    ?cx chg:prunedFrom ?ctx_ .
  } || EXISTS {
    ?x chg:genRemoved ?ctx_ OPTION (INFERENCE NONE) .
    ?cx chg:genRemoved ?ctx_ OPTION (INFERENCE NONE) .
  } || EXISTS {
    ?x chg:deletedFrom ?ctx_ .
    ?cx chg:prunedFrom ?ctx_ .
  })

  OPTIONAL {
    ?cx a java:Entity .
    {
      SELECT DISTINCT ?cx (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
      WHERE {
        ?cx a ?c OPTION (INFERENCE NONE) .
      } GROUP BY ?cx
    }
  }

  {
    SELECT DISTINCT ?file (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?file src:location ?loc0 .
    } GROUP BY ?file
  }
  {
    SELECT DISTINCT ?file_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?file_ src:location ?loc0_ .
    } GROUP BY ?file_
  }

}
}
''' % NS_TBL

Q_DEL_MOV_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?ctx_ ?cx ?cx_ ?loc ?loc_ ?cat ?cat_cx
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?ctx_
    WHERE {
      ?x chg:removal ?ctx_ .

      FILTER (EXISTS {
        [] a chg:Deletion ;
           delta:entity1 ?x ;
           delta:entity2 ?ctx_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x .
      })

    } GROUP BY ?x ?ctx_
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }

  OPTIONAL {
    SELECT DISTINCT ?ctx_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?ctx_ (src:parent*/src:inFile/src:location)|src:location ?loc0_ .
    } GROUP BY ?ctx_
  }

  ?cx src:parent+ ?x ;
      chg:movedTo ?cx_ .

  FILTER NOT EXISTS {
    ?cx src:parent [ a src:ListNode ] .
  }

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }

  FILTER NOT EXISTS {
    ?x1 src:parent+ ?x .
    ?cx src:parent+ ?x1 .

    [] a chg:Move ;
       delta:entity1 ?x1 .
  }
  FILTER NOT EXISTS {
    ?x0 src:parent+ ?x .
    ?cx src:parent+ ?x0 .

    [] a chg:Deletion ;
       delta:entity1 ?x0 .
  }

  OPTIONAL {
    SELECT ?cx (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_cx)
    WHERE {
      ?cx a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?cx
  }

}
}
''' % NS_TBL

Q_DEL_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?ctx_ ?cx ?cx_ ?loc ?loc_ ?cat ?cat_cx
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?ctx_
    WHERE {
      ?x chg:removal ?ctx_ .

      # FILTER (EXISTS {
      #   [] a chg:Deletion ;
      #      delta:entity1 ?x ;
      #      delta:entity2 ?ctx_ .
      # } || EXISTS {
      #   [] a chg:Move ;
      #      delta:entity1 ?x .
      # })
    } GROUP BY ?x ?ctx_
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }

  OPTIONAL {
    SELECT DISTINCT ?ctx_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?ctx_ (src:parent*/src:inFile/src:location)|src:location ?loc0_ .
    } GROUP BY ?ctx_
  }

  ?cx src:parent ?x ;
      chg:relabeled ?cx_ .
  {
    ?cx chg:mappedStablyTo ?cx_ .
  }
  UNION
  {
    ?cx chg:movedTo ?cx_ .
    ?cx_ src:parent+ ?px_ .
    ?x src:parent ?px .
    ?px chg:movedTo ?px_ .
    FILTER NOT EXISTS {
      ?x chg:movedTo [] .
    }
  }

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }

  FILTER (NOT EXISTS {
    ?x a src:ListNode .
  } || EXISTS {
    ?x a ?catx OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty src:child0 ;
         owl:onClass ?lcat .
    }
    ?cx a ?lcat .
  })

  OPTIONAL {
    SELECT ?cx (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_cx)
    WHERE {
      ?cx a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?cx
  }

}
}
''' % NS_TBL

Q_DEL_FILE = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?file ?x ?cx ?ctx_ ?loc ?xcat ?cxcat
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    ?file a src:File ;
          src:location ?loc ;
          chg:prunedFrom ?ctx_ .

    ?ctx_ a src:SourceTree .

    FILTER EXISTS {
      [] a chg:Deletion ;
         delta:entity1 ?file ;
         delta:entity2 ?ctx_ .
    }

    ?x a ?xcat OPTION (INFERENCE NONE) ;
       src:inFile ?file .

    OPTIONAL {
      ?cx a ?cxcat OPTION (INFERENCE NONE) ;
          src:parent* ?x ;
          chg:removal ?ctx_ .
    }
  }
  UNION
  {
    ?file a src:File ;
          a src:Auxfile ;
          src:location ?loc ;
          chg:prunedFrom ?ctx_ .

    ?ctx_ a src:SourceTree .

    FILTER EXISTS {
      [] a chg:Deletion ;
         delta:entity1 ?file ;
         delta:entity2 ?ctx_ .
    }
  }

}
}
''' % NS_TBL

Q_MOV_FILE = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?file ?file_ ?loc ?loc_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?file a src:File ;
        src:location ?loc ;
        chg:movedTo ?file_ .

  ?file_ a src:File ;
         src:location ?loc_ .

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?file ;
       delta:entity2 ?file_ .
  }

}
}
''' % NS_TBL

Q_CHG_FILE = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?file ?file_ ?loc ?loc_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?file a src:Auxfile ;
        src:location ?loc ;
        chg:modified ?file_ .

  ?file_ a src:Auxfile ;
         src:location ?loc_ .

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?file ;
       delta:entity2 ?file_ .
  }

}
}
''' % NS_TBL

Q_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cx ?cx_ ?cat_cx
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?file ?file_
    WHERE {

      ?x a java:Entity ;
         src:parent*/src:inFile ?file ;
         chg:relabeled ?x_ .

      ?x_ a java:Entity ;
          src:parent*/src:inFile ?file_ .

      ?chg a chg:Relabeling ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .

    } GROUP BY ?x ?x_ ?file ?file_
  }

  FILTER NOT EXISTS {
    ?x chg:movedTo ?x_ .
  }

  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c_), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x_ a ?c_ OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?file (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?file src:location ?loc0 .
    } GROUP BY ?file
  }
  {
    SELECT DISTINCT ?file_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?file_ src:location ?loc0_ .
    } GROUP BY ?file_
  }

  OPTIONAL {
    ?cx src:parent ?x ;
        chg:relabeled ?cx_ .

    ?cx_ src:parent ?x_ .

    ?cchg a chg:Relabeling ;
          delta:entity1 ?cx ;
          delta:entity2 ?cx_ .

    FILTER (NOT EXISTS {
      ?x a src:ListNode .
    } && NOT EXISTS {
      ?x_ a src:ListNode .
    } && NOT EXISTS {
      ?cx chg:movedTo ?cx_ .
    })

    {
      SELECT ?cx_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c0_), "#"); SEPARATOR="|") AS ?cat_cx)
      WHERE {
        ?cx_ a ?c0_ OPTION (INFERENCE NONE) .
      } GROUP BY ?cx_
    }
  }

  OPTIONAL {
    ?cx src:parent ?x ;
        chg:relabeled ?cx_ .

    ?cx_ src:parent ?x_ .

    FILTER NOT EXISTS {
      ?cx chg:movedTo ?cx_ .
    }

    ?cchg a chg:Relabeling ;
          delta:entity1 ?cx ;
          delta:entity2 ?cx_ .

    ?x a ?catx OPTION (INFERENCE NONE) ;
       src:child ?cx ;
       ?p_child ?cx OPTION (INFERENCE NONE) .

    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
    }
    ?cx a ?child_class .

    ?x_ a ?catx_ OPTION (INFERENCE NONE) ;
        src:child ?cx_ ;
        ?p_child_ ?cx_ OPTION (INFERENCE NONE) .

    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
    }
    ?cx_ a ?child_class_ .

    {
      SELECT ?cx_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c0_), "#"); SEPARATOR="|") AS ?cat_cx)
      WHERE {
        ?cx_ a ?c0_ OPTION (INFERENCE NONE) .
      } GROUP BY ?cx_
    }

  }

}
}
''' % NS_TBL

Q_REL_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cx ?ctx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?file ?file_ ?cx ?catc ?ctx_
    WHERE {

      {
        SELECT DISTINCT ?x ?x_ ?file ?file_
        WHERE {
          ?x chg:relabeled ?x_ .
             #chg:mappedStablyTo ?x_ .

          ?x src:parent*/src:inFile ?file .
          ?x_ src:parent*/src:inFile ?file_ .

        } GROUP BY ?x ?x_ ?file ?file_
      }

      ?cx a ?catc OPTION (INFERENCE NONE) ;
          src:parent ?x ;
          chg:removal ?ctx_ .

      ?ctx_ src:parent*/src:inFile ?file_ .

    } GROUP BY ?x ?x_ ?file ?file_ ?cx ?catc ?ctx_
  }

  {
    ?x a ?catx OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
    }
    FILTER EXISTS {
      ?x ?p_child ?cx OPTION (INFERENCE NONE) .
      ?cx a ?child_class .
    }
    FILTER NOT EXISTS {
      ?x a src:ListNode .
    }
  }
  UNION
  {
    ?x a src:TupleNode .
  }

  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?file (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?file src:location ?loc0 .
    } GROUP BY ?file
  }
  {
    SELECT DISTINCT ?file_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?file_ src:location ?loc0_ .
    } GROUP BY ?file_
  }

}
}
''' % NS_TBL

Q_REL_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cx_ ?ctx
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?file ?file_ ?cx_ ?catc_ ?ctx
    WHERE {

      {
        SELECT DISTINCT ?x ?x_ ?file ?file_
        WHERE {
          ?x chg:relabeled ?x_ .
             #chg:mappedStablyTo ?x_ .

          ?x src:parent*/src:inFile ?file .
          ?x_ src:parent*/src:inFile ?file_ .

        } GROUP BY ?x ?x_ ?file ?file_
      }

      ?cx_ a ?catc_ OPTION (INFERENCE NONE) ;
           src:parent ?x_ ;
           chg:addition ?ctx .

      ?ctx src:parent*/src:inFile ?file .

    } GROUP BY ?x ?x_ ?file ?file_ ?cx_ ?catc_ ?ctx
  }

  {
    ?x_ a ?catx_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
    }
    FILTER EXISTS {
      ?x_ ?p_child_ ?cx_ OPTION (INFERENCE NONE) .
      ?cx_ a ?child_class_
    }
    FILTER NOT EXISTS {
      ?x_ a src:ListNode .
    }
  }
  UNION
  {
    ?x_ a src:TupleNode .
  }

  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?file (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?file src:location ?loc0 .
    } GROUP BY ?file
  }
  {
    SELECT DISTINCT ?file_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?file_ src:location ?loc0_ .
    } GROUP BY ?file_
  }

}
}
''' % NS_TBL

Q_MOV_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?x_ ?ctx ?ctx_ ?loc ?loc_ ?cat ?cat_ ?cx ?cx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_
    WHERE {
      ?x chg:movedTo ?x_ .

      FILTER EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }

    } GROUP BY ?x ?x_
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

  ?x chg:removal ?ctx_ .
  ?x_ chg:addition ?ctx .

  FILTER EXISTS {
     ?x src:parent*/src:inFile ?file .
     ?ctx src:parent*/src:inFile ?file .
  }
  FILTER EXISTS {
     ?x_ src:parent*/src:inFile ?file_ .
     ?ctx_ src:parent*/src:inFile ?file_ .
  }

  OPTIONAL {
    ?cx src:parent+ ?x ;
        chg:movedTo ?cx_ .

    ?cx_ src:parent+ ?x_ .

    {
      SELECT ?cx (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_cx)
      WHERE {
        ?cx a ?c OPTION (INFERENCE NONE) .
      } GROUP BY ?cx
    }
    {
      SELECT ?cx_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c_), "#"); SEPARATOR="|") AS ?cat_cx_)
      WHERE {
        ?cx_ a ?c_ OPTION (INFERENCE NONE) .
      } GROUP BY ?cx_
    }

    FILTER NOT EXISTS {
      [] a chg:Move ;
         delta:entity1 ?cx ;
         delta:entity2 ?cx_ .
    }

    FILTER NOT EXISTS {
      ?x1 a [] ;
          src:parent+ ?x ;
          chg:movedTo ?x1_ .
      ?cx src:parent+ ?x1 .
      [] a chg:Move ;
         delta:entity1 ?x1 ;
         delta:entity2 ?x1_ .
    }

  }

}
}
''' % NS_TBL

Q_MOVREL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cat_ #?ctx ?ctx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {
  ?x chg:movedTo ?x_ ;
     chg:movRelabeled ?x_ .

  ?x chg:removal ?ctx_ .
  ?x_ chg:addition ?ctx .

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

}
}
''' % NS_TBL

Q_MOV_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cat_ ?ctx ?ctx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x chg:movedTo ?x_ ;
     chg:movRelabeled ?x_ .

  ?x chg:removal ?ctx_ .
  ?x_ chg:addition ?ctx .

  ?x a ?catx OPTION(INFERENCE NONE) ;
     ?p_child ?cx OPTION(INFERENCE NONE) .

  ?x_ a ?catx_ OPTION(INFERENCE NONE) ;
      ?p_child_ ?cx_ OPTION(INFERENCE NONE) .

  GRAPH <http://codinuum.com/ont/cpi> {
    ?p_child rdfs:subPropertyOf src:child .
    ?catx rdfs:subClassOf* ?ln .
    ?ln owl:equivalentClass ?r .
    ?r a owl:Restriction ;
       owl:onProperty ?p_child ;
       owl:onClass ?child_class .
  }
  GRAPH <http://codinuum.com/ont/cpi> {
    ?p_child_ rdfs:subPropertyOf src:child .
    ?catx_ rdfs:subClassOf* ?ln_ .
    ?ln_ owl:equivalentClass ?r_ .
    ?r_ a owl:Restriction ;
        owl:onProperty ?p_child_ ;
        owl:onClass ?child_class_ .
  }

  FILTER (NOT EXISTS {
    ?x ?p_child_ ?cx0 .
    ?cx0 a ?child_class_ .
  } || NOT EXISTS {
    ?x_ ?p_child ?cx0_ .
    ?cx0_ a ?child_class .
  })

  FILTER NOT EXISTS {
    [] a chg:Move ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }
  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }
  FILTER NOT EXISTS {
    ?x a src:ListNode .
  }
  FILTER NOT EXISTS {
    ?x_ a src:ListNode .
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

}
}
''' % NS_TBL

Q_MOV_REL_EX_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cat_ ?ctx ?ctx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?ctx ?ctx_
    WHERE {

      ?x chg:movedTo ?x_ ;
         chg:movRelabeled ?x_ .

      ?x chg:removal ?ctx_ .
      ?x_ chg:addition ?ctx .

      FILTER NOT EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }
      FILTER EXISTS {
        [] a chg:Relabeling ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }
      FILTER NOT EXISTS {
        ?x a src:ListNode .
      }
      FILTER NOT EXISTS {
        ?x_ a src:ListNode .
      }

    } GROUP BY ?x ?x_ ?ctx ?ctx_
  }

  ?x a ?catx OPTION(INFERENCE NONE) .
  ?x_ a ?catx_ OPTION(INFERENCE NONE) .

  {
    ?x ?p_child ?cx OPTION (INFERENCE NONE) .

    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
    }
  }
  UNION
  {
    ?x_ ?p_child_ ?cx_ OPTION (INFERENCE NONE) .

    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
    }
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

}
}
''' % NS_TBL

Q_MOV_REL_EX2_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cat_ ?ctx ?ctx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?ctx ?ctx_
    WHERE {

      ?x chg:movedTo ?x_ ;
         chg:movRelabeled ?x_ .

      ?x chg:removal ?ctx_ .
      ?x_ chg:addition ?ctx .

      FILTER NOT EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }
      FILTER EXISTS {
        [] a chg:Relabeling ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }

    } GROUP BY ?x ?x_ ?ctx ?ctx_
  }

  {
    ?x java:name ?xname ;
       java:declaredBy [] .
  }
  UNION
  {
    ?x_ java:name ?xname_ ;
        java:declaredBy [] .
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

}
}
''' % NS_TBL

Q_DEL_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?y ?loc ?loc_ ?catxx ?catyy ?ctxx_ ?ctxy_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?px ?px_ ?x ?ctxx_ ?y ?ctxy_
    WHERE {

      {
        SELECT DISTINCT ?px ?px_ ?catp ?catp_ ?x ?catx ?ctxx_ ?y ?caty ?ctxy_
        WHERE {

          {
            SELECT DISTINCT ?px ?px_ ?catp ?catp_
            WHERE {

              ?px a ?catp OPTION (INFERENCE NONE) ;
                  chg:mappedStablyTo ?px_ .

              ?px_ a ?catp_ OPTION (INFERENCE NONE) .

              FILTER NOT EXISTS {
                ?px a src:ListNode .
              }
              FILTER NOT EXISTS {
                ?px_ a src:ListNode .
              }

            } GROUP BY ?px ?px_ ?catp ?catp_
          }

          ?x a ?catx OPTION (INFERENCE NONE) ;
             src:parent ?px ;
             chg:removal ?ctxx_ .

          FILTER EXISTS {
            [] a chg:Deletion ;
               delta:entity1 ?x ;
               delta:entity2 ?ctxx_ .
          }

          ?y a ?caty OPTION (INFERENCE NONE) ;
             src:parent ?px ;
             chg:removal ?ctxy_ .

          FILTER (?x != ?y)

        } GROUP BY ?px ?px_ ?catp ?catp_ ?x ?catx ?ctxx_ ?y ?caty ?ctxy_
      }

      ?z a ?catz OPTION (INFERENCE NONE) ;
         src:parent+ ?y ;
         chg:mappedStablyTo ?z_ .

      ?z_ a ?catz_ OPTION (INFERENCE NONE) ;
          src:parent+ ?px_ .

      ?px ?p_child0 ?x OPTION (INFERENCE NONE) ;
          ?p_child1 ?y OPTION (INFERENCE NONE) .

      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0 rdfs:subPropertyOf src:child .
        ?p_child1 rdfs:subPropertyOf src:child .

        ?catp rdfs:subClassOf* ?ln0 .
        ?ln0 owl:equivalentClass ?r0 .
        ?r0 a owl:Restriction ;
            owl:onProperty ?p_child0 ;
            owl:onClass ?child_class0 .
      }

      FILTER NOT EXISTS {
        ?y a ?child_class0 .
      }

      ?px_ ?p_child0 ?w_ .
      ?z_ src:parent* ?w_ .

    } GROUP BY ?px ?px_ ?x ?ctxx_ ?y ?ctxy_
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?catxx)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?y (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?catyy)
    WHERE {
      ?y a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?y
  }

  OPTIONAL {
    SELECT ?px (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?px src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?px
  }
  OPTIONAL {
    SELECT ?px_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?px_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?px_
  }

}
}
''' % NS_TBL


Q_MOV_MOVREL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("MoveRelabel" AS ?name)
(?x AS ?key) (?x_ AS ?key_)
(?cx AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x chg:movedTo ?x_ .

  ?cx src:parent* ?x ;
      chg:movedTo ?cx_ ;
      chg:movRelabeled ?cx_ .

  ?cx_ src:parent* ?x_ .

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }
  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }
  FILTER NOT EXISTS {#!!!!!OK
    ?x a src:ListNode .
  }
  FILTER NOT EXISTS {
    ?x_ a src:ListNode .
  }

}
}
''' % NS_TBL

Q_MOV_MOVREL_NAME_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("MoveRelabel" AS ?name)
(?x AS ?key) (?x_ AS ?key_)
(?cx AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x java:inMethodOrConstructor ?meth ;
     chg:movedTo ?x_ .

  ?cx a java:Name ;
      src:parent+ ?x ;
      chg:movedTo ?cx_ ;
      chg:movRelabeled ?cx_ .

  ?cx_ a java:Name ;
       java:name ?name_ ;
       src:parent+ ?x_ .

  FILTER NOT EXISTS {
    ?v java:declaredBy ?def ;
       java:name ?name_ .
    ?def java:inMethodOrConstructor ?meth .
  }

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }
  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }
  FILTER NOT EXISTS {#!!!!!OK
    ?x a src:ListNode .
  }
  FILTER NOT EXISTS {
    ?x_ a src:ListNode .
  }

}
}
''' % NS_TBL

Q_MOVINSREL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("MoveInsertRelabel" AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?cx AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x chg:movedTo ?x_ .

  ?x_ chg:genAdded ?ctx .

  ?cx src:parent* ?x ;
      chg:movedTo ?cx_ ;
      chg:relabeled ?cx_ .

  ?cx_ src:parent* ?x_ .

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }
  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }
  FILTER NOT EXISTS {
    [] a chg:Move ;
       delta:entity1 ?cx ;
       delta:entity2 ?cx_ .
  }
  FILTER NOT EXISTS {#!!!!!OK
    ?x a src:ListNode .
  }
  FILTER NOT EXISTS {
    ?x_ a src:ListNode .
  }

}
}
''' % NS_TBL

Q_MOVINS_INS_0_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveInsert:", ?fqn_) AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?ctxc AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx
    WHERE {

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
         chg:movedTo ?x_ .

      ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
          java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ ;
          chg:genAdded ?ctx .

      # FILTER EXISTS {
      #   [] a chg:Move ;
      #      delta:entity1 ?x ;
      #      delta:entity2 ?x_ .
      # }

    } GROUP BY ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx
  }

  ?cx_ src:parent ?x_ ;
       chg:addition ?ctxc .

  # FILTER (EXISTS {
  #   [] a chg:Insertion ;
  #      delta:entity1 ?catxc ;
  #      delta:entity2 ?cx_ .
  # } || EXISTS {
  #   [] a chg:Move ;
  #      delta:entity2 ?cx_ .
  # })

  {
    ?x_ a ?catx_ OPTION (INFERENCE NONE) .

    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
    }

    FILTER EXISTS {
      ?x_ ?p_child_ ?cx_ OPTION (INFERENCE NONE) .
      ?cx_ a ?child_class_
    }

    FILTER (NOT EXISTS {
      ?x_ a src:ListNode .
    } || NOT EXISTS {
      ?cx0_ src:parent ?x_ .
      FILTER (?cx0_ != ?cx_)
      GRAPH <http://codinuum.com/ont/cpi> {
        ?r_ owl:minQualifiedCardinality 1 .
      }
    })

    # FILTER NOT EXISTS {
    #   GRAPH <http://codinuum.com/ont/cpi> {
    #     ?r_ owl:maxQualifiedCardinality ?c .
    #   }
    # }

  }

}
}
''' % NS_TBL

Q_MOVINS_INS_1_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveInsert:", ?fqn_) AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?ctxc AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx
    WHERE {

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
         chg:movedTo ?x_ .

      ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
          java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ ;
          chg:genAdded ?ctx .

    } GROUP BY ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx
  }

  ?cx_ src:parent ?x_ ;
       chg:addition ?ctxc .

  ?x_ a src:TupleNode .

}
}
''' % NS_TBL

Q_INS_MOVINS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveInsert:", ?fqn_) AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?ctxc AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ ;
      chg:addition ?ctx .

  {
    SELECT DISTINCT ?x_ ?cx ?cx_ ?catc ?catc_ ?ctxc
    WHERE {

      ?cx a ?catc OPTION (INFERENCE NONE) ;
          chg:movedTo ?cx_ .

      ?cx_ a ?catc_ OPTION (INFERENCE NONE) ;
           src:parent ?x_ ;
           chg:genAdded ?ctxc .

    } GROUP BY ?x_ ?cx ?cx_ ?catc ?catc_ ?ctxc
  }

  FILTER (EXISTS {
    ?x_ a ?catx_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
    }

    FILTER EXISTS {
      ?x_ ?p_child_ ?cx_ OPTION (INFERENCE NONE) .
      ?cx_ a ?child_class_
    }

    FILTER (NOT EXISTS {
      ?x_ a src:ListNode .
    } || (NOT EXISTS {
      ?cx0_ src:parent ?x_ .
      FILTER (?cx0_ != ?cx_)
    } && EXISTS {
     GRAPH <http://codinuum.com/ont/cpi> {
        ?r_ owl:minQualifiedCardinality 1 .
      }
    }))

  } || EXISTS {
    ?x_ a src:TupleNode .
  })

}
}
''' % NS_TBL

Q_MOVDEL_DEL_0_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveDelete:", ?fqn) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?cx AS ?ent) (?ctxc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx_
    WHERE {

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
         chg:movedTo ?x_ ;
         chg:genRemoved ?ctx_ .

      ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
          java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ .

      # FILTER EXISTS {
      #   [] a chg:Move ;
      #      delta:entity1 ?x ;
      #      delta:entity2 ?x_ .
      # }

    } GROUP BY ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx_
  }

  ?cx a ?catcx OPTION (INFERENCE NONE) ;
      src:parent ?x ;
      chg:removal ?ctxc_ .

  # FILTER (EXISTS {
  #   [] a chg:Deletion ;
  #      delta:entity1 ?cx ;
  #      delta:entity2 ?catxc_ .
  # } || EXISTS {
  #   [] a chg:Move ;
  #      delta:entity1 ?cx .
  # })

  {
    ?x a ?catx OPTION (INFERENCE NONE) .

    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
    }

    FILTER EXISTS {
      ?x ?p_child ?cx OPTION (INFERENCE NONE) .
      ?cx a ?child_class .
    }

    FILTER (NOT EXISTS {
      ?x a src:ListNode .
    } || NOT EXISTS {
      ?cx0 src:parent ?x .
      FILTER (?cx0 != ?cx)
      GRAPH <http://codinuum.com/ont/cpi> {
        ?r owl:minQualifiedCardinality 1 .
      }
    })

    # FILTER NOT EXISTS {
    #   GRAPH <http://codinuum.com/ont/cpi> {
    #     ?r owl:maxQualifiedCardinality ?c .
    #   }
    # }

  }

}
}
''' % NS_TBL

Q_MOVDEL_DEL_1_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveDelete:", ?fqn) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?cx AS ?ent) (?ctxc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx_
    WHERE {

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
         chg:movedTo ?x_ ;
         chg:genRemoved ?ctx_ .

      ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
          java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ .

    } GROUP BY ?x ?x_ ?cat ?cat_ ?fqn ?fqn_ ?ctx_
  }

  ?cx a ?catcx OPTION (INFERENCE NONE) ;
      src:parent ?x ;
      chg:removal ?ctxc_ .

  ?x a src:TupleNode .

}
}
''' % NS_TBL

Q_DEL_LN_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("DeleteListNode:", ?fqn) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?px AS ?ent) (?ctxp_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?cat ?x ?ctx_ ?px ?ctxp_ ?ax ?ax_ ?meth ?fqn ?cata ?xx
    WHERE {

      {
        SELECT DISTINCT ?cat ?x ?ctx_ ?px ?ctxp_ ?ax ?ax_ ?meth ?fqn ?cata
        WHERE {

          {
            SELECT DISTINCT ?cat ?x ?ctx_ ?px ?ctxp_ ?ax ?meth
            WHERE {

              ?x a ?cat OPTION (INFERENCE NONE) ;
                 chg:removal ?ctx_ ;
                 src:parent ?px .

              ?px a src:ListNode ;
                  java:inMethodOrConstructor ?meth ;
                  src:parent+ ?ax ;
                  chg:removal ?ctxp_ .

            } GROUP BY ?cat ?x ?ctx_ ?px ?ctxp_ ?ax ?meth
          }

          ?ax a ?cata OPTION (INFERENCE NONE) ;
              java:inMethodOrConstructor ?meth ;
              chg:mappedStablyTo ?ax_ .

          ?meth java:fullyQualifiedName ?fqn .

          FILTER NOT EXISTS {
            ?ax a [] .
            ?ax0 chg:mappedStablyTo ?ax0_ ;
                 src:parent+ ?ax .
            ?px src:parent+ ?ax0 .
          }

        } GROUP BY ?cat ?x ?ctx_ ?px ?ctxp_ ?ax ?ax_ ?meth ?fqn ?cata
      }

      ?px src:parent+ ?xx .
      ?xx a ?catxx OPTION (INFERENCE NONE) ;
          src:parent+ ?ax .

      FILTER NOT EXISTS {
        ?xx a src:ListNode .
      }

      ?xx java:inMethodOrConstructor/java:fullyQualifiedName ?fqn .

    } GROUP BY ?cat ?x ?ctx_ ?px ?ctxp_ ?ax ?ax_ ?meth ?fqn ?cata ?xx
  }

  ?cx a ?catc OPTION (INFERENCE NONE) ;
      src:parent+ ?xx ;
      chg:mappedStablyTo ?cx_ .

  FILTER NOT EXISTS {
    ?cx src:parent ?xx .
    ?cx_ src:parent ?xx_ .
    ?xx_ a ?catxx OPTION (INFERENCE NONE) .
  }

  FILTER NOT EXISTS {
    ?xx a [] .
    ?cx src:parent+ ?y .
    ?y a src:ListNode ;
       src:parent+ ?xx .
  }

}
}
''' % NS_TBL

Q_DEL_LN_DEL_2_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("DeleteListNode") AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?ln AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ln ?ctx_ ?cat ?x ?ctxx_ ?p ?p_
    WHERE {

      {
        SELECT DISTINCT ?ln ?ctx_ ?cat ?x ?ctxx_
        WHERE {

          ?ln a src:ListNode ;
              a ?cat OPTION (INFERENCE NONE) ;
              chg:removal ?ctx_ .

          ?x src:parent ?ln ;
             chg:removal ?ctxx_ .

          [] a chg:Deletion ;
             delta:entity1 ?x ;
             delta:entity2 ?ctxx_ .

        } GROUP BY ?ln ?ctx_ ?cat ?x ?ctxx_
      }

      ?ln src:parent+ ?p .

      ?p chg:mappedStablyTo ?p_ .

      FILTER NOT EXISTS {
        ?p0 chg:mappedStablyTo ?p0_ .
        ?ln src:parent+ ?p0 .
        ?p0 src:parent+ ?p .
      }

    } GROUP BY ?ln ?ctx_ ?cat ?x ?ctxx_ ?p ?p_
  }

  ?x src:parent+ ?y .
  ?y src:parent ?p .

  FILTER NOT EXISTS {
   ?p src:child ?y ;
      ?p_child ?y OPTION (INFERENCE NONE) .
    ?p a ?catp OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catp rdfs:subClassOf*/owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
    }
    ?x a ?child_class .
  }

  FILTER NOT EXISTS {
    ?p a src:ListNode ;
       a ?catp OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?catp rdfs:subClassOf*/owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty src:child0 ;
         owl:onClass ?child_class .
    }
    ?x a ?child_class .
  }

}
}
''' % NS_TBL

Q_INS_LN_INS_2_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("InsertListNode") AS ?name)
(?ctxx AS ?ent) (?x_ AS ?ent_)
(?ctx AS ?dep) (?ln_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ln_ ?ctx ?cat_ ?x_ ?ctxx ?p ?p_
    WHERE {

      {
        SELECT DISTINCT ?ln_ ?ctx ?cat_ ?x_ ?ctxx
        WHERE {

          ?ln_ a src:ListNode ;
               a ?cat_ OPTION (INFERENCE NONE) ;
               chg:addition ?ctx .

          ?x_ src:parent ?ln_ ;
              chg:addition ?ctxx .

          [] a chg:Insertion ;
             delta:entity1 ?ctxx ;
             delta:entity2 ?x_ .

        } GROUP BY ?ln_ ?ctx ?cat_ ?x_ ?ctxx
      }

      ?ln_ src:parent+ ?p_ .

      ?p chg:mappedStablyTo ?p_ .

      FILTER NOT EXISTS {
        ?p0 chg:mappedStablyTo ?p0_ .
        ?ln_ src:parent+ ?p0_ .
        ?p0_ src:parent+ ?p_ .
      }

    } GROUP BY ?ln_ ?ctx ?cat_ ?x_ ?ctxx ?p ?p_
  }

  ?x_ src:parent+ ?y_ .
  ?y_ src:parent ?p_ .

  FILTER NOT EXISTS {
   ?p_ src:child ?y_ ;
       ?p_child_ ?y_ OPTION (INFERENCE NONE) .
    ?p_ a ?catp_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catp_ rdfs:subClassOf*/owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
    }
    ?x_ a ?child_class_ .
  }

  FILTER NOT EXISTS {
    ?p_ a src:ListNode ;
        a ?catp_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?catp_ rdfs:subClassOf*/owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty src:child0 ;
          owl:onClass ?child_class_ .
    }
    ?x_ a ?child_class_ .
  }

}
}
''' % NS_TBL


Q_DEL_METH_LN_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("DeleteListNode:", ?fqn) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?px AS ?ent) (?ctxp_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a ?cat OPTION (INFERENCE NONE) ;
     chg:removal ?ctx_ ;
     src:parent [ a src:ListNode ] ;
     src:parent+ ?px .

  ?px a ?catpx OPTION (INFERENCE NONE) ;
      a src:ListNode ;
      src:parent ?meth ;
      chg:removal ?ctxp_ .

  FILTER NOT EXISTS {
    ?x src:parent+ ?px0 .

    ?px0 a src:ListNode ;
         src:parent+ ?px ;
         chg:mappedStablyTo [ a src:ListNode ] .
  }

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn .

}
}
''' % NS_TBL

Q_INS_LN_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("InsertListNode:", ?fqn_) AS ?name)
#(?ctx AS ?key) (?x_ AS ?key_)
#(?ctxp AS ?ent) (?px_ AS ?ent_)
(?ctx AS ?ent) (?x_ AS ?ent_)
(?ctxp AS ?dep) (?px_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?cat_ ?x_ ?ctx ?px_ ?ctxp ?ax ?ax_ ?meth_ ?fqn_ ?cata_ ?xx_
    WHERE {

      {
        SELECT DISTINCT ?cat_ ?x_ ?ctx ?px_ ?ctxp ?ax ?ax_ ?meth_ ?fqn_ ?cata_
        WHERE {

          {
            SELECT DISTINCT ?cat_ ?x_ ?ctx ?px_ ?ctxp ?ax_ ?meth_
            WHERE {

              ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
                  chg:addition ?ctx ;
                  src:parent ?px_ .

              ?px_ a src:ListNode ;
                   java:inMethodOrConstructor ?meth_ ;
                   src:parent+ ?ax_ ;
                   chg:addition ?ctxp .

            } GROUP BY ?cat_ ?x_ ?ctx ?px_ ?ctxp ?ax_ ?meth_
          }

          ?ax_ a ?cata_ OPTION (INFERENCE NONE) ;
               java:inMethodOrConstructor ?meth_ .

          ?ax chg:mappedStablyTo ?ax_ .

          ?meth_ java:fullyQualifiedName ?fqn_ .

          FILTER NOT EXISTS {
            ?ax_ a [] .
            ?ax0 chg:mappedStablyTo ?ax0_ .
            ?ax0_ src:parent+ ?ax_ .
            ?px_ src:parent+ ?ax0_ .
          }

        } GROUP BY ?cat_ ?x_ ?ctx ?px_ ?ctxp ?ax ?ax_ ?meth_ ?fqn_ ?cata_
      }

      ?px_ src:parent+ ?xx_ .
      ?xx_ a ?catxx_ OPTION (INFERENCE NONE) ;
           src:parent+ ?ax_ .

      FILTER NOT EXISTS {
        ?xx_ a src:ListNode .
      }

      ?xx_ java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ .

    } GROUP BY ?cat_ ?x_ ?ctx ?px_ ?ctxp ?ax ?ax_ ?meth_ ?fqn_ ?cata_ ?xx_
  }

  ?cx_ a ?catc_ OPTION (INFERENCE NONE) ;
       src:parent+ ?xx_ .

  ?cx chg:mappedStablyTo ?cx_ .

  FILTER NOT EXISTS {
    ?cx src:parent ?xx .
    ?cx_ src:parent ?xx_ .
    ?xx a ?catxx_ OPTION (INFERENCE NONE) .
  }

  FILTER NOT EXISTS {
    ?xx_ a [] .
    ?cx_ src:parent+ ?y_ .
    ?y_ a src:ListNode ;
        src:parent+ ?xx_ .
  }

}
}
''' % NS_TBL

Q_INS_METH_LN_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("InsertListNode:", ?fqn_) AS ?name)
(?ctx AS ?ent) (?x_ AS ?ent_)
(?ctxp AS ?dep) (?px_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      chg:addition ?ctx ;
      src:parent [ a src:ListNode ] ;
      src:parent+ ?px_ .

  ?px_ a ?catpx_ OPTION (INFERENCE NONE) ;
       a src:ListNode ;
       src:parent ?meth_ ;
       chg:addition ?ctxp .

  FILTER NOT EXISTS {
    ?x_ src:parent+ ?px0_ .

    ?px0_ a src:ListNode ;
          src:parent+ ?px_ .

    ?px0 a src:ListNode ;
         chg:mappedStablyTo ?px0_ .
  }

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ .

}
}
''' % NS_TBL

Q_DEL_MOVDEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveDelete:", ?fqn) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?cx AS ?ent) (?ctxc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
     chg:removal ?ctx_ .

  {
    SELECT DISTINCT ?x ?cx ?cx_ ?catc ?catc_ ?ctxc_
    WHERE {

      ?cx a ?catc OPTION (INFERENCE NONE) ;
         src:parent ?x ;
         chg:movedTo ?cx_ ;
         chg:genRemoved ?ctxc_ .

      ?cx_ a ?catc_ OPTION (INFERENCE NONE) .

    } GROUP BY ?x ?cx ?cx_ ?catc ?catc_ ?ctxc_
  }

  FILTER (EXISTS {
    ?x a ?catx OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
    }

    FILTER EXISTS {
      ?x ?p_child ?cx OPTION (INFERENCE NONE) .
      ?cx a ?child_class .
    }

    FILTER (NOT EXISTS {
      ?x a src:ListNode .
    } || (NOT EXISTS {
      ?cx0 src:parent ?x .
      FILTER (?cx0 != ?cx)
    } && EXISTS {
      GRAPH <http://codinuum.com/ont/cpi> {
        ?r owl:minQualifiedCardinality 1 .
      }
    }))

  } || EXISTS {
    ?x a src:TupleNode .
  })

}
}
''' % NS_TBL

Q_RM_RET_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveReturn:", ?fqn) AS ?name)
(?ret AS ?key) (?ctx_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ret ?ctx_ ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ty ?ty_
    WHERE {
      ?ret a java:ReturnStatement ;
           java:inMethod ?meth ;
           chg:removal ?ctx_ .

      ?meth java:fullyQualifiedName ?fqn ;
            java:signature ?sig ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig_ ;
             src:child2 ?ty_ .

    } GROUP BY ?ret ?ctx_ ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ty ?ty_
  }

  ?ty chg:relabeled ?ty_ ;
      src:parent ?meth .

  ?ty_ a java:Void ;
       src:parent ?meth_ .

  FILTER EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?ret ;
       delta:entity2 ?ctx_ .
  }
  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?ty ;
       delta:entity2 ?ty_ .
  }

}
}
''' % NS_TBL

Q_INS_METH_MOVINS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("InsertMethod:", ?fqn_) AS ?name)
(?ctx AS ?key) (?meth_ AS ?key_)
(?ctx AS ?dep) (?meth_ AS ?dep_)
(?ctxc AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?meth_ ?fqn_
    WHERE {
      ?meth_ a java:MethodOrConstructor ;
          java:fullyQualifiedName ?fqn_ ;
          chg:addition ?ctx .

    } GROUP BY ?ctx ?meth_ ?fqn_
  }

  ?cx chg:movedTo ?cx_ .

  ?cx_ java:inMethodOrConstructor ?meth_ ;
       chg:genAdded ?ctxc .

}
}
''' % NS_TBL

Q_ADD_CTOR_ADD_INIT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("InsertConstructor:", ?fqn_) AS ?name)
(?ctx AS ?key) (?ctor_ AS ?key_)
(?ctxa AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?class_ ;
         java:fullyQualifiedName ?fqn_ ;
         chg:addition ?ctx .

  ?field_ a java:FieldDeclaration ;
          java:inTypeDeclaration ?class_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:inField ?field_ ;
          java:name ?fname_ .

  ?a_ a java:AssignmentStatement ;
      java:inConstructor ?ctor_ ;
      src:child0 ?facc_ ;
      chg:addition ?ctxa .

  ?facc_ java:name ?fname_ .

}
}
''' % NS_TBL

Q_WRAP_RET_ADD_EXIT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("WrapReturn:", ?fqn) AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?ctxe AS ?ent) (?exit_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_ ?body_
    WHERE {
      {
        SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_
        WHERE {
          ?meth java:fullyQualifiedName ?fqn ;
                java:signature ?sig ;
                chg:mappedTo ?meth_ .

          ?meth_ java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig_ .

          ?ret a java:ReturnStatement ;
               java:inMethod ?meth ;
               chg:mappedTo ?ret_ .

          ?ret_ a java:ReturnStatement ;
                java:inMethod ?meth_ ;
                src:parent+ ?x_ .

          ?x_ java:inMethod ?meth_ ;
              chg:insertedInto ?ctx .

        } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_
      }

      ?body_ a java:MethodBody ;
             src:parent ?meth_ .

    } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_ ?body_
  }

  ?exit_ a ?cate_ ;
         java:inMethod ?meth_ ;
         src:parent ?body_ ;
         chg:addition ?ctxe .

  FILTER (?cate_ IN (java:ReturnStatement, java:ThrowStatement))

  ?body_ src:children/rdf:rest+ ?b_ .

  ?b_ rdf:first ?throw_ ;
      rdf:rest rdf:nil .

}
}
''' % NS_TBL

Q_ADD_RET_ADD_EXIT_WRAP_RET_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("WrapReturn:", ?fqn) AS ?name)
(?ctxr AS ?ent0) (?ret_ AS ?ent0_)
(?ctxe AS ?ent1) (?exit_ AS ?ent1_)
(?ctx AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_ ?ctxr ?ret_ ?body_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_ ?ctxr ?ret_
        WHERE {

          ?meth java:fullyQualifiedName ?fqn ;
                java:signature ?sig ;
                chg:mappedTo ?meth_ .

          ?meth_ java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig_ .

          ?ret_ a java:ReturnStatement ;
                java:inMethod ?meth_ ;
                src:parent+ ?x_ ;
                chg:addition ?ctxr .

          ?x_ java:inMethod ?meth_ ;
              chg:insertedInto ?ctx .

        } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_ ?ctxr ?ret_
      }

      ?body_ a java:MethodBody ;
             src:parent ?meth_ .

    } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?ctx ?x_ ?ctxr ?ret_ ?body_
  }

  ?exit_ a ?cate_ ;
         java:inMethod ?meth_ ;
         src:parent ?body_ ;
         chg:addition ?ctxe .

  FILTER (?cate_ IN (java:ReturnStatement, java:ThrowStatement))

  ?body_ src:children/rdf:rest+ ?b_ .

  ?b_ rdf:first ?throw_ ;
      rdf:rest rdf:nil .

}
}
''' % NS_TBL

Q_UNWRAP_RET_RM_EXIT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("UnwrapReturn:", ?fqn) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?exit AS ?ent) (?ctxe_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?x ?ctx_ ?body
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?x ?ctx_
        WHERE {

          ?meth java:fullyQualifiedName ?fqn ;
                java:signature ?sig ;
                chg:mappedTo ?meth_ .

          ?meth_ java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig_ .

          ?ret a java:ReturnStatement ;
               java:inMethod ?meth ;
               src:parent+ ?x ;
               chg:mappedTo ?ret_ .

          ?ret_ a java:ReturnStatement ;
                java:inMethod ?meth_ .

          ?x java:inMethod ?meth ;
             chg:removal ?ctx_ .

        } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?x ?ctx_
      }

      ?body a java:MethodBody ;
            src:parent ?meth .

    } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?sig ?sig_ ?x ?ctx_ ?body
  }

  ?exit a ?cate ;
        java:inMethod ?meth ;
        src:parent ?body ;
        chg:removal ?ctxe_ .

  FILTER (?cate IN (java:ReturnStatement, java:ThrowStatement))

  ?body src:children/rdf:rest+ ?b .

  ?b rdf:first ?throw ;
     rdf:rest rdf:nil .

}
}
''' % NS_TBL

Q_ADD_RET_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddReturn:", ?fqn_) AS ?name)
(?ctx AS ?key) (?ret_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        chg:addition ?ctx .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        src:child2 ?ty ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ ;
         src:child2 ?ty_ .

  ?ty a java:Void ;
      src:parent ?meth ;
      chg:relabeled ?ty_ .

  ?ty_ src:parent ?meth_ .

  FILTER EXISTS {
    [] a chg:Insertion ;
       delta:entity1 ?ctx ;
       delta:entity2 ?ret_ .
  }
  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?ty ;
       delta:entity2 ?ty_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETVAL_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnValue:", ?fqn_) AS ?name)
(?e AS ?key) (?e_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?e a java:Expression ;
     src:parent ?ret ;
     chg:relabeled ?e_ .

  ?e_ a java:Expression ;
      src:parent ?ret_ .

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?e ;
       chg:mappedTo ?ret_ .

  ?ret_ a java:ReturnStatement ;
        src:child0 ?e_ ;
        java:inMethod ?meth_ .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        src:child2 ?ty ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ ;
         src:child2 ?ty_ .

  ?ty src:parent ?meth ;
      chg:relabeled ?ty_ .

  ?ty_ src:parent ?meth_ .

}
}
''' % NS_TBL

Q_CHG_RETVAL_DEL_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnValue:", ?sig) AS ?name)
(?val AS ?key) (?val_ AS ?key_)
(?ty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ty src:parent ?meth ;
      java:name ?tyname ;
      chg:removal ?ctx_ .

  ?meth a java:MethodDeclaration ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?sig0 ;
        src:child2 ?ty .

  BIND (CONCAT(?mfqn, ?sig0) AS ?sig)

  ?ret a java:ReturnStatement ;
       src:child0 ?val ;
       java:inMethod ?meth .

  ?val a java:Expression ;
       src:parent ?ret ;
       chg:relabeled ?val_ .

}
}
''' % NS_TBL

Q_CHG_RETVAL_INS_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnValue:", ?sig_) AS ?name)
(?val AS ?key) (?val_ AS ?key_)
(?ctx AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ty_ src:parent ?meth_ ;
        java:name ?tyname_ ;
        chg:addition ?ctx .

  ?meth_ a java:MethodDeclaration ;
          java:fullyQualifiedName ?mfqn_ ;
          java:signature ?sig0_ ;
          src:child2 ?ty_ .

  BIND (CONCAT(?mfqn_, ?sig0_) AS ?sig_)

  ?ret_ a java:ReturnStatement ;
        src:child0 ?val_ ;
        java:inMethod ?meth_ .

  ?val_ a java:Expression ;
        src:parent ?ret_ .

  ?val chg:relabeled ?val_ .

}
}
''' % NS_TBL

Q_MOV__DEL_OR_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT ?x ?x_ ?loc ?loc_ ?cat ?cat_ ?cx ?cx_ ?ctx ?ctx_ ?cat_cx ?cat_cx_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_
    WHERE {
      ?x chg:movedTo ?x_ .

      FILTER EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }

    } GROUP BY ?x ?x_
  }

  OPTIONAL {
    SELECT ?x (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat)
    WHERE {
      ?x a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x
  }
  OPTIONAL {
    SELECT ?x_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_)
    WHERE {
      ?x_ a ?c OPTION (INFERENCE NONE) .
    } GROUP BY ?x_
  }

  {
    SELECT DISTINCT ?x (GROUP_CONCAT(DISTINCT ?loc0; SEPARATOR="|") AS ?loc)
    WHERE {
      ?x src:parent*/src:inFile/src:location ?loc0 .
    } GROUP BY ?x
  }
  {
    SELECT DISTINCT ?x_ (GROUP_CONCAT(DISTINCT ?loc0_; SEPARATOR="|") AS ?loc_)
    WHERE {
      ?x_ src:parent*/src:inFile/src:location ?loc0_ .
    } GROUP BY ?x_
  }

  OPTIONAL {
    ?cx_ src:parent ?x_ ;
         chg:addition ?ctx .
    {
      SELECT ?cx_ (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_cx_)
      WHERE {
        ?cx_ a ?c OPTION (INFERENCE NONE) .
      } GROUP BY ?cx_
    }

    FILTER EXISTS {
      [] a chg:Insertion ;
         delta:entity2 ?cx_ .
    }
    FILTER NOT EXISTS {
      ?cx0 chg:movedTo ?cx_ .
    }
    FILTER NOT EXISTS {#!!!!!GOOD
      ?x_ a src:ListNode .
    }
  }

  OPTIONAL {
    ?cx src:parent ?x ;
         chg:removal ?ctx_ .
    {
      SELECT ?cx (GROUP_CONCAT(DISTINCT STRAFTER(STR(?c), "#"); SEPARATOR="|") AS ?cat_cx)
      WHERE {
        ?cx a ?c OPTION (INFERENCE NONE) .
      } GROUP BY ?cx
    }

    FILTER EXISTS {
      [] a chg:Deletion ;
         delta:entity1 ?cx .
    }
    FILTER NOT EXISTS {
      ?cx chg:movedTo ?cx0_ .
    }
    FILTER NOT EXISTS {#!!!!!GOOD
      ?x_ a src:ListNode .
    }
  }

}
}
''' % NS_TBL

Q_LV_RENAME_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?dtor AS ?ent) (?dtor_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:LocalVariableRename ;
       jref:originalDtor ?dtor ;
       jref:modifiedDtor ?dtor_ .

  ?dtor_ java:inMethodOrConstructor ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .
  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .
}
}
''' % NS_TBL

Q_LV_RENAME_R_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?v AS ?ent) (?v_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:LocalVariableRename ;
       jref:originalVariable ?v ;
       jref:modifiedVariable ?v_ .

  ?v chg:relabeled ?v_ .

  ?v_ java:inMethodOrConstructor ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .
  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .
}
}
''' % NS_TBL

Q_ADD_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?param_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:AddParameter ;
       jref:addedParameter ?param_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?param_ chg:addition ?ctx .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .
  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .
}
}
''' % NS_TBL

Q_ADD_PARAM_I_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?arg_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ref ?sig ?sig_ ?nth_ ?meth_
    WHERE {

      ?ref a jref:AddParameter ;
           jref:addedParameter ?param_ ;
           jref:originalMethod ?meth ;
           jref:modifiedMethod ?meth_ .

      ?param_ src:nth ?nth_ .

      ?meth java:signature ?sig0 ;
            java:fullyQualifiedName ?fqn .

      ?meth_ java:signature ?sig0_ ;
             java:fullyQualifiedName ?fqn_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ref ?sig ?sig_ ?nth_ ?meth_
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?arg_ src:parent ?args_ ;
        src:nth ?nth_ ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_ADD_PARAM_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ivk AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ref ?sig ?sig_ ?nth_ ?meth
    WHERE {

      ?ref a jref:AddParameter ;
           jref:addedParameter ?param_ ;
           jref:originalMethod ?meth ;
           jref:modifiedMethod ?meth_ .

      ?param_ src:nth ?nth_ .

      ?meth java:signature ?sig0 ;
            java:fullyQualifiedName ?fqn .

      ?meth_ java:signature ?sig0_ ;
             java:fullyQualifiedName ?fqn_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ref ?sig ?sig_ ?nth_ ?meth
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_RM_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?param AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:RemoveParameter ;
       jref:removedParameter ?param ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?param chg:removal ?ctx_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .
}
}
''' % NS_TBL

Q_RM_PARAM_D_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?arg AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ref ?sig ?sig_ ?nth ?meth
    WHERE {

      ?ref a jref:RemoveParameter ;
           jref:removedParameter ?param ;
           jref:originalMethod ?meth ;
           jref:modifiedMethod ?meth_ .

      ?param src:nth ?nth .

      ?meth java:signature ?sig0 ;
            java:fullyQualifiedName ?fqn .

      ?meth_ java:signature ?sig0_ ;
             java:fullyQualifiedName ?fqn_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ref ?sig ?sig_ ?nth ?meth
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth .

  ?arg src:parent ?args ;
       src:nth ?nth ;
       chg:removal ?ctx_ .

  ?args a java:Arguments ;
        src:parent ?ivk .

}
}
''' % NS_TBL

Q_RM_PARAM_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ivk AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ref ?sig ?sig_ ?nth ?meth
    WHERE {

      ?ref a jref:RemoveParameter ;
           jref:removedParameter ?param ;
           jref:originalMethod ?meth ;
           jref:modifiedMethod ?meth_ .

      ?param src:nth ?nth .

      ?meth java:signature ?sig0 ;
            java:fullyQualifiedName ?fqn .

      ?meth_ java:signature ?sig0_ ;
             java:fullyQualifiedName ?fqn_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ref ?sig ?sig_ ?nth ?meth
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_RENAME_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?meth AS ?ent) (?meth_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:RenameMethod ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth chg:mappingChange ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .
  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .
}
}
''' % NS_TBL

Q_RENAME_METH_EX_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ivk AS ?ent) (?ivk_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:RenameMethod ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth java:signature ?sig0 ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?meth_ java:signature ?sig0_ ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk java:mayInvokeMethod ?meth ;
       chg:relabeled ?ivk_ .

  ?ivk_ java:mayInvokeMethod ?meth_ .

}
}
''' % NS_TBL

Q_EXTRACT_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?meth_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractMethod ;
       jref:originalMethod ?meth ;
       jref:extractedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth_ chg:addition ?ctx .
}
}
''' % NS_TBL

Q_EXTRACT_METH_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractMethod ;
       jref:originalMethod ?meth ;
       jref:extractedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x_ src:parent+ ?meth_ ;
      chg:addition ?x .
}
}
''' % NS_TBL

Q_EXTRACT_METH_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractMethod ;
       jref:originalMethod ?meth ;
       jref:extractedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x_ src:parent+ ?meth_ .

  ?x chg:removal ?x_ .
}
}
''' % NS_TBL

Q_EXTRACT_METH_M_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractMethod ;
       jref:originalMethod ?meth ;
       jref:extractedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x_ src:parent+ ?meth_ .

  ?x chg:movedTo ?x_ .

  ?x src:parent+ ?meth .

}
}
''' % NS_TBL

Q_EXTRACT_METH_R_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractMethod ;
       jref:originalMethod ?meth ;
       jref:extractedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x_ src:parent+ ?meth_ .

  ?x chg:relabeled ?x_ .

  ?x src:parent+ ?meth .
}
}
''' % NS_TBL

Q_EXTRACT_METH_EX_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?ivk_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractMethod ;
       jref:originalMethod ?meth ;
       jref:extractedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk_ a java:Invocation ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_INLINE_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?meth AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineMethod ;
       jref:inlinedMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_INLINE_METH_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineMethod ;
       jref:inlinedMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x src:parent+ ?meth ;
     chg:removal ?x_ .
}
}
''' % NS_TBL

Q_INLINE_METH_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineMethod ;
       jref:inlinedMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x src:parent+ ?meth .

  ?x_ chg:addition ?x .
}
}
''' % NS_TBL

Q_INLINE_METH_M_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineMethod ;
       jref:inlinedMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x src:parent+ ?meth .

  ?x chg:movedTo ?x_ .

  ?x_ src:parent+ ?meth_ .
}
}
''' % NS_TBL

Q_INLINE_METH_R_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineMethod ;
       jref:inlinedMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x src:parent+ ?meth .

  ?x chg:relabeled ?x_ .

  ?x_ src:parent+ ?meth_ .
}
}
''' % NS_TBL

Q_INLINE_METH_EX_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ivk AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineMethod ;
       jref:inlinedMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth java:signature ?sig0 ;
        java:fullyQualifiedName ?fqn .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk a java:Invocation ;
       java:mayInvokeMethod ?meth ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_PULL_UP_FIELD_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?field_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PullUpField ;
       jref:originalField ?field ;
       jref:movedField ?field_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?field java:name ?fname .
  ?field_ java:name ?fname_ .

  ?class java:fullyQualifiedName ?fqn .
  ?class_ java:fullyQualifiedName ?fqn_ .

  ?field_ chg:addition ?ctx .

  BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)
}
}
''' % NS_TBL

Q_PULL_UP_FIELD_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?field AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PullUpField ;
       jref:originalField ?field ;
       jref:movedField ?field_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?field java:name ?fname .
  ?field_ java:name ?fname_ .

  ?class java:fullyQualifiedName ?fqn .
  ?class_ java:fullyQualifiedName ?fqn_ .

  ?field chg:removal ?ctx_ .

  BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)
}
}
''' % NS_TBL

Q_PUSH_DOWN_FIELD_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?field_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PushDownField ;
       jref:originalField ?field ;
       jref:movedField ?field_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?field java:name ?fname .
  ?field_ java:name ?fname_ .

  ?class java:fullyQualifiedName ?fqn .
  ?class_ java:fullyQualifiedName ?fqn_ .

  ?field_ chg:addition ?ctx .

  BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)
}
}
''' % NS_TBL

Q_PUSH_DOWN_FIELD_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?field AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PushDownField ;
       jref:originalField ?field ;
       jref:movedField ?field_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?field java:name ?fname .
  ?field_ java:name ?fname_ .

  ?class java:fullyQualifiedName ?fqn .
  ?class_ java:fullyQualifiedName ?fqn_ .

  ?field chg:removal ?ctx_ .

  BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)
}
}
''' % NS_TBL

Q_MOVE_FIELD_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?field_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:MoveField ;
       jref:originalField ?field ;
       jref:movedField ?field_ ;
       jref:fromClass ?class ;
       jref:toClass ?class_ .

  ?field java:name ?fname .
  ?field_ java:name ?fname_ .

  ?class java:fullyQualifiedName ?fqn .
  ?class_ java:fullyQualifiedName ?fqn_ .

  ?field_ chg:addition ?ctx .

  BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)
}
}
''' % NS_TBL

Q_MOVE_FIELD_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?field AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:MoveField ;
       jref:originalField ?field ;
       jref:movedField ?field_ ;
       jref:fromClass ?class ;
       jref:toClass ?class_ .

  ?field java:name ?fname .
  ?field_ java:name ?fname_ .

  ?class java:fullyQualifiedName ?fqn .
  ?class_ java:fullyQualifiedName ?fqn_ .

  ?field chg:removal ?ctx_ .

  BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)
}
}
''' % NS_TBL

Q_MOVE_FIELD_EX_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?acc_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ref ?tdecl_ ?fname_ ?tyname_ ?sig_ ?sig0_ ?ver_
    WHERE {

      ?ref a jref:MoveField ;
           jref:originalField ?field ;
           jref:movedField ?field_ ;
           jref:fromClass ?class ;
           jref:toClass ?class_ .

      ?field java:name ?fname .
      ?field_ java:name ?fname_ .

      ?class java:fullyQualifiedName ?fqn ;
             ver:version ?ver .

      ?class_ java:fullyQualifiedName ?fqn_ ;
              ver:version ?ver_ .

      ?tdecl_ java:subClassOf* ?class_ ;
              java:fullyQualifiedName ?tyname_ ;
              ver:version ?ver_ .

      BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)
      BIND(CONCAT(?tyname_, ".", ?fname_) AS ?sig0_)

    } GROUP BY ?ref ?tdecl_ ?fname_ ?tyname_ ?sig_ ?sig0_ ?ver_
  }

  {
    ?acc_ a java:FieldAccess ;
          java:name ?fname_ ;
          java:inTypeDeclaration ?tdecl_ ;
          chg:addition ?ctx .

    FILTER (EXISTS {
      [] a java:This ;
         src:parent ?acc_ .
    } || NOT EXISTS {
      [] src:parent ?acc_ .
    })
  }
  UNION
  {
    ?acc_ a java:FieldAccess ;
          java:inTypeDeclaration/ver:version ?ver_ ;
          java:name ?fname_ ;
          src:child0 ?e_ ;
          chg:addition ?ctx .

    ?e_ a java:Expression ;
        java:ofReferenceType/java:fullyQualifiedName ?tyname_ .
  }
  UNION
  {
    ?acc_ a java:Name ;
          java:inTypeDeclaration/ver:version ?ver_ ;
          java:name ?sig0_ ;
          chg:addition ?ctx .
  }

}
}
''' % NS_TBL

Q_MOVE_FIELD_EX_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?acc AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ref ?tdecl ?fname ?tyname ?sig_ ?sig0 ?ver
    WHERE {

      ?ref a jref:MoveField ;
           jref:originalField ?field ;
           jref:movedField ?field_ ;
           jref:fromClass ?class ;
           jref:toClass ?class_ .

      ?field java:name ?fname .
      ?field_ java:name ?fname_ .

      ?class java:fullyQualifiedName ?fqn ;
             ver:version ?ver .

      ?class_ java:fullyQualifiedName ?fqn_ ;
              ver:version ?ver_ .

      ?tdecl java:subClassOf* ?class ;
              java:fullyQualifiedName ?tyname ;
              ver:version ?ver .

      BIND(CONCAT(?fqn_, ".", ?fname_) AS ?sig_)

      BIND(CONCAT(?tyname, ".", ?fname) AS ?sig0)

    } GROUP BY ?ref ?tdecl ?fname ?tyname ?sig_ ?sig0 ?ver
  }

  {
    ?acc a java:FieldAccess ;
         java:name ?fname ;
         java:inTypeDeclaration ?tdecl ;
         chg:removal ?ctx_ .

    FILTER (EXISTS {
      [] a java:This ;
         src:parent ?acc .
    } || NOT EXISTS {
      [] src:parent ?acc .
    })
  }
  UNION
  {
    ?acc a java:FieldAccess ;
         java:inTypeDeclaration/ver:version ?ver ;
         java:name ?fname ;
         src:child0 ?e ;
         chg:removal ?ctx_ .

    ?e a java:Expression ;
       java:ofReferenceType/java:fullyQualifiedName ?tyname .
  }
  UNION
  {
    ?acc a java:Name ;
         java:inTypeDeclaration/ver:version ?ver ;
         java:name ?sig0 ;
         chg:removal ?ctx_ .
  }

}
}
''' % NS_TBL

Q_PULL_UP_METH_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?meth_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PullUpMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth_ chg:addition ?ctx .
}
}
''' % NS_TBL

Q_PULL_UP_METH_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?meth AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PullUpMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_PUSH_DOWN_METH_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?meth_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PushDownMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth_ chg:addition ?ctx .
}
}
''' % NS_TBL

Q_PUSH_DOWN_METH_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?meth AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PushDownMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_MOVE_METH_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?meth_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:MoveMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:fromClass ?class ;
       jref:toClass ?class_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth_ chg:addition ?ctx .
}
}
''' % NS_TBL

Q_MOVE_METH_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?meth AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:MoveMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:fromClass ?class ;
       jref:toClass ?class_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?meth chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_MOVE_METH_EX_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?ivk_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:MoveMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:fromClass ?class ;
       jref:toClass ?class_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk_ a java:Invocation ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_MOVE_METH_EX_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ivk AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:MoveMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:fromClass ?class ;
       jref:toClass ?class_ .

  ?meth java:signature ?sig0 ;
        java:fullyQualifiedName ?fqn .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk a java:Invocation ;
       java:mayInvokeMethod ?meth ;
       chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_MOVE_METH_EX_R_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ivk AS ?ent) (?ivk_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:MoveMethod ;
       jref:originalMethod ?meth ;
       jref:movedMethod ?meth_ ;
       jref:fromClass ?class ;
       jref:toClass ?class_ .

  ?meth java:signature ?sig0 ;
        java:fullyQualifiedName ?fqn .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk a java:Invocation ;
       chg:relabeled ?ivk_ .

  {
    ?ivk java:mayInvokeMethod ?meth .
  }
  UNION
  {
    ?ivk_ java:mayInvokeMethod ?meth_ .
  }

}
}
''' % NS_TBL

Q_IEV_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?vdtor_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractVariable ;
       jref:extractedVariable ?var_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?var_ java:declaredBy ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
         chg:addition ?ctx .
}
}
''' % NS_TBL

Q_IEV_I2_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?decl_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractVariable ;
       jref:extractedVariable ?var_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?var_ java:declaredBy ?vdtor_ .

  ?vdtor_ src:parent ?decl_ .

  ?decl_ chg:addition ?ctx .
}
}
''' % NS_TBL

Q_IEV_I3_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractVariable ;
       jref:originalContext ?ctx ;
       jref:modifiedContext ?ctx_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x_ src:parent ?ctx_ ;
      chg:addition ?ctx .
}
}
''' % NS_TBL

Q_IEV_M_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?expr AS ?ent) (?expr_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:ExtractVariable ;
       jref:originalExpr ?expr ;
       jref:movedExpr ?expr_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?expr chg:movedTo ?expr_ .
}
}
''' % NS_TBL

# Q_IEV_I_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# PREFIX ref: <%(ref_ns)s>
# PREFIX jref: <%(jref_ns)s>
# SELECT DISTINCT ?ref (?ctx AS ?ent) (?vdtor_ AS ?ent_) ?sig_
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   ?ref a jref:IntroduceExplainingVariable ;
#        jref:introducedVariable ?var_ ;
#        jref:originalMethod ?meth ;
#        jref:modifiedMethod ?meth_ .

#   ?meth_ java:signature ?sig0_ ;
#          java:fullyQualifiedName ?fqn_ .

#   BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

#   ?var_ java:declaredBy ?vdtor_ .

#   ?vdtor_ a java:VariableDeclarator ;
#          chg:addition ?ctx .
# }
# }
# ''' % NS_TBL

# Q_IEV_I2_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# PREFIX ref: <%(ref_ns)s>
# PREFIX jref: <%(jref_ns)s>
# SELECT DISTINCT ?ref (?ctx AS ?ent) (?decl_ AS ?ent_) ?sig_
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   ?ref a jref:IntroduceExplainingVariable ;
#        jref:introducedVariable ?var_ ;
#        jref:originalMethod ?meth ;
#        jref:modifiedMethod ?meth_ .

#   ?meth_ java:signature ?sig0_ ;
#          java:fullyQualifiedName ?fqn_ .

#   BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

#   ?var_ java:declaredBy ?vdtor_ .

#   ?vdtor_ src:parent ?decl_ .

#   ?decl_ chg:addition ?ctx .
# }
# }
# ''' % NS_TBL

# Q_IEV_I3_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# PREFIX ref: <%(ref_ns)s>
# PREFIX jref: <%(jref_ns)s>
# SELECT DISTINCT ?ref (?ctx AS ?ent) (?x_ AS ?ent_) ?sig_
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   ?ref a jref:IntroduceExplainingVariable ;
#        jref:originalContext ?ctx ;
#        jref:modifiedContext ?ctx_ ;
#        jref:originalMethod ?meth ;
#        jref:modifiedMethod ?meth_ .

#   ?meth_ java:signature ?sig0_ ;
#          java:fullyQualifiedName ?fqn_ .

#   BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

#   ?x_ src:parent ?ctx_ ;
#       chg:addition ?ctx .
# }
# }
# ''' % NS_TBL

# Q_IEV_M_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# PREFIX ref: <%(ref_ns)s>
# PREFIX jref: <%(jref_ns)s>
# SELECT DISTINCT ?ref (?expr AS ?ent) (?expr_ AS ?ent_) ?sig_
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   ?ref a jref:IntroduceExplainingVariable ;
#        jref:originalExpr ?expr ;
#        jref:movedExpr ?expr_ ;
#        jref:originalMethod ?meth ;
#        jref:modifiedMethod ?meth_ .

#   ?meth_ java:signature ?sig0_ ;
#          java:fullyQualifiedName ?fqn_ .

#   BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

#   ?expr chg:movedTo ?expr_ .
# }
# }
# ''' % NS_TBL

Q_INLINE_TEMP_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?vdtor AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineTemp ;
       jref:eliminatedVariable ?var ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?var java:declaredBy ?vdtor .

  ?vdtor a java:VariableDeclarator ;
         chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_INLINE_TEMP_D2_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?decl AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineTemp ;
       jref:eliminatedVariable ?var ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?var java:declaredBy ?vdtor .

  ?vdtor src:parent ?decl .

  ?decl chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_INLINE_TEMP_D3_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?ctx_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineTemp ;
       jref:originalContext ?ctx ;
       jref:modifiedContext ?ctx_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?x src:parent ?ctx ;
     chg:removal ?ctx_ .
}
}
''' % NS_TBL

Q_INLINE_TEMP_M_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?expr AS ?ent) (?expr_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineTemp ;
       jref:originalExpr ?expr ;
       jref:movedExpr ?expr_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?expr chg:movedTo ?expr_ .
}
}
''' % NS_TBL

Q_INLINE_TEMP_M2_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?x AS ?ent) (?x_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:InlineTemp ;
       jref:eliminatedVariable ?var ;
       jref:originalExpr ?expr ;
       jref:movedExpr ?expr_ ;
       jref:originalMethod ?meth ;
       jref:modifiedMethod ?meth_ .

  ?meth_ java:signature ?sig0_ ;
         java:fullyQualifiedName ?fqn_ .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?expr chg:mappedTo [] .
  [] chg:mappedTo ?expr_ .

  ?var src:parent ?x .

  ?x chg:movedTo ?x_ .

}
}
''' % NS_TBL

Q_PULL_UP_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT ?ref (?ctx AS ?ent) (?ivk_ AS ?ent_) ?sig_
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ref a jref:PullUpConstructorBody ;
       jref:originalCtor ?ctor ;
       jref:modifiedCtor ?ctor_ ;
       jref:originalClass ?class ;
       jref:modifiedClass ?class_ .

  ?ivk_ a java:SuperInvocation ;
        java:inConstructor ?ctor_ ;
        chg:addition ?ctx .
}
}
''' % NS_TBL


Q_ADD_TD_PUBLIC_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?ctx AS ?key) (?pub_ AS ?key_)
(?ctx AS ?dep) (?pub_ AS ?dep_)
(?ctxi AS ?ent) (?import_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?pub_ ?fqn_ ?ver_
    WHERE {
      ?pub_ a java:Public ;
            src:parent/src:parent/src:parent ?tdecl_ ;
            chg:addition ?ctx .

      ?tdecl_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:fullyQualifiedName ?fqn_ .

    } GROUP BY ?ctx ?pub_ ?fqn_ ?ver_
  }

  {
    SELECT DISTINCT ?ctxi ?import_ ?n ?ver_
    WHERE {
      ?import_ a java:ImportDeclaration ;
               src:parent/src:parent/src:inFile/ver:version ?ver_ ;
               chg:addition ?ctxi ;
               java:name ?n .
    } GROUP BY ?ctxi ?import_ ?n ?ver_
  }

  FILTER (?fqn_ = ?n)

}
}
''' % NS_TBL

Q_ADD_IMPORT_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddImport:", ?iname_) AS ?name)
(?ctx AS ?key) (?import_ AS ?key_)
(?ctx AS ?dep) (?import_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import_ ?iname_ ?cu_ ?ctx
    WHERE {

      ?import_ a java:ImportDeclaration ;
               a ?cat_ OPTION (INFERENCE NONE) ;
               java:name ?iname_ ;
               src:parent/src:parent ?cu_ ;
               chg:addition ?ctx .

      ?cu_ a java:CompilationUnit .

      FILTER (?cat_ IN (java:SingleStaticImportDeclaration, java:SingleTypeImportDeclaration))

    } GROUP BY ?import_ ?iname_ ?cu_ ?ctx
  }

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      src:parent+ ?cu_ ;
      java:name ?xname_ ;
      chg:addition ?ctxx .

  FILTER (?x_ != ?import_)

  FILTER (?iname_ = ?xname_ ||
          STRSTARTS(?xname_, CONCAT(?iname_, ".")) ||
          STRENDS(?iname_, CONCAT(".", ?xname_)) ||
          ?iname_ = STR(REPLACE(?xname_, "[$$]", ".")) ||
          STRSTARTS(STR(REPLACE(?xname_, "[$$]", ".")), ?iname_)
          )

}
}
''' % NS_TBL

Q_RM_IMPORT_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveImport:", ?iname_) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?import AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?iname ?cu ?ctx_
    WHERE {

      ?import a java:ImportDeclaration ;
              a ?cat OPTION (INFERENCE NONE) ;
              java:name ?iname ;
              src:parent/src:parent ?cu ;
              chg:removal ?ctx_ .

      ?cu a java:CompilationUnit .

      FILTER (?cat IN (java:SingleStaticImportDeclaration, java:SingleTypeImportDeclaration))

    } GROUP BY ?import ?iname ?cu ?ctx_
  }

  ?x a ?cat OPTION (INFERENCE NONE) ;
     src:parent+ ?cu ;
     java:name ?xname ;
     chg:removal ?ctxx_ .

  FILTER (?x != ?import)

  FILTER (?iname = ?xname ||
          STRSTARTS(?xname, CONCAT(?iname, ".")) ||
          STRENDS(?iname, CONCAT(".", ?xname)) ||
          ?iname = STR(REPLACE(?xname, "[$$]", ".")) ||
          STRSTARTS(STR(REPLACE(?xname, "[$$]", ".")), ?iname)
          )

}
}
''' % NS_TBL

Q_RM_IMPORT_RM_FILE_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveImport:", ?iname_) AS ?name)
(?import AS ?dep) (?ctxi_ AS ?dep_)
(?file AS ?ent) (?ctxf_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?iname ?cu ?ctxi_ ?v
    WHERE {

      ?import a java:SingleTypeImportDeclaration ;
              java:name ?iname ;
              src:parent/src:parent ?cu ;
              chg:removal ?ctxi_ .

      ?cu a java:CompilationUnit ;
          src:inFile/ver:version ?v .

    } GROUP BY ?import ?iname ?cu ?ctxi_ ?v
  }

  ?tdecl a java:TypeDeclaration ;
         src:inFile ?file .

  ?file a src:File ;
        ver:version ?v ;
        chg:removal ?ctxf_ .

  {
    ?tdecl java:fullyQualifiedName ?iname .
  }
  UNION
  {
    ?tdecl java:fullyQualifiedName ?xname .
    FILTER (STRSTARTS(?xname, CONCAT(?iname, ".")))
  }
  UNION
  {
    ?tdecl java:fullyQualifiedName ?xname .
    FILTER ((?iname = STR(REPLACE(?xname, "[$$]", "."))))
  }
  UNION
  {
    ?tdecl java:fullyQualifiedName ?xname .
    FILTER (STRSTARTS(STR(REPLACE(?xname, "[$$]", ".")), ?iname))
  }

}
}
''' % NS_TBL

Q_ADD_IMPORT_ADD_FILE_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddImport:", ?iname_) AS ?name)
(?ctxf AS ?dep) (?file_ AS ?dep_)
(?ctxi AS ?ent) (?import_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import_ ?iname_ ?cu_ ?ctxi ?v_
    WHERE {

      ?import_ a java:SingleTypeImportDeclaration ;
               java:name ?iname_ ;
               src:parent/src:parent ?cu_ ;
               chg:addition ?ctxi .

      ?cu_ a java:CompilationUnit ;
           src:inFile/ver:version ?v_ .

    } GROUP BY ?import_ ?iname_ ?cu_ ?ctxi ?v_
  }

  ?tdecl_ a java:TypeDeclaration ;
          src:inFile ?file_ .

  ?file_ a src:File ;
         ver:version ?v_ ;
         chg:addition ?ctxf .

  {
    ?tdecl_ java:fullyQualifiedName ?iname_ .
  }
  UNION
  {
    ?tdecl_ java:fullyQualifiedName ?xname_ .
    FILTER (STRSTARTS(?xname_, CONCAT(?iname_, ".")))
  }
  UNION
  {
    ?tdecl_ java:fullyQualifiedName ?xname_ .
    FILTER ((?iname_ = STR(REPLACE(?xname_, "[$$]", "."))))
  }
  UNION
  {
    ?tdecl_ java:fullyQualifiedName ?xname_ .
    FILTER (STRSTARTS(STR(REPLACE(?xname_, "[$$]", ".")), ?iname_))
  }

}
}
''' % NS_TBL

Q_RM_IMPORT_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveImport:", ?iname_) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?import AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?iname ?cu ?ctx_
    WHERE {

      ?import a java:ImportDeclaration ;
              a ?cat OPTION (INFERENCE NONE) ;
              java:name ?iname ;
              src:parent/src:parent ?cu ;
              chg:removal ?ctx_ .

      ?cu a java:CompilationUnit .

      FILTER (?cat IN (java:SingleStaticImportDeclaration, java:SingleTypeImportDeclaration))

    } GROUP BY ?import ?iname ?cu ?ctx_
  }

  ?x a ?cat OPTION (INFERENCE NONE) ;
     src:parent+ ?cu ;
     java:name ?xname ;
     chg:relabeled ?x_ .

  FILTER (?x != ?import)

  FILTER (?iname = ?xname ||
          STRSTARTS(?xname, CONCAT(?iname, ".")) ||
          STRENDS(?iname, CONCAT(".", ?xname)) ||
          ?iname = STR(REPLACE(?xname, "[$$]", ".")) ||
          STRSTARTS(STR(REPLACE(?xname, "[$$]", ".")), ?iname)
          )

}
}
''' % NS_TBL

Q_ADD_IMPORT_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddImport:", ?iname_) AS ?name)
(?ctx AS ?key) (?import_ AS ?key_)
(?ctx AS ?dep) (?import_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import_ ?iname_ ?cu_ ?ctx
    WHERE {

      ?import_ a java:ImportDeclaration ;
               a ?cat_ OPTION (INFERENCE NONE) ;
               java:name ?iname_ ;
               src:parent/src:parent ?cu_ ;
               chg:addition ?ctx .

      ?cu_ a java:CompilationUnit .

      FILTER (?cat_ IN (java:SingleStaticImportDeclaration, java:SingleTypeImportDeclaration))

    } GROUP BY ?import_ ?iname_ ?cu_ ?ctx
  }

  ?x a ?cat OPTION (INFERENCE NONE) ;
     chg:relabeled ?x_ .

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      src:parent+ ?cu_ ;
      java:name ?xname_ .

  FILTER (?x_ != ?import_)

  FILTER (?iname_ = ?xname_ ||
          STRSTARTS(?xname_, CONCAT(?iname_, ".")) ||
          STRENDS(?iname_, CONCAT(".", ?xname_)) ||
          ?iname_ = STR(REPLACE(?xname_, "[$$]", ".")) ||
          STRSTARTS(STR(REPLACE(?xname_, "[$$]", ".")), ?iname_)
          )

}
}
''' % NS_TBL

Q_RM_IMPORT_ADD_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddImport:", ?iname_) AS ?name)
(?ctx AS ?key) (?import_ AS ?key_)
(?ctx AS ?dep) (?import_ AS ?dep_)
(?import AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    {
      SELECT DISTINCT ?import ?iname ?cu ?ctx_ ?cu_
      WHERE {

        ?import a java:TypeImportOnDemandDeclaration ;
                java:name ?iname ;
                src:parent/src:parent ?cu ;
                chg:removal ?ctx_ .

        ?cu a java:CompilationUnit ;
            chg:mappedTo ?cu_ .

      } GROUP BY ?import ?iname ?cu ?ctx_ ?cu_
    }

    ?import_ a java:SingleTypeImportDeclaration ;
             java:name ?iname_ ;
             src:parent/src:parent ?cu_ ;
             chg:addition ?ctx .

    FILTER (STRSTARTS(?iname_, CONCAT(?iname, ".")))
  }
  UNION
  {
    {
      SELECT DISTINCT ?import ?iname ?cu ?ctx_ ?cu_
      WHERE {

        ?import a java:SingleTypeImportDeclaration ;
                java:name ?iname ;
                src:parent/src:parent ?cu ;
                chg:removal ?ctx_ .

        ?cu a java:CompilationUnit ;
            chg:mappedTo ?cu_ .

      } GROUP BY ?import ?iname ?cu ?ctx_ ?cu_
    }

    ?import_ a java:TypeImportOnDemandDeclaration ;
             java:name ?iname_ ;
             src:parent/src:parent ?cu_ ;
             chg:addition ?ctx .

    FILTER (STRSTARTS(?iname, CONCAT(?iname_, ".")))
  }

}
}
''' % NS_TBL

Q_RM_IMPORT_CHG_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddImport:", ?iname_) AS ?name)
(?import AS ?key) (?import_ AS ?key_)
(?import AS ?dep) (?import_ AS ?dep_)
(?import0 AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    {
      SELECT DISTINCT ?import0 ?iname ?cu ?ctx_ ?cu_
      WHERE {

        ?import0 a java:TypeImportOnDemandDeclaration ;
                 java:name ?iname ;
                 src:parent/src:parent ?cu ;
                 chg:removal ?ctx_ .

        ?cu a java:CompilationUnit ;
            chg:mappedTo ?cu_ .

      } GROUP BY ?import0 ?iname ?cu ?ctx_ ?cu_
    }

    ?import chg:relabeled ?import_ .

    ?import_ a java:SingleTypeImportDeclaration ;
             java:name ?iname_ ;
             src:parent/src:parent ?cu_ .

    FILTER (STRSTARTS(?iname_, CONCAT(?iname, ".")))
  }
  UNION
  {
    {
      SELECT DISTINCT ?import0 ?iname ?cu ?ctx_ ?cu_
      WHERE {

        ?import0 a java:SingleTypeImportDeclaration ;
                 java:name ?iname ;
                 src:parent/src:parent ?cu ;
                 chg:removal ?ctx_ .

        ?cu a java:CompilationUnit ;
            chg:mappedTo ?cu_ .

      } GROUP BY ?import0 ?iname ?cu ?ctx_ ?cu_
    }

    ?import chg:relabeled ?import_ .

    ?import_ a java:TypeImportOnDemandDeclaration ;
             java:name ?iname_ ;
             src:parent/src:parent ?cu_ .

    FILTER (STRSTARTS(?iname, CONCAT(?iname_, ".")))
  }

}
}
''' % NS_TBL

Q_CHG_IMPORT_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeImport:", ?iname_) AS ?name)
(?import AS ?key) (?import_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?import_ ?x ?x_
    WHERE {

      {
        SELECT DISTINCT ?import ?import_ ?cu ?cu_ ?x ?x_
        WHERE {

          {
            SELECT DISTINCT ?import ?import_ ?cu ?cu_
            WHERE {

              ?import a java:SingleTypeImportDeclaration ;
                      src:parent/src:parent ?cu ;
                      chg:relabeled ?import_ .

              ?import_ a java:SingleTypeImportDeclaration ;
                       src:parent/src:parent ?cu_ .

              ?cu a java:CompilationUnit ;
                  chg:mappedTo ?cu_ .

              ?cu_ a java:CompilationUnit .

            } GROUP BY ?import ?import_ ?cu ?cu_
          }

          ?x #a ?cat OPTION (INFERENCE NONE) ;
             src:parent+ ?cu ;
             chg:relabeled ?x_ .

        } GROUP BY ?import ?import_ ?cu ?cu_ ?x ?x_
      }

      ?x_ #a ?cat_ OPTION (INFERENCE NONE) ;
          src:parent+ ?cu_ .

      FILTER (?x != ?import)
      FILTER (?x_ != ?import_)

    } GROUP BY ?import ?import_ ?x ?x_
  }

  ?import java:name ?iname .
  ?import_ java:name ?iname_ .

  {
    ?x java:name ?xname .

    FILTER (?iname = ?xname ||
            STRSTARTS(?xname, CONCAT(?iname, ".")) ||
            STRENDS(?iname, CONCAT(".", ?xname)) ||
            ?iname = STR(REPLACE(?xname, "[$$]", ".")) ||
            STRSTARTS(STR(REPLACE(?xname, "[$$]", ".")), ?iname)
            )
  }
  UNION
  {
    ?x_ java:name ?xname_ .

    FILTER (?iname_ = ?xname_ ||
            STRSTARTS(?xname_, CONCAT(?iname_, ".")) ||
            STRENDS(?iname_, CONCAT(".", ?xname_)) ||
            ?iname_ = STR(REPLACE(?xname_, "[$$]", ".")) ||
            STRSTARTS(STR(REPLACE(?xname_, "[$$]", ".")), ?iname_)
            )
  }

}
}
''' % NS_TBL

Q_CHG_IMPORT_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeImport:", ?iname_) AS ?name)
(?import AS ?key) (?import_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?import_ ?iname ?iname_ ?cu ?cu_
    WHERE {

      ?import a java:SingleTypeImportDeclaration ;
              java:name ?iname ;
              src:parent/src:parent ?cu ;
              chg:relabeled ?import_ .

      ?import_ a java:SingleTypeImportDeclaration ;
               java:name ?iname_ ;
               src:parent/src:parent ?cu_ .

      ?cu a java:CompilationUnit ;
          chg:mappedTo ?cu_ .

      ?cu_ a java:CompilationUnit .

    } GROUP BY ?import ?import_ ?iname ?iname_ ?cu ?cu_
  }

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      src:parent+ ?cu_ ;
      java:name ?xname_ ;
      chg:addition ?ctx .

  FILTER (?x_ != ?import_)

  FILTER (?iname_ = ?xname_ ||
          STRSTARTS(?xname_, CONCAT(?iname_, ".")) ||
          STRENDS(?iname_, CONCAT(".", ?xname_)) ||
          ?iname_ = STR(REPLACE(?xname_, "[$$]", ".")) ||
          STRSTARTS(STR(REPLACE(?xname_, "[$$]", ".")), ?iname_)
          )

}
}
''' % NS_TBL

Q_CHG_IMPORT_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeImport:", ?iname_) AS ?name)
(?import AS ?key) (?import_ AS ?key_)
(?x AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?import_ ?iname ?iname_ ?cu ?cu_
    WHERE {

      ?import a java:SingleTypeImportDeclaration ;
              java:name ?iname ;
              src:parent/src:parent ?cu ;
              chg:relabeled ?import_ .

      ?import_ a java:SingleTypeImportDeclaration ;
               java:name ?iname_ ;
               src:parent/src:parent ?cu_ .

      ?cu a java:CompilationUnit ;
          chg:mappedTo ?cu_ .

      ?cu_ a java:CompilationUnit .

    } GROUP BY ?import ?import_ ?iname ?iname_ ?cu ?cu_
  }

  ?x a ?cat OPTION (INFERENCE NONE) ;
     src:parent+ ?cu ;
     java:name ?xname ;
     chg:removal ?ctx_ .

  FILTER (?x != ?import)

  FILTER (?iname = ?xname ||
          STRSTARTS(?xname, CONCAT(?iname, ".")) ||
          STRENDS(?iname, CONCAT(".", ?xname)) ||
          ?iname = STR(REPLACE(?xname, "[$$]", ".")) ||
          STRSTARTS(STR(REPLACE(?xname, "[$$]", ".")), ?iname)
          )

}
}
''' % NS_TBL

Q_ADD_FD_PUBLIC_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn) AS ?name)
(?ctx AS ?dep) (?pub_ AS ?dep_)
(?ctxf AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?pub_ ?fqn ?vdtor_
    WHERE {
      ?pub_ a java:Public ;
            src:parent/src:parent ?fdecl_ ;
            chg:addition ?ctx .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration/ver:version ?ver_ ;
              src:child2 ?vdtor_ ;
              java:fullyQualifiedName ?fqn .

    } GROUP BY ?ctx ?pub_ ?fqn ?vdtor_
  }

  ?facc_ java:declaredBy ?vdtor_ ;
         chg:addition ?ctxf .

  {
    ?facc_ a java:FieldAccess ;
           src:child0 ?e_ .

    FILTER NOT EXISTS {
      ?e_ a java:This .
    }
  }
  UNION
  {
    ?facc_ a java:Name .
  }

}
}
''' % NS_TBL

Q_ADD_FD_PUBLIC_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn) AS ?name)
(?ctx AS ?dep) (?pub_ AS ?dep_)
(?facc AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?pub_ ?fqn ?vdtor_
    WHERE {
      ?pub_ a java:Public ;
            src:parent/src:parent ?fdecl_ ;
            chg:addition ?ctx .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration/ver:version ?ver_ ;
              src:child2 ?vdtor_ ;
              java:fullyQualifiedName ?fqn .

    } GROUP BY ?ctx ?pub_ ?fqn ?vdtor_
  }

  ?facc_ java:declaredBy ?vdtor_ ;
         ^chg:relabeled ?facc .

  {
    ?facc_ a java:FieldAccess ;
           src:child0 ?e_ .

    FILTER NOT EXISTS {
      ?e_ a java:This .
    }
  }
  UNION
  {
    ?facc_ a java:Name .
  }

}
}
''' % NS_TBL

Q_ADD_MC_PUBLIC_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?ctx AS ?key) (?pub_ AS ?key_)
(?ctx AS ?dep) (?pub_ AS ?dep_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?pub_ ?mname ?mname_ ?class ?class_ ?fqn_
    WHERE {

      ?pub_ a java:Public ;
            java:inMethodOrConstructor ?meth_ ;
            chg:addition ?ctx .

      ?meth a java:MethodOrConstructor ;
            java:name ?mname ;
            java:inClass ?class ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:inClass ?class_ .

    } GROUP BY ?ctx ?pub_ ?mname ?mname_ ?class ?class_ ?fqn_
  }

  {
    SELECT DISTINCT ?class ?class_ ?extends ?extends_
    WHERE {

      ?class a java:ClassDeclaration ;
             java:name ?cname ;
             chg:mappedTo ?class_ .

      ?class_ a java:ClassDeclaration ;
              java:name ?cname_ .

      ?extends a java:Extends ;
               java:inClass ?class ;
               chg:mappedTo ?extends_ .

      ?extends_ a java:Extends ;
                java:inClass ?class_ .

    } GROUP BY ?class ?class_ ?extends ?extends_
  }

  {
    SELECT DISTINCT ?class ?class_ ?extends ?extends_ ?rty ?rty_
    WHERE {
      ?rty a java:ReferenceType ;
           java:name ?rty_name ;
           src:parent ?extends ;
           chg:relabeled ?rty_ .

      ?rty_ a java:ReferenceType ;
            src:parent ?extends_ ;
            java:name ?rty_name_ .

      ?class java:subClassOf+ ?super_class .
      ?class_ java:subClassOf+ ?super_class_ .

      ?super_class a java:ClassDeclaration ;
                   java:fullyQualifiedName ?rty_name .

      ?super_class_ a java:ClassDeclaration ;
                    java:fullyQualifiedName ?rty_name_ .

      ?super_meth_ a java:MethodOrConstructor ;
                   java:name ?mname_ ;
                   java:inClass ?super_class_ .

      ?protected_ a java:Protected ;
                  java:inMethodOrConstructor ?super_meth_

    } GROUP BY ?class ?class_ ?extends ?extends_ ?rty ?rty_
  }

}
}
''' % NS_TBL

Q_ADD_MC_PUBLIC_ADD_MC_PUBLIC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?ctx1 AS ?dep) (?pub1_ AS ?dep_)
(?ctx0 AS ?ent) (?pub0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx0 ?pub0_ ?mname ?mname_ ?class0 ?class0_ ?fqn0_
    WHERE {

      ?pub0_ a java:Public ;
            java:inMethodOrConstructor ?meth0_ ;
            chg:addition ?ctx0 .

      ?meth0 a java:MethodOrConstructor ;
             java:name ?mname ;
             java:inClass ?class0 ;
             chg:mappedTo ?meth0_ .

      ?meth0_ a java:MethodOrConstructor ;
              java:name ?mname_ ;
              java:fullyQualifiedName ?fqn0_ ;
              java:inClass ?class0_ .

    } GROUP BY ?ctx0 ?pub0_ ?mname ?mname_ ?class0 ?class0_ ?fqn0_
  }

  ?pub1_ a java:Public ;
         java:inMethodOrConstructor ?meth1_ ;
         chg:addition ?ctx1 .

  ?meth1 a java:MethodOrConstructor ;
         java:name ?mname ;
         java:inClass ?class1 ;
         chg:mappedTo ?meth1_ .

  ?meth1_ a java:MethodOrConstructor ;
          java:name ?mname_ ;
          java:fullyQualifiedName ?fqn1_ ;
          java:inClass ?class1_ .

  ?class1 java:subClassOf+ ?class0 .
  ?class1_ java:subClassOf+ ?class0_ .

}
}
''' % NS_TBL

Q_ADD_MC_PROTECTED_ADD_MC_PUBLIC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?ctx1 AS ?dep) (?pub1_ AS ?dep_)
(?ctx0 AS ?ent) (?protected_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx0 ?protected_ ?mname ?mname_ ?class0 ?class0_ ?fqn0_
    WHERE {

      ?protected_ a java:Protected ;
                  java:inMethodOrConstructor ?meth0_ ;
                  chg:addition ?ctx0 .

      ?meth0 a java:MethodOrConstructor ;
             java:name ?mname ;
             java:inClass ?class0 ;
             chg:mappedTo ?meth0_ .

      ?meth0_ a java:MethodOrConstructor ;
              java:name ?mname_ ;
              java:fullyQualifiedName ?fqn0_ ;
              java:inClass ?class0_ .

    } GROUP BY ?ctx0 ?protected_ ?mname ?mname_ ?class0 ?class0_ ?fqn0_
  }

  ?pub1_ a java:Public ;
         java:inMethodOrConstructor ?meth1_ ;
         chg:addition ?ctx1 .

  ?meth1 a java:MethodOrConstructor ;
         java:name ?mname ;
         java:inClass ?class1 ;
         chg:mappedTo ?meth1_ .

  ?meth1_ a java:MethodOrConstructor ;
          java:name ?mname_ ;
          java:fullyQualifiedName ?fqn1_ ;
          java:inClass ?class1_ .

  ?class1 java:subClassOf+ ?class0 .
  ?class1_ java:subClassOf+ ?class0_ .

}
}
''' % NS_TBL

Q_RM_MC_PUBLIC_RM_MC_PUBLIC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?pub0 AS ?dep) (?ctx0_ AS ?dep_)
(?pub1 AS ?ent) (?ctx1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx0_ ?pub0 ?mname ?mname_ ?class0 ?class0_ ?fqn0
    WHERE {

      ?pub0 a java:Public ;
            java:inMethodOrConstructor ?meth0 ;
            chg:removal ?ctx0_ .

      ?meth0_ a java:MethodOrConstructor ;
             java:name ?mname_ ;
             java:inClass ?class0_ ;
             ^chg:mappedTo ?meth0 .

      ?meth0 a java:MethodOrConstructor ;
             java:name ?mname ;
             java:fullyQualifiedName ?fqn0 ;
             java:inClass ?class0 .

    } GROUP BY ?ctx0_ ?pub0 ?mname ?mname_ ?class0 ?class0_ ?fqn0
  }

  ?pub1 a java:Public ;
        java:inMethodOrConstructor ?meth1 ;
        chg:removal ?ctx1_ .

  ?meth1_ a java:MethodOrConstructor ;
          java:name ?mname_ ;
          java:inClass ?class1_ ;
          ^chg:mappedTo ?meth1 .

  ?meth1 a java:MethodOrConstructor ;
         java:name ?mname ;
         java:fullyQualifiedName ?fqn1 ;
         java:inClass ?class1 .

  ?class1 java:subClassOf+ ?class0 .
  ?class1_ java:subClassOf+ ?class0_ .

}
}
''' % NS_TBL

Q_RM_MC_PUBLIC_RM_MC_PROTECTED_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?protected AS ?dep) (?ctx0_ AS ?dep_)
(?pub1 AS ?ent) (?ctx1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx0_ ?protected ?mname ?mname_ ?class0 ?class0_ ?fqn0
    WHERE {

      ?protected a java:Protected ;
                 java:inMethodOrConstructor ?meth0 ;
                 chg:removal ?ctx0_ .

      ?meth0_ a java:MethodOrConstructor ;
             java:name ?mname_ ;
             java:inClass ?class0_ ;
             ^chg:mappedTo ?meth0 .

      ?meth0 a java:MethodOrConstructor ;
             java:name ?mname ;
             java:fullyQualifiedName ?fqn0 ;
             java:inClass ?class0 .

    } GROUP BY ?ctx0_ ?protected ?mname ?mname_ ?class0 ?class0_ ?fqn0
  }

  ?pub1 a java:Public ;
        java:inMethodOrConstructor ?meth1 ;
        chg:removal ?ctx1_ .

  ?meth1_ a java:MethodOrConstructor ;
          java:name ?mname_ ;
          java:inClass ?class1_ ;
          ^chg:mappedTo ?meth1 .

  ?meth1 a java:MethodOrConstructor ;
         java:name ?mname ;
         java:fullyQualifiedName ?fqn1 ;
         java:inClass ?class1 .

  ?class1 java:subClassOf+ ?class0 .
  ?class1_ java:subClassOf+ ?class0_ .

}
}
''' % NS_TBL

Q_MOVE_SWITCH_LABEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX ref: <%(ref_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("MoveSwitchLabel:", ?fqn_) AS ?name)
(?sl AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?sl_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?e a java:Expression ;
     src:parent ?sl ;
     chg:mappedEqTo ?e_ ;
     chg:movedTo ?e_ .

  ?e_ a java:Expression ;
      src:parent ?sl_ .

  ?sl a java:SwitchLabel ;
      java:inStatement ?sw ;
      chg:movedTo ?sl_ ;
      chg:genRemoved ?ctx_ .

  ?sl_ java:inStatement ?sw_ ;
       chg:genAdded ?ctx .

  ?sw a java:SwitchStatement ;
      java:inMethodOrConstructor ?meth ;
      chg:mappedTo ?sw_ .

  ?sw_ a java:SwitchStatement ;
       java:inMethodOrConstructor ?meth_ .

}
}
''' % NS_TBL

Q_ADD_MC_PUBLIC_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?ctx AS ?key) (?pub_ AS ?key_)
(?ctx AS ?dep) (?pub_ AS ?dep_)
(?pctx AS ?ent) (?protected_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?pub_ ?mname ?mname_ ?class ?class_ ?fqn_
    WHERE {

      ?pub_ a java:Public ;
            java:inMethodOrConstructor ?meth_ ;
            chg:addition ?ctx .

      ?meth a java:MethodOrConstructor ;
            java:name ?mname ;
            java:inClass ?class ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:inClass ?class_ .

    } GROUP BY ?ctx ?pub_ ?mname ?mname_ ?class ?class_ ?fqn_
  }

  {
    SELECT DISTINCT ?class ?class_ ?extends ?extends_
    WHERE {

      ?class a java:ClassDeclaration ;
             java:name ?cname ;
             chg:mappedTo ?class_ .

      ?class_ a java:ClassDeclaration ;
              java:name ?cname_ .

      ?extends a java:Extends ;
               java:inClass ?class ;
               chg:mappedTo ?extends_ .

      ?extends_ a java:Extends ;
                java:inClass ?class_ .

    } GROUP BY ?class ?class_ ?extends ?extends_
  }

  ?rty a java:ReferenceType ;
       java:name ?rty_name ;
       src:parent ?extends ;
       chg:mappedTo ?rty_ .

  ?rty_ a java:ReferenceType ;
        src:parent ?extends_ ;
        java:name ?rty_name_ .

  {
    SELECT DISTINCT ?class ?class_ ?rty_name ?rty_name_ ?mname_ ?pctx ?protected_
    WHERE {
      ?class java:subClassOf+ ?super_class .
      ?class_ java:subClassOf+ ?super_class_ .

      ?super_class a java:ClassDeclaration ;
                   java:fullyQualifiedName ?rty_name .

      ?super_class_ a java:ClassDeclaration ;
                    java:fullyQualifiedName ?rty_name_ .

      ?super_meth_ a java:MethodOrConstructor ;
                   java:name ?mname_ ;
                   java:inClass ?super_class_ .

      ?protected_ a java:Protected ;
                  java:inMethodOrConstructor ?super_meth_ ;
                  chg:addition ?pctx .

    } GROUP BY ?class ?class_ ?rty_name ?rty_name_ ?mname_ ?pctx ?protected_
  }

}
}
''' % NS_TBL

Q_ADD_MC_PUBLIC_CHG_AC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPublic:", ?fqn_) AS ?name)
(?ctx AS ?key) (?pub_ AS ?key_)
(?ctx AS ?dep) (?pub_ AS ?dep_)
(?a AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?pub_ ?mname ?mname_ ?class ?class_ ?fqn_
    WHERE {

      ?pub_ a java:Public ;
            java:inMethodOrConstructor ?meth_ ;
            chg:addition ?ctx .

      ?meth a java:MethodOrConstructor ;
            java:name ?mname ;
            java:inClass ?class ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:inClass ?class_ .

    } GROUP BY ?ctx ?pub_ ?mname ?mname_ ?class ?class_ ?fqn_
  }

  ?a a java:Modifier ;
     chg:relabeled ?a_ .

  ?a_ a java:Modifier ;
      java:inMethodOrConstructor ?meth0_ .

  FILTER EXISTS {
    ?a_ a java:Public .
  }

  ?meth0 a java:MethodOrConstructor ;
         java:name ?mname ;
         java:inTypeDeclaration ?tdecl ;
         chg:mappedTo ?meth0_ .

  ?meth0_ a java:MethodOrConstructor ;
          java:name ?mname_ ;
          java:inTypeDeclaration ?tdecl_ .

  ?tdecl chg:mappedTo ?tdecl_ .

  ?class java:subClassOf+ ?tdecl .
  ?class_ java:subClassOf+ ?tdecl_ .

}
}
''' % NS_TBL

Q_CHG_M_ABST_INS_BODY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstract:", ?fqn) AS ?name)
(?abst AS ?key) (?a_ AS ?key_)
(?ctx AS ?ent) (?body_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?abst a java:Abstract ;
        java:inMethod ?meth ;
        chg:relabeled ?a_ .

  ?meth a java:MethodDeclaration ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodDeclaration ;
         java:name ?mname_ .

  ?body_ a java:MethodBody ;
         java:inMethod ?meth_ ;
         chg:addition ?ctx .

}
}
''' % NS_TBL

Q_ADD_M_ABST_DEL_BODY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstract:", ?fqn_) AS ?name)
(?ctx AS ?key) (?abst_ AS ?key_)
(?body AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?abst_ a java:Abstract ;
         java:inMethod ?meth_ ;
         chg:addition ?ctx .

  ?meth_ a java:MethodDeclaration ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?fqn_ .

  ?meth chg:mappedTo ?meth_ .

  ?body a java:MethodBody ;
        java:inMethod ?meth ;
        chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_M_ABST_DEL_BODY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstract:", ?fqn_) AS ?name)
(?mod AS ?key) (?abst_ AS ?key_)
(?body AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?abst_ a java:Abstract ;
         java:inMethod ?meth_ ;
         ^chg:relabeled ?mod .

  ?meth_ a java:MethodDeclaration ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?fqn_ .

  ?meth chg:mappedTo ?meth_ .

  ?body a java:MethodBody ;
        java:inMethod ?meth ;
        chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_M_ABST_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstract:", ?sig) AS ?name)
(?ctx AS ?ent) (?abst_ AS ?ent_)
(?meth0 AS ?dep) (?meth0_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?abst_ ?ctx ?mname ?mname_ ?tdecl ?tdecl_ ?sig ?sig_
    WHERE {
      ?abst_ a java:Abstract ;
             java:inMethod ?meth_ ;
             chg:addition ?ctx .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0_ ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig)

    } GROUP BY ?abst_ ?ctx ?mname ?mname_ ?tdecl ?tdecl_ ?sig ?sig_
  }

  ?tdecl0_ a java:TypeDeclaration ;
           java:subTypeOf+ ?tdecl_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          java:name ?mname_ .

  ?meth0 a java:MethodDeclaration ;
         chg:relabeled ?meth0_ .

  FILTER NOT EXISTS {
    ?abst0_ a java:Abstract ;
            java:inMethod ?meth0_ .
  }

}
}
''' % NS_TBL

Q_CHG_METH_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?meth0 AS ?dep) (?meth0_ AS ?dep_)
(?ctxr AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0 ?tdecl2_ ?rty1_ ?ctxr
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ ;
                  ^chg:relabeled ?meth0 .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             chg:addition ?ctxr .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0 ?tdecl2_ ?rty1_ ?ctxr
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_CHG_OVERRIDE_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeOverride:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?override AS ?key) (?override_ AS ?key_)
(?ctxr AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?tdecl2_ ?rty1_ ?ctxr ?override ?override_
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?override ?override_
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ .

          ?override_ a java:MarkerAnnotation ;
                     java:name "Override" ;
                     java:inMethod ?meth0_ ;
                     ^chg:relabeled ?override .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?override ?override_
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             chg:addition ?ctxr .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?tdecl2_ ?rty1_ ?ctxr ?override ?override_
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_CHG_METH_CHG_SUPERTY_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?meth0 AS ?dep) (?meth0_ AS ?dep_)
(?rty1 AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0 ?tdecl2_ ?rty1_ ?rty1
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ ;
                  ^chg:relabeled ?meth0 .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             ^chg:relabeled ?rty1 .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?meth0 ?tdecl2_ ?rty1_ ?rty1
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_CHG_OVERRIDE_CHG_SUPERTY_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeOverride:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?override AS ?key) (?override_ AS ?key_)
(?rty1 AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?tdecl2_ ?rty1_ ?rty1 ?override ?override_
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?override ?override_
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ .

          ?override_ a java:MarkerAnnotation ;
                     java:name "Override" ;
                     java:inMethod ?meth0_ ;
                     ^chg:relabeled ?override .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?override ?override_
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             ^chg:relabeled ?rty1 .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?tdecl2_ ?rty1_ ?rty1 ?override ?override_
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_ADD_METH_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?ctxm AS ?dep) (?meth0_ AS ?dep_)
(?ctxr AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?ctxr
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ ;
                  chg:addition ?ctxm .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             chg:addition ?ctxr .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?ctxr
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_ADD_OVERRIDE_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddOverride:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?ctxm AS ?key) (?override_ AS ?key_)
(?ctxr AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?ctxr ?override_
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?override_
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ .

          ?override_ a java:MarkerAnnotation ;
                     java:name "Override" ;
                     java:inMethod ?meth0_ ;
                     chg:addition ?ctxm .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?override_
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             chg:addition ?ctxr .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?ctxr ?override_
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_ADD_METH_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?ctxm AS ?dep) (?meth0_ AS ?dep_)
(?rty1 AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?rty1
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ ;
                  chg:addition ?ctxm .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             ^chg:relabeled ?rty1 .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?rty1
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_ADD_OVERRIDE_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddOverride:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?ctxm AS ?key) (?override_ AS ?key_)
(?rty1 AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?rty1 ?override_
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?override_
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ ;
                  chg:addition ?ctxm .

          ?override_ a java:MarkerAnnotation ;
                     java:name "Override" ;
                     java:inMethod ?meth0_ ;
                     chg:addition ?ctxm .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?override_
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             java:refersToDeclaration ?tdecl2_ ;
             src:parent ?super1_ ;
             ^chg:relabeled ?rty1 .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?tdecl2_ ?rty1_ ?rty1 ?override_
  }

  ?tdecl2_ a java:TypeDeclaration ;
           java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf* ?tdecl_ .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:name ?mname_ ;
         java:signature ?sig0_ .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth_ .
  } || EXISTS {
    ?tdecl_ a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_CHG_METH_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?dep) (?ctxr_ AS ?dep_)
(?meth0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_ ?tdecl2 ?rty1 ?ctxr_
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 ;
                 chg:relabeled ?meth0_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:removal ?ctxr_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_ ?tdecl2 ?rty1 ?ctxr_
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_CHG_OVERRIDE_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeOverride:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?key) (?ctxr_ AS ?key_)
(?override AS ?ent) (?override_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?tdecl2 ?rty1 ?ctxr_ ?override ?override_
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?override ?override_
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 .

          ?override a java:MarkerAnnotation ;
                    java:name "Override" ;
                    java:inMethod ?meth0 ;
                    chg:relabeled ?override_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?override ?override_
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:removal ?ctxr_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?tdecl2 ?rty1 ?ctxr_ ?override ?override_
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_CHG_METH_CHG_SUPERTY_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?dep) (?rty1_ AS ?dep_)
(?meth0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_ ?tdecl2 ?rty1 ?rty1_
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 ;
                 chg:relabeled ?meth0_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:relabeled ?rty1_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?meth0_ ?tdecl2 ?rty1 ?rty1_
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_CHG_OVERRIDE_CHG_SUPERTY_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeOverride:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?key) (?rty1_ AS ?key_)
(?override AS ?ent) (?override_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?tdecl2 ?rty1 ?rty1_ ?override ?override_
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?override ?override_
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 .

          ?override a java:MarkerAnnotation ;
                    java:name "Override" ;
                    java:inMethod ?meth0 ;
                    chg:relabeled ?override_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?override ?override_
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:relabeled ?rty1_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?tdecl2 ?rty1 ?rty1_ ?override ?override_
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_RM_METH_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?dep) (?ctxr_ AS ?dep_)
(?meth0 AS ?ent) (?ctxm_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?ctxr_
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 ;
                 chg:removal ?ctxm_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:removal ?ctxr_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?ctxr_
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_RM_OVERRIDE_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveOverride:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?key) (?ctxr_ AS ?key_)
(?override AS ?ent) (?ctxm_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?ctxr_ ?override
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?override
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 .

          ?override a java:MarkerAnnotation ;
                    java:name "Override" ;
                    java:inMethod ?meth0 ;
                    chg:removal ?ctxm_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?override
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:removal ?ctxr_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?ctxr_ ?override
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_RM_METH_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?dep) (?rty1_ AS ?dep_)
(?meth0 AS ?ent) (?ctxm_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?rty1_
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 ;
                 chg:removal ?ctxm_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:relabeled ?rty1_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?rty1_
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

Q_RM_OVERRIDE_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveOverride:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?key) (?rty1_ AS ?key_)
(?override AS ?ent) (?ctxm_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?rty1_ ?override
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?override
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 .

          ?override a java:MarkerAnnotation ;
                    java:name "Override" ;
                    java:inMethod ?meth0 ;
                    chg:removal ?ctxm_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?override
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            java:refersToDeclaration ?tdecl2 ;
            src:parent ?super1 ;
            chg:relabeled ?rty1_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?tdecl2 ?rty1 ?rty1_ ?override
  }

  ?tdecl2 a java:TypeDeclaration ;
          java:fullyQualifiedName ?cfqn ;
          java:subTypeOf* ?tdecl .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:name ?mname ;
        java:signature ?sig0 .

  FILTER (EXISTS {
    [] a java:Abstract ;
       java:inMethod ?meth .
  } || EXISTS {
    ?tdecl a java:InterfaceDeclaration .
  })

}
}
''' % NS_TBL

# Q_ADD_METH_ADD_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# SELECT DISTINCT
# (CONCAT("AddMethod:", ?sig) AS ?name)
# (?ctx AS ?ent) (?import_ AS ?ent_)
# (?ctx0 AS ?dep) (?meth0_ AS ?dep_)
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   {
#     SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctx0 ?file_ ?ver_ ?loc_
#     WHERE {

#       ?meth0_ a java:MethodDeclaration ;
#               java:inTypeDeclaration ?tdecl0_ ;
#               java:name ?mname_ ;
#               java:signature ?sig0_ ;
#               chg:addition ?ctx0 .

#       ?tdecl0_ src:inFile ?file_ .

#       ?file_ a src:File ;
#              src:location ?loc_ ;
#              ver:version ?ver_ .

#     } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctx0 ?file_ ?ver_ ?loc_
#   }

#   ?meth_ a java:MethodDeclaration ;
#          java:inTypeDeclaration ?tdecl_ ;
#          java:name ?mname_ ;
#          java:signature ?sig0_ .

#   ?tdecl_ a java:TypeDeclaration ;
#           ver:version ?ver_ ;
#           java:fullyQualifiedName ?cfqn_ .

#   FILTER (EXISTS {
#     [] a java:Abstract ;
#        java:inMethod ?meth_ .
#   } || EXISTS {
#     ?tdecl_ a java:InterfaceDeclaration .
#   })

#   ?tdecl0_ java:subTypeOf+ ?tdecl_ .

#   ?import_ a java:ImportDeclaration ;
#            src:parent/src:parent/src:inFile ?file_ ;
#            java:name ?iname_ ;
#            chg:addition ?ctx .

#   FILTER ((?iname_ = ?cfqn_) || (?iname_ = STR(REPLACE(?cfqn_, "[$$]", "."))))

# }
# }
# ''' % NS_TBL

# Q_ADD_METH_CHG_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# SELECT DISTINCT
# (CONCAT("AddMethod:", ?sig) AS ?name)
# (?import AS ?ent) (?import_ AS ?ent_)
# (?ctx0 AS ?dep) (?meth0_ AS ?dep_)
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   {
#     SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctx0 ?file_ ?ver_ ?loc_
#     WHERE {

#       ?meth0_ a java:MethodDeclaration ;
#               java:inTypeDeclaration ?tdecl0_ ;
#               java:name ?mname_ ;
#               java:signature ?sig0_ ;
#               chg:addition ?ctx0 .

#       ?tdecl0_ src:inFile ?file_ .

#       ?file_ a src:File ;
#              src:location ?loc_ ;
#              ver:version ?ver_ .

#     } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctx0 ?file_ ?ver_ ?loc_
#   }

#   ?meth_ a java:MethodDeclaration ;
#          java:inTypeDeclaration ?tdecl_ ;
#          java:name ?mname_ ;
#          java:signature ?sig0_ .

#   ?tdecl_ a java:TypeDeclaration ;
#           ver:version ?ver_ ;
#           java:fullyQualifiedName ?cfqn_ .

#   FILTER (EXISTS {
#     [] a java:Abstract ;
#        java:inMethod ?meth_ .
#   } || EXISTS {
#     ?tdecl_ a java:InterfaceDeclaration .
#   })

#   ?tdecl0_ java:subTypeOf+ ?tdecl_ .

#   ?import a java:ImportDeclaration ;
#           chg:relabeled ?import_ .

#   ?import_ a java:ImportDeclaration ;
#            src:parent/src:parent/src:inFile ?file_ ;
#            java:name ?iname_ .

#   FILTER ((?iname_ = ?cfqn_) || (?iname_ = STR(REPLACE(?cfqn_, "[$$]", "."))))

# }
# }
# ''' % NS_TBL

# Q_RM_METH_CHG_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# SELECT DISTINCT
# (CONCAT("RemoveMethod:", ?sig) AS ?name)
# (?import AS ?dep) (?import_ AS ?dep_)
# (?meth0 AS ?ent) (?ctx0_ AS ?ent_)
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   {
#     SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctx0_ ?file ?ver ?loc
#     WHERE {

#       ?meth0 a java:MethodDeclaration ;
#              java:inTypeDeclaration ?tdecl0 ;
#              java:name ?mname ;
#              java:signature ?sig0 ;
#              chg:removal ?ctx0_ .

#       ?tdecl0 src:inFile ?file .

#       ?file a src:File ;
#             src:location ?loc ;
#             ver:version ?ver .

#     } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctx0_ ?file ?ver ?loc
#   }

#   ?meth a java:MethodDeclaration ;
#         java:inTypeDeclaration ?tdecl ;
#         java:name ?mname ;
#         java:signature ?sig0 .

#   ?tdecl a java:TypeDeclaration ;
#          ver:version ?ver ;
#          java:fullyQualifiedName ?cfqn .

#   FILTER (EXISTS {
#     [] a java:Abstract ;
#        java:inMethod ?meth .
#   } || EXISTS {
#     ?tdecl a java:InterfaceDeclaration .
#   })

#   ?tdecl0 java:subTypeOf+ ?tdecl .

#   ?import a java:ImportDeclaration ;
#           src:parent/src:parent/src:inFile ?file ;
#           java:name ?iname ;
#           chg:relabeled ?import_ .

#   FILTER ((?iname = ?cfqn) || (?iname = STR(REPLACE(?cfqn, "[$$]", "."))))

# }
# }
# ''' % NS_TBL

# Q_RM_METH_RM_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# SELECT DISTINCT
# (CONCAT("RemoveMethod:", ?sig) AS ?name)
# (?import AS ?dep) (?ctx_ AS ?dep_)
# (?meth0 AS ?ent) (?ctx0_ AS ?ent_)
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   {
#     SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctx0_ ?file ?ver ?loc
#     WHERE {

#       ?meth0 a java:MethodDeclaration ;
#              java:inTypeDeclaration ?tdecl0 ;
#              java:name ?mname ;
#              java:signature ?sig0 ;
#              chg:removal ?ctx0_ .

#       ?tdecl0 src:inFile ?file .

#       ?file a src:File ;
#             src:location ?loc ;
#             ver:version ?ver .

#     } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctx0_ ?file ?ver ?loc
#   }

#   ?meth a java:MethodDeclaration ;
#         java:inTypeDeclaration ?tdecl ;
#         java:name ?mname ;
#         java:signature ?sig0 .

#   ?tdecl a java:TypeDeclaration ;
#          ver:version ?ver ;
#          java:fullyQualifiedName ?cfqn .

#   FILTER (EXISTS {
#     [] a java:Abstract ;
#        java:inMethod ?meth .
#   } || EXISTS {
#     ?tdecl a java:InterfaceDeclaration .
#   })

#   ?tdecl0 java:subTypeOf+ ?tdecl .

#   ?import a java:ImportDeclaration ;
#           src:parent/src:parent/src:inFile ?file ;
#           java:name ?iname ;
#           chg:removal ?ctx_ .

#   FILTER ((?iname = ?cfqn) || (?iname = STR(REPLACE(?cfqn, "[$$]", "."))))

# }
# }
# ''' % NS_TBL

Q_RM_METH_ADD_PTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?meth0 AS ?ent) (?ctx_ AS ?ent_)
(?ctxp AS ?dep) (?pty1_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mname ?tdecl ?tdecl_ ?sig ?sig0 ?tdecl0 ?tdecl0_ ?meth0 ?ctx_
    WHERE {

      {
        SELECT DISTINCT ?mname ?tdecl ?tdecl_ ?sig ?sig0
        WHERE {

          ?meth a java:MethodDeclaration ;
                java:inTypeDeclaration ?tdecl ;
                java:name ?mname ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodDeclaration ;
                 java:inTypeDeclaration ?tdecl_ ;
                 java:name ?mname ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0 .

          BIND (CONCAT(?fqn, ?sig0) AS ?sig)

          FILTER (EXISTS {
            ?abst a java:Abstract ;
                  java:inMethod ?meth .
          } || EXISTS {
            ?tdecl a java:InterfaceDeclaration .
          })

        } GROUP BY ?mname ?mname_ ?tdecl ?tdecl_ ?sig ?sig0
      }

      ?tdecl0 a java:TypeDeclaration ;
              java:subTypeOf+ ?tdecl ;
              chg:mappedTo ?tdecl0_ .

      ?meth0 a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl0 ;
             java:name ?mname ;
             java:signature ?sig0 ;
             chg:removal ?ctx_ .

    } GROUP BY ?mname ?mname_ ?tdecl ?tdecl_ ?sig ?sig0 ?tdecl0 ?tdecl0_ ?meth0 ?ctx_
  }

  ?meth1 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         java:name ?mname ;
         java:signature ?sig1 ;
         src:child3 ?params1 ;
         chg:mappedTo ?meth1_ .

  ?meth1_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          java:name ?mname ;
          java:signature ?sig0 ;
          src:child3 ?params1_ .

  ?tdecl0_ a java:TypeDeclaration ;
           java:subTypeOf+ ?tdecl_ .

  FILTER (?meth1 != ?meth0)
  FILTER (?sig1 != ?sig0)

  ?params1 a java:Parameters ;
           ?p_param ?param1 ;
           chg:mappedTo ?params1_ .

  ?params1_ a java:Parameters ;
            ?p_param ?param1_ .

  ?param1_ a java:Parameter ;
           src:child1 ?pty_ .

  ?pty1_ a java:Type ;
         src:parent ?param1_ ;
         chg:addition ?ctxp .

}
}
''' % NS_TBL

Q_ADD_METH_RM_PTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?sig) AS ?name)
(?ctx AS ?dep) (?meth0_ AS ?dep_)
(?pty1 AS ?ent) (?ctxp_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mname ?tdecl ?tdecl_ ?sig ?sig0 ?tdecl0 ?tdecl0_ ?meth0_ ?ctx
    WHERE {

      {
        SELECT DISTINCT ?mname ?tdecl ?tdecl_ ?sig ?sig0
        WHERE {

          ?meth a java:MethodDeclaration ;
                java:inTypeDeclaration ?tdecl ;
                java:name ?mname ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodDeclaration ;
                 java:inTypeDeclaration ?tdecl_ ;
                 java:name ?mname ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0 .

          BIND (CONCAT(?fqn, ?sig0) AS ?sig)

          FILTER (EXISTS {
            ?abst a java:Abstract ;
                  java:inMethod ?meth .
          } || EXISTS {
            ?tdecl a java:InterfaceDeclaration .
          })

        } GROUP BY ?mname ?mname_ ?tdecl ?tdecl_ ?sig ?sig0
      }

      ?tdecl0_ a java:TypeDeclaration ;
               java:subTypeOf+ ?tdecl_ .

      ?tdecl0 chg:mappedTo ?tdecl0_ .

      ?meth0_ a java:MethodDeclaration ;
              java:inTypeDeclaration ?tdecl0_ ;
              java:name ?mname ;
              java:signature ?sig0 ;
              chg:addition ?ctx .

    } GROUP BY ?mname ?mname_ ?tdecl ?tdecl_ ?sig ?sig0 ?tdecl0 ?tdecl0_ ?meth0_ ?ctx
  }

  ?meth1 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         java:name ?mname ;
         java:signature ?sig0 ;
         src:child3 ?params1 ;
         chg:mappedTo ?meth1_ .

  ?meth1_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          java:name ?mname ;
          java:signature ?sig1_ ;
          src:child3 ?params1_ .

  ?tdecl0 a java:TypeDeclaration ;
           java:subTypeOf+ ?tdecl .

  FILTER (?meth1_ != ?meth0_)
  FILTER (?sig1_ != ?sig0)

  ?params1 a java:Parameters ;
           ?p_param ?param1 ;
           chg:mappedTo ?params1_ .

  ?params1_ a java:Parameters ;
            ?p_param ?param1_ .

  ?param1 a java:Parameter ;
          src:child1 ?pty .

  ?pty1 a java:Type ;
        src:parent ?param1 ;
        chg:removal ?ctxp_ .

}
}
''' % NS_TBL

Q_RM_M_ABST_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstract:", ?sig) AS ?name)
(?abst AS ?dep) (?ctx_ AS ?dep_)
(?meth0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?abst ?ctx_ ?mname ?mname_ ?tdecl ?tdecl_ ?sig
    WHERE {
      ?abst a java:Abstract ;
            java:inMethod ?meth ;
            chg:removal ?ctx_ .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig)

    } GROUP BY ?abst ?ctx_ ?mname ?mname_ ?tdecl ?tdecl_ ?sig
  }

  ?tdecl0 a java:TypeDeclaration ;
          java:subTypeOf+ ?tdecl .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         java:name ?mname ;
         chg:relabeled ?meth0_ .

  FILTER NOT EXISTS {
    ?abst0 a java:Abstract ;
           java:inMethod ?meth0 .
  }

}
}
''' % NS_TBL

Q_ADD_ABS_METH_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstractMethod:", ?mfqn_, ".", "?msig_") AS ?name)
(?ctx0 AS ?dep) (?meth0_ AS ?dep_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
    WHERE {

      ?meth_ a java:MethodDeclaration ;
             java:name ?mname_ ;
             java:signature ?msig_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:inTypeDeclaration ?tdecl_ ;
             chg:addition ?ctx .

      ?tdecl_ a java:TypeDeclaration ;
              java:name ?tname_ ;
              ^chg:mappedTo ?tdecl .

      FILTER (EXISTS {
        ?meth_ src:child0 ?mods_ .
        [] a java:Abstract ;
           src:parent ?mods_ .
      } || EXISTS {
        ?tdecl_ a java:InterfaceDeclaration .
      })

    } GROUP BY ?ctx ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
  }

  ?class_ a java:TypeDeclaration ;
          java:name ?cname_ ;
          java:subTypeOf* ?tdecl_ .

  ?meth0_ a java:MethodDeclaration ;
          src:child5 ?mbody_ ;
          java:name ?mname_ ;
          java:signature ?msig_ ;
          java:fullyQualifiedName ?mfqn0_ ;
          chg:addition ?ctx0 .

  FILTER (EXISTS {
    ?meth0_ java:inClass ?class_ .
  } || EXISTS {
    ?meth0_ java:inInstanceCreation/java:ofReferenceType ?class_ .
  })

  FILTER NOT EXISTS {
    ?tdecl_ a [] .
    ?class_ java:subClassOf+ ?c_ .
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?tdecl_ .
    [] a java:MethodDeclaration ;
       src:child5 ?mb_ ;
       java:inClass ?c_ ;
       java:signature ?msig_ ;
       java:name ?mname_ .
  }

  # FILTER NOT EXISTS {
  #   ?c_ a java:ClassDeclaration ;
  #       java:subClassOf+ ?class_ .
  #   [] a java:MethodDeclaration ;
  #      src:child5 ?mb_ ;
  #      java:inClass ?c_ ;
  #      java:signature ?msig_ ;
  #      java:name ?mname_ .
  # }

}
}
''' % NS_TBL

Q_ADD_ABS_METH_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstractMethod:", ?mfqn_, ".", "?msig_") AS ?name)
(?meth0 AS ?dep) (?meth0_ AS ?dep_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
    WHERE {

      ?meth_ a java:MethodDeclaration ;
             java:name ?mname_ ;
             java:signature ?msig_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:inTypeDeclaration ?tdecl_ ;
             chg:addition ?ctx .

      ?tdecl_ a java:TypeDeclaration ;
              java:name ?tname_ ;
              ^chg:mappedTo ?tdecl .

      FILTER (EXISTS {
        ?meth_ src:child0 ?mods_ .
        [] a java:Abstract ;
           src:parent ?mods_ .
      } || EXISTS {
        ?tdecl_ a java:InterfaceDeclaration .
      })

    } GROUP BY ?ctx ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
  }

  ?class_ a java:TypeDeclaration ;
          java:name ?cname_ ;
          java:subTypeOf* ?tdecl_ .

  ?meth0_ a java:MethodDeclaration ;
          src:child5 ?mbody_ ;
          java:name ?mname_ ;
          java:signature ?msig_ ;
          java:fullyQualifiedName ?mfqn0_ ;
          ^chg:relabeled ?meth0 .

  FILTER (EXISTS {
    ?meth0_ java:inClass ?class_ .
  } || EXISTS {
    ?meth0_ java:inInstanceCreation/java:ofReferenceType ?class_ .
  })

  FILTER NOT EXISTS {
    ?tdecl_ a [] .
    ?class_ java:subClassOf+ ?c_ .
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?tdecl_ .
    [] a java:MethodDeclaration ;
       src:child5 ?mb_ ;
       java:inClass ?c_ ;
       java:signature ?msig_ ;
       java:name ?mname_ .
  }

  FILTER NOT EXISTS {
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?class_ .
    [] a java:MethodDeclaration ;
       src:child5 ?mb_ ;
       java:inClass ?c_ ;
       java:signature ?msig_ ;
       java:name ?mname_ .
  }

}
}
''' % NS_TBL

Q_CHG_ABS_METH_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstractMethod:", ?mfqn_, ".", "?msig_") AS ?name)
(?ctx0 AS ?dep) (?meth0_ AS ?dep_)
(?meth AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
    ?class_ ?cname_ ?meth0_ ?mfqn0_ ?ctx0
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
        WHERE {

          ?meth_ a java:MethodDeclaration ;
                 java:name ?mname_ ;
                 java:signature ?msig_ ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:inTypeDeclaration ?tdecl_ ;
                 ^chg:relabeled ?meth .

          ?tdecl_ a java:TypeDeclaration ;
                  java:name ?tname_ ;
                  ^chg:mappedTo ?tdecl .

          FILTER (EXISTS {
            ?meth_ src:child0 ?mods_ .
            [] a java:Abstract ;
               src:parent ?mods_ .
          } || EXISTS {
            ?tdecl_ a java:InterfaceDeclaration .
          })

        } GROUP BY ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
      }

      ?class_ a java:TypeDeclaration ;
              java:name ?cname_ ;
              java:subTypeOf* ?tdecl_ .

      ?meth0_ a java:MethodDeclaration ;
              src:child5 ?mbody_ ;
              java:name ?mname_ ;
              java:signature ?msig_ ;
              java:fullyQualifiedName ?mfqn0_ ;
              chg:addition ?ctx0 .

      FILTER (EXISTS {
        ?meth0_ java:inClass ?class_ .
      } || EXISTS {
        ?meth0_ java:inInstanceCreation/java:ofReferenceType ?class_ .
      })

    } GROUP BY ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
    ?class_ ?cname_ ?meth0_ ?mfqn0_ ?ctx0
  }

  FILTER NOT EXISTS {
    ?tdecl_ a [] .
    ?class_ java:subClassOf+ ?c_ .
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?tdecl_ .
    [] a java:MethodDeclaration ;
       src:child5 ?mb_ ;
       java:inClass ?c_ ;
       java:signature ?msig_ ;
       java:name ?mname_ .
  }

  FILTER NOT EXISTS {
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?class_ .
    [] a java:MethodDeclaration ;
       src:child5 ?mb_ ;
       java:inClass ?c_ ;
       java:signature ?msig_ ;
       java:name ?mname_ .
  }

}
}
''' % NS_TBL

Q_CHG_ABS_METH_CHG_METH_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangebstractMethod:", ?mfqn_, ".", "?msig_") AS ?name)
(?meth0 AS ?dep) (?meth0_ AS ?dep_)
(?meth AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
    ?class_ ?cname_ ?meth0_ ?mfqn0_ ?meth0
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
        WHERE {

          ?meth_ a java:MethodDeclaration ;
                 java:name ?mname_ ;
                 java:signature ?msig_ ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:inTypeDeclaration ?tdecl_ ;
                 ^chg:relabeled ?meth .

          ?tdecl_ a java:TypeDeclaration ;
                  java:name ?tname_ ;
                  ^chg:mappedTo ?tdecl .

          FILTER (EXISTS {
            ?meth_ src:child0 ?mods_ .
            [] a java:Abstract ;
               src:parent ?mods_ .
          } || EXISTS {
            ?tdecl_ a java:InterfaceDeclaration .
          })

        } GROUP BY ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
      }

      ?class_ a java:TypeDeclaration ;
              java:name ?cname_ ;
              java:subTypeOf* ?tdecl_ .

      ?meth0_ a java:MethodDeclaration ;
              src:child5 ?mbody_ ;
              java:name ?mname_ ;
              java:signature ?msig_ ;
              java:fullyQualifiedName ?mfqn0_ ;
              ^chg:relabeled ?meth0 .

      FILTER (EXISTS {
        ?meth0_ java:inClass ?class_ .
      } || EXISTS {
        ?meth0_ java:inInstanceCreation/java:ofReferenceType ?class_ .
      })

    } GROUP BY ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
    ?class_ ?cname_ ?meth0_ ?mfqn0_ ?meth0
  }

  FILTER NOT EXISTS {
    ?tdecl_ a [] .
    ?class_ java:subClassOf+ ?c_ .
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?tdecl_ .
    [] a java:MethodDeclaration ;
       src:child5 ?mb_ ;
       java:inClass ?c_ ;
       java:signature ?msig_ ;
       java:name ?mname_ .
  }

  FILTER NOT EXISTS {
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?class_ .
    [] a java:MethodDeclaration ;
       src:child5 ?mb_ ;
       java:inClass ?c_ ;
       java:signature ?msig_ ;
       java:name ?mname_ .
  }

}
}
''' % NS_TBL

Q_RM_ABS_METH_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstractMethod:", ?mfqn, "?msig") AS ?name)
(?meth AS ?dep) (?ctx_ AS ?dep_)
(?meth0 AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:name ?mname ;
            java:signature ?msig ;
            java:fullyQualifiedName ?mfqn ;
            java:inTypeDeclaration ?tdecl ;
            chg:removal ?ctx_ .

      ?tdecl a java:TypeDeclaration ;
             java:name ?tname ;
             chg:mappedTo ?tdecl_ .

      FILTER (EXISTS {
        ?meth src:child0 ?mods .
        [] a java:Abstract ;
           src:parent ?mods .
      } || EXISTS {
        ?tdecl a java:InterfaceDeclaration .
      })

    } GROUP BY ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
  }

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         java:subTypeOf* ?tdecl .

  ?meth0 a java:MethodDeclaration ;
         src:child5 ?mbody ;
         java:name ?mname ;
         java:signature ?msig ;
         java:fullyQualifiedName ?mfqn0 ;
         chg:removal ?ctx0_ .

  FILTER (EXISTS {
    ?meth0 java:inClass ?class .
  } || EXISTS {
    ?meth0 java:inInstanceCreation/java:ofReferenceType ?class .
  })

  FILTER NOT EXISTS {
    ?tdecl a [] .
    ?class java:subClassOf+ ?c .
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?tdecl .
    [] a java:MethodDeclaration ;
       src:child5 ?mb ;
       java:inClass ?c ;
       java:signature ?msig ;
       java:name ?mname .
  }

  # FILTER NOT EXISTS {
  #   ?c a java:ClassDeclaration ;
  #      java:subClassOf+ ?class .
  #   [] a java:MethodDeclaration ;
  #      src:child5 ?mb ;
  #      java:inClass ?c ;
  #      java:name ?mname .
  #      java:signature ?msig ;
  # }

}
}
''' % NS_TBL

Q_RM_ABS_METH_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstractMethod:", ?mfqn, "?msig") AS ?name)
(?meth AS ?dep) (?ctx_ AS ?dep_)
(?meth0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:name ?mname ;
            java:signature ?msig ;
            java:fullyQualifiedName ?mfqn ;
            java:inTypeDeclaration ?tdecl ;
            chg:removal ?ctx_ .

      ?tdecl a java:TypeDeclaration ;
             java:name ?tname ;
             chg:mappedTo ?tdecl_ .

      FILTER (EXISTS {
        ?meth src:child0 ?mods .
        [] a java:Abstract ;
           src:parent ?mods .
      } || EXISTS {
        ?tdecl a java:InterfaceDeclaration .
      })

    } GROUP BY ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
  }

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         java:subTypeOf* ?tdecl .

  ?meth0 a java:MethodDeclaration ;
         src:child5 ?mbody ;
         java:name ?mname ;
         java:signature ?msig ;
         java:fullyQualifiedName ?mfqn0 ;
         chg:relabeled ?meth0_ .

  FILTER (EXISTS {
    ?meth0 java:inClass ?class .
  } || EXISTS {
    ?meth0 java:inInstanceCreation/java:ofReferenceType ?class .
  })

  FILTER NOT EXISTS {
    ?tdecl a [] .
    ?class java:subClassOf+ ?c .
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?tdecl .
    [] a java:MethodDeclaration ;
       src:child5 ?mb ;
       java:inClass ?c ;
       java:signature ?msig ;
       java:name ?mname .
  }

  FILTER NOT EXISTS {
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?class .
    [] a java:MethodDeclaration ;
       src:child5 ?mb ;
       java:inClass ?c ;
       java:signature ?msig ;
       java:name ?mname .
  }

}
}
''' % NS_TBL

Q_CHG_ABS_METH_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstractMethod:", ?mfqn, "?msig") AS ?name)
(?meth AS ?dep) (?meth_ AS ?dep_)
(?meth0 AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:name ?mname ;
            java:signature ?msig ;
            java:fullyQualifiedName ?mfqn ;
            java:inTypeDeclaration ?tdecl ;
            chg:relabeled ?meth_ .

      ?tdecl a java:TypeDeclaration ;
             java:name ?tname ;
             chg:mappedTo ?tdecl_ .

      FILTER (EXISTS {
        ?meth src:child0 ?mods .
        [] a java:Abstract ;
           src:parent ?mods .
      } || EXISTS {
        ?tdecl a java:InterfaceDeclaration .
      })

    } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
  }

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         java:subTypeOf* ?tdecl .

  ?meth0 a java:MethodDeclaration ;
         src:child5 ?mbody ;
         java:name ?mname ;
         java:signature ?msig ;
         java:fullyQualifiedName ?mfqn0 ;
         chg:removal ?ctx0_ .

  FILTER (EXISTS {
    ?meth0 java:inClass ?class .
  } || EXISTS {
    ?meth0 java:inInstanceCreation/java:ofReferenceType ?class .
  })

  FILTER NOT EXISTS {
    ?tdecl a [] .
    ?class java:subClassOf+ ?c .
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?tdecl .
    [] a java:MethodDeclaration ;
       src:child5 ?mb ;
       java:inClass ?c ;
       java:signature ?msig ;
       java:name ?mname .
  }

  FILTER NOT EXISTS {
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?class .
    [] a java:MethodDeclaration ;
       src:child5 ?mb ;
       java:inClass ?c ;
       java:signature ?msig ;
       java:name ?mname .
  }

}
}
''' % NS_TBL

Q_CHG_ABS_METH_CHG_METH_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstractMethod:", ?mfqn, "?msig") AS ?name)
(?meth AS ?dep) (?meth_ AS ?dep_)
(?meth0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:name ?mname ;
            java:signature ?msig ;
            java:fullyQualifiedName ?mfqn ;
            java:inTypeDeclaration ?tdecl ;
            chg:relabeled ?meth_ .

      ?tdecl a java:TypeDeclaration ;
             java:name ?tname ;
             chg:mappedTo ?tdecl_ .

      FILTER (EXISTS {
        ?meth src:child0 ?mods .
        [] a java:Abstract ;
           src:parent ?mods .
      } || EXISTS {
        ?tdecl a java:InterfaceDeclaration .
      })

    } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
  }

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         java:subTypeOf* ?tdecl .

  ?meth0 a java:MethodDeclaration ;
         src:child5 ?mbody ;
         java:name ?mname ;
         java:signature ?msig ;
         java:fullyQualifiedName ?mfqn0 ;
         chg:relabeled ?meth0_ .

  FILTER (EXISTS {
    ?meth0 java:inClass ?class .
  } || EXISTS {
    ?meth0 java:inInstanceCreation/java:ofReferenceType ?class .
  })

  FILTER NOT EXISTS {
    ?tdecl a [] .
    ?class java:subClassOf+ ?c .
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?tdecl .
    [] a java:MethodDeclaration ;
       src:child5 ?mb ;
       java:inClass ?c ;
       java:signature ?msig ;
       java:name ?mname .
  }

  FILTER NOT EXISTS {
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?class .
    [] a java:MethodDeclaration ;
       src:child5 ?mb ;
       java:inClass ?c ;
       java:signature ?msig ;
       java:name ?mname .
  }

}
}
''' % NS_TBL

Q_CHG_ABS_METH_RETTY_CHG_METH_RETTY_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstractMethodReturnType:", ?mfqn, "?msig") AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?ty ?ty_
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:name ?mname ;
            java:signature ?msig ;
            java:fullyQualifiedName ?mfqn ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:name ?mname_ ;
             java:signature ?msig_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?ty_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?tdecl a java:TypeDeclaration ;
             chg:mappedTo ?tdecl_ .

      FILTER (EXISTS {
        ?meth src:child0 ?mods .
        [] a java:Abstract ;
           src:parent ?mods .
      } || EXISTS {
        ?tdecl a java:InterfaceDeclaration .
      })

    } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?ty ?ty_
  }

  ?class a java:TypeDeclaration ;
         java:subTypeOf* ?tdecl .

  ?meth0 a java:MethodDeclaration ;
         src:child5 [] ;
         java:name ?mname ;
         java:fullyQualifiedName ?mfqn0 ;
         java:signature ?msig ;
         src:child2 ?ty0 ;
         chg:mappedTo ?meth0_ .

  ?ty0 a java:Type ;
       chg:relabeled ?ty0_ .

  FILTER (EXISTS {
    ?meth0 java:inClass ?class .
  } || EXISTS {
    ?meth0 java:inInstanceCreation/java:ofReferenceType ?class .
  })

  FILTER NOT EXISTS {
    ?tdecl a [] .
    ?class java:subClassOf+ ?c .
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?tdecl .
    [] a java:MethodDeclaration ;
       src:child5 [] ;
       java:inClass ?c ;
       java:name ?mname .
  }

  FILTER NOT EXISTS {
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?class .
    [] a java:MethodDeclaration ;
       src:child5 [] ;
       java:inClass ?c ;
       java:name ?mname .
  }

}
}
''' % NS_TBL

Q_CHG_ABS_METH_RETTY_CHG_METH_RETTY_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstractMethodReturnType:", ?mfqn_, "?msig_") AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?ty ?ty_
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:name ?mname ;
            java:signature ?msig ;
            java:fullyQualifiedName ?mfqn ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:name ?mname_ ;
             java:signature ?msig_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?ty_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?tdecl a java:TypeDeclaration ;
             chg:mappedTo ?tdecl_ .

      FILTER (EXISTS {
        ?meth_ src:child0 ?mods_ .
        [] a java:Abstract ;
           src:parent ?mods_ .
      } || EXISTS {
        ?tdecl_ a java:InterfaceDeclaration .
      })

    } GROUP BY ?meth ?meth_ ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?ty ?ty_
  }

  ?class_ a java:TypeDeclaration ;
          java:subTypeOf* ?tdecl_ .

  ?meth0_ a java:MethodDeclaration ;
          src:child5 [] ;
          java:name ?mname_ ;
          java:fullyQualifiedName ?mfqn0_ ;
          java:signature ?msig_ ;
          src:child2 ?ty0_ ;
          ^chg:mappedTo ?meth0 .

  ?ty0 a java:Type ;
       chg:relabeled ?ty0_ .

  FILTER (EXISTS {
    ?meth0_ java:inClass ?class_ .
  } || EXISTS {
    ?meth0_ java:inInstanceCreation/java:ofReferenceType ?class_ .
  })

  FILTER NOT EXISTS {
    ?tdecl_ a [] .
    ?class_ java:subClassOf+ ?c_ .
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?tdecl_ .
    [] a java:MethodDeclaration ;
       src:child5 [] ;
       java:inClass ?c_ ;
       java:name ?mname_ .
  }

  FILTER NOT EXISTS {
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?class_ .
    [] a java:MethodDeclaration ;
       src:child5 [] ;
       java:inClass ?c_ ;
       java:name ?mname_ .
  }

}
}
''' % NS_TBL

Q_RM_M_ABST_INS_BODY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstract:", ?fqn) AS ?name)
(?abst AS ?key) (?ctx_ AS ?key_)
(?bctx AS ?ent) (?body_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?abst a java:Abstract ;
        java:inMethod ?meth ;
        chg:removal ?ctx_ .

  ?meth a java:MethodDeclaration ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodDeclaration ;
         java:name ?mname_ .

  ?body_ a java:MethodBody ;
         java:inMethod ?meth_ ;
         chg:addition ?bctx .

}
}
''' % NS_TBL

Q_RM_M_ABST_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstract:", ?fqn) AS ?name)
(?abst AS ?dep) (?ctx_ AS ?dep_)
(?meth0 AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?abst a java:Abstract ;
        java:inMethod ?meth ;
        chg:removal ?ctx_ .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?class ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodDeclaration ;
         java:name ?mname_ .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig)

  ?class0 java:subClassOf+ ?class .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?class0 ;
         java:name ?mname ;
         ?p ?o OPTION (INFERENCE NONE) ;
         java:fullyQualifiedName ?fqn0 ;
         chg:removal ?ctx0_ .

  FILTER NOT EXISTS {
    ?abst0 a java:Abstract ;
           java:inMethod ?meth0 .
  }

}
}
''' % NS_TBL

Q_ADD_M_ABST_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstract:", ?sig) AS ?name)
(?ctx AS ?ent) (?abst_ AS ?ent_)
(?ctx0 AS ?dep) (?meth0_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?abst_ a java:Abstract ;
         java:inMethod ?meth_ ;
         chg:addition ?ctx .

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?class_ ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ .

  ?meth a java:MethodDeclaration ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:mappedTo ?meth_ .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig)

  ?class0_ java:subClassOf+ ?class_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?class0_ ;
          java:name ?mname_ ;
          java:fullyQualifiedName ?fqn0_ ;
          chg:addition ?ctx0 .

  FILTER NOT EXISTS {
    ?abst0_ a java:Abstract ;
            java:inMethod ?meth0_ .
  }

}
}
''' % NS_TBL

Q_RM_C_ABST_RM_M_ABST_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstract:", ?cfqn) AS ?name)
(?mabst AS ?dep) (?ctxm_ AS ?dep_)
(?cabst AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mfqn ?mabst ?ctxm_
    WHERE {
      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ .

      ?mabst a java:Abstract ;
             java:inMethod ?meth ;
             chg:removal ?ctxm_ .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mfqn ?mabst ?ctxm_
  }

  {
    SELECT DISTINCT ?class ?class_ ?cfqn ?cabst ?ctx_
    WHERE {
      ?class a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?class_ .

      ?cabst a java:Abstract ;
             src:parent/src:parent/src:parent ?class ;
             chg:removal ?ctx_ .

    } GROUP BY ?class ?class_ ?cfqn ?cabst ?ctx_
  }

}
}
''' % NS_TBL

Q_ADD_C_ABST_ADD_M_ABST_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstract:", ?cfqn_) AS ?name)
(?ctx AS ?dep) (?cabst_ AS ?dep_)
(?ctxm AS ?ent) (?mabst_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mfqn_ ?mabst_ ?ctxm
    WHERE {
      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ .

      ?mabst_ a java:Abstract ;
              java:inMethod ?meth_ ;
              chg:addition ?ctxm .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mfqn_ ?mabst_ ?ctxm
  }

  {
    SELECT DISTINCT ?class ?class_ ?cfqn_ ?cabst_ ?ctx
    WHERE {
      ?class_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ ;
              ^chg:mappedTo ?class .

      ?cabst_ a java:Abstract ;
              src:parent/src:parent/src:parent ?class_ ;
              chg:addition ?ctx .

    } GROUP BY ?class ?class_ ?cfqn_ ?cabst_ ?ctx
  }

}
}
''' % NS_TBL

Q_ADD_C_ABST_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstract:", ?cfqn_) AS ?name)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?ctx AS ?ent) (?cabst_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
    WHERE {

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      ?super a java:SuperType ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?super_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?tdecl_ .

      ?ty a java:ReferenceType ;
          src:parent ?super ;
          java:refersToDeclaration ?td ;
          java:name ?tyname ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           java:refersToDeclaration ?td_ ;
           src:parent ?super_ ;
           java:name ?tyname_ .

    } GROUP BY ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
  }

  ?td a java:TypeDeclaration ;
      chg:mappedTo ?td0_ .

  ?cabst_ a java:Abstract ;
          src:parent/src:parent/src:parent ?td0_ ;
          chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_C_ABST_CHG_NEW_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstract:", ?cfqn) AS ?name)
(?cabst AS ?dep) (?ctx_ AS ?dep_)
(?new AS ?ent) (?new_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cfqn_ ?cabst ?ctx_ ?ver_
    WHERE {
      ?class a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?class_ .

      ?cabst a java:Abstract ;
             src:parent/src:parent/src:parent ?class ;
             chg:removal ?ctx_ .

      ?class_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ ;
              ver:version ?ver_ .

    } GROUP BY ?class ?class_ ?cfqn_ ?cabst ?ctx_ ?ver_
  }

  ?new a java:InstanceCreation ;
       chg:relabeled ?new_ .

  ?new_ a java:InstanceCreation ;
        java:inTypeDeclaration/ver:version ?ver_ ;
        src:child1/java:name ?cfqn_ .

}
}
''' % NS_TBL

Q_RM_ARG_RM_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveArgument:", ?cfqn) AS ?name)
(?ctor0 AS ?dep) (?ctx0_ AS ?dep_)
(?arg AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cfqn ?cfqn_ ?ctor ?ctx_
    WHERE {

      ?ctor a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?class ;
            chg:removal ?ctx_ .

      ?class a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      FILTER NOT EXISTS {
        [] a java:ConstructorDeclaration ;
           java:inTypeDeclaration ?class ;
           src:child2 ?params0 .
        FILTER NOT EXISTS {
          [] src:parent ?params0 .
        }
      }
      FILTER NOT EXISTS {
        [] a java:ConstructorDeclaration ;
           java:inTypeDeclaration ?class_ ;
           src:child2 ?params0_ .
        FILTER NOT EXISTS {
          [] src:parent ?params0_ .
        }
      }

    } GROUP BY ?class ?class_ ?cfqn ?cfqn_ ?ctor ?ctx_
  }

  ?new a java:InstanceCreation ;
       java:mayInvokeMethod ?ctor ;
       chg:mappedTo ?new_ .

  ?new_ a java:InstanceCreation ;
        src:child1/java:name ?cfqn_ .

  ?args a java:Arguments ;
        src:parent ?new ;
        chg:mappedTo ?args_ .

  ?args_ a java:Arguments ;
         src:parent ?new_ .

  ?arg a java:Expression ;
       src:parent ?args ;
       chg:removal ?ctxa_ .

  FILTER NOT EXISTS {
    [] src:parent ?args_ .
  }

  ?ctor0 a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?class ;
         chg:removal ?ctx0_ .

}
}
''' % NS_TBL

Q_ADD_ARG_ADD_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddArgument:", ?cfqn) AS ?name)
(?ctxa AS ?dep) (?arg_ AS ?dep_)
(?ctx0 AS ?ent) (?ctor0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cfqn ?cfqn_ ?ctor_ ?ctx
    WHERE {

      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?class_ ;
             chg:addition ?ctx .

      ?class a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      FILTER NOT EXISTS {
        [] a java:ConstructorDeclaration ;
           java:inTypeDeclaration ?class ;
           src:child2 ?params0 .
        FILTER NOT EXISTS {
          [] src:parent ?params0 .
        }
      }
      FILTER NOT EXISTS {
        [] a java:ConstructorDeclaration ;
           java:inTypeDeclaration ?class_ ;
           src:child2 ?params0_ .
        FILTER NOT EXISTS {
          [] src:parent ?params0_ .
        }
      }

    } GROUP BY ?class ?class_ ?cfqn ?cfqn_ ?ctor_ ?ctx
  }

  ?new_ a java:InstanceCreation ;
        java:mayInvokeMethod ?ctor_ ;
        ^chg:mappedTo ?new .

  ?new a java:InstanceCreation ;
       src:child1/java:name ?cfqn .

  ?args a java:Arguments ;
        src:parent ?new ;
        chg:mappedTo ?args_ .

  ?args_ a java:Arguments ;
         src:parent ?new_ .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        chg:addition ?ctxa .

  FILTER NOT EXISTS {
    [] src:parent ?args .
  }

  ?ctor0_ a java:ConstructorDeclaration ;
          java:inTypeDeclaration ?class_ ;
          chg:addition ?ctx0 .

}
}
''' % NS_TBL

Q_ADD_C_ABST_CHG_NEW_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddAbstract:", ?cfqn) AS ?name)
(?new AS ?dep) (?new_ AS ?dep_)
(?ctx AS ?ent) (?cabst_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cfqn ?cabst_ ?ctx ?ver
    WHERE {
      ?class a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             ver:version ?ver ;
             chg:mappedTo ?class_ .

      ?cabst_ a java:Abstract ;
              src:parent/src:parent/src:parent ?class_ ;
              chg:addition ?ctx .

      ?class_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ ;
              ver:version ?ver_ .

    } GROUP BY ?class ?class_ ?cfqn ?cabst_ ?ctx ?ver
  }

  ?new a java:InstanceCreation ;
       java:inTypeDeclaration/ver:version ?ver ;
       src:child1/java:name ?cfqn ;
       chg:relabeled ?new_ .

  ?new_ a java:InstanceCreation .

}
}
''' % NS_TBL

Q_RM_C_ABST_ADD_DEFAULT_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAbstract:", ?cfqn) AS ?name)
(?ctx AS ?dep) (?ctor_ AS ?dep_)
(?cabst AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cfqn ?cfqn_ ?cabst ?ctx_
    WHERE {
      ?class a java:ClassDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?class_ .

      ?cabst a java:Abstract ;
             src:parent/src:parent/src:parent ?class ;
             chg:removal ?ctx_ .

      ?class_ a java:ClassDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?class ?class_ ?cfqn ?cfqn_ ?cabst ?ctx_
  }

  ?ctor_ a java:ConstructorDeclaration ;
         java:inClass ?class_ ;
         chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?param_ a java:Parameter ;
            src:parent ?params_ .
    ?params_ a java:Parameters ;
             src:parent ?ctor_ .
  }

  FILTER EXISTS {
    [] java:subClassOf ?class_ .
  }

}
}
''' % NS_TBL

Q_CHG_FD_PUBLIC_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangePublic:", ?fqn) AS ?name)
(?x AS ?key) (?pub_ AS ?key_)
(?x AS ?dep) (?pub_ AS ?dep_)
(?ctxf AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?pub_ ?fqn ?fdecl_ ?facc_ ?ctxf ?meth_
    WHERE {

      {
        SELECT DISTINCT ?x ?pub_ ?fqn ?fdecl_ ?tdecl_
        WHERE {

          ?x a java:Modifier ;
             src:parent/src:parent ?fdecl ;
             chg:relabeled ?pub_ .

          ?pub_ a java:Public ;
                src:parent/src:parent ?fdecl_ .

          ?fdecl a java:FieldDeclaration ;
                 chg:mappedTo ?fdecl_ .

          ?fdecl_ a java:FieldDeclaration ;
                  java:inTypeDeclaration ?tdecl_ ;
                  java:fullyQualifiedName ?fqn .

        } GROUP BY ?x ?pub_ ?fqn ?fdecl_ ?tdecl_
      }

      ?facc_ a java:FieldAccess ;
             java:inMethodOrConstructor ?meth_ ;
             java:name ?fname ;
             src:child0 ?e_ ;
             chg:addition ?ctxf .

      ?e_ a java:Expression ;
          java:ofReferenceType ?tdecl0_ .

      ?tdecl0_ java:subClassOf* ?tdecl_ ;
               java:fullyQualifiedName ?tyname .

      #BIND(CONCAT(?tyname, ".", ?fname) AS ?fqn0)

    } GROUP BY ?x ?pub_ ?fqn ?fdecl_ ?facc_ ?ctxf ?meth_
  }

  ?meth_ java:inTypeDeclaration/ver:version ?ver_ .
  ?fdecl_ java:inTypeDeclaration/ver:version ?ver_ .

}
}
''' % NS_TBL

Q_CHG_FD_PROTECTED_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeProtected:", ?fqn_) AS ?name)
(?x AS ?key) (?prot_ AS ?key_)
(?x AS ?dep) (?prot_ AS ?dep_)
(?ctxf AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?prot_ ?fname_ ?fdecl_ ?tdecl_ ?fqn_
    WHERE {
      ?x a java:Modifier ;
         src:parent/src:parent ?fdecl ;
         chg:relabeled ?prot_ .

      ?prot_ a java:Protected ;
            src:parent/src:parent ?fdecl_ .

      ?fdecl a java:FieldDeclaration ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:name ?fname_ ;
              java:fullyQualifiedName ?fqn_ ;
              java:inTypeDeclaration ?tdecl_ .

    } GROUP BY ?x ?prot_ ?fname_ ?fdecl_ ?tdecl_ ?fqn_
  }

  ?tdecl0_ java:subClassOf+ ?tdecl_ ;
           java:fullyQualifiedName ?tyname_ .

  ?facc_ a java:FieldAccess ;
         java:inTypeDeclaration ?tdecl0_ ;
         java:name ?fname_ ;
         chg:addition ?ctxf .

  ?fdecl_ java:inTypeDeclaration/ver:version ?ver_ .

  ?tdecl0_ ver:version ?ver_ .

}
}
''' % NS_TBL

Q_CHG_FD_PROTECTED_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeProtected:", ?fqn_) AS ?name)
(?facc AS ?dep) (?x_ AS ?dep_)
(?mod AS ?ent) (?prot_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mod ?prot_ ?fname ?fdecl_ ?tdecl_ ?fqn_ ?vdtor
    WHERE {
      ?mod a java:Modifier ;
           src:parent/src:parent ?fdecl ;
           chg:relabeled ?prot_ .

      ?prot_ a java:Protected ;
            src:parent/src:parent ?fdecl_ .

      ?fdecl a java:FieldDeclaration ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:fullyQualifiedName ?fqn_ ;
              java:inTypeDeclaration ?tdecl_ .

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname .

    } GROUP BY ?mod ?prot_ ?fname ?fdecl_ ?tdecl_ ?fqn_ ?vdtor
  }

  ?facc a java:FieldAccess ;
        java:declaredBy ?vdtor ;
        chg:relabeled ?x_ .

  ?x_ a java:Entity ;
      a ?catx_ OPTION (INFERENCE NONE) .

  FILTER NOT EXISTS {
    ?tdecl0_ java:subClassOf+ ?tdecl_ ;
             java:fullyQualifiedName ?tyname_ .

    ?x_ java:inTypeDeclaration ?tdecl0_ .

    ?fdecl_ java:inTypeDeclaration/ver:version ?ver_ .

    ?tdecl0_ ver:version ?ver_ .
  }

}
}
''' % NS_TBL

Q_CHG_FD_PUBLIC_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangePublic:", ?fqn) AS ?name)
(?x AS ?key) (?pub_ AS ?key_)
(?x AS ?dep) (?pub_ AS ?dep_)
(?expr AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?pub_ ?fqn ?fdecl_ ?facc_ ?expr ?meth_
    WHERE {

      {
        SELECT DISTINCT ?x ?pub_ ?fqn ?fdecl_ ?tdecl_
        WHERE {

          ?x a java:Modifier ;
             src:parent/src:parent ?fdecl ;
             chg:relabeled ?pub_ .

          ?pub_ a java:Public ;
                src:parent/src:parent ?fdecl_ .

          ?fdecl a java:FieldDeclaration ;
                 chg:mappedTo ?fdecl_ .

          ?fdecl_ a java:FieldDeclaration ;
                  java:inTypeDeclaration ?tdecl_ ;
                  java:fullyQualifiedName ?fqn .

        } GROUP BY ?x ?pub_ ?fqn ?fdecl_ ?tdecl_
      }

      ?expr chg:relabeled ?facc_ .

      ?facc_ a java:FieldAccess ;
             java:inMethodOrConstructor ?meth_ ;
             java:name ?fname ;
             src:child0 ?e_ .

      ?e_ a java:Expression ;
          java:ofReferenceType ?tdecl0_ .

      ?tdecl0 java:subClassOf* ?tdecl_ ;
              java:fullyQualifiedName ?tyname .

      BIND(CONCAT(?tyname, ".", ?fname) AS ?fqn0)

    } GROUP BY ?x ?pub_ ?fqn ?fdecl_ ?facc_ ?expr ?meth_
  }

  ?meth_ java:inTypeDeclaration/ver:version ?ver_ .
  ?fdecl_ java:inTypeDeclaration/ver:version ?ver_ .

}
}
''' % NS_TBL

Q_ADD_CLASS_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddClass:", ?fqn_) AS ?name)
(?ctx AS ?key) (?class_ AS ?key_)
(?ctx AS ?dep) (?class_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class_ ?cname_ ?fqn_ ?ctx ?x_ ?ctxx ?xname_
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
    WHERE {

      {
        SELECT DISTINCT ?class_ ?cname_ ?fqn_ ?ctx ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
        WHERE {

          ?class_ a java:TypeDeclaration ;
                  #ver:version ?ver_ ;
                  java:name ?cname_ ;
                  java:fullyQualifiedName ?fqn_ ;
                  chg:addition ?ctx .

          FILTER NOT EXISTS {
            ?class chg:mappedTo ?class_ .
          }

          BIND (CONCAT(?fqn_, ".") AS ?pat0)
          BIND (CONCAT(?cname_, ".") AS ?pat1)
          BIND (CONCAT(?fqn_, "$$") AS ?pat2)
          BIND (CONCAT(?cname_, "$$") AS ?pat3)
          BIND (CONCAT(?fqn_, "<") AS ?pat4)
          BIND (CONCAT(?cname_, "<") AS ?pat5)

        } GROUP BY ?class_ ?cname_ ?fqn_ ?ctx ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
      }

      ?x_ a ?cat OPTION (INFERENCE NONE) ;
          #src:parent+/ver:version ?ver_ ;
          java:name ?xname_ ;
          chg:addition ?ctxx .

      FILTER EXISTS {
        ?class_ ver:version ?ver_ .
        ?x_ src:parent+/ver:version ?ver_ .
      }

    } GROUP BY ?class_ ?cname_ ?fqn_ ?ctx ?x_ ?ctxx ?xname_ ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
  }

  FILTER (?xname_ = ?fqn_ ||
          #?xname_ = ?cname_ ||
          STRSTARTS(?xname_, ?pat0) ||
          #STRSTARTS(?xname_, ?pat1) ||
          STRSTARTS(?xname_, ?pat2) ||
          #STRSTARTS(?xname_, ?pat3) ||
          STRSTARTS(?xname_, ?pat4)# ||
          #STRSTARTS(?xname_, ?pat5)
          )

}
}
''' % NS_TBL

Q_MOV_FILE_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("MoveFile:", ?loc) AS ?name)
(?file AS ?key) (?file_ AS ?key_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?class a java:TypeDeclaration ;
         src:inFile ?file ;
         chg:mappedTo ?class_ .

  ?class_ a java:TypeDeclaration ;
          src:inFile ?file_ ;
          ver:version ?ver_ ;
          java:name ?cname_ ;
          java:fullyQualifiedName ?fqn_ .

  ?file src:location ?loc ;
        chg:movedTo ?file_ .


  ?x_ a ?cat OPTION (INFERENCE NONE) ;
      src:parent+/ver:version ?ver_ ;
      java:name ?xname_ ;
      chg:addition ?ctxx .

  FILTER (?xname_ = ?fqn_ ||
          ?xname_ = ?cname_ ||
          STRSTARTS(?xname_, CONCAT(?fqn_, ".")) ||
          STRSTARTS(?xname_, CONCAT(?cname_, ".")) ||
          STRSTARTS(?xname_, CONCAT(?fqn_, "$$")) ||
          STRSTARTS(?xname_, CONCAT(?cname_, "$$"))
          )

}
}
''' % NS_TBL

Q_MOV_FILE_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("MoveFile:", ?loc) AS ?name)
(?file AS ?key) (?file_ AS ?key_)
(?x AS ?ent) (?ctxx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?class a java:TypeDeclaration ;
         src:inFile ?file ;
         ver:version ?ver ;
         java:name ?cname ;
         java:fullyQualifiedName ?fqn ;
         chg:mappedTo ?class_ .

  ?class_ a java:TypeDeclaration ;
          src:inFile ?file_ ;
          ver:version ?ver_ ;
          java:name ?cname_ ;
          java:fullyQualifiedName ?fqn_ .

  ?file src:location ?loc ;
        chg:movedTo ?file_ .


  ?x a ?cat OPTION (INFERENCE NONE) ;
     src:parent+/ver:version ?ver ;
     java:name ?xname ;
     chg:removal ?ctxx_ .

  FILTER (?xname = ?fqn ||
          ?xname = ?cname ||
          STRSTARTS(?xname, CONCAT(?fqn, ".")) ||
          STRSTARTS(?xname, CONCAT(?cname, ".")) ||
          STRSTARTS(?xname, CONCAT(?fqn, "$$")) ||
          STRSTARTS(?xname, CONCAT(?cname, "$$"))
          )

}
}
''' % NS_TBL

Q_MOV_FILE_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("MoveFile:", ?loc) AS ?name)
(?file AS ?key) (?file_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?class a java:TypeDeclaration ;
         src:inFile ?file ;
         ver:version ?ver ;
         java:name ?cname ;
         java:fullyQualifiedName ?fqn ;
         chg:mappedTo ?class_ .

  ?class_ a java:TypeDeclaration ;
          src:inFile ?file_ ;
          ver:version ?ver_ ;
          java:name ?cname_ ;
          java:fullyQualifiedName ?fqn_ .

  ?file src:location ?loc ;
        chg:movedTo ?file_ .


  ?x a ?cat OPTION (INFERENCE NONE) ;
     src:parent+/ver:version ?ver ;
     java:name ?xname ;
     chg:relabeled ?x_ .

  ?x_ java:name ?xname_ .

  FILTER (?xname = ?fqn ||
          ?xname = ?cname ||
          STRSTARTS(?xname, CONCAT(?fqn, ".")) ||
          STRSTARTS(?xname, CONCAT(?cname, ".")) ||
          STRSTARTS(?xname, CONCAT(?fqn, "$$")) ||
          STRSTARTS(?xname, CONCAT(?cname, "$$"))
          )

  FILTER (?xname_ = ?fqn_ ||
          ?xname_ = ?cname_ ||
          STRSTARTS(?xname_, CONCAT(?fqn_, ".")) ||
          STRSTARTS(?xname_, CONCAT(?cname_, ".")) ||
          STRSTARTS(?xname_, CONCAT(?fqn_, "$$")) ||
          STRSTARTS(?xname_, CONCAT(?cname_, "$$"))
          )

}
}
''' % NS_TBL

Q_RM_TD_PUBLIC_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemovePublic:", ?fqn) AS ?name)
#(?pub AS ?key) (?ctx_ AS ?key_)
#(?import AS ?ent) (?ctxi_ AS ?ent_)
(?pub AS ?ent) (?ctx_ AS ?ent_)
(?import AS ?dep) (?ctxi_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?pub ?ctx_ ?fqn ?ver
    WHERE {
      ?pub a java:Public ;
           src:parent/src:parent/src:parent ?tdecl ;
           chg:removal ?ctx_ .

      ?tdecl a java:TypeDeclaration ;
             ver:version ?ver ;
             java:fullyQualifiedName ?fqn .

    } GROUP BY ?pub ?ctx_ ?fqn ?ver
  }

  {
    SELECT DISTINCT ?import ?ctxi_ ?n ?ver
    WHERE {
      ?import a java:ImportDeclaration ;
              src:parent/src:parent/src:inFile/ver:version ?ver ;
              chg:removal ?ctxi_ ;
              java:name ?n .
    } GROUP BY ?import ?ctxi_ ?n ?ver
  }

  FILTER (?fqn = ?n)

}
}
''' % NS_TBL

Q_RM_FD_PUBLIC_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemovePublic:", ?fqn) AS ?name)
(?facc AS ?dep) (?ctxf_ AS ?dep_)
(?pub AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?pub ?ctx_ ?fqn ?vdtor
    WHERE {
      ?pub a java:Public ;
           src:parent/src:parent ?fdecl ;
           chg:removal ?ctx_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration/ver:version ?ver ;
             src:child2 ?vdtor ;
             java:fullyQualifiedName ?fqn .

    } GROUP BY ?pub ?ctx_ ?fqn ?vdtor
  }

  ?facc java:declaredBy ?vdtor ;
        chg:removal ?ctxf_ .

  {
    ?facc a java:FieldAccess ;
          src:child0 ?e .

    FILTER NOT EXISTS {
      ?e a java:This .
    }
  }
  UNION
  {
    ?facc a java:Name .
  }

}
}
''' % NS_TBL

Q_RM_FD_PUBLIC_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemovePublic:", ?fqn) AS ?name)
(?facc AS ?dep) (?facc_ AS ?dep_)
(?pub AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?pub ?ctx_ ?fqn ?vdtor
    WHERE {
      ?pub a java:Public ;
           src:parent/src:parent ?fdecl ;
           chg:removal ?ctx_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration/ver:version ?ver ;
             src:child2 ?vdtor ;
             java:fullyQualifiedName ?fqn .

    } GROUP BY ?pub ?ctx_ ?fqn ?vdtor
  }

  ?facc java:declaredBy ?vdtor ;
        chg:relabeled ?facc_ .

  {
    ?facc a java:FieldAccess ;
          src:child0 ?e .

    FILTER NOT EXISTS {
      ?e a java:This .
    }
  }
  UNION
  {
    ?facc a java:Name .
  }

}
}
''' % NS_TBL

Q_RM_FD_PRIVATE_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemovePrivate:", ?fqn) AS ?name)
(?priv AS ?key) (?ctx_ AS ?key_)
(?priv AS ?dep) (?ctx_ AS ?dep_)
(?ctxf AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?priv ?ctx_ ?fqn ?class_ ?fname_ ?vdtor_
    WHERE {
      ?priv a java:Private ;
            src:parent/src:parent ?fdecl ;
            chg:removal ?ctx_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname_ .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?priv ?ctx_ ?fqn ?class_ ?fname_ ?vdtor_
  }

  ?facc_ a java:FieldAccess ;
         java:declaredBy ?vdtor_ ;
         chg:addition ?ctxf .

  FILTER NOT EXISTS {
    ?facc_ java:inTypeDeclaration ?class_ .
  }

}
}
''' % NS_TBL

Q_CHG_FD_PRIVATE_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangePrivate:", ?fqn) AS ?name)
(?priv AS ?key) (?mod_ AS ?key_)
(?priv AS ?dep) (?mod_ AS ?dep_)
(?ctxf AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?priv ?mod_ ?fqn ?class_ ?fname_ ?vdtor_
    WHERE {
      ?priv a java:Private ;
            src:parent/src:parent ?fdecl ;
            chg:relabeled ?mod_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname_ .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?priv ?mod_ ?fqn ?class_ ?fname_ ?vdtor_
  }

  ?facc_ a java:FieldAccess ;
         java:declaredBy ?vdtor_ ;
         chg:addition ?ctxf .

  FILTER NOT EXISTS {
    ?facc_ java:inTypeDeclaration ?class_ .
  }

}
}
''' % NS_TBL

Q_ADD_FD_PRIVATE_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemovePrivate:", ?fqn) AS ?name)
(?facc AS ?dep) (?ctxf_ AS ?dep_)
(?ctx AS ?ent) (?priv_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?priv_ ?ctx ?fqn_ ?class ?fname ?vdtor
    WHERE {
      ?priv_ a java:Private ;
             src:parent/src:parent ?fdecl_ ;
            chg:addition ?ctx .

      ?fdecl_ a java:FieldDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             ^chg:mappedTo ?fdecl .

      ?fdecl a java:FieldDeclaration ;
              java:inTypeDeclaration ?class .

      ?vdtor a java:VariableDeclarator ;
              src:parent ?fdecl ;
              java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?priv_ ?ctx ?fqn_ ?class ?fname ?vdtor
  }

  ?facc a java:FieldAccess ;
        java:declaredBy ?vdtor ;
        chg:removal ?ctxf_ .

  FILTER NOT EXISTS {
    ?facc java:inTypeDeclaration ?class .
  }

}
}
''' % NS_TBL

Q_CHG_FD_PRIVATE_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangePrivate:", ?fqn) AS ?name)
(?facc AS ?dep) (?ctxf_ AS ?dep_)
(?mod AS ?ent) (?priv_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mod ?priv_ ?fqn_ ?class ?fname ?vdtor
    WHERE {
      ?priv_ a java:Private ;
             src:parent/src:parent ?fdecl_ ;
             ^chg:relabeled ?mod .

      ?fdecl_ a java:FieldDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             ^chg:mappedTo ?fdecl .

      ?fdecl a java:FieldDeclaration ;
              java:inTypeDeclaration ?class .

      ?vdtor a java:VariableDeclarator ;
              src:parent ?fdecl ;
              java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?mod ?priv_ ?fqn_ ?class ?fname ?vdtor
  }

  ?facc a java:FieldAccess ;
        java:declaredBy ?vdtor ;
        chg:removal ?ctxf_ .

  FILTER NOT EXISTS {
    ?facc java:inTypeDeclaration ?class .
  }

}
}
''' % NS_TBL

Q_RM_FD_FINAL_RM_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?fqn) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?x AS ?ent) (?ctxx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final ?ctx_ ?class ?fname ?fqn
    WHERE {

      ?final a java:Final ;
             src:parent/src:parent ?fdecl ;
             chg:removal ?ctx_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent/src:parent ?fdecl .
      }
      FILTER NOT EXISTS {
        ?vdtor src:child0 [] .
      }

    } GROUP BY ?final ?ctx_ ?class ?fname ?fqn
  }

  ?meth a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?class .

  ?assign a ?cat OPTION (INFERENCE NONE) ;
          java:inConstructor ?meth ;
          src:child0 ?x .

  FILTER (?cat IN (java:Assign,java:AssignStatement))

  ?x java:name ?fname ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_RM_FD_FINAL_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?fqn) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final ?ctx_ ?class ?class_ ?fname ?fqn
    WHERE {

      ?final a java:Final ;
             src:parent/src:parent ?fdecl ;
             chg:removal ?ctx_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent/src:parent ?fdecl .
      }

    } GROUP BY ?final ?ctx_ ?class ?class_ ?fname ?fqn
  }

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration/java:subTypeOf* ?class_ .

  ?assign_ a ?cat_ OPTION (INFERENCE NONE) ;
           java:inMethodOrConstructor ?meth_ ;
           src:child0 ?x_ .

  FILTER (?cat_ IN (java:Assign,java:AssignStatement))

  ?x_ java:name ?fname ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_RM_FD_FINAL_CHG_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?fqn) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final ?ctx_ ?class ?class_ ?fname ?fqn ?vdtor
    WHERE {

      ?final a java:Final ;
             src:parent/src:parent ?fdecl ;
             chg:removal ?ctx_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent/src:parent ?fdecl .
      }

    } GROUP BY ?final ?ctx_ ?class ?class_ ?fname ?fqn ?vdtor
  }

  {
    ?meth a java:ConstructorDeclaration ;
          java:inTypeDeclaration ?class .

    ?assign a ?cat OPTION (INFERENCE NONE) ;
            java:inConstructor ?meth ;
            src:child0 ?x .

    FILTER (?cat IN (java:Assign,java:AssignStatement))

    ?x java:name ?fname ;
       chg:relabeled ?x_ .

    FILTER NOT EXISTS {
      ?vdtor src:child0 [] .
    }
  }
  UNION
  {
    ?meth_ a java:MethodOrConstructor ;
           java:inTypeDeclaration/java:subTypeOf* ?class_ .

    ?assign_ a ?cat_ OPTION (INFERENCE NONE) ;
             java:inMethodOrConstructor ?meth_ ;
             src:child0 ?x_ .

    FILTER (?cat_ IN (java:Assign,java:AssignStatement))

    ?x_ java:name ?fname ;
        ^chg:relabeled ?x .
  }

}
}
''' % NS_TBL

Q_RM_M_FINAL_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?mfqn, ?msig) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?ctx0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final ?ctx_
    WHERE {
      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?final a java:Final ;
             java:inMethod ?meth ;
             chg:removal ?ctx_ .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final ?ctx_
  }

  ?class0_ java:subTypeOf+ ?class_ .

  ?meth0_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?class0_ ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?mfqn0_ ;
         java:signature ?msig0_ ;
         chg:addition ?ctx0 .

}
}
''' % NS_TBL

Q_RM_M_FINAL_ADD_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?mfqn, ?msig) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?ctx0 AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final ?ctx_
    WHERE {
      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?final a java:Final ;
             java:inMethod ?meth ;
             chg:removal ?ctx_ .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final ?ctx_
  }

  ?class0_ java:subTypeOf+ ?class_ .

  ?meth0_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?class0_ ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?mfqn0_ ;
         java:signature ?msig0_ .

  ?ref a jref:AddParameter ;
       jref:addedParameter ?param_ ;
       jref:modifiedMethod ?meth0_ .

  ?param_ chg:addition ?ctx0 .

}
}
''' % NS_TBL

Q_ADD_M_FINAL_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?mfqn_, ".", ?msig_) AS ?name)
(?meth0 AS ?dep) (?ctx0_ AS ?dep_)
(?ctx AS ?ent) (?final_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final_ ?ctx
    WHERE {
      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?final_ a java:Final ;
              java:inMethod ?meth_ ;
              chg:addition ?ctx .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final_ ?ctx
  }

  ?class0 java:subTypeOf+ ?class .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?class0 ;
         java:name ?mname ;
         java:fullyQualifiedName ?mfqn0 ;
         java:signature ?msig0 ;
         chg:removal ?ctx0_ .

}
}
''' % NS_TBL

Q_ADD_M_FINAL_RM_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?mfqn_, ".", ?msig_) AS ?name)
(?param AS ?dep) (?ctx0_ AS ?dep_)
(?ctx AS ?ent) (?final_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final_ ?ctx
    WHERE {
      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?final_ a java:Final ;
              java:inMethod ?meth_ ;
              chg:addition ?ctx .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final_ ?ctx
  }

  ?class0 java:subTypeOf+ ?class .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?class0 ;
         java:name ?mname ;
         java:fullyQualifiedName ?mfqn0 ;
         java:signature ?msig0 .

  ?ref a jref:RemoveParameter ;
       jref:removedParameter ?param ;
       jref:originalMethod ?meth0 .

  ?param chg:removal ?ctx0_ .

}
}
''' % NS_TBL

Q_ADD_FD_FINAL_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?fqn_) AS ?name)
(?ctx AS ?ent) (?final_ AS ?ent_)
(?ctxx AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final_ ?ctx ?class_ ?fname ?fqn_
    WHERE {

      ?final_ a java:Final ;
              src:parent/src:parent ?fdecl_ ;
              chg:addition ?ctx .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?fdecl_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent/src:parent ?fdecl_ .
      }
      FILTER NOT EXISTS {
        ?vdtor_ src:child0 [] .
      }

    } GROUP BY ?final_ ?ctx ?class_ ?fname ?fqn_
  }

  ?meth_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?class_ .

  ?assign_ a ?cat_ OPTION (INFERENCE NONE) ;
           java:inConstructor ?meth_ ;
           src:child0 ?x_ .

  FILTER (?cat_ IN (java:Assign,java:AssignStatement))

  ?x_ java:name ?fname ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_ADD_FD_FINAL_CHG_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?fqn_) AS ?name)
(?ctx AS ?ent) (?final_ AS ?ent_)
(?x AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final_ ?ctx ?class_ ?fname ?fqn_ ?vdtor_
    WHERE {

      ?final_ a java:Final ;
              src:parent/src:parent ?fdecl_ ;
              chg:addition ?ctx .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?fdecl_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent/src:parent ?fdecl_ .
      }

    } GROUP BY ?final_ ?ctx ?class_ ?fname ?fqn_ ?vdtor_
  }

  {
    ?meth a java:MethodOrConstructor ;
          java:inTypeDeclaration/java:subTypeOf* ?class .

    ?assign a ?cat OPTION (INFERENCE NONE) ;
            java:inMethodOrConstructor ?meth ;
            src:child0 ?x .

    FILTER (?cat IN (java:Assign,java:AssignStatement))

    ?x java:name ?fname ;
       chg:relabeled ?x_ .
  }
  UNION
  {
    ?meth_ a java:ConstructorDeclaration ;
           java:inTypeDeclaration ?class_ .

    ?assign_ a ?cat_ OPTION (INFERENCE NONE) ;
             java:inConstructor ?meth_ ;
             src:child0 ?x_ .

    FILTER (?cat_ IN (java:Assign,java:AssignStatement))

    ?x_ java:name ?fname ;
        ^chg:relabeled ?x .

    FILTER NOT EXISTS {
      ?vdtor_ src:child0 [] .
    }
  }

}
}
''' % NS_TBL

Q_ADD_FD_FINAL_RM_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?fqn_) AS ?name)
(?ctx AS ?ent) (?final_ AS ?ent_)
(?x AS ?dep) (?ctxx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final_ ?ctx ?class ?class_ ?fname ?fqn_
    WHERE {

      ?final_ a java:Final ;
              src:parent/src:parent ?fdecl_ ;
              chg:addition ?ctx .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?fdecl_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent/src:parent ?fdecl_ .
      }

    } GROUP BY ?final_ ?ctx ?class ?class_ ?fname ?fqn_
  }

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration/java:subTypeOf* ?class .

  ?assign a ?cat OPTION (INFERENCE NONE) ;
          java:inMethodOrConstructor ?meth ;
          src:child0 ?x .

  FILTER (?cat IN (java:Assign,java:AssignStatement))

  ?x java:name ?fname ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_CHG_M_MOD_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeModifier:", ?sig_) AS ?name)
(?mod AS ?dep) (?mod_ AS ?dep_)
(?meth AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mod ?mod_ ?meth ?meth_ ?sig_ ?sig0_ ?class ?class_ ?mname ?mname_
    WHERE {
      ?mod a java:Modifier ;
           java:inMethod ?meth ;
           chg:relabeled ?mod_ .

      ?mod_ a java:Modifier ;
            java:inMethod ?meth_ .

      ?meth a java:MethodDeclaration ;
            java:name ?mname ;
            java:inTypeDeclaration ?class ;
            chg:relabeled ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:name ?mname_ ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?mod ?mod_ ?meth ?meth_ ?sig_ ?sig0_ ?class ?class_ ?mname ?mname_
  }

  ?class_ java:subTypeOf+ ?super_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?super_ ;
          java:name ?mname_ ;
          java:signature ?sig0_ .


  { ?mod a java:Protected . } UNION { ?mod a java:Private . }
  ?mod_ a java:Public .
  FILTER (NOT EXISTS {
    ?m_ a java:AccessModifier ;
        src:parent/src:parent ?meth0_ .
  } || EXISTS {
    ?m_ a java:Public ;
        src:parent/src:parent ?meth0_ .
  })

}
}
''' % NS_TBL

Q_CHG_M_PUBLIC_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangePublic:", ?mfqn_, ".", ?msig) AS ?name)
(?mod AS ?dep) (?mod_ AS ?dep_)
(?ivk AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mod ?mod_
    WHERE {

      ?meth a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn ;
             java:signature ?msig ;
             src:child0 ?mods ;
             java:inTypeDeclaration ?tdecl0 ;
             chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             src:child0 ?mods_ ;
             java:inTypeDeclaration ?tdecl0_ .

      ?mods a java:Modifiers .

      ?mods_ a java:Modifiers .

      ?mod src:parent ?mods ;
           chg:relabeled ?mod_ .

      ?mod_ a java:Public ;
            src:parent ?mods_ .

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mod ?mod_
  }

  ?ivk_ java:mayInvokeMethod ?meth_ ;
        java:inTypeDeclaration ?tdecl_ ;
        ^chg:relabeled ?ivk .


  ?mod a java:Protected .

  FILTER NOT EXISTS {
    ?tdecl_ java:subTypeOf ?tdecl0_ .
  }

}
}
''' % NS_TBL

Q_CHG_M_PUBLIC_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangePublic:", ?mfqn_, ".", ?msig) AS ?name)
(?mod AS ?dep) (?mod_ AS ?dep_)
(?ctx AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mod ?mod_
    WHERE {

      ?meth a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn ;
             java:signature ?msig ;
             src:child0 ?mods ;
             java:inTypeDeclaration ?tdecl0 ;
             chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             src:child0 ?mods_ ;
             java:inTypeDeclaration ?tdecl0_ .

      ?mods a java:Modifiers .

      ?mods_ a java:Modifiers .

      ?mod src:parent ?mods ;
           chg:relabeled ?mod_ .

      ?mod_ a java:Public ;
            src:parent ?mods_ .

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mod ?mod_
  }

  ?ivk_ java:mayInvokeMethod ?meth_ ;
        java:inTypeDeclaration ?tdecl_ ;
        chg:addition ?ctx .


  ?mod a java:Protected .

  FILTER NOT EXISTS {
    ?tdecl_ java:subTypeOf ?tdecl0_ .
  }

}
}
''' % NS_TBL

Q_CHG_M_PROTECTED_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeProtected:", ?mfqn, ?msig) AS ?name)
(?mod AS ?ent) (?mod_ AS ?ent_)
(?ivk AS ?dep) (?ivk_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mod ?mod_
    WHERE {

      ?meth a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn ;
             java:signature ?msig ;
             src:child0 ?mods ;
             java:inTypeDeclaration ?tdecl0 ;
             chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             src:child0 ?mods_ ;
             java:inTypeDeclaration ?tdecl0_ .

      ?mods a java:Modifiers .

      ?mods_ a java:Modifiers .

      ?mod src:parent ?mods ;
           chg:relabeled ?mod_ .

      ?mod_ a java:Protected ;
            src:parent ?mods_ .

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mod ?mod_
  }

  ?ivk java:mayInvokeMethod ?meth ;
       java:inTypeDeclaration ?tdecl ;
       chg:relabeled ?ivk_ .


  ?mod a java:Public .

  FILTER NOT EXISTS {
    ?tdecl java:subTypeOf ?tdecl0 .
  }

}
}
''' % NS_TBL

Q_CHG_M_PROTECTED_RM_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeProtected:", ?mfqn, ?msig) AS ?name)
(?mod AS ?ent) (?mod_ AS ?ent_)
(?ivk AS ?dep) (?ctx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mods ?mods_
    WHERE {

      ?meth a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn ;
             java:signature ?msig ;
             src:child0 ?mods ;
             java:inTypeDeclaration ?tdecl0 ;
             chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             src:child0 ?mods_ ;
             java:inTypeDeclaration ?tdecl0_ .

      ?mods a java:Modifiers .

      ?mods_ a java:Modifiers .

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?tdecl0 ?tdecl0_ ?mods ?mods_
  }

  ?mod a ?catm OPTION (INFERENCE NONE) ;
       src:parent ?mods ;
       chg:relabeled ?mod_ .

  ?mod_ a ?catm_ OPTION (INFERENCE NONE) ;
        src:parent ?mods_ .

  FILTER (?catm = java:Public && ?catm_ = java:Protected ||
          ?catm = java:Protected && ?catm_ = java:Private)

  ?ivk java:mayInvokeMethod ?meth ;
       java:inTypeDeclaration ?tdecl ;
       chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?tdecl java:subTypeOf ?tdecl0 .
  }

}
}
''' % NS_TBL

Q_RM_M_PRIVATE_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemovePrivate:", ?sig_) AS ?name)
(?priv AS ?key) (?ctx_ AS ?key_)
(?priv AS ?dep) (?ctx_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?priv ?ctx_ ?sig_ ?class_ ?meth_
    WHERE {
      ?priv a java:Private ;
            java:inMethod ?meth ;
            chg:removal ?ctx_ .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?priv ?ctx_ ?sig_ ?class_ ?meth_
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctxi .

  FILTER NOT EXISTS {
    ?ivk_ java:inMethodOrConstructor/java:inClass ?class_ .
  }

}
}
''' % NS_TBL

Q_ADD_M_PRIVATE_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddPrivate:", ?sig) AS ?name)
(?ivk AS ?dep) (?ctxi_ AS ?dep_)
(?ctx AS ?ent) (?priv_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?priv_ ?ctx ?sig ?class ?meth
    WHERE {
      ?priv_ a java:Private ;
             java:inMethod ?meth_ ;
             chg:addition ?ctx .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             ^chg:mappedTo ?meth .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?priv_ ?ctx ?sig ?class ?meth
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth ;
       chg:removal ?ctxi_ .

  FILTER NOT EXISTS {
    ?ivk java:inMethodOrConstructor/java:inClass ?class .
  }

}
}
''' % NS_TBL

Q_CHG_M_PRIVATE_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemovePrivate:", ?sig_) AS ?name)
(?priv AS ?key) (?mod_ AS ?key_)
(?priv AS ?dep) (?mod_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?priv ?mod_ ?sig_ ?class_ ?meth_
    WHERE {
      ?priv a java:Private ;
            java:inMethod ?meth ;
            chg:relabeled ?mod_ .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?class ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

    } GROUP BY ?priv ?mod_ ?sig_ ?class_ ?meth_
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctxi .

  FILTER NOT EXISTS {
    ?ivk_ java:inMethodOrConstructor/java:inClass ?class_ .
  }

}
}
''' % NS_TBL

Q_RM_CLASS_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveClass:", ?fqn) AS ?name)
(?class AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?ctxx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?ctx_ ?cname ?fqn ?x ?ctxx_ ?xname
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
    WHERE {

      {
        SELECT DISTINCT ?class ?ctx_ ?cname ?fqn ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
        WHERE {

          ?class a java:TypeDeclaration ;
                 java:name ?cname ;
                 java:fullyQualifiedName ?fqn ;
                 chg:removal ?ctx_ .

          FILTER NOT EXISTS {
            ?class chg:mappedTo ?class_ .
          }

          BIND (CONCAT(?fqn, ".") AS ?pat0)
          BIND (CONCAT(?cname, ".") AS ?pat1)
          BIND (CONCAT(?fqn, "$$") AS ?pat2)
          BIND (CONCAT(?cname, "$$") AS ?pat3)
          BIND (CONCAT(?fqn, "<") AS ?pat4)
          BIND (CONCAT(?cname, "<") AS ?pat5)

        } GROUP BY ?class ?ctx_ ?cname ?fqn ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
      }

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:name ?xname ;
         chg:removal ?ctxx_ .

      FILTER EXISTS {
        ?class ver:version ?ver .
        ?x src:parent+/ver:version ?ver .
      }

    } GROUP BY ?class ?ctx_ ?cname ?fqn ?x ?ctxx_ ?xname ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
  }

  FILTER (?xname = ?fqn ||
          #?xname = ?cname ||
          STRSTARTS(?xname, ?pat0) ||
          #STRSTARTS(?xname, ?pat1) ||
          STRSTARTS(?xname, ?pat2) ||
          #STRSTARTS(?xname, ?pat3) ||
          STRSTARTS(?xname, ?pat4)# ||
          #STRSTARTS(?xname, ?pat5)
          )

}
}
''' % NS_TBL

Q_ADD_CLASS_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddClass:", ?fqn_) AS ?name)
(?ctx AS ?key) (?class_ AS ?key_)
(?ctx AS ?dep) (?class_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class_ ?cname_ ?fqn_ ?ctx ?x ?x_ ?xname_
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
    WHERE {

      {
        SELECT DISTINCT ?class_ ?cname_ ?fqn_ ?ctx ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
        WHERE {

          ?class_ a java:TypeDeclaration ;
                  java:name ?cname_ ;
                  java:fullyQualifiedName ?fqn_ ;
                  chg:addition ?ctx .

          FILTER NOT EXISTS {
            ?class chg:mappedTo ?class_ .
          }

          BIND (CONCAT(?fqn_, ".") AS ?pat0)
          BIND (CONCAT(?cname_, ".") AS ?pat1)
          BIND (CONCAT(?fqn_, "$$") AS ?pat2)
          BIND (CONCAT(?cname_, "$$") AS ?pat3)
          BIND (CONCAT(?fqn_, "<") AS ?pat4)
          BIND (CONCAT(?cname_, "<") AS ?pat5)

        } GROUP BY ?class_ ?cname_ ?fqn_ ?ctx ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
      }

      ?x_ a ?cat OPTION (INFERENCE NONE) ;
          java:name ?xname_ .

      ?x chg:relabeled ?x_ .

      FILTER EXISTS {
        ?class_ ver:version ?ver_ .
        ?x_ src:parent+/ver:version ?ver_ .
      }

      FILTER NOT EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x ;
           delta:entity2 ?x_ .
      }

    } GROUP BY ?class_ ?cname_ ?fqn_ ?ctx ?x ?x_ ?xname_ ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
  }

  FILTER (?xname_ = ?fqn_ ||
          #?xname_ = ?cname_ ||
          STRSTARTS(?xname_, ?pat0) ||
          #STRSTARTS(?xname_, ?pat1) ||
          STRSTARTS(?xname_, ?pat2) ||
          #STRSTARTS(?xname_, ?pat3) ||
          STRSTARTS(?xname_, ?pat4)# ||
          #STRSTARTS(?xname_, ?pat5)
          )

}
}
''' % NS_TBL

Q_CHG_CLASS_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeClass:", ?fqn) AS ?name)
(?class AS ?key) (?class_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?x ?x_ ?xname ?xname_ ?cat
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
    WHERE {

      {
        SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_
        ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
        WHERE {

          ?class a java:TypeDeclaration ;
                 java:name ?cname ;
                 java:fullyQualifiedName ?fqn ;
                 chg:relabeled ?class_ .

          ?class_ a java:TypeDeclaration ;
                  java:name ?cname_ ;
                  java:fullyQualifiedName ?fqn_ .

          BIND (CONCAT(?fqn, ".") AS ?pat0)
          BIND (CONCAT(?fqn, "$$") AS ?pat1)
          BIND (CONCAT(?fqn, "<") AS ?pat2)

          BIND (CONCAT(?fqn_, ".") AS ?pat3)
          BIND (CONCAT(?fqn_, "$$") AS ?pat4)
          BIND (CONCAT(?fqn_, "<") AS ?pat5)

        } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_
        ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
      }

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:name ?xname ;
         chg:relabeled ?x_ .

      ?x_ java:name ?xname_ .

      FILTER EXISTS {
        ?class ver:version ?ver .
        ?x src:parent+/ver:version ?ver .
      }
      FILTER EXISTS {
        ?class_ ver:version ?ver_ .
        ?x_ src:parent+/ver:version ?ver_ .
      }

    } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?x ?x_ ?xname ?xname_ ?cat
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
  }

  FILTER (?xname = ?fqn ||
          ?xname_ = ?fqn_ ||
          STRSTARTS(?xname, ?pat0) ||
          STRSTARTS(?xname, ?pat1) ||
          STRSTARTS(?xname, ?pat2) ||
          STRSTARTS(?xname_, ?pat3) ||
          STRSTARTS(?xname_, ?pat4) ||
          STRSTARTS(?xname_, ?pat5)
          )

}
}
''' % NS_TBL

Q_CHG_CLASS_CHG_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeClass:", ?fqn) AS ?name)
(?class AS ?key) (?class_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?fqn0 ?fqn0_ ?ctor_fqn ?ctor_fqn_
    ?ver ?ver_
    WHERE {
      ?class a java:TypeDeclaration ;
             ver:version ?ver ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn0 ;
              chg:relabeled ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn0_ .

      BIND (REPLACE(?fqn0, "[$$]", ".") AS ?fqn)
      BIND (REPLACE(?fqn0_, "[$$]", ".") AS ?fqn_)

      BIND (CONCAT(?fqn0, ".<init>") AS ?ctor_fqn)
      BIND (CONCAT(?fqn0_, ".<init>") AS ?ctor_fqn_)

    } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?fqn0 ?fqn0_ ?ctor_fqn ?ctor_fqn_
    ?ver ?ver_
  }

  {
    ?x a java:ConstructorDeclaration ;
       java:inTypeDeclaration ?class ;
       java:fullyQualifiedName ?ctor_fqn0 ;
       chg:relabeled ?x_ .

    ?x_ a java:ConstructorDeclaration ;
        java:inTypeDeclaration/ver:version ?ver_ .
  }
  UNION
  {
    ?x_ a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?class_ ;
        java:fullyQualifiedName ?ctor_fqn0_ ;
        ^chg:relabeled ?x .

    ?x a java:ConstructorDeclaration ;
       java:inTypeDeclaration/ver:version ?ver .
  }

}
}
''' % NS_TBL

Q_CHG_CLASS_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeClass:", ?fqn) AS ?name)
(?class AS ?key) (?class_ AS ?key_)
(?x AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?x ?ctx_ ?xname ?cat
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
    WHERE {

      {
        SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_
        ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
        WHERE {

          ?class a java:TypeDeclaration ;
                 java:name ?cname ;
                 java:fullyQualifiedName ?fqn ;
                 chg:relabeled ?class_ .

          ?class_ a java:TypeDeclaration ;
                  java:name ?cname_ ;
                  java:fullyQualifiedName ?fqn_ .

          BIND (CONCAT(?fqn, ".") AS ?pat0)
          BIND (CONCAT(?fqn, "$$") AS ?pat1)
          BIND (CONCAT(?fqn, "<") AS ?pat2)

          BIND (CONCAT(?fqn_, ".") AS ?pat3)
          BIND (CONCAT(?fqn_, "$$") AS ?pat4)
          BIND (CONCAT(?fqn_, "<") AS ?pat5)

        } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_
        ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
      }

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:name ?xname ;
         chg:removal ?ctx_ .

      FILTER EXISTS {
        ?class ver:version ?ver .
        ?x src:parent+/ver:version ?ver .
      }

    } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?x ?ctx_ ?xname ?cat
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
  }

  FILTER (?xname = ?fqn ||
          STRSTARTS(?xname, ?pat0) ||
          STRSTARTS(?xname, ?pat1) ||
          STRSTARTS(?xname, ?pat2)
          )

}
}
''' % NS_TBL

Q_CHG_CLASS_RM_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeClass:", ?fqn) AS ?name)
(?class AS ?key) (?class_ AS ?key_)
(?x AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?fqn0 ?fqn0_ ?ctor_fqn ?ctor_fqn_
    ?ver ?ver_
    WHERE {
      ?class a java:TypeDeclaration ;
             ver:version ?ver ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn0 ;
              chg:relabeled ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn0_ .

      BIND (REPLACE(?fqn0, "[$$]", ".") AS ?fqn)
      BIND (REPLACE(?fqn0_, "[$$]", ".") AS ?fqn_)

      BIND (CONCAT(?fqn0, ".<init>") AS ?ctor_fqn)
      BIND (CONCAT(?fqn0_, ".<init>") AS ?ctor_fqn_)

    } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?fqn0 ?fqn0_ ?ctor_fqn ?ctor_fqn_
    ?ver ?ver_
  }

  ?x a java:ConstructorDeclaration ;
     java:inTypeDeclaration ?class ;
     java:fullyQualifiedName ?ctor_fqn0 ;
     chg:removal ?ctx_ .

  ?ctx_ src:parent*/ver:version ?ver_ .

}
}
''' % NS_TBL

Q_CHG_CLASS_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeClass:", ?fqn) AS ?name)
(?class AS ?key) (?class_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?x_ ?ctx ?xname_ ?cat_
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
    WHERE {

      {
        SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_
        ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
        WHERE {

          ?class a java:TypeDeclaration ;
                 java:name ?cname ;
                 java:fullyQualifiedName ?fqn ;
                 chg:relabeled ?class_ .

          ?class_ a java:TypeDeclaration ;
                  java:name ?cname_ ;
                  java:fullyQualifiedName ?fqn_ .

          BIND (CONCAT(?fqn, ".") AS ?pat0)
          BIND (CONCAT(?fqn, "$$") AS ?pat1)
          BIND (CONCAT(?fqn, "<") AS ?pat2)

          BIND (CONCAT(?fqn_, ".") AS ?pat3)
          BIND (CONCAT(?fqn_, "$$") AS ?pat4)
          BIND (CONCAT(?fqn_, "<") AS ?pat5)

        } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_
        ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
      }

      ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
          java:name ?xname_ ;
          chg:addition ?ctx .

      FILTER EXISTS {
        ?class_ ver:version ?ver_ .
        ?x_ src:parent+/ver:version ?ver_ .
      }

    } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?x_ ?ctx ?xname_ ?cat_
    ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
  }

  FILTER (?xname_ = ?fqn_ ||
          STRSTARTS(?xname_, ?pat3) ||
          STRSTARTS(?xname_, ?pat4) ||
          STRSTARTS(?xname_, ?pat5)
          )

}
}
''' % NS_TBL

Q_CHG_CLASS_ADD_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeClass:", ?fqn) AS ?name)
(?class AS ?key) (?class_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?fqn0 ?fqn0_ ?ctor_fqn ?ctor_fqn_
    ?ver ?ver_
    WHERE {
      ?class a java:TypeDeclaration ;
             ver:version ?ver ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn0 ;
              chg:relabeled ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn0_ .

      BIND (REPLACE(?fqn0, "[$$]", ".") AS ?fqn)
      BIND (REPLACE(?fqn0_, "[$$]", ".") AS ?fqn_)

      BIND (CONCAT(?fqn0, ".<init>") AS ?ctor_fqn)
      BIND (CONCAT(?fqn0_, ".<init>") AS ?ctor_fqn_)

    } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?fqn0 ?fqn0_ ?ctor_fqn ?ctor_fqn_
    ?ver ?ver_
  }

  ?x_ a java:ConstructorDeclaration ;
      java:inTypeDeclaration ?class_ ;
      java:fullyQualifiedName ?ctor_fqn0_ ;
      chg:addition ?ctx .

  ?ctx src:parent*/ver:version ?ver .

}
}
''' % NS_TBL

Q_CHG_CLASS_CHG_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeClass:", ?fqn) AS ?name)
(?class AS ?key) (?class_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?fqn ?fqn_ ?ver ?ver_
    WHERE {
      ?class a java:TypeDeclaration ;
             ver:version ?ver ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn ;
             chg:relabeled ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn_ .

    } GROUP BY ?class ?class_ ?fqn ?fqn_ ?ver ?ver_
  }

  ?x a java:ImportDeclaration ;
     java:name ?xname ;
     chg:relabeled ?x_ .

  ?x_ a java:ImportDeclaration ;
      java:name ?xname_ .

  FILTER EXISTS {
    ?x src:parent/src:parent/src:inFile/ver:version ?ver .
    ?x_ src:parent/src:parent/src:inFile/ver:version ?ver_ .
  }

  FILTER (?xname = STR(REPLACE(?fqn, "[$$]", ".")) ||
          ?xname_ = STR(REPLACE(?fqn_, "[$$]", ".")))

}
}
''' % NS_TBL

Q_ADD_CLASS_ADD_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddClass:", ?fqn) AS ?name)
(?ctx AS ?dep) (?class_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?class_ ?fqn_ ?ver_
    WHERE {

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:fullyQualifiedName ?fqn_ ;
              chg:addition ?ctx .

    } GROUP BY ?ctx ?class_ ?fqn_ ?ver_
  }

  ?x_ a java:ImportDeclaration ;
      java:name ?xname_ ;
      chg:addition ?ctxx .

  FILTER EXISTS {
    ?x_ src:parent/src:parent/src:inFile/ver:version ?ver_ .
  }

  FILTER ((?xname_ = ?fqn_) || (?xname_ = STR(REPLACE(?fqn_, "[$$]", "."))))

}
}
''' % NS_TBL

Q_RM_CLASS_RM_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveClass:", ?fqn) AS ?name)
(?import AS ?dep) (?ctxi_ AS ?dep_)
(?class AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?ctx_ ?fqn ?ver
    WHERE {

      ?class a java:TypeDeclaration ;
             ver:version ?ver ;
             java:fullyQualifiedName ?fqn ;
             chg:removal ?ctx_ .

    } GROUP BY ?class ?ctx_ ?fqn ?ver
  }

  {
    SELECT DISTINCT ?import ?ver ?iname ?ctxi_
    WHERE {
      ?import a java:ImportDeclaration ;
              src:parent/src:parent/src:inFile/ver:version ?ver ;
              java:name ?iname ;
              chg:removal ?ctxi_ .

    } GROUP BY ?import ?ver ?iname ?ctxi_
  }

  FILTER ((?iname = ?fqn) || (?iname = STR(REPLACE(?fqn, "[$$]", "."))))

}
}
''' % NS_TBL

Q_RM_IMPORT_RM_RTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveImport:", ?iname) AS ?name)
(?rty AS ?dep) (?ctx_ AS ?dep_)
(?import AS ?ent) (?ctxi_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?file ?iname ?ctxi_
    WHERE {
      ?import a java:ImportDeclaration ;
              src:parent/src:parent/src:inFile ?file ;
              java:name ?iname ;
              chg:removal ?ctxi_ .

    } GROUP BY ?import ?file ?iname ?ctxi_
  }

  {
    SELECT DISTINCT ?rty ?file ?rname ?ctx_
    WHERE {

      ?rty a java:ReferenceType ;
           java:inTypeDeclaration/src:inFile ?file ;
           java:name ?rname ;
           chg:removal ?ctx_ .

    } GROUP BY ?rty ?file ?rname ?ctx_
  }

  FILTER (?iname = ?rname ||
          STRSTARTS(?rname, CONCAT(?iname, "<")) ||
          STRENDS(?iname, CONCAT(".", ?rname)) ||
          ?iname = STR(REPLACE(?rname, "[$$]", "."))
          )

}
}
''' % NS_TBL

Q_ADD_IMPORT_ADD_RTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddImport:", ?iname_) AS ?name)
(?ctxi AS ?dep) (?import_ AS ?dep_)
(?ctx AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import_ ?file_ ?iname_ ?ctxi
    WHERE {

      ?import_ a java:SingleTypeImportDeclaration ;
               src:parent/src:parent/src:inFile ?file_ ;
               java:name ?iname_ ;
               chg:addition ?ctxi .

    } GROUP BY ?import_ ?file_ ?iname_ ?ctxi
  }

  {
    SELECT DISTINCT ?rty_ ?file_ ?rname_ ?ctx
    WHERE {

      ?rty_ a java:ReferenceType ;
            java:inTypeDeclaration/src:inFile ?file_ ;
            java:name ?rname_ ;
            chg:addition ?ctx .

    } GROUP BY ?rty_ ?file_ ?rname_ ?ctx
  }

  FILTER (?iname_ = ?rname_ ||
          STRSTARTS(?rname_, CONCAT(?iname_, "<")) ||
          STRENDS(?iname_, CONCAT(".", ?rname_)) ||
          ?iname_ = STR(REPLACE(?rname_, "[$$]", "."))
          )

}
}
''' % NS_TBL

Q_RM_IMPORT_CHG_RTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveImport:", ?iname) AS ?name)
(?rty AS ?dep) (?rty_ AS ?dep_)
(?import AS ?ent) (?ctxi_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?import ?file ?iname ?ctxi_
    WHERE {
      ?import a java:ImportDeclaration ;
              src:parent/src:parent/src:inFile ?file ;
              java:name ?iname ;
              chg:removal ?ctxi_ .

    } GROUP BY ?import ?file ?iname ?ctxi_
  }

  {
    SELECT DISTINCT ?rty ?file ?rname ?rty_
    WHERE {

      ?rty a java:ReferenceType ;
           java:inTypeDeclaration/src:inFile ?file ;
           java:name ?rname ;
           chg:relabeled ?rty_ .

    } GROUP BY ?rty ?file ?rname ?rty_
  }

  FILTER (?iname = ?rname ||
          STRENDS(?iname, CONCAT(".", ?rname)) ||
          ?iname = STR(REPLACE(?rname, "[$$]", "."))
          )

}
}
''' % NS_TBL

Q_RM_CLASS_CHG_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveClass:", ?fqn) AS ?name)
(?import AS ?dep) (?import_ AS ?dep_)
(?class AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?ctx_ ?fqn ?ver
    WHERE {

      ?class a java:TypeDeclaration ;
             ver:version ?ver ;
             java:fullyQualifiedName ?fqn ;
             chg:removal ?ctx_ .

    } GROUP BY ?class ?ctx_ ?fqn ?ver
  }

  {
    SELECT DISTINCT ?import ?ver ?iname ?import_
    WHERE {
      ?import a java:ImportDeclaration ;
              src:parent/src:parent/src:inFile/ver:version ?ver ;
              java:name ?iname ;
              chg:relabeled ?import_ .

    } GROUP BY ?import ?ver ?iname ?import_
  }

  FILTER ((?iname = ?fqn) || (?iname = STR(REPLACE(?fqn, "[$$]", "."))))

}
}
''' % NS_TBL

Q_ADD_CLASS_CHG_IMPORT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddClass:", ?fqn) AS ?name)
(?ctx AS ?dep) (?class_ AS ?dep_)
(?import AS ?ent) (?import_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class_ ?ctx ?fqn_ ?ver_
    WHERE {

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:fullyQualifiedName ?fqn_ ;
              chg:addition ?ctx .

    } GROUP BY ?class_ ?ctx ?fqn_ ?ver_
  }

  {
    SELECT DISTINCT ?import ?ver_ ?iname_ ?import_
    WHERE {
      ?import a java:ImportDeclaration ;
              src:parent/src:parent/src:inFile/ver:version ?ver ;
              java:name ?iname ;
              chg:relabeled ?import_ .

      ?import_ a java:ImportDeclaration ;
               src:parent/src:parent/src:inFile/ver:version ?ver_ ;
               java:name ?iname_ .


    } GROUP BY ?import ?ver_ ?iname_ ?import_
  }

  FILTER ((?iname_ = ?fqn_) || (?iname_ = STR(REPLACE(?fqn_, "[$$]", "."))))

}
}
''' % NS_TBL

Q_RM_CLASS_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveClass:", ?fqn) AS ?name)
#(?class AS ?key) (?ctx_ AS ?key_)
#(?x AS ?ent) (?x_ AS ?ent_)
(?class AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?ctx_ ?cname ?fqn ?x ?x_ ?xname ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
    WHERE {

      {
        SELECT DISTINCT ?class ?ctx_ ?cname ?fqn ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
        WHERE {

          ?class a java:ClassDeclaration ;
                 #ver:version ?ver ;
                 java:name ?cname ;
                 java:fullyQualifiedName ?fqn ;
                 chg:removal ?ctx_ .

          FILTER NOT EXISTS {
            ?class chg:mappedTo ?class_ .
          }

          BIND (CONCAT(?fqn, ".") AS ?pat0)
          BIND (CONCAT(?cname, ".") AS ?pat1)
          BIND (CONCAT(?fqn, "$$") AS ?pat2)
          BIND (CONCAT(?cname, "$$") AS ?pat3)
          BIND (CONCAT(?fqn, "<") AS ?pat4)
          BIND (CONCAT(?cname, "<") AS ?pat5)

        } GROUP BY ?class ?ctx_ ?cname ?fqn ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
      }

      ?x a ?cat OPTION (INFERENCE NONE) ;
         #src:parent+/ver:version ?ver ;
         java:name ?xname ;
         chg:relabeled ?x_ .

      FILTER EXISTS {
        ?class ver:version ?ver .
        ?x src:parent+/ver:version ?ver .
      }

    } GROUP BY ?class ?ctx_ ?cname ?fqn ?x ?x_ ?xname ?pat0 ?pat1 ?pat2 ?pat3 ?pat4 ?pat5
  }

  FILTER (?xname = ?fqn ||
          #?xname = ?cname ||
          STRSTARTS(?xname, ?pat0) ||
          #STRSTARTS(?xname, ?pat1) ||
          STRSTARTS(?xname, ?pat2) ||
          #STRSTARTS(?xname, ?pat3) ||
          STRSTARTS(?xname, ?pat4)# ||
          #STRSTARTS(?xname, ?pat5)
          )

}
}
''' % NS_TBL

Q_ADD_METH_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?sig_) AS ?name)
(?ctx AS ?key) (?meth_ AS ?key_)
(?ctx AS ?dep) (?meth_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?ver_ ?meth_ ?ctx ?sig_
    WHERE {
      ?meth_ a java:MethodOrConstructor ;
             java:inTypeDeclaration/ver:version ?ver_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ ;
             chg:addition ?ctx .

     ?ver ver:next ?ver_ .

      FILTER NOT EXISTS {
        ?meth chg:mappedStablyTo ?meth_ ;
              java:inTypeDeclaration/ver:version ?ver ;
              java:name ?mn .
        ?meth_ java:name ?mn .
      }

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ver ?ver_ ?meth_ ?ctx ?sig_
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        chg:addition ?ctxi .

  {
    ?ivk_ java:mayInvokeMethod ?meth_ .
  }
  UNION
  {
    ?ivk_ java:mayInvokeMethod ?meth0_ .
    ?meth0_ java:inTypeDeclaration/java:subClassOf+ ?tdecl_ .
    ?tdecl_ a java:InterfaceDeclaration .
    ?meth_ java:inTypeDeclaration ?tdecl_ .
  }

}
}
''' % NS_TBL

Q_CHG_METH_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?mfqn_, ?msig_) AS ?name)
(?meth AS ?dep) (?meth_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?meth ?mfqn_ ?msig_
    WHERE {
      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             ^chg:relabeled ?meth .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

    } GROUP BY ?meth_ ?meth ?mfqn_ ?msig_
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        chg:addition ?ctxi .

  {
    ?ivk_ java:mayInvokeMethod ?meth_ .
  }
  UNION
  {
    ?ivk_ java:mayInvokeMethod ?meth0_ .
    ?meth0_ java:inTypeDeclaration/java:subClassOf+ ?tdecl_ .
    ?tdecl_ a java:InterfaceDeclaration .
    ?meth_ java:inTypeDeclaration ?tdecl_ .
  }

}
}
''' % NS_TBL

Q_ADD_METH_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?sig_) AS ?name)
(?ctx AS ?key) (?meth_ AS ?key_)
(?ctx AS ?dep) (?meth_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?ver_ ?meth_ ?ctx ?sig_
    WHERE {
      ?meth_ a java:MethodOrConstructor ;
             java:inTypeDeclaration/ver:version ?ver_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ ;
             chg:addition ?ctx .

     ?ver ver:next ?ver_ .

      FILTER NOT EXISTS {
        ?meth chg:mappedStablyTo ?meth_ ;
              java:inTypeDeclaration/ver:version ?ver ;
              java:name ?mn .
        ?meth_ java:name ?mn .
      }

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ver ?ver_ ?meth_ ?ctx ?sig_
  }

  ?ivk a java:InvocationOrInstanceCreation .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:inMethodOrConstructor/java:fullyQualifiedName ?xxx_ .

  ?x src:parent? ?ivk ;
     chg:relabeled ?x_ .

  ?x_ src:parent? ?ivk_ .

  {
    ?ivk_ java:mayInvokeMethod ?meth_ .
  }
  UNION
  {
    ?ivk_ java:mayInvokeMethod ?meth0_ .
    ?meth0_ java:inTypeDeclaration/java:subClassOf+ ?tdecl_ .
    ?tdecl_ a java:InterfaceDeclaration .
    ?meth_ java:inTypeDeclaration ?tdecl_ .
  }

}
}
''' % NS_TBL

Q_RM_METH_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?ver_ ?meth ?ctx_ ?sig
    WHERE {
      ?meth a java:MethodOrConstructor ;
            java:inTypeDeclaration/ver:version ?ver ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:removal ?ctx_ .

    ?ver ver:next ?ver_ .

    FILTER NOT EXISTS {
      ?meth chg:mappedStablyTo ?meth_ ;
            java:name ?mn .
      ?meth_ java:inTypeDeclaration/ver:version ?ver_ ;
             java:name ?mn .
    }

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:originalMethod ?meth .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

    } GROUP BY ?ver ?ver_ ?meth ?ctx_ ?sig
  }

  ?ivk a java:InvocationOrInstanceCreation .

  ?ivk_ a java:InvocationOrInstanceCreation .

  ?x src:parent? ?ivk ;
     chg:relabeled ?x_ .

  ?x_ src:parent? ?ivk_ .

  {
     ?ivk java:mayInvokeMethod ?meth .
  }
  UNION
  {
    ?ivk java:mayInvokeMethod ?meth0 .
    ?meth0 java:inTypeDeclaration/java:subClassOf+ ?tdecl .
    ?tdecl a java:InterfaceDeclaration .
    ?meth java:inTypeDeclaration ?tdecl .
  }

}
}
''' % NS_TBL

Q_ADD_METH_ADD_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?sig_) AS ?name)
(?ctx AS ?dep) (?meth_ AS ?dep_)
(?ctxa AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration/ver:version ?ver_ ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ ;
         chg:addition ?ctx .

  ?ver ver:next ?ver_ .

  FILTER NOT EXISTS {
    ?meth chg:mappedStablyTo ?meth_ ;
          java:inTypeDeclaration/ver:version ?ver ;
          java:name ?mn .
    ?meth_ java:name ?mn .
  }
  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:movedMethod ?meth_ .
  }

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        chg:addition ?ctxa .

}
}
''' % NS_TBL

Q_ADD_METH_CHG_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?sig_) AS ?name)
(?ctx AS ?dep) (?meth_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration/ver:version ?ver_ ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ ;
         chg:addition ?ctx .

  ?ver ver:next ?ver_ .

  FILTER NOT EXISTS {
    ?meth chg:mappedStablyTo ?meth_ ;
          java:inTypeDeclaration/ver:version ?ver ;
          java:name ?mn .
    ?meth_ java:name ?mn .
  }
  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:movedMethod ?meth_ .
  }

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        ^chg:mappedTo ?arg .

  ?x src:parent* ?arg ;
     chg:relabeled ?x_ .

  ?x_ src:parent* ?arg_ .

}
}
''' % NS_TBL

Q_CHG_METH_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?sig) AS ?name)
(?meth AS ?key) (?meth_ AS ?key_)
(?meth AS ?dep) (?meth_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:relabeled ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ .

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:movedMethod ?meth_ .
  }

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctxi .

}
}
''' % NS_TBL

Q_CHG_METH_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?sig) AS ?name)
(?meth AS ?key) (?meth_ AS ?key_)
(?ivk AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {
      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:relabeled ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .
    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth ;
         jref:movedMethod ?meth_ .
  }

  {
    SELECT DISTINCT ?meth ?ivk
    WHERE {
      ?ivk a java:InvocationOrInstanceCreation ;
           java:mayInvokeMethod ?meth .
    } GROUP BY ?meth ?ivk
  }
  UNION
  {
    SELECT DISTINCT ?meth_ ?ivk_
    WHERE {
       ?ivk_ a java:InvocationOrInstanceCreation ;
             java:mayInvokeMethod ?meth_ .
    } GROUP BY ?sig_ ?meth_
  }

  ?ivk chg:relabeled ?ivk_ .

}
}
''' % NS_TBL

Q_CHG_ABS_METH_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAbstractMethod:", ?sig) AS ?name)
(?meth AS ?key) (?meth_ AS ?key_)
(?meth0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mname ?mname_ ?sig ?sig_ ?class ?class_
    WHERE {
      ?abst a java:Abstract ;
            java:inMethod ?meth ;
            chg:mappedTo ?abst_ .

      ?abst_ a java:Abstract ;
             java:inMethod ?meth_ .

      ?meth a java:MethodOrConstructor ;
            java:name ?mname ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:relabeled ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:name ?mname_ ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?mname ?mname_ ?sig ?sig_ ?class ?class_
  }

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth ;
         jref:movedMethod ?meth_ .
  }

  ?class0 java:subClassOf* ?class .
  ?class0_ java:subClassOf* ?class_ .

  {
    SELECT DISTINCT ?class0 ?class0_ ?meth0 ?meth0_ ?mname ?mname_ ?fqn0 ?fqn0_
    WHERE {

      ?meth0 a java:MethodDeclaration ;
             java:name ?mname ;
             java:fullyQualifiedName ?fqn0 ;
             src:child5 [] ;
             chg:relabeled ?meth0_ .

      {
        ?meth0 java:inTypeDeclaration ?class0 .
      }
      UNION
      {
        ?meth0 java:inInstanceCreation/java:ofReferenceType ?class0 .
      }

      ?meth0_ a java:MethodDeclaration ;
              java:name ?mname_ ;
              java:fullyQualifiedName ?fqn0_ ;
              src:child5 [] .

      {
        ?meth0_ java:inTypeDeclaration ?class0_ .
      }
      UNION
      {
        ?meth0_ java:inInstanceCreation/java:ofReferenceType ?class0_ .
      }

    } GROUP BY ?class0 ?class0_ ?meth0 ?meth0_ ?mname ?mname_ ?fqn0 ?fqn0_
  }

}
}
''' % NS_TBL

Q_CHG_METH_CHG_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?sig) AS ?name)
(?meth AS ?key) (?meth_ AS ?key_)
(?a AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {
      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:relabeled ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .
    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth ;
         jref:movedMethod ?meth_ .
  }

  {
    SELECT DISTINCT ?meth_ ?ivk_
    WHERE {
      ?ivk_ java:mayInvokeMethod ?meth_ .
    } GROUP BY ?meth_ ?ivk_
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       chg:mappedTo ?ivk_ .

  ?a src:parent+ ?ivk ;
     chg:relabeled ?a_ .

  ?a_ src:parent+ ?ivk_ .

}
}
''' % NS_TBL

Q_RM_METH_RM_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?ver_ ?meth ?ctx_ ?sig
    WHERE {
      ?meth a java:MethodOrConstructor ;
            java:inTypeDeclaration/ver:version ?ver ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:removal ?ctx_ .

    ?ver ver:next ?ver_ .

    FILTER NOT EXISTS {
      ?meth chg:mappedStablyTo ?meth_ ;
            java:name ?mn .
      ?meth_ java:inTypeDeclaration/ver:version ?ver_ ;
             java:name ?mn .
    }

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:originalMethod ?meth .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

    } GROUP BY ?ver ?ver_ ?meth ?ctx_ ?sig
  }

  ?ivk a java:InvocationOrInstanceCreation .

  ?x src:parent? ?ivk ;
     chg:removal ?ctxx_ .

  {
    ?ivk java:mayInvokeMethod ?meth .
  }
  UNION
  {
    ?ivk java:mayInvokeMethod ?meth0 .
    ?meth0 java:inTypeDeclaration/java:subClassOf+ ?tdecl .
    ?tdecl a java:InterfaceDeclaration .
    ?meth java:inTypeDeclaration ?tdecl .
  }

}
}
''' % NS_TBL

Q_RM_DEF_RM_USE_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(?def AS ?ent) (?ctxd_ AS ?ent_)
(?use AS ?dep) (?ctxu_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?def a java:VariableDeclarator ;
       chg:removal ?ctxd_ .

  ?use java:declaredBy ?vdtor ;
       chg:removal ?ctxu_ .

}
}
''' % NS_TBL

Q_ADD_USE_ADD_DEF_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(?ctxu AS ?ent) (?use_ AS ?ent_)
(?ctxd AS ?dep) (?def_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?def_ a java:VariableDeclarator ;
        chg:addition ?ctxd .

  ?use_ java:declaredBy ?vdtor ;
        chg:addition ?ctxu .

}
}
''' % NS_TBL

Q_RM_SUPER_IVK_RM_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperInvocation:", ?cfqn) AS ?name)
(?meth AS ?dep) (?ctxm_ AS ?dep_)
(?ivk AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ivk ?ctx_ ?meth0 ?cfqn
    WHERE {
      ?ivk a java:SuperInvocation ;
           src:child1 ?args ;
           java:mayInvokeMethod ?meth0 ;
           java:inConstructor ?ctor ;
           chg:removal ?ctx_ .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args .
      }

      ?ctor a java:ConstructorDeclaration ;
            java:fullyQualifiedName ?cfqn .

      FILTER NOT EXISTS {
        [] a java:Parameter ;
           src:parent/src:parent ?ctor .
      }
    } GROUP BY ?ivk ?ctx_ ?meth0 ?cfqn
  }

  ?meth0 a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?tdecl .

  ?meth a java:ConstructorDeclaration ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        java:inTypeDeclaration ?tdecl ;
        src:child2 ?params ;
        chg:removal ?ctxm_ .

  FILTER EXISTS {
    [] a java:Parameter ;
       src:parent ?params .
  }

  BIND (CONCAT(?mfqn, ?msig) AS ?sig) .

}
}
''' % NS_TBL

Q_RM_SUPER_IVK_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperInvocation:", ?cfqn) AS ?name)
(?ivk AS ?dep) (?ctx_ AS ?dep_)
(?sty AS ?ent) (?sty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?ivk ?ctx_ ?meth0 ?cfqn
    WHERE {
      ?ivk a java:SuperInvocation ;
           src:child1 ?args ;
           java:mayInvokeMethod ?meth0 ;
           java:inConstructor ?ctor ;
           chg:removal ?ctx_ .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args .
      }

      ?ctor a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?cfqn .

    } GROUP BY ?class ?ivk ?ctx_ ?meth0 ?cfqn
  }

  ?super a java:SuperType ;
         java:inTypeDeclaration ?class ;
         chg:mappedTo ?super_ .

  ?sty a java:ReferenceType ;
       src:parent ?super ;
       chg:relabeled ?sty_ .

}
}
''' % NS_TBL

Q_RM_SUPER_IVK_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperInvocation:", ?cfqn) AS ?name)
(?ivk AS ?dep) (?ctx_ AS ?dep_)
(?sty AS ?ent) (?ctxs_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?ivk ?ctx_ ?meth0 ?cfqn
    WHERE {
      ?ivk a java:SuperInvocation ;
           src:child1 ?args ;
           java:mayInvokeMethod ?meth0 ;
           java:inConstructor ?ctor ;
           chg:removal ?ctx_ .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args .
      }

      ?ctor a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?cfqn .

    } GROUP BY ?class ?ivk ?ctx_ ?meth0 ?cfqn
  }

  ?super a java:SuperType ;
         java:inTypeDeclaration ?class ;
         chg:mappedTo ?super_ .

  ?sty a java:ReferenceType ;
       src:parent ?super ;
       chg:removal ?ctxs_ .

}
}
''' % NS_TBL

Q_ADD_SUPER_IVK_ADD_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperInvocation:", ?cfqn_) AS ?name)
(?ctx AS ?dep) (?ivk_ AS ?dep_)
(?ctxm AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ivk_ ?ctx ?meth_ ?cfqn_
    WHERE {
      ?ivk_ a java:SuperInvocation ;
            src:child1 ?args_ ;
            java:mayInvokeMethod ?meth_ ;
            java:inConstructor ?ctor_ ;
            chg:addition ?ctx .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args_ .
      }

      ?ctor_ a java:ConstructorDeclaration ;
             java:fullyQualifiedName ?cfqn_ .

      FILTER NOT EXISTS {
        [] a java:Parameter ;
           src:parent/src:parent ?ctor_ .
      }
    } GROUP BY ?ivk_ ?ctx ?meth_ ?cfqn_
  }

  ?meth_ a java:ConstructorDeclaration ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ ;
         java:inTypeDeclaration ?tdecl_ ;
         src:child2 ?params_ ;
         chg:addition ?ctxm .

  FILTER EXISTS {
    [] a java:Parameter ;
       src:parent ?params_ .
  }

  BIND (CONCAT(?mfqn_, ?msig_) AS ?sig_) .

}
}
''' % NS_TBL

Q_ADD_SUPER_IVK_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperInvocation:", ?cfqn_) AS ?name)
(?sty AS ?dep) (?sty_ AS ?dep_)
(?ctx AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class_ ?ivk_ ?ctx ?meth_ ?cfqn_
    WHERE {
      ?ivk_ a java:SuperInvocation ;
            src:child1 ?args_ ;
            java:mayInvokeMethod ?meth_ ;
            java:inConstructor ?ctor_ ;
            chg:addition ?ctx .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args_ .
      }

      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?class_ ?ivk_ ?ctx ?meth_ ?cfqn_
  }

  ?super_ a java:SuperType ;
          java:inTypeDeclaration ?class_ ;
          ^chg:mappedTo ?super .

  ?sty_ a java:ReferenceType ;
        src:parent ?super_ ;
        ^chg:relabeled ?sty .

}
}
''' % NS_TBL

Q_ADD_SUPER_IVK_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperInvocation:", ?cfqn_) AS ?name)
(?ctxs AS ?dep) (?sty_ AS ?dep_)
(?ctx AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class_ ?ivk_ ?ctx ?meth_ ?cfqn_
    WHERE {
      ?ivk_ a java:SuperInvocation ;
            src:child1 ?args_ ;
            java:mayInvokeMethod ?meth_ ;
            java:inConstructor ?ctor_ ;
            chg:addition ?ctx .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args_ .
      }

      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?class_ ?ivk_ ?ctx ?meth_ ?cfqn_
  }

  ?super_ a java:SuperType ;
          java:inTypeDeclaration ?class_ ;
          ^chg:mappedTo ?super .

  ?sty_ a java:ReferenceType ;
        src:parent ?super_ ;
        chg:addition ?ctxs .

}
}
''' % NS_TBL

Q_RM_CTOR_ADD_SUPER_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveConstructor:", ?sig) AS ?name)
(?ctx AS ?dep) (?ivk_ AS ?dep_)
(?meth AS ?ent) (?ctxm_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ivk_ ?ctx ?meth_ ?cfqn_
    WHERE {
      ?ivk_ a java:SuperInvocation ;
            src:child1 ?args_ ;
            java:mayInvokeMethod ?meth_ ;
            java:inConstructor ?ctor_ ;
            chg:addition ?ctx .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args_ .
      }

      ?ctor_ a java:ConstructorDeclaration ;
             java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?ivk_ ?ctx ?meth_ ?cfqn_
  }

  ?meth_ a java:ConstructorDeclaration ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ ;
         java:inTypeDeclaration ?tdecl_ ;
         src:child2 ?params_ .

  ?tdecl chg:mappedTo ?tdecl_ .

  ?meth a java:ConstructorDeclaration ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        java:inTypeDeclaration ?tdecl ;
        chg:removal ?ctxm_ .

  FILTER NOT EXISTS {
    [] a java:Parameter ;
       src:parent/src:parent ?meth .
  }

  BIND (CONCAT(?mfqn, ?msig) AS ?sig) .
  BIND (CONCAT(?mfqn_, ?msig_) AS ?sig_) .

}
}
''' % NS_TBL

Q_ADD_CTOR_RM_SUPER_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveConstructor:", ?sig) AS ?name)
(?ctxm AS ?dep) (?meth_ AS ?dep_)
(?ivk AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ivk ?ctx_ ?meth ?cfqn
    WHERE {
      ?ivk a java:SuperInvocation ;
           src:child1 ?args ;
           java:mayInvokeMethod ?meth ;
           java:inConstructor ?ctor ;
           chg:removal ?ctx_ .

      FILTER EXISTS {
        [] a java:Expression ;
           src:parent ?args .
      }

      ?ctor a java:ConstructorDeclaration ;
            java:fullyQualifiedName ?cfqn .

    } GROUP BY ?ivk ?ctx_ ?meth ?cfqn
  }

  ?meth a java:ConstructorDeclaration ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        java:inTypeDeclaration ?tdecl ;
        src:child2 ?params .

  ?tdecl chg:mappedTo ?tdecl_ .

  ?meth_ a java:ConstructorDeclaration ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ ;
         java:inTypeDeclaration ?tdecl_ ;
         chg:addition ?ctxm .

  FILTER NOT EXISTS {
    [] a java:Parameter ;
       src:parent/src:parent ?meth_ .
  }

  BIND (CONCAT(?mfqn, ?msig) AS ?sig) .
  BIND (CONCAT(?mfqn_, ?msig_) AS ?sig_) .

}
}
''' % NS_TBL

Q_CHG_METH_RM_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?sig) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?meth AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:relabeled ?meth_ .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?ivk a java:InvocationOrInstanceCreation .

  ?x src:parent? ?ivk ;
     chg:removal ?ctxx_ .

  {
    ?ivk java:mayInvokeMethod ?meth .
  }
  UNION
  {
    ?ivk java:mayInvokeMethod ?meth0 .
    ?meth0 java:inTypeDeclaration/java:subClassOf+ ?tdecl .
    ?tdecl a java:InterfaceDeclaration .
    ?meth java:inTypeDeclaration ?tdecl .
  }

}
}
''' % NS_TBL

Q_RM_METH_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?meth AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration ?class ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:removal ?ctx_ .

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration ?class_ ;
         java:name ?mname ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0 ;
         chg:addition ?ctx .

  ?class chg:mappedTo ?class_ .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

}
}
''' % NS_TBL

Q_RM_METH_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?meth AS ?key) (?ctx_ AS ?key_)
(?meth0 AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?ver_ ?class ?class_ ?meth ?ctx_ ?mname ?mfqn ?msig ?sig
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:inTypeDeclaration/ver:version ?ver ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:removal ?ctx_ .

     ?ver ver:next ?ver_ .

      BIND (CONCAT(?mfqn, ?msig) AS ?sig) .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER NOT EXISTS {
        ?meth chg:mappedStablyTo ?meth_ ;
              java:name ?mn .
        ?meth_ java:inTypeDeclaration/ver:version ?ver_ ;
               java:name ?mn .
      }
      FILTER NOT EXISTS {
        [] a jref:MoveMethod ;
           jref:originalMethod ?meth .
      }

    } GROUP BY ?ver ?ver_ ?class ?class_ ?meth ?ctx_ ?mname ?mfqn ?msig ?sig
  }

  ?ivk java:mayInvokeMethod ?meth ;
       chg:mappedStablyTo ?ivk_ .

  ?ivk_ java:mayInvokeMethod ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration ?class_ ;
         java:name ?mname ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig ;
         ^chg:relabeled ?meth0 .

  ?meth0 a java:MethodOrConstructor ;
         java:name ?mname0 ;
         java:fullyQualifiedName ?mfqn0 .

}
}
''' % NS_TBL

Q_RM_METH_ADD_METH_2_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?meth AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration ?class ;
        java:name ?mname ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        chg:removal ?ctx_ .

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration ?class_ ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ ;
         chg:addition ?ctx .

  ?stmt a java:Statement ;
        java:inMethodOrConstructor ?meth ;
        chg:mappedStablyTo ?stmt_ .

  ?stmt_ a java:Statement ;
         java:inMethodOrConstructor ?meth_ .

  BIND (CONCAT(?mfqn, ?msig) AS ?sig) .
  BIND (CONCAT(?mfqn_, ?msig_) AS ?sig_) .

}
}
''' % NS_TBL

Q_ADD_METH_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?sig_) AS ?name)
(?ctx AS ?key) (?meth_ AS ?key_)
(?ctx AS ?dep) (?meth_ AS ?dep_)
(?ivk AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth_ a java:MethodOrConstructor ;
         java:inTypeDeclaration/ver:version ?ver_ ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ ;
         chg:addition ?ctx .

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ver ver:next ?ver_ .

  FILTER NOT EXISTS {
    ?meth chg:mappedStablyTo ?meth_ ;
          java:inTypeDeclaration/ver:version ?ver ;
          java:name ?mn .
    ?meth_ java:name ?mn .
  }
  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:movedMethod ?meth_ .
  }

  ?ivk chg:relabeled ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ .

}
}
''' % NS_TBL

Q_ADD_METH_CHG_SUPER_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?fqn_) AS ?name)
(?ctx AS ?key) (?meth_ AS ?key_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth_ a java:MethodDeclaration ;
         java:name ?mname_ ;
         java:fullyQualifiedName ?fqn_ ;
         java:inClass ?class_ ;
         chg:addition ?ctx .

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?impl_
    WHERE {

      ?class a java:ClassDeclaration ;
             java:name ?cname ;
             chg:mappedTo ?class_ .

      ?class_ a java:ClassDeclaration ;
              java:name ?cname_ .

      ?impl_ a java:Implements ;
             java:inClass ?class_ .

    } GROUP BY ?class ?class_ ?cname ?cname_ ?impl_
  }

  ?rty a java:ReferenceType ;
       java:name ?rty_name ;
       java:inClass ?class ;
       chg:relabeled ?rty_ .

  ?rty_ a java:ReferenceType ;
        src:parent ?impl_ ;
        java:name ?rty_name_ .

  ?iface_ a java:InterfaceDeclaration ;
                ver:version ?ver_ ;
                java:fullyQualifiedName ?rty_name_ .

  ?super_meth_ a java:MethodDeclaration ;
               java:name ?mname_ ;
               java:inInterface ?iface_ .

}
}
''' % NS_TBL

Q_CHG_SUPER_DEL_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuper:", ?cfqn) AS ?name)
(?sup AS ?key) (?sup_ AS ?key_)
(?rty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cfqn ?cfqn_ ?sup ?sup_
    WHERE {

      ?class a java:ClassDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:ClassDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      ?sup a java:SuperType ;
            src:parent/src:parent ?class ;
            chg:relabeled ?ext_ .

      ?sup_ a java:SuperType ;
            src:parent/src:parent ?class_ .

    } GROUP BY ?class ?class_ ?cfqn ?cfqn_ ?sup ?sup_
  }

  ?rty a java:ReferenceType ;
       src:parent ?sup ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_SUPER_INS_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuper:", ?cfqn_) AS ?name)
(?sup AS ?key) (?sup_ AS ?key_)
(?ctx AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cfqn ?cfqn_ ?sup ?sup_
    WHERE {

      ?class a java:ClassDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:ClassDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      ?sup a java:SuperType ;
            src:parent/src:parent ?class ;
            chg:relabeled ?ext_ .

      ?sup_ a java:SuperType ;
            src:parent/src:parent ?class_ .

    } GROUP BY ?class ?class_ ?cfqn ?cfqn_ ?sup ?sup_
  }

  ?rty_ a java:ReferenceType ;
        src:parent ?sup_ ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_METH_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
#(?meth AS ?key) (?ctx_ AS ?key_)
#(?ivk AS ?ent) (?ivk_ AS ?ent_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
(?ivk AS ?dep) (?ivk_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration/ver:version ?ver ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:removal ?ctx_ .

  ?ver ver:next ?ver_ .

  FILTER NOT EXISTS {
    ?meth chg:mappedStablyTo ?meth_ ;
          java:name ?mn .
    ?meth_ java:inTypeDeclaration/ver:version ?ver_ ;
           java:name ?mn .
  }
  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth .
  }

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth ;
       chg:relabeled ?ivk_ .

}
}
''' % NS_TBL

Q_RM_METH_RM_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?arg AS ?dep) (?ctxa_ AS ?dep_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration/ver:version ?ver ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:removal ?ctx_ .

  ?ver ver:next ?ver_ .

  FILTER NOT EXISTS {
    ?meth chg:mappedStablyTo ?meth_ ;
          java:name ?mn .
    ?meth_ java:inTypeDeclaration/ver:version ?ver_ ;
           java:name ?mn .
  }
  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth .
  }

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth .

  ?arg a java:Expression ;
       src:parent ?args ;
       chg:removal ?ctxa_ .

  ?args a java:Arguments ;
        src:parent ?ivk .

}
}
''' % NS_TBL

Q_RM_METH_CHG_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration/ver:version ?ver ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:removal ?ctx_ .

  ?ver ver:next ?ver_ .

  FILTER NOT EXISTS {
    ?meth chg:mappedStablyTo ?meth_ ;
          java:name ?mn .
    ?meth_ java:inTypeDeclaration/ver:version ?ver_ ;
           java:name ?mn .
  }
  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth .
  }

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth .

  ?arg a java:Expression ;
       src:parent ?args ;
       chg:mappedTo ?arg_ .

  ?args a java:Arguments ;
        src:parent ?ivk .

  ?x src:parent* ?arg ;
     chg:relabeled ?x_ .

  ?x_ src:parent* ?arg_ .

}
}
''' % NS_TBL

Q_RM_METH_ADD_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?sig) AS ?name)
(?ctxa AS ?dep) (?arg_ AS ?dep_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration/ver:version ?ver ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:removal ?ctx_ .

  ?ver ver:next ?ver_ .

  FILTER NOT EXISTS {
    ?meth chg:mappedStablyTo ?meth_ ;
          java:name ?mn .
    ?meth_ java:inTypeDeclaration/ver:version ?ver_ ;
           java:name ?mn .
  }
  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth .
  }

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth ;
       chg:mappedTo ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        chg:addition ?ctxa .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

}
}
''' % NS_TBL

Q_CHG_METH_ADD_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?sig) AS ?name)
(?ctxa AS ?dep) (?arg_ AS ?dep_)
(?meth AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:relabeled ?meth_ .

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth .
  }

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth ;
       chg:mappedTo ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        chg:addition ?ctxa .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

}
}
''' % NS_TBL

Q_CHG_METH_RM_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?sig) AS ?name)
(?arg AS ?dep) (?ctxa_ AS ?dep_)
(?meth AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:relabeled ?meth_ .

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth .
  }

  BIND (CONCAT(?fqn, ?sig0) AS ?sig) .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth .

  ?arg a java:Expression ;
       src:parent ?args ;
       chg:removal ?ctxa_ .

  ?args a java:Arguments ;
        src:parent ?ivk .

}
}
''' % NS_TBL

Q_ADD_FIELD_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddField:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field_ a java:FieldDeclaration ;
          java:fullyQualifiedName ?fqn_ ;
          java:inTypeDeclaration/ver:version ?ver_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:inField ?field_ ;
          java:name ?fname_ ;
          chg:addition ?ctx .

  FILTER NOT EXISTS {
    [] chg:mappedStablyTo ?vdtor_ .
  }

  ?x_ java:declaredBy ?vdtor_ ;
      java:inTypeDeclaration/ver:version ?ver_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_ADD_FIELD_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddField:", ?fqn_) AS ?name)
(?ctx AS ?key) (?vdtor_ AS ?key_)
(?ctxa AS ?ent) (?assign_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl_ ?field_ ?ctx ?vdtor_ ?fname_ ?tyname_ ?ver_
    WHERE {

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl0_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ ;
              chg:addition ?ctx .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo ?vdtor_ .
      }
      # FILTER NOT EXISTS {
      #   ?ref a jref:MoveField ;
      #        jref:movedField ?field_ .
      # }

      ?tdecl_ java:subClassOf* ?tdecl0_ ;
              java:fullyQualifiedName ?tyname_ ;
              ver:version ?ver_ .

    } GROUP BY ?tdecl_ ?field_ ?ctx ?vdtor_ ?fname_ ?tyname_ ?ver_
  }

  BIND(CONCAT(?tyname_, ".", ?fname_) AS ?fqn_)


  ?assign_ a java:AssignStatement ;
           java:inConstructor/java:inTypeDeclaration ?tdecl_ ;
           src:child0 ?x_ ;
           chg:addition ?ctxa .

  ?x_ a java:FieldAccess ;
      java:name ?fname_ .

  FILTER (EXISTS {
    [] a java:This ;
       src:parent ?x_ .
  } || NOT EXISTS {
    [] src:parent ?x_ .
  })

}
}
''' % NS_TBL

Q_CHG_FIELD_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeField:", ?fqn_) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?ctxa AS ?ent) (?assign_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl_ ?vdtor ?vdtor_ ?fname_ ?tyname_ ?ver_
    WHERE {

      ?field a java:FieldDeclaration ;
             chg:mappedTo ?field_ .

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl0_ .

      ?vdtor a java:VariableDeclarator ;
              java:inField ?field ;
              chg:relabeled ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

      ?tdecl_ java:subClassOf* ?tdecl0_ ;
              java:fullyQualifiedName ?tyname_ ;
              ver:version ?ver_ .

    } GROUP BY ?tdecl_ ?vdtor ?vdtor_ ?fname_ ?tyname_ ?ver_
  }

  BIND(CONCAT(?tyname_, ".", ?fname_) AS ?fqn_)


  ?assign_ a java:AssignStatement ;
           java:inConstructor ?ctor_ ;
           src:child0 ?x_ ;
           chg:addition ?ctxa .

  ?x_ a java:FieldAccess ;
      java:inTypeDeclaration ?tdecl_ ;
      java:name ?fname_ .

  FILTER (EXISTS {
    [] a java:This ;
       src:parent ?x_ .
  } || NOT EXISTS {
    [] src:parent ?x_ .
  })

}
}
''' % NS_TBL

Q_RM_FIELD_RM_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn) AS ?name)
(?vdtor AS ?key) (?ctx_ AS ?key_)
(?assign AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?field ?ctx_ ?vdtor ?fname ?tyname ?ver
    WHERE {

      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl0 .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo ?vdtor_ .
      }
      FILTER NOT EXISTS {
        ?ref a jref:MoveField ;
             jref:originalField ?field .
      }

      ?tdecl java:subClassOf* ?tdecl0 ;
             java:fullyQualifiedName ?tyname ;
             ver:version ?ver .

    } GROUP BY ?tdecl ?field ?ctx_ ?vdtor ?fname ?tyname ?ver
  }

  BIND(CONCAT(?tyname, ".", ?fname) AS ?fqn)


  ?assign a java:AssignStatement ;
          java:inConstructor/java:inTypeDeclaration ?tdecl ;
          src:child0 ?x ;
          chg:removal ?ctxa_ .

  ?x a java:FieldAccess ;
     java:name ?fname .

  FILTER (EXISTS {
    [] a java:This ;
       src:parent ?x .
  } || NOT EXISTS {
    [] src:parent ?x .
  })

}
}
''' % NS_TBL

Q_CHG_FIELD_RM_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeField:", ?fqn) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?assign AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?field ?vdtor ?vdtor_ ?fname ?tyname ?ver
    WHERE {

      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl0 ;
             chg:mappedTo ?field_ .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:relabeled ?vdtor_ .

      ?vdtor_ java:inField ?field_ .

      ?tdecl java:subClassOf* ?tdecl0 ;
             java:fullyQualifiedName ?tyname ;
             ver:version ?ver .

    } GROUP BY ?tdecl ?field ?vdtor ?vdtor_ ?fname ?tyname ?ver
  }

  BIND(CONCAT(?tyname, ".", ?fname) AS ?fqn)


  ?assign a java:AssignStatement ;
          java:inConstructor ?ctor ;
          src:child0 ?x ;
          chg:removal ?ctxa_ .

  ?x a java:FieldAccess ;
     java:inTypeDeclaration ?tdecl ;
     java:name ?fname .

  FILTER (EXISTS {
    [] a java:This ;
       src:parent ?x .
  } || NOT EXISTS {
    [] src:parent ?x .
  })

}
}
''' % NS_TBL

Q_RM_FIELD_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field a java:FieldDeclaration ;
         java:fullyQualifiedName ?fqn ;
         java:inTypeDeclaration/ver:version ?ver .

  ?vdtor a java:VariableDeclarator ;
         java:inField ?field ;
         java:name ?fname ;
         chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?vdtor chg:mappedStablyTo ?vdtor_ .
  }

  ?x java:declaredBy ?vdtor ;
     java:inTypeDeclaration/ver:version ?ver ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_RM_FIELD_ADD_OBJ_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn) AS ?name)
(?ctxe AS ?dep) (?e_ AS ?dep_)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?field ?ctx_ ?vdtor ?fname ?tyname ?tdecl_
    WHERE {

      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl0 .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo ?vdtor_ .
      }

      ?tdecl java:subClassOf* ?tdecl0 ;
             java:fullyQualifiedName ?tyname .

      ?tdecl0 chg:mappedTo ?tdecl0_ .

      ?tdecl_ java:subClassOf* ?tdecl0_ .

    } GROUP BY ?tdecl ?field ?ctx_ ?vdtor ?fname ?tyname ?tdecl_
  }

  BIND(CONCAT(?tyname, ".", ?fname) AS ?fqn)

  ?x_ a java:FieldAccess ;
      java:inTypeDeclaration ?tdecl_ ;
      java:name ?fname ;
      src:child0 ?e_ .

  ?e_ a java:Expression ;
      chg:addition ?ctxe .

  ?x a java:FieldAccess ;
     java:inTypeDeclaration ?tdecl ;
     java:name ?fname ;
     chg:mappedTo ?x_ .

  FILTER (EXISTS {
    [] a java:This ;
       src:parent ?x .
  } || NOT EXISTS {
    [] src:parent ?x .
  })

}
}
''' % NS_TBL

Q_ADD_FIELD_RM_OBJ_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddField:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?e AS ?ent) (?ctxe_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?tdecl_ ?field_ ?ctx ?vdtor_ ?fname_ ?tyname_
    WHERE {

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl0_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ ;
              chg:addition ?ctx .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo ?vdtor_ .
      }

      ?tdecl_ java:subClassOf* ?tdecl0_ ;
              java:fullyQualifiedName ?tyname_ .

      ?tdecl0 chg:mappedTo ?tdecl0_ .

      ?tdecl java:subClassOf* ?tdecl0 .

    } GROUP BY ?tdecl ?tdecl_ ?field_ ?ctx ?vdtor_ ?fname_ ?tyname_
  }

  BIND(CONCAT(?tyname_, ".", ?fname_) AS ?fqn_)

  ?x a java:FieldAccess ;
      java:inTypeDeclaration ?tdecl ;
      java:name ?fname_ ;
      src:child0 ?e ;
      chg:mappedTo ?x_ .

  ?e a java:Expression ;
     chg:removal ?ctxe_ .

  ?x_ a java:FieldAccess ;
      java:inTypeDeclaration ?tdecl_ ;
      java:name ?fname_ .

  FILTER (EXISTS {
    [] a java:This ;
       src:parent ?x_ .
  } || NOT EXISTS {
    [] src:parent ?x_ .
  })

}
}
''' % NS_TBL

Q_RM_FIELD_ADD_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn, ".", ?fname) AS ?name)
(?vdtor AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl java:fullyQualifiedName ?fqn .

  ?x a java:FieldAccess ;
     java:inTypeDeclaration ?tdecl ;
     java:declaredBy ?vdtor ;
     java:name ?fname ;
     chg:mappedStablyTo ?x_ .

  FILTER (EXISTS {
    ?x src:child0 [ a java:This ] .
  } || NOT EXISTS {
    ?x src:child0 [] .
  })

  ?x_ a java:FieldAccess ;
      java:inTypeDeclaration ?tdecl_ ;
      java:declaredBy ?vdtor_ ;
      java:name ?fname .

  {
    SELECT DISTINCT ?vdtor ?tdecl0 ?fname ?ctx_
    WHERE {

      ?field a java:FieldDeclaration ;
             src:child2 ?vdtor ;
             java:inTypeDeclaration ?tdecl0 .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo [] .
      }

    } GROUP BY ?vdtor ?tdecl0 ?fname ?ctx_
  }

  {
    SELECT DISTINCT ?vdtor_ ?tdecl0_ ?fname ?ctx
    WHERE {

      ?field_ a java:FieldDeclaration ;
              src:child2 ?vdtor_ ;
              java:inTypeDeclaration ?tdecl0_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname ;
              chg:addition ?ctx .

      FILTER NOT EXISTS {
        [] chg:mappedStablyTo ?vdtor_ .
      }

    } GROUP BY ?vdtor_ ?tdecl0_ ?fname ?ctx
  }

  ?tdecl0 chg:mappedTo ?tdecl0_ .

}
}
''' % NS_TBL

Q_RM_FIELD_CHG_OBJ_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn) AS ?name)
(?e AS ?dep) (?e_ AS ?dep_)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?field ?ctx_ ?vdtor ?fname ?tyname ?ver
    WHERE {

      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl0 .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo ?vdtor_ .
      }

      ?tdecl java:subClassOf* ?tdecl0 ;
             java:fullyQualifiedName ?tyname ;
             ver:version ?ver .

    } GROUP BY ?tdecl ?field ?ctx_ ?vdtor ?fname ?tyname ?ver
  }

  BIND(CONCAT(?tyname, ".", ?fname) AS ?fqn)


  ?x a java:FieldAccess ;
     java:inTypeDeclaration/ver:version ?ver ;
     java:name ?fname ;
     src:child0 ?e .

  ?e a java:Expression ;
     java:ofReferenceType/java:fullyQualifiedName ?tyname ;
     chg:relabeled ?e_ .

}
}
''' % NS_TBL

Q_CHG_FIELD_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeField:", ?fqn_) AS ?name)
(?vdtor AS ?dep) (?vdtor_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:inField ?field ;
         java:name ?fname ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:inField ?field_ ;
          java:name ?fname_ .

  ?field a java:FieldDeclaration ;
         chg:relabeled ?field_ .

  ?field_ a java:FieldDeclaration ;
          java:fullyQualifiedName ?fqn_ ;
          java:inTypeDeclaration/ver:version ?ver_ .

  ?x_ java:declaredBy ?vdtor_ ;
      java:inTypeDeclaration/ver:version ?ver_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_CHG_FIELD_TY_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType:", ?fqn_, ".", ?fname_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class_
    WHERE {
      ?field a java:FieldDeclaration ;
             chg:mappedTo ?field_ .

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?ty a java:Type ;
          a ?cat OPTION (INFERENCE NONE) ;
          java:inField ?field ;
          chg:relabeled ?ty_ .

      ?ty_ a java:Type ;
           java:inField ?field_ .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class_
  }

  # FILTER NOT EXISTS {
  #   ?ref a jref:MoveField ;
  #        jref:movedField ?field_ .
  # }

  ?subclass_ java:subClassOf* ?class_ ;
             java:fullyQualifiedName ?fqn_ .

  ?x_ a java:FieldAccess ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctxx ;
      java:inTypeDeclaration ?subclass_ ;
      java:name ?fname_ .

}
}
''' % NS_TBL

Q_CHG_FIELD_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeField:", ?fqn) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?vdtor AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:inField ?field ;
         java:name ?fname ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:inField ?field_ ;
          java:name ?fname_ .

  ?field a java:FieldDeclaration ;
         java:fullyQualifiedName ?fqn ;
         java:inTypeDeclaration/ver:version ?ver ;
         chg:relabeled ?field_ .

  ?field_ a java:FieldDeclaration .

  ?x java:declaredBy ?vdtor ;
     java:inTypeDeclaration/ver:version ?ver ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_CHG_FIELD_TY_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType:", ?fqn, ".", ?fname) AS ?name)
#(?ty AS ?key) (?ty_ AS ?key_)
#(?x AS ?ent) (?ctxx_ AS ?ent_)
(?ty AS ?ent) (?ty_ AS ?ent_)
(?x AS ?dep) (?ctxx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class
    WHERE {
      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?field_ .

      ?field_ a java:FieldDeclaration .

      ?ty a java:Type ;
          a ?cat OPTION (INFERENCE NONE) ;
          java:inField ?field ;
          chg:relabeled ?ty_ .

      ?ty_ a java:Type ;
           java:inField ?field_ .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class
  }

  # FILTER NOT EXISTS {
  #   ?ref a jref:MoveField ;
  #        jref:originalField ?field .
  # }

  ?subclass java:subClassOf* ?class ;
            java:fullyQualifiedName ?fqn .

  ?x a java:FieldAccess ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctxx_ ;
     java:inTypeDeclaration ?subclass ;
     java:name ?fname .

}
}
''' % NS_TBL

Q_RM_FIELD_TY_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFieldType:", ?fqn, ".", ?fname) AS ?name)
(?ty AS ?key) (?ctxt_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ctxt_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class
    WHERE {
      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?field_ .

      ?field_ a java:FieldDeclaration .

      ?ty a java:Type ;
          a ?cat OPTION (INFERENCE NONE) ;
          java:inField ?field ;
          chg:removal ?ctxt_ .

      ?ty_ a java:Type ;
           java:inField ?field_ .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

    } GROUP BY ?ty ?ctxt_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class
  }

  # FILTER NOT EXISTS {
  #   ?ref a jref:MoveField ;
  #        jref:originalField ?field .
  # }

  ?subclass java:subClassOf* ?class ;
            java:fullyQualifiedName ?fqn .

  ?x a java:FieldAccess ;
     java:declaredBy ?vdtor ;
     java:inTypeDeclaration ?subclass ;
     java:name ?fname ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_ADD_FIELD_TY_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFieldType:", ?fqn, ".", ?fname) AS ?name)
(?ctxt AS ?key) (?ty_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty_ ?ctxt ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class_
    WHERE {
      ?field a java:FieldDeclaration ;
             chg:mappedTo ?field_ .

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?ty a java:Type ;
          java:inField ?field .

      ?ty_ a java:Type ;
           java:inField ?field_ ;
           chg:addition ?ctxt .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

    } GROUP BY ?ty_ ?ctxt ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class_
  }

  # FILTER NOT EXISTS {
  #   ?ref a jref:MoveField ;
  #        jref:originalField ?field .
  # }

  ?subclass_ java:subClassOf* ?class_ ;
             java:fullyQualifiedName ?fqn_ .

  ?x_ a java:FieldAccess ;
      java:declaredBy ?vdtor_ ;
      java:inTypeDeclaration ?subclass_ ;
      java:name ?fname_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_CHG_ADD_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAddField:", ?tyname, ".", ?fname) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?ctx AS ?ent) (?field0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field a java:FieldDeclaration ;
         java:inTypeDeclaration ?tdecl ;
         chg:relabeled ?field_ .

  ?tdecl java:fullyQualifiedName ?tyname .

  ?vdtor a java:VariableDeclarator ;
         java:inField ?field ;
         java:name ?fname ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:inField ?field_ ;
          java:name ?fname_ .

  ?x a java:FieldAccess ;
     java:inTypeDeclaration ?tdecl ;
     java:name ?fname .

  ?x chg:mappedEqTo ?x_ ;
     chg:mappedStablyTo ?x_ .

  {
    SELECT DISTINCT ?ctx ?x_ ?tdecl_ ?fname ?field0_
    WHERE {

      ?x_ a java:FieldAccess ;
          java:inTypeDeclaration ?tdecl_ ;
          java:name ?fname .

      ?field0_ a java:FieldDeclaration ;
               java:name ?fname ;
               chg:addition ?ctx ;
               java:inTypeDeclaration ?tdecl0_ .

      FILTER EXISTS {
        ?tdecl_ java:subClassOf* ?tdecl0_ .
      }

    } GROUP BY ?ctx ?x_ ?tdecl_ ?fname ?field0_
  }

}
}
''' % NS_TBL


Q_ADD_FIELD_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddField:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field_ a java:FieldDeclaration ;
          java:fullyQualifiedName ?fqn_ ;
          java:inTypeDeclaration/ver:version ?ver_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:inField ?field_ ;
          java:name ?fname_ ;
          chg:addition ?ctx .

  FILTER NOT EXISTS {
    [] chg:mappedStablyTo ?vdtor_ .
  }

  ?x_ java:declaredBy ?vdtor_ ;
      java:inTypeDeclaration/ver:version ?ver_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_ADD_ENUMCONST_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddEnumConst:", ?fqn_) AS ?name)
(?ctx AS ?key) (?econst_ AS ?key_)
(?ctx AS ?dep) (?econst_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?enum_ ?econst_ ?ctx ?ename_ ?tyname_ ?ver_
    WHERE {

      ?econst_ a java:EnumConstant ;
               java:name ?ename_ ;
               java:inEnum ?enum_ ;
               chg:addition ?ctx .

      FILTER NOT EXISTS {
        ?econst chg:mappedStablyTo ?econst_ .
      }

      ?enum_ a java:EnumDeclaration ;
             java:fullyQualifiedName ?tyname_ ;
             src:inFile/ver:version ?ver_ .

    } GROUP BY ?enum_ ?econst_ ?ctx ?ename_ ?tyname_ ?ver_
  }

  BIND(CONCAT(?tyname_, ".", ?ename_) AS ?fqn_)

  ?x_ java:name ?xname_ ;
      java:inTypeDeclaration ?tdecl_ .

  ?tdecl_ java:name ?cname_ ;
          ver:version ?ver_ .

  ?x chg:relabeled ?x_ .

  FILTER (?xname_ IN (?fqn_, ?ename_))

}
}
''' % NS_TBL

Q_ADD_ENUMCONST_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddEnumConst:", ?fqn_) AS ?name)
(?ctx AS ?key) (?econst_ AS ?key_)
(?ctx AS ?dep) (?econst_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?enum_ ?econst_ ?ctx ?ename_ ?tyname_ ?ver_
    WHERE {

      ?econst_ a java:EnumConstant ;
               java:name ?ename_ ;
               java:inEnum ?enum_ ;
               chg:addition ?ctx .

      FILTER NOT EXISTS {
        ?econst chg:mappedStablyTo ?econst_ .
      }

      ?enum_ a java:EnumDeclaration ;
             java:fullyQualifiedName ?tyname_ ;
             src:inFile/ver:version ?ver_ .

    } GROUP BY ?enum_ ?econst_ ?ctx ?ename_ ?tyname_ ?ver_
  }

  BIND(CONCAT(?tyname_, ".", ?ename_) AS ?fqn_)

  ?x_ java:name ?xname_ ;
      java:inTypeDeclaration ?tdecl_ ;
      chg:addition ?ctxx .

  ?tdecl_ java:name ?cname_ ;
          ver:version ?ver_ .

  FILTER NOT EXISTS {
    ?x_ a java:EnumConstant .
  }

  FILTER (?xname_ IN (?fqn_, ?ename_))

}
}
''' % NS_TBL

Q_RM_FIELD_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn) AS ?name)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field a java:FieldDeclaration ;
         java:fullyQualifiedName ?fqn ;
         java:inTypeDeclaration/ver:version ?ver .

  ?vdtor a java:VariableDeclarator ;
         java:inField ?field ;
         java:name ?fname ;
         chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?vdtor chg:mappedStablyTo ?vdtor_ .
  }

  ?x java:declaredBy ?vdtor ;
     java:inTypeDeclaration/ver:version ?ver ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_RM_SUPERTY_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperType:", ?tyname) AS ?name)
(?rty AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?field ?rty ?ctx_ ?vdtor ?fname ?tyname ?ver ?tyname0
    WHERE {

      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl0 .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname .

      ?tdecl java:subClassOf+ ?tdecl0 ;
             java:fullyQualifiedName ?tyname ;
             ver:version ?ver .

      ?sty a java:SuperType ;
           src:parent/src:parent ?tdecl .

      ?rty a java:ReferenceType ;
           src:parent ?sty ;
           java:name ?tyname0 ;
           chg:removal ?ctx_ .

    } GROUP BY ?tdecl ?field ?rty ?ctx_ ?vdtor ?fname ?tyname ?ver ?tyname0
  }

  {
    ?x a java:FieldAccess ;
       java:inTypeDeclaration/ver:version ?ver ;
       java:name ?fname ;
       src:child0 ?e ;
       chg:relabeled ?x_ .

    ?e a java:Expression ;
       java:ofReferenceType/java:fullyQualifiedName ?tyname .
  }
  UNION
  {
    ?x a java:FieldAccess ;
       java:inTypeDeclaration ?tdecl ;
       java:name ?fname ;
       chg:relabeled ?x_ .

    FILTER (EXISTS {
      [] a java:This ;
         src:parent ?x .
    } || NOT EXISTS {
      [] src:parent ?x .
    })
  }
  UNION
  {
    ?x a java:Name ;
       java:inTypeDeclaration/ver:version ?ver ;
       java:name ?fqn ;
       chg:relabeled ?x_ .

    FILTER (?fqn = CONCAT(?tyname, ".", ?fname))
  }
  UNION
  {
    ?x a java:FieldAccess ;
       java:name ?fname ;
       java:inInstanceCreation ?new ;
       chg:relabeled ?x_ .

    ?new a java:InstanceCreation ;
         java:ofReferenceType ?tdecl .
  }

}
}
''' % NS_TBL

Q_ADD_SUPERTY_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperType:", ?tyname_) AS ?name)
(?ctx AS ?dep) (?rty_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl_ ?field_ ?rty_ ?ctx ?vdtor_ ?fname_ ?tyname_ ?ver_ ?tyname0_
    WHERE {

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl0_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

      ?tdecl_ java:subClassOf+ ?tdecl0_ ;
              java:fullyQualifiedName ?tyname_ ;
              ver:version ?ver_ .

      ?sty_ a java:SuperType ;
            src:parent/src:parent ?tdecl_ .

      ?rty_ a java:ReferenceType ;
            src:parent ?sty_ ;
            java:name ?tyname0_ ;
            chg:addition ?ctx .

    } GROUP BY ?tdecl_ ?field_ ?rty_ ?ctx ?vdtor_ ?fname_ ?tyname_ ?ver_ ?tyname0_
  }

  {
    ?x_ a java:FieldAccess ;
        java:inTypeDeclaration/ver:version ?ver_ ;
        java:name ?fname_ ;
        src:child0 ?e_ ;
        ^chg:relabeled ?x .

    ?e_ a java:Expression ;
        java:ofReferenceType/java:fullyQualifiedName ?tyname_ .
  }
  UNION
  {
    ?x_ a java:FieldAccess ;
        java:inTypeDeclaration ?tdecl_ ;
        java:name ?fname_ ;
        ^chg:relabeled ?x .

    FILTER (EXISTS {
      [] a java:This ;
         src:parent ?x_ .
    } || NOT EXISTS {
      [] src:parent ?x_ .
    })
  }
  UNION
  {
    ?x_ a java:Name ;
        java:inTypeDeclaration/ver:version ?ver_ ;
        java:name ?fqn_ ;
        ^chg:relabeled ?x .

    FILTER (?fqn_ = CONCAT(?tyname_, ".", ?fname_))
  }
  UNION
  {
    ?x_ a java:FieldAccess ;
        java:name ?fname_ ;
        java:inInstanceCreation ?new_ ;
        ^chg:relabeled ?x .

    ?new_ a java:InstanceCreation ;
          java:ofReferenceType ?tdecl_ .
  }

}
}
''' % NS_TBL

Q_RM_SUPERTY_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperType:", ?tyname0) AS ?name)
(?rty AS ?ent) (?ctx_ AS ?ent_)
(?ctx AS ?dep) (?meth_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rty ?ctx_ ?tyname0 ?tyname ?tdecl ?tdecl_ ?meth_ ?ctx ?mname ?sig_ ?sig0_
    WHERE {

      {
        SELECT DISTINCT ?rty ?ctx_ ?tyname0 ?tyname ?tdecl ?tdecl_
        WHERE {

          ?rty a java:ReferenceType ;
               src:parent ?sty ;
               java:name ?tyname0 ;
               chg:removal ?ctx_ .

          ?sty a java:SuperType ;
               src:parent/src:parent ?tdecl .

          ?tdecl a java:TypeDeclaration ;
                 java:fullyQualifiedName ?tyname ;
                 ver:version ?ver ;
                 chg:mappedTo ?tdecl_ .

        } GROUP BY ?rty ?ctx_ ?tyname0 ?tyname ?tdecl ?tdecl_
      }

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ ;
             java:name ?mname ;
             chg:addition ?ctx .

      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_)

    } GROUP BY ?rty ?ctx_ ?tyname0 ?tyname ?tdecl ?tdecl_ ?meth_ ?ctx ?mname ?sig_ ?sig0_
  }

  FILTER EXISTS {
    ?tdecl java:subTypeOf+ ?tdecl0 .

    ?tdecl0 a java:TypeDeclaration ;
            java:fullyQualifiedName ?tyname0 .

    ?meth0 a java:MethodDeclaration ;
           java:inTypeDeclaration ?tdecl0 ;
           java:name ?mname ;
           java:signature ?sig0_ .
  }

}
}
''' % NS_TBL

Q_RM_METH_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?cfqn, ".", ?mname, ?sig0) AS ?name)
(?meth AS ?dep) (?ctx_ AS ?dep_)
(?ctx0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?ctx_ ?mname ?sig0 ?tdecl ?tdecl_ ?cfqn ?cfqn_
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:name ?mname ;
            java:signature ?sig0 ;
            chg:removal ?ctx_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      FILTER (EXISTS {
        [] a java:Abstract ;
           java:inMethod ?meth .
      } || EXISTS {
        ?tdecl a java:InterfaceDeclaration .
      })

    } GROUP BY ?meth ?ctx_ ?mname ?sig0 ?tdecl ?tdecl_ ?cfqn ?cfqn_
  }

  {
    SELECT DISTINCT ?tdecl0_ ?ty0_ ?cfqn_ ?ctx0
    WHERE {

      ?super0_ a java:SuperType ;
               java:inTypeDeclaration ?tdecl0_ .

      ?ty0_ a java:ReferenceType ;
            java:name ?cfqn_ ;
            src:parent ?super0_ ;
            chg:addition ?ctx0 .

    } GROUP BY ?tdecl0_ ?ty0_ ?cfqn_ ?ctx0
  }

  ?tdecl_ ver:version ?ver_ .

  ?tdecl0_ a java:TypeDeclaration ;
           ver:version ?ver_ ;
           java:subTypeOf ?tdecl_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

  FILTER NOT EXISTS {
    [] a java:MethodDeclaration ;
       java:inTypeDeclaration ?tdecl0_ ;
       java:name ?mname ;
       java:signature ?sig0 .
  }

}
}
''' % NS_TBL

Q_ADD_METH_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?cfqn_, ".", ?mname, ?sig0) AS ?name)
(?ty0 AS ?dep) (?ctx0_ AS ?dep_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?ctx ?mname ?sig0 ?tdecl ?tdecl_ ?cfqn ?cfqn_
    ?ty0 ?ctx0_ ?tdecl0
    WHERE {

      {
        SELECT DISTINCT ?meth_ ?ctx ?mname ?sig0 ?tdecl ?tdecl_ ?cfqn ?cfqn_
        WHERE {

          ?meth_ a java:MethodDeclaration ;
                 java:inTypeDeclaration ?tdecl_ ;
                 java:name ?mname ;
                 java:signature ?sig0 ;
                 chg:addition ?ctx .

          ?tdecl_ a java:TypeDeclaration ;
                  java:fullyQualifiedName ?cfqn_ .

          ?tdecl a java:TypeDeclaration ;
                 java:fullyQualifiedName ?cfqn ;
                 chg:mappedTo ?tdecl_ .

          FILTER (EXISTS {
            [] a java:Abstract ;
               java:inMethod ?meth_ .
          } || EXISTS {
            ?tdecl_ a java:InterfaceDeclaration .
          })

        } GROUP BY ?meth_ ?ctx ?mname ?sig0 ?tdecl ?tdecl_ ?cfqn ?cfqn_
      }

      ?super0 a java:SuperType ;
              java:inTypeDeclaration ?tdecl0 .

      ?ty0 a java:ReferenceType ;
           java:name ?cfqn ;
           src:parent ?super0 ;
           chg:removal ?ctx0_ .

      ?tdecl0 java:subTypeOf+ ?tdecl .

    } GROUP BY ?meth_ ?ctx ?mname ?sig0 ?tdecl ?tdecl_ ?cfqn ?cfqn_
    ?ty0 ?ctx0_ ?tdecl0
  }

  FILTER NOT EXISTS {
    ?meth0 a java:MethodDeclaration ;
           java:inTypeDeclaration ?tdecl0 ;
           java:name ?mname ;
           java:signature ?sig0 .
  }

}
}
''' % NS_TBL

Q_ADD_SUPERTY_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperType:", ?tyname0_) AS ?name)
(?ctx AS ?dep) (?rty_ AS ?dep_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rty_ ?ctx ?tyname0_ ?tyname_ ?tdecl ?tdecl_ ?meth ?ctx_ ?mname ?sig ?sig0
    WHERE {

      {
        SELECT DISTINCT ?rty_ ?ctx ?tyname0_ ?tyname_ ?tdecl ?tdecl_
        WHERE {

      ?rty_ a java:ReferenceType ;
            src:parent ?sty_ ;
            java:name ?tyname0_ ;
            chg:addition ?ctx .

      ?sty_ a java:SuperType ;
            src:parent/src:parent ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?tyname_ ;
              ver:version ?ver_ .

      ?tdecl chg:mappedTo ?tdecl_ .

        } GROUP BY ?rty_ ?ctx ?tyname0_ ?tyname_ ?tdecl ?tdecl_
      }

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            java:name ?mname ;
            chg:removal ?ctx_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig)

    } GROUP BY ?rty_ ?ctx ?tyname0_ ?tyname_ ?tdecl ?tdecl_ ?meth ?ctx_ ?mname ?sig ?sig0
  }

  FILTER EXISTS {
    ?tdecl_ java:subTypeOf+ ?tdecl0_ .

    ?tdecl0_ a java:TypeDeclaration ;
             java:fullyQualifiedName ?tyname0_ .

    ?meth0_ a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl0_ ;
            java:name ?mname ;
            java:signature ?sig0 .
  }

}
}
''' % NS_TBL

Q_RM_ENUMCONST_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveEnumConst:", ?fqn) AS ?name)
(?econst AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?enum ?econst ?ctx_ ?ename ?tyname ?ver
    WHERE {

      ?econst a java:EnumConstant ;
              java:name ?ename ;
              java:inEnum ?enum ;
              chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?econst chg:mappedStablyTo ?econst_ .
      }

      ?enum a java:EnumDeclaration ;
            java:fullyQualifiedName ?tyname ;
            src:inFile/ver:version ?ver .

    } GROUP BY ?enum ?econst ?ctx_ ?ename ?tyname ?ver
  }

  BIND(CONCAT(?tyname, ".", ?ename) AS ?fqn)

  ?x java:name ?xname ;
     java:inTypeDeclaration ?tdecl .

  ?tdecl java:name ?cname ;
         ver:version ?ver .

  ?x chg:relabeled ?x_ .

  FILTER (?xname IN (?fqn, ?ename))

}
}
''' % NS_TBL

Q_CHG_ENUMCONST_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeEnumConst:", ?fqn) AS ?name)
(?econst AS ?key) (?econst_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?enum ?econst ?ename ?tyname ?ver ?ver_ ?enum_ ?econst_ ?ename_ ?tyname_
    WHERE {

      ?econst a java:EnumConstant ;
              java:name ?ename ;
              java:inEnum ?enum ;
              chg:relabeled ?econst_ .

      ?econst_ a java:EnumConstant ;
               java:name ?ename_ ;
               java:inEnum ?enum_ .

      ?enum a java:EnumDeclaration ;
            java:fullyQualifiedName ?tyname ;
            src:inFile/ver:version ?ver .

      ?enum_ a java:EnumDeclaration ;
             java:fullyQualifiedName ?tyname_ ;
             src:inFile/ver:version ?ver_ .

    } GROUP BY ?enum ?econst ?ename ?tyname ?ver ?ver_ ?enum_ ?econst_ ?ename_ ?tyname_
  }

  BIND(CONCAT(?tyname, ".", ?ename) AS ?fqn)
  BIND(CONCAT(?tyname_, ".", ?ename_) AS ?fqn_)

  ?x java:name ?xname ;
     java:inTypeDeclaration ?tdecl ;
     chg:relabeled ?x_ .

  ?x_ java:name ?xname_ ;
      java:inTypeDeclaration ?tdecl_ .

  ?tdecl java:name ?cname ;
         ver:version ?ver .

  ?tdecl_ java:name ?cname_ ;
          ver:version ?ver_ .

  FILTER (?x != ?econst && ?x_ != ?econst_)

  FILTER (?xname IN (?fqn, ?ename) || ?xname_ IN (?fqn_, ?ename_))

}
}
''' % NS_TBL

Q_RM_ENUMCONST_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveEnumConst:", ?fqn) AS ?name)
(?econst AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?ctxx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?enum ?econst ?ctx_ ?ename ?tyname ?ver
    WHERE {

      ?econst a java:EnumConstant ;
              java:name ?ename ;
              java:inEnum ?enum ;
              chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?econst chg:mappedStablyTo ?econst_ .
      }

      ?enum a java:EnumDeclaration ;
            java:fullyQualifiedName ?tyname ;
            src:inFile/ver:version ?ver .

    } GROUP BY ?enum ?econst ?ctx_ ?ename ?tyname ?ver
  }

  BIND(CONCAT(?tyname, ".", ?ename) AS ?fqn)

  ?x java:name ?xname ;
     java:inTypeDeclaration ?tdecl ;
     chg:removal ?ctxx_ .

  ?tdecl java:name ?cname ;
         ver:version ?ver .

  FILTER NOT EXISTS {
    ?x a java:EnumConstant .
  }

  FILTER (?xname IN (?fqn, ?ename))

}
}
''' % NS_TBL

Q_CHG_FIELD_REL0_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeField:", ?fqn_, ".", ?fname_) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl_ ?field ?field_ ?vdtor ?vdtor_ ?fname ?fname_ ?tyname_ ?ver_
    WHERE {

      ?field a java:FieldDeclaration ;
             chg:relabeled ?field_ .

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl0_ .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:relabeled ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveField ;
             jref:movedField ?field_ .
      }

      ?tdecl_ java:subClassOf* ?tdecl0_ ;
              java:fullyQualifiedName ?tyname_ ;
              ver:version ?ver_ .

     } GROUP BY ?tdecl_ ?field ?field_ ?vdtor ?vdtor_ ?fname ?fname_ ?tyname_ ?ver_
   }

  BIND(CONCAT(?tyname_, ".", ?fname_) AS ?fqn_)

  {
    ?x_ a java:FieldAccess ;
        java:inTypeDeclaration/ver:version ?ver_ ;
        java:name ?fname_ ;
        src:child0 ?e_ .

    ?x chg:relabeled ?x_ .

    ?e_ a java:Expression ;
        java:ofReferenceType/java:fullyQualifiedName ?tyname_ .
  }
  UNION
  {
    ?x_ a java:FieldAccess ;
        java:inTypeDeclaration ?tdecl_ ;
        java:name ?fname_ .

    ?x chg:relabeled ?x_ .

    FILTER (EXISTS {
      [] a java:This ;
         src:parent ?x_ .
    } || NOT EXISTS {
      [] src:parent ?x_ .
    })
  }
  UNION
  {
     ?x_ a java:Name ;
         java:inTypeDeclaration/ver:version ?ver_ ;
         java:name ?fqn_ .

    ?x chg:relabeled ?x_ .
  }

}
}
''' % NS_TBL

Q_CHG_FIELD_REL1_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeField:", ?fqn, ".", ?fname) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?field ?field_ ?vdtor ?vdtor_ ?fname ?fname_ ?tyname ?ver
    WHERE {

      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl0 ;
             chg:relabeled ?field_ .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:relabeled ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveField ;
             jref:originalField ?field .
      }

      ?tdecl java:subClassOf* ?tdecl0 ;
             java:fullyQualifiedName ?tyname ;
             ver:version ?ver .

     } GROUP BY ?tdecl ?field ?field_ ?vdtor ?vdtor_ ?fname ?fname_ ?tyname ?ver
   }

  BIND(CONCAT(?tyname, ".", ?fname) AS ?fqn)

  {
    ?x a java:FieldAccess ;
       java:inTypeDeclaration/ver:version ?ver ;
       java:name ?fname ;
       src:child0 ?e ;
       chg:relabeled ?x_ .

    ?e a java:Expression ;
       java:ofReferenceType/java:fullyQualifiedName ?tyname .
  }
  UNION
  {
    ?x a java:FieldAccess ;
       java:inTypeDeclaration ?tdecl ;
       java:name ?fname ;
       chg:relabeled ?x_ .

    FILTER (EXISTS {
      [] a java:This ;
         src:parent ?x .
    } || NOT EXISTS {
      [] src:parent ?x .
    })
  }
  UNION
  {
     ?x a java:Name ;
        java:inTypeDeclaration/ver:version ?ver ;
        java:name ?fqn ;
        chg:relabeled ?x_ .
  }

}
}
''' % NS_TBL


Q_ADD_VDTOR_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddVdtor:", ?mfqn_, ":", ?vname_) AS ?name)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ ;
          java:inMethodOrConstructor/java:fullyQualifiedName ?mfqn_ ;
          chg:addition ?ctx .

  ?x_ a ?cat OPTION (INFERENCE NONE) ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_RM_BLOCK_ADD_VDTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveBlock:", ?fqn_, ":", ?vname_) AS ?name)
(?block AS ?dep) (?ctxb_ AS ?dep_)
(?ctxv AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?block ?ctxb_ ?ctxx ?vdtor_ ?ctxv ?vname_ ?x_ ?fqn_
    WHERE {
      ?block a java:Block ;
             chg:removal ?ctxb_ .

      ?stable src:parent+ ?block ;
              chg:mappedTo ?stable_ .

      ?stable_ src:parent+ ?vdtor_ .


      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ ;
              java:inMethodOrConstructor ?meth_ ;
              chg:addition ?ctxv .

      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig_ .

      ?x_ a ?cat OPTION (INFERENCE NONE) ;
          chg:addition ?ctxx ;
          java:declaredBy ?vdtor_ .

    } GROUP BY ?block ?ctxb_ ?ctxx ?vdtor_ ?ctxv ?vname_ ?x_ ?fqn_
  }

  FILTER NOT EXISTS {
    ?ctxx src:parent+ ?block .
  }

}
}
''' % NS_TBL

Q_RM_VDTOR_ADD_VDTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAddVdtor:", ?cfqn, ":", ?vname) AS ?name)
(?vdtor AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
         chg:removal ?ctx_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor ;
     chg:mappedStablyTo ?x_ .

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      java:declaredBy ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ ;
          chg:addition ?ctx .

}
}
''' % NS_TBL

Q_ADD_PARAM_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddParam:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?param_ AS ?key_)
(?ctx AS ?dep) (?param_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition ?ctx .

#  FILTER NOT EXISTS {
#    ?param chg:mappedTo ?param_ .
#  }

  ?meth chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?x_ a ?cat OPTION (INFERENCE NONE) ;
      chg:addition ?ctxx ;
      java:declaredBy ?param_ .

}
}
''' % NS_TBL

Q_ADD_PARAM_ADD_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddParam:", ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?param_ AS ?key_)
(?ctxa AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?param_ ?pname_ ?meth_ ?fqn_ ?sig_
    WHERE {
      ?param_ a java:Parameter ;
              src:parent ?params_ ;
              java:name ?pname_ ;
              chg:addition ?ctx .

      ?params_ a java:Parameters ;
               src:parent ?meth_ .

      ?meth chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:signature ?sig0_ ;
             java:fullyQualifiedName ?fqn_ .

      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_)

      # FILTER NOT EXISTS {
      #   ?ref a jref:AddParameter ;
      #        jref:addedParameter ?param_ ;
      #        jref:modifiedMethod ?meth_ .
      # }

    } GROUP BY ?ctx ?param_ ?pname_ ?meth_ ?fqn_ ?sig_
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        chg:addition ?ctxa .

}
}
''' % NS_TBL

Q_ADD_PARAM_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddParam:", ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?param_ AS ?key_)
(?ctx AS ?dep) (?param_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {
      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:originalMethod ?meth ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition ?ctx .


  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctxi .

}
}
''' % NS_TBL

Q_INS_IVK_ADD_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("InsertInvocation:", ?fqn_) AS ?name)
(?ctx AS ?key) (?ivk_ AS ?key_)
(?ctxa AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ ;
        java:mayInvokeMethod [] ;
        chg:addition ?ctx .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?args chg:mappedStablyTo ?args_ .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        chg:addition ?ctxa .

}
}
''' % NS_TBL

Q_RM_PARAM_RM_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveParam:", ?sig, ":", ?pname) AS ?name)
(?param AS ?key) (?ctx_ AS ?key_)
(?arg AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?param ?ctx_ ?pname ?meth ?fqn ?sig
    WHERE {
      ?param a java:Parameter ;
             src:parent ?params ;
             java:name ?pname ;
             chg:removal ?ctx_ .

      ?params a java:Parameters ;
              src:parent ?meth .

      ?meth a java:MethodOrConstructor ;
            java:signature ?sig0 ;
            java:fullyQualifiedName ?fqn ;
            chg:mappedTo ?meth_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig)

      # FILTER NOT EXISTS {
      #   ?ref a jref:RemoveParameter ;
      #        jref:removedParameter ?param ;
      #        jref:originalMethod ?meth .
      # }

    } GROUP BY ?param ?ctx_ ?pname ?meth ?fqn ?sig
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth .

  ?args a java:Arguments ;
        src:parent ?ivk .

  ?arg a java:Expression ;
       src:parent ?args ;
       chg:removal ?ctxa_ .

}
}
''' % NS_TBL

Q_RM_PARAM_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveParam:", ?sig, ":", ?pname) AS ?name)
(?param AS ?key) (?ctx_ AS ?key_)
(?param AS ?dep) (?ctx_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {
      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:originalMethod ?meth ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  ?param a java:Parameter ;
         java:name ?pname ;
         java:inMethodOrConstructor ?meth ;
         chg:removal ?ctx_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctxi .

}
}
''' % NS_TBL

Q_RM_LVD_ADD_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveLVD:", ?fqn, ":", ?vname) AS ?name)
(?vdecl AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdecl a java:LocalVariableDeclarationStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child1 ?ty ;
         src:child2 ?vdtor ;
         chg:removal ?ctx_ .

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .


  ?param_ a java:Parameter ;
          java:name ?vname ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition ?ctx .

}
}
''' % NS_TBL

Q_ADD_LVD_CHG_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddLVD:", ?fqn_, ":", ?vname_) AS ?name)
(?ctx AS ?key) (?vdecl_ AS ?key_)
(?param AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdecl_ a java:LocalVariableDeclarationStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child1 ?ty_ ;
          src:child2 ?vdtor_ ;
          chg:addition ?ctx .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .


  ?param a java:Parameter ;
         java:name ?vname_ ;
         java:inMethodOrConstructor ?meth ;
         chg:relabeled ?param_ .

}
}
''' % NS_TBL

Q_ADD_USE_ADD_INI_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddUse:", ?fqn_, ":", ?vname_) AS ?name)
(?ctx AS ?dep) (?ini_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdecl_ ?vdtor_ ?vname_ ?fqn_ ?ctx ?ini_
    WHERE {

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              java:inMethodOrConstructor ?meth_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

      ?vdecl chg:mappedTo ?vdecl_ .
      ?vdtor_ java:initializer ?ini_ .
      ?ini_ chg:addition ?ctx .

      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig_ .

    } GROUP BY ?vdecl_ ?vdtor_ ?vname_ ?fqn_ ?ctx ?ini_
  }

  ?x_ java:declaredBy ?vdtor_ ;
      java:inStatement ?stmt_ ;
      chg:addition ?ctxx .

  FILTER NOT EXISTS {
    ?stmt_ a java:AssignmentStatement ;
           src:child0 ?x_ .
  }

}
}
''' % NS_TBL

Q_ADD_USE_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddUse:", ?fqn_, ":", ?vname_) AS ?name)
(?ctxa AS ?dep) (?assign_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdecl_ ?ctx ?vdtor_ ?vname_ ?fqn ?fqn_ ?x_ ?ctxx ?stmt_ ?min ?assign_ ?ctxa
    WHERE {

      {
        SELECT DISTINCT ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_ ?ctxx ?x_ ?stmt_
        (MIN(?step0) AS ?min)
        WHERE {

          {
            SELECT DISTINCT ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_ ?ctxx ?x_ ?stmt_ ?assign0_
            WHERE {

              {
                SELECT DISTINCT ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_ ?ctxx ?x_ ?stmt_
                WHERE {

                  {
                    SELECT DISTINCT ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_
                    WHERE {

                      ?vdecl_ a java:LocalVariableDeclarationStatement ;
                              java:inMethodOrConstructor ?meth_ ;
                              src:child1 ?ty_ ;
                              src:child2 ?vdtor_ ;
                              chg:addition ?ctx .

                      ?vdtor_ a java:VariableDeclarator ;
                              java:name ?vname_ .

                      FILTER NOT EXISTS {
                        ?vdtor_ java:initializer [] .
                      }

                      ?meth java:fullyQualifiedName ?fqn ;
                            java:signature ?sig ;
                            chg:mappedTo ?meth_ .

                      ?meth_ java:fullyQualifiedName ?fqn_ ;
                             java:signature ?sig_ .

                    } GROUP BY ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_
                  }

                  ?x_ java:declaredBy ?vdtor_ ;
                      java:inStatement ?stmt_ ;
                      chg:addition ?ctxx .

                  FILTER NOT EXISTS {
                    ?stmt_ a java:AssignmentStatement ;
                           src:child0 ?x_ .
                  }

                } GROUP BY ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_ ?ctxx ?x_ ?stmt_
              }

              ?vdecl_ java:successor ?assign0_ OPTION (TRANSITIVE,
                                                       T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

              ?assign0_ a java:AssignStatement ;
                        src:child0 ?y0_ ;
                        chg:addition [] .

              ?y0_ java:declaredBy ?vdtor_ .

              ?assign0_ java:successor ?stmt_ OPTION (TRANSITIVE,
                                                      T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

            } GROUP BY ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_ ?ctxx ?x_ ?stmt_ ?assign0_
          }

#          FILTER EXISTS {
            ?vdecl_ java:successor ?assign0_ OPTION (TRANSITIVE,
                                                     T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
            #?assign0_ java:successor ?stmt_ OPTION (TRANSITIVE,
                                                     T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
            ?stmt_ ^java:successor ?assign0_ OPTION (TRANSITIVE,
                                                     T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
#          }

          FILTER NOT EXISTS {
            {
              SELECT ?assign0_ ?a0_ ?b0_
              WHERE {
                ?a0_ java:successor ?b0_ .
                FILTER (?b0_ != ?assign0_)
              }
            } OPTION (TRANSITIVE, T_IN(?a0_), T_OUT(?b0_), T_MIN(1), T_NO_CYCLES,
                      T_STEP('path_id') AS ?pid0)
            FILTER (?a0_ = ?vdecl_ && ?b0_ = ?stmt_)
          }

          {
            SELECT ?a1_ ?b1_
            WHERE {
              ?a1_ java:successor ?b1_ .
            }
          } OPTION (TRANSITIVE,
                    T_IN(?a1_), T_OUT(?b1_), T_DISTINCT, T_MIN(1), T_NO_CYCLES, T_SHORTEST_ONLY,
                    T_STEP('step_no') AS ?step0) .
          FILTER (?a1_ = ?assign0_ && ?b1_ = ?stmt_)

        } GROUP BY ?ctx ?vdecl_ ?vdtor_ ?vname_ ?fqn ?fqn_ ?ctxx ?x_ ?stmt_
      }

      ?vdecl_ java:successor ?assign_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

      ?assign_ a java:AssignStatement ;
               src:child0 ?y_ ;
               chg:addition ?ctxa .

      ?y_ java:declaredBy ?vdtor_ .

#      ?assign_ java:successor ?stmt_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

    } GROUP BY ?vdecl_ ?ctx ?vdtor_ ?vname_ ?fqn ?fqn_ ?x_ ?ctxx ?stmt_ ?min ?assign_ ?ctxa
  }

  {
    SELECT ?a3_ ?b3_
    WHERE {
      ?a3_ java:successor ?b3_ .
    }
  } OPTION (TRANSITIVE, T_IN(?a3_), T_OUT(?b3_), T_DISTINCT, T_MIN(1), T_NO_CYCLES, T_SHORTEST_ONLY,
            T_STEP('step_no') AS ?step) .
  FILTER (?a3_ = ?assign_ && ?b3_ = ?stmt_)

  FILTER (?step = ?min)

}
}
''' % NS_TBL

Q_RM_USE_RM_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveUse:", ?fqn, ":", ?vname) AS ?name)
(?assign AS ?ent) (?ctxa_ AS ?ent_)
(?x AS ?dep) (?ctxx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt ?min ?assign ?ctxa_
    WHERE {

      {
        SELECT DISTINCT ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt
        (MIN(?step0) AS ?min)
        WHERE {

          {
            SELECT DISTINCT ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt ?assign0
            WHERE {

              {
                SELECT DISTINCT ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt
                WHERE {

                  {
                    SELECT DISTINCT ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_
                    WHERE {

                      ?vdecl a java:LocalVariableDeclarationStatement ;
                             java:inMethodOrConstructor ?meth ;
                             src:child1 ?ty ;
                             src:child2 ?vdtor ;
                             chg:removal ?ctx_ .

                      ?vdtor a java:VariableDeclarator ;
                             java:name ?vname .

                      FILTER NOT EXISTS {
                        ?vdtor java:initializer [] .
                      }

                      ?meth java:fullyQualifiedName ?fqn ;
                            java:signature ?sig ;
                            chg:mappedTo ?meth_ .

                      ?meth_ java:fullyQualifiedName ?fqn_ ;
                             java:signature ?sig_ .

                    } GROUP BY ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_
                  }

                  ?x java:declaredBy ?vdtor ;
                     java:inStatement ?stmt ;
                     chg:removal ?ctxx_ .

                  FILTER NOT EXISTS {
                    ?stmt a java:AssignmentStatement ;
                          src:child0 ?x .
                  }

                } GROUP BY ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt
              }

              ?vdecl java:successor ?assign0 OPTION (TRANSITIVE,
                                                     T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

              ?assign0 a java:AssignStatement ;
                       src:child0 ?y0 ;
                       chg:removal [] .

              ?y0 java:declaredBy ?vdtor .

              ?assign0 java:successor ?stmt OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

            } GROUP BY ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt ?assign0
          }

#          FILTER EXISTS {
            ?vdecl java:successor ?assign0 OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
            ?assign0 java:successor ?stmt OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
            #?stmt ^java:successor ?assign0 OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
#          }

          FILTER NOT EXISTS {
            {
              SELECT ?assign0 ?a0 ?b0
              WHERE {
                ?a0 java:successor ?b0 .
                FILTER (?b0 != ?assign0)
              }
            } OPTION (TRANSITIVE, T_IN(?a0), T_OUT(?b0), T_MIN(1), T_NO_CYCLES,
                      T_STEP('path_id') AS ?pid0)
            FILTER (?a0 = ?vdecl && ?b0 = ?stmt)
          }

          {
            SELECT ?a1 ?b1
            WHERE {
              ?a1 java:successor ?b1 .
            }
          } OPTION (TRANSITIVE,
                    T_IN(?a1), T_OUT(?b1), T_DISTINCT, T_MIN(1), T_NO_CYCLES, T_SHORTEST_ONLY,
                    T_STEP('step_no') AS ?step0) .
          FILTER (?a1 = ?assign0 && ?b1 = ?stmt)

        } GROUP BY ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt
      }

      ?vdecl java:successor ?assign OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

      ?assign a java:AssignStatement ;
              src:child0 ?y ;
              chg:removal ?ctxa_ .

      ?y java:declaredBy ?vdtor .

#      ?assign java:successor ?stmt OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

    } GROUP BY ?vdecl ?ctx_ ?vdtor ?vname ?fqn ?fqn_ ?x ?ctxx_ ?stmt ?min ?assign ?ctxa_
  }

  {
    SELECT ?a3 ?b3
    WHERE {
      ?a3 java:successor ?b3 .
    }
  } OPTION (TRANSITIVE, T_IN(?a3), T_OUT(?b3), T_DISTINCT, T_MIN(1), T_NO_CYCLES, T_SHORTEST_ONLY,
            T_STEP('step_no') AS ?step) .
  FILTER (?a3 = ?assign && ?b3 = ?stmt)

  FILTER (?step = ?min)

}
}
''' % NS_TBL

Q_ADD_LVD_RM_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddLVD:", ?fqn_, ":", ?vname_) AS ?name)
(?ctx AS ?key) (?vdecl_ AS ?key_)
(?param AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdecl_ a java:LocalVariableDeclarationStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child1 ?ty_ ;
          src:child2 ?vdtor_ ;
          chg:addition ?ctx .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .


  ?param a java:Parameter ;
         java:name ?vname_ ;
         java:inMethodOrConstructor ?meth ;
         chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_PARAM_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddParam:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?param_ AS ?key_)
(?ctx AS ?dep) (?param_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition ?ctx .

#  FILTER NOT EXISTS {
#    ?param chg:mappedTo ?param_ .
#  }

  ?meth chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?x chg:relabeled ?x_ .

  ?x_ a ?cat OPTION (INFERENCE NONE) ;
      java:declaredBy ?param_ .

}
}
''' % NS_TBL

Q_ADD_PARAM_ADD_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddParam:", ?sig0_, ":", ?pname0_) AS ?name)
(?ctx0 AS ?key) (?param0_ AS ?key_)
(?ctx1 AS ?ent) (?param1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl0_ ?sig0_ ?ctx0 ?param0_ ?p_child
    WHERE {
      ?ref0 a jref:AddParameter ;
            jref:addedParameter ?param0_ ;
            jref:originalMethod ?meth0 ;
            jref:modifiedMethod ?meth0_ .

      ?param0_ chg:addition ?ctx0 .

      ?meth0 a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl0 ;
             chg:mappedTo ?meth0_ .

      ?meth0_ a java:MethodDeclaration ;
              java:inTypeDeclaration ?tdecl0_ ;
              java:fullyQualifiedName ?fqn0_ ;
              java:signature ?sig_ ;
              src:child3 ?params0_ .

      BIND (CONCAT(?fqn0_, ?sig_) AS ?sig0_) .

      ?params0_ ?p_child ?param0_ .

    } GROUP BY ?tdecl0_ ?sig0_ ?ctx0 ?param0_ ?p_child
  }

  ?param0_ java:name ?pname0_ .

  ?tdecl1_ java:subTypeOf ?tdecl0_ .

  ?meth1 a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl1 ;
        chg:mappedTo ?meth1_ .

  ?meth1_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl1_ ;
          java:fullyQualifiedName ?fqn1_ ;
          java:signature ?sig_ ;
          src:child3 ?params1_ .

  ?ref1 a jref:AddParameter ;
        jref:addedParameter ?param1_ ;
        jref:originalMethod ?meth1 ;
        jref:modifiedMethod ?meth1_ .

  ?param1_ chg:addition ?ctx1 .

  BIND (CONCAT(?fqn1_, ?sig_) AS ?sig1_) .

  ?params1_ ?p_child ?param1_ .

}
}
''' % NS_TBL

Q_RM_PARAM_RM_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveParam:", ?sig0, ":", ?pname0) AS ?name)
(?param0 AS ?key) (?ctx0_ AS ?key_)
(?param1 AS ?ent) (?ctx1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl0 ?sig0 ?ctx0_ ?param0 ?p_child
    WHERE {
      ?ref0 a jref:RemoveParameter ;
            jref:removedParameter ?param0 ;
            jref:originalMethod ?meth0 ;
            jref:modifiedMethod ?meth0_ .

      ?param0 chg:removal ?ctx0_ .

      ?meth0 a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl0 ;
             java:fullyQualifiedName ?fqn0 ;
             java:signature ?sig ;
             src:child3 ?params0 ;
             chg:mappedTo ?meth0_ .

      ?meth0_ a java:MethodDeclaration ;
              java:inTypeDeclaration ?tdecl0_ .

      BIND (CONCAT(?fqn0, ?sig) AS ?sig0) .

      ?params0 ?p_child ?param0 .

    } GROUP BY ?tdecl0 ?sig0 ?ctx0_ ?param0 ?p_child
  }

  ?param0 java:name ?pname0 .

  ?tdecl1 java:subTypeOf ?tdecl0 .

  ?meth1 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl1 ;
         java:fullyQualifiedName ?fqn1 ;
         java:signature ?sig ;
         src:child3 ?params1 ;
         chg:mappedTo ?meth1_ .

  ?meth1_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl1_ .

  ?ref1 a jref:RemoveParameter ;
        jref:removedParameter ?param1 ;
        jref:originalMethod ?meth1 ;
        jref:modifiedMethod ?meth1_ .

  ?param1 chg:removal ?ctx1_ .

  BIND (CONCAT(?fqn1, ?sig) AS ?sig1) .

  ?params1 ?p_child ?param1 .

}
}
''' % NS_TBL

Q_CHG_PARAM_CHG_USE_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParam:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?param AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:Parameter ;
         java:name ?pname ;
         java:inMethodOrConstructor ?meth ;
         chg:relabeled ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          java:inMethodOrConstructor ?meth_ .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?x chg:relabeled ?x_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?param .

}
}
''' % NS_TBL

Q_CHG_PARAM_CHG_USE_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParam:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?param AS ?dep) (?param_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:Parameter ;
         java:name ?pname ;
         java:inMethodOrConstructor ?meth ;
         chg:relabeled ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          java:inMethodOrConstructor ?meth_ .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?x chg:relabeled ?x_ .

  ?x_ a ?cat OPTION (INFERENCE NONE) ;
      java:declaredBy ?param_ .

}
}
''' % NS_TBL

Q_INS_METH_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("InsertMethod:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?meth_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition [] .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ ;
         chg:insertedInto ?ctx .

  ?x chg:relabeled ?x_ .

  ?x_ a ?cat OPTION (INFERENCE NONE) ;
      java:declaredBy ?param_ .

}
}
''' % NS_TBL

Q_INS_METH_ADD_VDTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("InsertMethod:", ?fqn_, ?sig_, ":", ?vname_) AS ?name)
(?ctx AS ?key) (?meth_ AS ?key_)
(?ctxv AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         java:inMethodOrConstructor ?meth .

  ?meth java:fullyQualifiedName ?fqn ;
        src:parent+/src:inFile/src:location ?loc ;
        java:signature ?sig .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor .

  ?x chg:mappedStablyTo ?x_ .

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      java:declaredBy ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition ?ctxv .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ ;
         chg:insertedInto ?ctx .

}
}
''' % NS_TBL

Q_ADD_VDTOR_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddVdtor:", ?cfqn_, ":", ?vname) AS ?name)
(?ctx AS ?key) (?vdtor_ AS ?key_)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname ;
          java:inTypeDeclaration/java:fullyQualifiedName ?cfqn_ ;
          chg:addition ?ctx .

  ?x_ a ?cat OPTION (INFERENCE NONE) ;
      java:declaredBy ?vdtor_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_RM_VDTOR_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveVdtor:", ?cfqn, ":", ?vname) AS ?name)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
         chg:removal ?ctx_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor ;
     chg:relabeled ?x_ .
}
}
''' % NS_TBL

Q_RM_VDTOR_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveVdtor:", ?mfqn, ":", ?vname) AS ?name)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?ctxx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         java:inMethodOrConstructor/java:fullyQualifiedName ?mfqn ;
         chg:removal ?ctx_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_ADD_BLOCK_RM_VDTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddBlock:", ?fqn, ":", ?vname) AS ?name)
(?ctxb AS ?ent) (?block_ AS ?ent_)
(?vdtor AS ?dep) (?ctxv_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?block_ ?ctxb ?ctxx_ ?vdtor ?ctxv_ ?vname ?x ?fqn
    WHERE {
      ?block_ a java:Block ;
              chg:addition ?ctxb .

      ?stable_ src:parent+ ?block_ ;
               ^chg:mappedTo ?stable .

      ?stable src:parent+ ?vdtor .


      ?vdtor a java:VariableDeclarator ;
              java:name ?vname ;
              java:inMethodOrConstructor ?meth ;
              chg:removal ?ctxv_ .

      ?meth java:fullyQualifiedName ?fqn ;
            java:signature ?sig .

      ?x a ?cat OPTION (INFERENCE NONE) ;
          chg:removal ?ctxx_ ;
          java:declaredBy ?vdtor .

    } GROUP BY ?block_ ?ctxb ?ctxx_ ?vdtor ?ctxv_ ?vname ?x ?fqn
  }

  FILTER NOT EXISTS {
    ?ctxx_ src:parent+ ?block_ .
  }

}
}
''' % NS_TBL

Q_RM_PARAM_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveParam:", ?fqn, ?sig, ":", ?pname) AS ?name)
#(?param AS ?key) (?ctx_ AS ?key_)
#(?x AS ?ent) (?ctxx_ AS ?ent_)
(?param AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?ctxx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:Parameter ;
         java:name ?pname ;
         java:inMethodOrConstructor ?meth ;
         chg:removal ?ctx_ .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     chg:removal ?ctxx_ ;
     java:declaredBy ?param .

}
}
''' % NS_TBL

Q_MOVDEL_METH_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("MoveDeleteMethod:", ?fqn, ?sig, ":", ?pname) AS ?name)
(?meth AS ?key) (?ctx_ AS ?key_)
(?x AS ?ent) (?ctxx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:Parameter ;
         java:name ?pname ;
         java:inMethodOrConstructor ?meth .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:genRemoved ?ctx_ ;
        chg:movedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?param_ a java:Parameter ;
          java:inMethodOrConstructor ?meth_ .

  FILTER NOT EXISTS {
    ?param chg:removal [] .
  }

  FILTER NOT EXISTS {
    ?param_ java:name ?pname .
  }

  ?x a ?cat OPTION (INFERENCE NONE) ;
     chg:removal ?ctxx_ ;
     java:declaredBy ?param .

}
}
''' % NS_TBL

Q_RM_STMT_INS_BODY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("InsertBody:", ?fqn) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?cat ?px ?ctx_ ?x_ ?ctx ?sx0 ?sx0_ ?fqn
    WHERE {

      ?x a ?cat OPTION (INFERENCE NONE) ;
         a java:Statement ;
         src:parent ?px ;
         chg:removal ?ctx_ .

      ?px a java:MethodBody ;
          src:parent ?meth .

      ?meth java:fullyQualifiedName ?fqn .

      ?x_ a java:MethodBody ;
          chg:addition ?ctx .

      ?sx0 src:parent+ ?x ;
           chg:mappedStablyTo ?sx0_ .

      ?sx0_ src:parent+ ?x_ .

    } GROUP BY ?x ?cat ?px ?ctx_ ?x_ ?ctx ?sx0 ?sx0_ ?fqn
  }

  ?sx src:parent+ ?x ;
      chg:mappedStablyTo ?sx_ .

  FILTER (?sx != ?sx0 && ?sx_ != ?sx0_)

  FILTER NOT EXISTS {
    ?x_ a [] .
    ?sx_ src:parent+ ?x_ .
  }

}
}
''' % NS_TBL

Q_RM_PARAM_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveParam:", ?fqn, ?sig, ":", ?pname) AS ?name)
#(?param AS ?key) (?ctx_ AS ?key_)
#(?x AS ?ent) (?x_ AS ?ent_)
(?param AS ?ent) (?ctx_ AS ?ent_)
(?x AS ?dep) (?x_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:Parameter ;
         java:name ?pname ;
         java:inMethodOrConstructor ?meth ;
         chg:removal ?ctx_ .

#  FILTER NOT EXISTS {
#    ?param chg:mappedTo ?param_ .
#  }

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?param ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_RM_ADD_VDTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAddVdtor:", ?fqn, ?sig, ":", ?vname) AS ?name)
(?vdtor AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         java:inMethodOrConstructor ?meth ;
         chg:removal ?ctx_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     chg:mappedStablyTo ?x_ ;
     java:declaredBy ?vdtor .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition ?ctx .

  ?x_ java:declaredBy ?vdtor_ .

  ?meth chg:mappedTo ?meth_ .
}
}
''' % NS_TBL

Q_CHG_PARAM_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParam:", ?fqn, ?sig, ":", ?pname) AS ?name)
(?param AS ?key) (?param_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?params a java:Parameters ;
          src:parent ?meth ;
          chg:mappedTo ?params_ .

  ?params_ a java:Parameters ;
           src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:parent ?params ;
         chg:relabeled ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:parent ?params_ .

  ?x chg:relabeled ?x_ ;
     java:declaredBy ?param .

  ?x_ java:declaredBy ?param_ .

}
}
''' % NS_TBL

Q_INS_PARAM_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("FakeAddParam:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?param_ AS ?key_)
(?ctx AS ?dep) (?param_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?fqn_ ?sig_ ?ctx ?param_ ?pname_
    WHERE {
      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig_ .

      ?params_ a java:Parameters ;
               src:parent ?meth_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ ;
              chg:addition ?ctx .

      # FILTER NOT EXISTS {
      #   ?ref a jref:AddParameter ;
      #        jref:modifiedMethod ?meth_ ;
      #        jref:addedParameter ?param_ .
      # }

    } GROUP BY ?meth_ ?fqn_ ?sig_ ?ctx ?param_ ?pname_
  }

  ?x chg:relabeled ?x_ .

  ?x_ java:declaredBy ?param_ .

}
}
''' % NS_TBL

Q_INS_PARAM_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("FakeAddParam:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?param_ AS ?key_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?fqn_ ?sig_ ?ctx ?param_ ?pname_
    WHERE {
      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig_ .

      ?params_ a java:Parameters ;
               src:parent ?meth_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ ;
              chg:addition ?ctx .

      # FILTER NOT EXISTS {
      #   ?ref a jref:AddParameter ;
      #        jref:modifiedMethod ?meth_ ;
      #        jref:addedParameter ?param_ .
      # }

    } GROUP BY ?meth_ ?fqn_ ?sig_ ?ctx ?param_ ?pname_
  }

  ?x_ java:declaredBy ?param_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_CHG_PARAM_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParam:", ?fqn_, ?sig_, ":", ?pname_) AS ?name)
(?param AS ?key) (?param_ AS ?key_)
(?param AS ?dep) (?param_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  # ?meth java:fullyQualifiedName ?fqn ;
  #       java:signature ?sig ;
  #       chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  # ?params a java:Parameters ;
  #         src:parent ?meth ;
  #         chg:mappedTo ?params_ .

  ?params_ a java:Parameters ;
           src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:parent ?params ;
         chg:relabeled ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:parent ?params_ .

  ?x_ java:declaredBy ?param_ ;
      chg:addition ?ctx

}
}
''' % NS_TBL

Q_CHG_PARAM_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParam:", ?fqn, ?sig, ":", ?pname_) AS ?name)
#(?param AS ?key) (?param_ AS ?key_)
#(?x AS ?ent) (?ctx_ AS ?ent_)
(?param AS ?ent) (?param_ AS ?ent_)
(?x AS ?dep) (?ctx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig .
  #       chg:mappedTo ?meth_ .

  # ?meth_ java:fullyQualifiedName ?fqn_ ;
  #        java:signature ?sig_ .

  ?params a java:Parameters ;
          src:parent ?meth .
  #         chg:mappedTo ?params_ .

  # ?params_ a java:Parameters ;
  #          src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:parent ?params ;
         chg:relabeled ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:parent ?params_ .

  ?x java:declaredBy ?param ;
     chg:removal ?ctx_

}
}
''' % NS_TBL

Q_CHG_PARAM_INS_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamArg:", ?sig_, ":", ?pname_) AS ?name)
(?param AS ?key) (?param_ AS ?key_)
(?ctxa AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  ?params a java:Parameters ;
          src:parent ?meth ;
          chg:mappedTo ?params_ .

  ?params_ a java:Parameters ;
           ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
           src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:parent ?params ;
         chg:relabeled ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:parent ?params_ .

  FILTER NOT EXISTS {
    ?ty src:parent ?param ;
        chg:mappedStablyTo ?ty_ ;
        chg:mappedEqTo ?ty_ .

    ?ty_ src:parent ?param_ .
  }
#
  {
    SELECT DISTINCT ?ivk_ ?args_ ?p_child_ ?arg_ ?ctxa ?meth_
    WHERE {

      ?ivk_ java:mayInvokeMethod ?meth_ .

      ?args_ a java:Arguments ;
             ?p_child_ ?arg_ OPTION (INFERENCE NONE) ;
             src:parent ?ivk_ .

      ?arg_ chg:addition ?ctxa .

    } GROUP BY ?ivk_ ?args_ ?p_child_ ?arg_ ?ctxa ?meth_
  }

}
}
''' % NS_TBL

Q_CHG_PARAM_CHG_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamArg:", ?sig_, ":", ?pname_) AS ?name)
(?param AS ?key) (?param_ AS ?key_)
(?arg AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child ?p_child_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0_ .

          FILTER NOT EXISTS {
            ?ref a jref:MoveMethod ;
                 jref:movedMethod ?meth_ .
          }

          BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
          BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

        } GROUP BY ?meth ?meth_ ?sig ?sig_
      }

      ?params a java:Parameters ;
              ?p_child ?param OPTION (INFERENCE NONE) ;
              src:parent ?meth ;
              chg:mappedTo ?params_ .

      ?params_ a java:Parameters ;
               ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
               src:parent ?meth_ .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params ;
             chg:relabeled ?param_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child ?p_child_
  }

  FILTER NOT EXISTS {
    ?ty src:parent ?param ;
        chg:mappedStablyTo ?ty_ ;
        chg:mappedEqTo ?ty_ .

    ?ty_ src:parent ?param_ .
  }

  {
    ?ivk java:mayInvokeMethod ?meth .

    ?args a java:Arguments ;
          ?p_child ?arg OPTION (INFERENCE NONE) ;
          src:parent ?ivk .

    ?arg chg:relabeled ?arg_ .
  }
  UNION
  {
    ?ivk_ java:mayInvokeMethod ?meth_ .

    ?args_ a java:Arguments ;
           ?p_child_ ?arg_ OPTION (INFERENCE NONE) ;
           src:parent ?ivk_ .

    ?arg_ ^chg:relabeled ?arg .
  }

}
}
''' % NS_TBL

Q_CHG_PARAM_TY_DEL_ARG_CAST_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamType:", ?sig, ":", ?pname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?arg AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0_ .

          FILTER NOT EXISTS {
            ?ref a jref:MoveMethod ;
                 jref:movedMethod ?meth_ .
          }

          BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
          BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

        } GROUP BY ?meth ?meth_ ?sig ?sig_
      }

      ?params a java:Parameters ;
              ?p_child ?param OPTION (INFERENCE NONE) ;
              src:parent ?meth ;
              chg:mappedTo ?params_ .

      ?params_ a java:Parameters ;
               #?p_child_ ?param_ OPTION (INFERENCE NONE) ;
               src:parent ?meth_ .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params ;
             chg:mappedTo ?param_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child
  }

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?ty_ a java:Type .

  {
    ?ty src:parent ?param OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
    ?ty_ src:parent ?param_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
  }
  UNION
  {
    ?ty src:parent ?param .
    ?ty_ src:parent ?param_ .
  }

#

  ?ivk java:mayInvokeMethod ?meth .

  ?args a java:Arguments ;
        ?p_child0 ?arg OPTION (INFERENCE NONE) ;
        src:parent ?ivk .

  GRAPH <http://codinuum.com/ont/cpi> {
    ?p_child0 rdfs:subPropertyOf src:child .
  }

  ?arg a java:Cast ;
       src:parent ?args ;
       chg:deletedFrom ?ctx_ .

  FILTER (?p_child = ?p_child0)

}
}
''' % NS_TBL

Q_CHG_PARAM_TY_INS_ARG_CAST_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamType:", ?sig, ":", ?pname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ctx AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0_ .

          FILTER NOT EXISTS {
            ?ref a jref:MoveMethod ;
                 jref:movedMethod ?meth_ .
          }

          BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
          BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

        } GROUP BY ?meth ?meth_ ?sig ?sig_
      }

      ?params a java:Parameters ;
              #?p_child ?param OPTION (INFERENCE NONE) ;
              src:parent ?meth ;
              chg:mappedTo ?params_ .

      ?params_ a java:Parameters ;
               ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
               src:parent ?meth_ .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params ;
             chg:mappedTo ?param_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
  }

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?ty_ a java:Type .

  {
    ?ty src:parent ?param OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
    ?ty_ src:parent ?param_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
  }
  UNION
  {
    ?ty src:parent ?param .
    ?ty_ src:parent ?param_ .
  }

#

  ?ivk_ java:mayInvokeMethod ?meth_ .

  ?args_ a java:Arguments ;
         ?p_child0_ ?arg_ OPTION (INFERENCE NONE) ;
         src:parent ?ivk_ .

  GRAPH <http://codinuum.com/ont/cpi> {
    ?p_child0_ rdfs:subPropertyOf src:child .
  }

  ?arg_ a java:Cast ;
        src:parent ?args_ ;
       chg:insertedInto ?ctx .

  FILTER (?p_child_ = ?p_child0_)

}
}
''' % NS_TBL

Q_CHG_PARAM_TY_CHG_ARG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamType:", ?sig_, ":", ?pname_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?aty AS ?ent) (?aty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0_ .

          FILTER NOT EXISTS {
            ?ref a jref:MoveMethod ;
                 jref:movedMethod ?meth_ .
          }

          BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
          BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

        } GROUP BY ?meth ?meth_ ?sig ?sig_
      }

      ?params a java:Parameters ;
              src:parent ?meth ;
              chg:mappedTo ?params_ .

      ?params_ a java:Parameters ;
               ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
               src:parent ?meth_ .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params ;
             chg:mappedTo ?param_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
  }

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?ty_ a java:Type .

  {
    ?ty src:parent ?param OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
    ?ty_ src:parent ?param_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
  }
  UNION
  {
    ?ty src:parent ?param .
    ?ty_ src:parent ?param_ .
  }

#
  OPTIONAL {
    SELECT DISTINCT ?ivk_ ?args_ ?p_child0_ ?arg ?arg_ ?ty0 ?ty0_ ?meth_ ?aty ?aty_
    WHERE {

      ?ivk_ java:mayInvokeMethod ?meth_ .

      ?args_ a java:Arguments ;
             ?p_child0_ ?arg_ OPTION (INFERENCE NONE) ;
             src:parent ?ivk_ .

      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0_ rdfs:subPropertyOf src:child .
      }

      ?arg src:parent ?args ;
           chg:mappedTo ?arg_ .

      ?arg_ src:parent ?args_ .

      {
        ?arg java:declaredBy ?vdtor .
        ?arg_ java:declaredBy ?vdtor_ .

        ?vdtor src:parent ?vdecl .

        ?vdecl #a java:LocalVariableDeclarationStatement ;
               src:child1 ?ty0 .

        ?vdtor_ src:parent ?vdecl_ .

        ?vdecl_ #a java:LocalVariableDeclarationStatement ;
                src:child1 ?ty0_ .
      }
      UNION
      {
        ?arg java:declaredBy ?param0 .
        ?arg_ java:declaredBy ?param0_ .

        ?param0 a java:Parameter ;
                src:child1 ?ty0 .

        ?param0_ a java:Parameter ;
                 src:child1 ?ty0_ .
      }

      ?ty0 chg:mappedTo ?ty0_ .

      ?aty src:parent ?ty0 OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(0)) .
      ?aty_ src:parent ?ty0_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(0)) .

      ?aty chg:relabeled ?aty_ .

    } GROUP BY ?ivk_ ?args_ ?p_child0_ ?arg ?arg_ ?ty0 ?ty0_ ?meth_ ?aty ?aty_
  }

  FILTER (?p_child_ = ?p_child0_)

}
}
''' % NS_TBL

Q_CHG_PARAM_TY_ADD_ARG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamType:", ?sig_, ":", ?pname_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ctx0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0_ .

          FILTER NOT EXISTS {
            ?ref a jref:MoveMethod ;
                 jref:movedMethod ?meth_ .
          }

          BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
          BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

        } GROUP BY ?meth ?meth_ ?sig ?sig_
      }

      ?params a java:Parameters ;
              src:parent ?meth ;
              chg:mappedTo ?params_ .

      ?params_ a java:Parameters ;
               ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
               src:parent ?meth_ .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params ;
             chg:mappedTo ?param_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
  }

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?ty_ a java:Type .

  {
    ?ty src:parent ?param OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
    ?ty_ src:parent ?param_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
  }
  UNION
  {
    ?ty src:parent ?param .
    ?ty_ src:parent ?param_ .
  }

#
  OPTIONAL {
    SELECT DISTINCT ?ivk_ ?args_ ?p_child0_ ?arg ?arg_ ?ctx0 ?ty0_ ?meth_
    WHERE {

      ?ivk_ java:mayInvokeMethod ?meth_ .

      ?args_ a java:Arguments ;
             ?p_child0_ ?arg_ OPTION (INFERENCE NONE) ;
             src:parent ?ivk_ .

      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0_ rdfs:subPropertyOf src:child .
      }

      ?arg src:parent ?args ;
           chg:mappedTo ?arg_ .

      ?arg_ src:parent ?args_ .

      {
        ?arg_ java:declaredBy ?vdtor_ .

        ?vdtor_ src:parent ?vdecl_ .

        ?vdecl_ #a java:LocalVariableDeclarationStatement ;
                src:child1 ?ty0_ .
      }
      UNION
      {
        ?arg_ java:declaredBy ?param0_ .

        ?param0_ a java:Parameter ;
                 src:child1 ?ty0_ .
      }

      ?ty0_ chg:addition ?ctx0 .

    } GROUP BY ?ivk_ ?args_ ?p_child0_ ?arg ?arg_ ?ctx0 ?ty0_ ?meth_
  }

  FILTER (?p_child_ = ?p_child0_)

}
}
''' % NS_TBL

Q_CHG_PARAM_TY_RM_ARG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamType:", ?sig_, ":", ?pname_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?fqn ;
                java:signature ?sig0 ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?fqn_ ;
                 java:signature ?sig0_ .

          FILTER NOT EXISTS {
            ?ref a jref:MoveMethod ;
                 jref:movedMethod ?meth_ .
          }

          BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
          BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

        } GROUP BY ?meth ?meth_ ?sig ?sig_
      }

      ?params a java:Parameters ;
              src:parent ?meth ;
              chg:mappedTo ?params_ .

      ?params_ a java:Parameters ;
               ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
               src:parent ?meth_ .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params ;
             chg:mappedTo ?param_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?param ?param_ ?pname ?pname_ ?p_child_
  }

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?ty_ a java:Type .

  {
    ?ty src:parent ?param OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
    ?ty_ src:parent ?param_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
  }
  UNION
  {
    ?ty src:parent ?param .
    ?ty_ src:parent ?param_ .
  }

#
  OPTIONAL {
    SELECT DISTINCT ?ivk_ ?args_ ?p_child0_ ?arg ?arg_ ?ty0 ?ctx0_ ?meth_
    WHERE {

      ?ivk_ java:mayInvokeMethod ?meth_ .

      ?args_ a java:Arguments ;
             ?p_child0_ ?arg_ OPTION (INFERENCE NONE) ;
             src:parent ?ivk_ .

      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0_ rdfs:subPropertyOf src:child .
      }

      ?arg src:parent ?args ;
           chg:mappedTo ?arg_ .

      ?arg_ src:parent ?args_ .

      {
        ?arg java:declaredBy ?vdtor .

        ?vdtor src:parent ?vdecl .

        ?vdecl #a java:LocalVariableDeclarationStatement ;
               src:child1 ?ty0 .
      }
      UNION
      {
        ?arg java:declaredBy ?param0 .

        ?param0 a java:Parameter ;
                src:child1 ?ty0 .
      }

      ?ty0 chg:removal ?ctx0_ .

    } GROUP BY ?ivk_ ?args_ ?p_child0_ ?arg ?arg_ ?ty0 ?ctx0_ ?meth_
  }

  FILTER (?p_child_ = ?p_child0_)

}
}
''' % NS_TBL

Q_DEL_PARAM_TY_CHG_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("DeleteParamType:", ?sig, ":", ?pname) AS ?name)
(?pty AS ?key) (?ctx_ AS ?key_)
(?a AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty ?ctx_ ?ivk
    ?args ?arg
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty ?ctx_ ?ivk
        WHERE {

          {
            SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty ?ctx_
            WHERE {

              ?meth a java:MethodOrConstructor ;
                    java:fullyQualifiedName ?fqn ;
                    java:signature ?sig0 ;
                    chg:mappedTo ?meth_ .

              ?meth_ a java:MethodOrConstructor ;
                     java:fullyQualifiedName ?fqn_ ;
                     java:signature ?sig0_ .

              FILTER(?sig0 != ?sig0_)

              ?params a java:Parameters ;
                      src:parent ?meth ;
                      chg:mappedTo ?params_ .

              ?params_ a java:Parameters ;
                       src:parent ?meth_ .

              ?param a java:Parameter ;
                     src:nth ?nth ;
                     java:name ?pname ;
                     src:parent ?params ;
                     src:child1 ?pty ;
                     chg:mappedTo ?param_ .

              ?param_ a java:Parameter ;
                      src:nth ?nth_ ;
                      java:name ?pname_ ;
                      src:parent ?params_ ;
                      src:child1 ?pty_ .

              ?pty chg:removal ?ctx_ .

              BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
              BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

            } GROUP BY ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty ?ctx_
          }

          ?ivk a java:InvocationOrInstanceCreation ;
               java:mayInvokeMethod ?meth .

        } GROUP BY ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty ?ctx_ ?ivk
      }

      ?args a java:Arguments ;
            src:parent ?ivk .

      ?arg a java:Argument ;
           src:nth ?nth ;
           src:parent ?args .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty ?ctx_
    ?ivk ?args ?arg
  }

  ?a src:parent* ?arg ;
     chg:relabeled ?a_ .

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth ;
         jref:movedMethod ?meth_ .
  }

}
}
''' % NS_TBL

Q_INS_PARAM_TY_CHG_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("InsertParamType:", ?sig_, ":", ?pname_) AS ?name)
(?ctx AS ?key) (?pty_ AS ?key_)
(?a AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty_ ?ctx ?ivk_
    ?args ?args_ ?arg ?arg_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty_ ?ctx ?ivk_
        WHERE {

          {
            SELECT DISTINCT ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty_ ?ctx
            WHERE {

              ?meth a java:MethodOrConstructor ;
                    java:fullyQualifiedName ?fqn ;
                    java:signature ?sig0 ;
                    chg:mappedTo ?meth_ .

              ?meth_ a java:MethodOrConstructor ;
                     java:fullyQualifiedName ?fqn_ ;
                     java:signature ?sig0_ .

              FILTER(?sig0 != ?sig0_)

              ?params a java:Parameters ;
                      src:parent ?meth ;
                      chg:mappedTo ?params_ .

              ?params_ a java:Parameters ;
                       src:parent ?meth_ .

              ?param a java:Parameter ;
                     src:nth ?nth ;
                     java:name ?pname ;
                     src:parent ?params ;
                     src:child1 ?pty ;
                     chg:mappedTo ?param_ .

              ?param_ a java:Parameter ;
                      src:nth ?nth_ ;
                      java:name ?pname_ ;
                      src:parent ?params_ ;
                      src:child1 ?pty_ .

              ?pty_ chg:addition ?ctx .

              BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
              BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

            } GROUP BY ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty_ ?ctx
          }

          ?ivk_ a java:InvocationOrInstanceCreation ;
                java:mayInvokeMethod ?meth_ .

        } GROUP BY ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty_ ?ctx ?ivk_
      }

      ?args_ a java:Arguments ;
             src:parent ?ivk_ .

      ?arg_ a java:Argument ;
            src:nth ?nth_ ;
            src:parent ?args_ .

    } GROUP BY ?meth ?meth_ ?sig ?sig_ ?nth ?nth_ ?pname ?pname_ ?pty_ ?ctx
    ?ivk_ ?args_ ?arg_
  }

  ?a chg:relabeled ?a_ .

  ?a_ src:parent* ?arg_ .

  FILTER NOT EXISTS {
    ?ref a jref:MoveMethod ;
         jref:originalMethod ?meth ;
         jref:movedMethod ?meth_ .
  }

}
}
''' % NS_TBL

Q_CHG_PARAM_TY_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamType:", ?sig_, ":", ?pname_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?arg AS ?ent) (?args_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  ?params a java:Parameters ;
          ?p_child ?param OPTION (INFERENCE NONE) ;
          src:parent ?meth ;
          chg:mappedTo ?params_ .

  ?params_ a java:Parameters ;
           ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
           src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:parent ?params ;
         chg:mappedTo ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:parent ?params_ .


  ?ty src:parent ?param ;
      chg:relabeled ?ty_ .

  ?ty_ src:parent ?param_ .


  OPTIONAL {
    SELECT DISTINCT ?ivk ?ivk_ ?args ?args_ ?p_child0 ?p_child0_ ?arg ?arg_ ?ty0 ?ty0_ ?meth ?meth_
    WHERE {

      ?ivk java:mayInvokeMethod ?meth ;
           chg:mappedTo ?ivk_ .

      ?ivk_ java:mayInvokeMethod ?meth_ .

      ?args a java:Arguments ;
            ?p_child0 ?arg OPTION (INFERENCE NONE) ;
            src:parent ?ivk ;
            chg:mappedTo ?args_ .

      ?args_ a java:Arguments ;
             ?p_child0_ ?arg_ OPTION (INFERENCE NONE) ;
             src:parent ?ivk_ .

      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0 rdfs:subPropertyOf src:child .
      }
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0_ rdfs:subPropertyOf src:child .
      }

      ?arg src:parent ?args ;
           chg:removal ?args_ .

      ?arg_ src:parent ?args_ .


    } GROUP BY ?ivk ?ivk_ ?args ?args_ ?p_child0 ?p_child0_ ?arg ?arg_ ?ty0 ?ty0_ ?meth ?meth_
  }

  FILTER (?p_child = ?p_child0)
  FILTER (?p_child_ = ?p_child0_)

}
}
''' % NS_TBL

Q_RM_PARAM_TY_RM_USE_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveParamType:", ?sig, ":", ?pname) AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?ty AS ?ent) (?ctxt_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  ?params a java:Parameters ;
          src:parent ?meth ;
          chg:mappedTo ?params_ .

  ?params_ a java:Parameters ;
           src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:child1 ?ty ;
         src:parent ?params ;
         chg:mappedTo ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:child1 ?ty_ ;
          src:parent ?params_ .


  ?ty src:parent ?param ;
      chg:removal ?ctxt_ .

  ?x java:declaredBy ?param ;
     java:name ?pname ;
     chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_PARAM_TY_ADD_USE_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddParamType:", ?sig, ":", ?pname) AS ?name)
(?ctxt AS ?dep) (?ty_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  ?params a java:Parameters ;
          src:parent ?meth ;
          chg:mappedTo ?params_ .

  ?params_ a java:Parameters ;
           src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:child1 ?ty ;
         src:parent ?params ;
         chg:mappedTo ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:child1 ?ty_ ;
          src:parent ?params_ .


  ?ty_ src:parent ?param_ ;
       chg:addition ?ctxt .

  ?x_ java:declaredBy ?param_ ;
      java:name ?pname_ ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_PARAM_TY_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParamType:", ?sig_, ":", ?pname_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?args AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER NOT EXISTS {
        ?ref a jref:MoveMethod ;
             jref:movedMethod ?meth_ .
      }

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?sig ?sig_
  }

  ?params a java:Parameters ;
          ?p_child ?param OPTION (INFERENCE NONE) ;
          src:parent ?meth ;
          chg:mappedTo ?params_ .

  ?params_ a java:Parameters ;
           ?p_child_ ?param_ OPTION (INFERENCE NONE) ;
           src:parent ?meth_ .

  ?param a java:Parameter ;
         java:name ?pname ;
         src:parent ?params ;
         chg:mappedTo ?param_ .

  ?param_ a java:Parameter ;
          java:name ?pname_ ;
          src:parent ?params_ .


  ?ty src:parent ?param ;
      chg:relabeled ?ty_ .

  ?ty_ src:parent ?param_ .


  OPTIONAL {
    SELECT DISTINCT ?ivk ?ivk_ ?args ?args_ ?p_child0 ?p_child0_ ?arg ?arg_ ?ty0 ?ty0_ ?meth ?meth_
    WHERE {

      ?ivk java:mayInvokeMethod ?meth ;
           chg:mappedTo ?ivk_ .

      ?ivk_ java:mayInvokeMethod ?meth_ .

      ?args a java:Arguments ;
            ?p_child0 ?arg OPTION (INFERENCE NONE) ;
            src:parent ?ivk ;
            chg:mappedTo ?args_ .

      ?args_ a java:Arguments ;
             ?p_child0_ ?arg_ OPTION (INFERENCE NONE) ;
             src:parent ?ivk_ .

      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0 rdfs:subPropertyOf src:child .
      }
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0_ rdfs:subPropertyOf src:child .
      }

      ?arg src:parent ?args .

      ?arg_ src:parent ?args_ ;
            chg:addition ?args .


    } GROUP BY ?ivk ?ivk_ ?args ?args_ ?p_child0 ?p_child0_ ?arg ?arg_ ?ty0 ?ty0_ ?meth ?meth_
  }

  FILTER (?p_child = ?p_child0)
  FILTER (?p_child_ = ?p_child0_)

}
}
''' % NS_TBL

Q_ADD_CTOR_INS_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddCtor:", ?sig_) AS ?name)
(?ctx AS ?key) (?ctor_ AS ?key_)
(?ctxa AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor_ a java:ConstructorDeclaration ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ ;
         chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?ctor chg:mappedTo ?ctor_ .
  }

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk_ a java:InstanceCreation ;
        java:mayInvokeMethod ?ctor_ .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?arg_ src:parent ?args_ ;
        chg:addition ?ctxa .

}
}
''' % NS_TBL

Q_ADD_CTOR_CHG_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddCtor:", ?sig_) AS ?name)
(?ctx AS ?key) (?ctor_ AS ?key_)
(?arg AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor_ a java:ConstructorDeclaration ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ ;
         chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?ctor chg:mappedTo ?ctor_ .
  }

  BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

  ?ivk_ a java:InstanceCreation ;
        java:mayInvokeMethod ?ctor_ .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?arg chg:relabeled ?arg_ .

  ?arg_ src:parent ?args_ .

}
}
''' % NS_TBL

Q_CHG_VDTOR_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVdtor:", ?cfqn, ":", ?vname) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor java:name ?vname ;
         java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ java:name ?vname_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     chg:relabeled ?x_ .

  {
    ?vdtor a java:VariableDeclarator .
    ?x java:declaredBy ?vdtor .
  }
  UNION
  {
    ?vdtor_ a java:VariableDeclarator .
    ?x_ java:declaredBy ?vdtor_ .
  }

}
}
''' % NS_TBL

Q_CHG_VDTOR_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVdtor:", ?cfqn, ":", ?vname) AS ?name)
(?vdtor AS ?ent) (?vdtor_ AS ?ent_)
(?x AS ?dep) (?ctx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ #a java:VariableDeclarator ;
          java:name ?vname_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_VDTOR_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVdtor:", ?cfqn, ":", ?vname) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?vdtor AS ?dep) (?vdtor_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor #a java:VariableDeclarator ;
         java:name ?vname ;
         java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ .

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_RETTY_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?facc AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?sig ?sig_ ?ver ?ver_ ?meth
    WHERE {

      ?meth java:fullyQualifiedName ?fqn ;
            java:inTypeDeclaration/ver:version ?ver ;
            java:signature ?sig0 ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:inTypeDeclaration/ver:version ?ver_ ;
             java:signature ?sig0_ ;
             src:child2 ?ty_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

      ?ty a java:ReferenceType ;
          chg:relabeled ?ty_ ;
          src:parent ?meth .

      ?ty_ a java:ReferenceType ;
           src:parent ?meth_ .

    } GROUP BY ?ty ?ty_ ?sig ?sig_ ?ver ?ver_ ?meth
  }

  ?ty_ java:name ?ty_name_ .

  ?iface_ a java:InterfaceDeclaration ;
          java:fullyQualifiedName ?ty_name_ .


  ?facc a java:FieldAccess ;
        src:child0 ?ivk ;
        src:parent+/src:inFile/src:location ?loc ;
        chg:removal ?ctx_ .

  ?ivk a java:Invocation ;
       java:mayInvokeMethod ?meth .

}
}
''' % NS_TBL

Q_CHG_RETTY_ADD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ctx AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?sig ?sig_ ?ver ?ver_ ?meth ?meth_
    WHERE {

      ?meth java:fullyQualifiedName ?fqn ;
            java:inTypeDeclaration/ver:version ?ver ;
            java:signature ?sig0 ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:inTypeDeclaration/ver:version ?ver_ ;
             java:signature ?sig0_ ;
             src:child2 ?ty_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

      ?ty a java:ReferenceType ;
          chg:relabeled ?ty_ ;
          src:parent ?meth .

      ?ty_ a java:ReferenceType ;
           src:parent ?meth_ .

    } GROUP BY ?ty ?ty_ ?sig ?sig_ ?ver ?ver_ ?meth ?meth_
  }

  ?ty java:name ?ty_name .

  ?iface a java:InterfaceDeclaration ;
         java:fullyQualifiedName ?ty_name .


  ?facc_ a java:FieldAccess ;
         src:parent+/src:inFile/src:location ?loc_ ;
         src:child0 ?ivk_ ;
         chg:addition ?ctx .

  ?ivk_ a java:Invocation ;
        java:mayInvokeMethod ?meth_ .

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_RETTY_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?sig_ ?tdecl_ ?mname_ ?msig_ ?tyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?ty ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?ty_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?msig_ .

      BIND (CONCAT(?fqn, ?msig) AS ?sig) .
      BIND (CONCAT(?fqn_, ?msig_) AS ?sig_) .

      ?ty a java:ReferenceType ;
          src:parent ?meth ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           src:parent ?meth_ ;
           java:name ?tyname_ .

    } GROUP BY ?ty ?ty_ ?sig_ ?tdecl_ ?mname_ ?msig_ ?tyname_
  }

  ?tdecl0_ java:subTypeOf+ ?tdecl_ .

  {
    SELECT DISTINCT ?ty0 ?ty0_ ?sig0_ ?tdecl0_ ?mname_ ?msig0_ ?tyname_
    WHERE {

      ?meth0 a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl0 ;
            src:child2 ?ty0 ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn0 ;
            java:signature ?msig ;
            chg:mappedTo ?meth0_ .

      ?meth0_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl0_ ;
             src:child2 ?ty0_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn0_ ;
             java:signature ?msig_ .

      BIND (CONCAT(?fqn0, ?msig) AS ?sig0) .
      BIND (CONCAT(?fqn0_, ?msig_) AS ?sig0_) .

      ?ty0 a java:ReferenceType ;
          src:parent ?meth0 ;
          chg:relabeled ?ty0_ .

      ?ty0_ a java:ReferenceType ;
           src:parent ?meth0_ ;
           java:name ?tyname_ .

    } GROUP BY ?ty0 ?ty0_ ?sig0_ ?tdecl0_ ?mname_ ?msig0_ ?tyname_
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_SUPERTY_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?sty AS ?ent) (?sty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?sig ?tdecl ?mname ?msig ?rtdecl
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?ty ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?ty_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?msig_ .

      BIND (CONCAT(?fqn, ?msig) AS ?sig) .
      BIND (CONCAT(?fqn_, ?msig_) AS ?sig_) .

      ?ty a java:ReferenceType ;
          src:parent ?meth ;
          java:refersToDeclaration ?rtdecl ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           src:parent ?meth_ .

    } GROUP BY ?ty ?ty_ ?sig ?tdecl ?mname ?msig ?rtdecl
  }

  ?tdecl0 java:fullyQualifiedName ?cfqn ;
          java:subTypeOf+ ?tdecl .


  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         src:child2 ?ty0 ;
         java:name ?mname ;
         java:fullyQualifiedName ?fqn0 ;
         java:signature ?msig0 ;
         chg:mappedTo ?meth0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          src:child2 ?ty0_ ;
          java:name ?mname_ ;
          java:fullyQualifiedName ?fqn0_ ;
          java:signature ?msig0_ .

  FILTER EXISTS {
    ?meth0 src:child0/src:child [a java:MarkerAnnotation ; java:name "Override"] .
  }

  BIND (CONCAT(?fqn0, ?msig) AS ?sig0) .
  BIND (CONCAT(?fqn0_, ?msig_) AS ?sig0_) .

  ?ty0 a java:ReferenceType ;
       java:refersToDeclaration ?rtdecl0 ;
       chg:mappedEqTo ?ty0_ .

  ?ty0_ a java:ReferenceType .


  ?rtdecl0 java:subTypeOf+ ?rtdecl .

  ?super a java:SuperType ;
         java:inTypeDeclaration ?rtdecl0 ;
         chg:mappedTo ?super_ .

  ?sty a java:ReferenceType ;
       src:parent ?super ;
       chg:relabeled ?sty_ .

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_SUPERTY_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?sty AS ?ent) (?sty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?sig_ ?tdecl_ ?mname_ ?msig_ ?rtdecl_
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?ty ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?ty_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?msig_ .

      BIND (CONCAT(?fqn, ?msig) AS ?sig) .
      BIND (CONCAT(?fqn_, ?msig_) AS ?sig_) .

      ?ty a java:ReferenceType ;
          src:parent ?meth ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           src:parent ?meth_ ;
           java:refersToDeclaration ?rtdecl_ .

    } GROUP BY ?ty ?ty_ ?sig_ ?tdecl_ ?mname_ ?msig_ ?rtdecl_
  }

  ?tdecl0_ java:fullyQualifiedName ?cfqn_ ;
           java:subTypeOf+ ?tdecl_ .


  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         src:child2 ?ty0 ;
         java:name ?mname ;
         java:fullyQualifiedName ?fqn0 ;
         java:signature ?msig0 ;
         chg:mappedTo ?meth0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          src:child2 ?ty0_ ;
          java:name ?mname_ ;
          java:fullyQualifiedName ?fqn0_ ;
          java:signature ?msig0_ .

  FILTER EXISTS {
    ?meth0_ src:child0/src:child [a java:MarkerAnnotation ; java:name "Override"] .
  }

  BIND (CONCAT(?fqn0, ?msig) AS ?sig0) .
  BIND (CONCAT(?fqn0_, ?msig_) AS ?sig0_) .

  ?ty0 a java:ReferenceType ;
       #src:parent ?meth0 ;
       chg:mappedEqTo ?ty0_ .

  ?ty0_ a java:ReferenceType ;
        #src:parent ?meth0_ ;
        java:refersToDeclaration ?rtdecl0_ .


  ?rtdecl0_ java:subTypeOf+ ?rtdecl_ .

  ?super_ a java:SuperType ;
          java:inTypeDeclaration ?rtdecl0_ ;
          ^chg:mappedTo ?super .

  ?sty_ a java:ReferenceType ;
        src:parent ?super_ ;
        ^chg:relabeled ?sty .

}
}
''' % NS_TBL

Q_RM_RETTY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveReturnType:", ?mfqn, ?msig) AS ?name)
(?ty AS ?key) (?ctx_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

 {
   SELECT DISTINCT ?ty ?ctx_ ?meth ?mname ?mfqn ?msig
   WHERE {

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?ty ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig .

      ?ty a java:ReferenceType ;
          chg:removal ?ctx_ .

   } GROUP BY ?ty ?ctx_ ?meth ?mname ?mfqn ?msig
 }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr .

  ?expr a java:Expression ;
        java:mayInvokeMethod ?meth0 .


  ?meth0 a java:MethodDeclaration ;
         src:child2 ?ty0 ;
         chg:mappedTo ?meth0_ .

  ?meth0_ a java:MethodDeclaration ;
          src:child2 ?ty0_ .

  ?ty0 a java:ReferenceType ;
       chg:relabeled ?ty0_ .

}
}
''' % NS_TBL

Q_ADD_RETTY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddReturnType:", ?mfqn_, ?msig_) AS ?name)
(?ctx AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

 {
   SELECT DISTINCT ?ty_ ?ctx ?meth_ ?mname_ ?mfqn_ ?msig_
   WHERE {

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?ty_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?ty_ a java:ReferenceType ;
           chg:addition ?ctx .

   } GROUP BY ?ty_ ?ctx ?meth_ ?mname_ ?mfqn_ ?msig_
 }

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr_ a java:Expression ;
         java:mayInvokeMethod ?meth0_ .


  ?meth0 a java:MethodDeclaration ;
         src:child2 ?ty0 ;
         chg:mappedTo ?meth0_ .

  ?meth0_ a java:MethodDeclaration ;
          src:child2 ?ty0_ .

  ?ty0 a java:ReferenceType ;
       chg:relabeled ?ty0_ .

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?mfqn, ?msig) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?meth ?meth_ ?mname ?mfqn ?msig
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?ty ;
            java:name ?mname ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?ty_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?ty a java:ReferenceType ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType .

    } GROUP BY ?ty ?ty_ ?meth ?meth_ ?mname ?mfqn ?msig
  }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr ;
       chg:mappedTo ?ret_ .

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr a java:Expression ;
        java:mayInvokeMethod ?meth0 ;
        chg:mappedTo ?expr_ .

  ?expr_ a java:Expression ;
         java:mayInvokeMethod ?meth0_ .


  ?meth0 a java:MethodDeclaration ;
         src:child2 ?ty0 ;
         chg:mappedTo ?meth0_ .

  ?meth0_ a java:MethodDeclaration ;
          src:child2 ?ty0_ .

  ?ty0 a java:ReferenceType ;
       chg:relabeled ?ty0_ .

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_LVD_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?mfqn, ?msig) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?vty AS ?ent) (?vty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?ty ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?ty_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?ty chg:relabeled ?ty_ .

    } GROUP BY ?ty ?ty_ ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_
  }

  ?vty src:parent ?vdecl ;
       chg:relabeled ?vty_ .

  ?vty_ src:parent ?vdecl_ .

  ?vdecl a java:LocalVariableDeclarationStatement ;
         java:inMethod ?meth ;
         src:child2 ?vdtor ;
         chg:mappedTo ?vdecl_ .

  ?vdecl_ a java:LocalVariableDeclarationStatement ;
          java:inMethod ?meth_ ;
          src:child2 ?vdtor_ .

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ .

  FILTER EXISTS {
    ?ret a java:ReturnStatement ;
         java:inMethod ?meth ;
         src:child0 ?x ;
         chg:mappedTo ?ret_ .

    ?ret_ a java:ReturnStatement ;
          java:inMethod ?meth_ ;
          src:child0 ?x_ .

    ?x java:declaredBy ?vdtor ;
       java:name ?vname ;
       chg:mappedTo ?x_ .

    ?x_ java:declaredBy ?vdtor_ ;
        java:name ?vname_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_RETTY_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?sig ?tdecl ?mname ?msig ?tyname
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            src:child2 ?rt ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             src:child2 ?rt_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?msig_ .

      BIND (CONCAT(?fqn, ?msig) AS ?sig) .
      BIND (CONCAT(?fqn_, ?msig_) AS ?sig_) .

      ?ty a java:ReferenceType ;
          src:parent ?meth ;
          java:name ?tyname ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           src:parent ?meth_ .

    } GROUP BY ?ty ?ty_ ?sig ?tdecl ?mname ?msig ?tyname
  }

  ?tdecl0 java:subTypeOf+ ?tdecl .

  {
    SELECT DISTINCT ?ty0 ?ty0_ ?sig0 ?tdecl0 ?mname ?msig0 ?tyname
    WHERE {

      ?meth0 a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl0 ;
            src:child2 ?ty0 ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn0 ;
            java:signature ?msig ;
            chg:mappedTo ?meth0_ .

      ?meth0_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl0_ ;
             src:child2 ?ty0_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn0_ ;
             java:signature ?msig_ .

      BIND (CONCAT(?fqn0, ?msig) AS ?sig0) .
      BIND (CONCAT(?fqn0_, ?msig_) AS ?sig0_) .

      ?ty0 a java:ReferenceType ;
          src:parent ?meth0 ;
          java:name ?tyname ;
          chg:relabeled ?ty0_ .

      ?ty0_ a java:ReferenceType ;
           src:parent ?meth0_ .

    } GROUP BY ?ty0 ?ty0_ ?sig0 ?tdecl0 ?mname ?msig0 ?tyname
  }

}
}
''' % NS_TBL

Q_CHG_LVD_TY_CHG_INI_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVType:", ?fqn, ?sig, ":", ?vname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

#  {
#    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig
#    WHERE {

      ?vdecl a java:LocalVariableDeclarationStatement ;
             java:inMethodOrConstructor ?meth ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?vdecl_ .

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

#    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig
#  }

  {
    ?vdtor src:child0 ?x .
    ?vdtor_ src:child0 ?x_ .
    ?x a java:Expression ;
       chg:relabeled ?x_ .
  }
  UNION
  {
    ?vdtor src:child0 ?init .
    ?vdtor_ src:child0 ?init_ .

    ?init a java:Expression ;
          chg:mappedTo ?init_ .

    ?x a java:Type ;
       src:parent+ ?init ;
       java:name ?ty_name ;
       chg:relabeled ?x_ .

    ?x_ a java:Type ;
        src:parent+ ?init_ ;
        java:name ?ty_name_ .

    FILTER EXISTS {
      ?ty java:name ?ty_name .
      ?ty_ java:name ?ty_name_ .
    }
  }

}
}
''' % NS_TBL

Q_CHG_LVD_TY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVType:", ?fqn, ":", ?vname) AS ?name)
(?vty AS ?key) (?vty_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vty ?vty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?fqn_ ?ivk ?ivk_
    WHERE {

  {
    SELECT DISTINCT ?vty ?vty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?fqn_
    WHERE {

      ?vty src:parent ?vdecl ;
           chg:relabeled ?vty_ .

      ?vty_ src:parent ?vdecl_ .

      ?vdecl a java:LocalVariableDeclarationStatement ;
             java:inMethodOrConstructor/java:fullyQualifiedName ?fqn ;
             src:child2 ?vdtor ;
             chg:mappedTo ?vdecl_ .

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ ;
              src:child2 ?vdtor_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

    } GROUP BY  ?vty ?vty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?fqn_
  }

  {
    ?vdtor src:child0 ?ivk .
    ?vdtor_ src:child0 ?ivk_ .
  }
  UNION
  {
    ?lhs java:declaredBy ?vdtor .
    ?lhs_ java:declaredBy ?vdtor_ .

    ?assign a java:AssignmentStatement ;
            src:child0 ?lhs ;
            src:child1 ?ivk ;
            chg:mappedTo ?assign_ .

    ?assign_ a java:AssignmentStatement ;
             src:child0 ?lhs_ ;
             src:child1 ?ivk_ .
  }

    } GROUP BY ?vty ?vty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?fqn_ ?ivk ?ivk_
  }

  ?ivk a java:Invocation ;
       chg:mappedTo ?ivk_ .

  ?ivk java:mayInvokeMethod ?meth .
  ?ivk_ java:mayInvokeMethod ?meth_ .

  {
    SELECT DISTINCT ?ty ?ty_ ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             src:child2 ?ty_ .

      ?ty chg:relabeled ?ty_ .

      BIND (CONCAT(?mfqn, ?msig) AS ?sig) .
      BIND (CONCAT(?mfqn_, ?msig_) AS ?sig_) .

    } GROUP BY ?ty ?ty_ ?meth ?meth_ ?sig ?sig_
  }

}
}
''' % NS_TBL

Q_RM_LVD_TY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveVType:", ?fqn, ":", ?vname) AS ?name)
(?vty AS ?dep) (?ctx_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vty ?ctx_ ?vdtor ?vname ?fqn
    WHERE {

      ?vty src:parent ?vdecl ;
           chg:removal ?ctx_ .

      ?vdecl a java:LocalVariableDeclarationStatement ;
             java:inMethodOrConstructor/java:fullyQualifiedName ?fqn ;
             src:child2 ?vdtor .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname .

    } GROUP BY ?vty ?ctx_ ?vdtor ?vname ?fqn
  }

  {
    ?vdtor src:child0 ?ivk .
  }
  UNION
  {
    ?lhs java:declaredBy ?vdtor .

    ?assign a java:AssignmentStatement ;
            src:child0 ?lhs ;
            src:child1 ?ivk .
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth .

  {
    SELECT DISTINCT ?ty ?ty_ ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ ;
             src:child2 ?ty_ .

      ?ty src:parent ?meth ;
          chg:relabeled ?ty_ .

      ?ty_ src:parent ?meth_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ty ?ty_ ?meth ?meth_ ?sig ?sig_
  }

}
}
''' % NS_TBL

Q_ADD_LVD_TY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddVType:", ?fqn_, ":", ?vname_) AS ?name)
(?ctx AS ?ent) (?vty_ AS ?ent_)
(?ty AS ?dep) (?ty_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?vty_ ?vdtor_ ?vname_ ?fqn_
    WHERE {

      ?vty_ src:parent ?vdecl_ ;
            chg:addition ?ctx .

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ ;
              src:child2 ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

    } GROUP BY ?ctx ?vty_ ?vdtor_ ?vname_ ?fqn_
  }

  {
    ?vdtor_ src:child0 ?ivk_ .
  }
  UNION
  {
    ?lhs_ java:declaredBy ?vdtor_ .

    ?assign_ a java:AssignmentStatement ;
             src:child0 ?lhs_ ;
             src:child1 ?ivk_ .
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ .

  {
    SELECT DISTINCT ?ty ?ty_ ?meth ?meth_ ?sig ?sig_
    WHERE {

      ?meth java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            src:child2 ?ty ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ ;
             src:child2 ?ty_ .

      ?ty src:parent ?meth ;
          chg:relabeled ?ty_ .

      ?ty_ src:parent ?meth_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ty ?ty_ ?meth ?meth_ ?sig ?sig_
  }

}
}
''' % NS_TBL

Q_CHG_LVD_TY_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVType:", ?fqn, ?sig, ":", ?vname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

#  {
#    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig
#    WHERE {

      ?vdecl a java:LocalVariableDeclarationStatement ;
             java:inMethodOrConstructor ?meth ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?vdecl_ .

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

#    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig
#  }

  {
    ?x_ java:declaredBy ?vdtor_ .
  }
  UNION
  {
    ?vdtor_ src:child0 ?x_ .
  }

  ?x_ a java:Expression ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_LVD_TY_INS_P_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVType:", ?fqn, ?sig, ":", ?vname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ctxp AS ?ent) (?px_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig ?fqn_ ?sig_
    WHERE {

  ?vdecl a java:LocalVariableDeclarationStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child1 ?ty ;
         src:child2 ?vdtor ;
         chg:mappedTo ?vdecl_ .

  ?vdecl_ a java:LocalVariableDeclarationStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child1 ?ty_ ;
          src:child2 ?vdtor_ .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ .

    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig ?fqn_ ?sig_
  }

  ?x java:declaredBy ?vdtor ;
     src:parent ?px ;
     chg:mappedTo ?x_ .

  ?x_ java:declaredBy ?vdtor_ ;
      src:parent ?px_ .

  ?px a ?catp OPTION (INFERENCE NONE) .

  ?px_ a ?catp_ OPTION (INFERENCE NONE) .

  FILTER (?catp IN (java:FieldAccess,
                    java:ArrayAccess,
                    java:PrimaryMethodInvocation,
                    java:PrimaryMethodInvocationStatement))

  FILTER (?catp_ IN (java:FieldAccess,
                     java:ArrayAccess,
                     java:PrimaryMethodInvocation,
                     java:PrimaryMethodInvocationStatement))

  ?px_ chg:addition ?ctxp .

}
}
''' % NS_TBL

Q_CHG_LVD_TY_DEL_P_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVType:", ?fqn, ?sig, ":", ?vname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?px AS ?ent) (?ctxp_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig ?fqn_ ?sig_
    WHERE {

      ?vdecl a java:LocalVariableDeclarationStatement ;
             java:inMethodOrConstructor ?meth ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?vdecl_ .

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              java:inMethodOrConstructor ?meth_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig ?fqn_ ?sig_
  }

  ?x java:declaredBy ?vdtor ;
     src:parent ?px ;
     chg:mappedTo ?x_ .

  ?x_ java:declaredBy ?vdtor_ ;
      src:parent ?px_ .

  ?px a ?catp OPTION (INFERENCE NONE) .

  ?px_ a ?catp_ OPTION (INFERENCE NONE) .

  FILTER (?catp IN (java:FieldAccess,
                    java:ArrayAccess,
                    java:PrimaryMethodInvocation,
                    java:PrimaryMethodInvocationStatement))

  FILTER (?catp_ IN (java:FieldAccess,
                     java:ArrayAccess,
                     java:PrimaryMethodInvocation,
                     java:PrimaryMethodInvocationStatement))

  ?px chg:removal ?ctxp_ .

}
}
''' % NS_TBL

Q_RM_LVD_INI_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveVIni:", ?fqn, ":", ?vname) AS ?name)
(?init AS ?key) (?ctx_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         java:inMethodOrConstructor ?meth ;
         src:child0 ?init ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ ;
          java:inMethodOrConstructor ?meth_ .

  ?init a java:Expression ;
        chg:removal ?ctx_ .

  ?meth java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:mappedTo ?meth_ .

  ?meth_ java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .


  ?x a ?cat OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor ;
     chg:relabeled ?x_ .

  ?x_ a ?cat_ OPTION (INFERENCE NONE) .

}
}
''' % NS_TBL

Q_CHG_LVD_TY_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeVType:", ?fqn, ?sig, ":", ?vname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig
    WHERE {

      ?vdecl a java:LocalVariableDeclarationStatement ;
             java:inMethodOrConstructor ?meth ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?vdecl_ .

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig
  }

  ?use java:declaredBy ?vdtor ;
       chg:mappedTo ?use_ .

  ?use_ java:declaredBy ?vdtor_ .

  {
    ?use chg:relabeled ?use_ .
    BIND(?use AS ?x)
    BIND(?use_ AS ?x_)
  }
  UNION
  {
    ?use src:parent ?x .
    ?use_ src:parent ?x_ .
  }
  UNION
  {
    ?op src:child0 ?use ;
        src:child1 ?x ;
        chg:mappedTo ?op_ .

    ?op_ src:child0 ?use_ ;
         src:child1 ?x_ .
  }
  UNION
  {
    ?op src:child0 ?x ;
        src:child1 ?use ;
        chg:mappedTo ?op_ .

    ?op_ src:child0 ?x_ ;
         src:child1 ?use_ .
  }

  ?x chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_RM_LVD_TY_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveVType:", ?fqn, ?sig, ":", ?vname) AS ?name)
(?ty AS ?key) (?ctx_ AS ?key_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig ?ctx_
    WHERE {

      ?vdecl a java:LocalVariableDeclarationStatement ;
             java:inMethodOrConstructor ?meth ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?vdecl_ .

      ?vdecl_ a java:LocalVariableDeclarationStatement ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig .

      ?ty a java:Type ;
          chg:removal ?ctx_ .

      ?ty_ a java:Type ;
           chg:addition ?ctx .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?vname_ .

    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?vname ?vname_ ?fqn ?sig ?ctx_
  }

  ?x java:declaredBy ?vdtor ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_CHG_FD_TY_CHG_FA_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFType:", ?fqn, ".", ?fname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ty0 AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn
  }

  ?facc a java:FieldAccess ;
        java:name ?fname ;
        java:inMethodOrConstructor ?meth ;
        chg:mappedTo ?facc_ .

  ?facc_ a java:FieldAccess ;
         java:name ?fname_ ;
         java:inMethodOrConstructor ?meth_ ;
         java:inTypeDeclaration ?tdecl_ .

  ?meth chg:mappedTo ?meth_ .

  ?vdecl0 a java:LocalVariableDeclarationStatement ;
          java:inMethodOrConstructor ?meth ;
          src:child1 ?ty0 ;
          src:child2 ?vdtor0 ;
          chg:mappedTo ?vdecl0_ .

  ?vdecl0_ a java:LocalVariableDeclarationStatement ;
           java:inMethodOrConstructor ?meth_ ;
           src:child1 ?ty0_ ;
           src:child2 ?vdtor0_ .

  ?ty0 chg:relabeled ?ty0_ .

  ?vdtor0 a java:VariableDeclarator ;
          java:name ?vname0 ;
          src:child0 ?init ;
          chg:mappedTo ?vdtor0_ .

  ?vdtor0_ a java:VariableDeclarator ;
           java:name ?vname0_ ;
           src:child0 ?init_ .

  ?facc src:parent* ?init .

  ?facc_ src:parent* ?init_ .

}
}
''' % NS_TBL

Q_CHG_FD_TY_CHG_PARAM_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFType:", ?fqn, ".", ?fname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?pty AS ?ent) (?pty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class ?class_
    WHERE {
      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?field_ .

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?ty a java:Type ;
          a ?cat OPTION (INFERENCE NONE) ;
          java:inField ?field ;
          chg:relabeled ?ty_ .

      ?ty_ a java:Type ;
           java:inField ?field_ .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ .

    } GROUP BY ?ty ?ty_ ?vdtor ?vdtor_ ?field ?field_ ?fname ?fname_ ?class ?class_
  }

  FILTER NOT EXISTS {
    ?ref a jref:MoveField ;
         jref:movedField ?field_ .
  }

  {
    SELECT DISTINCT ?class ?class_ ?fname ?fname_ ?fqn ?fqn_ ?x ?x_ ?meth ?meth_ ?pty ?pty_
    WHERE {

      ?subclass java:subClassOf* ?class ;
                java:fullyQualifiedName ?fqn ;
                chg:mappedTo ?subclass_ .

      ?subclass_ java:subClassOf* ?class_ ;
                 java:fullyQualifiedName ?fqn_ .


      {
        SELECT DISTINCT ?x ?x_ ?meth ?meth_ ?subclass ?subclass_ ?fname ?fname_
        WHERE {

          ?x a java:FieldAccess ;
             java:inMethodOrConstructor ?meth ;
             java:inTypeDeclaration ?subclass ;
             java:name ?fname ;
             chg:mappedTo ?x_ .

          ?x_ a java:FieldAccess ;
              java:inMethodOrConstructor ?meth_ ;
              java:inTypeDeclaration ?subclass_ ;
              java:name ?fname_ .

          ?meth chg:mappedTo ?meth_ .

        } GROUP BY ?x ?x_ ?meth ?meth_ ?subclass ?subclass_ ?fname ?fname_
      }

      ?params a java:Parameters ;
              src:parent ?meth ;
              chg:mappedTo ?params_ .

      ?params_ a java:Parameters ;
               src:parent ?meth_ .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params ;
             chg:mappedTo ?param_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

      ?pty a java:Type ;
           src:parent+ ?param ;
           chg:relabeled ?pty_ .

      ?pty_ a java:Type ;
            src:parent+ ?param_ .

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x .
      } || NOT EXISTS {
        [] src:parent ?x .
      })

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x_ .
      } || NOT EXISTS {
        [] src:parent ?x_ .
      })

      ?a a java:AssignmentStatement ;
         src:child0 ?x ;
         src:child1 ?e ;
         chg:mappedTo ?a_ .

      ?a_ a java:AssignmentStatement ;
          src:child0 ?x_ ;
          src:child1 ?e_ .

      ?v java:declaredBy ?param ;
         src:parent* ?e ;
         chg:mappedTo ?v_ .

      ?v_ java:declaredBy ?param_ ;
          src:parent* ?e_ .

    } GROUP BY ?class ?class_ ?fname ?fname_ ?fqn ?fqn_ ?x ?x_ ?meth ?meth_ ?pty ?pty_
  }

}
}
''' % NS_TBL

Q_CHG_LHS_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("ChangeLHS" AS ?name)
(?lhs AS ?key) (?lhs_ AS ?key_)
(?rhs AS ?ent) (?rhs_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?assign a java:AssignmentStatement ;
          src:child0 ?lhs ;
          src:child1 ?rhs ;
          chg:mappedTo ?assign_ .

  ?assign_ a java:AssignmentStatement ;
          src:child0 ?lhs_ ;
          src:child1 ?rhs_ .

  ?lhs chg:relabeled ?lhs_ .

  ?rhs chg:relabeled ?rhs_ .


  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?lhs ;
       delta:entity2 ?lhs_ .
  }
  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?rhs ;
       delta:entity2 ?rhs_ .
  }

}
}
''' % NS_TBL

Q_CHG_INI_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("ChangeInitializer" AS ?name)
(?retty AS ?dep) (?retty_ AS ?dep_)
(?ini AS ?ent) (?ini_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdecl a java:LocalVariableDeclarationStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child1 ?ty ;
         src:child2 ?vdtor ;
         chg:mappedTo ?vdecl_ .

  ?vdecl_ a java:LocalVariableDeclarationStatement ;
          src:child1 ?ty_ ;
          src:child2 ?vdtor_ .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig .

  ?ty a java:Type ;
      chg:mappedEqTo ?ty_ .

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         src:child0 ?ini ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname ;
          src:child0 ?ini_ .


  ?ini chg:relabeled ?ini_ .

  ?ini_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?callee_ .

  ?callee a java:MethodDeclaration ;
          src:child2 ?retty ;
          chg:mappedTo ?callee_ .

  ?callee_ a java:MethodDeclaration ;
           src:child2 ?retty_ .

  ?retty chg:relabeled ?retty_ .

}
}
''' % NS_TBL

Q_CHG_LHS_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("ChangeLHS" AS ?name)
(?lhs AS ?key) (?lhs_ AS ?key_)
(?ctx AS ?ent) (?rhs_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?assign a java:AssignmentStatement ;
          src:child0 ?lhs ;
          src:child1 ?rhs ;
          chg:mappedTo ?assign_ .

  ?assign_ a java:AssignmentStatement ;
          src:child0 ?lhs_ ;
          src:child1 ?rhs_ .

  ?lhs chg:relabeled ?lhs_ .

  ?rhs_ chg:addition ?ctx .

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?lhs ;
       delta:entity2 ?lhs_ .
  }
  FILTER EXISTS {
    [] a chg:Insertion ;
       delta:entity1 ?ctx ;
       delta:entity2 ?rhs_ .
  }

}
}
''' % NS_TBL

Q_CHG_LHS_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("ChangeLHS" AS ?name)
(?lhs AS ?key) (?lhs_ AS ?key_)
(?rhs AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?assign a java:AssignmentStatement ;
          src:child0 ?lhs ;
          src:child1 ?rhs ;
          chg:mappedTo ?assign_ .

  ?assign_ a java:AssignmentStatement ;
          src:child0 ?lhs_ ;
          src:child1 ?rhs_ .

  ?lhs chg:relabeled ?lhs_ .

  ?rhs chg:removal ?ctx_ .

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?lhs ;
       delta:entity2 ?lhs_ .
  }
  FILTER EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?rhs ;
       delta:entity2 ?ctx_ .
  }

}
}
''' % NS_TBL

Q_CHG_EQ_OPERAND_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("ChangeEq" AS ?name)
(?x AS ?key) (?x_ AS ?key_)
(?ctx AS ?ent) (?y_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?eqop a java:EqualityOp ;
        chg:mappedTo ?eqop_ .

  ?eqop_ a java:EqualityOp .

  ?x a java:Expression ;
     src:parent ?eqop ;
     chg:relabeled ?x_ .

  ?x_ src:parent ?eqop_ .

  ?y a java:Expression ;
     src:parent ?eqop .

  ?y_ src:parent ?eqop_ ;
      chg:addition ?ctx .

  FILTER (?x != ?y && ?x_ != ?y_)

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }

  FILTER EXISTS {
    [] a chg:Insertion ;
       delta:entity1 ?ctx ;
       delta:entity2 ?y_ .
  }

}
}
''' % NS_TBL

Q_CHG_EQ_OPERAND_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
("ChangeEqOperand" AS ?name)
(?x AS ?key) (?x_ AS ?key_)
(?y AS ?ent) (?y_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?eqop a java:EqualityOp ;
        chg:mappedTo ?eqop_ .

  ?eqop_ a java:EqualityOp .

  ?x a java:Expression ;
     src:parent ?eqop ;
     chg:relabeled ?x_ .

  ?x_ src:parent ?eqop_ .

  ?y a java:Expression ;
     src:parent ?eqop ;
     chg:relabeled ?y_ .

  ?y_ src:parent ?eqop_ .

  FILTER (?x != ?y && ?x_ != ?y_)

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }

  FILTER EXISTS {
    [] a chg:Relabeling ;
       delta:entity1 ?y ;
       delta:entity2 ?y_ .
  }

}
}
''' % NS_TBL

Q_ADD_IM_PARAM_ADD_M_PARAM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddIMethodParam:", ?fqn_) AS ?name)
(?ctx AS ?key) (?param_ AS ?key_)
(?ctx0 AS ?ent) (?param0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?param_ ?fqn_ ?sig_ ?mname_ ?iface ?iface_ ?iname_
    WHERE {

      ?param_ a java:Parameter ;
              src:parent ?params_ ;
              java:name ?pname_ ;
              chg:addition ?ctx .

      ?params_ a java:Parameters ;
               src:parent ?meth_ .

      ?meth a java:MethodDeclaration ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodDeclaration ;
             java:name ?mname_ ;
             java:signature ?sig_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:inInterface ?iface_ .

      ?iface a java:InterfaceDeclaration ;
             java:name ?iname_ ;
             chg:mappedTo ?iface_ .

    } GROUP BY ?ctx ?param_ ?fqn_ ?sig_ ?mname_ ?iface ?iface_ ?iname_
  }

  ?class_ a java:ClassDeclaration ;
          java:name ?cname_ ;
          java:subClassOf ?iface_ .

  FILTER NOT EXISTS {
    ?class_ src:child0 [a java:Abstract] .
  }

  {
    SELECT DISTINCT ?param0_ ?ctx0 ?mname_ ?sig_ ?class_
    WHERE {
      ?param0_ a java:Parameter ;
               src:parent ?params0_ ;
               java:name ?pname0_ ;
               chg:addition ?ctx0 .

      ?params0_ a java:Parameters ;
                src:parent ?meth0_ .

      ?meth0_ a java:MethodDeclaration ;
              java:name ?mname_ ;
              java:signature ?sig_ ;
              java:inClass ?class_ .

    } GROUP BY ?param0_ ?ctx0 ?mname_ ?sig_ ?class_
  }

}
}
''' % NS_TBL

Q_RM_EXPR_REL_EXPR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveExpr:", ?fqn) AS ?name)
(?expr AS ?key) (?ctx_ AS ?key_)
(?e AS ?ent) (?e_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?expr a java:Expression ;
        java:inMethodOrConstructor ?meth ;
        chg:removal ?ctx_ .

  ?meth java:fullyQualifiedName ?fqn .

  ?se a java:Expression ;
      src:parent ?expr ;
      chg:mappedEqTo ?se_ .

  ?se a java:Expression .

  ?e src:parent ?se ;
     chg:relabeled ?e_ .

  ?e_  src:parent ?se_ .

}
}
''' % NS_TBL

Q_ADD_RET_ADD_EXPR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddReturn:", ?fqn) AS ?name)
(?ctx AS ?key) (?ret_ AS ?key_)
(?ctxe AS ?ent) (?expr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ ;
        chg:addition ?ctx .

  ?meth a java:MethodDeclaration ;
        java:returnTypeName ?rtyname ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodDeclaration ;
         java:fullyQualifiedName ?fqn_ ;
         java:returnTypeName ?rtyname_ .

  FILTER (?rtyname != "void")
  FILTER (?rtyname_ != "void")

  ?expr_ a java:Expression ;
         chg:addition ?ctxe .

}
}
''' % NS_TBL

Q_RM_RETTY_RM_RETVAL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?ctx_ AS ?key_)
(?expr AS ?ent) (?ctxe_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?retty ?sig ?rtyname ?ctx_ #?meth_ ?retty_ ?sig_ ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 .
            # chg:mappedTo ?meth_ .

      ?retty chg:removal ?ctx_ .

      # ?meth_ a java:MethodDeclaration ;
      #        src:child2 ?retty_ ;
      #        java:returnTypeName ?rtyname_ ;
      #        java:inTypeDeclaration ?class_ ;
      #        java:name ?mname_ ;
      #        java:fullyQualifiedName ?fqn_ ;
      #        java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      # BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?retty ?sig ?rtyname ?ctx_ #?meth_ ?retty_ ?sig_ ?rtyname_
  }

  ?ret a java:ReturnStatement ;
        java:inMethod ?meth ;
        src:child0 ?expr .

  ?expr a java:Expression ;
        chg:removal ?ctxe_ .

}
}
''' % NS_TBL

Q_RM_RETTY_CHG_RETVAL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?ctx_ AS ?key_)
(?expr AS ?ent) (?expr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?retty ?sig ?rtyname ?ctx_ #?meth_ ?retty_ ?sig_ ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 .
            # chg:mappedTo ?meth_ .

      ?retty chg:removal ?ctx_ .

      # ?meth_ a java:MethodDeclaration ;
      #        src:child2 ?retty_ ;
      #        java:returnTypeName ?rtyname_ ;
      #        java:inTypeDeclaration ?class_ ;
      #        java:name ?mname_ ;
      #        java:fullyQualifiedName ?fqn_ ;
      #        java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      # BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?retty ?sig ?rtyname ?ctx_ #?meth_ ?retty_ ?sig_ ?rtyname_
  }

  ?ret a java:ReturnStatement ;
        java:inMethod ?meth ;
        src:child0 ?expr .

  ?expr a java:Expression ;
        chg:relabeled ?expr_ .

}
}
''' % NS_TBL

Q_ADD_RETTY_ADD_RETVAL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddReturnType:", ?sig) AS ?name)
(?ctx AS ?key) (?retty_ AS ?key_)
(?ctxe AS ?ent) (?expr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?retty_ ?sig_ ?rtyname_ ?ctx #?meth ?retty ?sig ?rtyname
    WHERE {

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?retty_ chg:addition ?ctx .

      # ?meth a java:MethodDeclaration ;
      #       src:child2 ?retty ;
      #       java:returnTypeName ?rtyname ;
      #       java:inTypeDeclaration ?class ;
      #       java:name ?mname ;
      #       java:fullyQualifiedName ?fqn ;
      #       java:signature ?sig0 ;
      #       chg:mappedTo ?meth_ .

      ?class chg:mappedTo ?class_ .

      # BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth_ ?retty_ ?sig_ ?rtyname_ ?ctx #?meth ?retty ?sig ?rtyname
  }

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr_ a java:Expression ;
         chg:addition ?ctxe .

}
}
''' % NS_TBL

Q_ADD_RETTY_CHG_RETVAL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddReturnType:", ?sig) AS ?name)
(?ctx AS ?key) (?retty_ AS ?key_)
(?expr AS ?ent) (?expr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?retty_ ?sig_ ?rtyname_ ?ctx #?meth ?retty ?sig ?rtyname
    WHERE {

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?retty_ chg:addition ?ctx .

      # ?meth a java:MethodDeclaration ;
      #       src:child2 ?retty ;
      #       java:returnTypeName ?rtyname ;
      #       java:inTypeDeclaration ?class ;
      #       java:name ?mname ;
      #       java:fullyQualifiedName ?fqn ;
      #       java:signature ?sig0 ;
      #       chg:mappedTo ?meth_ .

      ?class chg:mappedTo ?class_ .

      # BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth_ ?retty_ ?sig_ ?rtyname_ ?ctx #?meth ?retty ?sig ?rtyname
  }

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr_ a java:Expression ;
         ^chg:relabeled ?expr .

}
}
''' % NS_TBL

Q_CHG_RETTY_RM_RETVAL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?expr AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

#      FILTER (STR(?rtyname) != "void")
#      FILTER (STR(?rtyname_) = "void")

      ?class chg:mappedTo ?class_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr .

  ?expr a java:Expression ;
        chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_IVK_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?ivk AS ?dep) (?ivk_ AS ?dep_)
(?retty AS ?ent) (?retty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER (STR(?rtyname) != "void")

      ?class chg:mappedTo ?class_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ivk a java:Invocation ;
       java:inTypeDeclaration/java:name ?tname ;
       java:mayInvokeMethod ?meth ;
       chg:relabeled ?ivk_ .

  FILTER NOT EXISTS {
    ?ivk_ java:mayInvokeMethod ?meth_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_IVK_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?dep) (?retty_ AS ?dep_)
(?ivk AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      FILTER (STR(?rtyname_) != "void")

      ?class chg:mappedTo ?class_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ivk_ a java:Invocation ;
        java:inTypeDeclaration/java:name ?tname_ ;
        java:mayInvokeMethod ?meth_ ;
        ^chg:relabeled ?ivk .

  FILTER NOT EXISTS {
    ?ivk java:mayInvokeMethod ?meth .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_RETVAL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?expr AS ?ent) (?expr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr ;
       chg:mappedTo ?ret_ .

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr a java:Expression ;
        chg:relabeled ?expr_ .

  # FILTER NOT EXISTS {
  #   ?retty_ java:refersToDeclaration ?rdecl_ .
  #   ?expr_ java:ofReferenceType ?edecl_ .
  #   ?edecl_ java:subTypeOf* ?rdecl_ .
  # }

}
}
''' % NS_TBL

Q_CHG_RETTY_ADD_RETVAL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?ctx AS ?ent) (?expr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr_ a java:Expression ;
         chg:addition ?ctx .

}
}
''' % NS_TBL

# Q_ADD_SUPERTY_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# PREFIX delta: <%(delta_ns)s>
# SELECT DISTINCT
# (CONCAT("AddSuperType:", ?fqn_) AS ?name)
# (?ctx AS ?key) (?super_ AS ?key_)
# (?ivk AS ?ent) (?ivk_ AS ?ent_)
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   ?class a java:TypeDeclaration ;
#          java:name ?cname ;
#          java:fullyQualifiedName ?fqn ;
#          chg:mappedTo ?class_ .

#   ?class_ a java:TypeDeclaration ;
#           ver:version ?ver_ ;
#           java:name ?cname_ ;
#           java:fullyQualifiedName ?fqn_ .

#   ?super_ a java:SuperType ;
#           java:inTypeDeclaration ?class_ ;
#           chg:addition ?ctx .

#   ?ty_ a java:ReferenceType ;
#        java:name ?fqn0_ ;
#        src:parent ?super_ ;
#        chg:addition ?ctx .


#   ?class0_ a java:TypeDeclaration ;
#            ver:version ?ver_ ;
#            java:fullyQualifiedName ?fqn0_ .

#   ?ivk_ java:mayInvokeMethod ?meth_ ;
#         java:inTypeDeclaration ?class_ .

#   ?meth_ a java:MethodDeclaration ;
#          java:inTypeDeclaration ?class0_ .

#   ?ivk chg:relabeled ?ivk_ ;
#        chg:mappedStablyTo ?ivk_ .

# }
# }
# ''' % NS_TBL

Q_ADD_SUPERTY_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperType:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?ty_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
    WHERE {
    ?class a java:TypeDeclaration ;
           java:name ?cname ;
           java:fullyQualifiedName ?fqn ;
           chg:mappedTo ?class_ .

    ?class_ a java:TypeDeclaration ;
            ver:version ?ver_ ;
            java:name ?cname_ ;
            java:fullyQualifiedName ?fqn_ .

    ?super_ a java:SuperType ;
            java:inTypeDeclaration ?class_ .

    ?ty_ a java:ReferenceType ;
         java:name ?fqn0_ ;
         src:parent ?super_ ;
         chg:addition ?ctx .

    } GROUP BY ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
  }

  ?class0_ a java:TypeDeclaration ;
           ver:version ?ver_ ;
           java:subTypeOf* ?class1_ ;
           java:fullyQualifiedName ?fqn0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?class1_ .

  ?ivk_ java:mayInvokeMethod ?meth0_ ;
        java:inTypeDeclaration ?class_ ;
        chg:addition ?ctxi .

}
}
''' % NS_TBL

Q_ADD_SUPERTY_ADD_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperType:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?ty_ AS ?dep_)
(?ctxf AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
    WHERE {
      ?class a java:TypeDeclaration ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?class_ .

      ?ty_ a java:ReferenceType ;
           java:name ?fqn0_ ;
           src:parent ?super_ ;
           chg:addition ?ctx .

    } GROUP BY ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
  }

  ?facc_ a java:FieldAccess ;
         java:declaredBy ?vdtor_ ;
         java:inTypeDeclaration ?class_ ;
         chg:addition ?ctxf .

  ?vdtor_ a java:VariableDeclarator ;
          java:inTypeDeclaration ?class1_ .

  ?class0_ a java:TypeDeclaration ;
           ver:version ?ver_ ;
           java:subTypeOf* ?class1_ ;
           java:fullyQualifiedName ?fqn0_ .

}
}
''' % NS_TBL

Q_ADD_SUPERTY_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperType:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?ty_ AS ?dep_)
(?ivk AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
    WHERE {
      ?class a java:TypeDeclaration ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?class_ .

      ?ty_ a java:ReferenceType ;
           java:name ?fqn0_ ;
           src:parent ?super_ ;
           chg:addition ?ctx .

    } GROUP BY ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
  }

  ?class0_ a java:TypeDeclaration ;
           ver:version ?ver_ ;
           java:subTypeOf* ?class1_ ;
           java:fullyQualifiedName ?fqn0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?class1_ .

  ?ivk_ java:mayInvokeMethod ?meth0_ ;
        java:inTypeDeclaration ?class_ ;
        ^chg:relabeled ?ivk .

}
}
''' % NS_TBL

Q_ADD_SUPERTY_CHG_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperType:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?ty_ AS ?dep_)
(?facc AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
    WHERE {
      ?class a java:TypeDeclaration ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?class_ .

      ?ty_ a java:ReferenceType ;
           java:name ?fqn0_ ;
           src:parent ?super_ ;
           chg:addition ?ctx .

    } GROUP BY ?ver_ ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx ?ty_ ?fqn0_
  }

  ?facc_ a java:FieldAccess ;
         java:declaredBy ?vdtor_ ;
         java:inTypeDeclaration ?class_ ;
         ^chg:relabeled ?facc .

  ?vdtor_ a java:VariableDeclarator ;
          java:inTypeDeclaration ?class1_ .

  ?class0_ a java:TypeDeclaration ;
           ver:version ?ver_ ;
           java:subTypeOf* ?class1_ ;
           java:fullyQualifiedName ?fqn0_ .

}
}
''' % NS_TBL

Q_RM_SUPERTY_RM_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperType:", ?fqn) AS ?name)
(?ty AS ?ent) (?ctx_ AS ?ent_)
(?ivk AS ?dep) (?ctxi_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
    WHERE {
    ?class a java:TypeDeclaration ;
           ver:version ?ver ;
           java:name ?cname ;
           java:fullyQualifiedName ?fqn ;
           chg:mappedTo ?class_ .

    ?class_ a java:TypeDeclaration ;
            #ver:version ?ver_ ;
            java:name ?cname_ ;
            java:fullyQualifiedName ?fqn_ .

    ?super a java:SuperType ;
            java:inTypeDeclaration ?class .

    ?ty a java:ReferenceType ;
         java:name ?fqn0 ;
         src:parent ?super ;
         chg:removal ?ctx_ .

    } GROUP BY ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
  }


  ?class0 a java:TypeDeclaration ;
          ver:version ?ver ;
          java:subTypeOf* ?class1 ;
          java:fullyQualifiedName ?fqn0 .

  ?meth0 a java:MethodDeclaration ;
          java:inTypeDeclaration ?class1 .

  ?ivk java:mayInvokeMethod ?meth0 ;
       java:inTypeDeclaration ?class ;
       chg:removal ?ctxi_ .

}
}
''' % NS_TBL

Q_RM_SUPERTY_RM_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperType:", ?fqn) AS ?name)
(?ty AS ?ent) (?ctx_ AS ?ent_)
(?facc AS ?dep) (?ctxf_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
    WHERE {
    ?class a java:TypeDeclaration ;
           ver:version ?ver ;
           java:name ?cname ;
           java:fullyQualifiedName ?fqn ;
           chg:mappedTo ?class_ .

    ?class_ a java:TypeDeclaration ;
            #ver:version ?ver_ ;
            java:name ?cname_ ;
            java:fullyQualifiedName ?fqn_ .

    ?super a java:SuperType ;
            java:inTypeDeclaration ?class .

    ?ty a java:ReferenceType ;
         java:name ?fqn0 ;
         src:parent ?super ;
         chg:removal ?ctx_ .

    } GROUP BY ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
  }

  ?facc a java:FieldAccess ;
        java:declaredBy ?vdtor ;
        java:inTypeDeclaration ?class ;
        chg:removal ?ctxf_ .

  ?vdtor a java:VariableDeclarator ;
         java:inTypeDeclaration ?class1 .

  ?class0 a java:TypeDeclaration ;
          ver:version ?ver ;
          java:subTypeOf* ?class1 ;
          java:fullyQualifiedName ?fqn0 .

}
}
''' % NS_TBL

Q_RM_SUPERTY_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperType:", ?fqn) AS ?name)
(?ivk AS ?dep) (?ivk_ AS ?dep_)
(?ty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
    WHERE {
    ?class a java:TypeDeclaration ;
           ver:version ?ver ;
           java:name ?cname ;
           java:fullyQualifiedName ?fqn ;
           chg:mappedTo ?class_ .

    ?class_ a java:TypeDeclaration ;
            #ver:version ?ver_ ;
            java:name ?cname_ ;
            java:fullyQualifiedName ?fqn_ .

    ?super a java:SuperType ;
            java:inTypeDeclaration ?class .

    ?ty a java:ReferenceType ;
         java:name ?fqn0 ;
         src:parent ?super ;
         chg:removal ?ctx_ .

    } GROUP BY ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
  }

  ?class0 a java:TypeDeclaration ;
          ver:version ?ver ;
          java:subTypeOf* ?class1 ;
          java:fullyQualifiedName ?fqn0 .

  ?meth0 a java:MethodDeclaration ;
          java:inTypeDeclaration ?class1 .

  ?ivk java:mayInvokeMethod ?meth0 ;
       java:inTypeDeclaration ?class ;
       chg:relabeled ?ivk_ .

}
}
''' % NS_TBL

Q_RM_SUPERTY_CHG_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperType:", ?fqn) AS ?name)
(?facc AS ?dep) (?facc_ AS ?dep_)
(?ty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
    WHERE {
    ?class a java:TypeDeclaration ;
           ver:version ?ver ;
           java:name ?cname ;
           java:fullyQualifiedName ?fqn ;
           chg:mappedTo ?class_ .

    ?class_ a java:TypeDeclaration ;
            #ver:version ?ver_ ;
            java:name ?cname_ ;
            java:fullyQualifiedName ?fqn_ .

    ?super a java:SuperType ;
            java:inTypeDeclaration ?class .

    ?ty a java:ReferenceType ;
         java:name ?fqn0 ;
         src:parent ?super ;
         chg:removal ?ctx_ .

    } GROUP BY ?ver ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ctx_ ?ty ?fqn0
  }

  ?facc a java:FieldAccess ;
        java:declaredBy ?vdtor ;
        java:inTypeDeclaration ?class ;
        chg:relabeled ?facc_ .

  ?vdtor a java:VariableDeclarator ;
         java:inTypeDeclaration ?class1 .

  ?class0 a java:TypeDeclaration ;
          ver:version ?ver ;
          java:subTypeOf* ?class1 ;
          java:fullyQualifiedName ?fqn0 .

}
}
''' % NS_TBL

# Q_ADD_SUPERTY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# PREFIX delta: <%(delta_ns)s>
# SELECT DISTINCT
# (CONCAT("AddSuperType:", ?tyname_) AS ?name)
# (?ctx AS ?key) (?ty_ AS ?key_)
# (?ty0 AS ?ent) (?ty0_ AS ?ent_)
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   {
#     SELECT DISTINCT ?ver_ ?ctx ?ty_ ?tyname_ ?cfqn_
#     WHERE {
#       ?class a java:TypeDeclaration ;
#              java:name ?cname ;
#              java:fullyQualifiedName ?cfqn ;
#              chg:mappedTo ?class_ .

#       ?class_ a java:TypeDeclaration ;
#               ver:version ?ver_ ;
#               java:name ?cname_ ;
#               java:fullyQualifiedName ?cfqn_ .

#       ?super_ a java:SuperType ;
#               java:inTypeDeclaration ?class_ .

#       ?ty_ a java:ReferenceType ;
#            java:name ?tyname_ ;
#            src:parent ?super_ ;
#            chg:addition ?ctx .

#     } GROUP BY ?ver_ ?ctx ?ty_ ?tyname_ ?cfqn_
#   }

#   ?val_ a java:Expression ;
#         src:parent ?ret_ ;
#         java:typeName ?cfqn_ .

#   ?ret_ a java:ReturnStatement ;
#         java:inMethod ?meth0_ .

#   ?meth0_ a java:MethodDeclaration ;
#           java:inTypeDeclaration/ver:version ?ver_ ;
#           java:fullyQualifiedName ?mfqn0_ ;
#           src:child2 ?ty0_ .

#   ?ty0_ a java:ReferenceType ;
#         java:name ?tyname_ ;
#         ^chg:relabeled ?ty0 .

# }
# }
# ''' % NS_TBL

Q_ADD_SUPERTY_ADD_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddSuperType:", ?cfqn_) AS ?name)
(?ctx AS ?dep) (?ty_ AS ?dep_)
(?ctxt AS ?ent) (?ty0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver_ ?ctx ?ty_ ?tyname_ ?cfqn_ ?ty0_ ?ctxt ?meth0_ ?mfqn0_
    WHERE {

      {
        SELECT DISTINCT ?ver_ ?ctx ?ty_ ?tyname_ ?cfqn_
        WHERE {

          ?class a java:TypeDeclaration ;
                 java:name ?cname ;
                 java:fullyQualifiedName ?cfqn ;
                 chg:mappedTo ?class_ .

          ?class_ a java:TypeDeclaration ;
                  ver:version ?ver_ ;
                  java:name ?cname_ ;
                  java:fullyQualifiedName ?cfqn_ .

          ?super_ a java:SuperType ;
                  java:inTypeDeclaration ?class_ .

          ?ty_ a java:ReferenceType ;
               java:name ?tyname_ ;
               src:parent ?super_ ;
               chg:addition ?ctx .

        } GROUP BY ?ver_ ?ctx ?ty_ ?tyname_ ?cfqn_
      }

      ?ty0_ src:parent ?meth0_ ;
            java:name ?tyname_ ;
            chg:addition ?ctxt .

      ?meth0_ a java:MethodDeclaration ;
              java:inTypeDeclaration/ver:version ?ver_ ;
              java:fullyQualifiedName ?mfqn0_ ;
              src:child2 ?ty0_ .

    } GROUP BY ?ver_ ?ctx ?ty_ ?tyname_ ?cfqn_ ?ty0_ ?ctxt ?meth0_ ?mfqn0_
  }

  ?val_ a java:Expression ;
        src:parent ?ret_ ;
        java:typeName ?cfqn_ .

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth0_ .

}
}
''' % NS_TBL

Q_RM_SUPERTY_RM_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperType:", ?cfqn) AS ?name)
(?ty0 AS ?dep) (?ctxt_ AS ?dep_)
(?ty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?ctx_ ?ty ?tyname ?cfqn ?ty0 ?ctxt_ ?meth0 ?mfqn0
    WHERE {

      {
        SELECT DISTINCT ?ver ?ctx_ ?ty ?tyname ?cfqn
        WHERE {

          ?class a java:TypeDeclaration ;
                 ver:version ?ver ;
                 java:name ?cname ;
                 java:fullyQualifiedName ?cfqn ;
                 chg:mappedTo ?class_ .

          ?class_ a java:TypeDeclaration ;
                  #ver:version ?ver_ ;
                  java:name ?cname_ ;
                  java:fullyQualifiedName ?cfqn_ .

          ?super a java:SuperType ;
                 java:inTypeDeclaration ?class .

          ?ty a java:ReferenceType ;
              java:name ?tyname ;
              src:parent ?super ;
              chg:removal ?ctx_ .

        } GROUP BY ?ver ?ctx_ ?ty ?tyname ?cfqn
      }

      ?ty0 src:parent ?meth0 ;
           java:name ?tyname ;
           chg:removal ?ctxt_ .

      ?meth0 a java:MethodDeclaration ;
             java:inTypeDeclaration/ver:version ?ver ;
             java:fullyQualifiedName ?mfqn0 ;
             src:child2 ?ty0 .

    } GROUP BY ?ver ?ctx_ ?ty ?tyname ?cfqn ?ty0 ?ctxt_ ?meth0 ?mfqn0
  }

  ?val a java:Expression ;
       src:parent ?ret ;
       java:typeName ?cfqn .

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth0 .

}
}
''' % NS_TBL

Q_CHG_SUPERTY_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperType:", ?fqn_) AS ?name)
(?super AS ?key) (?super_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         java:fullyQualifiedName ?fqn ;
         chg:mappedTo ?class_ .

  ?class_ a java:TypeDeclaration ;
          java:name ?cname_ ;
          java:fullyQualifiedName ?fqn_ .

  ?super a java:SuperType ;
         java:inTypeDeclaration ?class ;
         chg:relabeled ?super_ .

  ?super_ a java:SuperType ;
          java:inTypeDeclaration ?class_ .

  ?ty a java:ReferenceType ;
      src:parent ?super ;
      chg:relabeled ?ty_ .

  ?ty_ a java:ReferenceType ;
       src:parent ?super_ .

}
}
''' % NS_TBL

Q_CHG_SUPERTY_ADD_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperType:", ?fqn_) AS ?name)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ty ?ty_
    WHERE {
      ?class a java:TypeDeclaration ;
             ver:version ?ver ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:TypeDeclaration ;
              ver:version ?ver_ ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn_ .

      ?super a java:SuperType ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?super_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?class_ .

      ?ty a java:ReferenceType ;
          src:parent ?super ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           src:parent ?super_ .

    } GROUP BY ?class ?class_ ?cname ?cname_ ?fqn ?fqn_ ?ty ?ty_
  }

  ?field_ a java:FieldDeclaration ;
          java:inTypeDeclaration ?class_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:inField ?field_ ;
          java:name ?fname_ ;
          chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?vdtor chg:mappedStablyTo ?vdtor_ .
  }
  # FILTER NOT EXISTS {
  #   ?ref a jref:MoveField ;
  #        jref:movedField ?field_ .
  # }

}
}
''' % NS_TBL

Q_RM_FIELD_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn, ".", ?fname) AS ?name)
(?ctx AS ?dep) (?ty_ AS ?dep_)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname ?fqn ?vdtor ?ctx_ ?fname
    WHERE {

      ?class a java:TypeDeclaration ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?class_ .

      ?field a java:FieldDeclaration ;
             java:inTypeDeclaration ?class .

      ?vdtor a java:VariableDeclarator ;
             java:inField ?field ;
             java:name ?fname ;
             chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo ?vdtor_ .
      }

    } GROUP BY ?class ?class_ ?cname ?fqn ?vdtor ?ctx_ ?fname
  }

  FILTER NOT EXISTS {
    ?class java:subTypeOf+ ?class0 .
    ?field0 a java:FieldDeclaration ;
            java:inTypeDeclaration ?class0 .
    ?vdtor0 a java:VariableDeclarator ;
            java:inField ?field0 ;
            java:name ?fname .
  }

  ?class_ a java:TypeDeclaration ;
          java:name ?cname_ ;
          java:fullyQualifiedName ?fqn_ .

  ?super_ a java:SuperType ;
          java:inTypeDeclaration ?class_ .

  ?ty_ a java:ReferenceType ;
       java:name ?tyname_ ;
       src:parent ?super_ ;
       chg:addition ?ctx .

  FILTER EXISTS {
    ?class_ java:subTypeOf ?class1_ .
    ?class1_ java:fullyQualifiedName ?tyname_ .
    ?class1_ java:subTypeOf* ?class0_ .
    ?field0_ a java:FieldDeclaration ;
             java:inTypeDeclaration ?class0_ .
    ?vdtor0_ a java:VariableDeclarator ;
             java:inField ?field0_ ;
             java:name ?fname .
  }

}
}
''' % NS_TBL

Q_ADD_FIELD_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddField:", ?fqn_, ".", ?fname_) AS ?name)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?ty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?cname_ ?fqn_ ?vdtor_ ?ctx ?fname_
    WHERE {

      ?class_ a java:TypeDeclaration ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn_ ;
              ^chg:mappedTo ?class .

      ?field_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?class_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inField ?field_ ;
              java:name ?fname_ ;
              chg:addition ?ctx .

      FILTER NOT EXISTS {
        ?vdtor chg:mappedStablyTo ?vdtor_ .
      }

    } GROUP BY ?class ?class_ ?cname_ ?fqn_ ?vdtor_ ?ctx ?fname_
  }

  FILTER NOT EXISTS {
    ?class_ java:subTypeOf+ ?class0_ .
    ?field0_ a java:FieldDeclaration ;
             java:inTypeDeclaration ?class0_ .
    ?vdtor0_ a java:VariableDeclarator ;
             java:inField ?field0_ ;
             java:name ?fname_ .
  }

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         java:fullyQualifiedName ?fqn .

  ?super a java:SuperType ;
         java:inTypeDeclaration ?class .

  ?ty a java:ReferenceType ;
      java:name ?tyname ;
      src:parent ?super ;
      chg:removal ?ctx_ .

  FILTER EXISTS {
    ?class java:subTypeOf ?class1 .
    ?class1 java:fullyQualifiedName ?tyname .
    ?class1 java:subTypeOf* ?class0 .
    ?field0 a java:FieldDeclaration ;
            java:inTypeDeclaration ?class0 .
    ?vdtor0 a java:VariableDeclarator ;
            java:inField ?field0 ;
            java:name ?fname_ .
  }

}
}
''' % NS_TBL

Q_CHG_SUPERTY_RM_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperType:", ?cfqn) AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
    WHERE {

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      ?super a java:SuperType ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?super_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?tdecl_ .

      ?ty a java:ReferenceType ;
          src:parent ?super ;
          java:refersToDeclaration ?td ;
          java:name ?tyname ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           java:refersToDeclaration ?td_ ;
           src:parent ?super_ ;
           java:name ?tyname_ .

    } GROUP BY ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
  }

  ?fdecl a java:FieldDeclaration ;
         java:inTypeDeclaration ?td0 ;
         src:child2 ?vdtor .

  ?td java:subTypeOf* ?td0 .

  ?x java:declaredBy ?vdtor ;
     java:name ?fname ;
     java:inTypeDeclaration* ?tdecl ;
     chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_SUPERTY_CHG_FACC_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperType:", ?cfqn) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
    WHERE {

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      ?super a java:SuperType ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?super_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?tdecl_ .

      ?ty a java:ReferenceType ;
          src:parent ?super ;
          java:refersToDeclaration ?td ;
          java:name ?tyname ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           java:refersToDeclaration ?td_ ;
           src:parent ?super_ ;
           java:name ?tyname_ .

    } GROUP BY ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
  }

  ?fdecl a java:FieldDeclaration ;
         java:inTypeDeclaration ?td0 ;
         src:child2 ?vdtor .

  ?td java:subTypeOf* ?td0 .

  ?x java:declaredBy ?vdtor ;
     java:name ?fname ;
     java:inTypeDeclaration* ?tdecl ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_CHG_SUPERTY_ADD_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperType:", ?cfqn) AS ?name)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
    WHERE {

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      ?super a java:SuperType ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?super_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?tdecl_ .

      ?ty a java:ReferenceType ;
          src:parent ?super ;
          java:refersToDeclaration ?td ;
          java:name ?tyname ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           java:refersToDeclaration ?td_ ;
           src:parent ?super_ ;
           java:name ?tyname_ .

    } GROUP BY ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
  }

  ?fdecl_ a java:FieldDeclaration ;
          java:inTypeDeclaration ?td0_ ;
          src:child2 ?vdtor_ .

  ?td_ java:subTypeOf* ?td0_ .

  ?x_ java:declaredBy ?vdtor_ ;
      java:name ?fname_ ;
      java:inTypeDeclaration* ?tdecl_ ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_SUPERTY_CHG_FACC_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperType:", ?cfqn) AS ?name)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
    WHERE {

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

      ?super a java:SuperType ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?super_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?tdecl_ .

      ?ty a java:ReferenceType ;
          src:parent ?super ;
          java:refersToDeclaration ?td ;
          java:name ?tyname ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           java:refersToDeclaration ?td_ ;
           src:parent ?super_ ;
           java:name ?tyname_ .

    } GROUP BY ?ty ?ty_ ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?tyname ?tyname_ ?td ?td_
  }

  ?fdecl_ a java:FieldDeclaration ;
          java:inTypeDeclaration ?td0_ ;
          src:child2 ?vdtor_ .

  ?td_ java:subTypeOf* ?td0_ .

  ?x_ java:declaredBy ?vdtor_ ;
      java:name ?fname_ ;
      java:inTypeDeclaration* ?tdecl_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_CHG_SUPERTY_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperType:", ?fqn_) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ivk AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?fqn ?fqn_ ?ty ?ty_
    WHERE {
      ?class a java:TypeDeclaration ;
             java:name ?cname ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?class_ .

      ?class_ a java:TypeDeclaration ;
              java:name ?cname_ ;
              java:fullyQualifiedName ?fqn_ .

      ?super a java:SuperType ;
             java:inTypeDeclaration ?class ;
             chg:mappedTo ?super_ .

      ?super_ a java:SuperType ;
              java:inTypeDeclaration ?class_ .

      ?ty a java:ReferenceType ;
          src:parent ?super ;
          chg:relabeled ?ty_ .

      ?ty_ a java:ReferenceType ;
           src:parent ?super_ .

    } GROUP BY ?class ?class_ ?fqn ?fqn_ ?ty ?ty_
  }

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?class ;
        java:fullyQualifiedName ?cfqn ;
        java:signature ?sig0 ;
        chg:mappedTo ?ctor_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?class_ ;
         java:fullyQualifiedName ?cfqn_ ;
         java:signature ?sig0_ .

  BIND (CONCAT(?cfqn, ?sig0) AS ?sig) .
  BIND (CONCAT(?cfqn_, ?sig0_) AS ?sig_) .


  ?ivk a java:InstanceCreation ;
       java:mayInvokeMethod ?ctor ;
       chg:relabeled ?ivk_ .

  ?ivk_ a java:InstanceCreation ;
        java:mayInvokeMethod ?ctor_ .

}
}
''' % NS_TBL

Q_RM_BR_ADD_BR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("BranchingStatement:", ?fqn_) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:BranchingStatement ;
     java:inMethodOrConstructor/java:fullyQualifiedName ?fqn ;
     chg:removal ?ctx_ ;
     src:parent ?ctx .

  ?x_ a java:BranchingStatement ;
      java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ ;
      chg:addition ?ctx ;
      src:parent ?ctx_ .

  ?ctx a src:ListNode .

  ?ctx_ a src:ListNode .

}
}
''' % NS_TBL

Q_RM_BR_ADD_NON_BR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("BranchingStatement:", ?fqn_) AS ?name)
(?stmt AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?stmt_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?stmt a java:BranchingStatement ;
        a ?cat OPTION (INFERENCE NONE) ;
        java:inMethodOrConstructor/java:fullyQualifiedName ?fqn ;
        src:parent ?block ;
        chg:removal ?ctx_ .

  ?block a src:ListNode ;
         chg:mappedTo ?block_ .

  ?stmt_ a java:Statement ;
         a ?cat_ OPTION (INFERENCE NONE) ;
         java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ ;
         src:parent ?block_ ;
         chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?stmt_ a java:BranchingStatement .
  }

  FILTER NOT EXISTS {
    ?s a java:Statement ;
       src:parent ?block .
    FILTER (?s != ?stmt)
  }
  FILTER NOT EXISTS {
    ?s_ a java:Statement ;
        src:parent ?block_ .
    FILTER (?s_ != ?stmt_)
  }

}
}
''' % NS_TBL


Q_D_INS_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(?ctx AS ?dep) (?x_ AS ?dep_)
(?ctxc AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?x_
    WHERE {

      ?x_ chg:addition ?ctx .

      FILTER (EXISTS {
        [] a chg:Insertion ;
           delta:entity1 ?ctx ;
           delta:entity2 ?x_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity2 ?x_ .
      })

    } GROUP BY ?ctx ?x_
  }

  #

  {
    SELECT DISTINCT ?x_ ?bx_
    WHERE {

      ?bx_ a src:ListNode ;
           src:parent* ?x_ ;
           chg:addition ?ctxb .

      FILTER ((?bx_ != ?x_ && NOT EXISTS {
        [] a chg:Insertion ;
           delta:entity1 ?ctxb ;
           delta:entity2 ?bx_ .
      } && NOT EXISTS {
        [] a chg:Move ;
           delta:entity2 ?bx_ .
      } && NOT EXISTS {
        ?x_ a [] .
        ?bx_ src:parent+ ?bx0_ .
        ?bx0_ src:parent+ ?x_ ;
              chg:addition ?ctxb0 .
        FILTER (EXISTS {
          [] a chg:Insertion ;
             delta:entity1 ?ctxb0 ;
             delta:entity2 ?bx0_ .
        } || EXISTS {
          [] a chg:Move ;
             delta:entity2 ?bx0_ .
        })
      }) || ?bx_ = ?x_ )

    } GROUP BY ?x_ ?bx_
  }

  #

  # {
  #   SELECT DISTINCT ?bx_ ?ctxc ?cx_ ?catc_
  #   WHERE {
      ?cx_ a ?catc_ OPTION (INFERENCE NONE) ;
           src:parent ?bx_ ;
           chg:addition ?ctxc .

      FILTER (EXISTS {
        [] a chg:Insertion ;
           delta:entity1 ?ctxc ;
           delta:entity2 ?cx_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity2 ?cx_ .
      })

  #   } GROUP BY ?bx_ ?ctxc ?cx_ ?catc_
  # }

  FILTER EXISTS {
    ?bx_ a ?catb_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catb_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
    }

    FILTER EXISTS {
      ?bx_ ?p_child_ ?cx_ OPTION (INFERENCE NONE) .
      ?cx_ a ?child_class_
    }

    FILTER NOT EXISTS {
      ?x_ src:parent+ ?px_ .
      ?px chg:mappedStablyTo ?px_ .

      FILTER NOT EXISTS {
        ?x_ src:parent+ ?px0_ .
        ?px0_ src:parent+ ?px_ .
        ?px0 chg:mappedStablyTo ?px0_ .
      }

      ?px_ a ?catp_ OPTION (INFERENCE NONE) .
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0_ rdfs:subPropertyOf src:child .
        ?catp_ rdfs:subClassOf* ?ln0_ .
        ?ln0_ owl:equivalentClass ?r0_ .
        ?r0_ a owl:Restriction ;
             owl:onProperty ?p_child0_ ;
             owl:onClass ?child_class_ .
      }
    }

  }

}
}
''' % NS_TBL

Q_D_DEL_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(?x AS ?ent) (?ctx_ AS ?ent_)
(?cx AS ?dep) (?ctxc_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?ctx_
    WHERE {

      ?x chg:removal ?ctx_ .

      FILTER (EXISTS {
        [] a chg:Deletion ;
           delta:entity1 ?x ;
           delta:entity2 ?ctx_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity1 ?x .
      })

    } GROUP BY ?x ?ctx_
  }

  #

  {
    SELECT DISTINCT ?x ?bx
    WHERE {

      ?bx a src:ListNode ;
          src:parent* ?x ;
          chg:removal ?ctxb_ .

      FILTER ((?bx != ?x && NOT EXISTS {
        [] a chg:Deletion ;
           delta:entity1 ?bx ;
           delta:entity2 ?ctxb_ .
      } && NOT EXISTS {
        [] a chg:Move ;
           delta:entity1 ?bx .
      } && NOT EXISTS {
        ?x a [] .
        ?bx src:parent+ ?bx0 .
        ?bx0 src:parent+ ?x ;
             chg:removal ?ctxb0_ .
        FILTER (EXISTS {
          [] a chg:Deletion ;
             delta:entity1 ?bx0 ;
             delta:entity2 ?ctxb0_ .
        } || EXISTS {
          [] a chg:Move ;
             delta:entity1 ?bx0 .
        })
      }) || ?bx = ?x )

    } GROUP BY ?x ?bx
  }

  #

  # {
  #   SELECT DISTINCT ?bx ?cx ?ctxc_ ?catc
  #   WHERE {

      ?cx a ?catc OPTION (INFERENCE NONE) ;
          src:parent ?bx ;
          chg:removal ?ctxc_ .

      FILTER (EXISTS {
        [] a chg:Deletion ;
           delta:entity1 ?cx ;
           delta:entity2 ?ctxc_ .
      } || EXISTS {
        [] a chg:Move ;
           delta:entity1 ?cx .
      })

  #   } GROUP BY ?bx ?cx ?ctxc_ ?catc
  # }

  FILTER EXISTS {
    ?bx a ?catb OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catb rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
    }

    FILTER EXISTS {
      ?bx ?p_child ?cx OPTION (INFERENCE NONE) .
      ?cx a ?child_class
    }

    FILTER NOT EXISTS {
      ?x src:parent+ ?px .
      ?px chg:mappedStablyTo ?px_ .

      FILTER NOT EXISTS {
        ?x src:parent+ ?px0 .
        ?px0 src:parent+ ?px .
        ?px0 chg:mappedStablyTo ?px0_ .
      }

      ?px a ?catp OPTION (INFERENCE NONE) .
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0 rdfs:subPropertyOf src:child .
        ?catp rdfs:subClassOf* ?ln0 .
        ?ln0 owl:equivalentClass ?r0 .
        ?r0 a owl:Restriction ;
            owl:onProperty ?p_child0 ;
            owl:onClass ?child_class .
      }
    }
  }

}
}
''' % NS_TBL

Q_ADD_STMT_ADD_RET_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddStatement:", ?fqn_) AS ?name)
(?ctxr AS ?dep) (?ret_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?fqn_ ?x_ ?ctx ?ret_ ?ctxr
    WHERE {

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ .

      ?x_ a java:BlockStatement ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition ?ctx .

      ?ret_ a java:ReturnStatement ;
            java:inMethodOrConstructor ?meth_ ;
            chg:addition ?ctxr .

      FILTER NOT EXISTS {
        ?ret_ java:successor [] .
      }
      FILTER NOT EXISTS {
        ?ret_ src:parent+ ?if_ .
        ?if_ a ?cati_ .
        FILTER (?cati_ IN (java:IfStatement, java:SwitchStatement)) .
      }

    } GROUP BY ?meth_ ?fqn_ ?x_ ?ctx ?ret_ ?ctxr
  }

  ?x_ java:successor ?ret_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

  # FILTER EXISTS {
  #   ?y0_ java:name ?name ;
  #        src:parent+ ?ret_ .

  #   ?y1_ java:name ?name ;
  #        src:parent* ?x_ .
  # }
  FILTER NOT EXISTS {
    [] a java:Literal ;
       src:parent ?ret_ .
  }

}
}
''' % NS_TBL

Q_RM_LOOP_RM_CONT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveLoop:", ?fqn) AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?stmt AS ?ent) (?ctxs_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    ?x a java:ContinueStatement ;
       src:parent+ ?stmt ;
       chg:removal ?ctx_ .

    ?stmt a java:LoopStatement ;
          chg:removal ?ctxs_ .
  }
  UNION
  {
    ?x a java:BreakStatement ;
       src:parent+ ?stmt ;
       chg:removal ?ctx_ .

    ?stmt a ?cats ;
          chg:removal ?ctxs_ .

    FILTER (?cats IN (java:LoopStatement, java:SwitchStatement))
  }

  ?x java:inMethodOrConstructor/java:fullyQualifiedName ?fqn .

}
}
''' % NS_TBL

Q_INS_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddStatement:", ?fqn_) AS ?name)
(?ctx0 AS ?key) (?ins0_ AS ?key_)
(?px AS ?ent) (?ins1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_ ?ins1_ ?cati1_ ?child_class
    WHERE {

      {
        SELECT DISTINCT ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_ ?ins1_ ?cati1_ ?p_child
        WHERE {

          {
            SELECT DISTINCT ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_ ?ins1_ ?cati1_
            WHERE {

              {
                SELECT DISTINCT ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_
                WHERE {

                  ?ins0_ a ?cati0_ OPTION (INFERENCE NONE) ;
                         src:parent+ ?px_ ;
                         chg:addition ?ctx0 .

                  ?px java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
                      chg:mappedStablyTo ?px_ .

                  ?px_ java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ .

                  FILTER NOT EXISTS {
                    ?px a src:ListNode .
                  }
                  FILTER NOT EXISTS {
                    ?px_ a src:ListNode .
                  }

                  ?x_ a ?catx_ OPTION (INFERENCE NONE) ;
                      src:parent+ ?ins0_ ;
                      src:parent+ ?px_ .

                  ?x a ?catx OPTION (INFERENCE NONE) ;
                     src:parent ?px ;
                     chg:mappedStablyTo ?x_ .

                } GROUP BY ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_
              }

              ?ins1_ a ?cati1_ OPTION (INFERENCE NONE) ;
                     chg:addition ?px .

            } GROUP BY ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_ ?ins1_ ?cati1_
          }

          ?px ?p_child ?x OPTION (INFERENCE NONE) .
          ?px_ ?p_child ?ins1_ .

        } GROUP BY ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_ ?ins1_ ?cati1_ ?p_child
      }

      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child rdfs:subPropertyOf src:child .
      }

      ?px a ?catp OPTION (INFERENCE NONE) .
      ?px_ a ?catp_ OPTION (INFERENCE NONE) .

      GRAPH <http://codinuum.com/ont/cpi> {
        ?catp rdfs:subClassOf* ?ln .
        ?ln owl:equivalentClass ?r .
        ?r a owl:Restriction ;
           owl:onProperty ?p_child ;
           owl:onClass ?child_class .
      }

    } GROUP BY ?ins0_ ?cati0_ ?px_ ?ctx0 ?px ?fqn ?fqn_ ?x ?x_ ?ins1_ ?cati1_ ?child_class
  }

  ?x a ?child_class .

}
}
''' % NS_TBL

Q_DEL_SIBLINGS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("DeleteSiblings:", ?fqn) AS ?name)
(?cx0 AS ?key) (?ctxc0_ AS ?key_)
(?cx1 AS ?ent) (?ctxc1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?cat ?cat_ ?fqn ?fqn_
    WHERE {

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
         chg:mappedStablyTo ?x_ .

      ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
          java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ .

      FILTER NOT EXISTS {
        ?x a src:ListNode .
      }

    } GROUP BY ?x ?x_ ?cat ?cat_ ?fqn ?fqn_
  }

  ?cx0 a ?catc0 OPTION (INFERENCE NONE) ;
      src:parent ?x ;
      chg:removal ?ctxc0_ .

  FILTER EXISTS {
    ?x a ?catx OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child0 rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child0 ;
         owl:onClass ?child_class0 .
    }
    FILTER EXISTS {
      ?x ?p_child0 ?cx0 OPTION (INFERENCE NONE) .
      ?cx0 a ?child_class0 .
    }
  }

  ?cx1 a ?catc1 OPTION (INFERENCE NONE) ;
       src:parent ?x ;
       chg:removal ?ctxc1_ .

  FILTER EXISTS {
    ?x a ?catx OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child1 rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child1 ;
         owl:onClass ?child_class1 .
    }
    FILTER EXISTS {
      ?x ?p_child1 ?cx1 OPTION (INFERENCE NONE) .
      ?cx1 a ?child_class1 .
    }
  }

  FILTER (?cx0 != ?cx1)

  FILTER EXISTS {
    ?cx0 a [] .
    ?ccx00 chg:mappedStablyTo ?ccx00_ .
    ?ccx00 src:parent+ ?cx0 .
    ?ccx00_ a ?child_class0 ;
            src:parent ?x_ .

    ?ccx01 chg:mappedStablyTo ?ccx01_ .
    ?ccx01 src:parent+ ?cx0 .
    ?ccx01_ a ?child_class1 ;
            src:parent ?x_ .

    FILTER (?ccx00_ != ?ccx01_)
  }

  FILTER NOT EXISTS {
    ?cx1 a [] .
    ?ccx1 src:parent+ ?cx1 ;
          chg:mappedStablyTo ?ccx1_ .
  }


  FILTER NOT EXISTS {

    ?cx0_ a ?catc0_ OPTION (INFERENCE NONE) ;
          src:parent ?x_ ;
          chg:addition ?ctxc0 .

    FILTER EXISTS {
      ?x_ a ?catx_ OPTION (INFERENCE NONE) .
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0_ rdfs:subPropertyOf src:child .
        ?catx_ rdfs:subClassOf* ?ln_ .
        ?ln_ owl:equivalentClass ?r_ .
        ?r_ a owl:Restriction ;
            owl:onProperty ?p_child0_ ;
            owl:onClass ?child_class0_ .
      }
      FILTER EXISTS {
        ?x_ ?p_child0_ ?cx0_ OPTION (INFERENCE NONE) .
        ?cx0_ a ?child_class0_ .
      }
    }

    ?cx1_ a ?catc1_ OPTION (INFERENCE NONE) ;
          src:parent ?x_ ;
          chg:addition ?ctxc1 .

    FILTER EXISTS {
      ?x_ a ?catx_ OPTION (INFERENCE NONE) .
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child1_ rdfs:subPropertyOf src:child .
        ?catx_ rdfs:subClassOf* ?ln_ .
        ?ln_ owl:equivalentClass ?r_ .
        ?r_ a owl:Restriction ;
            owl:onProperty ?p_child1_ ;
            owl:onClass ?child_class1_ .
      }
      FILTER EXISTS {
        ?x_ ?p_child1_ ?cx1_ OPTION (INFERENCE NONE) .
        ?cx1_ a ?child_class1_ .
      }
    }

    FILTER (?cx0_ != ?cx1_)

  }

}
}
''' % NS_TBL

Q_INS_SIBLINGS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("InsertSiblings:", ?fqn_) AS ?name)
(?ctxc0 AS ?key) (?cx0_ AS ?key_)
(?ctxc1 AS ?ent) (?cx1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?cat ?cat_ ?fqn ?fqn_
    WHERE {

      ?x a ?cat OPTION (INFERENCE NONE) ;
         java:inTypeDeclaration/java:fullyQualifiedName ?fqn ;
         chg:mappedStablyTo ?x_ .

      ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
          java:inTypeDeclaration/java:fullyQualifiedName ?fqn_ .

      FILTER NOT EXISTS {
        ?x a src:ListNode .
      }

    } GROUP BY ?x ?x_ ?cat ?cat_ ?fqn ?fqn_
  }

  ?cx0_ a ?catc0_ OPTION (INFERENCE NONE) ;
        src:parent ?x_ ;
        chg:addition ?ctxc0 .

  FILTER EXISTS {
    ?x_ a ?catx_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child0_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child0_ ;
          owl:onClass ?child_class0_ .
    }
    FILTER EXISTS {
      ?x_ ?p_child0_ ?cx0_ OPTION (INFERENCE NONE) .
      ?cx0_ a ?child_class0_ .
    }
  }

  ?cx1_ a ?catc1_ OPTION (INFERENCE NONE) ;
        src:parent ?x_ ;
        chg:addition ?ctxc1 .

  FILTER EXISTS {
    ?x_ a ?catx_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child1_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child1_ ;
          owl:onClass ?child_class1_ .
    }
    FILTER EXISTS {
      ?x_ ?p_child1_ ?cx1_ OPTION (INFERENCE NONE) .
      ?cx1_ a ?child_class1_ .
    }
  }

  FILTER (?cx0_ != ?cx1_)

  FILTER EXISTS {
    ?cx0_ a [] .
    ?ccx00 chg:mappedStablyTo ?ccx00_ .
    ?ccx00_ src:parent+ ?cx0_ .
    ?ccx00 a ?child_class0_ ;
           src:parent ?x .

    ?ccx01 chg:mappedStablyTo ?ccx01_ .
    ?ccx01_ src:parent+ ?cx0_ .
    ?ccx01 a ?child_class1_ ;
           src:parent ?x .

    FILTER (?ccx00 != ?ccx01)
  }

  FILTER NOT EXISTS {
    ?cx1_ a [] .
    ?ccx1 chg:mappedStablyTo ?ccx1_ .
    ?ccx1_ src:parent+ ?cx1_ .
  }


  FILTER NOT EXISTS {

    ?cx0 a ?catc0 OPTION (INFERENCE NONE) ;
         src:parent ?x ;
         chg:removal ?ctxc0_ .

    FILTER EXISTS {
      ?x a ?catx OPTION (INFERENCE NONE) .
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child0 rdfs:subPropertyOf src:child .
        ?catx rdfs:subClassOf* ?ln .
        ?ln owl:equivalentClass ?r .
        ?r a owl:Restriction ;
           owl:onProperty ?p_child0 ;
           owl:onClass ?child_class0 .
      }
      FILTER EXISTS {
        ?x ?p_child0 ?cx0 OPTION (INFERENCE NONE) .
        ?cx0 a ?child_class0 .
      }
    }

    ?cx1 a ?catc1 OPTION (INFERENCE NONE) ;
         src:parent ?x ;
         chg:removal ?ctxc1_ .

    FILTER EXISTS {
      ?x a ?catx OPTION (INFERENCE NONE) .
      GRAPH <http://codinuum.com/ont/cpi> {
        ?p_child1 rdfs:subPropertyOf src:child .
        ?catx rdfs:subClassOf* ?ln .
        ?ln owl:equivalentClass ?r .
        ?r a owl:Restriction ;
           owl:onProperty ?p_child1 ;
           owl:onClass ?child_class1 .
      }
      FILTER EXISTS {
        ?x ?p_child1 ?cx1 OPTION (INFERENCE NONE) .
        ?cx1 a ?child_class1 .
      }
    }

    FILTER (?cx0 != ?cx1)

  }

}
}
''' % NS_TBL

Q_DEL_METH_INS_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("DeleteMethod:", ?fqn) AS ?name)
(?meth AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:removal ?ctx_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ ;
         chg:addition ?ctx .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:name ?iname ;
       java:mayInvokeMethod ?meth ;
       src:treeDigest ?d ;
       chg:mappedEqTo ?ivk_ ;
       chg:mappedStablyTo ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:name ?iname_ ;
        src:treeDigest ?d ;
        java:mayInvokeMethod ?meth_ .

  FILTER (STRENDS(?fqn, ?iname))
  FILTER (STRENDS(?fqn_, ?iname_))

}
}
''' % NS_TBL

Q_CHG_METH_INS_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeMethod:", ?fqn) AS ?name)
(?meth AS ?key) (?meth0_ AS ?key_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:relabeled ?meth0_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ ;
         chg:addition ?ctx .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:name ?iname ;
       java:mayInvokeMethod ?meth ;
       src:treeDigest ?d ;
       chg:mappedEqTo ?ivk_ ;
       chg:mappedStablyTo ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:name ?iname_ ;
        src:treeDigest ?d ;
        java:mayInvokeMethod ?meth_ .

  FILTER (STRENDS(?fqn, ?iname))
  FILTER (STRENDS(?fqn_, ?iname_))

}
}
''' % NS_TBL

Q_DEL_METH_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("DeleteMethod:", ?fqn) AS ?name)
(?meth AS ?key) (?ctx_ AS ?key_)
(?meth0 AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:removal ?ctx_ .

  ?meth0 chg:relabled ?meth_ .
  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig_ .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:name ?iname ;
       java:mayInvokeMethod ?meth ;
       src:treeDigest ?d ;
       chg:mappedEqTo ?ivk_ ;
       chg:mappedStablyTo ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:name ?iname_ ;
        src:treeDigest ?d ;
        java:mayInvokeMethod ?meth_ .

  FILTER (STRENDS(?fqn, ?iname))
  FILTER (STRENDS(?fqn_, ?iname_))

}
}
''' % NS_TBL

Q_CHG_FIELD_TY_CHG_LVD_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType:", ?fqn) AS ?name)
(?tyl AS ?key) (?tyl_ AS ?key_)
(?tyr AS ?ent) (?tyr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?lhs ?lhs_ ?rhs ?rhs_ ?fqn
    WHERE {

      ?assign a java:AssignStatement ;
              java:inMethodOrConstructor/java:fullyQualifiedName ?fqn ;
              src:child0 ?lhs ;
              src:child1 ?rhs ;
              chg:mappedStablyTo ?assign_ .

      ?assign_ a java:AssignStatement ;
               src:child0 ?lhs_ ;
               src:child1 ?rhs_ .

      ?lhs chg:mappedStablyTo ?lhs_ .
      ?rhs chg:mappedStablyTo ?rhs_ .

    } GROUP BY ?lhs ?lhs_ ?rhs ?rhs_ ?fqn
  }

  ?lhs a java:FieldAccess ;
       java:name ?fname ;
       java:declaredBy ?fdtor .

  ?lhs_ a java:FieldAccess ;
        java:declaredBy ?fdtor_ .

  ?fdtor java:inField/src:child1 ?tyl .
  ?fdtor_ java:inField/src:child1 ?tyl_ .

  ?tyl chg:relabeled ?tyl_ .


  ?rhs java:declaredBy ?def .
  ?rhs_ java:declaredBy ?def_ .
  ?def chg:mappedStablyTo ?def_ .

  {
    ?def a java:Parameter ;
         src:child1 ?tyr .

    ?def_ a java:Parameter ;
          src:child1 ?tyr_ .
  }
  UNION
  {
    ?def a java:VariableDeclarator ;
         java:inVariableDeclaration ?vdecl .

    ?vdecl src:child1 ?tyr ;
           chg:mappedTo ?vdecl_ .

    ?vdecl_ src:child1 ?tyr_ ;
            src:child2 ?def_ .
  }

  ?tyr chg:relabeled ?tyr_ .

}
}
''' % NS_TBL

Q_CHG_IVK_RM_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeInvocation:", ?fqn) AS ?name)
(?ivk AS ?key) (?ivk_ AS ?key_)
(?arg AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk a java:InvocationOrInstanceCreation ;
       java:name ?mname ;
       java:inMethodOrConstructor/java:fullyQualifiedName ?fqn ;
       chg:relabeled ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:name ?mname_ ;
        java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ .

  ?args a java:Arguments ;
        src:parent ?ivk .

  ?arg a java:Expression ;
       src:parent ?args ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_IVK_ADD_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeInvocation:", ?fqn) AS ?name)
(?ivk AS ?key) (?ivk_ AS ?key_)
(?ctx AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk a java:InvocationOrInstanceCreation ;
       java:name ?mname ;
       java:inMethodOrConstructor/java:fullyQualifiedName ?fqn ;
       chg:relabeled ?ivk_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:name ?mname_ ;
        java:inMethodOrConstructor/java:fullyQualifiedName ?fqn_ .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
       chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_FIELD_INS_CAST_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?fqn, ".", ?fname) AS ?name)
(?ctx AS ?dep) (?cast_ AS ?dep_)
(?fdtor AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:FieldAccess ;
     java:name ?fname ;
     src:child0 ?e ;
     chg:mappedTo ?x_ .

  ?e java:ofReferenceType ?rty ;
     chg:mappedTo ?e_ .

  ?x_ a java:FieldAccess ;
      java:name ?fname ;
      src:child0/java:ofReferenceType ?rty_ .

  ?rty java:fullyQualifiedName ?fqn ;
       chg:mappedTo ?rty_ .

  ?rty_ java:fullyQualifiedName ?fqn_ .

 ?cast_ a java:Cast ;
        src:parent/src:parent ?x_ ;
        src:child1 ?e_ ;
        chg:addition ?ctx .


 ?e a java:FieldAccess ;
    java:declaredBy ?fdtor .

 ?fdtor chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_RM_RHS_ADD_INI_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveRHS:", ?vname) AS ?name)
(?ctx AS ?dep) (?ini_ AS ?dep_)
(?rhs AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rhs ?ini_
    WHERE {
      ?rhs chg:movedTo ?ini_ .

      FILTER EXISTS {
        [] a chg:Move ;
           delta:entity1 ?rhs ;
           delta:entity2 ?ini_ .
      }

    } GROUP BY ?rhs ?ini_
  }

  ?rhs a java:Expression ;
       src:parent ?assign ;
       chg:genRemoved ?ctx_ .

  ?assign a java:AssignmentStatement ;
          src:child0/java:name ?vname .

  ?ini_ a java:Expression ;
        src:parent ?vdtor_ ;
        chg:genAdded ?ctx .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname ;
          src:parent ?vdecl_ .

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         chg:mappedTo ?vdtor_ .

}
}
''' % NS_TBL

Q_CHG_PKG_MOV_FILE_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangePkg:", ?pname) AS ?name)
(?pkg AS ?key) (?pkg_ AS ?key_)
(?file AS ?ent) (?file_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?pkg ?pkg_ ?pname ?pname_ ?file ?file_
    WHERE {

      ?pkg a java:PackageDeclaration ;
           src:parent+/src:inFile ?file ;
           java:name ?pname ;
           chg:relabeled ?pkg_ .

      ?pkg_ a java:PackageDeclaration ;
            src:parent+/src:inFile ?file_ ;
            java:name ?pname_ .

    } GROUP BY ?pkg ?pkg_ ?pname ?pname_ ?file ?file_
  }

  ?file a src:File ;
        src:location ?loc ;
        chg:movedTo ?file_ .

  ?file_ a src:File ;
         src:location ?loc_ .

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?file ;
       delta:entity2 ?file_ .
  }

}
}
''' % NS_TBL

Q_MOV_METH_REL_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveRenameMethod:", ?fqn) AS ?name)
(?meth AS ?dep) (?meth_ AS ?dep_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?class ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:movRelabeled ?meth_ ;
        chg:relabeled ?meth_ ;
        chg:genRemoved ?ctx_ .

  ?meth_ a java:MethodDeclaration ;
        java:inTypeDeclaration ?class_ ;
        java:name ?mname_ ;
        java:fullyQualifiedName ?fqn_ ;
        java:signature ?sig_ ;
        chg:genAdded ?ctx .

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         chg:mappedStablyTo ?class_ .

  FILTER (?sig = ?sig_)

}
}
''' % NS_TBL

Q_RM_OVERRIDE_RENAME_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveOverride:", ?fqn) AS ?name)
(?annot AS ?dep) (?ctx_ AS ?dep_)
(?meth AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?annot a java:MarkerAnnotation ;
         java:name "Override" ;
         java:inMethod ?meth ;
         chg:removal ?ctx_ .

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?class ;
        java:name ?mname ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        chg:relabeled ?meth_ .

  ?meth_ a java:MethodDeclaration ;
        java:inTypeDeclaration ?class_ ;
        java:name ?mname_ ;
        java:fullyQualifiedName ?fqn_ ;
        java:signature ?sig_ .

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         chg:mappedTo ?class_ .

  FILTER NOT EXISTS {
    ?class_ java:subClassOf+ ?class0_ .

    ?meth0_ a java:MethodDeclaration ;
            java:inTypeDeclaration ?class0_ ;
            java:name ?mname_ ;
            java:fullyQualifiedName ?fqn0_ ;
            java:signature ?sig_ .
  }

}
}
''' % NS_TBL

Q_CHG_SUPER_RM_SUPERIVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveSuperInvocation:", ?fqn) AS ?name)
(?super AS ?dep) (?ctx_ AS ?dep_)
(?extends AS ?ent) (?implements_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?class a java:TypeDeclaration ;
         java:name ?cname ;
         java:fullyQualifiedName ?fqn ;
         chg:mappedTo ?class_ .

  ?class_ a java:TypeDeclaration ;
          java:name ?cname_ ;
          java:fullyQualifiedName ?fqn_ .

  ?extends a java:Extends ;
           java:inTypeDeclaration ?class ;
           chg:relabeled ?implements_ .

  ?implements_ a java:Implements ;
               java:inTypeDeclaration ?class_ .

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?class ;
        chg:mappedTo ?ctor_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?class_ .

  ?super a java:SuperInvocation ;
         java:inConstructor ?ctor ;
         chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_EXC_CHG_CATCH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeException:", ?ename) AS ?name)
(?exc AS ?key) (?exc_ AS ?key_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rty ?rty_ ?ename ?ename_ ?block ?block_
    WHERE {

      ?rty a java:ReferenceType ;
           java:name ?ename ;
           src:parent ?param ;
           chg:relabeled ?rty_ .

      ?rty_ a java:ReferenceType ;
            java:name ?ename_ ;
            src:parent ?param_ .

      ?param a java:CatchParameter ;
             java:name ?pname ;
             chg:mappedTo ?param_ .

      ?param_ a java:CatchParameter ;
              java:name ?pname_ .

      ?catch a java:CatchClause ;
             src:parent ?try ;
             src:child0 ?param ;
             chg:mappedTo ?catch_ .

      ?catch_ a java:CatchClause ;
              src:parent ?try_ ;
              src:child0 ?param_ .

      ?try a java:TryStatement ;
           #java:inMethodOrConstructor ?meth ;
           src:child1 ?block ;
           src:child2 ?catch ;
           chg:mappedTo ?try_ .

      ?try_ a java:TryStatement ;
            #java:inMethodOrConstructor ?meth_ ;
            src:child1 ?block_ ;
            src:child2 ?catch_ .

    } GROUP BY ?rty ?rty_ ?ename ?ename_ ?block ?block_
  }

  {
    ?ivk a java:InvocationOrInstanceCreation ;
         src:parent+ ?block ;
         java:name ?iname ;
         java:mayInvokeMethod ?callee .

    ?callee a java:MethodOrConstructor ;
            src:child3|src:child4 ?throws .

    ?throws a java:Throws ;
            src:child0 ?exc .

    ?exc a java:ReferenceType ;
         java:name ?ename ;
         chg:relabeled ?exc_ .
  }
  UNION
  {
    ?ivk_ a java:InvocationOrInstanceCreation ;
          src:parent+ ?block_ ;
          java:name ?iname_ ;
          java:mayInvokeMethod ?callee_ .

    ?callee_ a java:MethodOrConstructor ;
             src:child3|src:child4 ?throws_ .

    ?throws_ a java:Throws ;
             src:child0 ?exc_ .

    ?exc_ a java:ReferenceType ;
          java:name ?ename_ .

    ?exc chg:relabeled ?exc_ .
  }

}
}
''' % NS_TBL

Q_ADD_EXC_CHG_CATCH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddException:", ?ename_) AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rty ?rty_ ?ename ?ename_ ?block ?block_
    WHERE {

      ?rty a java:ReferenceType ;
           java:name ?ename ;
           src:parent ?param ;
           chg:relabeled ?rty_ .

      ?rty_ a java:ReferenceType ;
            java:name ?ename_ ;
            src:parent ?param_ .

      ?param a java:CatchParameter ;
             java:name ?pname ;
             chg:mappedTo ?param_ .

      ?param_ a java:CatchParameter ;
              java:name ?pname_ .

      ?catch a java:CatchClause ;
             src:parent ?try ;
             src:child0 ?param ;
             chg:mappedTo ?catch_ .

      ?catch_ a java:CatchClause ;
              src:parent ?try_ ;
              src:child0 ?param_ .

      ?try a java:TryStatement ;
           #java:inMethodOrConstructor ?meth ;
           src:child1 ?block ;
           src:child2 ?catch ;
           chg:mappedTo ?try_ .

      ?try_ a java:TryStatement ;
            #java:inMethodOrConstructor ?meth_ ;
            src:child1 ?block_ ;
            src:child2 ?catch_ .

    } GROUP BY ?rty ?rty_ ?ename ?ename_ ?block ?block_
  }

  {
    ?x_ a java:ThrowStatement ;
        src:parent+ ?block_ ;
        src:child0/java:typeName ?ename_ ;
        chg:addition ?ctx .
  }
  UNION
  {
    ?x_ a java:InvocationOrInstanceCreation ;
        src:parent+ ?block_ ;
        java:name ?iname_ ;
        java:mayInvokeMethod ?callee_ ;
        chg:addition ?ctx .

    ?callee_ a java:MethodOrConstructor ;
             src:child3|src:child4 ?throws_ .

    ?throws_ a java:Throws ;
             src:child0 ?exc_ .

    ?exc_ a java:ReferenceType ;
          java:name ?ename_ .
  }
  UNION
  {
    ?ivk_ a java:InvocationOrInstanceCreation ;
          src:parent+ ?block_ ;
          java:name ?iname_ ;
          java:mayInvokeMethod ?callee_ .

    ?callee_ a java:MethodOrConstructor ;
             src:child3|src:child4 ?throws_ .

    ?throws_ a java:Throws ;
             src:child0 ?exc_ .

    ?x_ a java:ReferenceType ;
        java:name ?ename_ ;
        chg:addition ?ctx .
  }

}
}
''' % NS_TBL

Q_RM_EXC_CHG_CATCH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveException:", ?ename) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rty ?rty_ ?ename ?ename_ ?block ?block_
    WHERE {

      ?rty a java:ReferenceType ;
           java:name ?ename ;
           src:parent ?param ;
           chg:relabeled ?rty_ .

      ?rty_ a java:ReferenceType ;
            java:name ?ename_ ;
            src:parent ?param_ .

      ?param a java:CatchParameter ;
             java:name ?pname ;
             chg:mappedTo ?param_ .

      ?param_ a java:CatchParameter ;
              java:name ?pname_ .

      ?catch a java:CatchClause ;
             src:parent ?try ;
             src:child0 ?param ;
             chg:mappedTo ?catch_ .

      ?catch_ a java:CatchClause ;
              src:parent ?try_ ;
              src:child0 ?param_ .

      ?try a java:TryStatement ;
           #java:inMethodOrConstructor ?meth ;
           src:child1 ?block ;
           src:child2 ?catch ;
           chg:mappedTo ?try_ .

      ?try_ a java:TryStatement ;
            #java:inMethodOrConstructor ?meth_ ;
            src:child1 ?block_ ;
            src:child2 ?catch_ .

    } GROUP BY ?rty ?rty_ ?ename ?ename_ ?block ?block_
  }

  {
    ?x a java:ThrowStatement ;
       src:parent+ ?block ;
       src:child0/java:typeName ?ename ;
       chg:removal ?ctx_ .
  }
  UNION
  {
    ?x a java:InvocationOrInstanceCreation ;
       src:parent+ ?block ;
       java:name ?iname ;
       java:mayInvokeMethod ?callee ;
       chg:removal ?ctx_ .

    ?callee a java:MethodOrConstructor ;
            src:child3|src:child4 ?throws .

    ?throws a java:Throws ;
            src:child0 ?exc .

    ?exc a java:ReferenceType ;
         java:name ?ename .
  }
  UNION
  {
    ?ivk a java:InvocationOrInstanceCreation ;
         src:parent+ ?block ;
         java:name ?iname ;
         java:mayInvokeMethod ?callee .

    ?callee a java:MethodOrConstructor ;
            src:child3|src:child4 ?throws .

    ?throws a java:Throws ;
            src:child0 ?exc .

    ?x a java:ReferenceType ;
       java:name ?ename ;
       chg:removal ?ctx_ .
  }

}
}
''' % NS_TBL

Q_ADD_EXC_ADD_CATCH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddException:", ?ename_) AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?ctx0 AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx0 ?rty_ ?ename_ ?block_
    WHERE {

      ?rty_ a java:ReferenceType ;
            java:name ?ename_ ;
            chg:addition ?ctx0 .

      ?param_ a java:CatchParameter ;
              src:child1 ?rty_ ;
              java:name ?pname_ .

      ?catch_ a java:CatchClause ;
              src:parent ?try_ ;
              src:child0 ?param_ .

      ?try_ a java:TryStatement ;
            src:child1 ?block_ ;
            src:child2 ?catch_ .

    } GROUP BY ?ctx0 ?rty_ ?ename_ ?block_
  }

  {
    ?x_ a java:ThrowStatement ;
        src:parent+ ?block_ ;
        src:child0/java:typeName ?ename_ ;
        chg:addition ?ctx .
  }
  UNION
  {
    ?x_ a java:InvocationOrInstanceCreation ;
        src:parent+ ?block_ ;
        java:name ?iname_ ;
        java:mayInvokeMethod ?callee_ ;
        chg:addition ?ctx .

    ?callee_ a java:MethodOrConstructor ;
             src:child3|src:child4 ?throws_ .

    ?throws_ a java:Throws ;
             src:child0 ?exc_ .

    ?exc_ a java:ReferenceType ;
          java:name ?ename_ .
  }
  UNION
  {
    ?ivk_ a java:InvocationOrInstanceCreation ;
          src:parent+ ?block_ ;
          java:name ?iname_ ;
          java:mayInvokeMethod ?callee_ .

    ?callee_ a java:MethodOrConstructor ;
             src:child3|src:child4 ?throws_ .

    ?throws_ a java:Throws ;
             src:child0 ?exc_ .

    ?x_ a java:ReferenceType ;
        java:name ?ename_ ;
        chg:addition ?ctx .
  }

}
}
''' % NS_TBL

Q_RM_EXC_RM_CATCH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveException:", ?ename) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?rty AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx0_ ?rty ?ename ?block
    WHERE {

      ?rty a java:ReferenceType ;
           java:name ?ename ;
           chg:removal ?ctx0_ .

      ?param a java:CatchParameter ;
             src:child1 ?rty ;
             java:name ?pname .

      ?catch a java:CatchClause ;
             src:parent ?try ;
             src:child0 ?param .

      ?try a java:TryStatement ;
           src:child1 ?block ;
           src:child2 ?catch .

    } GROUP BY ?ctx0_ ?rty ?ename ?block
  }

  {
    ?x a java:ThrowStatement ;
       src:parent+ ?block ;
       src:child0/java:typeName ?ename ;
       chg:removal ?ctx_ .
  }
  UNION
  {
    ?x a java:InvocationOrInstanceCreation ;
       src:parent+ ?block ;
       java:name ?iname ;
       java:mayInvokeMethod ?callee ;
       chg:removal ?ctx_ .

    ?callee a java:MethodOrConstructor ;
            src:child3|src:child4 ?throws .

    ?throws a java:Throws ;
            src:child0 ?exc .

    ?exc a java:ReferenceType ;
         java:name ?ename .
  }
  UNION
  {
    ?ivk a java:InvocationOrInstanceCreation ;
         src:parent+ ?block ;
         java:name ?iname ;
         java:mayInvokeMethod ?callee .

    ?callee a java:MethodOrConstructor ;
            src:child3|src:child4 ?throws .

    ?throws a java:Throws ;
            src:child0 ?exc .

    ?x a java:ReferenceType ;
       java:name ?ename ;
       chg:removal ?ctx_ .
  }

}
}
''' % NS_TBL

Q_CHG_EXC_RM_CATCH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeException:", ?fqn) AS ?name)
(?exc AS ?key) (?exc_ AS ?key_)
(?rty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?exc ?exc_ ?callee ?ename ?ename_
    WHERE {

      ?callee a java:MethodOrConstructor ;
              src:child3|src:child4 ?throws .

      ?throws a java:Throws ;
              src:child0 ?exc .

      ?exc a java:ReferenceType ;
           java:name ?ename ;
           chg:relabeled ?exc_ .

      ?exc_ a java:ReferenceType ;
            java:name ?ename_ .

    } GROUP BY ?exc ?exc_ ?callee ?ename ?ename_
  }

  ?try a java:TryStatement ;
       #java:inMethodOrConstructor ?meth ;
       src:child1 ?block ;
       src:child2 ?catch .

  ?ivk a java:InvocationOrInstanceCreation ;
       src:parent+ ?block ;
       java:name ?iname ;
       java:mayInvokeMethod ?callee .

  ?catch a java:CatchClause ;
         src:parent ?try ;
         src:child0 ?param .

  ?param a java:CatchParameter ;
         src:child1 ?rty ;
         java:name ?pname .

  ?rty a java:ReferenceType ;
       java:name ?ename ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_EXC_ADD_CATCH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeException:", ?fqn) AS ?name)
(?exc AS ?key) (?exc_ AS ?key_)
(?ctx AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?exc ?exc_ ?callee_ ?ename ?ename_
    WHERE {

      ?callee_ a java:MethodOrConstructor ;
               src:child3|src:child4 ?throws_ .

      ?throws_ a java:Throws ;
               src:child0 ?exc_ .

      ?exc a java:ReferenceType ;
           java:name ?ename ;
           chg:relabeled ?exc_ .

      ?exc_ a java:ReferenceType ;
            java:name ?ename_ .

    } GROUP BY ?exc ?exc_ ?callee_ ?ename ?ename_
  }

  ?try_ a java:TryStatement ;
        #java:inMethodOrConstructor ?meth_ ;
        src:child1 ?block_ ;
        src:child2 ?catch_ .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        src:parent+ ?block_ ;
        java:name ?iname_ ;
        java:mayInvokeMethod ?callee_ .

  ?catch_ a java:CatchClause ;
          src:parent ?try_ ;
          src:child0 ?param_ .

  ?param_ a java:CatchParameter ;
          src:child1 ?rty_ ;
          java:name ?pname_ .

  ?rty_ a java:ReferenceType ;
        java:name ?ename ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_ADD_IVK_ADD_THROWS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThrows:", ?fqn_) AS ?name)
(?ctx AS ?key) (?rty_ AS ?key_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         src:child3|src:child4 ?throws_ .

  ?throws_ a java:Throws ;
           src:child0 ?rty_ .

  ?rty_ a java:ReferenceType ;
        java:name ?ename_ ;
        chg:addition ?ctx .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:inMethodOrConstructor ?meth_ ;
        java:name ?iname_ ;
        java:mayInvokeMethod ?callee_ ;
        chg:addition ?ctxi .


  ?callee_ a java:MethodOrConstructor ;
           src:child3|src:child4 ?throws0_ .

  ?throws0_ a java:Throws ;
           src:child0 ?exc_ .

  ?exc_ a java:ReferenceType ;
        java:name ?ename_ .

}
}
''' % NS_TBL

Q_ADD_THROWS_CHG_THROW_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThrows:", ?sig) AS ?name)
(?ctx AS ?key) (?exc_ AS ?key_)
(?e AS ?ent) (?e_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ ;
         src:child3|src:child4 ?throws_ .

  ?throws_ a java:Throws ;
           src:child0 ?exc_ .

  ?exc_ a java:ReferenceType ;
        java:name ?ename_ ;
        chg:addition ?ctx .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig)

  ?throw a java:ThrowStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child0 ?e ;
         chg:mappedTo ?throw_ .

  ?throw_ a java:ThrowStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child0 ?e_ .

  ?e a java:Expression ;
     chg:relabeled ?e_ .

  ?e_ java:typeName ?ename_ .

}
}
''' % NS_TBL

Q_RM_THROWS_CHG_THROW_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThrows:", ?sig) AS ?name)
(?exc AS ?key) (?ctx_ AS ?key_)
(?e AS ?ent) (?e_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig0 ;
        src:child3|src:child4 ?throws ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?sig0_ .

  ?throws a java:Throws ;
          src:child0 ?exc .

  ?exc a java:ReferenceType ;
       java:name ?ename ;
       chg:removal ?ctx_ .

  BIND (CONCAT(?fqn, ?sig0) AS ?sig)

  ?throw a java:ThrowStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child0 ?e ;
         chg:mappedTo ?throw_ .

  ?throw_ a java:ThrowStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child0 ?e_ .

  ?e a java:Expression ;
     chg:relabeled ?e_ .

  ?e java:typeName ?ename .

}
}
''' % NS_TBL

Q_RM_THROWS_RM_EXC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThrows:", ?sig) AS ?name)
(?exc AS ?key) (?ctxe_ AS ?key_)
(?throws AS ?ent) (?ctxt_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        src:child3|src:child4 ?throws .

  BIND (CONCAT(?mfqn, ?msig) AS ?sig)

  ?throws a java:Throws ;
          chg:removal ?ctxt_ .

  ?exc a java:ReferenceType ;
       src:parent ?throws ;
       java:name ?ename ;
       chg:removal ?ctxe_ .

  FILTER NOT EXISTS {
    ?exc0 a java:ReferenceType ;
          src:parent ?throws .
    FILTER (?exc0 != ?exc)
  }

}
}
''' % NS_TBL

Q_ADD_THROWS_ADD_EXC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThrows:", ?sig) AS ?name)
(?ctxe AS ?key) (?exc_ AS ?key_)
(?ctxt AS ?ent) (?throws_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ ;
         src:child3|src:child4 ?throws_ .

  BIND (CONCAT(?mfqn_, ?msig_) AS ?sig_)

  ?throws_ a java:Throws ;
           chg:addition ?ctxt .

  ?exc_ a java:ReferenceType ;
        src:parent ?throws_ ;
        java:name ?ename_ ;
        chg:addition ?ctxe .

  FILTER NOT EXISTS {
    ?exc0_ a java:ReferenceType ;
           src:parent ?throws_ .
    FILTER (?exc0_ != ?exc_)
  }

}
}
''' % NS_TBL

Q_RM_THROWS_RM_THROW_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThrows:", ?mfqn, ?msig) AS ?name)
(?throw AS ?dep) (?ctxe_ AS ?dep_)
(?exc AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?ename ?exc ?ctx_
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            src:child3|src:child4 ?throws ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?throws a java:Throws ;
              src:child0 ?exc .

      ?exc a java:ReferenceType ;
           java:name ?ename ;
           chg:removal ?ctx_ .

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?ename ?exc ?ctx_
  }

  ?throw a java:ThrowStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child0 ?e ;
         chg:removal ?ctxe_ .

  ?e a java:Expression ;
     java:ofReferenceType ?edecl .

  ?edecl java:fullyQualifiedName ?fqn .

  FILTER (EXISTS {
    ?ty a java:ReferenceType ;
        src:parent [a java:SuperType; java:inTypeDeclaration ?edecl] ;
        java:name ?ename .
  } || EXISTS {
     ?exc java:ofReferenceType ?edecl0 .
     ?edecl java:subTypeOf* ?edecl0 .
  })

}
}
''' % NS_TBL

Q_RM_THROWS_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThrows:", ?mfqn, ?msig) AS ?name)
(?exc AS ?dep) (?ctx_ AS ?dep_)
(?ivk AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?mfqn ?fsig ?meth_ ?exc ?ctx_
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?mfqn ;
            java:name ?mname ;
            java:signature ?msig ;
            src:child3|src:child4 ?throws ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:name ?mname_ ;
             java:signature ?msig_ .

      ?throws a java:Throws ;
              src:child0 ?exc .

      ?exc a java:ReferenceType ;
           java:name ?ename ;
           chg:removal ?ctx_ .

    } GROUP BY ?meth ?mfqn ?fsig ?meth_ ?exc ?ctx_
  }

  ?ivk_ java:mayInvokeMethod ?meth_ ;
        java:name ?iname_ ;
        ^chg:relabeled ?ivk .

}
}
''' % NS_TBL

Q_ADD_THROWS_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThrows:", ?mfqn, ?msig) AS ?name)
(?ivk AS ?dep) (?ivk_ AS ?dep_)
(?ctx AS ?ent) (?exc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?mfqn ?fsig ?meth_ ?exc_ ?ctx
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?mfqn ;
            java:name ?mname ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:name ?mname_ ;
             java:signature ?msig_ ;
             src:child3|src:child4 ?throws_ .

      ?throws_ a java:Throws ;
               src:child0 ?exc_ .

      ?exc_ a java:ReferenceType ;
            java:name ?ename_ ;
            chg:addition ?ctx .

    } GROUP BY ?meth ?mfqn ?fsig ?meth_ ?exc_ ?ctx
  }

  ?ivk java:mayInvokeMethod ?meth ;
       java:name ?iname ;
       chg:relabeled ?ivk_ .

}
}
''' % NS_TBL

Q_ADD_THROWS_ADD_THROW_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThrows:", ?mfqn, ?msig) AS ?name)
(?ctxe AS ?ent) (?throw_ AS ?ent_)
(?ctx AS ?dep) (?exc_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?ename_ ?exc_ ?ctx
    WHERE {

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            chg:mappedTo ?meth_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             src:child3|src:child4 ?throws_ .

      ?throws_ a java:Throws ;
               src:child0 ?exc_ .

      ?exc_ a java:ReferenceType ;
            java:name ?ename_ ;
            chg:addition ?ctx .

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?ename_ ?exc_ ?ctx
  }

  ?throw_ a java:ThrowStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child0 ?e_ ;
          chg:addition ?ctxe .

  ?e_ a java:Expression ;
      java:ofReferenceType ?edecl_ .

  ?edecl_ java:fullyQualifiedName ?fqn_ .

  FILTER (EXISTS {
    ?ty_ a java:ReferenceType ;
         src:parent [a java:SuperType; java:inTypeDeclaration ?edecl_] ;
         java:name ?ename_ .
  } || EXISTS {
     ?exc_ java:ofReferenceType ?edecl0_ .
     ?edecl_ java:subTypeOf* ?edecl0_ .
  })

}
}
''' % NS_TBL

Q_CHG_THROWS_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeThrows:", ?fqn_) AS ?name)
(?rty AS ?key) (?rty_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?rty ?rty_ ?ename ?ename_ ?x_ ?ctx ?ename0_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?fqn ?fqn_ ?rty ?rty_ ?ename ?ename_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?fqn ;
                src:child3|src:child4 ?throws ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?fqn_ ;
                 src:child3|src:child4 ?throws_ .

          ?throws a java:Throws ;
                  src:child0 ?rty ;
                  chg:mappedTo ?throws_ .

          ?throws_ a java:Throws ;
                   src:child0 ?rty_ .

          ?rty a java:ReferenceType ;
               java:name ?ename ;
               chg:relabeled ?rty_ .

          ?rty_ a java:ReferenceType ;
                java:name ?ename_ .

        } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?rty ?rty_ ?ename ?ename_
      }

      {
        ?x_ a java:ThrowStatement ;
            java:inMethodOrConstructor ?meth_ ;
            src:child0/java:typeName ?ename0_ ;
            chg:addition ?ctx .
      }
      UNION
      {
        {
          SELECT DISTINCT ?meth_ ?x_ ?ctx ?ename0_
          WHERE {
            ?x_ a java:InvocationOrInstanceCreation ;
                java:inMethodOrConstructor ?meth_ ;
                java:name ?iname_ ;
                java:mayInvokeMethod ?callee_ ;
                chg:addition ?ctx .

            ?callee_ a java:MethodOrConstructor ;
                     src:child3|src:child4 ?throws0_ .

            ?throws0_ a java:Throws ;
                      src:child0 ?exc_ .

            ?exc_ a java:ReferenceType ;
                  java:name ?ename0_ .
          } GROUP BY ?meth_ ?x_ ?ctx ?ename0_
        }
      }

    } GROUP BY ?meth ?meth_ ?fqn ?fqn_ ?rty ?rty_ ?ename ?ename_ ?x_ ?ctx ?ename0_
  }

  BIND (IRI(STR(?ename_)) AS ?ename_iri_)
  BIND (IRI(STR(?ename0_)) AS ?ename0_iri_)

  FILTER (?ename0_iri_ = ?ename_iri_ || EXISTS {
    ?ename0_iri_ java:subClassNameOf ?ename_iri_
  })

}
}
''' % NS_TBL

Q_ADD_THROWS_ADD_THROWS_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThrows:", ?sig_) AS ?name)
(?ctx0 AS ?key) (?exc0_ AS ?key_)
(?ctx AS ?ent) (?exc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?callee_ ?exc0_ ?ename_ ?ctx0 ?sig_
    WHERE {

      ?callee_ a java:MethodOrConstructor ;
               src:child3|src:child4 ?throws0_ ;
               java:fullyQualifiedName ?fqn_ ;
               java:signature ?msig_ .

      ?throws0_ a java:Throws ;
                src:child0 ?exc0_ .

      ?exc0_ a java:ReferenceType ;
             java:name ?ename_ ;
             chg:addition ?ctx0 .

      BIND (CONCAT(?fqn_, ?msig_) AS ?sig_)


    } GROUP BY ?callee_ ?exc0_ ?ename_ ?ctx0 ?sig_
  }

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:inMethodOrConstructor ?meth_ ;
        java:mayInvokeMethod ?callee_ .

  ?meth_ a java:MethodOrConstructor ;
         src:child3|src:child4 ?throws_ .

  ?throws_ a java:Throws ;
           src:child0 ?exc_ .

  ?exc_ a java:ReferenceType ;
        java:name ?ename_ ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_THROWS_RM_THROWS_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThrows:", ?fqn0) AS ?name)
(?exc0 AS ?key) (?ctx0_ AS ?key_)
(?exc AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?callee ?exc0 ?ename ?ctx0_ ?sig
    WHERE {

      ?callee a java:MethodOrConstructor ;
              src:child3|src:child4 ?throws0 ;
              java:fullyQualifiedName ?fqn ;
              java:signature ?msig .

      ?throws0 a java:Throws ;
               src:child0 ?exc0 .

      ?exc0 a java:ReferenceType ;
            java:name ?ename ;
            chg:removal ?ctx0_ .

      BIND (CONCAT(?fqn, ?msig) AS ?sig)


    } GROUP BY ?callee ?exc0 ?ename ?ctx0_ ?sig
  }

  ?ivk a java:InvocationOrInstanceCreation ;
       java:inMethodOrConstructor ?meth ;
       java:mayInvokeMethod ?callee .

  ?meth a java:MethodOrConstructor ;
        src:child3|src:child4 ?throws .

  ?throws a java:Throws ;
          src:child0 ?exc .

  ?exc a java:ReferenceType ;
       java:name ?ename ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_THROWS_ADD_THROWS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThrows:", ?fqn0_) AS ?name)
(?ctx0 AS ?key) (?exc0_ AS ?key_)
(?ctx AS ?ent) (?exc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth0_ ?class0_ ?fqn0_ ?sig_ ?mname_ ?exc0_ ?ctx0 ?ename_
    WHERE {

      ?meth0_ a java:MethodOrConstructor ;
              java:inTypeDeclaration ?class0_ ;
              java:fullyQualifiedName ?fqn0_ ;
              java:name ?mname_ ;
              java:signature ?sig_ ;
              src:child3|src:child4 ?throws0_ .

      ?throws0_ a java:Throws ;
                src:child0 ?exc0_ .

      ?exc0_ a java:ReferenceType ;
             java:name ?ename_ ;
             chg:addition ?ctx0 .

    } GROUP BY ?meth0_ ?class0_ ?fqn0_ ?sig_ ?mname_ ?exc0_ ?ctx0 ?ename_
  }

  ?class_ java:subTypeOf+ ?class0_ .

  ?meth_ a java:MethodOrConstructor ;
          java:inTypeDeclaration ?class_ ;
          java:fullyQualifiedName ?fqn_ ;
          java:signature ?sig ;
          java:name ?mname_ ;
          src:child3|src:child4 ?throws_ .

  ?throws_ a java:Throws ;
            src:child0 ?exc_ .

  ?exc_ a java:ReferenceType ;
        java:name ?ename_ ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_THROWS_RM_THROWS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThrows:", ?fqn0) AS ?name)
(?exc0 AS ?key) (?ctx0_ AS ?key_)
(?exc AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth0 ?class0 ?fqn0 ?sig ?mname ?exc0 ?ctx0_ ?ename
    WHERE {

      ?meth0 a java:MethodOrConstructor ;
             java:inTypeDeclaration ?class0 ;
             java:fullyQualifiedName ?fqn0 ;
             java:name ?mname ;
             java:signature ?sig ;
             src:child3|src:child4 ?throws0 .

      ?throws0 a java:Throws ;
               src:child0 ?exc0 .

      ?exc0 a java:ReferenceType ;
            java:name ?ename ;
            chg:removal ?ctx0_ .

    } GROUP BY ?meth0 ?class0 ?fqn0 ?sig ?mname ?exc0 ?ctx0_ ?ename
  }

  ?class java:subTypeOf+ ?class0 .

  ?meth a java:MethodOrConstructor ;
        java:inTypeDeclaration ?class ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?sig ;
        java:name ?mname ;
        src:child3|src:child4 ?throws .

  ?throws a java:Throws ;
          src:child0 ?exc .

  ?exc a java:ReferenceType ;
       java:name ?ename ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_OVERRIDE_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddOverride:", ?mfqn_, ?msig_) AS ?name)
(?rty AS ?dep) (?rty_ AS ?dep_)
(?ctx AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?a_ ?ctx ?mname_ ?mfqn_ ?msig_ ?tdecl_
    WHERE {

      ?a_ a java:MarkerAnnotation ;
          src:parent/src:parent ?meth_ ;
          java:name "Override" ;
          chg:addition ?ctx .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:name ?mname_ ;
             java:signature ?msig_ .

    } GROUP BY ?a_ ?ctx ?mname_ ?mfqn_ ?msig_ ?tdecl_
  }

  ?tdecl_ java:subTypeOf+ ?tdecl0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          java:name ?mname_ ;
          java:signature ?msig_ ;
          src:child2 ?rty_ .

  ?rty_ a java:Type ;
        ^chg:relabeled ?rty .

}
}
''' % NS_TBL

Q_ADD_OVERRIDE_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddOverride:", ?mfqn_, ?msig_) AS ?name)
(?meth0 AS ?dep) (?meth0_ AS ?dep_)
(?ctx AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?a_ ?ctx ?mname_ ?mfqn_ ?msig_ ?tdecl_
    WHERE {

      ?a_ a java:MarkerAnnotation ;
          src:parent/src:parent ?meth_ ;
          java:name "Override" ;
          chg:addition ?ctx .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:name ?mname_ ;
             java:signature ?msig_ .

    } GROUP BY ?a_ ?ctx ?mname_ ?mfqn_ ?msig_ ?tdecl_
  }

  ?tdecl_ java:subTypeOf+ ?tdecl0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          java:name ?mname_ ;
          java:signature ?msig_ ;
          ^chg:relabeled ?meth0 .

}
}
''' % NS_TBL

Q_ADD_OVERRIDE_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddOverride:", ?mfqn_, ?msig_) AS ?name)
(?ctx0 AS ?dep) (?meth0_ AS ?dep_)
(?ctx AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?a_ ?ctx ?mname_ ?mfqn_ ?msig_ ?tdecl_
    WHERE {

      ?a_ a java:MarkerAnnotation ;
          src:parent/src:parent ?meth_ ;
          java:name "Override" ;
          chg:addition ?ctx .

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:name ?mname_ ;
             java:signature ?msig_ .

    } GROUP BY ?a_ ?ctx ?mname_ ?mfqn_ ?msig_ ?tdecl_
  }

  ?tdecl_ java:subTypeOf+ ?tdecl0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl0_ ;
          java:name ?mname_ ;
          java:signature ?msig_ ;
          chg:addition ?ctx0 .

}
}
''' % NS_TBL

Q_RM_OVERRIDE_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveOverride:", ?mfqn, ?msig) AS ?name)
(?a AS ?dep) (?ctx_ AS ?dep_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?a ?ctx_ ?mname ?mfqn ?msig ?tdecl
    WHERE {

      ?a a java:MarkerAnnotation ;
         src:parent/src:parent ?meth ;
         java:name "Override" ;
         chg:removal ?ctx_ .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?mfqn ;
            java:name ?mname ;
            java:signature ?msig .

    } GROUP BY ?a ?ctx_ ?mname ?mfqn ?msig ?tdecl
  }

  ?tdecl java:subTypeOf+ ?tdecl0 .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         java:name ?mname ;
         java:signature ?msig ;
         src:child2 ?rty .

  ?rty a java:Type ;
       chg:relabeled ?rty_ .

}
}
''' % NS_TBL

Q_RM_OVERRIDE_CHG_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveOverride:", ?mfqn, ?msig) AS ?name)
(?a AS ?dep) (?ctx_ AS ?dep_)
(?meth0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?a ?ctx_ ?mname ?mfqn ?msig ?tdecl
    WHERE {

      ?a a java:MarkerAnnotation ;
         src:parent/src:parent ?meth ;
         java:name "Override" ;
         chg:removal ?ctx_ .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?mfqn ;
            java:name ?mname ;
            java:signature ?msig .

    } GROUP BY ?a ?ctx_ ?mname ?mfqn ?msig ?tdecl
  }

  ?tdecl java:subTypeOf+ ?tdecl0 .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         java:name ?mname ;
         java:signature ?msig ;
         chg:relabeled ?meth0_ .

}
}
''' % NS_TBL

Q_RM_OVERRIDE_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveOverride:", ?mfqn, ?msig) AS ?name)
(?a AS ?dep) (?ctx_ AS ?dep_)
(?meth0 AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?a ?ctx_ ?mname ?mfqn ?msig ?tdecl
    WHERE {

      ?a a java:MarkerAnnotation ;
         src:parent/src:parent ?meth ;
         java:name "Override" ;
         chg:removal ?ctx_ .

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?mfqn ;
            java:name ?mname ;
            java:signature ?msig .

    } GROUP BY ?a ?ctx_ ?mname ?mfqn ?msig ?tdecl
  }

  ?tdecl java:subTypeOf+ ?tdecl0 .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl0 ;
         java:name ?mname ;
         java:signature ?msig ;
         chg:removal ?ctx0_ .

}
}
''' % NS_TBL

Q_RM_ASSIGN_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAssign:", ?vname) AS ?name)
(?a AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?vdtor_ ?vname ?vname_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             src:parent ?vdecl ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?vdecl_ ;
              java:name ?vname_ .

      ?vdecl a ?cat OPTION (INFERENCE NONE) ;
             chg:mappedTo ?vdecl_ .

      ?final a java:Final ;
             src:parent/src:parent ?vdecl ;
             chg:mappedTo ?final_ .

      ?final_ a java:Final ;
              src:parent/src:parent ?vdecl_ .

    } GROUP BY ?vdtor ?vdtor_ ?vname ?vname_
  }

  ?a a java:AssignmentOp ;
     src:child0 ?lhs ;
     chg:removal ?ctx_ .

  ?lhs java:declaredBy ?vdtor .

  ?a_ a java:AssignmentOp ;
      src:child0 ?lhs_ ;
      chg:addition ?ctx .

  ?lhs_ java:declaredBy ?vdtor_ .

  {
    ?a java:inMethodOrConstructor ?meth .
    ?meth chg:mappedTo ?meth_ .
    ?a_ java:inMethodOrConstructor ?meth_ .
  }
  UNION
  {
    ?a java:inField ?field .
    ?field chg:mappedTo ?field_ .
    ?a_ java:inField ?field_ .
  }

}
}
''' % NS_TBL

Q_RM_METH_RM_RET_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?fqn, ".", ?msig) AS ?name)
(?ret AS ?dep) (?ctxr_ AS ?dep_)
(?meth AS ?ent) (?ctxm_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ret a java:ReturnStatement ;
       java:inMethodOrConstructor ?meth ;
       chg:removal ?ctxr_ .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?msig ;
        chg:removal ?ctxm_ .

  ?x java:inMethodOrConstructor ?meth ;
     chg:mappedTo ?x_ .

  FILTER (EXISTS {
    ?x_ java:inStaticInitializer [] .
  } || EXISTS {
    ?x_ java:inInstanceInitializer [] .
  })

}
}
''' % NS_TBL

Q_ADD_METH_ADD_RET_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?fqn_, ".", ?msig_) AS ?name)
(?ctxm AS ?dep) (?meth_ AS ?dep_)
(?ctxr AS ?ent) (?ret_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ret_ a java:ReturnStatement ;
        java:inMethodOrConstructor ?meth_ ;
        chg:addition ?ctxr .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?msig_ ;
         chg:addition ?ctxm .

  ?x_ java:inMethodOrConstructor ?meth_ ;
      ^chg:mappedTo ?x .

  FILTER (EXISTS {
    ?x java:inStaticInitializer [] .
  } || EXISTS {
    ?x java:inInstanceInitializer [] .
  })

}
}
''' % NS_TBL

Q_CHG_SUPER_ADD_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperClass:", ?cfqn) AS ?name)
(?rty AS ?key) (?rty_ AS ?key_)
(?ctxa AS ?ent) (?arg_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
    WHERE {

      {
        SELECT DISTINCT ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_
        WHERE {

          ?rty a java:ReferenceType ;
               java:name ?cfqn0 ;
               src:parent ?super ;
               chg:relabeled ?rty_ .

          ?rty_ a java:ReferenceType ;
                java:name ?cfqn0_ ;
                src:parent ?super_ .

          ?super a java:SuperType ;
                 src:parent/src:parent ?tdecl .

          ?super_ a java:SuperType ;
                  src:parent/src:parent ?tdecl_ .

        } GROUP BY ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_
      }

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
  }

  {
    SELECT DISTINCT ?ivk ?ivk_ ?tdecl ?tdecl_ ?meth ?meth_ ?fqn ?fqn_ ?sig0 ?sig0_
    WHERE {

      ?ivk a java:SuperInvocation ;
           java:inTypeDeclaration ?tdecl ;
           java:mayInvokeMethod ?meth ;
           chg:mappedTo ?ivk_ .

      ?ivk_ a java:SuperInvocation ;
            java:inTypeDeclaration ?tdecl_ ;
            java:mayInvokeMethod ?meth_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

    } GROUP BY ?ivk ?ivk_ ?tdecl ?tdecl_ ?meth ?meth_ ?fqn ?fqn_ ?sig0 ?sig0_
  }

  ?arg_ a java:Expression ;
        src:parent ?args_ ;
        chg:addition ?ctxa .

  ?args_ a java:Arguments ;
         src:parent ?ivk_ .

  FILTER EXISTS {
    ?meth a java:MethodOrConstructor ;
          java:inTypeDeclaration ?tdecl0 .

    ?meth_ a java:MethodOrConstructor ;
           java:inTypeDeclaration ?tdecl0_ .

    ?tdecl java:subTypeOf+ ?tdecl0 .
    ?tdecl_ java:subTypeOf+ ?tdecl0_ .
  }

}
}
''' % NS_TBL

Q_CHG_SUPER_RM_ARG_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeSuperClass:", ?cfqn) AS ?name)
(?rty AS ?key) (?rty_ AS ?key_)
(?arg AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
    WHERE {

      {
        SELECT DISTINCT ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_
        WHERE {

          ?rty a java:ReferenceType ;
               java:name ?cfqn0 ;
               src:parent ?super ;
               chg:relabeled ?rty_ .

          ?rty_ a java:ReferenceType ;
                java:name ?cfqn0_ ;
                src:parent ?super_ .

          ?super a java:SuperType ;
                 src:parent/src:parent ?tdecl .

          ?super_ a java:SuperType ;
                  src:parent/src:parent ?tdecl_ .

        } GROUP BY ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_
      }

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?rty ?rty_ ?cfqn0 ?cfqn0_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
  }

  {
    SELECT DISTINCT ?ivk ?ivk_ ?tdecl ?tdecl_ ?meth ?meth_ ?fqn ?fqn_ ?sig0 ?sig0_
    WHERE {

      ?ivk a java:SuperInvocation ;
           java:inTypeDeclaration ?tdecl ;
           java:mayInvokeMethod ?meth ;
           chg:mappedTo ?ivk_ .

      ?ivk_ a java:SuperInvocation ;
            java:inTypeDeclaration ?tdecl_ ;
            java:mayInvokeMethod ?meth_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

    } GROUP BY ?ivk ?ivk_ ?tdecl ?tdecl_ ?meth ?meth_ ?fqn ?fqn_ ?sig0 ?sig0_
  }

  ?arg a java:Expression ;
       src:parent ?args ;
       chg:removal ?ctxa_ .

  ?args a java:Arguments ;
        src:parent ?ivk .

  FILTER EXISTS {
    ?meth a java:MethodOrConstructor ;
          java:inTypeDeclaration ?tdecl0 .

    ?meth_ a java:MethodOrConstructor ;
           java:inTypeDeclaration ?tdecl0_ .

    ?tdecl java:subTypeOf+ ?tdecl0 .
    ?tdecl_ java:subTypeOf+ ?tdecl0_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_ADD_CAST_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?fqn_, ".", ?msig_) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?ctx AS ?ent) (?cast_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?cast_ a java:Cast ;
         src:child0/java:name ?tyname_ ;
         src:child1 ?ivk_ ;
         chg:addition ?ctx .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        java:mayInvokeMethod ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?fqn_ ;
         java:signature ?msig_ ;
         src:child2 ?retty_ .

  ?retty_ a java:Type ;
          ^chg:relabeled ?retty .

  FILTER NOT EXISTS {
    ?retty_ java:name ?tyname_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?ctx AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver_ ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ .
      ?class_ ver:version ?ver_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ver_ ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr ;
       chg:mappedTo ?ret_ .

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr a java:Expression ;
        chg:mappedTo ?expr_ .

  ?expr_ a java:Expression ;
         java:ofReferenceType ?ety_ .

  ?ety_ a java:TypeDeclaration ;
        ver:version ?ver_ .

  ?sty_ a java:SuperType ;
        src:parent/src:parent ?ety_ .

  ?rty_ a java:ReferenceType ;
        src:parent ?sty_ ;
        java:name ?rtyname_ ;
        chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?expr java:ofReferenceType ?ety .
    ?ety chg:mappedStablyTo ?ety_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_SUPERTY_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver_ ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ .
      ?class_ ver:version ?ver_ .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ver_ ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr ;
       chg:mappedTo ?ret_ .

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr a java:Expression ;
        chg:mappedTo ?expr_ .

  ?expr_ a java:Expression ;
         java:ofReferenceType ?ety_ .

  ?ety_ a java:TypeDeclaration ;
        ver:version ?ver_ .

  ?sty_ a java:SuperType ;
        src:parent/src:parent ?ety_ .

  ?rty_ a java:ReferenceType ;
        src:parent ?sty_ ;
        java:name ?rtyname_ ;
        ^chg:relabeled ?rty .

  FILTER NOT EXISTS {
    ?expr java:ofReferenceType ?ety .
    ?ety chg:mappedStablyTo ?ety_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?rty AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ ;
             ver:version ?ver .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ver ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr ;
       chg:mappedTo ?ret_ .

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr a java:Expression ;
        java:ofReferenceType ?ety ;
        chg:mappedTo ?expr_ .

  ?ety a java:TypeDeclaration ;
       ver:version ?ver .

  ?sty a java:SuperType ;
       src:parent/src:parent ?ety .

  ?rty a java:ReferenceType ;
       src:parent ?sty ;
       java:name ?rtyname ;
       chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?expr_ java:ofReferenceType ?ety_ .
    ?ety chg:mappedStablyTo ?ety_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_SUPERTY_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?sig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ver ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child2 ?retty ;
            java:returnTypeName ?rtyname ;
            java:inTypeDeclaration ?class ;
            java:name ?mname ;
            java:fullyQualifiedName ?fqn ;
            java:signature ?sig0 ;
            chg:mappedTo ?meth_ .

      ?retty chg:relabeled ?retty_ .

      ?meth_ a java:MethodDeclaration ;
             src:child2 ?retty_ ;
             java:returnTypeName ?rtyname_ ;
             java:inTypeDeclaration ?class_ ;
             java:name ?mname_ ;
             java:fullyQualifiedName ?fqn_ ;
             java:signature ?sig0_ .

      ?class chg:mappedTo ?class_ ;
             ver:version ?ver .

      BIND (CONCAT(?fqn, ?sig0) AS ?sig) .
      BIND (CONCAT(?fqn_, ?sig0_) AS ?sig_) .

    } GROUP BY ?ver ?meth ?meth_ ?retty ?retty_ ?sig ?sig_ ?rtyname ?rtyname_
  }

  ?ret a java:ReturnStatement ;
       java:inMethod ?meth ;
       src:child0 ?expr ;
       chg:mappedTo ?ret_ .

  ?ret_ a java:ReturnStatement ;
        java:inMethod ?meth_ ;
        src:child0 ?expr_ .

  ?expr a java:Expression ;
        java:ofReferenceType ?ety ;
        chg:mappedTo ?expr_ .

  ?ety a java:TypeDeclaration ;
       ver:version ?ver .

  ?sty a java:SuperType ;
       src:parent/src:parent ?ety .

  ?rty a java:ReferenceType ;
       src:parent ?sty ;
       java:name ?rtyname ;
       chg:relabeled ?rty_ .

  FILTER NOT EXISTS {
    ?expr_ java:ofReferenceType ?ety_ .
    ?ety chg:mappedStablyTo ?ety_ .
  }

}
}
''' % NS_TBL

Q_CHG_RETTY_ADD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?mfqn_, ?msig_) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x_ a java:Entity ;
      a ?cat_ OPTION (INFERENCE NONE) ;
      chg:addition ?ctx .

  ?ivk_ a java:InvocationOrInstanceCreation ;
        src:parent ?x_ ;
        java:mayInvokeMethod ?meth_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ ;
         src:child2 ?retty_ .

  ?retty_ a java:Type ;
          ^chg:relabeled ?retty .

}
}
''' % NS_TBL

Q_CHG_RETTY_RM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?mfqn, ?msig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?x AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:Entity ;
     a ?cat OPTION (INFERENCE NONE) ;
     chg:removal ?ctx_ .

  ?ivk a java:InvocationOrInstanceCreation ;
       src:parent ?x ;
       java:mayInvokeMethod ?meth .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        src:child2 ?retty .

  ?retty a java:Type ;
         chg:relabeled ?retty_ .

}
}
''' % NS_TBL

Q_CHG_RETTY_RM_CAST_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?fqn, ".", ?msig) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?cast AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?cast a java:Cast ;
        src:child0/java:name ?tyname ;
        src:child1 ?ivk ;
        chg:removal ?ctx_ .

  ?ivk a java:InvocationOrInstanceCreation ;
       java:mayInvokeMethod ?meth .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?fqn ;
        java:signature ?msig ;
        src:child2 ?retty .

  ?retty a java:Type ;
         chg:relabeled ?retty_ .

  FILTER NOT EXISTS {
    ?retty java:name ?tyname .
  }

}
}
''' % NS_TBL

Q_RM_LV_FINAL_RM_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?mfqn, ?msig, ":", ?vname) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?final AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final ?ctx_ ?meth ?meth_ ?vname ?vname_
    WHERE {

      ?final a java:Final ;
             src:parent ?mods ;
             chg:removal ?ctx_ .

      {
        ?def a java:Parameter ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             src:child0 ?mods ;
             chg:mappedTo ?param_ .

        ?def_ a java:Parameter ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ .
      }
      UNION
      {
        ?vdecl a java:LocalVariableDeclarationStatement ;
               java:inMethodOrConstructor ?meth ;
               src:child ?mods ;
               chg:mappedTo ?vdecl_ .

        ?vdecl_ a java:LocalVariableDeclarationStatement ;
                java:inMethodOrConstructor ?meth_ .

        ?def a java:VariableDeclarator ;
             src:parent ?vdecl ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

        ?def_ a java:VariableDeclarator ;
              src:parent ?vdecl_ ;
              java:name ?vname_ .
      }

      ?meth a java:MethodOrConstructor ;
            chg:mappedTo ?meth_ .

    } GROUP BY ?final ?ctx_ ?meth ?meth_ ?vname ?vname_ ?def ?def_
  }

  ?x a java:Name ;
     java:declaredBy ?def ;
     java:inMethodOrConstructor ?meth0 ;
     java:name ?vname ;
     chg:removal ?ctxx_ .

  ?meth0 a java:MethodOrConstructor ;
         java:inInstanceCreation/java:inMethodOrConstructor ?meth .

  ?meth java:fullyQualifiedName ?mfqn ;
        java:signature ?msig .

}
}
''' % NS_TBL

Q_RM_LV_FINAL_CHG_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?mfqn, ?msig, ":", ?vname) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?final AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final ?ctx_ ?meth ?meth_ ?vname ?vname_
    WHERE {

      ?final a java:Final ;
             src:parent ?mods ;
             chg:removal ?ctx_ .

      {
        ?def a java:Parameter ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             src:child0 ?mods ;
             chg:mappedTo ?param_ .

        ?def_ a java:Parameter ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ .
      }
      UNION
      {
        ?vdecl a java:LocalVariableDeclarationStatement ;
               java:inMethodOrConstructor ?meth ;
               src:child ?mods ;
               chg:mappedTo ?vdecl_ .

        ?vdecl_ a java:LocalVariableDeclarationStatement ;
                java:inMethodOrConstructor ?meth_ .

        ?def a java:VariableDeclarator ;
             src:parent ?vdecl ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

        ?def_ a java:VariableDeclarator ;
              src:parent ?vdecl_ ;
              java:name ?vname_ .
      }

      ?meth a java:MethodOrConstructor ;
            chg:mappedTo ?meth_ .

    } GROUP BY ?final ?ctx_ ?meth ?meth_ ?vname ?vname_ ?def ?def_
  }

  ?x a java:Name ;
     java:declaredBy ?def ;
     java:inMethodOrConstructor ?meth0 ;
     java:name ?vname ;
     chg:relabeled ?x_ .

  ?meth0 a java:MethodOrConstructor ;
         java:inInstanceCreation/java:inMethodOrConstructor ?meth .

  ?meth java:fullyQualifiedName ?mfqn ;
        java:signature ?msig .

}
}
''' % NS_TBL

Q_ADD_LV_FINAL_ADD_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?mfqn_, ".", ?msig_, ":", ?vname_) AS ?name)
(?ctx AS ?dep) (?final_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final_ ?ctx ?meth ?meth_ ?vname ?vname_
    WHERE {

      ?final_ a java:Final ;
              src:parent ?mods_ ;
              chg:addition ?ctx .

      {
        ?def a java:Parameter ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             chg:mappedTo ?param_ .

        ?def_ a java:Parameter ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ ;
              src:child0 ?mods_ .
      }
      UNION
      {
        ?vdecl a java:LocalVariableDeclarationStatement ;
               java:inMethodOrConstructor ?meth ;
               chg:mappedTo ?vdecl_ .

        ?vdecl_ a java:LocalVariableDeclarationStatement ;
                java:inMethodOrConstructor ?meth_ ;
                src:child ?mods_ .

        ?def a java:VariableDeclarator ;
             src:parent ?vdecl ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

        ?def_ a java:VariableDeclarator ;
              src:parent ?vdecl_ ;
              java:name ?vname_ .
      }

      ?meth a java:MethodOrConstructor ;
            chg:mappedTo ?meth_ .

    } GROUP BY ?final_ ?ctx ?meth ?meth_ ?vname ?vname_ ?def ?def_
  }

  ?x_ a java:Name ;
      java:declaredBy ?def_ ;
      java:inMethodOrConstructor ?meth0_ ;
      java:name ?vname_ ;
      chg:addition ?ctxx .

  ?meth0_ a java:MethodOrConstructor ;
          java:inInstanceCreation/java:inMethodOrConstructor ?meth_ .

  ?meth_ java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ .

}
}
''' % NS_TBL

Q_ADD_LV_FINAL_CHG_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?mfqn_, ".", ?msig_, ":", ?vname_) AS ?name)
(?ctx AS ?dep) (?final_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final_ ?ctx ?meth ?meth_ ?vname ?vname_
    WHERE {

      ?final_ a java:Final ;
              src:parent ?mods_ ;
              chg:addition ?ctx .

      {
        ?def a java:Parameter ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             chg:mappedTo ?param_ .

        ?def_ a java:Parameter ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ ;
              src:child0 ?mods_ .
      }
      UNION
      {
        ?vdecl a java:LocalVariableDeclarationStatement ;
               java:inMethodOrConstructor ?meth ;
               chg:mappedTo ?vdecl_ .

        ?vdecl_ a java:LocalVariableDeclarationStatement ;
                java:inMethodOrConstructor ?meth_ ;
                src:child ?mods_ .

        ?def a java:VariableDeclarator ;
             src:parent ?vdecl ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

        ?def_ a java:VariableDeclarator ;
              src:parent ?vdecl_ ;
              java:name ?vname_ .
      }

      ?meth a java:MethodOrConstructor ;
            chg:mappedTo ?meth_ .

    } GROUP BY ?final_ ?ctx ?meth ?meth_ ?vname ?vname_ ?def ?def_
  }

  ?x_ a java:Name ;
      java:declaredBy ?def_ ;
      java:inMethodOrConstructor ?meth0_ ;
      java:name ?vname_ ;
      ^chg:relabeled ?x .

  ?meth0_ a java:MethodOrConstructor ;
          java:inInstanceCreation/java:inMethodOrConstructor ?meth_ .

  ?meth_ java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ .

}
}
''' % NS_TBL

Q_CHG_IVK_RM_VDTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeInvocation:", ?cfqn, ":", ?iname) AS ?name)
(?ivk AS ?dep) (?x_ AS ?dep_)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk a ?cat OPTION (INFERENCE NONE) ;
       java:name ?iname ;
       java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
       src:child0 ?e ;
       chg:relabeled ?x_ .

  FILTER (?cat IN (java:PrimaryMethodInvocation,
                   java:PrimaryMethodInvocationStatement,
                   java:FieldAccess))

  ?e a ?cate OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor .

  FILTER (?cate IN (java:FieldAccess,java:Name))

  ?vdtor chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?e java:ofReferenceType [] .
    FILTER NOT EXISTS {
      ?e java:typeDims [] .
    }
  }

}
}
''' % NS_TBL

Q_CHG_IVK_CHG_VDTOR_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeInvocation:", ?cfqn, ":", ?iname) AS ?name)
(?ivk AS ?dep) (?x_ AS ?dep_)
(?vdtor AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk a ?cat OPTION (INFERENCE NONE) ;
       java:name ?iname ;
       java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
       src:child0 ?e ;
       chg:relabeled ?x_ .

  FILTER (?cat IN (java:PrimaryMethodInvocation,
                   java:PrimaryMethodInvocationStatement,
                   java:FieldAccess))

  ?e a ?cate OPTION (INFERENCE NONE) ;
     java:declaredBy ?vdtor .

  FILTER (?cate IN (java:FieldAccess,java:Name))

  ?vdtor chg:relabeled ?vdtor_ .

  FILTER NOT EXISTS {
    ?e java:ofReferenceType [] .
    FILTER NOT EXISTS {
      ?e java:typeDims [] .
    }
  }

}
}
''' % NS_TBL

Q_CHG_IVK_ADD_VDTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeInvocation:", ?cfqn_, ":", ?iname_) AS ?name)
(?ctx AS ?dep) (?vdtor_ AS ?dep_)
(?x AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk_ a ?cat_ OPTION (INFERENCE NONE) ;
        java:name ?iname_ ;
        java:inTypeDeclaration/java:fullyQualifiedName ?cfqn_ ;
        src:child0 ?e_ ;
        ^chg:relabeled ?x .

  FILTER (?cat_ IN (java:PrimaryMethodInvocation,
                    java:PrimaryMethodInvocationStatement,
                    java:FieldAccess))

  ?e_ a ?cate_ OPTION (INFERENCE NONE) ;
      java:declaredBy ?vdtor_ .

  FILTER (?cate_ IN (java:FieldAccess,java:Name))

  ?vdtor_ chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?e_ java:ofReferenceType [] .
    FILTER NOT EXISTS {
      ?e_ java:typeDims [] .
    }
  }

}
}
''' % NS_TBL

Q_CHG_IVK_CHG_VDTOR_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeInvocation:", ?cfqn_, ":", ?iname_) AS ?name)
(?vdtor AS ?dep) (?vdtor_ AS ?dep_)
(?x AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk_ a ?cat_ OPTION (INFERENCE NONE) ;
        java:name ?iname_ ;
        java:inTypeDeclaration/java:fullyQualifiedName ?cfqn_ ;
        src:child0 ?e_ ;
        ^chg:relabeled ?x .

  FILTER (?cat_ IN (java:PrimaryMethodInvocation,
                    java:PrimaryMethodInvocationStatement,
                    java:FieldAccess))

  ?e_ a ?cate_ OPTION (INFERENCE NONE) ;
      java:declaredBy ?vdtor_ .

  FILTER (?cate_ IN (java:FieldAccess,java:Name))

  ?vdtor chg:relabeled ?vdtor_ .

  FILTER NOT EXISTS {
    ?e_ java:ofReferenceType [] .
    FILTER NOT EXISTS {
      ?e_ java:typeDims [] .
    }
  }

}
}
''' % NS_TBL

Q_CHG_IVK_CHG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeInvocation:", ?cfqn, ":", ?iname) AS ?name)
(?x AS ?key) (?x_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?x_ ?iname ?cfqn ?tyname ?tyname_ ?vdtor ?vdtor_
    WHERE {

      {
        SELECT DISTINCT ?x ?x_ ?iname ?cfqn ?e ?e_
        WHERE {

          ?x a ?cat OPTION (INFERENCE NONE) ;
             java:name ?iname ;
             java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
             src:child0 ?e ;
             chg:relabeled ?x_ .

          ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
              src:child0 ?e_ .

          FILTER (?cat IN (java:PrimaryMethodInvocation,
                           java:PrimaryMethodInvocationStatement,
                           java:FieldAccess))

          FILTER (?cat_ IN (java:PrimaryMethodInvocation,
                            java:PrimaryMethodInvocationStatement,
                            java:FieldAccess))

        } GROUP BY ?x ?x_ ?iname ?cfqn ?e ?e_
      }

      ?e a ?cate OPTION (INFERENCE NONE) ;
         java:typeName ?tyname ;
         java:declaredBy ?vdtor ;
         chg:mappedTo ?e_ .

      ?e_ a ?cate_ OPTION (INFERENCE NONE) ;
          java:typeName ?tyname_ ;
          java:declaredBy ?vdtor_ ;
          src:parent ?x_ .

      FILTER (?cate IN (java:FieldAccess,java:Name))
      FILTER (?cate_ IN (java:FieldAccess,java:Name))

    } GROUP BY ?x ?x_ ?iname ?cfqn ?tyname ?tyname_ ?vdtor ?vdtor_
  }

  {
    ?vdtor a java:Parameter ;
           src:child1 ?ty .
  }
  UNION
  {
    ?vdtor a java:VariableDeclarator ;
           src:parent/src:child1 ?ty .
  }
  UNION
  {
    ?vdtor_ a java:Parameter ;
            src:child1 ?ty_ .
  }
  UNION
  {
    ?vdtor_ a java:VariableDeclarator ;
            src:parent/src:child1 ?ty_ .
  }

  ?ty a java:ReferenceType ;
      chg:relabeled ?ty_ .

}
}
''' % NS_TBL

Q_RM_IVK_CHG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveInvocation:", ?cfqn, ":", ?iname) AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?ctx_ ?iname ?cfqn ?tyname ?vdtor
    WHERE {

      {
        SELECT DISTINCT ?x ?ctx_ ?iname ?cfqn ?e
        WHERE {

          ?x a ?cat OPTION (INFERENCE NONE) ;
             java:name ?iname ;
             java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
             src:child0 ?e ;
             chg:removal ?ctx_ .

          FILTER (?cat IN (java:PrimaryMethodInvocation,
                           java:PrimaryMethodInvocationStatement,
                           java:FieldAccess))

        } GROUP BY ?x ?ctx_ ?iname ?cfqn ?e
      }

      ?e a ?cate OPTION (INFERENCE NONE) ;
         java:typeName ?tyname ;
         java:declaredBy ?vdtor .

      FILTER (?cate IN (java:FieldAccess,java:Name))

    } GROUP BY ?x ?ctx_ ?iname ?cfqn ?tyname ?vdtor
  }

  {
    ?vdtor a java:Parameter ;
           src:child1 ?ty .
  }
  UNION
  {
    ?vdtor a java:VariableDeclarator ;
           src:parent/src:child1 ?ty .
  }

  ?ty a java:ReferenceType ;
      chg:relabeled ?ty_ .

}
}
''' % NS_TBL

Q_RM_IVK_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveInvocation:", ?cfqn, ":", ?iname) AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?ty0 AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?x ?ctx_ ?iname ?cfqn ?tyname ?vdtor
    WHERE {

      {
        SELECT DISTINCT ?x ?ctx_ ?iname ?cfqn ?e
        WHERE {

          ?x a ?cat OPTION (INFERENCE NONE) ;
             java:name ?iname ;
             java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
             src:child0 ?e ;
             chg:removal ?ctx_ .

          FILTER (?cat IN (java:PrimaryMethodInvocation,
                           java:PrimaryMethodInvocationStatement,
                           java:FieldAccess))

        } GROUP BY ?x ?ctx_ ?iname ?cfqn ?e
      }

      ?e a ?cate OPTION (INFERENCE NONE) ;
         java:typeName ?tyname ;
         java:declaredBy ?vdtor .

      FILTER (?cate IN (java:FieldAccess,java:Name))

    } GROUP BY ?x ?ctx_ ?iname ?cfqn ?tyname ?vdtor
  }

  {
    ?vdtor a java:Parameter ;
           src:child1 ?ty .
  }
  UNION
  {
    ?vdtor a java:VariableDeclarator ;
           src:parent/src:child1 ?ty .
  }

  ?ty a java:ReferenceType ;
      java:refersToDeclaration ?class .

  {
    SELECT DISTINCT ?class ?class_ ?ctx0_ ?ty0 ?fqn0
    WHERE {
    ?class a java:TypeDeclaration ;
           chg:mappedTo ?class_ .

    ?class_ a java:TypeDeclaration .

    ?super a java:SuperType ;
            java:inTypeDeclaration ?class .

    ?ty0 a java:ReferenceType ;
         java:name ?fqn0 ;
         src:parent ?super ;
         chg:removal ?ctx0_ .

    } GROUP BY ?class ?class_ ?ctx0_ ?ty0 ?fqn0
  }

  FILTER NOT EXISTS {
    ?ty0 java:refersToDeclaration [] .
  }

}
}
''' % NS_TBL

Q_ADD_IVK_CHG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddInvocation:", ?cfqn_, ":", ?iname_) AS ?name)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?x_ ?iname_ ?cfqn_ ?tyname_ ?vdtor_
    WHERE {

      {
        SELECT DISTINCT ?ctx ?x_ ?iname_ ?cfqn_ ?e_
        WHERE {

          ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
              java:name ?iname_ ;
              java:inTypeDeclaration/java:fullyQualifiedName ?cfqn_ ;
              src:child0 ?e_ ;
              chg:addition ?ctx .

          FILTER (?cat_ IN (java:PrimaryMethodInvocation,
                            java:PrimaryMethodInvocationStatement,
                            java:FieldAccess))

        } GROUP BY ?ctx ?x_ ?iname_ ?cfqn_ ?e_
      }

      ?e_ a ?cate_ OPTION (INFERENCE NONE) ;
          java:typeName ?tyname_ ;
          java:declaredBy ?vdtor_ ;
          src:parent ?x_ .

      FILTER (?cate_ IN (java:FieldAccess,java:Name))

    } GROUP BY ?ctx ?x_ ?iname_ ?cfqn_ ?tyname_ ?vdtor_
  }

  {
    ?vdtor_ a java:Parameter ;
            src:child1 ?ty_ .
  }
  UNION
  {
    ?vdtor_ a java:VariableDeclarator ;
            src:parent/src:child1 ?ty_ .
  }

  ?ty a java:ReferenceType ;
      chg:relabeled ?ty_ .

}
}
''' % NS_TBL

Q_ADD_IVK_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddInvocation:", ?cfqn_, ":", ?iname_) AS ?name)
(?ctx0 AS ?dep) (?ty0_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctx ?x_ ?iname_ ?cfqn_ ?tyname_ ?vdtor_
    WHERE {

      {
        SELECT DISTINCT ?ctx ?x_ ?iname_ ?cfqn_ ?e_
        WHERE {

          ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
              java:name ?iname_ ;
              java:inTypeDeclaration/java:fullyQualifiedName ?cfqn_ ;
              src:child0 ?e_ ;
              chg:addition ?ctx .

          FILTER (?cat_ IN (java:PrimaryMethodInvocation,
                            java:PrimaryMethodInvocationStatement,
                            java:FieldAccess))

        } GROUP BY ?ctx ?x_ ?iname_ ?cfqn_ ?e_
      }

      ?e_ a ?cate_ OPTION (INFERENCE NONE) ;
          java:typeName ?tyname_ ;
          java:declaredBy ?vdtor_ ;
          src:parent ?x_ .

      FILTER (?cate_ IN (java:FieldAccess,java:Name))

    } GROUP BY ?ctx ?x_ ?iname_ ?cfqn_ ?tyname_ ?vdtor_
  }

  {
    ?vdtor_ a java:Parameter ;
            src:child1 ?ty_ .
  }
  UNION
  {
    ?vdtor_ a java:VariableDeclarator ;
            src:parent/src:child1 ?ty_ .
  }

  ?ty_ a java:ReferenceType ;
       java:refersToDeclaration ?class_ .

  {
    SELECT DISTINCT ?class ?class_ ?ctx0 ?ty0_ ?fqn0_
    WHERE {
    ?class a java:TypeDeclaration ;
           chg:mappedTo ?class_ .

    ?class_ a java:TypeDeclaration .

    ?super_ a java:SuperType ;
            java:inTypeDeclaration ?class_ .

    ?ty0_ a java:ReferenceType ;
          java:name ?fqn0_ ;
          src:parent ?super_ ;
          chg:addition ?ctx0 .

    } GROUP BY ?class ?class_ ?ctx0 ?ty0_ ?fqn0_
  }

  FILTER NOT EXISTS {
    ?ty0_ java:refersToDeclaration [] .
  }

}
}
''' % NS_TBL

Q_CHG_ARG_TY_CHG_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeArgumentType:", ?cfqn, ".", ?fname) AS ?name)
(?x AS ?key) (?x_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field java:inTypeDeclaration/java:fullyQualifiedName ?cfqn .

  {
    SELECT DISTINCT ?field ?field_ ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
    WHERE {

      ?field #a java:FieldDeclaration ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?field_ .

      ?field_ #a java:FieldDeclaration ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

    } GROUP BY ?field ?field_ ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
  }

  {
    ?arg java:declaredBy ?vdtor ;
         src:parent ?args .

    ?args a java:Arguments ;
          src:parent ?x .

    ?x a java:InvocationOrInstanceCreation ;
       java:name ?xname ;
       java:mayInvokeMethod ?meth .
  }
  UNION
  {
    ?arg_ java:declaredBy ?vdtor_ ;
          src:parent ?args_ .

    ?args_ a java:Arguments ;
           src:parent ?x_ .

    ?x_ a java:InvocationOrInstanceCreation ;
        java:name ?xname_ ;
        java:mayInvokeMethod ?meth_ .
  }

  ?x chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_CHG_ARG_TY_RM_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeArgumentType:", ?cfqn, ".", ?fname) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?def java:inTypeDeclaration/java:fullyQualifiedName ?cfqn .

  {
    SELECT DISTINCT ?def ?def_ ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
    WHERE {

      ?def  src:child1 ?ty ;
            src:child2 ?vdtor ;
            chg:mappedTo ?def_ .

      ?def_ src:child1 ?ty_ ;
            src:child2 ?vdtor_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

    } GROUP BY ?def ?def_ ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
  }

  ?arg java:declaredBy ?vdtor ;
       src:parent ?args .

  ?args a java:Arguments ;
        src:parent ?x .

  ?x a java:InvocationOrInstanceCreation ;
     java:name ?xname ;
     java:mayInvokeMethod ?meth ;
     chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_ARG_TY_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeArgumentType:", ?cfqn, ".", ?fname) AS ?name)
(?ctx AS ?key) (?x_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?def java:inTypeDeclaration/java:fullyQualifiedName ?cfqn .

  {
    SELECT DISTINCT ?def ?def_ ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
    WHERE {

      ?def  src:child1 ?ty ;
            src:child2 ?vdtor ;
            chg:mappedTo ?def_ .

      ?def_ src:child1 ?ty_ ;
            src:child2 ?vdtor_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

    } GROUP BY ?def ?def_ ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
  }

  ?arg_ java:declaredBy ?vdtor_ ;
        src:parent ?args_ .

  ?args_ a java:Arguments ;
         src:parent ?x_ .

  ?x_ a java:InvocationOrInstanceCreation ;
      java:name ?xname_ ;
      java:mayInvokeMethod ?meth_ ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_STATIC_RM_NAME_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveStatic:", ?ffqn) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?static AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?fname ?static ?ctx_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             src:parent ?fdecl .

      ?fdecl a java:FieldDeclaration ;
             src:child0 ?mods ;
             src:child2 ?vdtor ;
             java:inTypeDeclaration ?tdecl .

      ?mods a java:Modifiers .

      ?static a java:Static ;
              src:parent ?mods ;
              chg:removal ?ctx_ .

    } GROUP BY ?vdtor ?fname ?static ?ctx_
  }

  ?x a java:Name ;
     java:name ?ffqn ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_RM_STATIC_CHG_NAME_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveStatic:", ?ffqn) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?static AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?fname ?static ?ctx_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             src:parent ?fdecl .

      ?fdecl a java:FieldDeclaration ;
             src:child0 ?mods ;
             src:child2 ?vdtor ;
             java:inTypeDeclaration ?tdecl .

      ?mods a java:Modifiers .

      ?static a java:Static ;
              src:parent ?mods ;
              chg:removal ?ctx_ .

    } GROUP BY ?vdtor ?fname ?static ?ctx_
  }

  ?x a java:Name ;
     java:name ?ffqn ;
     java:declaredBy ?vdtor ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_ADD_STATIC_ADD_NAME_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddStatic:", ?ffqn) AS ?name)
(?ctxx AS ?ent) (?x_ AS ?ent_)
(?ctx AS ?dep) (?static_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor_ ?fname_ ?static_ ?ctx
    WHERE {

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ ;
              src:parent ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              src:child0 ?mods_ ;
              src:child2 ?vdtor_ ;
              java:inTypeDeclaration ?tdecl_ .

      ?mods_ a java:Modifiers .

      ?static_ a java:Static ;
               src:parent ?mods_ ;
               chg:addition ?ctx .

    } GROUP BY ?vdtor_ ?fname_ ?static_ ?ctx
  }

  ?x_ a java:Name ;
      java:name ?ffqn_ ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_ADD_STATIC_CHG_NAME_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddStatic:", ?ffqn) AS ?name)
(?x AS ?ent) (?x_ AS ?ent_)
(?ctx AS ?dep) (?static_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor_ ?fname_ ?static_ ?ctx
    WHERE {

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ ;
              src:parent ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              src:child0 ?mods_ ;
              src:child2 ?vdtor_ ;
              java:inTypeDeclaration ?tdecl_ .

      ?mods_ a java:Modifiers .

      ?static_ a java:Static ;
               src:parent ?mods_ ;
               chg:addition ?ctx .

    } GROUP BY ?vdtor_ ?fname_ ?static_ ?ctx
  }

  ?x_ a java:Name ;
      java:name ?ffqn_ ;
      java:declaredBy ?vdtor_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_CHG_STATIC_ADD_NAME_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeStatic:", ?ffqn) AS ?name)
(?x AS ?ent) (?x_ AS ?ent_)
(?ctx AS ?dep) (?static_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor_ ?fname_ ?static_ ?mod
    WHERE {

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ ;
              src:parent ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              src:child0 ?mods_ ;
              src:child2 ?vdtor_ ;
              java:inTypeDeclaration ?tdecl_ .

      ?mods_ a java:Modifiers .

      ?static_ a java:Static ;
               src:parent ?mods_ ;
               ^chg:relabeled ?mod .

    } GROUP BY ?vdtor_ ?fname_ ?static_ ?mod
  }

  ?x_ a java:Name ;
      java:name ?ffqn_ ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_CHG_STATIC_CHG_NAME_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeStatic:", ?ffqn) AS ?name)
(?x AS ?ent) (?x_ AS ?ent_)
(?mod AS ?dep) (?static_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor_ ?fname_ ?static_ ?mod
    WHERE {

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ ;
              src:parent ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              src:child0 ?mods_ ;
              src:child2 ?vdtor_ ;
              java:inTypeDeclaration ?tdecl_ .

      ?mods_ a java:Modifiers .

      ?static_ a java:Static ;
               src:parent ?mods_ ;
               ^chg:relabeled ?mod .

    } GROUP BY ?vdtor_ ?fname_ ?static_ ?mod
  }

  ?x_ a java:Name ;
      java:name ?ffqn_ ;
      java:declaredBy ?vdtor_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_CHG_STATIC_RM_NAME_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeStatic:", ?ffqn) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?static AS ?ent) (?mod_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?fname ?static ?mod_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             src:parent ?fdecl .

      ?fdecl a java:FieldDeclaration ;
             src:child0 ?mods ;
             src:child2 ?vdtor ;
             java:inTypeDeclaration ?tdecl .

      ?mods a java:Modifiers .

      ?static a java:Static ;
              src:parent ?mods ;
              chg:relabeled ?mod_ .

    } GROUP BY ?vdtor ?fname ?static ?mod_
  }

  ?x a java:Name ;
     java:name ?ffqn ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_CHG_STATIC_CHG_NAME_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeStatic:", ?ffqn) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?static AS ?ent) (?mod_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?fname ?static ?mod_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             src:parent ?fdecl .

      ?fdecl a java:FieldDeclaration ;
             src:child0 ?mods ;
             src:child2 ?vdtor ;
             java:inTypeDeclaration ?tdecl .

      ?mods a java:Modifiers .

      ?static a java:Static ;
              src:parent ?mods ;
              chg:relabeled ?mod_ .

    } GROUP BY ?vdtor ?fname ?static ?mod_
  }

  ?x a java:Name ;
     java:name ?ffqn ;
     java:declaredBy ?vdtor ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_CHG_RETTY_CHG_FIELD_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeReturnType:", ?mfqn) AS ?name)
(?retty AS ?key) (?retty_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_ ?rhs ?rhs_
    WHERE {

      {
        SELECT DISTINCT ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
        WHERE {

          ?field a java:FieldDeclaration ;
                 src:child1 ?ty ;
                 src:child2 ?vdtor ;
                 chg:mappedTo ?field_ .

          ?field_ a java:FieldDeclaration ;
                  src:child1 ?ty_ ;
                  src:child2 ?vdtor_ .

          ?vdtor a java:VariableDeclarator ;
                 java:name ?fname ;
                 chg:mappedTo ?vdtor_ .

          ?vdtor_ a java:VariableDeclarator ;
                  java:name ?fname_ .

          ?ty a java:Type ;
              chg:relabeled ?ty_ .

        } GROUP BY ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_
      }

      ?assign a java:AssignmentStatement ;
              src:child0 ?lhs ;
              src:child1 ?rhs ;
              chg:mappedTo ?assign_ .

      ?assign_ a java:AssignmentStatement ;
               src:child0 ?lhs_ ;
               src:child1 ?rhs_ .

      ?lhs java:declaredBy ?vdtor ;
           chg:mappedTo ?lhs_ .

      ?lhs_ java:declaredBy ?vdtor_ ;
            src:parent ?args_ .

    } GROUP BY ?vdtor ?vdtor_ ?fname ?fname_ ?ty ?ty_ ?rhs ?rhs_
  }

  ?x a java:InvocationOrInstanceCreation ;
     src:parent* ?rhs ;
     java:name ?xname ;
     java:mayInvokeMethod ?meth ;
     chg:mappedTo ?x_ .

  ?x_ a java:InvocationOrInstanceCreation ;
      src:parent* ?rhs_ ;
      java:name ?xname_ ;
      java:mayInvokeMethod ?meth_ .

  ?meth a java:MethodDeclaration ;
        java:fullyQualifiedName ?mfqn ;
        src:child2 ?retty ;
        chg:mappedTo ?meth_ .

  ?meth_ a java:MethodDeclaration ;
         java:fullyQualifiedName ?mfqn_ ;
         src:child2 ?retty_ .

  ?retty chg:relabeled ?retty_ .

}
}
''' % NS_TBL

Q_RM_M_FINAL_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?mfqn, ?msig) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final ?ctx_ ?rty ?rty_ ?tdecl ?tdecl_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
        ?final ?ctx_
        WHERE {
          ?meth a java:MethodDeclaration ;
                java:inTypeDeclaration ?class ;
                java:name ?mname ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodDeclaration ;
                 java:inTypeDeclaration ?class_ ;
                 java:name ?mname_ ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ .

          ?final a java:Final ;
                 java:inMethod ?meth ;
                 chg:removal ?ctx_ .

        } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
        ?final ?ctx_
      }

      ?rty a java:ReferenceType ;
           java:refersToDeclaration ?class0 ;
           src:parent [ a java:SuperType ] ;
           java:inTypeDeclaration ?tdecl ;
           chg:relabeled ?rty_ .

      ?rty_ a java:ReferenceType ;
            java:refersToDeclaration ?class0_ ;
            src:parent [ a java:SuperType ] ;
            java:inTypeDeclaration ?tdecl_ .

      ?class0_ java:subTypeOf* ?class_ .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final ?ctx_ ?rty ?rty_ ?tdecl ?tdecl_
  }

  ?tdecl_ a java:TypeDeclaration .

  FILTER EXISTS {
    [] a java:MethodDeclaration ;
       java:inTypeDeclaration ?tdecl_ ;
       java:name ?mname_ ;
       java:signature ?msig_ .
  }

}
}
''' % NS_TBL

Q_ADD_M_FINAL_CHG_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?mfqn, ?msig) AS ?name)
(?ctx AS ?ent) (?final_ AS ?ent_)
(?rty AS ?dep) (?rty_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final_ ?ctx ?rty ?rty_ ?tdecl ?tdecl_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
        ?final_ ?ctx
        WHERE {
          ?meth a java:MethodDeclaration ;
                java:inTypeDeclaration ?class ;
                java:name ?mname ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodDeclaration ;
                 java:inTypeDeclaration ?class_ ;
                 java:name ?mname_ ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ .

          ?final_ a java:Final ;
                  java:inMethod ?meth_ ;
                  chg:addition ?ctx .

        } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
        ?final_ ?ctx
      }

      ?rty a java:ReferenceType ;
           java:refersToDeclaration ?class0 ;
           src:parent [ a java:SuperType ] ;
           java:inTypeDeclaration ?tdecl ;
           chg:relabeled ?rty_ .

      ?rty_ a java:ReferenceType ;
            java:refersToDeclaration ?class0_ ;
            src:parent [ a java:SuperType ] ;
            java:inTypeDeclaration ?tdecl_ .

      ?class0 java:subTypeOf* ?class .

    } GROUP BY ?meth ?meth_ ?class ?class_ ?mname ?mname_ ?mfqn ?mfqn_ ?msig ?msig_
    ?final_ ?ctx ?rty ?rty_ ?tdecl ?tdecl_
  }

  ?tdecl a java:TypeDeclaration .

  FILTER EXISTS {
    [] a java:MethodDeclaration ;
       java:inTypeDeclaration ?tdecl ;
       java:name ?mname ;
       java:signature ?msig .
  }

}
}
''' % NS_TBL

Q_CHG_FOR_PARAM_TY_CHG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeForParameterType:", ?mfqn, ?msig) AS ?name)
(?pty AS ?key) (?pty_ AS ?key_)
(?ety AS ?ent) (?ety_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?expr ?expr_ ?pty ?pty_ ?mfqn ?msig
    WHERE {

      ?for a java:EnhancedForStatement ;
           java:inMethodOrConstructor [ java:fullyQualifiedName ?mfqn; java:signature ?msig ] ;
           src:child0 ?param ;
           src:child1 ?expr ;
           chg:mappedTo ?for_ .

      ?for_ a java:EnhancedForStatement ;
            src:child0 ?param_ ;
            src:child1 ?expr_ .

      ?param a java:Parameter ;
             src:child1 ?pty ;
             chg:mappedTo ?param_ .

      ?param_ a java:Parameter ;
              src:child1 ?pty_ .

      ?pty chg:relabeled ?pty_ .

    } GROUP BY ?expr ?expr_ ?pty ?pty_ ?mfqn ?msig
  }

  {
    SELECT DISTINCT ?expr ?expr_ ?ety ?ety_
    WHERE {

      ?expr chg:mappedTo ?expr_ .

      {
        ?expr java:declaredBy ?vdtor .
        ?expr_ java:declaredBy ?vdtor_ .

        ?vdtor src:parent ?vdecl .

        ?vdecl #a java:LocalVariableDeclarationStatement ;
               src:child1 ?ty0 .

        ?vdtor_ src:parent ?vdecl_ .

        ?vdecl_ #a java:LocalVariableDeclarationStatement ;
                src:child1 ?ty0_ .
      }
      UNION
      {
        ?expr java:declaredBy ?param0 .
        ?expr_ java:declaredBy ?param0_ .

        ?param0 a java:Parameter ;
                src:child1 ?ty0 .

        ?param0_ a java:Parameter ;
                 src:child1 ?ty0_ .
      }

      ?ty0 a java:Type ;
           chg:mappedTo ?ty0_ .

      ?ty0_ a java:Type .

      ?ety src:parent ?ty0 OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(0)) .
      ?ety_ src:parent ?ty0_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(0)) .

      ?ety chg:relabeled ?ety_ .

    } GROUP BY ?expr ?expr_ ?ety ?ety_
  }

}
}
''' % NS_TBL

# Q_ADD_STMT_ADD_COND_JAVA = '''DEFINE input:inference "ont.cpi"
# PREFIX fb:  <%(fb_ns)s>
# PREFIX ver: <%(ver_ns)s>
# PREFIX src: <%(src_ns)s>
# PREFIX chg: <%(chg_ns)s>
# PREFIX java: <%(java_ns)s>
# PREFIX delta: <%(delta_ns)s>
# SELECT DISTINCT
# (CONCAT("ChangeForParameterType:", ?mfqn, ?msig) AS ?name)
# (?ctx AS ?dep) (?cond_ AS ?dep_)
# (?ctxs AS ?ent) (?stmt_ AS ?ent_)
# WHERE {
# GRAPH <%(fb_ns)s%%(proj_id)s> {

#   ?if_ a java:IfStatement ;
#        src:child0 ?cond_ .

#   ?cond_ a java:Expression ;
#          chg:addition ?ctx .

#   ?stmt_ a java:Statement ;
#          src:parent+ ?if_ ;
#          chg:addition ?ctxs .

# }
# }
# ''' % NS_TBL

Q_RM_STATIC_CHG_INIT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveStatic") AS ?name)
(?expr AS ?dep) (?expr_ AS ?dep_)
(?static0 AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field a java:FieldDeclaration ;
         src:child0 ?mods ;
         src:child2 ?vdtor ;
         chg:mappedTo ?field_ .

  ?field_ a java:FieldDeclaration ;
          src:child0 ?mods_ ;
          src:child2 ?vdtor_ .

  ?static a java:Static ;
         src:parent ?mods .

  ?vdtor a java:VariableDeclarator ;
         java:name ?fname ;
         src:child0 ?expr ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?fname_ ;
          src:child0 ?expr_ .

  ?expr chg:relabeled ?expr_ .

#

  ?expr java:declaredBy ?vdtor0 .

  ?vdtor0 a java:VariableDeclarator ;
          src:parent/src:child0 ?mods0 ;
          java:name ?vname0 .

  ?static0 a java:Static ;
          src:parent ?mods0 ;
          chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_STATIC_CHG_INIT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddStatic") AS ?name)
(?expr AS ?ent) (?expr_ AS ?ent_)
(?ctx AS ?dep) (?static0_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?field a java:FieldDeclaration ;
         src:child0 ?mods ;
         src:child2 ?vdtor ;
         chg:mappedTo ?field_ .

  ?field_ a java:FieldDeclaration ;
          src:child0 ?mods_ ;
          src:child2 ?vdtor_ .

  ?static_ a java:Static ;
          src:parent ?mods_ .

  ?vdtor a java:VariableDeclarator ;
         java:name ?fname ;
         src:child0 ?expr ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?fname_ ;
          src:child0 ?expr_ .

  ?expr chg:relabeled ?expr_ .

#

  ?expr_ java:declaredBy ?vdtor0_ .

  ?vdtor0_ a java:VariableDeclarator ;
           src:parent/src:child0 ?mods0_ ;
           java:name ?vname0_ .

  ?static0_ a java:Static ;
            src:parent ?mods0_ ;
            chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_LABEL_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveLabel") AS ?name)
(?stmt0 AS ?dep) (?ctx0_ AS ?dep_)
(?lstmt AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?lstmt a java:LabeledStatement ;
         java:name ?lab ;
         src:child0 ?stmt ;
         chg:removal ?ctx_ .

  ?stmt a java:Statement ;
        a ?cat OPTION (INFERENCE NONE) .

  ?stmt0 a ?cat0 OPTION (INFERENCE NONE) ;
         src:parent+ ?stmt ;
         java:name ?lab ;
         chg:removal ?ctx0_ .

  FILTER (?cat0 IN (java:BreakStatement,java:ContinueStatement))

}
}
''' % NS_TBL

Q_RM_LABEL_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveLabel") AS ?name)
(?stmt0 AS ?dep) (?stmt0_ AS ?dep_)
(?lstmt AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?lstmt a java:LabeledStatement ;
         java:name ?lab ;
         src:child0 ?stmt ;
         chg:removal ?ctx_ .

  ?stmt a java:Statement ;
        a ?cat OPTION (INFERENCE NONE) .

  ?stmt0 a ?cat0 OPTION (INFERENCE NONE) ;
         src:parent+ ?stmt ;
         java:name ?lab ;
         chg:relabeled ?stmt0_ .

  FILTER (?cat0 IN (java:BreakStatement,java:ContinueStatement))

}
}
''' % NS_TBL

Q_ADD_LABEL_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddLabel") AS ?name)
(?ctx AS ?dep) (?lstmt_ AS ?dep_)
(?ctx0 AS ?ent) (?stmt0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?lstmt_ a java:LabeledStatement ;
          java:name ?lab_ ;
          src:child0 ?stmt_ ;
          chg:addition ?ctx .

  ?stmt_ a java:Statement ;
         a ?cat_ OPTION (INFERENCE NONE) .

  ?stmt0_ a ?cat0_ OPTION (INFERENCE NONE) ;
          src:parent+ ?stmt_ ;
         java:name ?lab_ ;
         chg:addition ?ctx0 .

  FILTER (?cat0_ IN (java:BreakStatement,java:ContinueStatement))

}
}
''' % NS_TBL

Q_ADD_LABEL_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddLabel") AS ?name)
(?ctx AS ?dep) (?lstmt_ AS ?dep_)
(?stmt0 AS ?ent) (?stmt0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?lstmt_ a java:LabeledStatement ;
          java:name ?lab_ ;
          src:child0 ?stmt_ ;
          chg:addition ?ctx .

  ?stmt_ a java:Statement ;
         a ?cat_ OPTION (INFERENCE NONE) .

  ?stmt0_ a ?cat0_ OPTION (INFERENCE NONE) ;
          src:parent+ ?stmt_ ;
         java:name ?lab_ ;
         ^chg:relabeled ?stmt0 .

  FILTER (?cat0_ IN (java:BreakStatement,java:ContinueStatement))

}
}
''' % NS_TBL


Q_CHG_FD_TY_INS_RHS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType") AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ctx AS ?ent) (?e_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
  }

  ?x java:declaredBy ?vdtor .
  ?x_ java:declaredBy ?vdtor_ .

  ?a a java:AssignmentStatement ;
     src:child0 ?x ;
     src:child1 ?e ;
     chg:mappedTo ?a_ .

  ?a_ a java:AssignmentStatement ;
      src:child0 ?x_ ;
      src:child1 ?e_ .

  ?e_ chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_FD_TY_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType") AS ?name)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?ctx AS ?ent) (?a_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
  }

  ?x_ java:declaredBy ?vdtor_ .

  ?a_ a java:AssignmentStatement ;
      src:child0 ?x_ ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_FD_TY_DEL_RHS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType") AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?e AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
  }

  ?x java:declaredBy ?vdtor .
  ?x_ java:declaredBy ?vdtor_ .

  ?a a java:AssignmentStatement ;
     src:child0 ?x ;
     src:child1 ?e ;
     chg:mappedTo ?a_ .

  ?a_ a java:AssignmentStatement ;
      src:child0 ?x_ ;
      src:child1 ?e_ .

  ?e chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_FD_TY_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType") AS ?name)
(?a AS ?dep) (?ctx_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
  }

  ?x java:declaredBy ?vdtor .

  ?a a java:AssignmentStatement ;
     src:child0 ?x ;
     chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_FD_TY_CHG_RHS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldType") AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?e AS ?ent) (?e_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn ?vdtor ?vdtor_
  }

  ?x java:declaredBy ?vdtor .
  ?x_ java:declaredBy ?vdtor_ .

  ?a a java:AssignmentStatement ;
     src:child0 ?x ;
     src:child1 ?e ;
     chg:mappedTo ?a_ .

  ?a_ a java:AssignmentStatement ;
      src:child0 ?x_ ;
      src:child1 ?e_ .

  ?e chg:relabeled ?e_ .

}
}
''' % NS_TBL

Q_RM_INIT_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveInitializer") AS ?name)
(?ctxa AS ?dep) (?assign_ AS ?dep_)
(?ini AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?stmt_ ?succ_
     ?ini ?ctx_ ?assign_ ?ctxa
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini ?ctx_ ?stmt_
        WHERE {

          ?vdtor a java:VariableDeclarator ;
                 java:inMethodOrConstructor ?meth ;
                 java:name ?vname ;
                 src:child0 ?ini ;
                 chg:mappedTo ?vdtor_ .

          ?ini chg:removal ?ctx_ .

          ?vdtor_ a java:VariableDeclarator ;
                  java:inBlockStatement ?stmt_ ;
                  java:inMethodOrConstructor ?meth_ ;
                  java:name ?vname_ .

        } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini ?ctx_ ?stmt_
      }

      ?stmt_ java:successor ?assign_ OPTION (TRANSITIVE, T_DISTINCT) .

      ?assign_ a java:AssignmentStatement ;
               src:child0/java:name ?vname_ ;
               chg:addition ?ctxa .

      ?assign_ java:successor ?succ_ OPTION (TRANSITIVE, T_DISTINCT) .

      ?succ_ a java:Statement .

    } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?stmt_ ?succ_
     ?ini ?ctx_ ?assign_ ?ctxa
  }

  ?v_ a java:Name ;
      src:parent+ ?succ_ ;
      java:name ?vname_ .

  FILTER NOT EXISTS {
    ?succ_ a java:AssignmentStatement .
  }

}
}
''' % NS_TBL

Q_ADD_INIT_RM_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddInitializer") AS ?name)
(?ctx AS ?dep) (?ini_ AS ?dep_)
(?assign AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?stmt ?succ
     ?ini_ ?ctx ?assign ?ctxa_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini_ ?ctx ?stmt
        WHERE {

          ?vdtor a java:VariableDeclarator ;
                 java:inBlockStatement ?stmt ;
                 java:inMethodOrConstructor ?meth ;
                 java:name ?vname ;
                 chg:mappedTo ?vdtor_ .

          ?vdtor_ a java:VariableDeclarator ;
                  java:inMethodOrConstructor ?meth_ ;
                  java:name ?vname_ ;
                  src:child0 ?ini_ .

          ?ini_ chg:addition ?ctx .

        } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini_ ?ctx ?stmt
      }

      ?stmt java:successor ?assign OPTION (TRANSITIVE, T_DISTINCT) .

      ?assign a java:AssignmentStatement ;
              src:child0/java:name ?vname ;
              chg:removal ?ctxa_ .

      ?assign java:successor ?succ OPTION (TRANSITIVE, T_DISTINCT) .

      ?succ a java:Statement .

    } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?stmt ?succ
     ?ini_ ?ctx ?assign ?ctxa_
  }

  ?v a java:Name ;
     src:parent+ ?succ ;
     java:name ?vname .

  FILTER NOT EXISTS {
    ?succ a java:AssignmentStatement .
  }

}
}
''' % NS_TBL

Q_ADD_INIT_CHG_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddInitializer:", ?vname_) AS ?name)
(?ctx AS ?dep) (?ini_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini_ ?ctx ?stmt_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ ;
              java:inBlockStatement ?stmt_ ;
              src:child0 ?ini_ .

      ?ini_ chg:addition ?ctx .

    } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini_ ?ctx ?stmt_
  }

  ?x_ a java:Name ;
      java:name ?vname_ ;
      java:declaredBy ?vdtor_ ;
      ^chg:relabeled ?x .

  FILTER NOT EXISTS {
    ?stmt_ java:successor ?assign_ OPTION (TRANSITIVE, T_DISTINCT) .
    ?assign_ a java:AssignmentStatement ;
             src:child0/java:name ?vname_ .
    ?assign_ java:successor ?succ_ OPTION (TRANSITIVE, T_DISTINCT) .
    ?succ_ a java:Statement .
    ?x_ src:parent+ ?succ_ .
  }

}
}
''' % NS_TBL

Q_ADD_INIT_ADD_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddInitializer:", ?vname_) AS ?name)
(?ctx AS ?dep) (?ini_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini_ ?ctx ?stmt_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ ;
              java:inBlockStatement ?stmt_ ;
              src:child0 ?ini_ .

      ?ini_ chg:addition ?ctx .

    } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini_ ?ctx ?stmt_
  }

  ?x_ a java:Name ;
      java:name ?vname_ ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctxx .

  FILTER NOT EXISTS {
    ?stmt_ java:successor ?assign_ OPTION (TRANSITIVE, T_DISTINCT) .
    ?assign_ a java:AssignmentStatement ;
             src:child0/java:name ?vname_ .
    ?assign_ java:successor ?succ_ OPTION (TRANSITIVE, T_DISTINCT) .
    ?succ_ a java:Statement .
    ?x_ src:parent+ ?succ_ .
  }

}
}
''' % NS_TBL

Q_RM_INIT_CHG_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveInitializer:", ?vname) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?ini AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini ?ctx_ ?stmt
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             java:inBlockStatement ?stmt ;
             src:child0 ?ini ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ .

      ?ini chg:removal ?ctx_ .

    } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini ?ctx_ ?stmt
  }

  ?x a java:Name ;
     java:name ?vname ;
     java:declaredBy ?vdtor ;
     chg:relabeled ?x_ .

  FILTER NOT EXISTS {
    ?stmt java:successor ?assign OPTION (TRANSITIVE, T_DISTINCT) .
    ?assign a java:AssignmentStatement ;
             src:child0/java:name ?vname .
    ?assign java:successor ?succ OPTION (TRANSITIVE, T_DISTINCT) .
    ?succ a java:Statement .
    ?x src:parent+ ?succ .
  }

}
}
''' % NS_TBL

Q_RM_INIT_RM_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveInitializer:", ?vname) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?ini AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini ?ctx_ ?stmt
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             java:inBlockStatement ?stmt ;
             src:child0 ?ini ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ .

      ?ini chg:removal ?ctx_ .

    } GROUP BY ?meth ?meth_ ?vdtor ?vdtor_ ?vname ?vname_ ?ini ?ctx_ ?stmt
  }

  ?x a java:Name ;
     java:name ?vname ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctxx_ .

  FILTER NOT EXISTS {
    ?stmt java:successor ?assign OPTION (TRANSITIVE, T_DISTINCT) .
    ?assign a java:AssignmentStatement ;
             src:child0/java:name ?vname .
    ?assign java:successor ?succ OPTION (TRANSITIVE, T_DISTINCT) .
    ?succ a java:Statement .
    ?x src:parent+ ?succ .
  }

}
}
''' % NS_TBL

Q_RM_ASSIGN_RM_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAssignment:", ?vname) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?assign AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?vdtor ?vname ?stmt ?x ?ctxx_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             java:inMethodOrConstructor ?meth ;
             java:name ?vname ;
             java:inBlockStatement ?stmt .

      FILTER NOT EXISTS {
        ?vdtor src:child0 [] .
      }

      ?x a java:Name ;
         java:name ?vname ;
         java:declaredBy ?vdtor ;
         chg:removal ?ctxx_ .

    } GROUP BY ?meth ?vdtor ?vname ?stmt ?x ?ctxx_
  }

  ?stmt java:successor ?assign OPTION (TRANSITIVE, T_DISTINCT) .

  ?assign a java:AssignmentStatement ;
          java:successor ?succ OPTION (TRANSITIVE, T_DISTINCT) ;
          src:child0/java:name ?vname ;
          chg:removal ?ctx_ .

  ?succ a java:Statement .

  ?x src:parent+ ?succ .

}
}
''' % NS_TBL

Q_ADD_ASSIGN_ADD_LVAR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddAssignment:", ?vname_) AS ?name)
(?ctx AS ?dep) (?assign_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?vdtor_ ?vname_ ?stmt_ ?x_ ?ctxx
    WHERE {

      ?vdtor_ a java:VariableDeclarator ;
              java:inMethodOrConstructor ?meth_ ;
              java:name ?vname_ ;
              java:inBlockStatement ?stmt_ .

      FILTER NOT EXISTS {
        ?vdtor_ src:child0 [] .
      }

      ?x_ a java:Name ;
          java:name ?vname_ ;
          java:declaredBy ?vdtor_ ;
          chg:addition ?ctxx .

    } GROUP BY ?meth_ ?vdtor_ ?vname_ ?stmt_ ?x_ ?ctxx
  }

  ?stmt_ java:successor ?assign_ OPTION (TRANSITIVE, T_DISTINCT) .

  ?assign_ a java:AssignmentStatement ;
           java:successor ?succ_ OPTION (TRANSITIVE, T_DISTINCT) ;
           src:child0/java:name ?vname_ ;
           chg:addition ?ctx .

  ?succ_ a java:Statement .

  ?x_ src:parent+ ?succ_ .

}
}
''' % NS_TBL

Q_MOVE_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveAssignment") AS ?name)
(?assign AS ?key) (?ctxa_ AS ?key_)
(?ctxa AS ?ent) (?assign_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fqn ?vdtor ?vdtor_ ?fname ?fname_ ?ctor ?ctor_
    WHERE {

      ?tdecl java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ .

      ?ctor a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            chg:mappedTo ?ctor_ .

      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?tdecl_ .

    } GROUP BY ?fqn ?vdtor ?vdtor_ ?fname ?fname_ ?ctor ?ctor_
  }

  ?assign a java:AssignmentStatement ;
          java:inConstructor ?ctor ;
          src:child0 ?lhs ;
          chg:genRemoved ?ctxa_ .

  ?assign_ a java:AssignmentStatement ;
           java:inConstructor ?ctor_ ;
           src:child0 ?lhs_ ;
           chg:genAdded ?ctxa .

  ?assign chg:movedTo ?assign_ .

  ?lhs java:declaredBy ?vdtor .
  ?lhs_ java:declaredBy ?vdtor_ .

}
}
''' % NS_TBL

Q_RM_ACC_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAccessModifier") AS ?name)
(?acc0 AS ?key) (?ctxa0_ AS ?key_)
(?meth0 AS ?ent) (?ctxm0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?mfqn ?msig ?mname ?cata
    WHERE {

      ?meth a java:MethodDeclaration ;
            src:child0 ?mods ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?mfqn ;
            java:name ?mname ;
            java:signature ?msig .

      ?acc a java:AccessModifier ;
           a ?cata OPTION (INFERENCE NONE) ;
           src:parent ?mods .

      FILTER (EXISTS {
        [] a java:Abstract ;
           java:inMethod ?meth .
      } || EXISTS {
        ?tdecl a java:InterfaceDeclaration .
      })

    } GROUP BY ?tdecl ?mfqn ?msig ?mname ?cata
  }

  ?tdecl ver:version ?ver .

  {
    SELECT DISTINCT ?meth0 ?ctxm0_ ?msig ?mname ?acc0 ?ctxa0_ ?cata0
    WHERE {

      ?meth0 a java:MethodDeclaration ;
             src:child0 ?mods0 ;
             java:name ?mname ;
             java:signature ?msig ;
             chg:removal ?ctxm0_ .

      ?override0 a java:MarkerAnnotation ;
                 src:parent ?mods0 ;
                 java:name "Override" .

      ?acc0 a java:AccessModifier ;
            a ?cata0 OPTION (INFERENCE NONE) ;
            src:parent ?mods0 ;
            chg:removal ?ctxa0_ .

    } GROUP BY ?meth0 ?ctxm0_ ?msig ?mname ?acc0 ?ctxa0_ ?cata0
  }

  {
    ?meth0 java:inTypeDeclaration ?tdecl0 .
  }
  UNION
  {
    ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
  }

  ?tdecl0 ver:version ?ver ;
          java:subTypeOf* ?tdecl .

  FILTER (?cata = java:Public && ?cata0 = java:Public)

}
}
''' % NS_TBL

Q_ADD_ACC_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddAccessModifier") AS ?name)
(?ctxa0 AS ?key) (?acc0_ AS ?key_)
(?ctxm0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl_ ?mfqn_ ?msig_ ?mname_ ?cata_
    WHERE {

      ?meth_ a java:MethodDeclaration ;
             src:child0 ?mods_ ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:name ?mname_ ;
             java:signature ?msig_ .

      ?acc_ a java:AccessModifier ;
            a ?cata_ OPTION (INFERENCE NONE) ;
            src:parent ?mods_ .

      FILTER (EXISTS {
        [] a java:Abstract ;
           java:inMethod ?meth_ .
      } || EXISTS {
        ?tdecl_ a java:InterfaceDeclaration .
      })

    } GROUP BY ?tdecl_ ?mfqn_ ?msig_ ?mname_ ?cata_
  }

  ?tdecl_ ver:version ?ver_ .

  {
    SELECT DISTINCT ?meth0_ ?ctxm0 ?msig_ ?mname_ ?acc0_ ?ctxa0 ?cata0_
    WHERE {

      ?meth0_ a java:MethodDeclaration ;
              src:child0 ?mods0_ ;
              java:name ?mname_ ;
              java:signature ?msig_ ;
              chg:addition ?ctxm0 .

      ?override0_ a java:MarkerAnnotation ;
                  src:parent ?mods0_ ;
                  java:name "Override" .

      ?acc0_ a java:AccessModifier ;
             a ?cata0_ OPTION (INFERENCE NONE) ;
             src:parent ?mods0_ ;
             chg:addition ?ctxa0 .

    } GROUP BY ?meth0_ ?ctxm0 ?msig_ ?mname_ ?acc0_ ?ctxa0 ?cata0_
  }

  {
    ?meth0_ java:inTypeDeclaration ?tdecl0_ .
  }
  UNION
  {
    ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
  }

  ?tdecl0_ ver:version ?ver_ ;
          java:subTypeOf* ?tdecl_ .

  FILTER (?cata_ = java:Public && ?cata0_ = java:Public)

}
}
''' % NS_TBL

Q_RM_TY_REL_EXPR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveType") AS ?name)
(?ty AS ?key) (?ctx_ AS ?key_)
(?px AS ?ent) (?px_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:Expression ;
     java:declaredBy ?vdtor ;
     java:name ?fname ;
     src:parent ?px ;
     chg:mappedTo ?x_ .

  ?x_ a java:Expression ;
      java:declaredBy ?vdtor_ ;
      java:name ?fname_ .

  FILTER NOT EXISTS {
    ?x java:typeName ?tyname .
    ?x_ java:typeName ?tyname .
  }

  ?px a java:Expression ;
      a ?cat OPTION (INFERENCE NONE) ;
      chg:relabeled ?px_ .

  [] src:child1 ?ty ;
     src:child2 ?vdtor .

  ?ty a java:Type ;
      chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_RM_TY_DEL_EXPR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveType") AS ?name)
(?ty AS ?key) (?ctx_ AS ?key_)
(?px AS ?ent) (?ctxp_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:Expression ;
     java:declaredBy ?vdtor ;
     java:name ?fname ;
     src:parent ?px ;
     chg:mappedTo ?x_ .

  ?x_ a java:Expression ;
      java:declaredBy ?vdtor_ ;
      java:name ?fname_ .

  FILTER NOT EXISTS {
    ?x java:typeName ?tyname .
    ?x_ java:typeName ?tyname .
  }

  ?px a java:Expression ;
      a ?cat OPTION (INFERENCE NONE) ;
      chg:removal ?ctxp_ .

  [] src:child1 ?ty ;
     src:child2 ?vdtor .

  ?ty a java:Type ;
      chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_TY_INS_EXPR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddType") AS ?name)
(?ctx AS ?key) (?ty_ AS ?key_)
(?ctxp AS ?ent) (?px_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:Expression ;
     java:declaredBy ?vdtor ;
     java:name ?fname ;
     chg:mappedTo ?x_ .

  ?x_ a java:Expression ;
      src:parent ?px_ ;
      java:declaredBy ?vdtor_ ;
      java:name ?fname_ .

  FILTER NOT EXISTS {
    ?x java:typeName ?tyname .
    ?x_ java:typeName ?tyname .
  }

  ?px_ a java:Expression ;
      a ?cat_ OPTION (INFERENCE NONE) ;
      chg:addition ?ctxp .

  [] src:child1 ?ty_ ;
     src:child2 ?vdtor_ .

  ?ty_ a java:Type ;
       chg:addition ?ctx .

}
}
''' % NS_TBL

Q_ADD_TY_REL_EXPR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddType") AS ?name)
(?ctx AS ?key) (?ty_ AS ?key_)
(?px AS ?ent) (?px_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:Expression ;
     java:declaredBy ?vdtor ;
     java:name ?fname ;
     chg:mappedTo ?x_ .

  ?x_ a java:Expression ;
      src:parent ?px_ ;
      java:declaredBy ?vdtor_ ;
      java:name ?fname_ .

  FILTER NOT EXISTS {
    ?x java:typeName ?tyname .
    ?x_ java:typeName ?tyname .
  }

  ?px_ a java:Expression ;
      a ?cat_ OPTION (INFERENCE NONE) ;
      ^chg:relabeled ?px .

  [] src:child1 ?ty_ ;
     src:child2 ?vdtor_ .

  ?ty_ a java:Type ;
       chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_STATIC_RM_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveStatic") AS ?name)
(?static AS ?ent) (?ctx_ AS ?ent_)
(?ivk AS ?dep) (?ctxi_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?civk a java:ConstructorInvocation ;
        a ?cat OPTION (INFERENCE NONE) ;
        src:child1 ?args .

  FILTER (?cat IN (java:SuperInvocation,java:ThisInvocation))

  ?ivk a java:Invocation ;
       src:parent+ ?args ;
       java:mayInvokeMethod ?meth ;
       chg:removal ?ctxi_ .

  ?meth a java:MethodDeclaration ;
         java:fullyQualifiedName ?mfqn ;
         src:child0 ?mods .

  ?static a java:Static ;
          src:parent ?mods ;
          chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_ADD_STATIC_ADD_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddStatic") AS ?name)
(?ctx AS ?dep) (?static_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?civk_ a java:ConstructorInvocation ;
         a ?cat_ OPTION (INFERENCE NONE) ;
         src:child1 ?args_ .

  FILTER (?cat_ IN (java:SuperInvocation,java:ThisInvocation))

  ?ivk_ a java:Invocation ;
        src:parent+ ?args_ ;
        java:mayInvokeMethod ?meth_ ;
        chg:addition ?ctxi .

  ?meth_ a java:MethodDeclaration ;
         java:fullyQualifiedName ?mfqn_ ;
         src:child0 ?mods_ .

  ?static_ a java:Static ;
           src:parent ?mods_ ;
           chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_ACC_RM_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAccessModifier") AS ?name)
(?acc AS ?ent) (?acc_ AS ?ent_)
(?x AS ?dep) (?ctx_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:FieldAccess ;
     java:inTypeDeclaration ?tdecl ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctx_ .

  [] java:inTypeDeclaration ?tdecl0 ;
     src:child2 ?vdtor ;
     src:child0/src:child ?acc .

  ?acc a java:AccessModifier ;
       chg:relabeled ?acc_ .

  ?acc_ a java:Private .

  ?tdecl java:subTypeOf+ ?tdecl0 .

}
}
''' % NS_TBL

Q_CHG_ACC_ADD_FACC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeAccessModifier") AS ?name)
(?acc AS ?dep) (?acc_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x_ a java:FieldAccess ;
      java:inTypeDeclaration ?tdecl_ ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctx .

  [] java:inTypeDeclaration ?tdecl0_ ;
     src:child2 ?vdtor_ ;
     src:child0/src:child ?acc_ .

  ?acc_ a java:AccessModifier ;
        ^chg:relabeled ?acc .

  ?acc a java:Private .

  ?tdecl_ java:subTypeOf+ ?tdecl0_ .

}
}
''' % NS_TBL

Q_RM_IF_ADD_IF_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveIf") AS ?name)
(?if0 AS ?key) (?ctx0_ AS ?key_)
(?ctx0 AS ?ent) (?if0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctor ?fname ?vdtor ?assign0 ?if0 ?ctx0_ ?if0_ ?ctx0 ?x0
    WHERE {

      ?ctor a java:ConstructorDeclaration .

      {
        SELECT DISTINCT ?ctor ?fname ?vdtor ?assign0 ?if0 ?ctx0_
        WHERE {

          ?assign0 a java:AssignmentStatement ;
                   src:parent+ ?if0 ;
                   src:child0 ?x0 .

          ?if0 a java:IfStatement ;
               java:inConstructor ?ctor ;
               chg:removal ?ctx0_ .

          ?x0 a java:FieldAccess ;
              java:declaredBy ?vdtor ;
              java:name ?fname .

        } GROUP BY ?ctor ?fname ?vdtor ?assign0 ?if0 ?ctx0_
      }

      ?assign0 chg:mappedTo ?assign0_ .
      ?ctor chg:mappedTo ?ctor_ .
      ?vdtor chg:mappedTo ?vdtor_ .
      ?x0 chg:mappedTo ?x0_ .

      ?assign0_ a java:AssignmentStatement ;
                src:parent+ ?if0_ ;
                src:child0 ?x0_ .

      ?if0_ a java:IfStatement ;
            java:inConstructor ?ctor_ ;
            chg:addition ?ctx0 .

      ?x0_ a java:FieldAccess ;
           java:declaredBy ?vdtor_ ;
           java:name ?fname_ .

    } GROUP BY ?ctor ?fname ?vdtor ?assign0 ?if0 ?ctx0_ ?if0_ ?ctx0 ?x0
  }

  {
    SELECT DISTINCT ?ctor ?fname ?vdtor ?assign1 ?if1 ?ctx1_
    WHERE {

      ?assign1 a java:AssignmentStatement ;
               src:parent+ ?if1 ;
               src:child0 ?x1 .

      ?if1 a java:IfStatement ;
           java:inConstructor ?ctor ;
           chg:removal ?ctx1_ .

      ?x1 a java:FieldAccess ;
          java:declaredBy ?vdtor ;
          java:name ?fname .

    } GROUP BY ?ctor ?fname ?vdtor ?assign1 ?if1 ?ctx1_
  }

  FILTER (?assign0 != ?assign1)

}
}
''' % NS_TBL

Q_DEL_COND_RM_COND_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("DeleteCond") AS ?name)
(?cond AS ?ent) (?ctx_ AS ?ent_)
(?e AS ?dep) (?ctxe_ AS ?dep_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?if a java:IfStatement ;
      src:child0 ?cond ;
      chg:mappedTo ?if_ .

  ?cond a java:Expression ;
        a ?cat OPTION (INFERENCE NONE) ;
        src:child+ ?e ;
        chg:deletedFrom ?ctx_ .

  FILTER (EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?cond ;
       delta:entity2 ?ctx_ .
  } || EXISTS {
    [] a chg:Move ;
       delta:entity1 ?cond .
  })

  ?e a java:Expression ;
     a ?cate OPTION (INFERENCE NONE) ;
     java:typeName ?tyname ;
     chg:removal ?ctxe_ .

  FILTER (?tyname != "boolean")

  FILTER (EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?e ;
       delta:entity2 ?ctxe_ .
  } || EXISTS {
    [] a chg:Move ;
       delta:entity1 ?e .
  })

}
}
''' % NS_TBL

Q_INS_COND_ADD_COND_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("InsertCond") AS ?name)
(?ctx AS ?dep) (?cond_ AS ?dep_)
(?ctxe AS ?ent) (?e_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?if_ a java:IfStatement ;
       src:child0 ?cond_ ;
       ^chg:mappedTo ?if .

  ?cond_ a java:Expression ;
         a ?cat_ OPTION (INFERENCE NONE) ;
         src:child+ ?e_ ;
         chg:insertedInto ?ctx .

  FILTER (EXISTS {
    [] a chg:Insertion ;
       delta:entity1 ?ctx ;
       delta:entity2 ?cond_ .
  } || EXISTS {
    [] a chg:Move ;
       delta:entity2 ?cond_ .
  })

  ?e_ a java:Expression ;
     a ?cate_ OPTION (INFERENCE NONE) ;
     java:typeName ?tyname_ ;
     chg:addition ?ctxe .

  FILTER (?tyname_ != "boolean")

  FILTER (EXISTS {
    [] a chg:Insertion ;
       delta:entity1 ?ctxe ;
       delta:entity2 ?e_ .
  } || EXISTS {
    [] a chg:Move ;
       delta:entity2 ?e_ .
  })

}
}
''' % NS_TBL

Q_MOVREL_V_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveRenameVar") AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x java:name ?xname ;
     java:declaredBy ?vdtor ;
     chg:movedTo ?x_ ;
     chg:relabeled ?x_ .

  ?x_ java:name ?xname_ ;
      java:declaredBy ?vdtor_ .

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }

  ?x java:inStatement ?stmt .

  FILTER NOT EXISTS {
    [] a java:VariableDeclarator ;
       java:name ?xname_ ;
       java:inStatement/java:successor+ ?stmt .
  }

  FILTER NOT EXISTS {
    [] a java:VariableDeclarator ;
       java:name ?xname_ ;
       src:parent ?field .

    ?field a java:FieldDeclaration ;
           java:inTypeDeclaration ?tdecl .

    ?x java:inTypeDeclaration+/java:subTypeOf* ?tdecl .
  }

}
}
''' % NS_TBL

Q_ADD_CTOR_IVK_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddConstructorInvocation") AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?ctx AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ivk_ a java:ConstructorInvocation ;
        java:inConstructor ?ctor_ ;
        chg:addition ?ctx .

  ?ctor a java:ConstructorDeclaration ;
        src:child4 ?body ;
        chg:mappedTo ?ctor_ .

  ?body a java:ConstructorBody .

  ?x a java:Entity ;
     src:parent ?body ;
     chg:removal ?ctx_ .

  {
    ?body src:child0 ?x .
  }
  UNION
  {
    ?y src:parent ?body .

    FILTER (?y != ?x)

    ?cx src:parent+ ?body ;
        chg:mappedStablyTo ?cx_ .

    ?cx_ src:parent+ ?ivk_ .

    ?cx src:parent+ ?y .

    ?x java:successor ?y OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .
  }

}
}
''' % NS_TBL

Q_RM_FOR_INIT_RM_LVD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveForInit") AS ?name)
(?for_init AS ?key) (?ctx0_ AS ?key_)
(?lvd AS ?ent) (?ctx1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?for_init a java:ForInit ;
            java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
            chg:removal ?ctx0_ .

  ?lvd a java:LocalVariableDeclaration ;
       src:parent ?for_init ;
       chg:removal ?ctx1_ .

}
}
''' % NS_TBL

Q_ADD_FOR_INIT_ADD_LVD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveForInit") AS ?name)
(?ctx0 AS ?key) (?for_init_ AS ?key_)
(?ctx1 AS ?ent) (?lvd_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?for_init_ a java:ForInit ;
             java:inTypeDeclaration/java:fullyQualifiedName ?cfqn_ ;
             chg:addition ?ctx0 .

  ?lvd_ a java:LocalVariableDeclaration ;
        src:parent ?for_init_ ;
        chg:addition ?ctx1 .

}
}
''' % NS_TBL

Q_ADD_CONT_ADD_LOOP_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddLoop") AS ?name)
(?ctxl AS ?dep) (?loop_ AS ?dep_)
(?ctxc AS ?ent) (?cont_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?cont_ a ?cat_ OPTION (INFERENCE NONE) ;
         java:inTypeDeclaration/java:name ?tname_ ;
         src:parent+ ?loop_ ;
         chg:addition ?ctxc .

  FILTER (?cat_ IN (java:ContinueStatement, java:BreakStatement))

  ?loop_ a java:LoopStatement ;
         chg:addition ?ctxl .

  FILTER NOT EXISTS {
    ?loop0_ a java:LoopStatement ;
            src:parent+ ?loop_ .
    ?cont_ src:parent+ ?loop0_ .
  }

  FILTER NOT EXISTS {
    ?loop_ src:parent+ ?loop0_ .
    ?loop0_ a java:LoopStatement .
  }

}
}
''' % NS_TBL

Q_RM_CONT_RM_LOOP_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveLoop") AS ?name)
(?cont AS ?dep) (?ctxc_ AS ?dep_)
(?loop AS ?ent) (?ctxl_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?cont a ?cat OPTION (INFERENCE NONE) ;
        java:inTypeDeclaration/java:name ?tname ;
        src:parent+ ?loop ;
        chg:removal ?ctxc_ .

  FILTER (?cat IN (java:ContinueStatement, java:BreakStatement))

  ?loop a java:LoopStatement ;
        chg:removal ?ctxl_ .

  FILTER NOT EXISTS {
    ?loop0 a java:LoopStatement ;
           src:parent+ ?loop .
    ?cont src:parent+ ?loop0 .
  }

  FILTER NOT EXISTS {
    ?loop src:parent+ ?loop0 .
    ?loop0 a java:LoopStatement .
  }

}
}
''' % NS_TBL

Q_ADD_LVAR_DEL_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddLocalVariable:", ?mfqn_, ?msig_, ":", ?pname_) AS ?name)
(?meth AS ?dep) (?ctx_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mfqn_ ?msig_ ?x_ ?ctx ?pname_
    WHERE {
      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ .

      ?params_ a java:Parameters ;
               src:parent ?meth_ .

      ?param_ a java:Parameter ;
              java:name ?pname_ ;
              src:parent ?params_ .

      ?x_ a java:Name ;
          java:declaredBy ?param_ ;
          java:name ?pname_ ;
          chg:addition ?ctx .

    } GROUP BY ?mfqn ?msig ?x_ ?ctx
  }

  ?x_ src:parent ?y_ .

  ?y_ a ?cat OPTION (INFERENCE NONE) ;
      ^chg:mappedStablyTo ?y .

  ?y java:inMethodOrConstructor ?meth .

  ?meth chg:removal ?ctx_ .

  ?params a java:Parameters ;
          src:parent ?meth .

  FILTER NOT EXISTS {
    ?param a java:Parameter ;
           java:name ?pname_ ;
           src:parent ?params .
  }

}
}
''' % NS_TBL

Q_RM_LVAR_INS_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveLocalVariable:", ?mfqn, ?msig, ":", ?pname) AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mfqn ?msig ?x ?ctx_ ?pname
    WHERE {
      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig .

      ?params a java:Parameters ;
              src:parent ?meth .

      ?param a java:Parameter ;
             java:name ?pname ;
             src:parent ?params .

      ?x a java:Name ;
         java:declaredBy ?param ;
         java:name ?pname ;
         chg:removal ?ctx_ .

    } GROUP BY ?mfqn ?msig ?x ?ctx_ ?pname
  }

  ?x src:parent ?y .

  ?y a ?cat OPTION (INFERENCE NONE) ;
     chg:mappedStablyTo ?y_ .

  ?y_ java:inMethodOrConstructor ?meth_ .

  ?meth_ chg:addition ?ctx .

  ?params_ a java:Parameters ;
           src:parent ?meth_ .

  FILTER NOT EXISTS {
    ?param_ a java:Parameter ;
            java:name ?pname ;
            src:parent ?params_ .
  }

}
}
''' % NS_TBL

Q_DEL_STMT_INS_STMT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("DeleteStatement") AS ?name)
(?stmt AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?stmt_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?stmt a java:BlockStatement ;
        src:parent [ a java:BlockStatementList ] ;
        java:inMethodOrConstructor ?meth ;
        chg:removal ?ctx_ .

  ?x a java:Expression ;
     java:inBlockStatement ?stmt ;
     chg:mappedStablyTo ?x_ .

  ?x_ a java:Expression ;
      java:inBlockStatement ?stmt_ .

  ?stmt_ a java:BlockStatement ;
         src:parent [ a java:BlockStatementList ] ;
         chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_OVERRIDED_METH_RM_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?cfqn0, ".", ?mname, ?sig0) AS ?name)
(?rty1 AS ?dep) (?ctxr_ AS ?dep_)
(?meth0 AS ?ent) (?ctxm_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0 java:fullyQualifiedName ?cfqn0 .
  {
    SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?rty1 ?ctxr_
    WHERE {

      {
        SELECT DISTINCT ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_
        WHERE {

          ?meth0 a java:MethodDeclaration ;
                 java:name ?mname ;
                 java:signature ?sig0 ;
                 chg:removal ?ctxm_ .

          ?tdecl0 a java:TypeDeclaration .
          {
            ?meth0 java:inInstanceCreation/java:ofReferenceType ?tdecl0 .
          }
          UNION
          {
            ?meth0 java:inTypeDeclaration ?tdecl0 .
          }

        } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_
      }

      ?tdecl0 java:subTypeOf* ?tdecl1 .

      ?super1 a java:SuperType ;
              src:parent/src:parent ?tdecl1 .

      ?rty1 a java:ReferenceType ;
            src:parent ?super1 ;
            chg:removal ?ctxr_ .

    } GROUP BY ?meth0 ?mname ?sig0 ?tdecl0 ?ctxm_ ?rty1 ?ctxr_
  }

  FILTER (NOT EXISTS {
    ?rty1 java:refersToDeclaration [] .
  } && NOT EXISTS {
    ?tdecl0 java:subTypeOf* ?tdecl1x .
    ?super1x a java:SuperType ;
             src:parent/src:parent ?tdecl1x .
    ?rty1x a java:ReferenceType ;
           src:parent ?super1x ;
           chg:removal [] .
    FILTER (?rty1x != ?rty1)
  } && NOT EXISTS {
    ?tdecl0x java:subTypeOf* ?tdecl1 .
    ?tdecl0x a java:TypeDeclaration .
    {
      ?meth0x java:inInstanceCreation/java:ofReferenceType ?tdecl0x .
    }
    UNION
    {
      ?meth0x java:inTypeDeclaration ?tdecl0x .
    }
    ?meth0x a java:MethodDeclaration ;
            java:name ?mname ;
            java:signature ?sig0 ;
            chg:removal [] .
    FILTER (?meth0x != ?meth0)
  } || EXISTS {
    ?rty1 java:refersToDeclaration ?tdecl2 .
    ?tdecl2 a java:TypeDeclaration ;
            java:fullyQualifiedName ?cfqn ;
            java:subTypeOf* ?tdecl .

    ?meth a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl ;
          java:name ?mname ;
          java:signature ?sig0 .

    FILTER (EXISTS {
      [] a java:Abstract ;
         java:inMethod ?meth .
    } || EXISTS {
      ?tdecl a java:InterfaceDeclaration .
    })
  })

}
}
''' % NS_TBL

Q_ADD_OVERRIDED_METH_ADD_SUPERTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?cfqn0_, ".", ?mname_, ?sig0_) AS ?name)
(?ctxm AS ?dep) (?meth0_ AS ?dep_)
(?ctxr AS ?ent) (?rty1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?tdecl0_ java:fullyQualifiedName ?cfqn0_ .
  {
    SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?rty1_ ?ctxr
    WHERE {

      {
        SELECT DISTINCT ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm
        WHERE {

          ?meth0_ a java:MethodDeclaration ;
                  java:name ?mname_ ;
                  java:signature ?sig0_ ;
                  chg:addition ?ctxm .

          ?tdecl0_ a java:TypeDeclaration .
          {
            ?meth0_ java:inInstanceCreation/java:ofReferenceType ?tdecl0_ .
          }
          UNION
          {
            ?meth0_ java:inTypeDeclaration ?tdecl0_ .
          }

        } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm
      }

      ?tdecl0_ java:subTypeOf* ?tdecl1_ .

      ?super1_ a java:SuperType ;
               src:parent/src:parent ?tdecl1_ .

      ?rty1_ a java:ReferenceType ;
             src:parent ?super1_ ;
             chg:addition ?ctxr .

    } GROUP BY ?meth0_ ?mname_ ?sig0_ ?tdecl0_ ?ctxm ?rty1_ ?ctxr
  }

  FILTER (NOT EXISTS {
    ?rty1_ java:refersToDeclaration [] .
  } && NOT EXISTS {
    ?tdecl0_ java:subTypeOf* ?tdecl1x_ .
    ?super1x_ a java:SuperType ;
              src:parent/src:parent ?tdecl1x_ .
    ?rty1x_ a java:ReferenceType ;
            src:parent ?super1x_ ;
            chg:addition [] .
    FILTER (?rty1x_ != ?rty1_)
  } && NOT EXISTS {
    ?tdecl0x_ java:subTypeOf* ?tdecl1_ .
    ?tdecl0x_ a java:TypeDeclaration .
    {
      ?meth0x_ java:inInstanceCreation/java:ofReferenceType ?tdecl0x_ .
    }
    UNION
    {
      ?meth0x_ java:inTypeDeclaration ?tdecl0x_ .
    }
    ?meth0x_ a java:MethodDeclaration ;
             java:name ?mname_ ;
             java:signature ?sig0_ ;
             chg:addition [] .
    FILTER (?meth0x_ != ?meth0_)
  } || EXISTS {
    ?rty1_ java:refersToDeclaration ?tdecl2_ .
    ?tdecl2_ a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn_ ;
             java:subTypeOf* ?tdecl_ .

    ?meth_ a java:MethodDeclaration ;
           java:inTypeDeclaration ?tdecl_ ;
           java:name ?mname_ ;
           java:signature ?sig0_ .

    FILTER (EXISTS {
      [] a java:Abstract ;
         java:inMethod ?meth_ .
    } || EXISTS {
      ?tdecl_ a java:InterfaceDeclaration .
    })
  })

}
}
''' % NS_TBL

Q_RM_DEFAULT_CTOR_RM_DEFAULT_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveDefaultConstructor:", ?cfqn) AS ?name)
(?ctor AS ?dep) (?ctx_ AS ?dep_)
(?ctor0 AS ?ent) (?ctx0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor0 a java:ConstructorDeclaration ;
         java:inClass ?class0 ;
         chg:removal ?ctx0_ .

  FILTER NOT EXISTS {
    ?param0 a java:Parameter ;
            src:parent ?params0 .
    ?params0 a java:Parameters ;
             src:parent ?ctor0 .
  }

  ?class java:fullyQualifiedName ?cfqn ;
         java:subClassOf ?class0 .

  ?ctor a java:ConstructorDeclaration ;
        java:inClass ?class ;
        chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?param a java:Parameter ;
           src:parent ?params .
    ?params a java:Parameters ;
            src:parent ?ctor .
  }

}
}
''' % NS_TBL

Q_ADD_DEFAULT_CTOR_ADD_DEFAULT_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddDefaultConstructor:", ?cfqn_) AS ?name)
(?ctx0 AS ?dep) (?ctor0_ AS ?dep_)
(?ctx AS ?ent) (?ctor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor0_ a java:ConstructorDeclaration ;
          java:inClass ?class0_ ;
          chg:addition ?ctx0 .

  FILTER NOT EXISTS {
    ?param0_ a java:Parameter ;
             src:parent ?params0_ .
    ?params0_ a java:Parameters ;
              src:parent ?ctor0_ .
  }

  ?class_ java:fullyQualifiedName ?cfqn_ ;
          java:subClassOf ?class0_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inClass ?class_ ;
         chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?param_ a java:Parameter ;
            src:parent ?params_ .
    ?params_ a java:Parameters ;
             src:parent ?ctor_ .
  }

}
}
''' % NS_TBL

Q_RM_FD_FINAL_ADD_INI_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?fqn) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?ctx AS ?ent) (?ini_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final ?ctx_ ?class ?class_ ?fdecl ?fqn
   WHERE {

     ?final a java:Final ;
            src:parent ?mods ;
            chg:removal ?ctx_ .

     ?fdecl a java:FieldDeclaration ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?fqn ;
            src:child0 ?mods ;
            chg:mappedTo ?fdecl_ .

     ?fdecl_ a java:FieldDeclaration ;
             java:inTypeDeclaration ?class_ .

     ?class a java:TypeDeclaration ;
            chg:mappedTo ?class_ .

     FILTER NOT EXISTS {
       [] a java:Static ;
          src:parent ?mods .
     }

    } GROUP BY ?final ?ctx_ ?class ?class_ ?fdecl ?fqn
  }

  ?vdtor a java:VariableDeclarator ;
         src:parent ?fdecl ;
         java:name ?fname ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ src:child0 ?ini_ .

  ?ini_ a java:Expression ;
        chg:addition ?ctx .

}
}
''' % NS_TBL

Q_ADD_FD_FINAL_RM_INI_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?fqn_) AS ?name)
(?ini AS ?dep) (?ctx_ AS ?dep_)
(?ctx AS ?ent) (?final_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final_ ?ctx ?class ?class_ ?fdecl_ ?fqn_
   WHERE {

     ?final_ a java:Final ;
             src:parent ?mods_ ;
             chg:addition ?ctx .

     ?fdecl a java:FieldDeclaration ;
            java:inTypeDeclaration ?class ;
            chg:mappedTo ?fdecl_ .

     ?fdecl_ a java:FieldDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             src:child0 ?mods_ .

     ?class a java:TypeDeclaration ;
            chg:mappedTo ?class_ .

     FILTER NOT EXISTS {
       [] a java:Static ;
          src:parent ?mods_ .
     }

    } GROUP BY ?final_ ?ctx ?class ?class_ ?fdecl_ ?fqn_
  }

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?fdecl_ ;
          java:name ?fname_ ;
          ^chg:mappedTo ?vdtor .

  ?vdtor src:child0 ?ini .

  ?ini a java:Expression ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_RM_FIELD_ADD_FIELD_MOV_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("MoveField:", ?fqn) AS ?name)
(?fdecl AS ?key) (?ctx_ AS ?key_)
(?ctx AS ?ent) (?fdecl_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?class ?class_ ?fdecl ?fdecl_ ?fqn ?fqn_
    WHERE {

     ?fdecl a java:FieldDeclaration ;
            java:inTypeDeclaration ?class ;
            java:fullyQualifiedName ?fqn ;
            src:child0 ?mods ;
            chg:movedTo ?fdecl_ .

     ?fdecl_ a java:FieldDeclaration ;
             java:inTypeDeclaration ?class_ ;
             java:fullyQualifiedName ?fqn_ ;
             src:child0 ?mods_ .

     ?class a java:TypeDeclaration ;
            chg:mappedStablyTo ?class_ .

    } GROUP BY ?class ?class_ ?fdecl ?fdecl_ ?fqn ?fqn_
  }

  ?vdtor a java:VariableDeclarator ;
         src:parent ?fdecl ;
         java:name ?fname ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?fdecl_ ;
          java:name ?fname .

  ?fdecl chg:genRemoved ?ctx_ .
  ?fdecl_ chg:genAdded ?ctx .

}
}
''' % NS_TBL

Q_CHG_MOD_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeModifier:", ?mfqn0, ".", "?msig0") AS ?name)
(?meth0 AS ?dep) (?ctx0_ AS ?dep_)
(?mod0 AS ?ent) (?mod0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname ?class ?mod0 ?mod0_
    ?meth0 ?ctx0_ ?mfqn0 ?msig0
    WHERE {

      {
        SELECT DISTINCT ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
        WHERE {

          ?meth a java:MethodDeclaration ;
                java:name ?mname ;
                java:signature ?msig ;
                java:fullyQualifiedName ?mfqn ;
                java:inTypeDeclaration ?tdecl ;
                chg:removal ?ctx_ .

          FILTER (EXISTS {
            ?meth src:child0 ?mods .
            [] a java:Abstract ;
               src:parent ?mods .
          } || EXISTS {
            ?tdecl a java:InterfaceDeclaration .
          })

        } GROUP BY ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname
      }

      ?class a java:TypeDeclaration ;
             java:name ?cname ;
             java:subTypeOf* ?tdecl .

      ?meth0 a java:MethodDeclaration ;
             src:child5 [] ;
             java:name ?mname ;
             java:fullyQualifiedName ?mfqn0 ;
             java:signature ?msig0 ;
             src:child0 ?mods0 ;
             chg:removal ?ctx0_ .

      ?mod0 a java:AccessModifier ;
            a ?mcat0 OPTION (INFERENCE NONE) ;
            src:parent ?mods0 ;
            chg:relabeled ?mod0_ .

      ?mod0_ a java:AccessModifier ;
             a ?mcat0_ OPTION (INFERENCE NONE) .

      FILTER (?mcat0_ = java:Private)

      FILTER (EXISTS {
        ?meth0 java:inClass ?class .
      } || EXISTS {
        ?meth0 java:inInstanceCreation/java:ofReferenceType ?class .
      })

    } GROUP BY ?meth ?ctx_ ?mfqn ?msig ?mname ?tdecl ?tdecl_ ?tname ?class ?mod0 ?mod0_
    ?meth0 ?ctx0_ ?mfqn0  ?msig0
  }

  FILTER NOT EXISTS {
    ?tdecl a [] .
    ?class java:subClassOf+ ?c .
    ?c a java:ClassDeclaration ;
       java:subClassOf+ ?tdecl .
    [] a java:MethodDeclaration ;
       src:child5 [] ;
       java:inClass ?c ;
       java:name ?mname .
  }

}
}
''' % NS_TBL

Q_CHG_MOD_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeModifier:", ?mfqn0_, ".", "?msig0_") AS ?name)
(?mod0 AS ?dep) (?mod0_ AS ?dep_)
(?ctx0 AS ?ent) (?meth0_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?ctx ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_ ?class_
    ?mod0 ?mod0_ ?meth0_ ?ctx0 ?mfqn0_ ?msig0_
    WHERE {

      {
        SELECT DISTINCT ?meth_ ?ctx ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
        WHERE {

          ?meth_ a java:MethodDeclaration ;
                 java:name ?mname_ ;
                 java:signature ?msig_ ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:inTypeDeclaration ?tdecl_ ;
                 chg:addition ?ctx .

          FILTER (EXISTS {
            ?meth_ src:child0 ?mods_ .
            [] a java:Abstract ;
               src:parent ?mods_ .
          } || EXISTS {
            ?tdecl_ a java:InterfaceDeclaration .
          })

        } GROUP BY ?meth_ ?ctx ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_
      }

      ?class_ a java:TypeDeclaration ;
              java:name ?cname_ ;
              java:subTypeOf* ?tdecl_ .

      ?meth0_ a java:MethodDeclaration ;
              src:child5 [] ;
              java:name ?mname_ ;
              java:fullyQualifiedName ?mfqn0_ ;
              java:signature ?msig0_ ;
              src:child0 ?mods0_ ;
              chg:addition ?ctx0 .

      ?mod0_ a java:AccessModifier ;
             a ?mcat0_ OPTION (INFERENCE NONE) ;
             src:parent ?mods0_ ;
             ^chg:relabeled ?mod0 .

      ?mod0 a java:AccessModifier ;
            a ?mcat0 OPTION (INFERENCE NONE) .

      FILTER (?mcat0 = java:Private)

      FILTER (EXISTS {
        ?meth0_ java:inClass ?class_ .
      } || EXISTS {
        ?meth0_ java:inInstanceCreation/java:ofReferenceType ?class_ .
      })

    } GROUP BY ?meth_ ?ctx ?mfqn_ ?msig_ ?mname_ ?tdecl ?tdecl_ ?tname_ ?class_
    ?mod0 ?mod0_ ?meth0_ ?ctx0 ?mfqn0_ ?msig0_
  }

  FILTER NOT EXISTS {
    ?tdecl_ a [] .
    ?class_ java:subClassOf+ ?c_ .
    ?c_ a java:ClassDeclaration ;
        java:subClassOf+ ?tdecl_ .
    [] a java:MethodDeclaration ;
       src:child5 [] ;
       java:inClass ?c_ ;
       java:name ?mname_ .
  }

}
}
''' % NS_TBL

Q_ADD_LVD_FINAL_RM_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?mfqn_, ?msig_, ":", ?vname) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?ctx AS ?ent) (?final_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final_ ?ctx ?meth ?meth_ ?class ?class_ ?vdecl ?vdecl_ ?mfqn_ ?msig_
    WHERE {

      ?final_ a java:Final ;
              src:parent ?mods_ ;
              chg:addition ?ctx .

      ?vdecl a ?vcat OPTION (INFERENCE NONE) ;
             java:inMethodOrConstructor ?meth ;
             chg:mappedTo ?vdecl_ .

      ?meth a java:MethodOrConstructor ;
            java:inTypeDeclaration ?class .

      ?vdecl_ a ?vcat_ OPTION (INFERENCE NONE) ;
              java:inMethodOrConstructor ?meth_ ;
              src:child0 ?mods_ .

      ?meth_ a java:MethodOrConstructor ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             java:inTypeDeclaration ?class_ .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER (?vcat IN (java:LocalVariableDeclarationStatement,java:LocalVariableDeclaration))
      FILTER (?vcat_ IN (java:LocalVariableDeclarationStatement,java:LocalVariableDeclaration))

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent ?mods_ .
      }

    } GROUP BY ?final_ ?ctx ?meth ?meth_ ?class ?class_ ?vdecl ?vdecl_ ?mfqn_ ?msig_
  }

  ?vdtor a java:VariableDeclarator ;
         src:parent ?vdecl ;
         java:name ?vname .

  ?assign a ?cat OPTION (INFERENCE NONE) ;
          java:inMethodOrConstructor ?meth ;
          src:child0 ?x .

  FILTER (?cat IN (java:Assign,java:AssignStatement))

  ?x java:name ?vname ;
     java:declaredBy ?vdtor ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_RM_LVD_FINAL_ADD_ASSIGN_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?mfqn, ?msig, ":", ?vname_) AS ?name)
(?final AS ?dep) (?ctx_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?final ?ctx_ ?meth ?meth_ ?class ?class_ ?vdecl ?vdecl_ ?mfqn ?msig
    WHERE {

      ?final a java:Final ;
             src:parent ?mods ;
             chg:removal ?ctx_ .

      ?vdecl a ?vcat OPTION (INFERENCE NONE) ;
             java:inMethodOrConstructor ?meth ;
             src:child0 ?mods ;
             chg:mappedTo ?vdecl_ .

      ?vdecl_ a ?vcat_ OPTION (INFERENCE NONE) ;
              java:inMethodOrConstructor ?meth_ .

      ?meth a java:MethodOrConstructor ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            java:inTypeDeclaration ?class .

      ?meth_ a java:MethodOrConstructor ;
             java:inTypeDeclaration ?class_ .

      ?class a java:TypeDeclaration ;
             chg:mappedTo ?class_ .

      FILTER (?vcat IN (java:LocalVariableDeclarationStatement,java:LocalVariableDeclaration))
      FILTER (?vcat_ IN (java:LocalVariableDeclarationStatement,java:LocalVariableDeclaration))

      FILTER NOT EXISTS {
        [] a java:Static ;
           src:parent ?mods .
      }

    } GROUP BY ?final ?ctx_ ?meth ?meth_ ?class ?class_ ?vdecl ?vdecl_ ?mfqn ?msig
  }

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?vdecl_ ;
          java:name ?vname_ .

  ?assign_ a ?cat_ OPTION (INFERENCE NONE) ;
           java:inMethodOrConstructor ?meth_ ;
           src:child0 ?x_ .

  FILTER (?cat_ IN (java:Assign,java:AssignStatement))

  ?x_ java:name ?vname_ ;
      java:declaredBy ?vdtor_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_RM_EXTENDS_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("RemoveExtends:", ?cfqn) AS ?name)
(?ctx AS ?dep) (?meth_ AS ?dep_)
(?ety AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety ?ctx_ ?meth_ ?ctx ?mname ?ecfqn
    WHERE {

      {
        SELECT DISTINCT ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety ?ctx_ ?ecfqn
        WHERE {

          ?tdecl a java:TypeDeclaration ;
                 java:fullyQualifiedName ?cfqn ;
                 chg:mappedTo ?tdecl_ .

          ?tdecl_ a java:TypeDeclaration ;
                  java:fullyQualifiedName ?cfqn_ .

          ?extends a java:Extends ;
                   java:inTypeDeclaration ?tdecl .

          ?ety a java:ReferenceType ;
               java:name ?ecfqn ;
               src:parent ?extends ;
               chg:removal ?ctx_ .

        } GROUP BY ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety ?ctx_ ?ecfqn
      }

      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:name ?mname ;
             src:child5 [] ;
             chg:addition ?ctx .

    } GROUP BY ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety ?ctx_ ?meth_ ?ctx ?mname ?ecfqn
  }

  FILTER NOT EXISTS {
    ?meth a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl ;
          java:name ?mname .
  }

  FILTER EXISTS {
    ?tdecl java:subTypeOf+ ?etdecl0 .

    ?etdecl0 a java:TypeDeclaration ;
             java:fullyQualifiedName ?ecfqn0 .

    ?meth0 a java:MethodDeclaration ;
           java:inTypeDeclaration ?etdecl0 ;
           java:name ?mname ;
           src:child5 [] .
  }

  FILTER EXISTS {
    ?tdecl java:subTypeOf+ ?itdecl .

    ?itdecl a java:TypeDeclaration ;
            java:fullyQualifiedName ?icfqn .

    ?imeth a java:MethodDeclaration ;
           java:inTypeDeclaration ?itdecl ;
           java:name ?mname .

    FILTER (EXISTS {
      [] a java:Abstract ;
         java:inMethod ?imeth .
    } || EXISTS {
      ?itdecl a java:InterfaceDeclaration .
    })
  }

  FILTER EXISTS {
    ?tdecl_ java:subTypeOf+ ?itdecl_ .

    ?itdecl_ a java:TypeDeclaration ;
             java:fullyQualifiedName ?icfqn_ .

    ?imeth_ a java:MethodDeclaration ;
            java:inTypeDeclaration ?itdecl_ ;
            java:name ?mname .

    FILTER (EXISTS {
      [] a java:Abstract ;
         java:inMethod ?imeth_ .
    } || EXISTS {
      ?itdecl_ a java:InterfaceDeclaration .
    })
  }

}
}
''' % NS_TBL

Q_ADD_EXTENDS_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX jref: <%(jref_ns)s>
SELECT DISTINCT
(CONCAT("AddExtends:", ?cfqn_) AS ?name)
(?ctx AS ?dep) (?ety_ AS ?dep_)
(?meth AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety_ ?ctx ?meth ?ctx_ ?mname ?ecfqn_
    WHERE {

      {
        SELECT DISTINCT ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety_ ?ctx ?ecfqn_
        WHERE {

          ?tdecl a java:TypeDeclaration ;
                 java:fullyQualifiedName ?cfqn ;
                 chg:mappedTo ?tdecl_ .

          ?tdecl_ a java:TypeDeclaration ;
                  java:fullyQualifiedName ?cfqn_ .

          ?extends_ a java:Extends ;
                    java:inTypeDeclaration ?tdecl_ .

          ?ety_ a java:ReferenceType ;
                java:name ?ecfqn_ ;
                src:parent ?extends_ ;
                chg:addition ?ctx .

        } GROUP BY ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety_ ?ctx ?ecfqn_
      }

      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
             java:name ?mname ;
             src:child5 [] ;
             chg:removal ?ctx_ .

    } GROUP BY ?tdecl ?tdecl_ ?cfqn ?cfqn_ ?ety_ ?ctx ?meth ?ctx_ ?mname ?ecfqn_
  }

  FILTER NOT EXISTS {
    ?meth_ a java:MethodDeclaration ;
           java:inTypeDeclaration ?tdecl_ ;
           java:name ?mname .
  }

  FILTER EXISTS {
    ?tdecl_ java:subTypeOf+ ?etdecl0_ .

    ?etdecl0_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?ecfqn0_ .

    ?meth0_ a java:MethodDeclaration ;
            java:inTypeDeclaration ?etdecl0_ ;
            java:name ?mname ;
            src:child5 [] .
  }

  FILTER EXISTS {
    ?tdecl java:subTypeOf+ ?itdecl .

    ?itdecl a java:TypeDeclaration ;
            java:fullyQualifiedName ?icfqn .

    ?imeth a java:MethodDeclaration ;
           java:inTypeDeclaration ?itdecl ;
           java:name ?mname .

    FILTER (EXISTS {
      [] a java:Abstract ;
         java:inMethod ?imeth .
    } || EXISTS {
      ?itdecl a java:InterfaceDeclaration .
    })
  }

  FILTER EXISTS {
    ?tdecl_ java:subTypeOf+ ?itdecl_ .

    ?itdecl_ a java:TypeDeclaration ;
             java:fullyQualifiedName ?icfqn_ .

    ?imeth_ a java:MethodDeclaration ;
            java:inTypeDeclaration ?itdecl_ ;
            java:name ?mname .

    FILTER (EXISTS {
      [] a java:Abstract ;
         java:inMethod ?imeth_ .
    } || EXISTS {
      ?itdecl_ a java:InterfaceDeclaration .
    })
  }

}
}
''' % NS_TBL

Q_RM_FD_FINAL_RM_FD_STATIC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveFinal:", ?fqn) AS ?name)
(?static AS ?dep) (?ctx0_ AS ?dep_)
(?final AS ?ent) (?ctx1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?static a java:Static ;
          src:parent ?mods ;
          chg:removal ?ctx0_ .

  ?final a java:Final ;
         src:parent ?mods ;
         chg:removal ?ctx1_ .

  ?fdecl a java:FieldDeclaration ;
         src:parent ?cbody ;
         java:fullyQualifiedName ?fqn ;
         src:child0 ?mods .

  ?cbody a ?cat OPTION(INFERENCE NONE) ;
         java:inTypeDeclaration [] .

  FILTER (?cat IN (java:ClassBody,java:InterfaceBody))

}
}
''' % NS_TBL

Q_ADD_FD_FINAL_ADD_FD_STATIC_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddFinal:", ?fqn_) AS ?name)
(?ctx1 AS ?dep) (?final_ AS ?dep_)
(?ctx0 AS ?ent) (?static_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?static_ a java:Static ;
           src:parent ?mods_ ;
           chg:addition ?ctx0 .

  ?final_ a java:Final ;
          src:parent ?mods_ ;
          chg:addition ?ctx1 .

  ?fdecl_ a java:FieldDeclaration ;
          src:parent ?cbody_ ;
          java:fullyQualifiedName ?fqn_ ;
          src:child0 ?mods_ .

  ?cbody_ a ?cat_ OPTION(INFERENCE NONE) ;
          java:inTypeDeclaration [] .

  FILTER (?cat_ IN (java:ClassBody,java:InterfaceBody))

}
}
''' % NS_TBL

Q_RM_CTOR_BODY_RM_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveBody:", ?cfqn) AS ?name)
(?ctor AS ?dep) (?ctxc_ AS ?dep_)
(?x AS ?ent) (?ctxx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:signature ?csig ;
        java:fullyQualifiedName ?cfqn ;
        src:child4 ?body ;
        chg:removal ?ctxc_  .

  ?x src:parent ?body ;
     chg:removal ?ctxx_ .

  FILTER NOT EXISTS {
    ?x0 src:parent ?body .
    FILTER (?x0 != ?x)
  }

  FILTER NOT EXISTS {
    ?tdecl java:subTypeOf+ ?tdecl0 .

    ?ctor0 a java:ConstructorDeclaration ;
           java:inTypeDeclaration ?tdecl0 ;
           java:signature "()V" .
  }

}
}
''' % NS_TBL

Q_ADD_CTOR_BODY_ADD_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddBody:", ?cfqn_) AS ?name)
(?ctxx AS ?dep) (?x_ AS ?dep_)
(?ctxc AS ?ent) (?ctor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:signature ?csig_ ;
         java:fullyQualifiedName ?cfqn_ ;
         src:child4 ?body_ ;
         chg:addition ?ctxc  .

  ?x_ src:parent ?body_ ;
      chg:addition ?ctxx .

  FILTER NOT EXISTS {
    ?x0_ src:parent ?body_ .
    FILTER (?x0_ != ?x_)
  }

  FILTER NOT EXISTS {
    ?tdecl_ java:subTypeOf+ ?tdecl0_ .

    ?ctor0_ a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?tdecl0_ ;
            java:signature "()V" .
  }

}
}
''' % NS_TBL

Q_RM_FIELD_INI_ADD_FIELD_INI_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("MoveFieldInit:", ?cfqn) AS ?name)
(?ctx AS ?dep) (?assign_ AS ?dep_)
(?assign AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?assign ?ctx_ ?x ?fname ?tdecl ?ctor ?cfqn ?csig ?tdecl_
    WHERE {

      {
        SELECT DISTINCT ?assign ?ctx_ ?x ?fname ?tdecl ?ctor ?cfqn ?csig
        WHERE {

          {
            SELECT DISTINCT ?assign ?ctx_ ?x ?fname ?tdecl ?ctor ?cfqn ?csig
            WHERE {

              ?assign a ?cat OPTION (INFERENCE NONE) ;
                      java:inConstructor ?ctor ;
                      src:child0 ?x ;
                      chg:removal ?ctx_ .

              FILTER (?cat IN (java:Assign,java:AssignStatement))

              ?ctor a java:ConstructorDeclaration ;
                    java:inTypeDeclaration ?tdecl ;
                    java:signature ?csig ;
                    java:fullyQualifiedName ?cfqn ;
                    src:child4 ?body .

              ?x a java:FieldAccess ;
                 java:name ?fname .

            } GROUP BY ?assign ?ctx_ ?x ?fname ?tdecl ?ctor ?cfqn ?csig
          }

          FILTER (EXISTS {
            [] a java:This ;
               src:parent ?x .
          } || NOT EXISTS {
            [] src:parent ?x .
          })

          FILTER NOT EXISTS {
            ?assign0 a ?cat0 OPTION (INFERENCE NONE) ;
                     java:inConstructor ?ctor ;
                     src:child0 [ a java:FieldAccess; java:name ?fname ] .
            FILTER (?assign0 != ?assign)
          }

        } GROUP BY ?assign ?ctx_ ?x ?fname ?tdecl ?ctor ?cfqn ?csig
      }

      ?tdecl chg:mappedTo ?tdecl_ .
      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ .

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname .

    } GROUP BY ?assign ?ctx_ ?x ?fname ?tdecl ?ctor ?cfqn ?csig ?tdecl_
  }

  {
    SELECT DISTINCT ?assign_ ?ctx ?x_ ?fname ?tdecl_ ?ctor_ ?cfqn_ ?csig_
    WHERE {

      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:signature ?csig_ ;
             java:fullyQualifiedName ?cfqn_ ;
             src:child4 ?body_ .

      ?assign_ a ?cat_ OPTION (INFERENCE NONE) ;
               java:inConstructor ?ctor_ ;
               src:child0 ?x_ ;
               chg:addition ?ctx .

      FILTER (?cat_ IN (java:Assign,java:AssignStatement))

      ?x_ a java:FieldAccess ;
          java:name ?fname .

    } GROUP BY ?assign_ ?ctx ?x_ ?fname ?tdecl_ ?ctor_ ?cfqn_ ?csig_
  }

  FILTER NOT EXISTS {
    ?assign0_ a ?cat0 OPTION (INFERENCE NONE) ;
              java:inConstructor ?ctor_ ;
              src:child0 [ a java:FieldAccess; java:name ?fname ] .
    FILTER (?assign0_ != ?assign_)
  }

  FILTER (EXISTS {
    [] a java:This ;
       src:parent ?x_ .
  } || NOT EXISTS {
    [] src:parent ?x_ .
  })

}
}
''' % NS_TBL

Q_RM_RET_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveReturn:", ?mfqn) AS ?name)
(?meth AS ?dep) (?ctxm_ AS ?dep_)
(?ret AS ?ent) (?ctxr_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth a java:MethodDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:fullyQualifiedName ?mfqn ;
        src:child2 ?retty ;
        src:child5 ?body ;
        chg:removal ?ctxm_ .

  ?ret a java:ReturnStatement ;
       src:parent ?body ;
       chg:removal ?ctxr_ .

  ?tdecl chg:mappedTo ?tdecl_ .

  FILTER NOT EXISTS {
    ?retty a java:Void .
  }

  FILTER NOT EXISTS {
    ?ret0 a java:ReturnStatement ;
          src:parent ?body .
    FILTER (?ret0 != ?ret)
  }

  FILTER EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?ret .
  }

}
}
''' % NS_TBL

Q_ADD_RET_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddReturn:", ?mfqn_) AS ?name)
(?ctxr AS ?dep) (?ret_ AS ?dep_)
(?ctxm AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?meth_ a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:fullyQualifiedName ?mfqn_ ;
         src:child2 ?retty_ ;
         src:child5 ?body_ ;
         chg:addition ?ctxm .

  ?ret_ a java:ReturnStatement ;
        src:parent ?body_ ;
        chg:addition ?ctxr .

  ?tdecl chg:mappedTo ?tdecl_ .

  FILTER NOT EXISTS {
    ?retty_ a java:Void .
  }

  FILTER NOT EXISTS {
    ?ret0_ a java:ReturnStatement ;
           src:parent ?body_ .
    FILTER (?ret0_ != ?ret_)
  }

  FILTER EXISTS {
    [] a chg:Insertion ;
       delta:entity2 ?ret_ .
  }

}
}
''' % NS_TBL

Q_RM_ASSIGN_RM_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?tfqn, ".", ?fname) AS ?name)
(?vdtor AS ?dep) (?ctx_ AS ?dep_)
(?assign AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         src:parent ?fdecl ;
         java:name ?fname ;
         chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?vdtor src:child0 [] .
  }

  ?fdecl a java:FieldDeclaration ;
         java:inTypeDeclaration ?tdecl .

  ?tdecl a java:TypeDeclaration ;
         java:fullyQualifiedName ?tfqn ;
         chg:mappedTo ?tdecl_ .

  {
    SELECT DISTINCT ?tdecl ?fname (COUNT(DISTINCT ?ctor) AS ?n)
    (SAMPLE(?assign0) AS ?assign)
    WHERE {
      ?ctor a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?cfqn .

      ?assign0 a ?cat OPTION (INFERENCE NONE) ;
               java:inConstructor ?ctor ;
               src:child0 ?x .

      FILTER (?cat IN (java:Assign,java:AssignStatement))

      ?x a java:FieldAccess ;
         java:name ?fname .

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x .
      } || NOT EXISTS {
        [] src:parent ?x .
      })

    } GROUP BY ?tdecl ?fname
  }

  FILTER (?n = 1)

  ?assign chg:removal ?ctxa_ .

}
}
''' % NS_TBL

Q_RM_ASSIGN_RM_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAssign:", ?cfqn, ?csig, ".", ?fname) AS ?name)
(?ctor AS ?dep) (?ctx_ AS ?dep_)
(?assign AS ?ent) (?ctxa_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctor ?ctx_ ?fname ?tfqn ?cfqn ?csig
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname .

      FILTER NOT EXISTS {
        ?vdtor src:child0 [] .
      }

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?tfqn ;
             chg:mappedTo ?tdecl_ .

      ?ctor a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?cfqn ;
            java:signature ?csig ;
            src:child4 ?body ;
            chg:removal ?ctx_ .

    } GROUP BY ?ctor ?ctx_ ?fname ?tfqn ?cfqn ?csig
  }

  {
    SELECT DISTINCT ?ctor ?fname (COUNT(DISTINCT ?assign0) AS ?n)
    (SAMPLE(?assign0) AS ?assign)
    WHERE {
      ?assign0 a ?cat OPTION (INFERENCE NONE) ;
               java:inConstructor ?ctor ;
               src:child0 ?x .

      FILTER (?cat IN (java:Assign,java:AssignStatement))

      ?x a java:FieldAccess ;
         java:name ?fname .

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x .
      } || NOT EXISTS {
        [] src:parent ?x .
      })

    } GROUP BY ?ctor ?fname
  }

  FILTER (?n = 1)

  ?assign chg:removal ?ctxa_ .

}
}
''' % NS_TBL

Q_ADD_ASSIGN_ADD_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddAssign:", ?cfqn_, ?csig_, ".", ?fname_) AS ?name)
(?ctxa AS ?dep) (?assign_ AS ?dep_)
(?ctx AS ?ent) (?ctor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ctor_ ?ctx ?fname_ ?tfqn_ ?cfqn_ ?csig_
    WHERE {

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname_ .

      FILTER NOT EXISTS {
        ?vdtor_ src:child0 [] .
      }

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?tfqn_ ;
              ^chg:mappedTo ?tdecl .

      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?cfqn_ ;
             java:signature ?csig_ ;
             src:child4 ?body_ ;
             chg:addition ?ctx .

    } GROUP BY ?ctor_ ?ctx ?fname_ ?tfqn_ ?cfqn_ ?csig_
  }

  {
    SELECT DISTINCT ?ctor_ ?fname_ (COUNT(DISTINCT ?assign0_) AS ?n)
    (SAMPLE(?assign0_) AS ?assign_)
    WHERE {
      ?assign0_ a ?cat_ OPTION (INFERENCE NONE) ;
                java:inConstructor ?ctor_ ;
                src:child0 ?x_ .

      FILTER (?cat_ IN (java:Assign,java:AssignStatement))

      ?x_ a java:FieldAccess ;
         java:name ?fname_ .

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x_ .
      } || NOT EXISTS {
        [] src:parent ?x_ .
      })

    } GROUP BY ?ctor_ ?fname_
  }

  FILTER (?n = 1)

  ?assign_ chg:addition ?ctxa .

}
}
''' % NS_TBL

Q_CHG_LHS_RM_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveField:", ?tfqn, ".", ?fname) AS ?name)
(?vdtor AS ?dep) (?ctx_ AS ?dep_)
(?lhs AS ?ent) (?lhs_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         src:parent ?fdecl ;
         java:name ?fname ;
         chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?vdtor src:child0 [] .
  }

  ?fdecl a java:FieldDeclaration ;
         java:inTypeDeclaration ?tdecl .

  ?tdecl a java:TypeDeclaration ;
         java:fullyQualifiedName ?tfqn ;
         chg:mappedTo ?tdecl_ .

  {
    SELECT DISTINCT ?tdecl ?fname (COUNT(DISTINCT ?ctor) AS ?n)
    (SAMPLE(?assign0) AS ?assign)
    WHERE {
      ?ctor a java:ConstructorDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?cfqn .

      ?assign0 a ?cat OPTION (INFERENCE NONE) ;
               java:inConstructor ?ctor ;
               src:child0 ?x .

      FILTER (?cat IN (java:Assign,java:AssignStatement))

      ?x a java:FieldAccess ;
         java:name ?fname .

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x .
      } || NOT EXISTS {
        [] src:parent ?x .
      })

    } GROUP BY ?tdecl ?fname
  }

  FILTER (?n = 1)

  ?assign src:child0 ?lhs ;
          chg:mappedTo ?assign_ .

  ?lhs java:declaredBy ?dtor ;
       chg:relabeled ?lhs_ .

}
}
''' % NS_TBL

Q_ADD_ASSIGN_ADD_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddField:", ?tfqn_, ".", ?fname_) AS ?name)
(?ctxa AS ?dep) (?assign_ AS ?dep_)
(?ctx AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?fdecl_ ;
          java:name ?fname_ ;
          chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?vdtor_ src:child0 [] .
  }

  ?fdecl_ a java:FieldDeclaration ;
          java:inTypeDeclaration ?tdecl_ .

  ?tdecl_ a java:TypeDeclaration ;
          java:fullyQualifiedName ?tfqn_ ;
          ^chg:mappedTo ?tdecl .

  {
    SELECT DISTINCT ?tdecl_ ?fname_ (COUNT(DISTINCT ?ctor_) AS ?n)
    (SAMPLE(?assign0_) AS ?assign_)
    WHERE {
      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?cfqn_ .

      ?assign0_ a ?cat_ OPTION (INFERENCE NONE) ;
                java:inConstructor ?ctor_ ;
                src:child0 ?x_ .

      FILTER (?cat_ IN (java:Assign,java:AssignStatement))

      ?x_ a java:FieldAccess ;
          java:name ?fname_ .

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x_ .
      } || NOT EXISTS {
        [] src:parent ?x_ .
      })

    } GROUP BY ?tdecl_ ?fname_
  }

  FILTER (?n = 1)

  ?assign_ chg:addition ?ctxa .

}
}
''' % NS_TBL

Q_CHG_LHS_ADD_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddField:", ?tfqn_, ".", ?fname_) AS ?name)
(?lhs AS ?dep) (?lhs_ AS ?dep_)
(?ctx AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?fdecl_ ;
          java:name ?fname_ ;
          chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?vdtor_ src:child0 [] .
  }

  ?fdecl_ a java:FieldDeclaration ;
          java:inTypeDeclaration ?tdecl_ .

  ?tdecl_ a java:TypeDeclaration ;
          java:fullyQualifiedName ?tfqn_ ;
          ^chg:mappedTo ?tdecl .

  {
    SELECT DISTINCT ?tdecl_ ?fname_ (COUNT(DISTINCT ?ctor_) AS ?n)
    (SAMPLE(?assign0_) AS ?assign_)
    WHERE {
      ?ctor_ a java:ConstructorDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?cfqn_ .

      ?assign0_ a ?cat_ OPTION (INFERENCE NONE) ;
                java:inConstructor ?ctor_ ;
                src:child0 ?x_ .

      FILTER (?cat_ IN (java:Assign,java:AssignStatement))

      ?x_ a java:FieldAccess ;
          java:name ?fname_ .

      FILTER (EXISTS {
        [] a java:This ;
           src:parent ?x_ .
      } || NOT EXISTS {
        [] src:parent ?x_ .
      })

    } GROUP BY ?tdecl_ ?fname_
  }

  FILTER (?n = 1)

  ?assign_ src:child0 ?lhs_ ;
           ^chg:mappedTo ?assign .

  ?lhs_ java:declaredBy ?dtor_ ;
        ^chg:relabeled ?lhs .

}
}
''' % NS_TBL

Q_RM_THIS_IVK_RM_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThisInvocation:", ?cfqn) AS ?name)
(?ctor AS ?dep) (?ctx_ AS ?dep_)
(?ivk AS ?ent) (?ctxi_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         src:parent ?fdecl ;
         java:name ?fname .

  FILTER NOT EXISTS {
    ?vdtor src:child0 [] .
  }

  ?fdecl a java:FieldDeclaration ;
         java:inTypeDeclaration ?tdecl .

  ?tdecl a java:TypeDeclaration ;
         java:fullyQualifiedName ?tfqn ;
         chg:mappedTo ?tdecl_ .

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:fullyQualifiedName ?cfqn ;
        src:child4 ?body ;
        chg:removal ?ctx_ .

  ?ivk a java:ThisInvocation ;
       src:parent ?body ;
       chg:removal ?ctxi_ .

  FILTER NOT EXISTS {
    ?x src:parent ?body .
    FILTER (?x != ?ivk)
  }

  FILTER EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?ivk .
  }

  FILTER NOT EXISTS {
    ?y src:parent+ ?ivk ;
       chg:mappedStablyTo [] .
  }

}
}
''' % NS_TBL

Q_ADD_THIS_IVK_ADD_CTOR_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThisInvocation:", ?cfqn_) AS ?name)
(?ctxi AS ?dep) (?ivk_ AS ?dep_)
(?ctx AS ?ent) (?ctor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?fdecl_ ;
          java:name ?fname_ .

  FILTER NOT EXISTS {
    ?vdtor_ src:child0 [] .
  }

  ?fdecl_ a java:FieldDeclaration ;
          java:inTypeDeclaration ?tdecl_ .

  ?tdecl a java:TypeDeclaration ;
         java:fullyQualifiedName ?tfqn ;
         chg:mappedTo ?tdecl_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:fullyQualifiedName ?cfqn_ ;
         src:child4 ?body_ ;
         chg:addition ?ctx .

  ?ivk_ a java:ThisInvocation ;
        src:parent ?body_ ;
        chg:addition ?ctxi .

  FILTER NOT EXISTS {
    ?x_ src:parent ?body_ .
    FILTER (?x_ != ?ivk_)
  }

  FILTER EXISTS {
    [] a chg:Insertion ;
       delta:entity2 ?ivk_ .
  }

  FILTER NOT EXISTS {
    ?y_ src:parent+ ?ivk_ ;
        ^chg:mappedStablyTo [] .
  }

}
}
''' % NS_TBL

Q_CHG_FD_TY_RM_FACC_CTX_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFType:", ?fqn, ".", ?fname) AS ?name)
(?x AS ?key) (?ctx_ AS ?key_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn
  }

  ?facc a java:FieldAccess ;
        java:name ?fname ;
        java:inMethodOrConstructor ?meth ;
        src:parent ?x ;
        chg:mappedTo ?facc_ .

  ?facc_ a java:FieldAccess ;
         java:name ?fname_ ;
         java:inMethodOrConstructor ?meth_ ;
         java:inTypeDeclaration ?tdecl_ .

  ?meth chg:mappedTo ?meth_ .

  ?x a ?cat OPTION(INFERENCE NONE) ;
     chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_FD_TY_ADD_FACC_CTX_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFType:", ?fqn, ".", ?fname) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn
    WHERE {

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             src:child1 ?ty ;
             src:child2 ?vdtor ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ ;
              src:child1 ?ty_ ;
              src:child2 ?vdtor_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?fqn ;
             chg:mappedTo ?tdecl_ .

      ?ty a java:Type ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?fname ;
             chg:mappedTo ?vdtor_ .

      ?vdtor_ a java:VariableDeclarator ;
              java:name ?fname_ .

    } GROUP BY ?fname ?fname_ ?ty ?ty_ ?tdecl ?tdecl_ ?fqn
  }

  ?facc a java:FieldAccess ;
        java:name ?fname ;
        java:inMethodOrConstructor ?meth ;
        chg:mappedTo ?facc_ .

  ?facc_ a java:FieldAccess ;
         java:name ?fname_ ;
         src:parent ?x_ ;
         java:inMethodOrConstructor ?meth_ ;
         java:inTypeDeclaration ?tdecl_ .

  ?meth chg:mappedTo ?meth_ .

  ?x_ a ?cat_ OPTION(INFERENCE NONE) ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_MOV_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(?x AS ?dep) (?ctx_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x chg:movedTo ?x_ ;
     chg:relabeled ?x_ .
  ?x chg:genRemoved ?ctx_ .
  ?x_ chg:genAdded ?ctx .

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }

}
}
''' % NS_TBL

Q_MOV_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(?ctx AS ?dep) (?x_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x chg:movedTo ?x_ ;
     chg:relabeled ?x_ .
  ?x chg:genRemoved ?ctx_ .
  ?x_ chg:genAdded ?ctx .

  FILTER EXISTS {
    [] a chg:Move ;
       delta:entity1 ?x ;
       delta:entity2 ?x_ .
  }

}
}
''' % NS_TBL

Q_RM_METH_ADD_METH_3_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?mfqn, ?msig) AS ?name)
(?meth AS ?dep) (?cbody_ AS ?dep_)
(?cbody AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?mfqn ?msig ?cbody ?cbody_ ?mbody
    WHERE {

      ?meth a java:MethodDeclaration ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            src:parent ?cbody ;
            src:child5 ?mbody ;
            chg:removal ?cbody_ .

      ?cbody a java:ClassBody ;
             chg:mappedTo ?cbody_ .

      ?mbody a java:MethodBody ;
             src:parent ?meth ;
             chg:removal ?cbody_ .

    } GROUP BY ?meth ?mfqn ?msig ?cbody ?cbody_ ?mbody
  }

  ?meth_ a java:MethodDeclaration ;
         java:fullyQualifiedName ?mfqn_ ;
         src:parent ?cbody_ ;
         chg:addition ?cbody .

  ?s0 a java:BlockStatement ;
      src:parent ?mbody ;
      chg:mappedStablyTo ?s0_ .

  ?s0_ a java:BlockStatement ;
       java:inMethod ?m0_ .

  ?m0_ java:name ?mn0_ .

  ?s1 a java:BlockStatement ;
      src:parent ?mbody ;
      chg:mappedStablyTo ?s1_ .

  ?s1_ a java:BlockStatement ;
       java:inMethod ?m1_ .

  ?m1_ java:name ?mn1_ .

  FILTER (?s0 != ?s1 && ?s0_ != ?s1_)

  FILTER EXISTS {
    ?cbody_ src:children/rdf:rest+ ?b0_ .

    ?b0_ rdf:first ?m0_ ;
         rdf:rest ?b_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

    ?b_ rdf:first ?meth_ ;
        rdf:rest ?b1_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

    ?b1_ rdf:first ?m1_ .
  }

}
}
''' % NS_TBL

Q_ADD_PARAM_RM_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveMethod:", ?mfqn, ?msig) AS ?name)
(?meth AS ?dep) (?ctx_ AS ?dep_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?tdecl ?tdecl_ ?mfqn ?msig ?params ?ctx_
    WHERE {
      ?meth a java:MethodDeclaration ;
            java:inTypeDeclaration ?tdecl ;
            java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            src:child3 ?params ;
            chg:removal ?ctx_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?tfqn ;
             chg:mappedTo ?tdecl_ .

      FILTER NOT EXISTS {
        ?meth chg:mappedTo [] .
      }

    } GROUP BY ?meth ?tdecl ?tdecl_ ?mfqn ?msig ?params ?ctx_
  }

  ?x a ?catx OPTION (INFERENCE NONE) ;
     src:parent+ ?params ;
     chg:movedTo ?x_ .

  ?x_ chg:addition ?ctx .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl ;
         java:fullyQualifiedName ?mfqn ;
         chg:mappedTo ?meth0_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl_ ;
          java:fullyQualifiedName ?mfqn_ ;
          java:signature ?msig ;
          src:child3 ?params0_ .

  ?x_ src:parent+ ?params0_ .

}
}
''' % NS_TBL

Q_ADD_PARAM_CHG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddParameter:", ?mfqn, ?msig) AS ?name)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?ctx AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param_ ?ctx ?pname_ ?def ?def_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param_ ?ctx ?pname_
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ .

          ?params_ a java:Parameters ;
                   src:parent ?meth_ .

          ?param_ a java:Parameter ;
                  java:name ?pname_ ;
                  src:parent ?params_ ;
                  chg:addition ?ctx .

        } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param_ ?ctx ?pname_
      }

      ?x a java:InvocationOrInstanceCreation ;
         java:mayInvokeMethod ?meth ;
         chg:mappedTo ?x_ .

      ?x_ a java:InvocationOrInstanceCreation ;
          java:mayInvokeMethod ?meth0_ .

      ?args a java:Arguments ;
            src:parent ?x ;
            chg:mappedTo ?args_ .

      ?args_ a java:Arguments ;
             src:parent ?x_ .

      ?arg a java:Expression ;
           src:parent ?args ;
           java:declaredBy ?def ;
           java:typeName ?atyname ;
           chg:mappedTo ?arg_ .

      ?arg_ a java:Expression ;
            src:parent ?args_ ;
            java:typeName ?atyname_ ;
            java:declaredBy ?def_ .

      FILTER (?atyname != ?atyname_)

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param_ ?ctx ?pname_ ?def ?def_
  }

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?ty_ a java:Type .

  {
    ?def src:parent ?y .
    ?ty src:parent ?y .
  }
  UNION
  {
    ?ty src:parent ?def .
  }

  {
    ?def_ src:parent ?y_ .
    ?ty_ src:parent ?y_ .
  }
  UNION
  {
    ?ty_ src:parent ?def_ .
  }

}
}
''' % NS_TBL

Q_RM_PARAM_CHG_TY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveParameter:", ?mfqn, ?msig) AS ?name)
(?ty AS ?dep) (?ty_ AS ?dep_)
(?param AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param ?ctx_ ?pname ?def ?def_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param ?ctx_ ?pname
        WHERE {

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ .

          ?params a java:Parameters ;
                  src:parent ?meth .

          ?param a java:Parameter ;
                 java:name ?pname ;
                 src:parent ?params ;
                 chg:removal ?ctx_ .

        } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param ?ctx_ ?pname
      }

      ?x a java:InvocationOrInstanceCreation ;
         java:mayInvokeMethod ?meth ;
         chg:mappedTo ?x_ .

      ?x_ a java:InvocationOrInstanceCreation ;
          java:mayInvokeMethod ?meth0_ .

      ?args a java:Arguments ;
            src:parent ?x ;
            chg:mappedTo ?args_ .

      ?args_ a java:Arguments ;
             src:parent ?x_ .

      ?arg a java:Expression ;
           src:parent ?args ;
           java:declaredBy ?def ;
           java:typeName ?atyname ;
           chg:mappedTo ?arg_ .

      ?arg_ a java:Expression ;
            src:parent ?args_ ;
            java:typeName ?atyname_ ;
            java:declaredBy ?def_ .

      FILTER (?atyname != ?atyname_)

    } GROUP BY ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?param ?ctx_ ?pname ?def ?def_
  }

  ?ty a java:Type ;
      chg:relabeled ?ty_ .

  ?ty_ a java:Type .

  {
    ?def src:parent ?y .
    ?ty src:parent ?y .
  }
  UNION
  {
    ?ty src:parent ?def .
  }

  {
    ?def_ src:parent ?y_ .
    ?ty_ src:parent ?y_ .
  }
  UNION
  {
    ?ty_ src:parent ?def_ .
  }

}
}
''' % NS_TBL

Q_RM_PARAM_ADD_METH_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddMethod:", ?mfqn_, ?msig_) AS ?name)
(?x AS ?dep) (?ctx_ AS ?dep_)
(?ctx AS ?ent) (?meth_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth_ ?tdecl ?tdecl_ ?mfqn_ ?msig_ ?params_ ?ctx
    WHERE {
      ?meth_ a java:MethodDeclaration ;
             java:inTypeDeclaration ?tdecl_ ;
             java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             src:child3 ?params_ ;
             chg:addition ?ctx .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?tfqn ;
             chg:mappedTo ?tdecl_ .

      FILTER NOT EXISTS {
        ?meth_ ^chg:mappedTo [] .
      }

    } GROUP BY ?meth_ ?tdecl ?tdecl_ ?mfqn_ ?msig_ ?params_ ?ctx
  }

  ?x_ a ?catx_ OPTION (INFERENCE NONE) ;
      src:parent+ ?params_ ;
      ^chg:movedTo ?x .

  ?x chg:removal ?ctx_ .

  ?meth0_ a java:MethodDeclaration ;
          java:inTypeDeclaration ?tdecl_ ;
          java:fullyQualifiedName ?mfqn_ ;
          ^chg:mappedTo ?meth0 .

  ?meth0 a java:MethodDeclaration ;
         java:inTypeDeclaration ?tdecl ;
         java:fullyQualifiedName ?mfqn ;
         java:signature ?msig_ ;
         src:child3 ?params0 .

  ?x src:parent+ ?params0 .

}
}
''' % NS_TBL

Q_CHG_CATCH_PARAM_REL_I_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeCatchParameter:", ?mfqn_, ?msig_, ":", ?pname_) AS ?name)
(?param AS ?dep) (?param_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param_ a java:CatchParameter ;
          src:child1 ?rty_ ;
          java:name ?pname_ ;
          ^chg:relabeled ?param .

  ?catch_ a java:CatchClause ;
          java:inMethodOrConstructor ?meth_ ;
          src:parent ?try_ ;
          src:child0 ?param_ .

  ?rty_ a java:ReferenceType ;
        java:name ?ename_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ .

  ?x_ a java:Name ;
      java:name ?pname_ ;
      java:declaredBy ?param_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_ADD_CATCH_PARAM_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddCatchParameter:", ?mfqn_, ?msig_, ":", ?pname_) AS ?name)
(?ctxp AS ?dep) (?param_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param_ a java:CatchParameter ;
          src:child1 ?rty_ ;
          java:name ?pname_ ;
          chg:addition ?ctxp .

  ?catch_ a java:CatchClause ;
          java:inMethodOrConstructor ?meth_ ;
          src:parent ?try_ ;
          src:child0 ?param_ .

  ?rty_ a java:ReferenceType ;
        java:name ?ename_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ .

  ?x_ a java:Name ;
      java:name ?pname_ ;
      java:declaredBy ?param_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_ADD_CATCH_PARAM_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("AddCatchParameter:", ?mfqn_, ?msig_, ":", ?pname_) AS ?name)
(?ctxp AS ?dep) (?param_ AS ?dep_)
(?x AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param_ a java:CatchParameter ;
          src:child1 ?rty_ ;
          java:name ?pname_ ;
          chg:addition ?ctxp .

  ?catch_ a java:CatchClause ;
          java:inMethodOrConstructor ?meth_ ;
          src:parent ?try_ ;
          src:child0 ?param_ .

  ?rty_ a java:ReferenceType ;
        java:name ?ename_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ .

  ?x_ a java:Name ;
      java:name ?pname_ ;
      java:declaredBy ?param_ ;
      ^chg:relabeled ?x .

}
}
''' % NS_TBL

Q_CHG_CATCH_PARAM_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeCatchParameter:", ?mfqn_, ?msig_, ":", ?pname_) AS ?name)
(?param AS ?dep) (?param_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param_ a java:CatchParameter ;
          src:child1 ?rty_ ;
          java:name ?pname_ ;
          ^chg:relabeled ?param .

  ?catch_ a java:CatchClause ;
          java:inMethodOrConstructor ?meth_ ;
          src:parent ?try_ ;
          src:child0 ?param_ .

  ?rty_ a java:ReferenceType ;
        java:name ?ename_ .

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ .

  ?x_ a java:Name ;
      java:name ?pname_ ;
      java:declaredBy ?param_ ;
      chg:addition ?ctxx .

}
}
''' % NS_TBL

Q_CHG_CATCH_PARAM_REL_D_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeCatchParameter:", ?mfqn, ?msig, ":", ?pname) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?param AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:CatchParameter ;
         src:child1 ?rty ;
         java:name ?pname ;
         chg:relabeled ?param_ .

  ?catch a java:CatchClause ;
         java:inMethodOrConstructor ?meth ;
         src:parent ?try ;
         src:child0 ?param .

  ?rty a java:ReferenceType ;
       java:name ?ename .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig .

  ?x a java:Name ;
     java:name ?pname ;
     java:declaredBy ?param ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_RM_CATCH_PARAM_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveCatchParameter:", ?mfqn, ?msig, ":", ?pname) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?param AS ?ent) (?ctxp_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:CatchParameter ;
         src:child1 ?rty ;
         java:name ?pname ;
         chg:removal ?ctxp_ .

  ?catch a java:CatchClause ;
         java:inMethodOrConstructor ?meth ;
         src:parent ?try ;
         src:child0 ?param .

  ?rty a java:ReferenceType ;
       java:name ?ename .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig .

  ?x a java:Name ;
     java:name ?pname ;
     java:declaredBy ?param ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_RM_CATCH_PARAM_REL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("RemoveCatchParameter:", ?mfqn, ?msig, ":", ?pname) AS ?name)
(?x AS ?dep) (?x_ AS ?dep_)
(?param AS ?ent) (?ctxp_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:CatchParameter ;
         src:child1 ?rty ;
         java:name ?pname ;
         chg:removal ?ctxp_ .

  ?catch a java:CatchClause ;
         java:inMethodOrConstructor ?meth ;
         src:parent ?try ;
         src:child0 ?param .

  ?rty a java:ReferenceType ;
       java:name ?ename .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig .

  ?x a java:Name ;
     java:name ?pname ;
     java:declaredBy ?param ;
     chg:relabeled ?x_ .

}
}
''' % NS_TBL

Q_CHG_CATCH_PARAM_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
SELECT DISTINCT
(CONCAT("ChangeCatchParameter:", ?mfqn, ?msig, ":", ?pname) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?param AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?param a java:CatchParameter ;
         src:child1 ?rty ;
         java:name ?pname ;
         chg:relabeled ?param_ .

  ?catch a java:CatchClause ;
         java:inMethodOrConstructor ?meth ;
         src:parent ?try ;
         src:child0 ?param .

  ?rty a java:ReferenceType ;
       java:name ?ename .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig .

  ?x a java:Name ;
     java:name ?pname ;
     java:declaredBy ?param ;
     chg:removal ?ctxx_ .

}
}
''' % NS_TBL

Q_RM_THIS_IVK_RM_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveThisInvocation:", ?cfqn, ?csig) AS ?name)
(?vdtor AS ?dep) (?ctx_ AS ?dep_)
(?ivk AS ?ent) (?ctxi_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?ctx_ ?fname ?tdecl ?tdecl_ ?tfqn
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             src:parent ?fdecl ;
             java:name ?fname ;
             chg:removal ?ctx_ .

      FILTER NOT EXISTS {
        ?vdtor src:child0 [] .
      }

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?tfqn ;
             chg:mappedTo ?tdecl_ .

    } GROUP BY ?vdtor ?ctx_ ?fname ?tdecl ?tdecl_ ?tfqn
  }

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:fullyQualifiedName ?cfqn ;
        java:signature ?csig ;
        src:child4 ?body ;
        chg:mappedTo ?ctor_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:fullyQualifiedName ?cfqn_ ;
         src:child4 ?body_ .

  ?ivk a java:ThisInvocation ;
       src:parent ?body ;
       chg:removal ?ctxi_ .

  FILTER NOT EXISTS {
    ?x src:parent ?body .
    FILTER (?x != ?ivk)
  }

  FILTER EXISTS {
    [] a chg:Deletion ;
       delta:entity1 ?ivk .
  }

  FILTER NOT EXISTS {
    ?y src:parent+ ?ivk ;
       chg:mappedStablyTo [] .
  }

}
}
''' % NS_TBL

Q_ADD_THIS_IVK_ADD_FIELD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddThisInvocation:", ?cfqn_, ?csig_) AS ?name)
(?ctxi AS ?dep) (?ivk_ AS ?dep_)
(?ctx AS ?ent) (?vdtor_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor_ ?ctx ?fname_ ?tdecl ?tdecl_ ?tfqn_
    WHERE {

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?fdecl_ ;
              java:name ?fname_ ;
              chg:addition ?ctx .

      FILTER NOT EXISTS {
        ?vdtor_ src:child0 [] .
      }

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?tfqn_ ;
              ^chg:mappedTo ?tdecl .

    } GROUP BY ?vdtor_ ?ctx ?fname_ ?tdecl ?tdecl_ ?tfqn_
  }

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:fullyQualifiedName ?cfqn ;
        src:child4 ?body ;
        chg:mappedTo ?ctor_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:fullyQualifiedName ?cfqn_ ;
         java:signature ?csig_ ;
         src:child4 ?body_ .

  ?ivk_ a java:ThisInvocation ;
        src:parent ?body_ ;
        chg:addition ?ctxi .

  FILTER NOT EXISTS {
    ?x_ src:parent ?body_ .
    FILTER (?x_ != ?ivk_)
  }

  FILTER EXISTS {
    [] a chg:Insertion ;
       delta:entity2 ?ivk_ .
  }

  FILTER NOT EXISTS {
    ?y_ src:parent+ ?ivk_ ;
        ^chg:mappedStablyTo [] .
  }

}
}
''' % NS_TBL

Q_ADD_STMT_RM_THIS_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddStatement:", ?cfqn_, ?csig_) AS ?name)
(?ivk AS ?dep) (?ctxi_ AS ?dep_)
(?ctx AS ?ent) (?stmt_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:fullyQualifiedName ?cfqn ;
        java:signature ?csig ;
        src:child4 ?body ;
        chg:mappedTo ?ctor_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:fullyQualifiedName ?cfqn_ ;
         java:signature ?csig_ ;
         src:child4 ?body_ .

  ?ivk a java:ThisInvocation ;
       src:parent ?body ;
       chg:removal ?ctxi_ .

  ?x src:parent+ ?ivk ;
     chg:mappedStablyTo ?x_ .

  ?s_ src:parent ?body_ .

  ?x_ src:parent+ ?s_ .

  ?stmt_ a ?cat_ OPTION (INFERENCE NONE) ;
         src:parent ?body_ ;
         java:successor ?s_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) ;
         chg:addition ?ctx .

}
}
''' % NS_TBL

Q_RM_STMT_ADD_THIS_IVK_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddStatement:", ?cfqn, ?csig) AS ?name)
(?stmt AS ?dep) (?ctx_ AS ?dep_)
(?ctxi AS ?ent) (?ivk_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ctor a java:ConstructorDeclaration ;
        java:inTypeDeclaration ?tdecl ;
        java:fullyQualifiedName ?cfqn ;
        java:signature ?csig ;
        src:child4 ?body ;
        chg:mappedTo ?ctor_ .

  ?ctor_ a java:ConstructorDeclaration ;
         java:inTypeDeclaration ?tdecl_ ;
         java:fullyQualifiedName ?cfqn_ ;
         java:signature ?csig_ ;
         src:child4 ?body_ .

  ?ivk_ a java:ThisInvocation ;
        src:parent ?body_ ;
        chg:addition ?ctxi .

  ?x_ src:parent+ ?ivk_ ;
      ^chg:mappedStablyTo ?x .

  ?s src:parent ?body .

  ?x src:parent+ ?s .

  ?stmt a ?cat OPTION (INFERENCE NONE) ;
        src:parent ?body ;
        java:successor ?s OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) ;
        chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_LVD_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeLocalVariableDeclaration:", ?mfqn, ?msig) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?ctx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         src:child0 ?ini ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ ;
          src:child0 ?ini_ .

  ?vdecl a java:LocalVariableDeclarationStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child1 ?ty ;
         src:child2 ?vdtor ;
         chg:mappedTo ?vdecl_ .

  ?vdecl_ a java:LocalVariableDeclarationStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child1 ?ty_ ;
          src:child2 ?vdtor_ .

  ?meth java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        chg:mappedTo ?meth_ .

  ?x_ a ?cat_ OPTION (INFERENCE NONE) ;
      src:parent+ ?ini_ ;
      chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_LVD_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeLocalVariableDeclaration:", ?mfqn, ?msig) AS ?name)
(?vdtor AS ?key) (?vdtor_ AS ?key_)
(?x AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         src:child0 ?ini ;
         chg:relabeled ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          java:name ?vname_ ;
          src:child0 ?ini_ .

  ?vdecl a java:LocalVariableDeclarationStatement ;
         java:inMethodOrConstructor ?meth ;
         src:child1 ?ty ;
         src:child2 ?vdtor ;
         chg:mappedTo ?vdecl_ .

  ?vdecl_ a java:LocalVariableDeclarationStatement ;
          java:inMethodOrConstructor ?meth_ ;
          src:child1 ?ty_ ;
          src:child2 ?vdtor_ .

  ?meth java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        chg:mappedTo ?meth_ .

  ?x a ?cat OPTION (INFERENCE NONE) ;
     src:parent+ ?ini ;
     chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_RM_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("Change") AS ?name)
(?cx0 AS ?key) (?cx0_ AS ?key_)
(?cx AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:Entity ;
     java:inTypeDeclaration/src:inFile ?file ;
     chg:mappedTo ?x_ .

  ?x_ a java:Entity ;
      java:inTypeDeclaration/src:inFile ?file_ .

  FILTER (EXISTS {
    ?x a java:AssignmentOp .
  } || EXISTS {
    ?x a java:AssignmentStatement .
  })

  FILTER (EXISTS {
    ?x_ a java:AssignmentOp .
  } || EXISTS {
    ?x_ a java:AssignmentStatement .
  })


  ?cx0_ src:parent+ ?x_ ;
        ^chg:relabeled ?cx0 .

  ?cx0 src:parent+ ?x .

  ?cx a ?catc OPTION (INFERENCE NONE) ;
      src:parent ?x ;
      chg:removal ?ctx_ .

  ?ctx_ src:parent*/src:inFile ?file_ .


  {
    ?x a ?catx OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child rdfs:subPropertyOf src:child .
      ?catx rdfs:subClassOf* ?ln .
      ?ln owl:equivalentClass ?r .
      ?r a owl:Restriction ;
         owl:onProperty ?p_child ;
         owl:onClass ?child_class .
      FILTER NOT EXISTS {
        ?r owl:minQualifiedCardinality [] .
      }
    }
    FILTER EXISTS {
      ?x ?p_child ?cx OPTION (INFERENCE NONE) .
      ?cx a ?child_class
    }
    FILTER NOT EXISTS {
      ?x a src:ListNode .
    }
  }
  UNION
  {
    ?x a src:TupleNode .
  }

}
}
''' % NS_TBL

Q_CHG_ADD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("Change") AS ?name)
(?cx0 AS ?key) (?cx0_ AS ?key_)
(?ctx AS ?ent) (?cx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:Entity ;
     java:inTypeDeclaration/src:inFile ?file ;
     chg:mappedTo ?x_ .

  ?x_ a java:Entity ;
      java:inTypeDeclaration/src:inFile ?file_ .

  FILTER (EXISTS {
    ?x a java:AssignmentOp .
  } || EXISTS {
    ?x a java:AssignmentStatement .
  })

  FILTER (EXISTS {
    ?x_ a java:AssignmentOp .
  } || EXISTS {
    ?x_ a java:AssignmentStatement .
  })


  ?cx0 src:parent+ ?x ;
       chg:relabeled ?cx0_ .

  ?cx0_ src:parent+ ?x_ .

  ?cx_ a ?catc_ OPTION (INFERENCE NONE) ;
       src:parent ?x_ ;
       chg:addition ?ctx .

  ?ctx src:parent*/src:inFile ?file .


  {
    ?x_ a ?catx_ OPTION (INFERENCE NONE) .
    GRAPH <http://codinuum.com/ont/cpi> {
      ?p_child_ rdfs:subPropertyOf src:child .
      ?catx_ rdfs:subClassOf* ?ln_ .
      ?ln_ owl:equivalentClass ?r_ .
      ?r_ a owl:Restriction ;
          owl:onProperty ?p_child_ ;
          owl:onClass ?child_class_ .
      FILTER NOT EXISTS {
        ?r_ owl:minQualifiedCardinality [] .
      }
    }
    FILTER EXISTS {
      ?x_ ?p_child_ ?cx_ OPTION (INFERENCE NONE) .
      ?cx_ a ?child_class_
    }
    FILTER NOT EXISTS {
      ?x_ a src:ListNode .
    }
  }
  UNION
  {
    ?x_ a src:TupleNode .
  }

}
}
''' % NS_TBL

Q_CHG_PARAM_ADD_THIS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParameter:", ?mfqn, ?msig, ":", ?name) AS ?name)
(?ctx AS ?dep) (?this_ AS ?dep_)
(?param AS ?ent) (?param_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?param ?param_ ?name ?name_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_
    WHERE {

      ?param a java:Parameter ;
             java:name ?name ;
             java:inMethodOrConstructor ?meth ;
             chg:relabeled ?param_ .

      ?param_ a java:Parameter ;
              java:name ?name_ ;
              java:inMethodOrConstructor ?meth_ .

      ?meth java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            java:inTypeDeclaration ?tdecl ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             java:inTypeDeclaration ?tdecl_ .

    } GROUP BY ?param ?param_ ?name ?name_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_
  }

  ?x a java:FieldAccess ;
     java:inMethodOrConstructor ?meth ;
     java:name ?name_ ;
     chg:mappedTo ?x_ .

  ?x_ a java:FieldAccess ;
      java:inMethodOrConstructor ?meth_ ;
      java:name ?name_ .

  ?this_ a java:This ;
         src:parent ?x_ ;
         chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_PARAM_RM_THIS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeParameter:", ?mfqn, ?msig, ":", ?name) AS ?name)
(?param AS ?dep) (?param_ AS ?dep_)
(?this AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?param ?param_ ?name ?name_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_
    WHERE {

      ?param a java:Parameter ;
             java:name ?name ;
             java:inMethodOrConstructor ?meth ;
             chg:relabeled ?param_ .

      ?param_ a java:Parameter ;
              java:name ?name_ ;
              java:inMethodOrConstructor ?meth_ .

      ?meth java:fullyQualifiedName ?mfqn ;
            java:signature ?msig ;
            java:inTypeDeclaration ?tdecl ;
            chg:mappedTo ?meth_ .

      ?meth_ java:fullyQualifiedName ?mfqn_ ;
             java:signature ?msig_ ;
             java:inTypeDeclaration ?tdecl_ .

    } GROUP BY ?param ?param_ ?name ?name_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_
  }

  ?x_ a java:FieldAccess ;
      java:inMethodOrConstructor ?meth_ ;
      java:name ?name ;
      ^chg:mappedTo ?x .

  ?x a java:FieldAccess ;
     java:inMethodOrConstructor ?meth ;
     java:name ?name .

  ?this a java:This ;
        src:parent ?x ;
        chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_RM_LN_CHILD_ADD_LN_CHILD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveListNodeChild:", ?mfqn, ?msig) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?ctxy AS ?ent) (?y_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x ?ctxx_ ?x0_ ?x1_
    WHERE {

      {
        SELECT DISTINCT ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x ?ctxx_ ?x0_ ?x1_
        WHERE {

          ?x a java:Entity ;
             src:parent ?ln ;
             chg:removal ?ctxx_ .

          ?x0_ a java:Entity ;
               src:parent ?ln_ ;
               chg:addition [] .

          ?ln a java:Entity ;
              a src:ListNode ;
              java:inMethodOrConstructor ?meth ;
              chg:mappedStablyTo ?ln_ .

          ?ln_ a java:Entity ;
               a src:ListNode ;
               java:inMethodOrConstructor ?meth_ .

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ .

          ?x1_ a java:Entity ;
               src:parent ?ln_ ;
               chg:addition [] .

          FILTER (?x0_ != ?x1_)

        } GROUP BY ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x ?ctxx_ ?x0_ ?x1_
      }

      FILTER EXISTS {
        ?s0 a java:Entity ;
            src:parent ?x OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) ;
            chg:mappedStablyTo ?s0_ .

        ?s1 a java:Entity ;
            src:parent ?x OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) ;
            chg:mappedStablyTo ?s1_ .

        FILTER (?s0 != ?s1)
        FILTER (?s0_ != ?s1_)

        ?s0_ src:parent ?x0_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
        ?s1_ src:parent ?x1_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
      }

    } GROUP BY ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x ?ctxx_ ?x0_ ?x1_
  }

  ?y_ a java:Entity ;
      src:parent ?ln_ ;
      chg:addition ?ctxy .

  FILTER EXISTS {
    ?ln_ src:children/rdf:rest* ?b0_ .
    ?b0_ rdf:first ?x0_ ;
         rdf:rest ?b1_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    ?b1_ rdf:first ?y_ ;
         rdf:rest ?b2_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    ?b2_ rdf:first ?x1_ .
  }

}
}
''' % NS_TBL

Q_ADD_LN_CHILD_RM_LN_CHILD_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddListNodeChild:", ?mfqn_, ?msig_) AS ?name)
(?y AS ?dep) (?ctxy_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x_ ?ctxx ?x0 ?x1
    WHERE {

      {
        SELECT DISTINCT ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x_ ?ctxx ?x0 ?x1
        WHERE {

          ?x_ a java:Entity ;
              src:parent ?ln_ ;
              chg:addition ?ctxx .

          ?x0 a java:Entity ;
              src:parent ?ln ;
              chg:removal [] .

          ?ln a java:Entity ;
              a src:ListNode ;
              java:inMethodOrConstructor ?meth ;
              chg:mappedStablyTo ?ln_ .

          ?ln_ a java:Entity ;
               a src:ListNode ;
               java:inMethodOrConstructor ?meth_ .

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ .

          ?x1 a java:Entity ;
              src:parent ?ln ;
              chg:removal [] .

          FILTER (?x0 != ?x1)

        } GROUP BY ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x_ ?ctxx ?x0 ?x1
      }

      FILTER EXISTS {
        ?s0_ a java:Entity ;
             src:parent ?x_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) ;
             ^chg:mappedStablyTo ?s0 .

        ?s1_ a java:Entity ;
             src:parent ?x_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) ;
             ^chg:mappedStablyTo ?s1 .

        FILTER (?s0 != ?s1)
        FILTER (?s0_ != ?s1_)

        ?s0 src:parent ?x0 OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
        ?s1 src:parent ?x1 OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
      }

    } GROUP BY ?ln ?ln_ ?meth ?meth_ ?mfqn ?mfqn_ ?msig ?msig_ ?x_ ?ctxx ?x0 ?x1
  }

  ?y a java:Entity ;
     src:parent ?ln ;
     chg:removal ?ctxy_ .

  FILTER EXISTS {
    ?ln src:children/rdf:rest* ?b0 .
    ?b0 rdf:first ?x0 ;
        rdf:rest ?b1 OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    ?b1 rdf:first ?y ;
        rdf:rest ?b2 OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    ?b2 rdf:first ?x1 .
  }

}
}
''' % NS_TBL

Q_ADD_RET_RM_STMT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddReturn:", ?mfqn_, ?msig_) AS ?name)
(?y AS ?dep) (?ctxy_ AS ?dep_)
(?ctxx AS ?ent) (?x_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x_ a java:BlockStatement ;
      a ?catx_ OPTION (INFERENCE NONE) ;
      java:inMethodOrConstructor ?meth_ ;
      chg:addition ?ctxx .

  FILTER (?catx_ IN (java:ReturnStatement,java:ContinueStatement,java:BreakStatement))

  FILTER NOT EXISTS {
    ?branch_ a java:BlockStatement ;
             a ?catb_ OPTION (INFERENCE NONE) .
    ?x_ src:parent+ ?branch_ .
    FILTER (?catb_ IN (java:IfStatement,java:SwitchStatement))
  }

  ?meth_ a java:MethodOrConstructor ;
         java:fullyQualifiedName ?mfqn_ ;
         java:signature ?msig_ ;
         ^chg:mappedTo ?meth .

  ?s_ src:parent+ ?x_ ;
      ^chg:mappedStablyTo ?s .

  ?s src:parent+ ?x .

  ?x a java:BlockStatement ;
     java:inMethodOrConstructor ?meth ;
     java:successor ?y OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

  ?y a java:BlockStatement ;
     chg:removal ?ctxy_ .

}
}
''' % NS_TBL

Q_RM_RET_ADD_STMT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddReturn:", ?mfqn, ?msig) AS ?name)
(?x AS ?dep) (?ctxx_ AS ?dep_)
(?ctxy AS ?ent) (?y_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?x a java:BlockStatement ;
     a ?catx OPTION (INFERENCE NONE) ;
     java:inMethodOrConstructor ?meth ;
     chg:removal ?ctxx_ .

  FILTER (?catx IN (java:ReturnStatement,java:ContinueStatement,java:BreakStatement))

  FILTER NOT EXISTS {
    ?branch a java:BlockStatement ;
            a ?catb OPTION (INFERENCE NONE) .
    ?x src:parent+ ?branch .
    FILTER (?catb IN (java:IfStatement,java:SwitchStatement))
  }

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        java:signature ?msig ;
        chg:mappedTo ?meth_ .

  ?s src:parent+ ?x ;
     chg:mappedStablyTo ?s_ .

  ?s_ src:parent+ ?x_ .

  ?x_ a java:BlockStatement ;
      java:inMethodOrConstructor ?meth_ ;
      java:successor ?y_ OPTION (TRANSITIVE, T_DISTINCT, T_NO_CYCLES, T_MIN(1)) .

  ?y_ a java:BlockStatement ;
      chg:addition ?ctxy .

}
}
''' % NS_TBL

Q_RM_IF_RM_JUMP_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveIf:", ?mfqn, ?msig) AS ?name)
(?y AS ?dep) (?ctxy_ AS ?dep_)
(?if AS ?ent) (?ctxi_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mfqn ?msig ?mfqn_ ?msig_ ?x ?x_ ?y ?ctxy_ ?if ?ctxi_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y ?ctxy_
        WHERE {

          ?y a java:BranchingStatement ;
             a ?caty OPTION (INFERENCE NONE) ;
             java:inMethodOrConstructor ?meth ;
             chg:removal ?ctxy_ .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ ;
                 ^chg:mappedTo ?meth .

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig .

        } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y ?ctxy_
      }

      ?y src:parent ?if OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

      ?if a java:BlockStatement ;
          a ?cati OPTION (INFERENCE NONE) ;
          chg:removal ?ctxi_ .

      FILTER (?cati IN (java:IfStatement,java:SwitchStatement))


      ?x a java:BlockStatement ;
         java:inMethodOrConstructor ?meth ;
         chg:removal [] .

      ?x_ a java:BlockStatement ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition [] .

#      FILTER EXISTS {
        ?s a java:Entity ;
           src:parent+ ?x ;
           chg:mappedStablyTo ?s_ .

        ?s_ a java:Entity ;
            src:parent+ ?x_ .
#      }

      FILTER NOT EXISTS {
        ?x src:parent ?if OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
      }

#      FILTER EXISTS {
        ?b rdf:first ?if ;
           rdf:rest+/rdf:first ?x .
#      }

    } GROUP BY ?mfqn ?msig ?mfqn_ ?msig_ ?x ?x_ ?y ?ctxy_ ?if ?ctxi_
  }

  FILTER NOT EXISTS {
    ?if src:parent ?if0 OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

    ?if0 a java:BlockStatement ;
         a ?cati0 OPTION (INFERENCE NONE) ;
         chg:mappedStablyTo ?if0_ .

    ?if0_ a java:BlockStatement ;
          a ?cati0_ OPTION (INFERENCE NONE) .

    FILTER (?cati0 IN (java:IfStatement,java:SwitchStatement))
    FILTER (?cati0_ IN (java:IfStatement,java:SwitchStatement))

    FILTER NOT EXISTS {
      ?x src:parent ?if0 OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    }
    FILTER NOT EXISTS {
      ?x_ src:parent ?if0_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    }
  }

}
}
''' % NS_TBL

Q_RM_LAST_IF_RM_JUMP_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveLastIf:", ?mfqn, ?msig) AS ?name)
(?if AS ?dep) (?ctxi_ AS ?dep_)
(?y AS ?ent) (?ctxy_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

    {
      SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y ?ctxy_ ?caty
      WHERE {

        ?y a java:BranchingStatement ;
           a ?caty OPTION (INFERENCE NONE) ;
           java:inMethodOrConstructor ?meth ;
           chg:removal ?ctxy_ .

        ?meth_ a java:MethodOrConstructor ;
               java:fullyQualifiedName ?mfqn_ ;
               java:signature ?msig_ ;
               ^chg:mappedTo ?meth .

        ?meth a java:MethodOrConstructor ;
              java:returnTypeName ?rtyname ;
              java:fullyQualifiedName ?mfqn ;
              java:signature ?msig .

        FILTER (?rtyname != "void")

      } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y ?ctxy_ ?caty
    }

    ?y src:parent ?if OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

    ?if a java:BlockStatement ;
        a ?cati OPTION (INFERENCE NONE) ;
        chg:removal ?ctxi_ .

    FILTER (?cati IN (java:IfStatement,java:SwitchStatement))

    FILTER NOT EXISTS {
      ?if java:successor ?succ .
      FILTER NOT EXISTS {
        ?succ src:parent+ ?if .
      }
    }

}
}
''' % NS_TBL

Q_ADD_IF_ADD_JUMP_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddIf:", ?mfqn_, ?msig_) AS ?name)
(?ctxi AS ?dep) (?if_ AS ?dep_)
(?ctxy AS ?ent) (?y_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mfqn ?msig ?mfqn_ ?msig_ ?x ?x_ ?y_ ?ctxy ?if_ ?ctxi
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y_ ?ctxy
        WHERE {

          ?y_ a java:BranchingStatement ;
              a ?caty_ OPTION (INFERENCE NONE) ;
              java:inMethodOrConstructor ?meth_ ;
              chg:addition ?ctxy .

          ?meth_ a java:MethodOrConstructor ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ ;
                 ^chg:mappedTo ?meth .

          ?meth a java:MethodOrConstructor ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig .

        } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y_ ?ctxy
      }

      ?y_ src:parent ?if_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

      ?if_ a java:BlockStatement ;
           a ?cati_ OPTION (INFERENCE NONE) ;
           chg:addition ?ctxi .

      FILTER (?cati_ IN (java:IfStatement,java:SwitchStatement))


      ?x a java:BlockStatement ;
         java:inMethodOrConstructor ?meth ;
         chg:removal [] .

      ?x_ a java:BlockStatement ;
          java:inMethodOrConstructor ?meth_ ;
          chg:addition [] .

#      FILTER EXISTS {
        ?s a java:Entity ;
           src:parent+ ?x ;
           chg:mappedStablyTo ?s_ .

        ?s_ a java:Entity ;
            src:parent+ ?x_ .
#      }

      FILTER NOT EXISTS {
        ?x_ src:parent ?if_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
      }

#      FILTER EXISTS {
        ?b rdf:first ?if_ ;
           rdf:rest+/rdf:first ?x_ .
#      }

    } GROUP BY ?mfqn ?msig ?mfqn_ ?msig_ ?x ?x_ ?y_ ?ctxy ?if_ ?ctxi
  }

  FILTER NOT EXISTS {
    ?if_ src:parent ?if0_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

    ?if0 a java:BlockStatement ;
         a ?cati0 OPTION (INFERENCE NONE) ;
         chg:mappedStablyTo ?if0_ .

    ?if0_ a java:BlockStatement ;
          a ?cati0_ OPTION (INFERENCE NONE) .

    FILTER (?cati0 IN (java:IfStatement,java:SwitchStatement))
    FILTER (?cati0_ IN (java:IfStatement,java:SwitchStatement))

    FILTER NOT EXISTS {
      ?x src:parent ?if0 OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    }
    FILTER NOT EXISTS {
      ?x_ src:parent ?if0_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .
    }
  }

}
}
''' % NS_TBL

Q_ADD_LAST_IF_ADD_JUMP_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddLastIf:", ?mfqn_, ?msig_) AS ?name)
(?ctxy AS ?dep) (?y_ AS ?dep_)
(?ctxi AS ?ent) (?if_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

    {
      SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y_ ?ctxy ?caty_
      WHERE {

        ?y_ a java:BranchingStatement ;
            a ?caty_ OPTION (INFERENCE NONE) ;
            java:inMethodOrConstructor ?meth_ ;
            chg:addition ?ctxy .

        ?meth_ a java:MethodOrConstructor ;
               java:fullyQualifiedName ?mfqn_ ;
               java:signature ?msig_ ;
               java:returnTypeName ?rtyname_ ;
               ^chg:mappedTo ?meth .

        ?meth a java:MethodOrConstructor ;
              java:fullyQualifiedName ?mfqn ;
              java:signature ?msig .

        FILTER (?rtyname_ != "void")

      } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?y_ ?ctxy ?caty_
    }

    ?y_ src:parent ?if_ OPTION (TRANSITIVE, T_DISTINCT, T_MIN(1)) .

    ?if_ a java:BlockStatement ;
         a ?cati_ OPTION (INFERENCE NONE) ;
         chg:addition ?ctxi .

    FILTER (?cati_ IN (java:IfStatement,java:SwitchStatement))

    FILTER NOT EXISTS {
      ?if_ java:successor ?succ_ .
      FILTER NOT EXISTS {
        ?succ_ src:parent+ ?if_ .
      }
    }

}
}
''' % NS_TBL

Q_RM_ROP_ADD_ROP_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveRelationalOp:", ?cfqn) AS ?name)
(?ctx AS ?dep) (?op_ AS ?dep_)
(?op AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?op a java:RelationalOp ;
      java:inTypeDeclaration/java:fullyQualifiedName ?cfqn ;
      chg:removal ?ctx_ .

  ?op_ a java:RelationalOp ;
       chg:addition ?ctx .

  ?e a java:Expression ;
     src:parent ?op ;
     chg:mappedStablyTo ?e_ .

  ?e_ a java:Expression ;
      src:parent ?op_ .

}
}
''' % NS_TBL

Q_CHG_TO_FD_PROTECTED_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldProtected:", ?cfqn, ".", ?fname) AS ?name)
(?facc AS ?dep) (?ctx_ AS ?dep_)
(?mod AS ?ent) (?mod_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mod ?mod_ ?fdecl ?fdecl_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
    WHERE {

      ?mod a java:Modifier ;
           src:parent ?mods ;
           chg:relabeled ?mod_ .

      ?mod_ a java:Protected ;
            src:parent ?mods_ .

      ?mods a java:Modifiers ;
            src:parent ?fdecl ;
            chg:mappedTo ?mods_ .

      ?mods_ a java:Modifiers ;
             src:parent ?fdecl_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?mod ?mod_ ?fdecl ?fdecl_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
  }

  ?vdtor a java:VariableDeclarator ;
         src:parent ?fdecl ;
         java:name ?fname ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?fdecl_ ;
          java:name ?fname_ .

  ?facc a java:FieldAccess ;
        java:inTypeDeclaration ?tdecl0 ;
        java:declaredBy ?vdtor ;
        java:name ?fname ;
        chg:removal ?ctx_ .

  FILTER NOT EXISTS {
    ?tdecl0 java:subTypeOf+ ?tdecl .
  }

  ?tdecl src:inFile ?file .
  ?pkg a java:PackageDeclaration ;
       src:parent/src:inFile ?file .

  ?tdecl0 src:inFile ?file0 .
  ?pkg0 a java:PackageDeclaration ;
        src:parent/src:inFile ?file0 .

  FILTER NOT EXISTS {
    ?pkg java:name ?pname .
    ?pkg0 java:name ?pname .
  }

}
}
''' % NS_TBL

Q_CHG_FROM_FD_PROTECTED_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeFieldProtected:", ?cfqn, ".", ?fname) AS ?name)
(?mod AS ?dep) (?mod_ AS ?dep_)
(?ctx AS ?ent) (?facc_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?mod ?mod_ ?fdecl ?fdecl_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
    WHERE {

      ?mod_ a java:Modifier ;
            src:parent ?mods_ ;
            ^chg:relabeled ?mod .

      ?mod a java:Protected ;
           src:parent ?mods .

      ?mods a java:Modifiers ;
            src:parent ?fdecl ;
            chg:mappedTo ?mods_ .

      ?mods_ a java:Modifiers ;
             src:parent ?fdecl_ .

      ?fdecl a java:FieldDeclaration ;
             java:inTypeDeclaration ?tdecl ;
             chg:mappedTo ?fdecl_ .

      ?fdecl_ a java:FieldDeclaration ;
              java:inTypeDeclaration ?tdecl_ .

      ?tdecl a java:TypeDeclaration ;
             java:fullyQualifiedName ?cfqn ;
             chg:mappedTo ?tdecl_ .

      ?tdecl_ a java:TypeDeclaration ;
              java:fullyQualifiedName ?cfqn_ .

    } GROUP BY ?mod ?mod_ ?fdecl ?fdecl_ ?tdecl ?tdecl_ ?cfqn ?cfqn_
  }

  ?vdtor a java:VariableDeclarator ;
         src:parent ?fdecl ;
         java:name ?fname ;
         chg:mappedTo ?vdtor_ .

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?fdecl_ ;
          java:name ?fname_ .

  ?facc_ a java:FieldAccess ;
         java:inTypeDeclaration ?tdecl0_ ;
         java:declaredBy ?vdtor_ ;
         java:name ?fname_ ;
         chg:addition ?ctx .

  FILTER NOT EXISTS {
    ?tdecl0_ java:subTypeOf+ ?tdecl_ .
  }

  ?tdecl src:inFile ?file .
  ?pkg a java:PackageDeclaration ;
       src:parent/src:inFile ?file .

  ?tdecl0 src:inFile ?file0 .
  ?pkg0 a java:PackageDeclaration ;
        src:parent/src:inFile ?file0 .

  FILTER NOT EXISTS {
    ?pkg java:name ?pname .
    ?pkg0 java:name ?pname .
  }

}
}
''' % NS_TBL

Q_ADD_RET_ADD_IF_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddIf:", ?mfqn, ?msig) AS ?name)
(?ctx AS ?dep) (?if_ AS ?dep_)
(?ctx0t AS ?ent0) (?ret0t_ AS ?ent0_)
(?ctx0e AS ?ent1) (?ret0e_ AS ?ent1_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_  ?if0_ ?ctx0t ?ret0t_ ?ctx0e ?ret0e_
    WHERE {

      {
        SELECT DISTINCT ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_
        WHERE {

          ?meth a java:MethodDeclaration ;
                java:fullyQualifiedName ?mfqn ;
                java:signature ?msig ;
                chg:mappedTo ?meth_ .

          ?meth_ a java:MethodDeclaration ;
                 java:fullyQualifiedName ?mfqn_ ;
                 java:signature ?msig_ .

          ?ret a java:ReturnStatement ;
               java:inMethod ?meth ;
               chg:mappedStablyTo ?ret_ .

          ?ret_ a java:ReturnStatement ;
                java:inMethod ?meth_ .

          FILTER NOT EXISTS {
            ?ret java:successor [] .
          }

          FILTER NOT EXISTS {
            ?ret_ java:successor [] .
          }

        } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_
      }

      ?if0_ a java:IfStatement ;
            src:parent/src:parent/src:parent/src:parent ?meth_ ;
            src:child1 ?then0_ ;
            src:child2 ?else0_ .

      ?ret0t_ a java:ReturnStatement ;
              src:parent ?then0_ ;
              chg:addition ?ctx0t .

      ?ret0e_ a java:ReturnStatement ;
              src:parent ?else0_ ;
              chg:addition ?ctx0e .

      FILTER EXISTS {
        [] rdf:first ?ret0t_ ;
           rdf:rest rdf:nil .
      }

      FILTER EXISTS {
        [] rdf:first ?ret0e_ ;
           rdf:rest rdf:nil .
      }

    } GROUP BY ?meth ?meth_ ?mfqn ?msig ?mfqn_ ?msig_ ?if0_ ?ctx0t ?ret0t_ ?ctx0e ?ret0e_
  }

  ?if0_ src:parent ?blk_ .
  ?blk_ a java:Block ;
        src:parent ?if_ .

  ?if_ a java:IfStatement ;
       src:parent/src:parent ?meth_ ;
       chg:addition ?ctx .

}
}
''' % NS_TBL

Q_CHG_LHS_TY_CHG_RETTY_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeLHSType:", ?mfqn) AS ?name)
(?ty AS ?key) (?ty_ AS ?key_)
(?rty AS ?ent) (?rty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?vdtor_ ?ty ?ty_
    WHERE {

      ?vdtor a java:VariableDeclarator ;
             src:parent ?vdecl .

      ?ty a java:Type ;
          src:parent ?vdecl ;
          chg:relabeled ?ty_ .

      ?vdtor_ a java:VariableDeclarator ;
              src:parent ?vdecl_ .

      ?ty_ a java:Type ;
           src:parent ?vdecl_ .
    } GROUP BY ?vdtor ?vdtor_ ?ty ?ty_
  }

  ?assign a ?cata ;
          java:inMethodOrConstructor/java:fullyQualifiedName ?mfqn ;
          src:child0 ?lhs ;
          src:child1 ?rhs ;
          chg:mappedTo ?assign_ .

  ?assign_ a ?cata_ ;
           java:inMethodOrConstructor/java:fullyQualifiedName ?mfqn_ ;
           src:child0 ?lhs_ ;
           src:child1 ?rhs_ .

  FILTER (?cata IN (java:Assign,java:AssignStatement))
  FILTER (?cata_ IN (java:Assign,java:AssignStatement))

  ?lhs java:declaredBy ?vdtor ;
       chg:mappedTo ?lhs_ .

  ?lhs_ java:declaredBy ?vdtor_ .

  ?rhs java:mayInvokeMethod ?meth ;
       chg:mappedTo ?rhs_ .

  ?rhs_ java:mayInvokeMethod ?meth_ .

  ?meth src:child2 ?rty ;
        chg:mappedTo ?meth_ .
  ?meth_ src:child2 ?rty_ .

  ?rty chg:relabeled ?rty_ .

}
}
''' % NS_TBL

Q_CHG_RHS_TY_RM_LHS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeRHSType:", ?mfqn) AS ?name)
(?lhs AS ?dep) (?ctx_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  {
    SELECT DISTINCT ?vdtor ?vname ?ty ?ty_
    WHERE {

      ?ty a java:Type ;
          src:parent ?vdecl ;
          chg:relabeled ?ty_ .

      ?vdtor a java:VariableDeclarator ;
             java:name ?vname ;
             src:parent ?vdecl .

    } GROUP BY ?vdtor ?vname ?ty ?ty_
  }

  ?rhs java:declaredBy ?vdtor ;
       src:parent ?assign .

  ?assign a ?cata ;
          java:inMethodOrConstructor/java:fullyQualifiedName ?mfqn ;
          src:child0 ?lhs ;
          src:child1 ?rhs .

  FILTER (?cata IN (java:Assign,java:AssignStatement))

  ?lhs a java:Expression ;
       chg:removal ?ctx_ .

}
}
''' % NS_TBL

Q_CHG_TY_RM_INIT_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("ChangeType:", ?mfqn) AS ?name)
(?init AS ?dep) (?ctx_ AS ?dep_)
(?ty AS ?ent) (?ty_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?ty a java:Type ;
      src:parent ?vdecl ;
      chg:relabeled ?ty_ .

  ?vdtor a java:VariableDeclarator ;
         java:name ?vname ;
         src:child0 ?init ;
         src:parent ?vdecl .

  ?init a java:Expression ;
        chg:removal ?ctx_ .

  ?vdecl java:inMethodOrConstructor/java:fullyQualifiedName ?mfqn .

}
}
''' % NS_TBL

Q_RM_VDTOR_ADD_VDTOR_MOV_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("MoveVariableDeclarator:", ?mfqn) AS ?name)
(?ctx AS ?key) (?vdtor_ AS ?key_)
(?vdtor AS ?ent) (?ctx_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?vdtor a java:VariableDeclarator ;
         src:parent ?vdecl ;
         chg:removal ?ctx_ ;
         chg:movedTo ?vdtor_ .

  ?vdecl src:parent ?blk ;
         java:inMethodOrConstructor ?meth .

  ?meth a java:MethodOrConstructor ;
        java:fullyQualifiedName ?mfqn ;
        chg:mappedTo ?meth_ .

  ?blk chg:mappedTo ?blk_ .

  ?vdtor_ a java:VariableDeclarator ;
          src:parent ?vdecl_ ;
          chg:addition ?ctx .

  ?vdecl_ java:inMethodOrConstructor ?meth_ .

  FILTER EXISTS {
    ?vdecl_ src:parent+ ?blk0_ .
    ?blk0_ src:parent+ ?blk_ .
  }

}
}
''' % NS_TBL


###

Q_AUXFILE_DEL_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("RemoveAuxfile:", ?loc0) AS ?name)
(?file0 AS ?key) (?ctx0_ AS ?key_)
(?file1 AS ?ent) (?ctx1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?file0 a src:Auxfile ;
         src:location ?loc0 ;
         chg:removal ?ctx0_ .

  ?file1 a src:Auxfile ;
         src:location ?loc1 ;
         chg:removal ?ctx1_ .

}
}
''' % NS_TBL

Q_AUXFILE_INS_JAVA = '''DEFINE input:inference "ont.cpi"
PREFIX fb:  <%(fb_ns)s>
PREFIX ver: <%(ver_ns)s>
PREFIX src: <%(src_ns)s>
PREFIX chg: <%(chg_ns)s>
PREFIX java: <%(java_ns)s>
PREFIX delta: <%(delta_ns)s>
SELECT DISTINCT
(CONCAT("AddAuxfile:", ?loc0_) AS ?name)
(?_ctx0 AS ?key) (?file0_ AS ?key_)
(?ctx1 AS ?ent) (?file1_ AS ?ent_)
WHERE {
GRAPH <%(fb_ns)s%%(proj_id)s> {

  ?file0_ a src:Auxfile ;
          src:location ?loc0_ ;
          chg:addition ?ctx0 .

  ?file1_ a src:Auxfile ;
          src:location ?loc1_ ;
          chg:addition ?ctx1 .

}
}
''' % NS_TBL

#####

K_INS = 'INS'
K_DEL = 'DEL'
K_REL = 'REL'
K_MOV = 'MOV'

KINDS = [K_INS, K_DEL, K_REL, K_MOV]


QUERY_TBL = {
    'java': [
        'ins',
        'ins_c',
        'del',
        'del_c',
        'rel',
        'mov',
        'movrel',
        'del_ins_mov',
        'del_ins_u',
        'del_ins_l',
        'del_ins_ln',
        'rel_del',
        'rel_ins',
        # 'ins_mov',
        # 'del_mov',
        'ins_rel',
        'del_rel',
        'mov_rel',
        'mov_rel_ex',
        'mov_rel_ex2',
        'del_del',
        # 'mov__del_or_ins',
    ],
}

QUERY_LIST = [
    'ins_file',
    'del_file',
    'mov_file',
    'chg_file',
]

REF_QUERY_TBL = {  # lang -> (query * tag) list
    'java': [
        ('LV_RENAME', K_REL),
        ('LV_RENAME_R', K_REL),

        ('ADD_PARAM', K_INS),
        ('ADD_PARAM_I_ARG', K_INS),
        ('ADD_PARAM_D', K_DEL),

        ('RM_PARAM', K_DEL),
        ('RM_PARAM_D_ARG', K_DEL),

        ('RENAME_METH', K_REL),
        ('RENAME_METH_EX', K_REL),

        ('EXTRACT_METH', K_INS),  # 10
        ('EXTRACT_METH_I', K_INS),
        # ('EXTRACT_METH_D', K_DEL),
        ('EXTRACT_METH_R', K_REL),
        ('EXTRACT_METH_M', K_MOV),
        ('EXTRACT_METH_EX', K_INS),

        ('INLINE_METH', K_DEL),
        ('INLINE_METH_D', K_DEL),
        # ('INLINE_METH_I', K_INS),
        ('INLINE_METH_R', K_REL),
        ('INLINE_METH_M', K_MOV),
        ('INLINE_METH_EX', K_DEL),

        ('PULL_UP_FIELD_I', K_INS),  # 20
        ('PULL_UP_FIELD_D', K_DEL),

        ('PUSH_DOWN_FIELD_I', K_INS),
        ('PUSH_DOWN_FIELD_D', K_DEL),

        ('MOVE_FIELD_I', K_INS),
        ('MOVE_FIELD_D', K_DEL),
        ('MOVE_FIELD_EX_I', K_INS),
        ('MOVE_FIELD_EX_D', K_DEL),

        ('PULL_UP_METH_I', K_INS),
        ('PULL_UP_METH_D', K_DEL),

        ('PUSH_DOWN_METH_I', K_INS),  # 30
        ('PUSH_DOWN_METH_D', K_DEL),

        ('MOVE_METH_I', K_INS),
        ('MOVE_METH_D', K_DEL),
        ('MOVE_METH_EX_I', K_INS),
        ('MOVE_METH_EX_D', K_DEL),
        ('MOVE_METH_EX_R', K_REL),

        ('IEV_I', K_INS),
        ('IEV_I2', K_INS),
        ('IEV_I3', K_INS),
        ('IEV_M', K_MOV),  # 40

        ('INLINE_TEMP_D', K_DEL),
        ('INLINE_TEMP_D2', K_DEL),
        ('INLINE_TEMP_D3', K_DEL),
        ('INLINE_TEMP_M', K_MOV),
        ('INLINE_TEMP_M2', K_MOV),
    ],
}

OTH_QUERY_TBL = {
    'java': [
        # (RULE_NAME, KEY, ENT)

        # ('INS_PARAM_INS', K_INS, K_INS),
        # ('MOV_MOVREL', K_MOV, K_REL),

        ('MOVINSREL', K_INS, K_REL),
        ('MOVINS_INS_0', K_INS, K_INS),
        ('MOVINS_INS_1', K_INS, K_INS),
        ('INS_MOVINS', K_INS, K_INS),
        ('MOVDEL_DEL_0', K_DEL, K_DEL),
        ('MOVDEL_DEL_1', K_DEL, K_DEL),
        ('DEL_MOVDEL', K_DEL, K_DEL),
        ('INS_INS', K_INS, K_INS),

        ('ADD_RET_REL', K_INS, K_REL),
        ('RM_RET_REL', K_DEL, K_REL),  # 10
        ('CHG_RETVAL_REL', K_REL, K_REL),
        ('CHG_RETVAL_DEL_RETTY', K_REL, K_DEL),
        ('CHG_RETVAL_INS_RETTY', K_REL, K_INS),
        ('ADD_RET_ADD_EXPR', K_INS, K_INS),
        ('WRAP_RET_ADD_EXIT', K_INS, K_INS),
        ('UNWRAP_RET_RM_EXIT', K_DEL, K_DEL),
        ('CHG_LVD_TY_CHG_RETTY', K_REL, K_REL),
        ('CHG_RETTY_DEL', K_REL, K_DEL),
        ('CHG_RETTY_ADD', K_REL, K_INS),

        ('CHG_EQ_OPERAND_REL', K_REL, K_REL),  # 20
        ('CHG_EQ_OPERAND_INS', K_REL, K_INS),
        ('CHG_LHS_REL', K_REL, K_REL),
        ('CHG_LHS_INS', K_REL, K_INS),
        ('CHG_LHS_DEL', K_REL, K_DEL),

        ('CHG_PARAM_REL', K_REL, K_REL),
        ('RM_PARAM_RM_ARG', K_DEL, K_DEL),
        ('CHG_PARAM_INS_ARG', K_REL, K_INS),
        ('CHG_PARAM_CHG_ARG', K_REL, K_REL),
        ('DEL_PARAM_TY_CHG_ARG', K_DEL, K_REL),
        ('INS_PARAM_TY_CHG_ARG', K_INS, K_REL),  # 30
        ('CHG_PARAM_TY_CHG_ARG_TY', K_REL, K_REL),
        ('CHG_PARAM_TY_RM_ARG_TY', K_REL, K_DEL),
        ('CHG_PARAM_TY_ADD_ARG_TY', K_REL, K_INS),
        ('CHG_PARAM_TY_DEL', K_REL, K_DEL),
        ('CHG_PARAM_TY_INS', K_REL, K_INS),
        ('ADD_PARAM_ADD_ARG', K_INS, K_INS),
        ('ADD_IM_PARAM_ADD_M_PARAM', K_INS, K_INS),
        ('RM_LVD_ADD_PARAM', K_DEL, K_INS),
        ('ADD_LVD_RM_PARAM', K_INS, K_DEL),
        ('ADD_LVD_CHG_PARAM', K_INS, K_REL),  # 40
        ('ADD_PARAM_ADD_PARAM', K_INS, K_INS),
        ('RM_PARAM_RM_PARAM', K_DEL, K_DEL),

        ('CHG_M_ABST_INS_BODY', K_REL, K_INS),
        ('RM_M_ABST_INS_BODY', K_DEL, K_INS),
        ('ADD_M_ABST_DEL_BODY', K_INS, K_DEL),
        ('CHG_M_ABST_DEL_BODY', K_REL, K_DEL),

        ('INS_METH_REL', K_INS, K_REL),
        ('INS_METH_ADD_VDTOR', K_INS, K_INS),
        ('ADD_CTOR_ADD_INIT', K_INS, K_INS),

        ('MOVE_SWITCH_LABEL', K_DEL, K_INS),
        ('CHG_CLASS_REL', K_REL, K_REL),
        ('CHG_CLASS_CHG_CTOR', K_REL, K_REL),
        ('CHG_CLASS_DEL', K_REL, K_DEL),
        ('CHG_CLASS_RM_CTOR', K_REL, K_DEL),
        ('CHG_CLASS_INS', K_REL, K_INS),
        ('CHG_CLASS_ADD_CTOR', K_REL, K_INS),
        ('CHG_FIELD_REL0', K_REL, K_REL),
        ('CHG_FIELD_REL1', K_REL, K_REL),
        ('CHG_VDTOR_REL', K_REL, K_REL),
        ('CHG_ADD_FIELD', K_REL, K_INS),
        ('INS_METH_ADD_VDTOR', K_INS, K_INS),
        ('ADD_CTOR_CHG_ARG', K_INS, K_REL),
        ('ADD_METH_CHG_SUPER', K_INS, K_REL),
        ('CHG_LVD_TY_CHG_INI', K_REL, K_REL),
        ('CHG_LVD_TY_INS', K_REL, K_INS),
        ('CHG_LVD_TY_REL', K_REL, K_REL),

        ('CHG_FD_TY_CHG_FA_TY', K_REL, K_REL),
        ('CHG_FD_TY_CHG_PARAM_TY', K_REL, K_REL),

        ('RM_EXPR_REL_EXPR', K_DEL, K_REL),
        ('RM_LVD_INI_REL', K_DEL, K_REL),
        ('CHG_SUPERTY_REL', K_REL, K_REL),
        ('CHG_SUPERTY_CHG_IVK', K_REL, K_REL),
        ('CHG_METH_REL', K_REL, K_REL),
        ('CHG_METH_CHG_ARG', K_REL, K_REL),
        ('ADD_CTOR_INS_ARG', K_INS, K_INS),

        ('RM_BR_ADD_BR', K_DEL, K_INS),
        ('RM_BR_ADD_NON_BR', K_DEL, K_INS),
        ('MOVDEL_METH_DEL', K_DEL, K_DEL),
        ('RM_ADD_VDTOR', K_DEL, K_INS),
        ('CHG_CLASS_CHG_IMPORT', K_REL, K_REL),
        ('CHG_IMPORT_REL', K_REL, K_REL),
        ('CHG_IMPORT_INS', K_REL, K_INS),
        ('CHG_IMPORT_DEL', K_REL, K_DEL),
        ('CHG_LVD_TY_DEL_P', K_REL, K_DEL),
        ('CHG_LVD_TY_INS_P', K_REL, K_INS),

        ('DEL_SIBLINGS', K_DEL, K_DEL),
        ('INS_SIBLINGS', K_INS, K_INS),

        ('INS_IVK_ADD_ARG', K_INS, K_INS),

        ('RM_LVD_TY_REL', K_DEL, K_REL),

        ('DEL_METH_INS_METH', K_DEL, K_INS),
        ('CHG_METH_INS_METH', K_REL, K_INS),
        ('DEL_METH_CHG_METH', K_DEL, K_REL),

        ('ADD_FIELD_ADD_ASSIGN', K_INS, K_INS),
        ('RM_FIELD_RM_ASSIGN', K_DEL, K_DEL),
        ('CHG_FIELD_RM_ASSIGN', K_REL, K_DEL),
        ('CHG_FIELD_ADD_ASSIGN', K_REL, K_INS),

        ('CHG_FIELD_TY_CHG_LVD_TY', K_REL, K_REL),

        ('CHG_IVK_RM_ARG', K_REL, K_DEL),
        ('CHG_IVK_ADD_ARG', K_REL, K_INS),

        ('RM_METH_ADD_METH', K_DEL, K_INS),
        ('RM_METH_ADD_METH_2', K_DEL, K_INS),

        ('CHG_RETTY_RM_RETVAL', K_REL, K_DEL),
        ('CHG_RETTY_CHG_RETVAL', K_REL, K_REL),
        ('CHG_RETTY_ADD_RETVAL', K_REL, K_INS),
        ('RM_RETTY_RM_RETVAL', K_DEL, K_DEL),
        ('RM_RETTY_CHG_RETVAL', K_DEL, K_REL),
        ('ADD_RETTY_ADD_RETVAL', K_INS, K_INS),
        ('ADD_RETTY_CHG_RETVAL', K_INS, K_REL),

        ('CHG_ABS_METH_CHG_METH', K_REL, K_REL),

        ('RM_VDTOR_ADD_VDTOR', K_DEL, K_INS),

        ('CHG_PKG_MOV_FILE', K_REL, K_MOV),

        ('AUXFILE_DEL', K_DEL, K_DEL),
        ('MOV_FILE_INS', K_MOV, K_INS),
        ('MOV_FILE_DEL', K_MOV, K_DEL),
        ('MOV_FILE_REL', K_MOV, K_REL),

        ('RM_FIELD_ADD_FIELD', K_DEL, K_INS),

        ('MOV_MOVREL_NAME', K_MOV, K_REL),

        ('CHG_EXC_CHG_CATCH', K_REL, K_REL),
        ('CHG_EXC_ADD_CATCH', K_REL, K_INS),
        ('CHG_EXC_RM_CATCH', K_REL, K_DEL),
        ('ADD_EXC_CHG_CATCH', K_INS, K_REL),
        ('ADD_EXC_ADD_CATCH', K_INS, K_INS),
        ('RM_EXC_CHG_CATCH', K_DEL, K_REL),
        ('RM_EXC_RM_CATCH', K_DEL, K_DEL),
        ('ADD_IVK_ADD_THROWS', K_INS, K_INS),
        ('ADD_THROWS_ADD_THROWS', K_INS, K_INS),
        ('CHG_THROWS_ADD_IVK', K_REL, K_INS),
        ('RM_THROWS_RM_THROWS', K_DEL, K_DEL),
        ('ADD_THROWS_CHG_THROW', K_INS, K_REL),

        ('RM_THROWS_CHG_THROW', K_DEL, K_REL),

        ('CHG_ENUMCONST_REL', K_REL, K_REL),

        ('CHG_RETTY_CHG_RETTY_D', K_REL, K_REL),
        ('CHG_RETTY_CHG_RETTY_I', K_REL, K_REL),

        ('ADD_THROWS_ADD_THROWS_IVK', K_INS, K_INS),
        ('RM_THROWS_RM_THROWS_IVK', K_DEL, K_DEL),

        ('RM_ASSIGN_ADD_ASSIGN', K_DEL, K_INS),

        ('CHG_SUPER_ADD_ARG', K_REL, K_INS),
        ('CHG_SUPER_RM_ARG', K_REL, K_DEL),

        ('CHG_RETTY_ADD_CAST', K_REL, K_INS),
        ('CHG_RETTY_RM_CAST', K_REL, K_DEL),

        ('CHG_IVK_CHG_TY', K_REL, K_REL),

        ('ADD_OVERRIDE_CHG_SUPERTY', K_INS, K_REL),
        ('ADD_OVERRIDE_ADD_SUPERTY', K_INS, K_INS),
        ('CHG_OVERRIDE_CHG_SUPERTY_I', K_REL, K_REL),
        ('CHG_OVERRIDE_ADD_SUPERTY', K_REL, K_INS),

        ('RM_OVERRIDE_CHG_SUPERTY', K_REL, K_DEL),
        ('RM_OVERRIDE_RM_SUPERTY', K_DEL, K_DEL),
        ('CHG_OVERRIDE_CHG_SUPERTY_D', K_REL, K_REL),
        ('CHG_OVERRIDE_RM_SUPERTY', K_DEL, K_REL),

        ('CHG_RETTY_CHG_FIELD_TY', K_REL, K_REL),

        ('CHG_FOR_PARAM_TY_CHG_TY', K_REL, K_REL),

        ('CHG_RETTY_CHG_RETTY_D', K_REL, K_REL),
        ('CHG_RETTY_CHG_RETTY_I', K_REL, K_REL),
        ('CHG_RETTY_CHG_RETTY', K_REL, K_REL),
        ('RM_RETTY_CHG_RETTY', K_DEL, K_REL),
        ('ADD_RETTY_CHG_RETTY', K_INS, K_REL),

        ('CHG_FD_TY_DEL_RHS', K_REL, K_DEL),
        ('CHG_FD_TY_INS_RHS', K_REL, K_INS),
        ('CHG_FD_TY_CHG_RHS', K_REL, K_REL),

        ('MOVE_ASSIGN', K_DEL, K_INS),

        ('CHG_PARAM_TY_DEL_ARG_CAST', K_REL, K_DEL),
        ('CHG_PARAM_TY_INS_ARG_CAST', K_REL, K_INS),

        ('RM_ACC_RM_METH', K_DEL, K_DEL),
        ('ADD_ACC_ADD_METH', K_INS, K_INS),

        ('RM_TY_DEL_EXPR', K_DEL, K_DEL),
        ('RM_TY_REL_EXPR', K_DEL, K_REL),
        ('ADD_TY_INS_EXPR', K_INS, K_INS),
        ('ADD_TY_REL_EXPR', K_INS, K_REL),

        ('RM_IF_ADD_IF', K_DEL, K_INS),

        ('CHG_ARG_TY_CHG_IVK', K_REL, K_REL),
        ('CHG_ARG_TY_RM_IVK', K_DEL, K_REL),
        ('CHG_ARG_TY_ADD_IVK', K_INS, K_REL),

        ('RM_FOR_INIT_RM_LVD', K_DEL, K_DEL),
        ('ADD_FOR_INIT_ADD_LVD', K_INS, K_INS),

        ('RM_THROWS_RM_EXC', K_DEL, K_DEL),
        ('ADD_THROWS_ADD_EXC', K_INS, K_INS),

        ('DEL_STMT_INS_STMT', K_DEL, K_INS),

        ('RM_FIELD_TY_REL', K_DEL, K_REL),
        ('ADD_FIELD_TY_REL', K_INS, K_REL),

        ('RM_FIELD_ADD_FIELD_MOV', K_DEL, K_INS),

        ('CHG_FD_TY_RM_FACC_CTX', K_DEL, K_REL),
        ('CHG_FD_TY_ADD_FACC_CTX', K_REL, K_INS),

        ('CHG_LVD_INS', K_REL, K_INS),
        ('CHG_LVD_DEL', K_REL, K_DEL),

        ('CHG_RM', K_REL, K_DEL),
        ('CHG_ADD', K_REL, K_INS),

        ('CHG_RETTY_RM', K_REL, K_DEL),
        ('CHG_RETTY_ADD', K_REL, K_INS),

        ('CHG_RETTY_CHG_LVD_TY', K_REL, K_REL),

        ('CHG_ABS_METH_RETTY_CHG_METH_RETTY_D', K_REL, K_REL),
        ('CHG_ABS_METH_RETTY_CHG_METH_RETTY_I', K_REL, K_REL),

        ('CHG_SUPER_DEL_TY', K_REL, K_DEL),
        ('CHG_SUPER_INS_TY', K_REL, K_INS),

        ('CHG_RETTY_ADD_SUPERTY', K_REL, K_INS),
        ('CHG_RETTY_CHG_SUPERTY_I', K_REL, K_REL),
        ('CHG_RETTY_RM_SUPERTY', K_REL, K_DEL),
        ('CHG_RETTY_CHG_SUPERTY_D', K_REL, K_REL),

        ('RM_METH_CHG_METH', K_DEL, K_REL),

        ('CHG_LHS_TY_CHG_RETTY', K_REL, K_REL),

        ('RM_VDTOR_ADD_VDTOR_MOV', K_INS, K_DEL),

        # ('RM_STMT_INS_BODY', K_DEL, K_INS),

        # (RULE_NAME, KEY, ENT)
    ],
}

OTH_DIR_QUERY_TBL = {
    'java': [
        # (RULE_NAME, DEP, ENT list) ENT list depends on DEP

        ('D_DEL_DEL', K_DEL, [K_DEL]),
        ('D_INS_INS', K_INS, [K_INS]),
        ('MOV_DEL', K_DEL, [K_MOV]),
        ('MOV_INS', K_INS, [K_MOV]),

        # ('RM_DEF_RM_USE', K_DEL, [K_DEL]),
        # ('ADD_USE_ADD_DEF', K_INS, [K_INS]),

        ('RM_METH_RM_IVK', K_DEL, [K_DEL]),
        ('RM_METH_REL', K_REL, [K_DEL]),
        ('RM_METH_RM_ARG', K_DEL, [K_DEL]),
        ('RM_METH_CHG_ARG', K_REL, [K_DEL]),
        ('RM_METH_ADD_ARG', K_INS, [K_DEL]),
        ('ADD_METH_ADD_ARG', K_INS, [K_INS]),
        ('ADD_METH_CHG_ARG', K_INS, [K_REL]),
        ('ADD_METH_ADD_IVK', K_INS, [K_INS]),
        ('ADD_METH_CHG_IVK', K_INS, [K_REL]),
        ('RM_METH_CHG_IVK', K_REL, [K_DEL]),
        ('ADD_METH_REL', K_INS, [K_REL]),
        ('CHG_METH_INS', K_REL, [K_INS]),
        ('CHG_METH_ADD_ARG', K_INS, [K_REL]),
        ('CHG_METH_RM_IVK', K_DEL, [K_REL]),
        ('CHG_METH_ADD_IVK', K_REL, [K_INS]),

        ('RM_CLASS_DEL', K_DEL, [K_DEL]),
        ('RM_CLASS_REL', K_REL, [K_DEL]),
        ('RM_CLASS_RM_IMPORT', K_DEL, [K_DEL]),
        ('ADD_CLASS_REL', K_INS, [K_REL]),
        ('ADD_CLASS_INS', K_INS, [K_INS]),
        ('ADD_CLASS_ADD_IMPORT', K_INS, [K_INS]),

        ('RM_FIELD_REL', K_REL, [K_DEL]),
        ('RM_FIELD_DEL', K_DEL, [K_DEL]),
        ('ADD_FIELD_INS', K_INS, [K_INS]),
        ('ADD_FIELD_REL', K_INS, [K_REL]),
        ('CHG_FIELD_INS', K_REL, [K_INS]),
        ('CHG_FIELD_DEL', K_DEL, [K_REL]),

        ('RM_FIELD_ADD_OBJ', K_INS, [K_DEL]),
        ('RM_FIELD_CHG_OBJ', K_REL, [K_DEL]),
        ('RM_FIELD_INS_CAST', K_INS, [K_DEL]),
        ('ADD_FIELD_RM_OBJ', K_INS, [K_DEL]),

        ('RM_SUPERTY_REL', K_REL, [K_DEL]),
        ('RM_SUPERTY_ADD_METH', K_INS, [K_DEL]),
        ('ADD_SUPERTY_REL', K_INS, [K_REL]),
        ('ADD_SUPERTY_RM_METH', K_INS, [K_DEL]),

        ('RM_ENUMCONST_REL', K_REL, [K_DEL]),
        ('RM_ENUMCONST_DEL', K_DEL, [K_DEL]),
        ('ADD_ENUMCONST_REL', K_INS, [K_REL]),
        ('ADD_ENUMCONST_INS', K_INS, [K_INS]),

        # ('CHG_FIELD_TY_INS', K_REL, [K_INS]),
        # ('CHG_FIELD_TY_DEL', K_DEL, [K_REL]),

        ('DEL_LN_DEL', K_DEL, [K_DEL]),
        ('DEL_LN_DEL_2', K_DEL, [K_DEL]),
        ('INS_LN_INS', K_INS, [K_INS]),
        ('INS_LN_INS_2', K_INS, [K_INS]),
        ('DEL_METH_LN_DEL', K_DEL, [K_DEL]),
        ('INS_METH_LN_INS', K_INS, [K_INS]),

        ('RM_VDTOR_DEL', K_DEL, [K_DEL]),
        ('RM_VDTOR_REL', K_REL, [K_DEL]),
        ('ADD_VDTOR_INS', K_INS, [K_INS]),
        ('ADD_VDTOR_REL', K_INS, [K_REL]),
        ('CHG_VDTOR_INS', K_REL, [K_INS]),
        ('CHG_VDTOR_DEL', K_DEL, [K_REL]),

        ('RM_PARAM_DEL', K_DEL, [K_DEL]),
        ('RM_PARAM_ADD_IVK', K_DEL, [K_INS]),
        ('RM_PARAM_REL', K_REL, [K_DEL]),
        ('ADD_PARAM_INS', K_INS, [K_INS]),
        ('ADD_PARAM_REL', K_INS, [K_REL]),
        ('ADD_PARAM_ADD_IVK', K_INS, [K_INS]),
        ('INS_PARAM_REL', K_INS, [K_REL]),
        ('CHG_PARAM_INS', K_REL, [K_INS]),
        ('CHG_PARAM_DEL', K_DEL, [K_REL]),
        ('CHG_PARAM_CHG_USE_D', K_REL, [K_REL]),
        ('CHG_PARAM_CHG_USE_I', K_REL, [K_REL]),

        ('ADD_IMPORT_INS', K_INS, [K_INS]),
        ('ADD_IMPORT_REL', K_INS, [K_REL]),
        ('ADD_IMPORT_ADD_RTY', K_INS, [K_INS]),
        ('ADD_IMPORT_ADD_FILE', K_INS, [K_INS]),
        ('RM_IMPORT_DEL', K_DEL, [K_DEL]),
        ('RM_IMPORT_REL', K_REL, [K_DEL]),
        ('RM_IMPORT_RM_FILE', K_DEL, [K_DEL]),
        ('RM_IMPORT_ADD_IMPORT', K_INS, [K_DEL]),
        ('RM_IMPORT_CHG_IMPORT', K_REL, [K_DEL]),
        ('RM_IMPORT_RM_RTY', K_DEL, [K_DEL]),
        ('RM_IMPORT_CHG_RTY', K_REL, [K_DEL]),

        ('ADD_FD_PUBLIC_INS', K_INS, [K_INS]),
        ('ADD_FD_PUBLIC_REL', K_INS, [K_REL]),
        ('ADD_FD_FINAL_ADD_ASSIGN', K_INS, [K_INS]),
        ('ADD_FD_FINAL_RM_ASSIGN', K_DEL, [K_INS]),
        ('ADD_FD_FINAL_CHG_ASSIGN', K_REL, [K_INS]),
        ('RM_FD_PUBLIC_DEL', K_DEL, [K_DEL]),
        ('RM_FD_PUBLIC_REL', K_REL, [K_DEL]),
        ('RM_FD_PRIVATE_INS', K_DEL, [K_INS]),
        ('CHG_FD_PRIVATE_INS', K_REL, [K_INS]),
        ('ADD_FD_PRIVATE_DEL', K_DEL, [K_INS]),
        ('CHG_FD_PRIVATE_DEL', K_DEL, [K_REL]),
        ('RM_FD_FINAL_RM_ASSIGN', K_DEL, [K_DEL]),
        ('RM_FD_FINAL_ADD_ASSIGN', K_DEL, [K_INS]),
        ('RM_FD_FINAL_CHG_ASSIGN', K_DEL, [K_REL]),
        ('CHG_FD_PUBLIC_INS', K_REL, [K_INS]),
        ('CHG_FD_PUBLIC_REL', K_REL, [K_REL]),
        ('CHG_FD_PROTECTED_INS', K_REL, [K_INS]),
        ('CHG_FD_PROTECTED_REL', K_REL, [K_REL]),

        ('RM_M_PRIVATE_INS', K_DEL, [K_INS]),
        ('ADD_M_PRIVATE_DEL', K_DEL, [K_INS]),
        ('CHG_M_PRIVATE_INS', K_REL, [K_INS]),
        ('ADD_MC_PUBLIC_REL', K_INS, [K_REL]),
        ('ADD_MC_PUBLIC_CHG_AC', K_INS, [K_REL]),
        ('ADD_MC_PUBLIC_INS', K_INS, [K_INS]),
        ('ADD_MC_PUBLIC_ADD_MC_PUBLIC', K_INS, [K_INS]),
        ('RM_MC_PUBLIC_RM_MC_PUBLIC', K_DEL, [K_DEL]),
        ('ADD_MC_PROTECTED_ADD_MC_PUBLIC', K_INS, [K_INS]),
        ('RM_MC_PUBLIC_RM_MC_PROTECTED', K_DEL, [K_DEL]),
        ('CHG_M_MOD_CHG_METH', K_REL, [K_REL]),

        ('RM_C_ABST_RM_M_ABST', K_DEL, [K_DEL]),
        ('RM_C_ABST_ADD_DEFAULT_CTOR', K_INS, [K_DEL]),
        ('RM_C_ABST_CHG_NEW', K_DEL, [K_REL]),
        ('ADD_C_ABST_CHG_NEW', K_REL, [K_INS]),
        ('ADD_C_ABST_ADD_M_ABST', K_INS, [K_INS]),

        ('ADD_TD_PUBLIC_INS', K_INS, [K_INS]),
        ('RM_TD_PUBLIC_DEL', K_DEL, [K_DEL]),

        ('RM_USE_RM_ASSIGN', K_DEL, [K_DEL]),
        ('ADD_USE_ADD_ASSIGN', K_INS, [K_INS]),
        ('ADD_USE_ADD_INI', K_INS, [K_INS]),

        ('ADD_STMT_ADD_RET', K_INS, [K_INS]),

        ('CHG_SUPERTY_ADD_FIELD', K_INS, [K_REL]),

        ('CHG_SUPERTY_RM_FACC', K_DEL, [K_REL]),
        ('CHG_SUPERTY_CHG_FACC_D', K_REL, [K_REL]),
        ('CHG_SUPERTY_ADD_FACC', K_REL, [K_INS]),
        ('CHG_SUPERTY_CHG_FACC_I', K_REL, [K_REL]),

        ('RM_LOOP_RM_CONT', K_DEL, [K_DEL]),

        ('RM_CLASS_CHG_IMPORT', K_REL, [K_DEL]),
        ('ADD_CLASS_CHG_IMPORT', K_INS, [K_REL]),

        ('CHG_INI_CHG_RETTY', K_REL, [K_REL]),

        ('ADD_ABS_METH_ADD_METH', K_INS, [K_INS]),
        ('ADD_ABS_METH_CHG_METH', K_REL, [K_INS]),
        ('CHG_ABS_METH_ADD_METH', K_INS, [K_REL]),
        ('CHG_ABS_METH_CHG_METH_I', K_REL, [K_REL]),
        ('RM_ABS_METH_RM_METH', K_DEL, [K_DEL]),
        ('RM_ABS_METH_CHG_METH', K_DEL, [K_REL]),
        ('CHG_ABS_METH_RM_METH', K_REL, [K_DEL]),
        ('CHG_ABS_METH_CHG_METH_D', K_REL, [K_REL]),

        ('RM_RHS_ADD_INI', K_INS, [K_DEL]),

        ('ADD_RET_ADD_EXIT_WRAP_RET', K_INS, [K_INS, K_INS]),

        ('MOV_METH_REL_METH', K_REL, [K_INS]),

        ('RM_OVERRIDE_RENAME_METH', K_DEL, [K_REL]),

        ('CHG_SUPER_RM_SUPERIVK', K_DEL, [K_REL]),

        ('ADD_SUPERTY_ADD_IVK', K_INS, [K_INS]),
        ('ADD_SUPERTY_CHG_IVK', K_INS, [K_REL]),
        ('ADD_SUPERTY_ADD_RETTY', K_INS, [K_INS]),
        ('RM_SUPERTY_RM_IVK', K_DEL, [K_DEL]),
        ('RM_SUPERTY_CHG_IVK', K_REL, [K_DEL]),
        ('RM_SUPERTY_RM_RETTY', K_DEL, [K_DEL]),

        ('ADD_M_ABST_CHG_METH', K_REL, [K_INS]),
        ('ADD_M_ABST_ADD_METH', K_INS, [K_INS]),
        ('RM_M_ABST_CHG_METH', K_DEL, [K_REL]),
        ('RM_M_ABST_RM_METH', K_DEL, [K_DEL]),

        ('ADD_METH_RM_PTY', K_INS, [K_DEL]),
        ('RM_METH_ADD_PTY', K_INS, [K_DEL]),

        # ('ADD_METH_ADD_IMPORT', K_INS, [K_INS]),
        # ('ADD_METH_CHG_IMPORT', K_INS, [K_REL]),
        # ('RM_METH_RM_IMPORT', K_DEL, [K_DEL]),
        # ('RM_METH_CHG_IMPORT', K_REL, [K_DEL]),

        ('ADD_METH_ADD_SUPERTY', K_INS, [K_INS]),
        ('ADD_METH_CHG_SUPERTY', K_INS, [K_REL]),
        ('RM_METH_RM_SUPERTY', K_DEL, [K_DEL]),
        ('RM_METH_CHG_SUPERTY', K_REL, [K_DEL]),
        ('CHG_METH_ADD_SUPERTY', K_REL, [K_INS]),
        ('CHG_METH_CHG_SUPERTY_I', K_REL, [K_REL]),
        ('CHG_METH_RM_SUPERTY', K_DEL, [K_REL]),
        ('CHG_METH_CHG_SUPERTY_D', K_REL, [K_REL]),
        ('ADD_METH_RM_SUPERTY', K_DEL, [K_INS]),
        ('RM_METH_ADD_SUPERTY', K_DEL, [K_INS]),

        ('RM_M_FINAL_ADD_METH', K_DEL, [K_INS]),
        ('ADD_M_FINAL_RM_METH', K_DEL, [K_INS]),
        ('RM_M_FINAL_ADD_PARAM', K_DEL, [K_INS]),
        ('ADD_M_FINAL_RM_PARAM', K_DEL, [K_INS]),

        ('RM_OVERRIDE_CHG_RETTY', K_DEL, [K_REL]),
        ('RM_OVERRIDE_CHG_METH', K_DEL, [K_REL]),
        ('RM_OVERRIDE_RM_METH', K_DEL, [K_DEL]),
        ('ADD_OVERRIDE_CHG_RETTY', K_REL, [K_INS]),
        ('ADD_OVERRIDE_CHG_METH', K_REL, [K_INS]),
        ('ADD_OVERRIDE_ADD_METH', K_INS, [K_INS]),

        ('RM_METH_RM_RET', K_DEL, [K_DEL]),
        ('ADD_METH_ADD_RET', K_INS, [K_INS]),

        ('RM_LV_FINAL_RM_LVAR', K_DEL, [K_DEL]),
        ('RM_LV_FINAL_CHG_LVAR', K_REL, [K_DEL]),
        ('ADD_LV_FINAL_ADD_LVAR', K_INS, [K_INS]),
        ('ADD_LV_FINAL_CHG_LVAR', K_INS, [K_REL]),

        ('RM_LVD_TY_CHG_RETTY', K_DEL, [K_REL]),
        ('ADD_LVD_TY_CHG_RETTY', K_REL, [K_INS]),

        ('RM_BLOCK_ADD_VDTOR', K_DEL, [K_INS]),
        ('ADD_BLOCK_RM_VDTOR', K_DEL, [K_INS]),

        ('CHG_M_PUBLIC_CHG_IVK', K_REL, [K_REL]),
        ('CHG_M_PUBLIC_ADD_IVK', K_REL, [K_INS]),
        ('CHG_M_PROTECTED_CHG_IVK', K_REL, [K_REL]),
        ('CHG_M_PROTECTED_RM_IVK', K_DEL, [K_REL]),

        ('CHG_IVK_RM_VDTOR', K_REL, [K_DEL]),
        ('CHG_IVK_CHG_VDTOR_D', K_REL, [K_REL]),
        ('CHG_IVK_ADD_VDTOR', K_INS, [K_REL]),
        ('CHG_IVK_CHG_VDTOR_I', K_REL, [K_REL]),

        ('RM_STATIC_RM_NAME', K_DEL, [K_DEL]),
        ('RM_STATIC_CHG_NAME_D', K_REL, [K_DEL]),
        ('ADD_STATIC_ADD_NAME', K_INS, [K_INS]),
        ('ADD_STATIC_CHG_NAME_I', K_INS, [K_REL]),

        ('CHG_STATIC_RM_NAME', K_DEL, [K_REL]),
        ('CHG_STATIC_CHG_NAME_D', K_REL, [K_REL]),
        ('CHG_STATIC_ADD_NAME', K_REL, [K_INS]),
        ('CHG_STATIC_CHG_NAME_I', K_REL, [K_REL]),

        ('RM_M_FINAL_CHG_SUPERTY', K_DEL, [K_REL]),
        ('ADD_M_FINAL_CHG_SUPERTY', K_REL, [K_INS]),

        ('RM_THROWS_RM_THROW', K_DEL, [K_DEL]),
        ('ADD_THROWS_ADD_THROW', K_INS, [K_INS]),

        ('RM_THROWS_CHG_IVK', K_DEL, [K_REL]),
        ('ADD_THROWS_CHG_IVK', K_REL, [K_INS]),

        # ('ADD_STMT_ADD_COND', K_INS, [K_INS]),

        ('RM_STATIC_CHG_INIT', K_REL, [K_DEL]),
        ('ADD_STATIC_CHG_INIT', K_INS, [K_REL]),

        ('RM_LABEL_DEL', K_DEL, [K_DEL]),
        ('RM_LABEL_REL', K_REL, [K_DEL]),
        ('ADD_LABEL_INS', K_INS, [K_INS]),
        ('ADD_LABEL_REL', K_INS, [K_REL]),

        ('RM_INIT_ADD_ASSIGN', K_INS, [K_DEL]),
        ('ADD_INIT_RM_ASSIGN', K_INS, [K_DEL]),

        ('RM_STATIC_RM_IVK', K_DEL, [K_DEL]),
        ('ADD_STATIC_ADD_IVK', K_INS, [K_INS]),

        ('CHG_ACC_ADD_FACC', K_REL, [K_INS]),
        ('CHG_ACC_RM_FACC', K_DEL, [K_REL]),

        ('DEL_COND_RM_COND', K_DEL, [K_DEL]),
        ('INS_COND_ADD_COND', K_INS, [K_INS]),

        ('MOVREL_V', K_MOV, [K_REL]),

        ('ADD_CTOR_IVK_DEL', K_DEL, [K_INS]),

        ('RM_SUPER_IVK_RM_CTOR', K_DEL, [K_DEL]),
        ('ADD_SUPER_IVK_ADD_CTOR', K_INS, [K_INS]),
        ('RM_CTOR_ADD_SUPER_IVK', K_INS, [K_DEL]),
        ('ADD_CTOR_RM_SUPER_IVK', K_INS, [K_DEL]),

        ('CHG_FD_TY_DEL', K_DEL, [K_REL]),
        ('CHG_FD_TY_INS', K_REL, [K_INS]),

        ('CHG_RETTY_CHG_IVK_D', K_REL, [K_REL]),
        ('CHG_RETTY_CHG_IVK_I', K_REL, [K_REL]),

        ('RM_FIELD_ADD_SUPERTY', K_INS, [K_DEL]),
        ('ADD_FIELD_RM_SUPERTY', K_INS, [K_DEL]),

        ('RM_CONT_RM_LOOP', K_DEL, [K_DEL]),
        ('ADD_CONT_ADD_LOOP', K_INS, [K_INS]),

        ('RM_LVAR_INS_METH', K_DEL, [K_INS]),
        ('ADD_LVAR_DEL_METH', K_DEL, [K_INS]),

        ('RM_INIT_CHG_LVAR', K_REL, [K_DEL]),
        ('ADD_INIT_CHG_LVAR', K_INS, [K_REL]),
        ('RM_INIT_RM_LVAR', K_DEL, [K_DEL]),
        ('ADD_INIT_ADD_LVAR', K_INS, [K_INS]),

        ('RM_ASSIGN_RM_LVAR', K_DEL, [K_DEL]),
        ('ADD_ASSIGN_ADD_LVAR', K_INS, [K_INS]),

        ('RM_DEFAULT_CTOR_RM_DEFAULT_CTOR', K_DEL, [K_DEL]),
        ('ADD_DEFAULT_CTOR_ADD_DEFAULT_CTOR', K_INS, [K_INS]),

        ('RM_FD_FINAL_ADD_INI', K_DEL, [K_INS]),
        ('ADD_FD_FINAL_RM_INI', K_DEL, [K_INS]),

        ('CHG_MOD_RM_METH', K_DEL, [K_REL]),
        ('CHG_MOD_ADD_METH', K_REL, [K_INS]),

        ('ADD_LVD_FINAL_RM_ASSIGN', K_DEL, [K_INS]),
        ('RM_LVD_FINAL_ADD_ASSIGN', K_DEL, [K_INS]),

        ('RM_EXTENDS_ADD_METH', K_INS, [K_DEL]),
        ('ADD_EXTENDS_RM_METH', K_INS, [K_DEL]),

        ('RM_FD_FINAL_RM_FD_STATIC', K_DEL, [K_DEL]),
        ('ADD_FD_FINAL_ADD_FD_STATIC', K_INS, [K_INS]),

        ('RM_CTOR_BODY_RM_CTOR', K_DEL, [K_DEL]),
        ('ADD_CTOR_BODY_ADD_CTOR', K_INS, [K_INS]),

        ('RM_FIELD_INI_ADD_FIELD_INI', K_INS, [K_DEL]),

        ('RM_RET_RM_METH', K_DEL, [K_DEL]),
        ('ADD_RET_ADD_METH', K_INS, [K_INS]),

        ('RM_ASSIGN_RM_FIELD', K_DEL, [K_DEL]),
        ('ADD_ASSIGN_ADD_FIELD', K_INS, [K_INS]),
        ('CHG_LHS_RM_FIELD', K_DEL, [K_REL]),
        ('CHG_LHS_ADD_FIELD', K_REL, [K_INS]),

        ('RM_THIS_IVK_RM_CTOR', K_DEL, [K_DEL]),
        ('ADD_THIS_IVK_ADD_CTOR', K_INS, [K_INS]),

        ('RM_METH_ADD_METH_3', K_DEL, [K_INS]),

        ('RM_PARAM_ADD_METH', K_DEL, [K_INS]),
        ('ADD_PARAM_RM_METH', K_DEL, [K_INS]),

        ('CHG_CATCH_PARAM_REL_I', K_REL, [K_REL]),
        ('ADD_CATCH_PARAM_INS', K_INS, [K_INS]),
        ('ADD_CATCH_PARAM_REL', K_INS, [K_REL]),
        ('CHG_CATCH_PARAM_INS', K_REL, [K_INS]),

        ('CHG_CATCH_PARAM_REL_D', K_REL, [K_REL]),
        ('RM_CATCH_PARAM_DEL', K_DEL, [K_DEL]),
        ('RM_CATCH_PARAM_REL', K_REL, [K_DEL]),
        ('CHG_CATCH_PARAM_DEL', K_DEL, [K_REL]),

        ('RM_THIS_IVK_RM_FIELD', K_DEL, [K_DEL]),
        ('ADD_THIS_IVK_ADD_FIELD', K_INS, [K_INS]),

        ('RM_ASSIGN_RM_CTOR', K_DEL, [K_DEL]),
        ('ADD_ASSIGN_ADD_CTOR', K_INS, [K_INS]),

        ('RM_PARAM_TY_RM_USE', K_DEL, [K_DEL]),
        ('ADD_PARAM_TY_ADD_USE', K_INS, [K_INS]),

        ('ADD_STMT_RM_THIS_IVK', K_DEL, [K_INS]),
        ('RM_STMT_ADD_THIS_IVK', K_DEL, [K_INS]),

        ('CHG_PARAM_ADD_THIS', K_INS, [K_REL]),
        ('CHG_PARAM_RM_THIS', K_REL, [K_DEL]),

        ('RM_LN_CHILD_ADD_LN_CHILD', K_DEL, [K_INS]),
        ('ADD_LN_CHILD_RM_LN_CHILD', K_DEL, [K_INS]),

        ('ADD_RET_RM_STMT', K_DEL, [K_INS]),
        ('RM_RET_ADD_STMT', K_DEL, [K_INS]),

        ('RM_IF_RM_JUMP', K_DEL, [K_DEL]),
        ('ADD_IF_ADD_JUMP', K_INS, [K_INS]),

        ('RM_IVK_CHG_TY', K_DEL, [K_REL]),
        ('ADD_IVK_CHG_TY', K_REL, [K_INS]),

        ('RM_IVK_RM_SUPERTY', K_DEL, [K_DEL]),
        ('ADD_IVK_ADD_SUPERTY', K_INS, [K_INS]),

        ('RM_LAST_IF_RM_JUMP', K_DEL, [K_DEL]),
        ('ADD_LAST_IF_ADD_JUMP', K_INS, [K_INS]),

        ('ADD_PARAM_CHG_TY', K_REL, [K_INS]),
        ('RM_PARAM_CHG_TY', K_REL, [K_DEL]),

        ('ADD_SUPERTY_ADD_FACC', K_INS, [K_INS]),
        ('ADD_SUPERTY_CHG_FACC', K_INS, [K_REL]),
        ('RM_SUPERTY_RM_FACC', K_DEL, [K_DEL]),
        ('RM_SUPERTY_CHG_FACC', K_REL, [K_DEL]),

        ('ADD_C_ABST_CHG_SUPERTY', K_REL, [K_INS]),

        ('RM_SUPER_IVK_CHG_SUPERTY', K_DEL, [K_REL]),
        ('RM_SUPER_IVK_RM_SUPERTY', K_DEL, [K_DEL]),
        ('ADD_SUPER_IVK_CHG_SUPERTY', K_REL, [K_INS]),
        ('ADD_SUPER_IVK_ADD_SUPERTY', K_INS, [K_INS]),

        ('RM_ARG_RM_CTOR', K_DEL, [K_DEL]),
        ('ADD_ARG_ADD_CTOR', K_INS, [K_INS]),

        ('RM_ROP_ADD_ROP', K_INS, [K_DEL]),

        ('CHG_TO_FD_PROTECTED_DEL', K_DEL, [K_REL]),
        ('CHG_FROM_FD_PROTECTED_INS', K_REL, [K_INS]),

        ('ADD_RET_ADD_IF', K_INS, [K_INS, K_INS]),

        ('CHG_RHS_TY_RM_LHS', K_DEL, [K_REL]),
        ('CHG_TY_RM_INIT', K_DEL, [K_REL]),

        ('RM_OVERRIDED_METH_RM_SUPERTY', K_DEL, [K_DEL]),
        ('ADD_OVERRIDED_METH_ADD_SUPERTY', K_INS, [K_INS]),

        # ('INS_METH_MOVINS', K_INS, [K_INS]),

        # (RULE_NAME, DEP, ENT list) ENT list depends on DEP
    ],
}
