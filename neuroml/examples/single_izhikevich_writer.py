from neuroml import IzhikevichCell, NeuroMLDocument
from neuroml.utils import validate_neuroml2
from neuroml.writers import NeuroMLWriter


def write_izhikevich(filename="./tmp/SingleIzhikevich_test.nml"):
    nml_doc = NeuroMLDocument(id="SingleIzhikevich")
    nml_filename = filename

    iz0 = IzhikevichCell(
        id="iz0", v0="-70mV", thresh="30mV", a="0.02", b="0.2", c="-65.0", d="6"
    )

    nml_doc.izhikevich_cells.append(iz0)

    NeuroMLWriter.write(nml_doc, nml_filename)
    validate_neuroml2(nml_filename)


write_izhikevich()
