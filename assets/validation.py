import pandas as pd
import numpy as np

historic_and_current = pd.read_csv('assets/historic_and_data.csv')
historic_and_current['externalreference'] = historic_and_current['externalreference'].astype(str)
current_data = historic_and_current.loc[historic_and_current['measurementdate'] >= '2021']
historic_data = historic_and_current.loc[historic_and_current['measurementdate'] <= '2021']
class validations:
    
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

    # # Limitsymbol > and factor check
    # def factor_validation(self):
    #     data, historic_and_data, data_historic = DataValidation().data_check()
    #     print('\n***Validatie van limietsymbool bij gebruik van factor voor berekende data***')
    #     colnum = pd.unique(data['externalreference'])
    #     factor = data.groupby('externalreference')
    #     for collectionnumber in colnum:
    #         factorgroups = factor.get_group(collectionnumber)
    #         factorgroups.to_csv('/Users/wouter/Documents/RWS/DataAnalyse/AquadeskData/testdata/limtisymbol.csv')
    #         calculated = sum(factorgroups['calculatedvalue'])
    #         measured = sum(factorgroups['measuredvalue'])
    #         values = calculated / measured
    #         if factorgroups['limitsymbol'].str.contains('>').any():
    #             continue
    #         elif values > 1:
    #             print('Bij collectienummer: ' + collectionnumber + ' is wel een factor gebruikt maar geen limietsymbool gevonden')
    #     print('Geen (andere) missende limietsymbolen bij gebruik van factoren gevonden')

    # # Check for missing taxa & new taxa, needs to be two columns (old, new) and grouped per taxongroup
    # def new_old_taxa(self):
    #     data, historic_and_data, data_historic = DataValidation().data_check()
    #     print('\n***Controle missende taxa***')
    #     print('Deze taxa zijn in voorgaande jaren wel in de meetlocaties gevonden maar niet in de huidige set:')
    #     groups = pd.unique(data_historic['taxongroup'])
    #     for group in groups:
    #         data_group_new = data[data['taxongroup'].astype(str).str.contains(group)]
    #         data_group_historic = data_historic[data_historic['taxongroup'].str.contains(group)]
    #         new = np.sort(pd.unique(data_group_new['parameter']))
    #         old = np.sort(pd.unique(data_group_historic['parameter']))
    #         diff_old = np.setdiff1d(old, new)
    #         diff_old = pd.DataFrame(data = diff_old, columns = ['parameter'])
    #         if diff_old.empty == False:
    #             print('\nTaxongroep: ' + str(group))
    #             for index , row in diff_old.iterrows():
    #                 print('Soort: '+ str(row['parameter']))
    #         else:
    #             pass        
    #     print('\nGeen (andere) missende taxa gevonden')
    #     print('\n***Controle nieuwe taxa***')
    #     for group in groups:
    #         data_group_new = data[data['taxongroup'].astype(str).str.contains(group)]
    #         data_group_historic = data_historic[data_historic['taxongroup'].str.contains(group)]
    #         new = np.sort(pd.unique(data_group_new['parameter']))
    #         old = np.sort(pd.unique(data_group_historic['parameter']))
    #         diff_new = np.setdiff1d(new, old)
    #         diff_new = pd.DataFrame(data = diff_new, columns = ['parameter'])
    #         if diff_new.empty == False:
    #             print('\nTaxongroep: ' + str(group))
    #             for index , row in diff_new.iterrows():
    #                 print('Soort: '+ str(row['parameter']))
    #         else:
    #             pass
    #     print('Geen (andere) nieuwe taxa gevonden')    