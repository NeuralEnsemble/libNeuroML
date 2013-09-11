from neuroml import loaders
import neuroml

doc = loaders.NeuroMLLoader.load('./test_files/Purk2M9s.nml')

sample_cell = doc.cells[0]

#extract the morphology:
sample_morphology = sample_cell.morphology

#randomly  change a segment id:
sample_morphology.segments[33].id = 'random_test'

newcell = neuroml.Cell()
newcell.id = "some random cell"

new_morphology = neuroml.Morphology()
newcell.morphology = new_morphology

new_morphology.id = 'some random morphology'

#add a few segments to that morphology:
for i in range(10):
    segment = neuroml.Segment()
    segment.id = "some random segment"
    new_morphology.add_segment(segment)

doc.add_cell(newcell)

f = open('./tmp/test_load_and_manipulate.xml','w')
doc.export(f,0)
