select 
    o.PCMID
    , o.CMID
    , p.SPEC
    , n.NAME
    , i.STOREID
from 
    CMOBJECTS o
    , CMOBJNAMES n
    ,  CMOBJPROPS7 p
    , CMCLASSES c
    , CMSTOREIDS i
where 
    o.CMID = p.CMID 
    and o.CLASSID = c.CLASSID 
    and o.CMID = n.CMID 
    and c.NAME='Report' 
    and n.ISDEFAULT=1
    and o.CMID = i.CMID
