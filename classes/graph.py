import pandas as pd

class Graphs:

    macev_taxongroup_colours = {
    'Annelida/Platyhelminthes - Hirudinea':'aqua', \
    'Annelida/Platyhelminthes - Polychaeta':'skyblue', \
    'Annelida/Platyhelminthes - Oligochaeta':'dodgerblue', \
    'Annelida/Platyhelminthes - Turbellaria':'darkblue', \
    'Arachnida':'dimgray', \
    'Bryozoa - Hydrozoa - Porifera':'lightgrey', \
    'Crustacea - Amphipoda':'pink', \
    'Crustacea - Decapoda':'magenta', \
    'Crustacea - Isopoda':'violet', \
    'Crustacea - Mysida':'purple', \
    'Crustacea - Remaining':'blueviolet', \
    'Echinodermata':'ivory', \
    'Insecta (Diptera) - Chironomidae':'orange', \
    'Insecta (Diptera) - Remaining':'limegreen', \
    'Insecta (Diptera) - Simuliidae':'green', \
    'Insecta - Coleoptera':'lawngreen', \
    'Insecta - Ephemeroptera':'seagreen', \
    'Insecta - Heteroptera':'darkolivegreen', \
    'Insecta - Lepidoptera':'mediumspringgreen', \
    'Insecta - Odonata':'greenyellow', \
    'Insecta - Remaining':'palegreen', \
    'Insecta - Trichoptera':'yellowgreen', \
    'Marien - Remaining':'dimgrey', \
    'Mollusca - Bivalvia':'yellow', \
    'Mollusca - Gastropoda':'gold', \
    'Collembola':'black'
    }
    
    # Divide dataset per year and calculate relative distribution per year, return te values from series to a dataframe and reset the first column to index and add column titles remove empty columns with only 0 values
    def value_per_year(relative_data_location_year):
        years = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']
        dataperyear = {}
        for year in years:
            dataperyear[year] = relative_data_location_year[relative_data_location_year['collectiondate']\
                .str\
                .contains(year)]\
                .groupby('name_tg')['calculatedvalue']\
                .sum()\
                .astype(int)\
                .to_frame()\
                .rename_axis('Taxongroup')\
                .rename(columns={'calculatedvalue':year})
        dataperyear = pd.concat(dataperyear, join='outer', axis=1)\
            .fillna(0)\
            .astype(int)
        dataperyear = dataperyear.loc[:, (dataperyear!=0)\
            .any(axis=0)]
        dataperyear.columns = dataperyear.columns.droplevel()
        dataperyear = dataperyear.T
        return dataperyear

    # Divide data per location
    def data_location(historic_and_current, object):
        datalocation = historic_and_current[historic_and_current["measurementobjectname"].str.contains(object)]
        return datalocation

    def relative_data_location_per_year(object, historic_and_current):
        relative_data_location_year = Graphs.data_location(object, historic_and_current) 
        relative_data_location_year = Graphs.value_per_year(relative_data_location_year)
        relative_data_location_year = relative_data_location_year
        return relative_data_location_year
    