from weather import Weather  

class Thermostat:
    def __init__(self, weather=None):
        self.weather = weather
        if self.weather is None:
            self.weather = Weather() 
        self.temperature = self.weather.current_temperature
        self.heating = False
        self.cooling = False

    def turn_on_heating(self):
        self.heating = True

    def turn_off_heating(self):
        self.heating = False

    def turn_on_cooling(self):
        self.cooling = True

    def turn_off_cooling(self):
        self.cooling = False

    def control_temperature(self):
        self.temperature = self.weather.current_temperature

        if self.temperature < 19.0:
            self.turn_on_heating()
        elif self.temperature >= 23.0:
            self.turn_off_heating()

        if self.temperature > 28.0:
            self.turn_on_cooling()
        elif self.temperature <= 23.0:
            self.turn_off_cooling()

my_thermostat = Thermostat()  # Create a Thermostat with the default Weather object


my_thermostat.control_temperature()
print("\nOptions:")
print("1. Turn on heating")
print("2. Turn off heating")
print("3. Turn on cooling")
print("4. Turn off cooling")
choice = input("Select an option: ")
if choice == "1":
    try:
        new_temp = float(input("Enter the desired temperature (in °C): "))
        my_thermostat.temperature = new_temp
        print(f"Temperature set to {new_temp}°C")
    except ValueError:
        print("Invalid input. Please enter a valid temperature value.")
elif choice == "2":
    my_thermostat.turn_on_heating()
    print("Heating turned on.")
elif choice == "3":
    my_thermostat.turn_on_cooling()
    print("Cooling turned on.")
elif choice == "4":
    my_thermostat.turn_off_cooling()
    print("Cooling turned off.")
else:
    print("Invalid choice. Please select a valid option.")
# Print the current temperature
print(f"Current temperature: {my_thermostat.temperature}°C")


