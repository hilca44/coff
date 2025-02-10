#!/bin/bash
# add_entry "Beispieltext $(date +%T)"
kff='#           s.ea  e.di  inv.  r.en  l.ast  t.odo  o.ds  a.dr  n.ew
#           p.df  doi.nv  d.eliv  c.onfi  copy.  h.ide  x.del'
koo=" [r] ren   [e] est  [c] cfm  [d] den   [i] inv"
ko2=" [n] new   [y] cop"
kos=" [N] new  [C] cop   [e] edi"
kaa="[ret] edi  [R] ren  [E] edi  [N] new"
moo='
#   __   __   __  
#  /  \ |__) |  \  '"$koo"'
#  \__/ |  \ |__/  '"$ko2"'
#               
'
mos='
#   __   __   __  
#  /  \ |  \ /__`  
#  \__/ |__/ .__/ '"$kos"'
#                 
'

ml='
#  
# L A S T  O R D E R S
#                 
'

maa='
#        __   __  
#   /\  |  \ |__)  
#  /~~\ |__/ |  \ '"$kaa"'
#                 
'

mis='
################# 
##  INVOIVES   ## '"$kos"'
#################    
'

mt='
#
# T O D O   '"$kos"'
#                  
'

mna='
##############################################
# NEW ADDRESS #  [ctrl+c] cancel #############
##############################################
'

mpdf='
# P D F 
'

ms='
##############################################
# S E A R C H #  [<] back to command mode  ###
##############################################
'

