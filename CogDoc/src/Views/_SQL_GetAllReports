select 
    o.PCMID
    , o.CMID
    , p.SPEC
    , n.NAME 
from 
    CMOBJECTS o
    , CMOBJNAMES n
    ,  CMOBJPROPS7 p
    , CMCLASSES c 
where 
    o.CMID = p.CMID 
    and o.CLASSID = c.CLASSID 
    and o.CMID = n.CMID 
    and c.NAME='Report' 
    and n.ISDEFAULT=1
