import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score
from imblearn.under_sampling import RandomUnderSampler
import joblib
import xgboost as xgb


data = pd.read_csv("wesad_sync.csv")
# Convert to binary
data['label'] = data['label'].apply(lambda x: 1 if x == 2 else 0)
rus = RandomUnderSampler()
data_x = data[['HR', 'acc_x', 'acc_y', 'acc_z']]
data_y = data['label']
x_res, y_res = rus.fit_resample(data_x, data_y)
x_res = x_res.reset_index(drop=True)
y_res = y_res.reset_index(drop=True)
data_x_train, data_x_test, data_y_train, data_y_test = train_test_split(x_res,y_res,test_size=0.2)
model = xgb.XGBClassifier(
    n_estimators=100, 
    learning_rate=0.1, 
    max_depth=3,
    objective='binary:logistic', # For classification
    eval_metric='logloss'
)

model.fit(data_x_train, data_y_train)
# joblib.dump(model, "WESAD_binary_xgboost.pkl")
