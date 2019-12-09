import csv
import sys

from classes.observation import Observation
from classes.dataset import Dataset


def getPrices(input, output):
    prices15 = []
    i = 0
    short_ns = "eg"

    ds_name = "%s:dataset-%s " % (short_ns, "prices")
    ds_prices = Dataset(ds_name)

    with open(input, newline='') as pricesCSV:
        reader = csv.DictReader(pricesCSV)
        for row in reader:
            price = row['Price']
            month = row['Month']
            year = row['Year']
            short_ns = "eg"

            i += 1
            subject = "%s:obs%d " % (short_ns, i)

            if year == "2015" or year == "2016" or year == "2017":
                obs = Observation(subject=subject)
                prices15.append((price, month))
                obs.addDimension(p="dbpedia:month", o=month)
                obs.addDimension(p="dbpedia:year", o=year)
                obs.addMeasure(p="cbo:price", o=price)

                ds_prices.addObservation(obs)
        ds_prices.saveToDisk(output)


if __name__ == "__main__":
    # input = "/home/mmami/FhG/Projects/BETTER/Data/WFP_Prices/WFP_Zimbabwe_Maize_prices.csv"
    # output = "/home/mmami/FhG/Projects/BETTER/Data/rdf-prices.ttl"

    input = sys.argv[1]
    output = sys.argv[2]

    getPrices(input, output)
