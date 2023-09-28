open_checkpoint ./checkpoints/picoblaze_synth.dcp

create_pblock pblock_1
# Error PBLOCK, too tight
# resize_pblock pblock_1 -add {SLICE_X27Y60:SLICE_X29Y64 RAMB18_X2Y24:RAMB18_X2Y25 RAMB36_X2Y12:RAMB36_X2Y12}
# Correct PBLOCK: since BRAM tiles are stacked vertically,
# we must grow horizontally to ensure that we can step and repeat
# without blocking access to other BRAMs with used SLICEs.
resize_pblock pblock_1 -add {SLICE_X26Y60:SLICE_X29Y64 RAMB18_X2Y24:RAMB18_X2Y25 RAMB36_X2Y12:RAMB36_X2Y12}
add_cells_to_pblock pblock_1 -top
# Ensure that the implementation is more amenable to relocation (can be more densely packed).
set_property CONTAIN_ROUTING 1 [get_pblocks pblock_1]

puts "current Vivado mode: $rdi::mode"
if { $rdi::mode eq "gui" } {
    select_objects [get_pblocks pblock_1]
    get_property GRID_RANGES [get_selected_objects]
}

create_clock -period 2.5 -name clk -waveform {0.000 1.25} [get_ports clk]
set_property HD.CLK_SRC BUFGCTRL_X0Y2 [get_ports clk]

place_design
route_design
report_utilization -pblocks pblock_1
select_objects [get_pblocks pblock_1]
