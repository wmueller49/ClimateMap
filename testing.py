import geopandas
import pandas as pd
import datetime

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
YEAR = 1900

temp_data = pd.read_csv("archive/GlobalLandTemperaturesByCountry.csv")

temp_data.loc[temp_data['Country'] == "Burma", "Country"] = "Myanmar"
temp_data.loc[temp_data['Country'] == "Bosnia And Herzegovina", "Country"] = "Bosnia and Herz."
temp_data.loc[temp_data['Country'] == "Central African Republic", "Country"] = "Central African Rep."
temp_data.loc[temp_data['Country'] == "Congo (Democratic Republic Of The)", "Country"] = "Dem. Rep. Congo"
temp_data.loc[temp_data['Country'] == "Côte D'Ivoire", "Country"] = "Côte d'Ivoire"
temp_data.loc[temp_data['Country'] == "Denmark (Europe)", "Country"] = "Denmark"
temp_data.loc[temp_data['Country'] == "Dominican Republic", "Country"] = "Dominican Rep."
temp_data.loc[temp_data['Country'] == "Equatorial Guinea", "Country"] = "Eq. Guinea"
temp_data.loc[temp_data['Country'] == "Falkland Islands (Islas Malvinas)", "Country"] = "Falkland Is."
temp_data.loc[temp_data['Country'] == "Central African Republic", "Country"] = "Central African Rep."
temp_data.loc[temp_data['Country'] == "Czech Republic", "Country"] = "Czechia"
temp_data.loc[temp_data['Country'] == "France (Europe)", "Country"] = "France"
temp_data.loc[temp_data['Country'] == "Guinea Bissau", "Country"] = "Guinea-Bissau"
temp_data.loc[temp_data['Country'] == "Macedonia", "Country"] = "North Macedonia"
temp_data.loc[temp_data['Country'] == "Netherlands (Europe)", "Country"] = "Netherlands"
temp_data.loc[temp_data['Country'] == "Palestina", "Country"] = "Palestine"
temp_data.loc[temp_data['Country'] == "Solomon Islands", "Country"] = "Solomon Is."
temp_data.loc[temp_data['Country'] == "Sudan", "Country"] = "S. Sudan"
temp_data.loc[temp_data['Country'] == "Timor Leste", "Country"] = "Timor-Leste"
temp_data.loc[temp_data['Country'] == "Trinidad And Tobago", "Country"] = "Trinidad and Tobago"
temp_data.loc[temp_data['Country'] == "United Kingdom (Europe)", "Country"] = "United Kingdom"
temp_data.loc[temp_data['Country'] == "United States", "Country"] = "United States of America"
temp_data.loc[temp_data['Country'] == "Western Sahara", "Country"] = "W. Sahara"


# temp_data.to_csv("archive/GlobalLandTempreaturesByCountry2.csv")


temp_data['dt'] = pd.to_datetime(temp_data['dt'])
temp_data = temp_data[temp_data['dt'].dt.year == YEAR]
temp_data = temp_data.groupby('Country', as_index=False)['AverageTemperature'].mean()


somaliland = world.loc[world['name'] == "Somaliland"]
sudan = world.loc[world['name'] == "Sudan"]



world = world.merge(temp_data, left_on='name', right_on='Country')
world = pd.concat([world, somaliland])
world = pd.concat([world, sudan])

world.loc[world["name"] == "Somaliland", "AverageTemperature"] = world[world['name'] == "Somalia"].AverageTemperature.values[0]
world.loc[world["name"] == "Sudan", "AverageTemperature"] = world[world['name'] == "S. Sudan"].AverageTemperature.values[0]

m = world.explore(column='AverageTemperature')

m.save('testing.html')