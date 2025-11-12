import polars as pl
import pandas as pd
import requests
import json
from typing import List, Dict, Tuple
import time
import numpy as np
from collections import Counter
from dotenv import load_dotenv
import os



load_dotenv()
API_KEY = os.getenv("API_TOKEN")



class ClanBasedStrategyClassifier:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        self.base_url = "https://api.clashroyale.com/v1"
        self.cards_df = None
        self.locations_df = None

    def fetch_cards(self):
        """Fetch all cards data"""
        url = f"{self.base_url}/cards"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        cards = resp.json().get("items", [])
        self.cards_df = pl.DataFrame(cards)
        print(f"Fetched {len(cards)} cards")
        return self.cards_df

    def fetch_locations(self):
        """Fetch all locations/regions"""
        url = f"{self.base_url}/locations"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        locations = resp.json().get("items", [])
        self.locations_df = pl.DataFrame(locations)
        print(f"Fetched {len(locations)} locations")
        return self.locations_df

    def get_location_name(self, location_id: int) -> str:
        """Get location name from ID"""
        if self.locations_df is not None:
            match = self.locations_df.filter(pl.col("id") == location_id)
            if len(match) > 0:
                return match.select("name").item()
        return f"Location_{location_id}"

    def fetch_top_clans_by_location(self, location_id: int, limit: int = 20) -> List[Dict]:
        """Fetch top clans from a specific location"""
        url = f"{self.base_url}/locations/{location_id}/rankings/clans"
        params = {"limit": limit}

        print(f"  Fetching top {limit} clans from location {location_id}...")
        resp = requests.get(url, params=params, headers=self.headers, timeout=10)
        resp.raise_for_status()

        clans = resp.json().get("items", [])
        print(f" Found {len(clans)} clans")
        return clans

    def fetch_clan_members(self, clan_tag: str) -> List[Dict]:
        """Fetch all members of a clan"""
        clan_tag_clean = clan_tag.replace("#", "")
        url = f"{self.base_url}/clans/%23{clan_tag_clean}/members"

        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()

        members = resp.json().get("items", [])
        return members

    def fetch_player_details(self, player_tag: str) -> Dict:
        """Fetch detailed player data including current deck"""
        player_tag_clean = player_tag.replace("#", "")
        url = f"{self.base_url}/players/%23{player_tag_clean}"

        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()

        return resp.json()

    def collect_clan_deck_data(self, location_ids: List[int],
                               clans_per_location: int = 10,
                               members_per_clan: int = 10,
                               delay_between_requests: float = 0.2) -> pd.DataFrame:
        """
        Collect deck data from clan members across regions

        Strategy:
        1. Get top clans from each region
        2. Get members from each clan
        3. Get deck data from each member

        This gives us regional strategy patterns through clan composition
        """
        deck_data = []

        for loc_id in location_ids:
            location_name = self.get_location_name(loc_id)
            print(f"\n{'=' * 60}")
            print(f"Region: {location_name} (ID: {loc_id})")
            print(f"{'=' * 60}")

            try:
                # Get top clans from this region
                top_clans = self.fetch_top_clans_by_location(loc_id, clans_per_location)

                for clan_idx, clan in enumerate(top_clans, 1):
                    clan_tag = clan.get("tag", "")
                    clan_name = clan.get("name", "Unknown")
                    clan_score = clan.get("clanScore", 0)

                    print(f"\n  [{clan_idx}/{len(top_clans)}] Clan: {clan_name} ({clan_tag}) - Score: {clan_score}")

                    try:
                        # Get clan members
                        members = self.fetch_clan_members(clan_tag)
                        print(f"    Found {len(members)} members")

                        # Sample members (don't fetch all 50 to save API calls)
                        sampled_members = members[:members_per_clan]

                        for member_idx, member in enumerate(sampled_members, 1):
                            player_tag = member.get("tag", "")
                            player_name = member.get("name", "Unknown")

                            print(f"      [{member_idx}/{len(sampled_members)}] {player_name}...", end=" ")

                            try:
                                player_details = self.fetch_player_details(player_tag)
                                current_deck = player_details.get("currentDeck", [])

                                if current_deck:
                                    card_ids = [card.get("id") or card.get("name") for card in current_deck]

                                    deck_data.append({
                                        "player_tag": player_tag.replace("#", ""),
                                        "player_name": player_name,
                                        "clan_tag": clan_tag.replace("#", ""),
                                        "clan_name": clan_name,
                                        "location_id": loc_id,
                                        "location_name": location_name,
                                        "cards": card_ids,
                                        "trophies": player_details.get("trophies", 0),
                                        "clan_score": clan_score
                                    })
                                    print(f" {len(card_ids)} cards")
                                else:
                                    print(" No deck")

                                time.sleep(delay_between_requests)

                            except requests.exceptions.HTTPError as e:
                                if e.response.status_code == 404:
                                    print(" Not found")
                                elif e.response.status_code == 429:
                                    print(" Rate limited! Waiting...")
                                    time.sleep(5)
                                else:
                                    print(f" HTTP {e.response.status_code}")
                            except Exception as e:
                                print(f" Error")
                                continue

                        time.sleep(delay_between_requests)

                    except Exception as e:
                        print(f"     Error getting clan members: {str(e)[:50]}")
                        continue

                decks_from_location = len([d for d in deck_data if d['location_id'] == loc_id])
                print(f"\n   Total decks from {location_name}: {decks_from_location}")

            except Exception as e:
                print(f"   Error: {e}")
                continue

        print(f"\n{'=' * 60}")
        print(f"TOTAL DECKS COLLECTED: {len(deck_data)}")
        print(f"{'=' * 60}")

        return pd.DataFrame(deck_data)

    def analyze_clan_strategies(self, deck_data: pd.DataFrame):
        """Analyze strategy differences between clans and regions"""
        print("\n" + "=" * 60)
        print("CLAN STRATEGY ANALYSIS")
        print("=" * 60)

        if deck_data.empty:
            print("No data to analyze!")
            return

        # 1. Cards by region
        print("\n1. Top Cards by Region:")
        for location in deck_data['location_name'].unique():
            location_data = deck_data[deck_data['location_name'] == location]

            # Flatten all cards from this region
            all_cards = []
            for cards in location_data['cards']:
                all_cards.extend(cards)

            card_freq = Counter(all_cards)
            print(f"\n  {location} (n={len(location_data)} decks):")
            for card, count in card_freq.most_common(10):
                percentage = (count / len(location_data)) * 100
                print(f"    {card}: {percentage:.1f}%")

        # 2. Cards by clan
        print("\n2. Sample Clan Strategies:")
        clans_sample = deck_data.groupby('clan_name').size().sort_values(ascending=False).head(5)

        for clan_name in clans_sample.index:
            clan_data = deck_data[deck_data['clan_name'] == clan_name]

            # Get most common cards in this clan
            all_cards = []
            for cards in clan_data['cards']:
                all_cards.extend(cards)

            card_freq = Counter(all_cards)
            location = clan_data.iloc[0]['location_name']

            print(f"\n  {clan_name} ({location}) - {len(clan_data)} decks:")
            for card, count in card_freq.most_common(5):
                percentage = (count / len(clan_data)) * 100
                print(f"    {card}: {percentage:.1f}%")

        # 3. Regional differences
        print("\n3. Cards with Regional Preferences:")

        # Build card frequency matrix
        card_location_freq = {}

        for _, row in deck_data.iterrows():
            location = row['location_name']
            for card in row['cards']:
                if card not in card_location_freq:
                    card_location_freq[card] = {}
                if location not in card_location_freq[card]:
                    card_location_freq[card][location] = 0
                card_location_freq[card][location] += 1

        # Calculate variance
        location_counts = deck_data.groupby('location_name').size().to_dict()
        card_variance = {}

        for card, loc_counts in card_location_freq.items():
            percentages = []
            for loc, count in loc_counts.items():
                pct = (count / location_counts[loc]) * 100
                percentages.append(pct)

            if len(percentages) > 1:
                card_variance[card] = np.var(percentages)

        # Show cards with high variance
        sorted_variance = sorted(card_variance.items(), key=lambda x: x[1], reverse=True)

        print("\n  Cards showing regional strategy differences:")
        for card, variance in sorted_variance[:10]:
            print(f"\n    {card} (variance: {variance:.2f}):")
            for loc in deck_data['location_name'].unique():
                loc_data = deck_data[deck_data['location_name'] == loc]
                card_count = sum(1 for cards in loc_data['cards'] if card in cards)
                pct = (card_count / len(loc_data)) * 100 if len(loc_data) > 0 else 0
                print(f"      {loc}: {pct:.1f}%")


def main():


    classifier = ClanBasedStrategyClassifier(API_KEY)

    # Fetch basic data
    print("=" * 60)
    print("FETCHING BASIC DATA")
    print("=" * 60)

    cards_df = classifier.fetch_cards()
    locations_df = classifier.fetch_locations()

    # Show available locations
    print("\nAvailable locations:")
    print(locations_df.select(["id", "name", "isCountry"]).head(20))

    # Choose locations to analyze
    # Use location IDs that you know have clan rankings
    target_locations = [
        57000000,  #Example: adjust based on your findings
        57000001,
        57000002
    ]

    print(f"\n{'=' * 60}")
    print("COLLECTING CLAN DATA")
    print("=" * 60)

    # Collect data
    deck_data = classifier.collect_clan_deck_data(
        location_ids=target_locations,
        clans_per_location=5,  # Top 5 clans per region
        members_per_clan=10,  # 10 members per clan
        delay_between_requests=0.2  # Rate limiting
    )

    if len(deck_data) > 0:
        print("\n Data collection successful!")
        print(f"Collected {len(deck_data)} decks")
        print(f"From {deck_data['clan_name'].nunique()} clans")
        print(f"Across {deck_data['location_name'].nunique()} regions")

        # Save raw data
        deck_data.to_csv("clan_based_deckss.csv", index=False)
        print("\n Saved to: clan_based_deckss.csv")

        # Analyze strategies
        classifier.analyze_clan_strategies(deck_data)

        # Now you can build your classifier
        print("\n" + "=" * 60)
        print("READY FOR CLASSIFICATION")
        print("=" * 60)
        print("\nNext steps:")


        return deck_data
    else:
        print(" No data collected!")
        return None


