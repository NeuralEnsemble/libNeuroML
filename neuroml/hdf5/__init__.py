
import neuroml
import numpy
import sys


def get_str_attribute_group(group, name):
  if not hasattr(group._v_attrs,name):
        return None

  for attrName in group._v_attrs._v_attrnames:
      if attrName == name:
          val = group._v_attrs[name]

          if isinstance(val,numpy.ndarray):
              val = val[0]
          elif isinstance(val, numpy.bytes_):
               val = val.decode('UTF-8')
          else:
               val = str(val)
              
          #print("-    Found [%s] in [%s]: %s = [%s] %s"%(attrName, group, name,val,type(val)))
          return val
  return None


