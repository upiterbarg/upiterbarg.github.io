# ------------------------- IMPORTS -------------------------

import pandas as pd
import numpy as np
import os
import sys
import pycountry
import reverse_geocode
import pycountry_convert as pc


# -------------------- GLOBAL VARIABLES ---------------------

# Cell size for defining home location
CELL = 25


# ------------------------ FUNCTIONS ------------------------


# Function to convert km to latitude
def km_to_lat(km):
    # Input:
    # -- km: a scalar of a distance in kilometers
    # Output:
    # -- a scalar of the converted distance in degrees (latitude)

    return 180 * km / (np.pi * 6371)


# Function to convert km to longitude
def km_to_lon(lat, km):
    # Input:
    # -- lat: a scalar of the latitude to consider for the calculation
    # -- km: a scalar of a distance in kilometers
    # Output:
    # -- a scalar of the converted distance in degrees (longitude)

    return 180 * km / (np.pi * 6371 * np.cos(lat * np.pi / 180))


# Function to add discretised latitude and longitude values to dataframe
def discretise_checkins(checkins_df):
    # Input:
    # -- checkins_df: a pandas dataframe containing check-in information
    # Output:
    # -- checkins_discrete_df: a pandas dataframe containing the discretised check-in information

    # Copy input
    checkins_discrete_df = checkins_df.copy()

    # Calculate index and discrete value of latitude
    index_lat = ((90 + checkins_discrete_df.latitude) / km_to_lat(CELL)).astype(int)
    discrete_lat = index_lat * km_to_lat(CELL) - 90

    # Calculate index and discrete value of longitude
    index_lon = (
        (180 + checkins_discrete_df.longitude) / km_to_lon(discrete_lat, CELL)
    ).astype(int)
    discrete_lon = index_lon * km_to_lon(discrete_lat, CELL) - 180

    # Add columns to dataframe
    checkins_discrete_df["discrete latitude"] = discrete_lat
    checkins_discrete_df["discrete longitude"] = discrete_lon
    checkins_discrete_df["position index"] = (
        index_lat.astype(str) + "-" + index_lon.astype(str)
    )

    return checkins_discrete_df


# Function to find home cells
def find_home_cells(checkins_discrete_df):
    # Input:
    # -- checkins_discrete_df: a pandas dataframe containing discretised check-in information
    # Output:
    # -- home_cell_df: a pandas dataframe containing the home cell information for each user

    # Group by user and position index and count amount of position indexes
    home_cell_df = checkins_discrete_df.groupby(
        ["user", "discrete latitude", "discrete longitude", "position index"],
        as_index=False,
    )["latitude"].count()

    # Group by user and select max number of position indexes
    home_cell_df = home_cell_df.loc[home_cell_df.groupby("user")["latitude"].idxmax()]

    # Reformat and rename data
    home_cell_df = home_cell_df.drop(["position index", "latitude"], axis=1)
    home_cell_df.columns = ["user", "home cell latitude", "home cell longitude"]

    return home_cell_df


# Function that finds user homes
def find_homes(checkins_df, home_cell_df):
    # Input:
    # -- checkins_df: a pandas dataframe containing check-in information
    # -- home_cell_df: a pandas dataframe containing discretised check-in information
    # Output:
    # -- home_df: a pandas dataframe containing the home location of each user

    # Merge checkins dataframe with home cell dataframe
    home_df = pd.merge(checkins_df, home_cell_df, on="user")

    # Keep checkins within home cell
    home_df = home_df[
        (home_df["latitude"] >= home_df["home cell latitude"])
        & (home_df["latitude"] < home_df["home cell latitude"] + km_to_lat(CELL))
    ]

    home_df = home_df[
        (home_df["longitude"] >= home_df["home cell longitude"])
        & (
            home_df["longitude"]
            < home_df["home cell longitude"]
            + km_to_lon(home_df["home cell latitude"], CELL)
        )
    ]

    # Group by user for mean latitude and longitude
    home_df = home_df.groupby("user", as_index=False)[["latitude", "longitude"]].mean()

    # Rename and Visualize data
    home_df.columns = ["user", "home latitude", "home longitude"]

    return home_df


# Function that creates dataframe with friendships and locations
def user_friend_location(edges_df, home_df):
    # Input:
    # -- edges_df: a pandas dataframe containing frienship networks
    # -- home_df: a pandas dataframe containing the home location of each user
    # Output:
    # -- edge_location_df: a pandas dataframe containing the and frienship networks the home location of each user

    # Create new datagram by merging edges and homes to show user home location
    edge_location_df = pd.merge(edges_df, home_df, on="user")

    # Create new dataframe from user homes, with new names to merge with edges dataframe
    friend_df = home_df.copy()
    friend_df.columns = ["friendship", "friend latitude", "friend longitude"]

    # Merge with previous dataframe to have user friendships, home location and friend home locations
    edge_location_df = pd.merge(edge_location_df, friend_df, on="friendship")

    # Sort by user and friendship and reset index to stay consistent
    edge_location_df = edge_location_df.sort_values(
        by=["user", "friendship"]
    ).reset_index(drop=True)

    return edge_location_df


# Function that converts iso alpha 2 country code to iso alpha 3
def alpha2_to_alpha3(code):
    # Input:
    # -- code: iso alpha 2 country code
    # Output:
    # -- Nan or iso alpha 3 country code

    # Get info from iso alpha 2 code
    country_info = pycountry.countries.get(alpha_2=code)

    # Convert to alpha 3 if exists
    if country_info is None:
        return np.nan
    else:
        return country_info.alpha_3


# Function that converts iso alpha 2 country code to country name
def alpha2_to_name(code):
    # Input:
    # -- code: iso alpha 2 country code
    # Output:
    # -- Nan or iso alpha 3 country code

    # Get info from iso alpha 2 code
    country_info = pycountry.countries.get(alpha_2=code)

    # Convert to country name if exists
    if country_info is None:
        return np.nan
    else:
        return country_info.name


# Function that gets iso alpha 3 country code from latitude and longitude
def get_country_code(lat, lon):
    # Input:
    # -- lat: location latitude
    # -- lon: location longitude
    # Output:
    # -- Nan or iso alpha 3 country code

    # Convert latitude and longitude to iso alpha 2 code
    country_code = reverse_geocode.search(((lat, lon), (lat, lon)))[0].get(
        "country_code"
    )

    if country_code == "IM":
        country_code = "GB"

    # Return iso alpha 3 country code
    return alpha2_to_alpha3(country_code)


# Function that gets country name code from latitude and longitude
def get_country_name(lat, lon):
    # Input:
    # -- lat: location latitude
    # -- lon: location longitude
    # Output:
    # -- Nan or iso alpha 3 country code

    # Convert latitude and longitude to iso alpha 2 code
    country_code = reverse_geocode.search(((lat, lon), (lat, lon)))[0].get(
        "country_code"
    )

    if country_code == "IM":
        country_code = "GB"

    # Return country name
    return alpha2_to_name(country_code)


# Function that converts iso alpha 2 country code to iso alpha 3
def alpha3_to_alpha2(code):
    # Input:
    # -- code: iso alpha 2 country code
    # Output:
    # -- Nan or iso alpha 3 country code

    # Get info from iso alpha 2 code
    country_info = pycountry.countries.get(alpha_3=code)

    # Convert to alpha 3 if exists
    if country_info is None:
        return np.nan
    else:
        return country_info.alpha_2


def get_continent_name(code):
    # Input:
    # -- code: iso alpha 3 country code
    # Output:
    # -- continent: name of the continent

    # Create continent variable
    continent = np.nan

    # Convert iso alpha 3 code to iso alpha 2 code
    country_code = alpha3_to_alpha2(code)
    if country_code == "VA":
        country_code = "IT"
    elif country_code == "SX":
        country_code = "NL"

    # Convert is alpha 2 code to continent code
    continent_code = pc.country_alpha2_to_continent_code(country_code)

    # Convert continent code to continent name
    if continent_code == "NA":
        continent = "North America"
    elif continent_code == "SA":
        continent = "South America"
    elif continent_code == "AF":
        continent = "Africa"
    elif continent_code == "AS":
        continent = "Asia"
    elif continent_code == "EU":
        continent = "Europe"

    # Return continent name
    return continent


# function that returns smallest array size where sum is above threshold
def smallest_subset_size(arr, x):
    # Initialize current sum and minimum length
    n = len(arr)
    curr_sum = 0
    min_len = n + 1

    # Initialize starting and ending indexes
    start = 0
    end = 0
    while end < n:
        # Keep adding array elements while current
        # sum is smaller than x
        while curr_sum <= x and end < n:
            curr_sum += arr[end]
            end += 1

        # If current sum becomes greater than x.
        while curr_sum > x and start < n:
            # Update minimum length if needed
            if end - start < min_len:
                min_len = end - start

            # remove starting elements
            curr_sum -= arr[start]
            start += 1

    return min_len


# Function that converts geographical coordinates to distance in km
def geo_to_km(lat_0_deg, lon_0_deg, lat_1_deg, lon_1_deg):
    # Input:
    # -- lat_0_deg: a scalar of latitude of location 0
    # -- lon_0_deg: a scalar of longitude of location 0
    # -- lat_1_deg: a scalar of latitude of location 1
    # -- lon_1_deg: a scalar of longitude of location 1
    # Output:
    # -- d: a scalar of the distance between location 0 and 1

    lat_0 = np.deg2rad(lat_0_deg)
    lon_0 = np.deg2rad(lon_0_deg)
    lat_1 = np.deg2rad(lat_1_deg)
    lon_1 = np.deg2rad(lon_1_deg)
    d_lat = lat_1 - lat_0
    lon_1 = np.deg2rad(lon_1_deg)

    a = np.sin(d_lat / 2) ** 2 + np.cos(lat_0) * np.cos(lat_1) * np.sin(d_lon / 2) ** 2
    d = 6371 * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return d
    d_lon = lon_1 - lon_0
    lon_1 = np.deg2rad(lon_1_deg)
