import pandas as pd
import matplotlib as mpl
import datetime

patients = pd.read_csv('patients.csv', parse_dates = ['BIRTHDATE', 'DEATHDATE'])[['Id', 'BIRTHDATE', 'DEATHDATE']]
totalcosts = pd.read_csv('procedures.csv')[['PATIENT', 'COST']]

patients['BIRTHYEAR'] = pd.DatetimeIndex(patients['BIRTHDATE']).year
patients['DEATHYEAR'] = pd.DatetimeIndex(patients['DEATHDATE']).year
patients['DEATHYEAR'].fillna(datetime.date.today().year, inplace = True)

patients['age'] = patients['DEATHYEAR'] - patients['BIRTHYEAR']
patients = patients[['Id', 'age']]

totalcosts = totalcosts.groupby(['PATIENT']).sum()

final = pd.merge(patients,totalcosts, left_on='Id',right_on='PATIENT',how='inner',suffixes=('_left','_right'))

final.sort_values(by = ['COST'], inplace = True)

final.plot.scatter(x = 'age', y = 'COST')
mpl.pyplot.show()
final.to_csv('test.csv')
