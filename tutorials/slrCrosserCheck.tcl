open_checkpoint ./checkpoints/slr_crosser_vu7p_32.dcp
create_clock -name clk -period 1.333 [get_nets clk]
report_timing_summary -delay_type min_max -report_unconstrained -check_timing_verbose -max_paths 10 -input_pins -routable_nets -name timing_1
close_design

open_checkpoint ./checkpoints/synth32_BB.dcp
read_checkpoint -cell crossing ./checkpoints/slr_crosser_vu7p_32.dcp
# Add pblocks
create_pblock pblock_top
add_cells_to_pblock pblock_top [get_cells [list T_top]] -clear_locs
resize_pblock [get_pblocks pblock_top] -add {CLOCKREGION_X5Y5:CLOCKREGION_X5Y5}
create_pblock pblock_bot
add_cells_to_pblock pblock_bot [get_cells [list T_bot]] -clear_locs
resize_pblock [get_pblocks pblock_bot] -add {CLOCKREGION_X5Y4:CLOCKREGION_X5Y4}
# Implement design and save
place_design
route_design
write_checkpoint -force ./checkpoints/routed_32.dcp

# report to GUI
report_timing_summary -delay_type min_max -report_unconstrained -check_timing_verbose -max_paths 10 -input_pins -routable_nets -name timing_all
report_timing -from {*/input0_north_reg*} -delay_type min_max -max_paths 10 -sort_by group -input_pins -name timing_North
report_timing -from {*/output0_north_reg*} -delay_type min_max -max_paths 10 -sort_by group -input_pins -name timing_North_after
report_timing -to {*/input0_north_reg*} -delay_type min_max -max_paths 10 -sort_by group -input_pins -name timing_North_before
report_timing -from {*/input0_south_reg*} -delay_type min_max -max_paths 10 -sort_by group -input_pins -name timing_South
report_timing -from {*/output0_south_reg*} -delay_type min -max_paths 10 -sort_by group -input_pins -name timing_South_after
report_timing -to {*/input0_south_reg*} -delay_type min_max -max_paths 10 -sort_by group -input_pins -name timing_South_before
