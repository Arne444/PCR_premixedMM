## Code to make a PCR reaction using a pre-mixed master-mix, distribute it between wells 
## of a 96-well plate, add primers and add a given number of template samples.

###INPUT### PCR variables
num_replicates = 3
num_templates = 2
num_primers = 2

total_PCR_volume = 25
master_mix_volume = 10
template_volume = 2
primer_volume = 2.5

from opentrons import robot, containers, instruments

#Define containers - source_tube rack = cold block
output = containers.load('96-PCR-flat', 'C1', 'output')
trash = containers.load('trash-box', 'A3')

#Create 6x12 p20 tip rack container
containers.create(
	'tiprack-200ul-6x12',
	grid=(6,12),
	spacing=(9, 9),
	diameter=5,
	depth=60
)

p20rack1 = containers.load('tiprack-200ul-6x12', 'B3', 'p20_rack1')
p20rack2 = containers.load('tiprack-200ul-6x12', 'B2', 'p20_rack2')

#Create 3x6 2ml tube rack for DNA samples
containers.create(
	'3x6-tube-rack-2ml',
	grid=(3,6),
	spacing=(19.5,19.5),
	diameter=9.5,
	depth=40
)

template_rack = containers.load('3x6-tube-rack-2ml', 'E1', 'template_rack')
source_tubes = containers.load('3x6-tube-rack-2ml', 'E3', 'tube_rack')

#Define pipette
p20 = instruments.Pipette(
    trash_container=trash,
    tip_racks=[p20rack1, p20rack2],
    min_volume=2,
    max_volume=20,
    axis="a"
)

#Define locations of PCR components
water_source = source_tubes.wells('A1')
master_mix_source = source_tubes.wells('A2')
F_primer_source = source_tubes.wells('B2')
R_primer_source = source_tubes.wells('C2')

#Define DNA volumes to be added
template_volumes = [template_volume] * num_templates
num_pcr_samples = len(DNA_volumes)
template_sources = template_rack.wells('A1', length=num_pcr_samples)
water_volume = total_PCR_volume - master_mix_volume - (2*primer_volume) - template_volume

#Add water
for i in range(len(water_volumes)):
	p20.transfer(
		water_volume, water_source, output.wells(i*num_replicates, 
		length=(num_replicates),skip=8), blow_out=True, touch_tip=True)

#distribute MasterMix
for i in range(len(template_volumes)):
	p20.transfer(
		master_mix_volume, master_mix_source, output.wells(i*num_replicates, 
		length=(num_replicates), skip=8), blow_out=True, touch_tip=True)
		
#distribute F primer
for i in range(len(template_volumes)):
	p20.transfer(
		primer_volume, F_primer_source, output.wells(i*num_replicates, 
		length=(num_replicates), skip=8), mix_after=(3, 3), blow_out=True, touch_tip=True, new_tip='always')

#distribute R primer
for i in range(len(template_volumes)):
	p20.transfer(
		primer_volume, R_primer_source, output.wells(i*num_replicates, 
		length=(num_replicates), skip=8), mix_after=(3, 3), blow_out=True, touch_tip=True, new_tip='always')
	
#distribute template DNA
for i in range(len(template_volumes)):
	p20.transfer(
		template_volumes[i], template_sources(i), output.wells(i*num_replicates, 
		length=(num_replicates), skip=8), mix_after=(3, 20), blow_out=True, 
		touch_tip=True, new_tip='always')
