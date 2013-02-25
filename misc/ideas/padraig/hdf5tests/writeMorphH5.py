import h5py
f = h5py.File('testMorph.hdf', 'w')
f.attrs['neurohdf_version'] = '0.1'

num_points = 200
num_cells = 10

neuroml = f.create_group("neuroml")

neuroml.attrs["id"] = "tester"


cell1 = neuroml.create_group("cell__cell1")
cell1.attrs["id"] = "cell1"


points = cell1.create_dataset("points", (num_points, 4), 'f')

for i in range(num_points):
    points[i] = (i*0.1,i*0.1,i*0.1,3)


pop1 = neuroml.create_group("population__pop1")
pop1.attrs["id"] = "pop1"
pop1.attrs["cell"] = cell1.attrs["id"]
pop1.attrs["size"] = num_cells

pop2 = neuroml.create_group("population__pop2")
pop2.attrs["id"] = "pop2"
pop2.attrs["size"] = num_cells



f.close()

    