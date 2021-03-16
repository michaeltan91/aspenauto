Aspenauto is an object oriented wrapper for Aspen Plus V8.8



# Example usage
```python
# load an Aspen Plus backup file
from aspenauto import Process
M1 = Process('M1. Methanol.bkp')
# run the model
M1.run()

# access stream properties
print(M1.streams['PS-CH3OH'].massflow)
print(M1.streams['PS-CH3OH'].massfrac)
print(M1.streams['PS-CH3OH'].pressure)
print(M1.streams['PS-CH3OH'].temperature)

# modify stream properties
M1.streams['PS-CH3OH'].massflow = 100
M1.streams['PS-CH3OH'].massfrac = []
M1.streams['PS-CH3OH'].pressure = 10
M1.streams['PS-CH3OH'].temperature = 400

# access block properties
print(M1.blocks['M1-E01'].pressure)
print(M1.blocks['M1-E01'].temperature)

# modifty block properties
M1.blocks['M1-E01'].temperature = 60
M1.blocks['M1-E01'].pressure = 10
```

# Requirements
*Python 3\
*Aspen Plus installation\
*Aspen Plus licence

