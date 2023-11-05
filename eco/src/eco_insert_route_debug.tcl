open_checkpoint ../checkpoints/boom_medium_routed.dcp
# Mark debug true
set_property mark_debug true [get_nets tl_slave_0_a_bits_data_OBUF*]
# Write the design
write_checkpoint -force eco_input.dcp
write_edif -force eco_input.edf
# Execute the EcoInsertRouteDebugApp.jar and display its output upon exit
puts [exec java -jar EcoInsertRouteDebugApp.jar eco_input.dcp eco_output.dcp]
# Close the old checkpoint
close_design
# Re-open the modified checkpoint
open_checkpoint eco_output.dcp
# Check design is fully routed
report_route_status
# Find all signals marked for debug and display them in a new GUI tab
show_objects -name find_1 [get_nets -hierarchical -top_net_of_hierarchical_group -filter { MARK_DEBUG == "TRUE" } ]
