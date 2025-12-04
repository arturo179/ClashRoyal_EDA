**Clash Royale Regional Playstyle Classification Using Machine Learning**
By Arturo Renteria


Abstract:

The purpose behind this to see if a machine learning model can reliably classify Clash Royale play regions
based on the composition of decks. This was done by analyzing a curated dataset from the Clash Royale Api.

The most effective model was the random forest model as it was able to find the hidden non-linear relationships between the players and stats of the cards

The dataset consisted of Player metadata, Clan information, Region labels, The eight cards used + their stats on the max level of the cards.

This led me to label the different regions into 6 separate categories known as 
`"WinCondition": ["Hog Rider", "Miner", "Graveyard", "Balloon", "Giant", "Royal Giant", "Goblin Barrel", "X-Bow", "Mortar"],
    "Beatdown": ["Golem", "Lava Hound", "Giant", "Electro Giant"],
    "Cycle": ["Skeletons", "Ice Spirit", "Fire Spirit", "Ice Golem"],
    "Air": ["Baby Dragon", "Lava Hound", "Minions", "Mega Minion", "Balloon"],
    "Control": ["Poison", "Tornado", "Bomb Tower", "Barbarian Barrel"],
    "BridgeSpam": ["Bandit", "Battle Ram", "Prince", "Dark Prince"],
    "SpellBait": ["Goblin Barrel", "Princess", "Rocket", "Inferno Tower"]`
This results from the common cards used from the decks of the top players of that region and the most common strategy always involved a win condition. 
`Conclusion`
Overal the best model was the random forest trained on an updated dataset that took in the information of the cards. Though as the data grew the recall and precision drastically went down as more regions were added to it. 







############################################################
    Baseline 0.09090909090909091
    precision    recall  f1-score   support

      Afghanistan       0.00      0.00      0.00        10
           Africa       0.00      0.00      0.00        10
          Albania       0.22      0.20      0.21        10
          Algeria       0.00      0.00      0.00        10
             Asia       0.00      0.00      0.00        10
           Europe       0.00      0.00      0.00        10
    International       0.08      0.10      0.09        10
    North America       0.07      0.10      0.08        10
          Oceania       0.17      0.20      0.18        10
    South America       0.09      0.10      0.10        10
    Åland Islands       0.43      0.30      0.35        10

     accuracy                           0.09       110
    macro avg       0.10      0.09      0.09       110
 weighted avg       0.10      0.09      0.09       110

############################################################

    randomForestClassifier
    0.14545454545454545
    precision    recall  f1-score   support

    Afghanistan     0.00      0.00      0.00        10
       Africa       0.25      0.20      0.22        10
      Albania       0.11      0.10      0.11        10
      Algeria       0.17      0.20      0.18        10
         Asia       0.33      0.20      0.25        10
       Europe       0.17      0.10      0.12        10
    International   0.14      0.20      0.17        10
    North America   0.14      0.20      0.17        10
      Oceania       0.12      0.10      0.11        10
    South America   0.18      0.20      0.19        10
    Åland Islands   0.12      0.10      0.11        10

     accuracy                           0.15       110
    macro avg       0.16      0.15      0.15       110
    weighted avg       0.16      0.15      0.15       110

############################################################
############################################################


    LogisticRegression
    0.1
    precision    recall  f1-score   support

    Afghanistan     0.13      0.20      0.16        10
       Africa       0.00      0.00      0.00        10
      Albania       0.00      0.00      0.00        10
      Algeria       0.06      0.10      0.07        10
         Asia       0.25      0.10      0.14        10
       Europe       0.07      0.10      0.08        10
    International   0.08      0.10      0.09        10
    North America   0.09      0.10      0.10        10
      Oceania       0.14      0.10      0.12        10
    South America   0.00      0.00      0.00        10
    Åland Islands   0.43      0.30      0.35        10

     accuracy                           0.10       110
    macro avg       0.11      0.10      0.10       110
 weighted avg       0.11      0.10      0.10       110

############################################################

