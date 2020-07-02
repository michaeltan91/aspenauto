
```python

# Example usage

# Load an Aspen Plus backup file
from aspenauto import Process
M1 = Process('M1 Methanol.bkp')



# Run the Aspen Plus simulation 
M1.run()
# View all streams in the Aspen Plus simulation
M1.streams
# Access a specific stream in the Aspen Plus simulation
M1.streams['S-101']
# Access the temperature property of a specific stream in the Aspen Plus simulation
M1.streams['S-101'].temperature
