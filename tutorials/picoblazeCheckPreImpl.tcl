open_checkpoint ./checkpoints/picoblaze_array_alt.dcp

update_clock_routing
route_design
report_timing_summary -delay_type min_max -report_unconstrained -check_timing_verbose -max_paths 10 -input_pins -routable_nets -name timing_1
