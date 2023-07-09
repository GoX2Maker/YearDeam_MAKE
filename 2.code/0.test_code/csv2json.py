
import pandas as pd


csvFilePath = r'1.data\3.DB\prescript_labeling.csv'
jsonFilePath = r'1.data\3.DB\prescript_labeling.json'
df = pd.read_csv(csvFilePath, encoding='utf-8')
df.to_json (jsonFilePath, orient='records', force_ascii=False)


 
