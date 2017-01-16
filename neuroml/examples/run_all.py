print("Running all examples...")

def run_example(ex_file):
    print("-------------------------------------\nRunning %s"%ex_file)
    exec("import %s"%ex_file[:-3])
    print("-------------------------------------\nCompleted: %s"%ex_file)

run_example("arraymorph_generation.py")
run_example("build_3D_network.py")
run_example("build_network.py")
run_example("build_network2.py")
run_example("build_complete.py")
run_example("ion_channel_generation.py")
run_example("json_serialization.py")
run_example("loading_modifying_writing.py")
# This next one takes a while to run but all of its functionality is covered in loading_modifying_writing.py
#run_example("loading_modifying_writing_large.py")
run_example("morphology_generation.py")
run_example("write_pynn.py")
run_example("write_syns.py")
run_example("single_izhikevich_reader.py")
run_example("single_izhikevich_writer.py")
