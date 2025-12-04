from matplotlib.pyplot import annotate
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler, label_binarize
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import roc_curve, auc, RocCurveDisplay
import matplotlib.pyplot as plt
df = pd.read_csv("clan_based_decks2.csv")

import ast

df['card_names'] = df['card_names'].apply(ast.literal_eval)

mlb = MultiLabelBinarizer()
card_features = mlb.fit_transform(df['card_names'])
card_df = pd.DataFrame(card_features, columns=mlb.classes_)
stats_col = ["avg_hp","avg_damage","avg_elixir","total_hp","total_damage"]
stats_col = [c for c in stats_col if c in df.columns]

deck_stats_df = df[stats_col].copy()
deck_stats_df = deck_stats_df.fillna(deck_stats_df.mean())
scaler_stats = StandardScaler()

deck_stats_scaled = scaler_stats.fit_transform(deck_stats_df)

deck_stats_df_scaled = pd.DataFrame(deck_stats_scaled, columns=stats_col,index=df.index)


X = pd.concat([card_df,deck_stats_df_scaled],axis=1)
X.columns = X.columns.astype(str)
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
report_dic = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report_dic).transpose()

region_rows = sorted(y_test.unique())
metrics_df = report_df.loc[region_rows, ['precision', 'recall', 'f1-score']]


ax = metrics_df.plot(kind="bar",figsize=(12,6),width =.8)

ax.set_title("Random Classification report")
ax.set_xlabel("Region")
ax.set_ylabel("Score")
ax.set_ylim(0,1)
plt.xticks(rotation=45,ha ="right")

for container in ax.containers:
    ax.bar_label(container,fmt='%.2f',label_type="center",fontsize = 8,color="white")

plt.legend(title="metric")
plt.tight_layout()
plt.show()


rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

print("#"*60)
print("randomForestClassifier")
print(accuracy_score(y_test, rf.predict(X_test)))
print(classification_report(y_test, rf.predict(X_test)))


report_dic = classification_report(y_test, rf_pred, output_dict=True)
report_df = pd.DataFrame(report_dic).transpose()

region_rows = sorted(y_test.unique())
metrics_df = report_df.loc[region_rows, ['precision', 'recall', 'f1-score']]


ax = metrics_df.plot(kind="bar",figsize=(12,6),width =.8)

ax.set_title(" Random forest Classification report")
ax.set_xlabel("Region")
ax.set_ylabel("Score")
ax.set_ylim(0,1)
plt.xticks(rotation=45,ha ="right")

for container in ax.containers:
    ax.bar_label(container,fmt='%.2f',label_type="center",fontsize = 8,color="white")

plt.legend(title="metric")
plt.tight_layout()
plt.show()

print("#"*60)

model_linear = LogisticRegression(max_iter=10000)
model_linear.fit(X_train, y_train)
y_pred_lr= model_linear.predict(X_test)
print("#"*60)
print("LogisticRegression")
print(accuracy_score(y_test, model_linear.predict(X_test)))
print(classification_report(y_test, model_linear.predict(X_test)))
print("#"*60)
region_patterns = df.explode('card_names').groupby(['location_name','card_names']).size().unstack(fill_value=0)

report_dic = classification_report(y_test, y_pred_lr, output_dict=True)
report_df = pd.DataFrame(report_dic).transpose()

region_rows = sorted(y_test.unique())
metrics_df = report_df.loc[region_rows, ['precision', 'recall', 'f1-score']]


ax = metrics_df.plot(kind="bar",figsize=(12,6),width =.8)

ax.set_title("Logistic Regression Classification report")
ax.set_xlabel("Region")
ax.set_ylabel("Score")
ax.set_ylim(0,1)
plt.xticks(rotation=45,ha ="right")

for container in ax.containers:
    ax.bar_label(container,fmt='%.2f',label_type="center",fontsize = 8,color="white")

plt.legend(title="metric")
plt.tight_layout()
plt.show()

classes = sorted(y.unique())
y_test_bin = label_binarize(y_test, classes=classes)
y_score = rf.predict_proba(X_test)

region_usage_rate = region_patterns.div(region_patterns.sum(axis=1), axis=0)

print("Card Usage Rate")
print(region_usage_rate.iloc[:5, :10])
print("#"*60)


import seaborn as sns
top_cards = region_patterns.sum(axis=0).sort_values(ascending=False).head(10).index
region_usage_top = region_usage_rate[top_cards]
plt.figure(figsize=(16,6))
sns.heatmap(region_usage_top, annot=False, fmt="g")
plt.title("Card Usage Rate")
plt.xlabel("Card")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,8))
for i, region in enumerate(classes):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr,tpr,lw=1.8,label=f'{region}(AUC = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves by Region')
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()


X_scaled_full = StandardScaler().fit_transform(X)
pca = PCA(n_components=2)
reduced = pca.fit_transform(X_scaled_full)

regions = y.astype("category")
region_codes = regions.cat.codes

plt.figure(figsize=(7,5))
plt.scatter(reduced[:, 0], reduced[:, 1], c=region_codes)
plt.title("PCA of decks (colored by region)")
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.tight_layout()
plt.show()

kmeans = KMeans(n_clusters=10, n_init="auto",random_state=42)
clusters = kmeans.fit_predict(reduced)

plt.figure(figsize=(7,5))
plt.scatter(reduced[:, 0], reduced[:, 1], c=clusters, s=10)
plt.title("PCA of decks (colored by cluster)")
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.tight_layout()
plt.show()

cluster_df = pd.DataFrame({'cluster': clusters, "region": y})
print("#" * 60)
print("Cluster vs Region")
print("#" * 60)
print(pd.crosstab(cluster_df["cluster"], cluster_df["region"], normalize='index', margins=False))


strategy_tags = {
    "WinCondition": ["Hog Rider", "Miner", "Graveyard", "Balloon",
                     "Giant", "Royal Giant", "Goblin Barrel", "X-Bow", "Mortar"],
    "Beatdown": ["Golem", "Lava Hound", "Giant", "Electro Giant"],
    "Cycle": ["Skeletons", "Ice Spirit", "Fire Spirit", "Ice Golem"],
    "Air": ["Baby Dragon", "Lava Hound", "Minions", "Mega Minion", "Balloon"],
    "Control": ["Poison", "Tornado", "Bomb Tower", "Barbarian Barrel"],
    "BridgeSpam": ["Bandit", "Battle Ram", "Prince", "Dark Prince"],
    "SpellBait": ["Goblin Barrel", "Princess", "Rocket", "Inferno Tower"]
}

region_strategy_counts = (
    df.explode("card_names")
    .groupby(["location_name", "card_names"])
    .size()
    .reset_index(name="count")
)

def card_strategy(card):
    tags = []
    for strat, cards in strategy_tags.items():
        if card in cards:
            tags.append(strat)
    return tags

region_strategy_counts["strategies"] = (
    region_strategy_counts["card_names"].apply(card_strategy)
)
region_strat_exploded = (
    region_strategy_counts.explode("strategies")
    .dropna(subset=["strategies"])
)
strategy_profile = region_strat_exploded.pivot_table(index="location_name", columns="strategies", values="count", aggfunc="sum", fill_value=0)
strategy_profile = strategy_profile.div(strategy_profile.sum(axis=1), axis=0)
print(strategy_profile.head())

plt.figure(figsize=(10, 6))
sns.heatmap(strategy_profile, annot=True, fmt=".2f", cmap="magma")
plt.title("Strategy Profile by Region")
plt.xlabel("Strategy")
plt.ylabel("Region")
plt.tight_layout()
plt.show()




