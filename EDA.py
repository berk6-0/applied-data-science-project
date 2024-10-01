import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

listings = pd.read_csv('listings_oslo.csv')

# Create cleaner versions of dataset, one for private rooms and one for entire home/apt
listings_clean = listings.drop(['name', 'host_name', 'neighbourhood_group', 'neighbourhood', 
                                'minimum_nights', 'number_of_reviews', 'last_review', 'reviews_per_month',
                                'calculated_host_listings_count','availability_365', 
                                'number_of_reviews_ltm', 'license;'], axis='columns')
listings_nona = listings_clean.dropna()

listings_private = listings_nona.loc[listings_nona['room_type'] == 'Private room']
# print(listings_private.head(15))
listings_entire = listings_nona.loc[listings_nona['room_type'] == 'Entire home/apt']
# print(listings_entire.head(15))

average_price = sum(listings_nona['price'])/len(listings_nona)
stdv_price = np.std(listings_nona['price'])
print(f'Average price of all listings: {round(average_price)}\nStd: {round(stdv_price)}')

average_price_p = sum(listings_private['price'])/len(listings_private)
stdv_price_p = np.std(listings_private['price'])
print(f'Average price of private rooms: {round(average_price_p)}\nStd: {round(stdv_price_p)}')

average_price_e = sum(listings_entire['price'])/len(listings_entire)
stdv_price_e = np.std(listings_entire['price'])
print(f'Average price of entire home/apt: {round(average_price_e)}\nStd: {round(stdv_price_e)}')

lat_range = (min(listings_nona['latitude']), max(listings_nona['latitude']))
long_range = (min(listings_nona['longitude']), max(listings_nona['longitude']))
print(f'Latitude range: {lat_range}\nLongitude range: {long_range}')

""" TODO: Create partitions of lat&long-areas, look at average price + std for these regions, 
for both private rooms and entire homes. """

def create_zones(n):
    if np.sqrt(n) != round(np.sqrt(n)):
        return "Number of zones must be square"
    
    lat_partition = np.linspace(lat_range[0], lat_range[1], int(np.sqrt(n)))
    long_partition = np.linspace(long_range[0], long_range[1], int(np.sqrt(n)))
    
    return lat_partition, long_partition

# def divide_by_zones(csv, n):
#     listings_list = []

#     lat_partition, long_partition = create_zones(n)

#     for i, lat in enumerate(lat_partition):
#         if i+1 < len(lat_partition):
#             new_csv = csv.loc[csv['latitude'] > lat]
#             new_csv = new_csv.loc[new_csv['latitude'] < lat_partition[i+1]]
#         for j, long in enumerate(long_partition):
#             if j+1 < len(long_partition):
#                 new_csv = new_csv.loc[new_csv['longitude'] > long]
#                 new_csv = new_csv.loc[new_csv['longitude'] < long_partition[j+1]]
#                 listings_list.append(new_csv)

#     return listings_list

def divide_by_zone(csv=str, n=25, lat_nr=int, long_nr=int):
    lats, longs = create_zones(n)

    zone = [lats[lat_nr-1], lats[lat_nr], longs[long_nr-1], longs[long_nr]]

    listings_zone = csv.loc[csv['latitude'] > zone[0]]
    listings_zone = listings_zone.loc[listings_zone['latitude'] < zone[1]]
    listings_zone = listings_zone.loc[listings_zone['longitude'] > zone[2]]
    listings_zone = listings_zone.loc[listings_zone['longitude'] < zone[3]]

    return listings_zone

def stat_dict(listing_type, stat_type):
    price_dict = {}
    if stat_type == 'average':
        for i in range(1, 5):
            for j in range(1, 5):
                av_price = np.average(divide_by_zone(csv=listing_type, lat_nr=i, long_nr=j)['price'])
                if av_price == av_price:
                    price_dict[str((i, j))] = av_price

    if stat_type == 'std':
        for i in range(1, 5):
            for j in range(1, 5):
                std_price = np.std(divide_by_zone(csv=listing_type, lat_nr=i, long_nr=j)['price'])
                if std_price == std_price:
                    price_dict[str((i, j))] = std_price

    if stat_type == 'size':
        for i in range(1, 5):
            for j in range(1, 5):
                size = len(divide_by_zone(csv=listing_type, lat_nr=i, long_nr=j).index)
                price_dict[str((i, j))] = size

    return price_dict

# print(stat_dict(listings_private, 'average'))
# print(stat_dict(listings_private, 'std'))

# print(stat_dict(listings_entire, 'average'))
# print(stat_dict(listings_entire, 'std'))

sizes = stat_dict(listings_entire, 'size')
plt.bar(sizes.keys(), sizes.values())
plt.title('Number of listings for entire home/apt by zone')
plt.show()

sizes = stat_dict(listings_private, 'size')
plt.bar(sizes.keys(), sizes.values())
plt.title('Number of listings for private rooms by zone')
plt.show()

prices = stat_dict(listings_entire, 'average')
stdevs_list = list(stat_dict(listings_entire, 'std').values())

plt.bar(prices.keys(), prices.values())
plt.errorbar(x=prices.keys(), y=prices.values(), yerr=stdevs_list, fmt='o', color='black')
plt.title('Average prices for entire home/apt by zone')
plt.show()

prices = stat_dict(listings_private, 'average')
stdevs_list = list(stat_dict(listings_private, 'std').values())

plt.bar(prices.keys(), prices.values())
plt.errorbar(x=prices.keys(), y=prices.values(), yerr=stdevs_list, fmt='o', color='black')
plt.title('Average prices for private rooms by zone')
plt.show()