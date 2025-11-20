
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler, label_binarize
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import roc_curve, auc, RocCurveDisplay
import matplotlib.pyplot as plt
df = pd.read_csv("clan_based_deckss.csv")

import ast

df['cards'] = df['cards'].apply(ast.literal_eval)

mlb = MultiLabelBinarizer()
card_features = mlb.fit_transform(df['cards'])
card_df = pd.DataFrame(card_features, columns=mlb.classes_)

data = pd.concat([card_df,df[['location_name']]],axis=1)

X = card_df
y = df['location_name']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
#Start of the different models to be tested
dummy = DummyClassifier(strategy='uniform', random_state=42)
dummy.fit(X_train, y_train)
y_pred = dummy.predict(X_test)


dummy.fit(X_train, y_train)
print("#"*60)
print("Baseline",accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
model = RandomForestClassifier()
model.fit(X_train, y_train)

print("#"*60)
print("randomForestClassifier")
print(accuracy_score(y_test, model.predict(X_test)))
print(classification_report(y_test, model.predict(X_test)))

print("#"*60)

model_linear = LogisticRegression(max_iter=10000)
model_linear.fit(X_train, y_train)
print("#"*60)
print("LogisticRegression")
print(accuracy_score(y_test, model_linear.predict(X_test)))
print(classification_report(y_test, model_linear.predict(X_test)))
print("#"*60)
region_patterns = df.explode('cards').groupby(['location_name','cards']).size().unstack(fill_value=0)


classes = sorted(y.unique())
y_test_bin = label_binarize(y_test, classes=classes)
y_score = model.predict_proba(X_test)

for i, region in enumerate(classes):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr,tpr,lw=2,label=f'{region}(AUC = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves by Region')
plt.legend(loc="lower right")
plt.show()


X_scaled = StandardScaler().fit_transform(card_df)
pca = PCA(n_components=2)
reduced = pca.fit_transform(card_df)

kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(reduced)

plt.scatter(reduced[:,0],reduced[:,1], c=clusters)
plt.show()

y_pred = model.predict(X_test)
disp = ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred,display_labels=model.classes_,normalize='true',cmap='Blues')
disp.plot()
