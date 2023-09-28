source ./kcu105.tcl

find_top
set_property top VexRiscv_1 [current_fileset]
reset_run synth_1
synth_design -mode out_of_context
write_checkpoint ./riscv_1_synth.dcp
# close_project
