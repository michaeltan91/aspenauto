Aspenauto is an object oriented wrapper for Aspen Plus V8.8



# Example usage
```python
# load an Aspen Plus backup file
from aspenauto import Process
M1 = Process('M1. Methanol.bkp')
# run the model
M1.run()
# stream properties
print(M1.streams['PS-CH3OH'].massflow)
print(M1.streams['PS-CH3OH'].massfrac)
print(M1.streams['PS-CH3OH'].pressure)
print(M1.streams['PS-CH3OH'].temperature)
```
