`Dataset`:My dataset comes from the clash royale API which houses player info clan info, location info, rank info which I used to create the dataset for clanbased decks based on the top ten players of the clans. 
To create this one must first sign up with an account to get access to the api and create a key that accepts the ip to make the calls to the api. 
I chose this because I thought it would be fun to find certain hidden trends or how different players act around the globe. Since this game is one I have played since a kid and still actively play it gave me the motivation to make a project out of it. 

`Learned`: In reading the data and creating features for it are the regions sharing same cards to put into their decks which at a first glance makese sense since these would be part of the meta of the game to create the most optimal decks from that. However what was found was that each region had a type of card used more than another so they may have been the same cards, but one used more often than the other. 

`Issues and Open Questions`: One of the questions I have thought about is being able to represent the world of clash royale through only the lens of the top players as though thye are the reason for leading meta trends, the problem comes down free to play and pay to win players. If I could some how figure out a signal for this it would help to make a feature for it. The missing data I feel that I cannot avoid is the info for players not in the top rankings since that data is not available unless you have their specific player tag. My data maybe limited depending on the type of players it is receiving it from. 
# Top Cards by Region & Sample Clan Strategies

A tidy breakdown of card usage by region, specific clan snapshots, and cards with notable regional differences.

---

## 1) Top Cards by Region
*(n = 50 decks per region; Usage = % of decks that include the card)*

### Europe
| # | Card              | Usage |
|---|-------------------|:-----:|
| 1 | The Log           | 48.0% |
| 2 | Cannon            | 36.0% |
| 3 | Fireball          | 34.0% |
| 4 | Skeletons         | 32.0% |
| 5 | Barbarian Barrel  | 28.0% |
| 6 | Ice Spirit        | 26.0% |
| 7 | Goblin Barrel     | 26.0% |
| 8 | Dart Goblin       | 24.0% |
| 9 | Arrows            | 24.0% |
|10 | Knight            | 24.0% |

### North America
| # | Card         | Usage |
|---|--------------|:-----:|
| 1 | The Log      | 46.0% |
| 2 | Skeletons    | 34.0% |
| 3 | Dart Goblin  | 26.0% |
| 4 | Arrows       | 26.0% |
| 5 | Ice Spirit   | 24.0% |
| 6 | Knight       | 24.0% |
| 7 | Tesla        | 24.0% |
| 8 | Firecracker  | 24.0% |
| 9 | Goblin Gang  | 20.0% |
|10 | Valkyrie     | 20.0% |

### South America
| # | Card         | Usage |
|---|--------------|:-----:|
| 1 | The Log      | 54.0% |
| 2 | Ice Spirit   | 36.0% |
| 3 | Fireball     | 34.0% |
| 4 | Skeletons    | 30.0% |
| 5 | Cannon       | 28.0% |
| 6 | Mega Knight  | 26.0% |
| 7 | Valkyrie     | 22.0% |
| 8 | Hog Rider    | 22.0% |
| 9 | Firecracker  | 20.0% |
|10 | Arrows       | 20.0% |

---

## 2) Sample Clan Strategies
*(10 decks sampled per clan)*

### 2 Chill guys (North America)
| Card          | Usage |
|---------------|:-----:|
| The Log       | 40.0% |
| Ice Wizard    | 30.0% |
| Firecracker   | 30.0% |
| Mini P.E.K.K.A| 30.0% |
| Fireball      | 20.0% |

### Deck Magnet (North America)
| Card        | Usage |
|-------------|:-----:|
| Skeletons   | 60.0% |
| Ice Spirit  | 50.0% |
| The Log     | 50.0% |
| Royal Hogs  | 40.0% |
| Arrows      | 40.0% |

### Fish (South America)
| Card           | Usage |
|----------------|:-----:|
| The Log        | 60.0% |
| Valkyrie       | 40.0% |
| Witch          | 40.0% |
| Electro Wizard | 30.0% |
| Mega Knight    | 30.0% |

### GTA5 ONLINE (South America)
| Card            | Usage |
|-----------------|:-----:|
| Mega Knight     | 60.0% |
| The Log         | 50.0% |
| Firecracker     | 50.0% |
| Hog Rider       | 50.0% |
| Skeleton Barrel | 30.0% |

### Griff and Dogs (North America)
| Card           | Usage |
|----------------|:-----:|
| The Log        | 50.0% |
| Skeletons      | 30.0% |
| Knight         | 30.0% |
| Fireball       | 30.0% |
| Skeleton Army  | 30.0% |

---

## 3) Cards with Regional Preferences
*(Higher variance ⇒ larger difference in regional usage)*

| Card             | Variance | Europe | North America | South America |
|------------------|:--------:|:------:|:-------------:|:-------------:|
| **Fireball**         | 72.00   | 34.0% | 16.0%         | 34.0%         |
| **Cannon**           | 67.56   | 36.0% | 16.0%         | 28.0%         |
| **Barbarian Barrel** | 46.22   | 28.0% | 16.0%         | 12.0%         |
| **Firecracker**      | 46.22   | 8.0%  | 24.0%         | 20.0%         |
| **Bats**             | 38.22   | 2.0%  | 14.0%         | 16.0%         |
| **Electro Wizard**   | 34.67   | 4.0%  | 8.0%          | 18.0%         |
| **Mega Knight**      | 34.67   | 12.0% | 16.0%         | 26.0%         |
| **Goblin Barrel**    | 32.89   | 26.0% | 18.0%         | 12.0%         |
| **Musketeer**        | 27.56   | 4.0%  | 2.0%          | 14.0%         |
| **Ice Spirit**       | 27.56   | 26.0% | 24.0%         | 36.0%         |

---

### Notes
- *Usage* is the share of sampled decks that include the card.
- Regional samples are equal-sized (50 decks each), enabling straightforward comparisons.
