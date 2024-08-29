
"""
Date: 11-05-2023
Team: Karthik Namani, Jessica R Hombal (karthik.namani@gds.ey.com, Jessica.R.Hombal@gds.ey.com)
Author: Jessica R Hombal (Jessica.R.Hombal@gds.ey.com)
File Name: Map_Target_to_Source.py

Date: 29-06-2023
Team: Sunny Sainani, Rohan Sharma (sunny.sainani@gds.ey.com, rohan.sharma7@gds.ey.com)
Author: Rohan Sharma (rohan.sharma7@gds.ey.com)
File Name: Map_Target_to_Source.py
Comments: Added derived to atomic logic

-----------------------------------------------------------------------------------------------------------------------

------ NLP Model development for mapping target records to source records ------

The goal of this development is to map the source records to their respective target records automatically 
without much human intervention. This process makes use of NLP modelling techniques such as Fuzzy string match 
and Semantic meaning to compute the scores that decide the best match.
Our chosen approach for mapping the best match is by considering the top three matching rows from computing 
similarity between Table name and Column name of source and target. Then finally re-arranging the top-three
similar rows on priority wise when it is computed against the Description using Word2Vec and Sentence Transformers.

-----------------------------------------------------------------------------------------------------------------------

------ Pre-requisites ------
1. Install pandas
2. Install numpy
3. Install NLTK
4. Install gensim
5. Install rapidfuzz
6. Install sentence-transformers

"""
#################################################################################################################################


import os
import sys
import pandas as pd
import numpy as np
import re
import json
import requests
import warnings
warnings.filterwarnings("ignore")
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
from scipy import spatial
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rapidfuzz import fuzz
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer

load_dotenv()

ALATION_API_TOKEN = os.getenv('API_TOKEN')
BASEURL = os.getenv('BASE_URL')

def get_source_df(base_url,token,gid):
    terms_url = '/integration/v2/term/?glossary_id=' + str(gid) + '&limit=10&skip=0&deleted=false'
    headers = {'Token': token, 'accept': 'application/json'}
    response = requests.get(base_url+terms_url, headers=headers,verify=False).json()
    source_df = pd.DataFrame.from_dict(response, orient='columns')
    source_df.to_csv('source_api_file.csv',index=False)
    source_df.rename(columns={'title': 'Attribute', 'description': 'Description'}, inplace=True)
    return source_df

def str_manipulation(text):
    words_list = re.findall(r'([a-z]+|[A-Z][a-z]*)', text)
    output_str = " ".join(words_list)
    output_str = output_str.lower()
    return output_str

# Function to remove HTML tags
def remove_html_tags(text):
    return BeautifulSoup(text, 'html.parser').get_text()

atm_attr = ['Payment_amount_Specifies the amount of the payment due','Payment_PaymentIdentifier_Unique identifier for each payment','Payment_PaymentDate_The date when each payment was made']
processed_attr = [str_manipulation(i) for i in atm_attr]

processed_attr = ['payment amount specifies the amount of the payment due','payment payment identifier unique identifier for each payment','payment payment date the date when each payment was made']

processed_attr1 = processed_attr[1:3]
processed_attr2 = processed_attr[1]
processed_attr3 = list([processed_attr[0],processed_attr[2]])



def preprocess(text):
    if isinstance(text, str) and text not in ('', 'NaN'):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokens = text.lower().split()
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        tokens = list(set(tokens))
        text = ' '.join(tokens)
        return text
    else:
        return ''


def fuzzy_score(source_col, target_col):
    
     # Calculate partial_ratio score
    partial_score = fuzz.partial_ratio(str(source_col), str(target_col))

    # Calculate token_sort_ratio score
    token_sort_score = fuzz.token_sort_ratio(str(source_col), str(target_col))

    # Get the highest score between partial_ratio and token_sort_ratio
    if token_sort_score > partial_score:
        highest_score_value = token_sort_score
    else:
        highest_score_value = partial_score
    return round(highest_score_value,2)

# Calculates the score on the basis of their meaning using Gensim word2vec
def calculate_similarity_score(sentence1, sentence2, model_path='path/to/word2vec/model'):
    # Load Word2Vec model
    word2vec_model = Word2Vec.load(model_path)

    # Calculate the similarity score
    similarity_score = word2vec_model.wv.n_similarity(sentence1, sentence2)
    similarity_score = similarity_score * 100
    
    return round(similarity_score, 2)

def semantic_transformer_score(source_col, target_col):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    source_embeddings = model.encode(source_col)
    target_embeddings = model.encode(target_col)
    score = (1 - spatial.distance.cosine(source_embeddings, target_embeddings))*100
    return round(score, 2)


def get_mapped_targets(source_df,target_df,source_table,source_attribute,source_description,target_table,target_attribute,target_description):
    top3_total_scores, fuzzy_scr, semantic_scr = [],[],[]
    #processed_attr = [str_manipulation(i) for i in mapping['Atomic Attribute concat']]
    if target_description is not None:
        target_df_copy = target_df[[target_table,target_attribute,target_description,(target_attribute+target_description)]].copy()
    else:
        target_df_copy = target_df[[target_table,target_attribute]].copy()
    if source_description is not None:
        source_df_copy = source_df[[source_table,source_attribute,source_description,(source_attribute+source_description),'al_datadict_item_properties', 'al_datadict_item_column_data_type','Attribute_Name']].copy()
    else:
        source_df_copy = source_df[[source_table,source_attribute,'al_datadict_item_properties', 'al_datadict_item_column_data_type','Attribute_Name']].copy()

    # source_df_copy = source_df.copy()
    # target_df_copy = target_df.copy()

    source_df_copy['Source Table'] = source_df_copy[source_table]
    source_df_copy['Source Attribute'] = source_df_copy[source_attribute]
    target_df_copy['Target Table'] = target_df_copy[target_table]
    target_df_copy['Target Attribute'] = target_df_copy[target_attribute]

    if target_description is not None: 
        target_df_copy['Target Description'] = target_df_copy[target_description]
        target_df_copy['Target Attribute Description'] = target_df['AttributeDescription']
    if target_table != "Target Table":
        target_df_copy.drop([target_table], axis=1, inplace=True)
    if target_attribute != "Target Attribute":
        target_df_copy.drop([target_attribute], axis=1, inplace=True)
    if target_description is not None and target_description != 'Target Description':
        target_df_copy.drop([target_description], axis=1, inplace=True)

    if source_description is not None:
        source_train = source_df_copy[(source_attribute+source_description)]
        source_df_copy['Source Description'] = source_df_copy[source_description]
        source_df_copy['Source Attribute Description'] = source_df['AttributeDescription']

    else:
        source_train = source_df_copy[source_attribute]
    if source_table != 'Source Table':
        source_df_copy.drop([source_table], axis=1, inplace=True)
    if source_attribute != 'Source Attribute':
        source_df_copy.drop([source_attribute], axis=1, inplace=True)
    if source_description is not None and source_description != 'Source Description':
        source_df_copy.drop([source_description], axis=1, inplace=True)

    mapped_targets_df = pd.DataFrame(columns=target_df_copy.columns)

    def train_word2vec_model(sentences, model_path='path/to/save/model'):
        # Preprocess the sentences
        preprocessed_sentences = [preprocess(sentence) for sentence in sentences]

        # Train Word2Vec model
        model = Word2Vec(preprocessed_sentences, min_count=1)

        # Save the trained model
        model.save(model_path)

    if os.path.exists('word2vec_model.bin'):
        os.remove('word2vec_model.bin')

    train_word2vec_model(source_train, model_path='word2vec_model.bin')

    for i, source_row in source_df_copy.iterrows():
        if source_description is not None: 
            source_desc = source_row['Source Description']
            source_tab_att = str(source_row['Source Attribute']) + "_" + str(source_row['Source Description']) + "_" + str(source_row['Source Attribute Description'])
            preprocessed_source_desc = preprocess(source_desc)
        else:
            source_tab_att = str(source_row['Source Attribute'])

        processed_source_tab_att = str_manipulation(str(source_tab_att))

        top3_scores = []
        top3_scores_index = []
        top3_scores_rows = []


        for j, target_row in target_df_copy.iterrows():
            if target_description is not None:
                target_tab_att = str(target_row['Target Attribute']) + "_" + str(target_row['Target Description'])+ "_" + str(target_row['Target Attribute Description'])
            else:
                target_tab_att = str(target_row['Target Attribute'])
            processed_target_tab_att = str_manipulation(str(target_tab_att))

            # Computing Fuzzy match score between table, column and description
            total_score = fuzzy_score(processed_source_tab_att, processed_target_tab_att)
            
            if bool(re.search(' Count ',processed_source_tab_att,re.IGNORECASE)):
                    if processed_target_tab_att==processed_attr2:
                        total_score = total_score*1.70
                        #print(re.search(' Count ',processed_source_tab_att,re.IGNORECASE)[0])
                    else:
                        pass
                    
                    
            if bool(re.search(' Total Payment Amount ',processed_source_tab_att,re.IGNORECASE)):
                for atm_concat in processed_attr3:
                    if processed_target_tab_att==atm_concat:
                        total_score = total_score*1.20
                        #print(re.search(' Total Payment Amount ',processed_source_tab_att,re.IGNORECASE)[0])
                    else:
                        pass
                    
            if bool(re.search(' Last .* Date ',processed_source_tab_att,re.IGNORECASE)):
                for atm_concat in processed_attr1:
                    if processed_target_tab_att==atm_concat:
                        total_score = total_score*1.20
                        #print(re.search(' Last .* Date ',processed_source_tab_att,re.IGNORECASE)[0])
                    else:
                        pass

            # Taking top-3 matches from target for a particular row of source
            # Top 3 scores extraction
            if len(top3_scores) < 3 or total_score > min(top3_scores):
                if len(top3_scores) == 3:
                    min_score_index = top3_scores.index(min(top3_scores))
                    top3_scores.pop(min_score_index)
                    top3_scores_index.pop(min_score_index)

                top3_scores.append(total_score)
                top3_scores_index.append(j)

                top3_scores_rows = target_df_copy.loc[top3_scores_index].copy()
                df = pd.DataFrame(top3_scores_rows)

        for data, tot_scr in zip(df.iterrows(), top3_scores):
            k, df_row = data

            if target_description is not None:
                target_desc = df_row['Target Description']
                preprocessed_target_desc = preprocess(target_desc)
                if preprocessed_target_desc == "" or (source_description is not None and preprocessed_source_desc == ""):
                    semantic_score = 0.0  # Assign a default or placeholder score for Null case
                else:
                    # Compute semantic similarity score against description of both source and target
                    if source_description is not None:  
                        semantic_score = semantic_transformer_score(str(preprocessed_source_desc), str(preprocessed_target_desc))
                    else: 
                        semantic_score = semantic_transformer_score(str(processed_source_tab_att), str(preprocessed_target_desc))

            else:
                if source_description is not None and preprocessed_source_desc == "":
                    semantic_score = 0.0
                else:
                    if source_description is not None:
                        semantic_score = semantic_transformer_score(str(preprocessed_source_desc), str(processed_target_tab_att))                                                   
                    else:
                        semantic_score = 0.0

            df.loc[k, 'fuzzy_score'] = tot_scr

            # Calculate the score for the current row
            score = tot_scr + semantic_score

            # Store the score in the 'total_score' column for the current row
            df.loc[k, 'total_score'] = np.round(score,2)

            # Store the score in the 'semantic_score' column for the current row
            df.loc[k, 'semantic_score'] = semantic_score

        # Sort the DataFrame rows in descending order of the 'total_score' column
        df = df.sort_values('total_score', ascending=False)
        # df.to_csv('intermediates/score_df.csv',index=False)
        # source_df_copy.to_csv('intermediates/source_df_before_merge_with_target.csv',index=False)
        # top3_total_scores.append(df['total_score'].tolist())
        # fuzzy_scr.append(df['fuzzy_score'].tolist())
        # semantic_scr.append(df['semantic_score'].tolist())

        # Get the best score (maximum) for each type of score
        best_total_score = max(top3_scores)
        best_fuzzy_score = max(df['fuzzy_score'])
        best_semantic_score = max(df['semantic_score'])

        top3_total_scores.append(best_total_score)
        fuzzy_scr.append(best_fuzzy_score)
        semantic_scr.append(best_semantic_score)

        df = df.drop(['total_score','fuzzy_score','semantic_score'], axis=1)

        mapped_targets_df.loc[i] = [df[col].tolist() for col in df.columns]
        # mapped_targets_df.to_csv('intermediates/mapped_targets.csv',index=False)

    def calculate_partial_match_score(total_score):
        partial_match_score = np.round((total_score / 200) * 100, 2)
        return partial_match_score
    
    
    source_df_copy = pd.concat([source_df_copy, mapped_targets_df], axis=1)
    source_df_copy[['Target Table 1','Target Table 2','Target Table 3']] = pd.DataFrame(source_df_copy['Target Table'].tolist(), index=source_df_copy.index)
    source_df_copy[['Target Attribute 1','Target Attribute 2','Target Attribute 3']] = pd.DataFrame(source_df_copy['Target Attribute'].tolist(), index=source_df_copy.index)
    if target_description is not None:
        source_df_copy[['Target Description 1','Target Description 2','Target Description 3']] = pd.DataFrame(source_df_copy['Target Description'].tolist(), index=source_df_copy.index)
        source_df_copy[['Target Attribute Description 1','Target Attribute Description 2','Target Attribute Description 3']] = pd.DataFrame(source_df_copy['Target Attribute Description'].tolist(), index=source_df_copy.index)
        source_df_copy['Target Description 1'] = source_df_copy['Target Attribute 1']
        source_df_copy['Target Attribute Description 1'] = source_df_copy['Target Attribute 1']
        source_df_copy.drop(['Target Table','Target Table 2','Target Table 3','Target Attribute','Target Attribute 2','Target Attribute 3','Target Description','AttributeDescription','Target Attribute Description','Target Description 2','Target Description 3','Target Attribute Description 2','Target Attribute Description 3'], axis=1, inplace=True)
    else:
        source_df_copy.drop(['Target Table','Target Attribute'], axis=1, inplace=True)

    source_df_copy['Fuzzy Score'] = fuzzy_scr
    source_df_copy['Semantic Score'] = semantic_scr
    source_df_copy['Total Score'] = top3_total_scores
    if  source_description is None and target_description is  None:
        source_df_copy['Partial_Match_Score'] = source_df_copy['Total Score']
    else:
        source_df_copy['Partial_Match_Score'] = source_df_copy['Total Score'].apply(calculate_partial_match_score)
    source_df_copy.rename(columns={'Target Attribute 1': 'Best recommendation based on Attribute', 'Target Description 1': 'Best recommendation based on Description', 
                                   'Target Attribute Description 1' : 'Best recommendation based on Attribute and Description'}, inplace=True)
    return source_df_copy.copy()  

def process_field(row):
    if pd.isna(row['Attribute']) or row['Attribute'] == '':
        value = row['key']
        value = value.split('.')[-1]
    else:
        value = row['Attribute']

    value = value.replace('_', ' ')
    return value

def Input(file_name,gid):
    target_df = get_source_df(BASEURL,ALATION_API_TOKEN,gid)
    source_df = pd.read_csv(file_name)
    source_df = source_df[source_df['al_datadict_item_properties'].str.split(';',expand=True)[1]=='otype=attribute']
    source_df['Attribute_Name'] = source_df['key'].str.split('.',expand=True)[3]
    source_df['description'] = source_df['description'].astype(str).apply(remove_html_tags)
    source_df.rename(columns={'title': 'Attribute', 'description': 'Description'}, inplace=True)
    source_df['Table'] = source_df['key']
    source_df['Attribute'] = source_df.apply(process_field, axis=1)
    target_df['Table'] = target_df.get('Table', 'dummy')
    source_df['AttributeDescription'] = source_df[['Attribute', 'Description']].astype(str).agg(' '.join, axis=1)
    target_df['AttributeDescription'] = target_df[['Attribute', 'Description']].astype(str).agg(' '.join, axis=1)
    return source_df, target_df

def save_dataframe_to_excel(df,initialFileName):
    root = tk.Tk()

    # Open save file dialog
    file_path = filedialog.asksaveasfilename(initialfile=initialFileName,defaultextension=".xlsx", 
                                             filetypes=[("Excel files", "*.xlsx"), 
                                                        ("All files", "*.*")])
    root.destroy()

    if file_path:
        df.to_excel(file_path, index=False)
        print(f"DataFrame saved to {file_path}")
    else:
        print("Save operation cancelled.")

def save_dataframe_to_csv(df,initialFileName):
    root = tk.Tk()

    # Open save file dialog
    file_path = filedialog.asksaveasfilename(initialfile=initialFileName,defaultextension=".csv", 
                                             filetypes=[("CSV files", "*.csv"), 
                                                        ("All files", "*.*")])
    root.destroy()

    if file_path:
        df.to_csv(file_path, index=False)
        print(f"DataFrame saved to {file_path}")
    else:
        print("Save operation cancelled.")

def main(file_name,gid, source_table, source_attribute, source_description, target_table, target_attribute, target_description):
    source, target = Input(file_name,gid)
    #source = pd.DataFrame(sourceReq)
    #target = pd.DataFrame(targetReq)
    # print(source.head(5))
    # print(target.head(5))
    mapped_source_df = get_mapped_targets(source, target, source_table, source_attribute, source_description, target_table, target_attribute, target_description)
    mapped_source_df.rename(columns={"Source Table":"Source Key"}, inplace=True)
    mapped_source_df.drop(['Target Table 1','Source Attribute Description'], axis=1, inplace=True)
    # mapped_source_df = mapped_source_df[mapped_source_df['Total Score'] > 60]
    business_df = mapped_source_df.drop(['Fuzzy Score', 'Semantic Score','Total Score','Partial_Match_Score'], axis =1)
    business_df['Suggested business term'] = ""
    print("Please save the Tech file:")
    save_dataframe_to_excel(mapped_source_df,"Tech_Data")
    print("Please save the business file:")
    save_dataframe_to_excel(business_df,"Business_data")
    print("*** Technical and Business files are saved successfully ***")


if __name__ == "__main__":  
    try: # Loop until a valid file is selected
        print("Please select the Data Dictionary file to be updated: ")
        root = tk.Tk() 
        inputFileName = filedialog.askopenfilename()
        print("Selected Data Dictionary file:",inputFileName)
        
        if inputFileName == "":
            print("You have not selected a Data Dictionary and hence cannot proceed further")
            sys.exit()
        gid = input("Please enter the Glossary ID from Alation: ")
    except NameError as e:
        print("You have not selected a Data Dictionary and hence cannot proceed further")
    
    

    
    # Run the script with the provided inputs
    main(inputFileName, gid, "Table", "Attribute", "Description", "Table", "Attribute", "Description")

#################################################################################################################################