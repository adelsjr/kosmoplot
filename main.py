import json
import requests
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord
import time
import datasources.datasources as ds

session = requests.Session

def fetch_stardata(config):
    url = config.get("ninja-api", "endpoint") + "/" + config.get("ninja-api", "resource")
    api_key = config.get("ninja-api", "api_key")
    offset = 0
    limit = 30
    constellation = 'orion'
    headers = {'X-Api-Key': api_key}
    raw_data = []
    while True:
        params = {'limit': limit, 'offset': offset, 'constellation': constellation }
        r = requests.get(url, headers=headers, params=params)
        data = json.loads(r.text)
        if not data:
            print('cai no if not')
            break
        for i in data:
            raw_data.append(i)
        offset = limit + offset
    return raw_data


def enrich_stardata(raw_data):
    enriched_data = []
    for i in raw_data:
        i.update({"declination": i["declination"].replace(u"\u00a0", " ")})
        i.update({"apparent_magnitude": i["apparent_magnitude"].replace(u"\u2212", "-")})
        enriched_data.append(i)
    return enriched_data

    #with open("output.json", "w") as write_file:
    #    json.dump(output, write_file, indent=4)

def plot_stars_2d():
    # Load the JSON data
    with open("output.json", "r") as f:
        data = json.load(f)

    visible = [obj for obj in data if obj["apparent_magnitude"] and float(obj["apparent_magnitude"]) < 3]
    not_visible = [obj for obj in data if obj["apparent_magnitude"] and float(obj["apparent_magnitude"]) > 3]

    # Create a list of objects with apparent magnitude less than 2
    #bright_objects = [obj for obj in data if obj["apparent_magnitude"] and float(obj["apparent_magnitude"]) < 3]

    # Extract RA and DEC values from the filtered list
    #ra_list = [obj["right_ascension"] for obj in bright_objects]
    #dec_list = [obj["declination"] for obj in bright_objects]

    visible_ra_list = [obj["right_ascension"] for obj in visible]
    visible_dec_list = [obj["declination"] for obj in visible]
    visible_disctance_list = [obj["apparent_magnitude"] for obj in visible]

    # Create SkyCoord objects
    #c = SkyCoord(ra=ra_list, dec=dec_list)
    c_visible = SkyCoord(ra=visible_ra_list, dec=visible_dec_list)

    # Extract RA and DEC values for plotting
    ra_plot = c_visible.ra.hour  # RA in hours
    dec_plot = c_visible.dec.degree  # DEC in degrees

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the stars
    ax.scatter(ra_plot, dec_plot, s=40, marker='o', color='blue')

    # Add annotations for the star names
    for i in range(len(bright_objects)):
        ax.annotate(bright_objects[i]["name"], (ra_plot[i], dec_plot[i]), size=10)

    # Set labels and title
    ax.set_xlabel("Right Ascension (RA) [hours]", labelpad=10)
    ax.set_ylabel("Declination (DEC) [degrees]", labelpad=10)
    ax.set_title("Equatorial Coordinates Plot", fontsize=16)

    # Adjust the plot layout
    plt.xlim(0, 24)  # Set RA limits to 0-24 hours
    plt.ylim(-90, 90)  # Set DEC limits to -90 to 90 degrees
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Invert the y-axis to match celestial coordinates convention
    plt.gca().invert_yaxis()

    plt.show()

def plot_stars_3d(data):
    def magnitude_to_size(magnitude, factor):
    #    brightness = 10**(-magnitude/2.5)
        brightness = float(magnitude)
        return brightness * factor
    
    # Load the JSON data
    #with open("output.json", "r") as f:
    #    data = json.load(f)

    visible = [obj for obj in data if obj["apparent_magnitude"] and float(obj["apparent_magnitude"]) < 3]
    not_visible = [obj for obj in data if (obj["distance_light_year"]) and (obj["apparent_magnitude"]) and float(obj["apparent_magnitude"]) > 3 and float(obj["distance_light_year"].replace(",", "")) < 2000 ]


    not_visible_ra_list = [obj["right_ascension"] for obj in not_visible]
    not_visible_dec_list = [obj["declination"] for obj in not_visible]
    not_visible_distance_list = [float(obj["distance_light_year"].replace(",", "")) * u.lightyear for obj in not_visible]

    not_visible_size_list = [magnitude_to_size(obj["apparent_magnitude"],30) for obj in not_visible]

    c_not_visible = SkyCoord(ra=not_visible_ra_list, dec=not_visible_dec_list, distance=not_visible_distance_list)

    not_visible_z = c_not_visible.dec.degree
    not_visible_x = c_not_visible.ra.hour
    not_visible_y = c_not_visible.distance.lyr

    visible_ra_list = [obj["right_ascension"] for obj in visible]
    visible_dec_list = [obj["declination"] for obj in visible]
    visible_distance_list = [float(obj["distance_light_year"]) * u.lightyear for obj in visible]

    not_visible_size_list = [magnitude_to_size(obj["apparent_magnitude"],2) for obj in not_visible]

    c_visible = SkyCoord(ra=visible_ra_list, dec=visible_dec_list, distance=visible_distance_list)

    z = c_visible.dec.degree
    x = c_visible.ra.hour
    y = c_visible.distance.lyr

    visible_size_list = [magnitude_to_size(obj["apparent_magnitude"],20) for obj in visible]

    # Create a list of objects with apparent magnitude less than 2
    #bright_objects = [obj for obj in data if obj["apparent_magnitude"] and float(obj["apparent_magnitude"]) < 3]

    # Define size based on aparent_magnitude
    #size_list = [magnitude_to_size(obj["apparent_magnitude"],30) for obj in bright_objects]
    

    # Extract RA, DEC and distance values from the filtered list
    #ra_list = [obj["right_ascension"] for obj in bright_objects]
    #dec_list = [obj["declination"] for obj in bright_objects]
    #distance_list = [float(obj["distance_light_year"]) * u.lightyear for obj in bright_objects]

    # Create SkyCoord objects
    #c = SkyCoord(ra=ra_list, dec=dec_list, distance=distance_list)

    # Extract RA and DEC values for plotting
    #z = c.dec.degree
    #x = c.ra.hour
    #y = c.distance.lightyear

    # Create the plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection='3d')

    # Plot the stars
    #ax.scatter(x,y,z, s=size_list, marker='o', color='green')
    #ax.scatter(x,y,z, s=visible_size_list, marker='o', color='blue')
    ax.scatter(x,y,z, s=60, marker='o', color='blue')
    ax.scatter(not_visible_x,not_visible_y,not_visible_z, s=not_visible_size_list, marker='o', color='black', alpha=0.25)

    # Set a 2D init to view constellation
    ax.view_init(elev=1, azim=90, roll=0)

    # Add annotations for the star names
    for i in range(len(visible)):
        ax.text(x[i], y[i], z[i], visible[i]["name"]) #, (ra_plot[i], dec_plot[i]), size=10)

    # Set labels and title
    ax.set_xlabel("Right Ascension", labelpad=4)
    ax.set_zlabel("Declination", labelpad=4)
    ax.set_ylabel("Distance [ly]", fontsize=4)

    #ax.set_zscale('log')
    # Adjust the plot layout
    #plt.xlim(0, 24)  # Set RA limits to 0-24 hours
    #plt.ylim(-90, 90)  # Set DEC limits to -90 to 90 degrees
    #plt.xticks(fontsize=12)
    #plt.yticks(fontsize=12)

    # Invert the y-axis to match celestial coordinates convention
    plt.gca().invert_yaxis()
    ax.invert_zaxis()

    plt.show()



#class CosmosConfigValidator:
#    def __init__(self, config) -> None:
#        self.config = config


#class CosmosDataFetcher:
#    def __init__(self, config: DataSourceConfigValidator):
#        self.config = config
#        self.session = requests.Session()
#
#    def fetch_data(self) -> list:
#        output = []
#        offset = 0
#        while True:
#            params = {""}

#def main():
ds_config = ds.DataSourceConfig("datasources.ini")
config = ds_config.get_config()
ds_config_rest = ds.ValidatorRest()

for section in ds_config.get_types("REST"):
    if ds_config_rest.validate_datasource_config(section, ds_config.get_config()):
        print("valid rest")
    else:
        print("invalid rest")

raw_star_data = fetch_stardata(config)
enriched_star_data = enrich_stardata(raw_star_data)
plot_stars_3d(enriched_star_data)

