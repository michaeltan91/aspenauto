
# Example Usage

## Loading the Interface
```python
# Load an Aspen Plus backup file
from aspenauto import Model
M1 = Model('M1 Methanol.bkp')
```

## Simulation Commands
```python
# Running the simulation
M1.run()
# Resetting the simulation
M1.reset()
# Close the Aspen Plus simulation
M1.close()
```


## Streams 
Units are equal to the standard units used in your Aspen Plus simulation.
Will change in a future build.
### Data Access
Accessing data requires the simulation to have been solved.
```python
# View all streams in the Aspen Plus simulation
M1.streams
# Access a specific stream in the Aspen Plus simulation (material stream).
M1.streams['S-101']
# Get the temperature of a specific stream in the Aspen Plus simulation
M1.streams['S-101'].temperature
# Get the pressure of the stream
M1.streams['S-101'].pressure
# Get the mass flow of the stream
M1.streams['S-101'].massflow
# Get the mole flow of the stream
M1.streams['S-101'].moleflow
# Get the volumetric flow of the stream
M1.streams['S-101'].volflow
# Get the mass fraction of all components in the stream
M1.streams['S-101'].massfrac
# Get the mole fractions of all components in the stream
M1.streams['S-101'].molefrac

# Access all material streams
M1.material_streams
# Access all heat streams
M1.heat_streams
# Access all work streams
M1.work_streams
```
Note: all streamtypes have different properties e.g. you can cannot request the temperature of a heat stream.
```python
# Quickly accessing the temperature of all material streams
for stream in M1.material_streams:
    print(stream.name, stream.temperature)
# Quickly accessing the massfrac of all material streams
for stream in M1.material_streams:
    print(stream.name, stream.massfrac)
```
All possible stream properties can be called by:
```python
# Check the possible property values that can be retrieved for the stream. e.g. temperature
M1.streams['S-101'].properties
# Check the fractional property values that can be retrieved for the stream. e.g. massfrac
M1.streams['S-101'].properties_frac
```
### Data maniplulation
Note: 
You can only set the value of a "feed" stream, any design spec/calulator will override your value.

```python
# Set the mass flow of a stream
M1.streams['F-CH4'].massflow = 1000
# Reset and re-run the model for your changes to have effect
M1.reset()
M1.run()

# Set the temperature of a stream
M1.streams['F-CH4'].temperature = 40
# Set the pressure of a stream
M1.streams['F-CH4'].pressure = 10
# Set the mass fractions of each components in the stream
M1.streams['F-CH4'].massfrac = {'CH4':0.96, 'H2O':0.04}
```


## Utilities
Accessing data requires the simulation to have been solved.
```python
# Access all utilities. Provides a dict of all utilities defined in the Aspen Plus simulation
M1.utilities
# Access a specific utility, e.g. coolwater utility named 'CW'. 
# Provides a dict of all blocks using that utility in the Aspen Plus simulation.
M1.utilities['CW'] 
# Access the utility and a specific block where the utility is used
M1.utilities['CW']['B1']
# Get the utility usage
M1.utilities['CW']['B1'].usage
# Get the utility duty
M1.utilities['CW']['B1'].duty

# Access all coolwater utilities
M1.coolwater
# Access all electricity utilities
M1.electricity
# Access all steam usage utilities
M1.steam
# Access all steam generation utilities
M1.steam_gen
# Access all refrigerator utilities
M1.refrigerant 
# Access all natural gas utilities
M1.natural_gas
# All utilities are stored in the similiar manner as the utilities dict.
# e.g. access the coolwater for block B1 as
M1.utilities['CW']['B1']
M1.coolwater['CW']['B1']

# Quickly accessing and storing the total utility usage per utility
total = {}
for util_name, util in M1.utilities.items():
    total[util_name] = sum(block.usage for block in util)
```


## Blocks (WIP)
Accessing data requires the simulation to be solved
```python
# Access all blocks
M1.blocks
# Access a specific block
M1.blocks['B1']
