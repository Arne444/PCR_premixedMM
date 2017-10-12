## Code to make a PCR reaction using a pre-mixed master-mix, distribute it between wells 
## of a 96-well plate, add primers and add a given number of template samples.

###INPUT### PCR variables
num_replicates = 8
num_templates = 4

total_PCR_volume = 20
master_mix_volume = 8
template_volume = 1
primer_volume = 2.5

#Define primer pairs

from opentrons import robot, containers, instruments

#Define containers - source_tube rack = cold block
pcr_plate = containers.load('96-PCR-flat', 'B1', 'pcr-plate')
trash = containers.load('trash-box', 'A3')
p200rack = containers.load('tiprack-200ul', 'A1', 'p200-rack')

#Create 96-well trough
containers.create(
	'96-well-square',
	grid=(8,12),
	spacing=(9,9),
	diameter=7,
	depth=40
)

mix_trough = containers.load('96-well-square', 'B2', 'mix-trough')

#Create 6x12 p20 tip rack container
containers.create(
	'tiprack-200ul-6x12',
	grid=(6,12),
	spacing=(9, 9),
	diameter=5,
	depth=60
)

p20rack = containers.load('tiprack-200ul-6x12', 'E1', 'p20-rack')

#Create 3x6 2ml tube rack for DNA samples
containers.create(
	'3x6-tube-rack-2ml',
	grid=(3,6),
	spacing=(19.5,19.5),
	diameter=9.5,
	depth=40
)

template_primer_rack = containers.load('3x6-tube-rack-2ml', 'B3', 'template-primer-rack')
cold_rack = containers.load('3x6-tube-rack-2ml', 'D3', 'cold-rack')

#Define pipettes
p20 = instruments.Pipette(
    trash_container=trash,
    tip_racks=[p20rack],
    min_volume=2,
    max_volume=20,
    axis="a"
)

p200 = instruments.Pipette(
	trash_container=trash,
	tip_racks=[p200rack],
	min_volume=20,
	max_volume=200,
	axis="b"
)

#Define locations of PCR components
water_source = cold_rack.wells('A1')
master_mix_source = cold_rack.wells('A2')
template_sources = template_primer_rack.columns('A')
F_primer_sources = template_primer_rack.columns('B')
R_primer_sources = template_primer_rack.columns('C')

#Define DNA volumes to be added
template_volumes = [template_volume] * num_templates
num_pcr_samples = len(template_volumes)
water_volume = total_PCR_volume - master_mix_volume - (2*primer_volume) - template_volume

mix_trough_bottom = [well.bottom() for well in mix_trough.wells('A1', length=num_templates)]

p200.pick_up_tip()

#Add water
p200.distribute(
	water_volume*(num_replicates+1), water_source, mix_trough_bottom, new_tip='never', 
	blow_out=True, disposal_volume=10)

p200.drop_tip()

#distribute MasterMix
p200.distribute(
	master_mix_volume*(num_replicates+1), master_mix_source, mix_trough_bottom, blow_out=True,
	disposal_volume=10)

#distribute F primers
for i in range(len(template_volumes)):
	p200.transfer(
		primer_volume*(num_replicates+1), F_primer_sources(i), mix_trough.wells(i).bottom(), 
		mix_after=(2, 20), blow_out=True, new_tip='always')

#distribute R primers
for i in range(len(template_volumes)):
	p200.transfer(
		primer_volume*(num_replicates+1), R_primer_sources(i), mix_trough.wells(i).bottom(), 
		mix_after=(2, 20), blow_out=True, touch_tip=True, new_tip='always')

#distribute template DNA
for i in range(len(template_volumes)):
	p20.transfer(
		template_volume*(num_replicates+1), template_sources(i), mix_trough.wells(i).bottom(), 
		mix_after=(2, 10), blow_out=True, touch_tip=True, new_tip='always')

#distribute mixes to PCR plate
for i in range(len(template_volumes)):
	pcr_plate_bottom = [well.bottom() for well in pcr_plate.wells(i*num_replicates, 
	length=num_replicates, skip=8)]
	p200.distribute(
		total_PCR_volume, mix_trough(i), pcr_plate_bottom, mix_before=(5,200), disposal_volume=5, 
		dispense_speed=300)
