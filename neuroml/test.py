from lxml import objectify
from neuroml import utils

file = '../testFiles/NML2_FullCell.nml'
doc = objectify.parse(file)
root = doc.getroot()
