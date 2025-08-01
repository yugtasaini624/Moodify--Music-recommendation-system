import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

def modelTrain():
    dfMain = pd.read_csv('mood.csv')
    df = dfMain.copy()

    colns = ['sleep_hours','screen_time','activity','time_of_day','mood_scale','social_preference']

    # converting text data to numerical
    time_order = ['morning','afternoon','evening','night']
    time_encoder = OrdinalEncoder(categories=[time_order])
    df['time_of_day'] = time_encoder.fit_transform(df[['time_of_day']])

    activity_order = ['studying','working out','relaxing']
    activity_encoder = OrdinalEncoder(categories=[activity_order])
    df['activity'] = activity_encoder.fit_transform(df[['activity']])

    df['social_preference'] = df['social_preference'].map({'no': 0, 'yes': 1})

    mood_encoder = LabelEncoder()
    df['mood'] = mood_encoder.fit_transform(df['mood'])

    # initialization
    X = df.iloc[:, 0:6]
    y = df.iloc[:, 6]

    # data training
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=34)
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # model fitting
    model.fit(X_train, y_train)

    return model, time_encoder, activity_encoder, colns, mood_encoder 

def predictor(input_list, model, time_encoder, activity_encoder, mood_encoder, colns):
    inputVal = pd.DataFrame([input_list], columns=colns)

    # changing text input to numerical
    inputVal['activity'] = activity_encoder.transform(inputVal[['activity']])
    inputVal['time_of_day'] = time_encoder.transform(inputVal[['time_of_day']])
    inputVal['social_preference'] = inputVal['social_preference'].map({'no': 0, 'yes': 1})

    # predicting mood
    y_pred = model.predict(inputVal)
    predicted_label = mood_encoder.inverse_transform([y_pred[0]])

    return predicted_label[0]  