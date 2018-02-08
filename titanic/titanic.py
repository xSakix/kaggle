#nspired by https://www.kaggle.com/mrisdal/exploring-survival-on-the-titanic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

print(len(train))
print(len(test))

full = train.copy(deep=True)
full = full.append(test)
# full = full.join(test)

print(full.head())
print(len(full))
print(full.dtypes)

names = full.Name
titles = []
surnames = []
for name in names.values:
    title = re.sub('(.*, )|(\\..*)', '', str(name))
    titles.append(title)
    surname = str(name).split(',')
    surnames.append(surname[0])

full['Title'] = titles
full['Surname'] = surnames
print('Unique surnames:' + str(full.Surname.nunique()) + "/" + str(len(full.Surname)))
tab = full.groupby(['Sex', 'Title']).size().unstack().fillna(0)
print(tab)
rare_titles = ['Capt', 'Col', 'Don', 'Dona', 'Dr', 'Jonkheer', 'Lady', 'Major', 'Rev', 'Sir', 'the Countess']
# print(rare_titles)
idx = pd.IndexSlice
full.loc[full['Title'] == 'Mlle', 'Title'] = 'Miss'
full.loc[full['Title'] == 'Ms', 'Title'] = 'Miss'
full.loc[full['Title'] == 'Mme', 'Title'] = 'Mrs'
for rare_title in rare_titles:
    full.loc[full['Title'] == rare_title, 'Title'] = 'Rare Title'

tab = full.groupby(['Sex', 'Title']).size().unstack().fillna(0)

print(tab)

# family size
full['Fsize'] = full['SibSp'] + full['Parch'] + 1
# print(len(full['Fsize']))
full['Family'] = full['Surname'].astype(str) + '_' + full['Fsize'].astype(str)
# print(full['Family'])
# print(len(full['Survived']))

sub = full[['Fsize', 'Survived']]
grouped = sub.groupby(['Fsize', 'Survived']).size()
grouped = grouped.reset_index(level=['Fsize', 'Survived'])
grouped.columns = ['Fsize', 'Survived', 'Count']
for fs in grouped['Fsize'].unique():
    if len(grouped[grouped['Fsize'] == fs]) < 2:
        df = pd.DataFrame([[fs,1.0,0]], columns=['Fsize', 'Survived', 'Count'])
        grouped = grouped.append(df)

print(grouped)

died = grouped[grouped['Survived'] == 0.]['Count'].values
survived = grouped[grouped['Survived'] == 1.]['Count'].values

print(died)
print(survived)

# plt.plot(full['Fsize']., full['Survived'],'o')
plt.bar(np.sort(full['Fsize'].unique())-0.2, died,width=0.5)
plt.bar(np.sort(full['Fsize'].unique()) + 0.3, survived,width=0.5)
plt.legend(['died','survived'])
plt.show()
