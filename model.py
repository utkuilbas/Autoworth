import pandas as pd
from sklearn import preprocessing
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import numpy as np

def predictPrice(jsonData):

    path = 'car-price-dataset.csv'
    df = pd.read_csv(path)

    le_dict = {} # label encoders işlemi gerçekleştirilir. veri değerlerini sayısal olarak etiketler.
    for item in ['Marka', 'Seri', 'Model', 'Yıl', 'VitesTipi', 'YakıtTipi', 'KasaTipi']:
        le = preprocessing.LabelEncoder()
        df[item] = le.fit_transform(df[item])
        df[item] = df[item].astype('int64')
        le_dict[item] = le

    X = df.drop(['Fiyat', 'MotorHacmi', 'MotorGücü', 'Çekiş'], axis=1)
    y = df['Fiyat']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=144) #eğitim ve test verisini ayırma

    #burası 10-15 dakika sürüyor, en iyi parametreleri bulmaya yarar. bir defa çalıştırmak yeterli, kullanılan veri için sonuç aşağıda best_params olarak verilmiştir.
    """params = {
        "colsample_bytree":[0.4,0.5,0.6],
        "learning_rate":[0.01,0.02,0.09],
        "max_depth":[2,3,4,5,6],
        "n_estimators":[100,200,500,2000]
    }

    xgb = XGBRegressor()
    grid = GridSearchCV(xgb,params,cv=10,n_jobs=-1,verbose=2)
    grid.fit(X_train,y_train)
    print(grid.best_params_)"""

    best_params = {'colsample_bytree': 0.4, 'learning_rate': 0.02, 'max_depth': 4, 'n_estimators': 2000}
    xgb1 = XGBRegressor(**best_params)
    model_xgb = xgb1.fit(X_train, y_train) # model eğitimi

    json_data = jsonData

    def transform_with_label_encoder(le, value):
        if value not in le.classes_:
            le.classes_ = np.append(le.classes_, value)

        return le.transform([value])[0]

    data = { # kullanıcıdan gelen veirler için label encoding işlemi
        "Marka": [transform_with_label_encoder(le_dict['Marka'], json_data['brand'])],
        "Seri": [transform_with_label_encoder(le_dict['Seri'], json_data['series'])],
        "Model": [transform_with_label_encoder(le_dict['Model'], json_data['model'])],
        "Yıl": [transform_with_label_encoder(le_dict['Yıl'], int(json_data['year']))],
        "Kilometre": [int(json_data['km'])],
        "VitesTipi": [transform_with_label_encoder(le_dict['VitesTipi'], json_data['transmission'])],
        "YakıtTipi": [transform_with_label_encoder(le_dict['YakıtTipi'], json_data['fuel'])],
        "KasaTipi": [transform_with_label_encoder(le_dict['KasaTipi'], json_data['body'])]
    }


    df2 = pd.DataFrame(data)


    prediction = model_xgb.predict(df2)[0]
    return prediction



