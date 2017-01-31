
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
              val = str(val[0])
          else:
              val = str(val)
          #print("- Found %s in %s: %s = [%s]"%(group, attrName, name,val))
          return val
  return None


