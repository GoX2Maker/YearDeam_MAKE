import pandas as pd

df = pd.read_csv(r'1.data\3.DB\medicine_list.csv')


# regex를 이용하여 영어, 숫자, 한글만 남기고 나머지 문자를 모두 제거합니다.
df['제품명'] = df['제품명'].str.replace(r'[^a-zA-Z0-9가-힣]', '', regex=True)

df.to_csv(r'1.data\3.DB\medicine_list.csv', index=False, encoding='utf-8')

