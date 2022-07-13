import pandas as pd
import numpy as np

historic_and_current = pd.read_csv('assets/historic_and_data_n.csv', dtype={'externalreference': str})
current_data = historic_and_current.loc[historic_and_current['measurementdate'] >= '2021']
measurementobjectnames = pd.unique(current_data['measurementobjectname'])
historic_data = historic_and_current.loc[historic_and_current['measurementdate'] <= '2021']
historic_location= []
for object in measurementobjectnames:
    historic_per_location = historic_data.loc[historic_data['measurementobjectname'] == object]
    historic_location = historic_per_location.append(historic_location)
class validations:
    
    # Validate the Collection numbers 
    def collection(collection_data):
        return collection_data.loc[collection_data['externalreference'].str.startswith('2021') == False]

    def taxonstatus(taxonstatus_data):
       return taxonstatus_data.loc[taxonstatus_data['statuscode'].isin([10, 80] ) == False] 
    
    # Oligochaeta count validation
    def oligochaeta(oligochaeta_data):
        externalreference = pd.unique(oligochaeta_data['externalreference'])
        data = []
        for reference in externalreference:
            measuredvalue = oligochaeta_data.loc[(oligochaeta_data['externalreference'] == reference) & (oligochaeta_data['name_tg'] == 'Annelida/Platyhelminthes - Oligochaeta'), 'measuredvalue'].sum()
            calculatedvalue = oligochaeta_data.loc[(oligochaeta_data['externalreference'] == reference) & (oligochaeta_data['name_tg'] == 'Annelida/Platyhelminthes - Oligochaeta'), 'calculatedvalue'].sum()
            if (calculatedvalue > 100) & (measuredvalue < 100):
               data = oligochaeta_data.loc[(oligochaeta_data['name_tg'] == 'Annelida/Platyhelminthes - Oligochaeta') & (oligochaeta_data['externalreference'] == reference)].append(data)
            else:
                pass
        return data

    # Chironomidae count validation 
    def chironomidae(chironomidae_data):
        externalreference = pd.unique(chironomidae_data['externalreference'])
        chiro_data = []
        for reference in externalreference:
            measuredvalue = chironomidae_data.loc[(chironomidae_data['externalreference'] == reference) & (chironomidae_data['name_tg'] == 'Insecta (Diptera) - Chironomidae'), 'measuredvalue'].sum()
            calculatedvalue = chironomidae_data.loc[(chironomidae_data['externalreference'] == reference) & (chironomidae_data['name_tg'] == 'Insecta (Diptera) - Chironomidae'), 'calculatedvalue'].sum()
            if (calculatedvalue > 100) & (measuredvalue < 100):
                chiro_data = chironomidae_data.loc[(chironomidae_data['name_tg'] == 'Insecta (Diptera) - Chironomidae') & (chironomidae_data['externalreference'] == reference)].append(chiro_data)
            else:
                pass
        return chiro_data

    # Other taxongroups count validation
    def taxongroup(taxongroup_data):
        externalreference = pd.unique(taxongroup_data['externalreference'])
        taxongroup = pd.unique(taxongroup_data['name_tg'])
        group_data = []
        for reference in externalreference:
            for group in taxongroup:
                measuredvalue = taxongroup_data.loc[(taxongroup_data['externalreference'] == reference) & (taxongroup_data['name_tg'] == group), 'measuredvalue'].sum()
                calculatedvalue = taxongroup_data.loc[(taxongroup_data['externalreference'] == reference) & (taxongroup_data['name_tg'] == group), 'calculatedvalue'].sum()
                if (calculatedvalue > 100) & (measuredvalue < 100):
                    group_data = taxongroup_data.loc[(taxongroup_data['name_tg'] == group) & (taxongroup_data['externalreference'] == reference)].append(group_data)
                else:
                    pass
        return group_data

    def factor(factor_data):
        externalreference = pd.unique(factor_data['externalreference'])
        factor = factor_data.groupby('externalreference')
        limit_data=[]
        for reference in externalreference:
            factorgroups = factor.get_group(reference)
            calculated = sum(factorgroups['calculatedvalue'])
            measured = sum(factorgroups['measuredvalue'])
            values = calculated / measured
            if factorgroups['limitsymbol'].str.contains('>').any():
                continue
            elif values > 1:
                limit_data = factor_data.loc[(factor_data['externalreference'] == reference)].append(limit_data)
        return limit_data

    def missing(missing_current_data, missing_historic_data):
        diff_old = pd.DataFrame(data = np.setdiff1d(np.sort(pd.unique(missing_historic_data['parameter'])), np.sort(pd.unique(missing_current_data['parameter']))), columns = ['parameter'])
        parameters = pd.unique(diff_old['parameter']) 
        old_data = []
        for parameter in parameters:
            print(parameter)
            old_data = missing_current_data.loc[(missing_current_data['parameter'] == parameter)].append(old_data)

        return old_data
            

    def new(new_current_data, new_historic_data):
        diff_new = pd.DataFrame(data = np.setdiff1d(np.sort(pd.unique(new_current_data['parameter'])), np.sort(pd.unique(new_historic_data['parameter']))), columns = ['parameter'])
        parameters = pd.unique(diff_new['parameter'])
        new_data =[]
        for parameter in parameters:
            new_data = new_current_data.loc[(current_data['parameter'] == parameter)].append(new_data)
        return new_data