## Code to make a PCR reaction using a pre-mixed master-mix, distribute it between wells of a 96-well plate and add 10 different DNA samples.

from opentrons import robot, containers, instruments

#Define containers - source_tube rack = cold block
source_tubes = containers.load('tube-rack-2ml', 'E5', 'tube_rack')
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

p20rack = containers.load('tiprack-200ul-6x12', 'B2', 'p20_rack')

#Create 3x6 2ml tube rack for DNA samples
containers.create(
	'3x6-tube-rack-2ml',
	grid=(3,6),
	spacing=(19.5,19.5),
	diameter=9.5,
	depth=40
)

DNA_rack = containers.load('3x6-tube-rack-2ml', 'C3', 'DNA_rack')

#Define pipette
p20 = instruments.Pipette(
    trash_container=trash,
    tip_racks=[p20rack],
    min_volume=2,
    max_volume=20,
    axis="a"
)

#Define DNA volumes to be added
total_volume = 25
DNA_volumes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
num_pcr_samples = len(DNA_volumes)
DNA_sources = dna_tubes.wells('A1', length=num_pcr_samples)

#Define locations of master mix components
mix_location = source_tubes.wells('B1')
water_source = source_tubes.wells('C1')

#Distribute Master Mix
p20.distribute(
    12,
    master_mix,
    output.wells('A1', length=num_pcr_samples),
    blow_out=True,
    touch_tip=True,
    new_tip='always'
)

#Add DNA
p20.transfer(
    DNA_volumes,
    DNA_sources,
    output.wells('A1', length=num_pcr_samples),
    mix_after=(3, 4),
    blow_out=True,
    touch_tip=True,
    new_tip='always'
)

#Add water
water_volumes = []
for v in DNA_volumes:
    water_volumes.append(total_volume - v - 12)

p20.transfer(
    water_volumes,
    water_source,
    output.wells('A1', length=num_pcr_samples),
    mix_after=(3, 20),
    blow_out=True,
    touch_tip=True,
    new_tip='always'
)