open_checkpoint ./checkpoints/slr_crosser_vu13p.dcp
set all_laguna_sites [get_sites -filter {NAME =~ "LAGUNA*"}]
set laguna_num [llength $all_laguna_sites]
puts "total $laguna_num LAGUNA sites: $all_laguna_sites"
