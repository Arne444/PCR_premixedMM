## Code to make a PCR reaction using a pre-mixed master-mix, distribute it between wells of a 96-well plate and add 10 different DNA samples.

from opentrons import robot, containers, instruments

source_tubes = containers.load('tube-rack-2ml', 'D2', 'tube rack')
dna_tubes = containers.load('tube-rack-2ml', 'C3', 'dna rack')
output = containers.load('96-PCR-flat', 'C1', 'output')

p20rack = containers.load('tiprack-10ul-H', 'B2', 'p20-rack')
trash = containers.load('trash-box', 'A3')

p20 = instruments.Pipette(
    trash_container=trash,
    tip_racks=[p20rack],
    min_volume=2,
    max_volume=20,
    axis="a"
)

total_volume = 25
DNA_volumes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
num_pcr_samples = len(DNA_volumes)
DNA_sources = dna_tubes.wells('A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3', 'A4')

master_mix = source_tubes.wells('B1')
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