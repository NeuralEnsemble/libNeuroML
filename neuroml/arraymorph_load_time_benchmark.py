import numpy as np

import neuroml
import neuroml.arraymorph as am


class Benchmark:
    def __init__(self, num_segments):
        self.num_segments = num_segments

    def set_up(self):
        num_segments = int(1e4)  # Per cell
        num_vertices = num_segments + 1

        x = np.linspace(0, 10, num_vertices)
        y = np.zeros(num_vertices)
        z = np.zeros(num_vertices)
        d = np.linspace(1, 0.01, num_vertices)

        vertices = np.array([x, y, z, d]).T

        connectivity = range(-1, num_segments)

        big_arraymorph = am.ArrayMorphology(
            vertices=vertices, connectivity=connectivity
        )
        transposed_x = x + 10
        transposed_vertices = np.array([transposed_x, y, z, d]).T

        transposed_arraymorph = am.ArrayMorphology(
            vertices=transposed_vertices, connectivity=connectivity
        )

        bigger_d = d + 0.5
        fatter_vertices = np.array([x, y, z, bigger_d]).T

        fatter_arraymorph = am.ArrayMorphology(
            vertices=fatter_vertices, connectivity=connectivity
        )

        neuroml_cell = neuroml.Cell(id="cell_4")
        neuroml_morphology = neuroml.Morphology(id="my_morph")
        neuroml_cell.morphology = neuroml_morphology

        self.transposed_arraymorph = transposed_arraymorph
        self.fatter_arraymorph = fatter_arraymorph
        self.big_arraymorph = big_arraymorph

        self.cell_1 = neuroml.Cell(id="cell_1")
        self.cell_2 = neuroml.Cell(id="cell_2")
        self.cell_3 = neuroml.Cell(id="cell_3")

        self.cell_1.morphology = transposed_arraymorph
        self.cell_2.morphology = fatter_arraymorph
        self.cell_3.morphology = big_arraymorph

        self.test_doc = neuroml.NeuroMLDocument(id="TestDocument")

        self.test_doc.cells.append(self.cell_1)
        self.test_doc.cells.append(self.cell_2)
        self.test_doc.cells.append(self.cell_3)
        self.test_doc.cells.append(neuroml_cell)
