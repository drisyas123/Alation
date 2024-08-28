# Import dependencies
import pandas as pd
import requests
import logging
import warnings
warnings.filterwarnings("ignore")

def run_script(file_path, domain_name, api_access_token):
   try:
         # Set all URLs and headers
         baseUrl= "https://67d9d41a-fe10-428b-ac97-e866b16ef372.alationcloud.com/" 
         refreshTokenURL = baseUrl + "v1/createRefreshToken/"
         APIAccessTokenURL = baseUrl + "integration/v1/createAPIAccessToken/"
         APIAccessTokenURL2 = baseUrl + "account/auth/"
         termsUrl = baseUrl + "integration/v2/term/"
         domainUrl = baseUrl + "integration/v2/domain/"
         templateUrl = baseUrl + "integration/v1/custom_template/"
         objectsURL = baseUrl + "integration/v1/otype/"
         customFieldsURL = baseUrl + "integration/v2/custom_field/"
         domainMembershipURL = baseUrl + "integration/v2/domain/membership/"
         userURL = baseUrl + "integration/v2/user/"
         searchURL = baseUrl + "integration/v1/search/"

         headers = {
            "accept": "application/json",
            "content-type": "application/json"
         }

         # Refresh access token
         # refreshTokenPayload = {
         #   "username": "adhi.adhikari@hpspartners.com",
         #   "password": "DuV-DPx4sDMiyG.",
         #   "name": "HPSAlationRefreshToken"
         # }

         # refreshTokenResponse = requests.post(refreshTokenURL, json=refreshTokenPayload, headers=headers, verify=False)
         # refreshTokenResponseDict = refreshTokenResponse.json()

         #print(refreshTokenResponse.text)
         ## Tokens are valid (active) for 60 days

         # refresh_token_secret = input("Please enter the refresh token: ")
         # refresh_token_secret = "mDmouAZ7GgowVKjTbGOBLrJgmNYZRp8ke_K4DKsEF5XkGgaau68d4GRw1Ci4jvUhwpLYQeQm10-SaAGd6V3yxw"

         # Get API Access Token
         # APIAccessTokenPayload = {
         #   "user_id": 4,
         #   "refresh_token": refreshTokenResponseDict["refresh_token"]
         # }

         # APIAccessTokenPayload = {
         #   "user_id": 4,
         #   "refresh_token": refresh_token_secret
         # }

         # APIAccessTokenPayloadResponse = requests.post(APIAccessTokenURL, json=APIAccessTokenPayload, headers=headers, verify=False)
         # APIAccessTokenPayloadResponseDict = APIAccessTokenPayloadResponse.json()

         #print(APIAccessTokenPayloadResponse.text)

         # INPUT
         # api_access_token = input("Please enter the API  token: ")
         # API access tokens are valid for 24 hours. Have to generate another after 24 hours

         #establish a header with the token
         # tokenHeader = {
         #     "accept": "application/json",
         #     "content-type": "application/json",
         #     "token": APIAccessTokenPayloadResponseDict["api_access_token"]
         # }

         tokenHeader = {
            "accept": "application/json",
            "content-type": "application/json",
            "token": api_access_token
         }

         # # get an input from the user
         # data_catalog_file_name = input("Enter the Data Catalog File Name with the file extension: ")

         # #check if file extension is .xlsx
         # if data_catalog_file_name.endswith('.xlsx') == False:
         #     print("Please enter a valid file name with the file extension")
         #     data_catalog_file_name = input("Enter the Data Catalog File Name with the file extension: ")

         # #convert the domain name to string
         # data_catalog_file_name = str(data_catalog_file_name)
         # #trim trailing spaces and characters
         # data_catalog_file_name = data_catalog_file_name.strip()

         # # get an input from the user
         # data_catalog_file_path = input("Enter the Data Catalog File Path: ")
         # #convert the domain name to string
         # data_catalog_file_path = str(data_catalog_file_path)
         # #trim trailing spaces and characters
         # data_catalog_file_path = data_catalog_file_path.strip()

         # # combine the file name and path with a \ separator
         # data_catalog_file = data_catalog_file_path + "\\" + data_catalog_file_name


         # #transform data_catalog_file string as a literal string
         # data_catalog_file = r"{}".format(data_catalog_file)

         # Read the Excel file into a pandas DataFrame
         try:
            df_catalog = pd.read_excel(file_path)
            # print("Excel file successfully read into a DataFrame!")
            #  print(df.head())  # Display the first few rows of the DataFrame
         except FileNotFoundError:
            print("The file was not found. Please check the path and try again.")
         except Exception as e:
            print("An error occurred while reading the Excel file:", e)

         # Columns list
         columns_list = df_catalog.columns.to_list()
         column_index_list = list(range(len(columns_list)))
         columns_df = pd.DataFrame(
            {'index': column_index_list,
            'column_name': columns_list
            })
         
         # # get an input from the user
         # domain_name = input("Enter the Domain that you would like uploaded: ")
         # #convert the domain name to camel case
         # domain_name = str(domain_name).title()
         # #trim trailing spaces and characters
         # domain_name = domain_name.strip()

         # # get a unique list of all the values in the domain column
         # domain_values__list = df_catalog[domain_name].unique()

         # # check if domain_name exists in the domain_values_list, if it does, continue, if not, print a message and ask for a new domain name
         # if domain_name not in domain_values__list:
         #     print("Domain name does not exist in the Data Catalog, please enter a valid domain name.")
         #     domain_name = input("Enter the Domain that you would like uploaded: ")
         #     #convert the domain name to camel case
         #     domain_name = str(domain_name).title()
         #     #trim trailing spaces and characters
         #     domain_name = domain_name.strip()

         # fill na's and convert to string
         df_catalog_1 = df_catalog.copy()
         df_catalog_1 = df_catalog_1.fillna('')

         df_catalog_1['Domain ID'] = df_catalog_1['Domain ID'].astype(str)
         df_catalog_1['Sub-Domain ID'] = df_catalog_1['Sub-Domain ID'].astype(str)

         # convert all required columns to string
         df_catalog_1['[Internal Purposes only] Assignment'] = df_catalog_1['[Internal Purposes only] Assignment'].astype(str)
         df_catalog_1['Preliminary Assignment of Critical Data Element [CDE]'] = df_catalog_1['Preliminary Assignment of Critical Data Element [CDE]'].astype(str)
         df_catalog_1 = df_catalog_1.astype(str)

         # strip all the whitespaces and special characters from the columns
         df_catalog_1 = df_catalog_1.map(lambda x: x.strip() if isinstance(x, str) else x)

         # Check if the domain name is in the dictionary
         if domain_name in df_catalog['[Internal Purposes only] Assignment'].values:
            # print(domain_name)
            # Filter the DataFrame based on the condition
            df_catalog_1 = df_catalog[df_catalog['[Internal Purposes only] Assignment'] == domain_name]
         else:
            # print(domain_name)
            print("Domain name not found in the file.")


         # filter for CDEs
         df_catalog_1 = df_catalog_1[df_catalog_1['Preliminary Assignment of Critical Data Element [CDE]'] == 'CDE']
         
         # delete all empty rows form df_catalog_1
         df_catalog_1 = df_catalog_1.dropna(how='all')

         # create a new copy for testing
         df_catalog_test = df_catalog_1.copy()

         ####### Code to delete all domains first ########

         # Get all domains from Alation
         getDomains = requests.get(domainUrl, headers=tokenHeader, verify=False)
         getDomainResponseDict = getDomains.json()

         # filter in the getDomainResponseDict for the domain with parent_id = None
         parentDomain = [domain for domain in getDomainResponseDict if domain['parent_id'] == None]
         
         # remove all keys except for 'id' from getDomainResponseDict
         getDomainResponseDict = [{k: v for k, v in d.items() if k == 'id'} for d in parentDomain]

         # create a list of all the ids from getDomainResponseDict
         domainIdList = [domain['id'] for domain in getDomainResponseDict]

         # create a list with one dictionary with the key 'id' and value domainIdList
         domainIdDict = {'id': domainIdList}

         ####### Code to upload domains and create hierarchy #######
         # create another dataframe with just Domain\n [Level 1] and Definition\n [Level 1]
         df_domain = df_catalog_1[['Data Domain\n [Level 1]', 'Definition\n [Level 1]']]

         #rename columns
         df_domain.columns = ['title', 'description']

         # keep unique value of title and description
         df_domain = df_domain.drop_duplicates()

         # take only the first row from df_domain
         df_domain = df_domain.head(1)

         #create a data dictionary from the dataframe
         df_domain_dict = df_domain.to_dict(orient='records')

         # example payload
         # domain_example_dict = [{'title': 'Hello',
         #   'description': 'World'},]

         #upload domain
         attribute_name = domain_name
         
         search_url = '/integration/v1/search/'
         all_params = 'q="%s"&limit=20&offset=0&filters={"otypes":["domain"]}' % attribute_name
         response = requests.get(searchURL, params=all_params, headers=tokenHeader, verify=False)
         search_result = response.json()
         
         #if not response.ok:
         if (search_result['total']) == 1:
            print('Domain already exists: '+domain_name)
         else:
            domainUploadResponse = requests.post(domainUrl, json=df_domain_dict, headers=tokenHeader, verify=False)
            domainUploadResponseDict = domainUploadResponse.json()
            # print(domainUploadResponse.text) 

            ########## Upload Subdomains ###########
            # upload sub-domains
            # create another dataframe with just Sub-Domain\n [Level 1] and Definition\n [Level 1]
            df_subdomain = df_catalog_1[['Sub-Domain \n[Level 2]', 'Definition\n [Level 2]']]

            #rename columns
            df_subdomain.columns = ['title', 'description']

            # create another column called parent_id and set it to the id field of the domainUploadResponse
            df_subdomain['parent_id'] = domainUploadResponseDict[0]['id']

            # keep unique value of title and description
            df_subdomain = df_subdomain.drop_duplicates()

            #create a data dictionary from the dataframe
            df_subdomain_dict = df_subdomain.to_dict(orient='records')

            # subdomain_example_dict = [{'title': 'Fund Financials',
            #   'description': 'test',
            #   'parent_id': 20}]

            #upload sub domain
            subDomainUploadResponse = requests.post(domainUrl, json=df_subdomain_dict, headers=tokenHeader, verify=False)
            domainUploadResponseDict = subDomainUploadResponse.json()
               
            # convert domainUploadResponse to dataframe
            subDomainUploadResponseDict = subDomainUploadResponse.json()
            df_subdomainUploadResponse = pd.DataFrame(subDomainUploadResponseDict)

            # Upload data class
            # create another dataframe with just Data Class\n  [Level 3] and Definition\n [Level 3]
            df_dataclass = df_catalog_1[['Sub-Domain \n[Level 2]', 'Data Class\n  [Level 3]', 'Definition\n [Level 3]']]

            #rename columns
            df_dataclass.columns = ['sub-domain', 'title', 'description']

            # keep unique value of title and description
            df_dataclass = df_dataclass.drop_duplicates()

            # create a new id column and set it to the id field of the df_subdomainUploadResponse based on the sub-domain column matching with the title column
            df_dataclass['parent_id'] = df_dataclass['sub-domain'].map(df_subdomainUploadResponse.set_index('title')['id'])

            # wherever the parent_id is null, set it to 0
            df_dataclass['parent_id'] = df_dataclass['parent_id'].fillna(0).astype(int)

            # drop sub-domain column
            df_dataclass = df_dataclass.drop(columns=['sub-domain'])

            #create a data dictionary from the dataframe
            df_dataclass_dict = df_dataclass.to_dict(orient='records')

            # dataclass_example_dict = [{'title': 'Example data class',
            #   'description': 'test',
            #   'parent_id': 23}]
            
            dataClassUploadResponse = requests.post(domainUrl, json=df_dataclass_dict, headers=tokenHeader, verify=False)
            dataClassUploadResponseDict = dataClassUploadResponse.json()
                  
            # convert domainUploadResponse to dataframe
            df_dataClassUploadResponse = pd.DataFrame(dataClassUploadResponseDict)
            
            # how to add custom fields to the domain, sub-domain and data class?

            ####### Code to upload business terms and atatch to the specific domains ######

            # parentId = 85
            # domainUrlwithParams = f"{domainUrl}?parent_id={parentId}"

            # Get all L3s where L2 is 5 and where L2 is 4
            domains = requests.get(domainUrl, headers=tokenHeader, verify=False)
            domainsDict = domains.json()
            df_domains = pd.DataFrame(domainsDict)

            # select custom columns
            df_catalog_2 = df_catalog_1.copy()
            df_catalog_2 = df_catalog_2[['Preliminary Assignment of Data Steward (DS)', 'Preliminary Assignment of Critical Data Element [CDE]', 'Preliminary Assignment Data Confidentiality', 'Preliminary Assignment \nData Sensitivity', 'Preliminary Assignment of System of Origin (SOO)', 'Preliminary Assignment of System of Record (SOR)', 'Consuming Systems/ Applications', 'Notes/Clarifications']] 

            #Add alation id for each domain
            # df_catalog_1['AlationDomainID'] = df_catalog_1.apply(lambda row:
            #    df_domains[df_domains['title'] == row['Data Domain\n [Level 1]']]['id'],
            #    axis=1)
            df_catalog_1['AlationDomainID'] = df_catalog_1.apply(lambda row: 
               df_domains[df_domains['title'] == row['Data Domain\n [Level 1]']]['id'].iloc[0] if not df_domains[df_domains['title'] == row['Data Domain\n [Level 1]']].empty else None, 
               axis=1)


            #Add alation id for each subdomain
            df_catalog_1['AlationSubDomainID'] = df_catalog_1.apply(lambda row:
               df_domains[df_domains['title'] == row['Sub-Domain \n[Level 2]']]['id'].iloc[0],
               axis=1)

            #Add alation id for each data class
            df_catalog_1['AlationDataClassID'] = df_catalog_1.apply(lambda row:
               df_domains[df_domains['title'] == row['Data Class\n  [Level 3]']]['id'].iloc[0],
               axis=1)

            # Ad-hoc - DO NOT RUN
            #make NA values of AlaionDomainID as 24.0
            # df_catalog_1['AlationDomainID'] = df_catalog_1['AlationDomainID'].fillna(24.0)

            #make alationDomainID, alationSubDomainID and alationDataClassID as integers
            df_catalog_1['AlationDomainID'] = df_catalog_1['AlationDomainID'].astype(int)
            df_catalog_1['AlationSubDomainID'] = df_catalog_1['AlationSubDomainID'].astype(int)
            df_catalog_1['AlationDataClassID'] = df_catalog_1['AlationDataClassID'].astype(int)


            if data_steward=="Y":
               ######### DO NOT RUN IF DATA STEWARDS ARE NOT BEING UPLOADED ####

               # TODO : Check condition for input Data Stewards uploaded or not

               # get all users from alation
               users = requests.get(userURL, headers=tokenHeader, verify=False)
               usersDict = users.json()

               if bool(usersDict) == False:
                     print("No users in Alation")
               else:
                     df_users = pd.DataFrame(usersDict)

               # convert domainUploadResponse to dataframe
               usersDictDf = pd.DataFrame(usersDict)

               # get all unique values of Preliminary Assignment of Data Steward (DS)
               names = df_catalog_2['Preliminary Assignment of Data Steward (DS)'].unique()

               # get all unique vallues of display_name
               names_1 = usersDictDf['display_name'].unique()

               # check if all values in names are in names_1
               all(elem in names_1 for elem in names)

               # what values are in names that are not in names_1
               not_in_names_1 = [elem for elem in names if elem not in names_1]


               #Ad-Hoc
               #change all the values of Preliminary Assignment of Data Steward (DS) in df_catalog_1 to 'Dimitrios Godosis' where the value of Preliminary Assignment of Data Steward (DS) is 'Dimitri Godosis'
               # df_catalog_1['Preliminary Assignment of Data Steward (DS)'] = df_catalog_1['Preliminary Assignment of Data Steward (DS)'].replace('Dimitri Godosis', 'Dimitrios Godosis')
               # df_catalog_2['Preliminary Assignment of Data Steward (DS)'] = df_catalog_2['Preliminary Assignment of Data Steward (DS)'].replace('Dimitri Godosis', 'Dimitrios Godosis')

               # get all unique values of Preliminary Assignment of Data Steward (DS)
               names = df_catalog_2['Preliminary Assignment of Data Steward (DS)'].unique()
               names_1 = usersDictDf['display_name'].unique()

               # check if all values in names are in names_1
               all(elem in names_1 for elem in names)

               # what values are in names that are not in names_1
               not_in_names_1 = [elem for elem in names if elem not in names_1]

               #Add user id for each business term
               if len(df_users) > 0:
                  df_catalog_2['oid'] = df_catalog_2.apply(lambda row:
                     df_users[df_users['display_name'] == row['Preliminary Assignment of Data Steward (DS)']]['id'].iloc[0],
                     axis=1)
                  
               #Add otype as "user" string
               if len(df_users) > 0:
                  df_catalog_2['otype'] = df_catalog_2.apply(lambda row:
                     'user',
                     axis=1)
                  
               #add a new column called Data Steward which combines oid and otype as a dictionary
               if len(df_users) > 0:
                  df_catalog_2['Data Steward'] = df_catalog_2.apply(lambda row:
                     {'otype': row['otype'], 'oid': row['oid']},
                     axis=1)
                  
               # put brackets around the Data Steward column
               if len(df_users) > 0:
                  df_catalog_2['Data Steward'] = df_catalog_2['Data Steward'].apply(lambda x: [x])\
            
            #####  END OF 'DO NOT RUN IF DATA STEWARDS ARE NOT BEING UPLOADED' ####


            #### Glossary ####

            # Add Code to check if glossary is already created, if not create one for the domain - Nomenclaure as  '<Domain Name> Business Glossary'
            # glossary_id = 14
            # Replace this with the name of an existing glossary
            glossary_name = domain_name

            # Set the search query string to the name of the glossary and set the otype
            all_params = 'q="%s"&limit=20&offset=0&filters={"otypes":["glossary_v3"]}' % glossary_name

            # Issue the get request
            response = requests.get(searchURL, params=all_params, headers=tokenHeader, verify=False)
            glossary_result = response.json()

            # Check in the json converted response to see if the glossary was found
            if (glossary_result['total']) == 1:
            
               # get the id of the glossary
               glossary_id = glossary_result['results'][0]['id']
               
               print("Glossary named %s does exist in the catalog. Its ID is: %s" % (glossary_name, glossary_id))
            else:
               print("Glossary named %s does not exist in the catalog." % glossary_name)


            # INPUT
            # Add the glossary ids for each Business Term
            businessGlossaryID = glossary_id
            # technicalGlossaryID = 2

            df_catalog_1['AlationBusinessGlossaryID'] = df_catalog_1.apply(lambda row:
               businessGlossaryID,
               axis=1)

            #Write code to get template ID from Alation via API
            templates = requests.get(templateUrl, headers=tokenHeader, verify=False)
            templatesDict = templates.json()
            df_templates = pd.DataFrame(templatesDict)

            # Add the glossary ids for each Business Term
            customBusinessTermTemplateID = df_templates[df_templates['title'] == 'Business Term']['id']

            df_catalog_1['AlationBusinessTermTemplateID'] = df_catalog_1.apply(lambda row:
               customBusinessTermTemplateID,
               axis=1)
            # columns_list = df_catalog_1.columns.to_list()
            # column_index_list = list(range(len(columns_list)))
            # columns_df = pd.DataFrame(
            #     {'index': column_index_list,
            #      'column_name': columns_list
            #     })

            df_catalog_3 = df_catalog_1.copy()

            # select needed columns
            df_catalog_1 = df_catalog_1[['Business Term\n[Level 4]', 'Definition\n [Level 4]', 'AlationDataClassID', 'AlationBusinessGlossaryID', 'AlationBusinessTermTemplateID']] 

            #rename columns
            df_catalog_1 = df_catalog_1.rename(columns={'Business Term\n[Level 4]': 'Title', 'Definition\n [Level 4]': 'Description'})

            #Write code to get objects from Alation via API
            # objects = requests.get(objectsURL, headers=tokenHeader, verify=False)
            # objectsDict = objects.json()
            # df_objects = pd.DataFrame(objectsDict)

            #Write code to get customFields from Alation via API
            customFields = requests.get(customFieldsURL, headers=tokenHeader, verify=False)
            customFieldsDict = customFields.json()
            df_customFields = pd.DataFrame(customFieldsDict)

            df_catalog_2["RowID"] = df_catalog_2.index

            df_catalog_2 = df_catalog_2.drop(columns=['Preliminary Assignment of Data Steward (DS)'])

            ### Run only if Stewards are being populated ###
            if data_steward == "Y":
            # drop oid and otype columns
               df_catalog_2 = df_catalog_2.drop(columns=['oid', 'otype'])

            #### End of 'Run only if Stewards are populated' ###

            #rename all columns by removing the prefix 'Preliminary Assignment of '
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Preliminary Assignment of ', '')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Preliminary Assignment \n', '')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Preliminary Assignment ', '')

            #rename Critical Data Element [CDE] to Critical Data Element (CDE)
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Critical Data Element [CDE]', 'Critical Data Element (CDE)')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Data Sensitivity', 'Sensitivity')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Data Confidentiality', 'Confidentiality')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('System of Origin (SOO)', 'System of Origin')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('System of Record (SOR)', 'System of Record')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Consuming Systems/ Applications', 'Consuming Systems/Applications')
            # Notes/Clarifications

            customFields = df_customFields['name_singular'].unique()

            # get list of columns names of df_catalog_2
            columns_list = df_catalog_2.columns.to_list()

            # check if all column_list values are in customFields
            check = all(elem in customFields for elem in columns_list)

            #what values are in columns_list that are not in customFields
            not_in_customFields = [elem for elem in columns_list if elem not in customFields]

            # make a long table from df_catalog_2 wide table
            df_catalog_2_long = pd.melt(df_catalog_2, id_vars=['RowID'], var_name='Field', value_name='value')
            # print(df_catalog_2_long.apply(lambda row:
            #    df_customFields[df_customFields['name_singular'] == row['Field']]['id'].iloc[0],
            #    axis=1))

            # create a new column field_id and set it to the ids of the custom fields
            df_catalog_2_long['field_id'] = df_catalog_2_long.apply(lambda row:
               df_customFields[df_customFields['name_singular'] == row['Field']]['id'].iloc[0],
               axis=1)
            
            # convert df_catalog_2 to dictionary
            df_catalog_2_long_dict = df_catalog_2_long.to_dict(orient='records')

            # In df_catalog_2_long_dict, replace \n\n with , in the value column
            for dict in df_catalog_2_long_dict:
               if isinstance(dict['value'], str):
                  dict['value'] = dict['value'].replace('\n\n', ', ')

            df_catalog_1.columns = df_catalog_1.columns.str.replace('Title', 'title')
            df_catalog_1.columns = df_catalog_1.columns.str.replace('Description', 'description')
            df_catalog_1.columns = df_catalog_1.columns.str.replace('AlationBusinessGlossaryID', 'glossary_ids')
            df_catalog_1.columns = df_catalog_1.columns.str.replace('AlationBusinessTermTemplateID', 'template_id')

            df_catalog_1["RowID"] = df_catalog_2.index

            # convert df_catalog_1 to dictionary
            df_catalog_1_long_dict = df_catalog_1.to_dict(orient='records')

            #remove the AlationDataClassID key from the dictionary
            df_catalog_1_long_dict = [{k: v for k, v in x.items() if k not in ['AlationDataClassID']} for x in df_catalog_1_long_dict]

            # change the data type of the glossary_ids to a list
            df_catalog_1_long_dict = [{k: [v] if k == 'glossary_ids' else v for k, v in x.items()} for x in df_catalog_1_long_dict]

            # add custom fields to the dictionary
            for dict in df_catalog_1_long_dict:
               for customDict in df_catalog_2_long_dict:
                  # print(dict['RowID'])
                  # print(customDict['RowID'])
                  if dict['RowID'] == customDict['RowID']:
                        df_catalog_2_long_dict_i = [x for x in df_catalog_2_long_dict if x['RowID'] == dict['RowID']]
                        df_catalog_2_long_dict_i_clean = [{k: v for k, v in x.items() if k not in ['RowID', 'Field']} for x in df_catalog_2_long_dict_i]
                        # print(df_catalog_2_long_dict_i)
                        dict.update(custom_fields=df_catalog_2_long_dict_i_clean)


            #remove the RowID key from the dictionary
            df_catalog_1_long_dict = [{k: v for k, v in x.items() if k not in ['RowID', 'Field']} for x in df_catalog_1_long_dict]

            # Make it so that it matches length of the dictionary

            # please change depending on how many terms to fetch
            fetchLimit = 200

            #INPUT
            termsUrlwithParams = f"{termsUrl}?glossary_id={glossary_id}&limit={fetchLimit}"
            # Get all terms
            terms = requests.get(termsUrlwithParams, headers=tokenHeader, verify=False)
            termsDict = terms.json()
            df_terms = pd.DataFrame(termsDict)

            # Create a list of all the ids from df_terms
            if df_terms.empty:
               term_ids = []
            else:
               term_ids = df_terms['id'].tolist()
               term_ids

            # example payload
            # term_ids = [12, 13]

            # create a dictionary where key is id and value is the term_ids list
            term_ids_dict = {}
            for id in term_ids:
               term_ids_dict['id'] = term_ids

            # Give user option if they want incremental update or full update
            # based on input, decide to delete terms or not

            # Delete all terms from Alation using the term_ids list
            if bool(term_ids_dict):
               deleteTerms = requests.delete(termsUrl, json=term_ids_dict, headers=tokenHeader, verify=False)
               # print(deleteTerms.text)


            #Post the terms
            termsResponse = requests.post(termsUrl, json=df_catalog_1_long_dict, headers=tokenHeader, verify=False)
            # print(termsResponse.text)



            # example payload for adding new businessterms
            # payload = [
            #   {'title': 'Net Asset Value Per Share',
            #   'description': 'This is a measure of a fund’s price per share and is calculated by subtracting the funds’ liabilities from its total assets and dividing by the total number of issued shares.',
            #   'glossary_ids': [1],
            #   'template_id': 43,
            #   'custom_fields': [{'value': 'No', 'field_id': 10007},
            #    {'value': '', 'field_id': 10009},
            #    {'value': '', 'field_id': 10010},
            #    {'value': '', 'field_id': 10011},
            #    {'value': '', 'field_id': 10012},
            #    {'value': '', 'field_id': 10013}]},
            #    {'title': 'Gross Asset Value Report Date',
            #   'description': 'The last date that the gross asset value was reported.',
            #   'glossary_ids': [1],
            #   'template_id': 43,
            #   'custom_fields': [{'value': 'CDE', 'field_id': 10007},
            #    {'value': '', 'field_id': 10009},
            #    {'value': '', 'field_id': 10010},
            #    {'value': '', 'field_id': 10011},
            #    {'value': '', 'field_id': 10012},
            #    {'value': '', 'field_id': 10013}]}
            # ]

            # payload = [{'title': 'VPM Account ID',
            #   'description': 'This field uniquely identifies a Account',
            #   'glossary_ids': [1],
            #   'template_id': 43,
            #   'custom_fields': [{'value': 'Wen Zhou', 'field_id': 8},
            #    {'value': 'CDE', 'field_id': 10007},
            #    {'value': 'C', 'field_id': 10009},
            #    {'value': 'P', 'field_id': 10010},
            #    {'value': 'VPM', 'field_id': 10011},
            #    {'value': 'VPM', 'field_id': 10012},
            #    {'value': 'HPS Data Warehouse, HPS Snowflake', 'field_id': 10013},
            #    {'value': '', 'field_id': 10014}]},
            #  {'title': 'VPM Account Name',
            #   'description': 'Name of  the account',
            #   'glossary_ids': [1],
            #   'template_id': 43,
            #   'custom_fields': [{'value': 'Wen Zhou', 'field_id': 8},
            #    {'value': 'CDE', 'field_id': 10007},
            #    {'value': 'C', 'field_id': 10009},
            #    {'value': 'P', 'field_id': 10010},
            #    {'value': 'VPM', 'field_id': 10011},
            #    {'value': 'VPM', 'field_id': 10012},
            #    {'value': 'HPS Data Warehouse, HPS Snowflake', 'field_id': 10013},
            #    {'value': '', 'field_id': 10014}]}
            # ]

            #convert payload to json
            # payload_json = json.dumps(payload)

            #Post the example terms
            # termsResponse = requests.post(termsUrl, json=payload, headers=tokenHeader, verify=False)
            # print(termsResponse.text)

            ##### Add Terms to the correct domains ####

            # Get all terms
            terms = requests.get(termsUrlwithParams, headers=tokenHeader, verify=False)
            termsDict = terms.json()
            df_terms = pd.DataFrame(termsDict)
            

            # Create a list of all the ids from df_terms
            # if df_terms.empty:
            #     term_ids = []
            # else:
            #     term_ids = df_terms['id'].tolist()
            #     term_ids


            # inner join df_catalog_3 and df_terms on  Business Term\n[Level 4] from df_catalog_3 and title from df_terms
            df_catalog_3['Business Term\n[Level 4]'] = df_catalog_3['Business Term\n[Level 4]'].str.strip()
            df_terms['title'] = df_terms['title'].str.strip()

            # rename the Business Term\n[Level 4] to business_term in df_catalog_3
            df_catalog_3 = df_catalog_3.rename(columns={'Business Term\n[Level 4]': 'business_term'})
            df_catalog_3_terms = pd.merge(df_catalog_3, df_terms, left_on='business_term', right_on='title', how='inner')

            # select the columns from the merged dataframe df_catalog_3_terms
            df_catalog_3_terms = df_catalog_3_terms[['id', 'AlationDataClassID']]

            #rename the id to oid
            df_catalog_3_terms = df_catalog_3_terms.rename(columns={'id': 'oid'})

            #rename the AlationDataClassID to id
            df_catalog_3_terms = df_catalog_3_terms.rename(columns={'AlationDataClassID': 'id'})

            # group df_catalog_3_terms by id and create a new column with oid as a list
            df_catalog_3_terms_grouped = df_catalog_3_terms.groupby('id')['oid'].apply(list).reset_index()

            #convert the dataframe to dictionary
            df_catalog_3_terms_dict = df_catalog_3_terms_grouped.to_dict(orient='records')

            # Add key value pair for exclude, recursive and otype
            df_catalog_3_terms_dict = [{**x, 'exclude': False, 'otype': 'glossary_term'} for x in df_catalog_3_terms_dict]

            # make oid a list
            # df_catalog_3_terms_dict = [{k: [v] if k == 'oid' else v for k, v in x.items()} for x in df_catalog_3_terms_dict]

            # #Add Domain to Business Terms one at a time
            for dict in df_catalog_3_terms_dict:
               domainMembershipResponse = requests.post(domainMembershipURL, json=dict, headers=tokenHeader, verify=False)
               # print(domainMembershipResponse.text)

            # example payload for adding domain to business terms
            # Net Asset Value Report Date
            # payload1 = [{'oid': [13],
            #   'id': 12,
            #   'exclude': False,
            #   'recursive': False,
            #   'otype': 'glossary_term'},
            #   {'oid': [12],
            #   'id': 12,
            #   'exclude': False,
            #   'recursive': False,
            #   'otype': 'glossary_term'}
            #   ]
            # Gross Asset Value Report Date
            # {'oid': [13],
            #   'id': 12,
            #   'exclude': False,
            #   'recursive': False,
            #   'otype': 'glossary_term'},
            # # Net Asset Value Per Share
            # {'oid': [12],
            #   'id': 12,
            #   'exclude': False,
            #   'recursive': False,
            #   'otype': 'glossary_term'}

            # #Add Domain to Business Terms one at a time
            # for payload1_dict in payload1:
            #     domainMembershipResponse = requests.post(domainMembershipURL, json=payload1_dict, headers=tokenHeader, verify=False)
            #     print(domainMembershipResponse.text)

            # #Add Domain to Business Terms
            # domainMembershipResponse = requests.post(domainMembershipURL, json=df_catalog_3_terms_dict, headers=tokenHeader, verify=False)
            # print(domainMembershipResponse.text)


            ###### Testing  ############

            # Get all terms
            terms = requests.get(termsUrlwithParams, headers=tokenHeader, verify=False)
            termsDict = terms.json()
            df_terms = pd.DataFrame(termsDict)

            # remove the <p> and </p> tags from the description column
            df_terms['description'] = df_terms['description'].str.replace('<p>', '')
            df_terms['description'] = df_terms['description'].str.replace('</p>', '')

            #rename all columns by removing the prefix 'Preliminary Assignment of '
            df_catalog_test.columns = df_catalog_test.columns.str.replace('Preliminary Assignment of ', '')
            df_catalog_test.columns = df_catalog_test.columns.str.replace('Preliminary Assignment \n', '')
            df_catalog_test.columns = df_catalog_test.columns.str.replace('Preliminary Assignment ', '')

            #rename Critical Data Element [CDE] to Critical Data Element (CDE)
            df_catalog_test.columns = df_catalog_test.columns.str.replace('Critical Data Element [CDE]', 'Critical Data Element (CDE)')
            df_catalog_test.columns = df_catalog_test.columns.str.replace('Data Sensitivity', 'Sensitivity')
            df_catalog_test.columns = df_catalog_test.columns.str.replace('Data Confidentiality', 'Confidentiality')
            df_catalog_test.columns = df_catalog_test.columns.str.replace('System of Origin (SOO)', 'System of Origin')
            df_catalog_test.columns = df_catalog_test.columns.str.replace('System of Record (SOR)', 'System of Record')
            df_catalog_2.columns = df_catalog_2.columns.str.replace('Data Steward (DS)', 'Data Steward')
            df_catalog_test.columns = df_catalog_test.columns.str.replace('Consuming Systems/ Applications', 'Consuming Systems/Applications')
            # Notes/Clarifications

            # remove first 10 columns
            df_catalog_test = df_catalog_test.iloc[:,10:]

            #rename Business Term\n[Level 4] to title and Definition\n [Level 4] to description
            df_catalog_test = df_catalog_test.rename(columns={'Business Term\n[Level 4]': 'title', 'Definition\n [Level 4]': 'description'})

            #remove Domain Owner/Data Owner (DO) - L1 Domain, Data Steward (DS) - L2 Sub-Domain, Data Steward (DS) - L3 Data Class, Data Steward (DS) - L4 Business Term
            df_catalog_test = df_catalog_test.drop(columns=['Domain Owner/Data Owner (DO) - L1 Domain']) 
            df_catalog_test = df_catalog_test.drop(columns=['Domain Owner/Data Owner (DO) - L2 Sub-Domain'])
            df_catalog_test = df_catalog_test.drop(columns=['Domain Owner/Data Owner (DO) - L3 Data Class'])
            df_catalog_test = df_catalog_test.drop(columns=['Data Steward (DS)'])

            # from Consuming Systems/ Applications, replace \n\n with , 
            df_catalog_test['Consuming Systems/Applications'] = df_catalog_test['Consuming Systems/Applications'].str.replace('\n\n', ', ')

            #compare title and description columns with the title and description columns in df_terms
            df_catalog_test['title'] = df_catalog_test['title'].str.strip()
            df_catalog_test['description'] = df_catalog_test['description'].str.strip()

            df_terms['title'] = df_terms['title'].str.strip()
            df_terms['description'] = df_terms['description'].str.strip()

            # inner join df_catalog_test and df_terms on title and description
            df_catalog_test_merge = pd.merge(df_catalog_test, df_terms, on=['title', 'description'], how='inner')

            # check dupliactes
            is_duplicated = df_catalog_test_merge['title'].duplicated().any()

            missing_rows = df_catalog_test_merge[~df_catalog_test_merge['title'].isin(df_catalog_test['title'])]
            missing_rows = missing_rows.drop_duplicates(subset=['title'])
            missing_funds_df = pd.DataFrame(missing_rows, columns=['title'])

            missing_rows = df_catalog_test[~df_catalog_test['title'].isin(df_catalog_test_merge['title'])]
            missing_rows = missing_rows.drop_duplicates(subset=['title'])
            missing_funds_df_1 = pd.DataFrame(missing_rows, columns=['title'])


            print("Final Results")
            print("==============")

            if len(missing_funds_df) == 0 and len(missing_funds_df_1) == 0:
               print("All Business Terms are in Alation")
            elif len(missing_funds_df) > len(missing_funds_df_1):
               print("Duplicate terms in Alation")
            else:
               print("Some Business Terms are not in Alation")

         print("Upload Completed")
   except Exception as e:
         logging.error(f"An error occurred: {e}")
            
        
        
if __name__ == "__main__":
    # Inputs from the user
    api_access_token = input("Please enter the API token: ")
    file_path = input("Please enter the Excel file path or file name: ")
    domain_name = input("Please enter the Domain to be filtered: ")
    data_steward = input("Do you want to run Data Steward?(Y/N): ")

    # Run the script with the provided inputs
    run_script(file_path, domain_name, api_access_token)
