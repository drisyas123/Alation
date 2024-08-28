import pandas as pd

data_dict_df = pd.read_csv('DataDictionary.csv')
business_df = pd.read_excel('business.xlsx')
merged_df = pd.merge(data_dict_df, business_df[['Source Key', 'Suggested business term']],
                     left_on='key', right_on='Source Key', how='left')

merged_df['business term'] = merged_df['Suggested business term']
merged_df = merged_df.drop(columns=['Source Key','Suggested business term'])

merged_df.to_csv('updated_dataDictionary.csv', index=False)
print("The file has been updated and saved as 'updated_dataDictionary.csv'.")