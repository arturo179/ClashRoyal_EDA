import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


def create_clash_royale_visualizations(deck_data: pd.DataFrame, output_dir: str = "."):


    if deck_data.empty:
        print("No data to visualize!")
        return None

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)

    print("\n" + "=" * 60)
    print("CREATING VISUALIZATIONS")
    print("=" * 60)

    viz_paths = {}

    # === VISUALIZATION 1: Distribution - Top Cards Overall ===
    print("\n1. Creating card usage distribution chart...")

    all_cards = []
    for cards in deck_data['cards']:
        all_cards.extend(cards)

    card_freq = Counter(all_cards)
    top_cards = dict(card_freq.most_common(15))

    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(top_cards)), list(top_cards.values()), color='steelblue')
    plt.xticks(range(len(top_cards)), list(top_cards.keys()), rotation=45, ha='right')
    plt.xlabel('Card Name', fontsize=12, fontweight='bold')
    plt.ylabel('Usage Count', fontsize=12, fontweight='bold')
    plt.title('Top 15 Most Used Cards Across All Regions', fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{int(height)}',
                 ha='center', va='bottom', fontsize=9)

    viz1_path = f"{output_dir}/viz1_card_distribution.png"
    plt.savefig(viz1_path, dpi=300, bbox_inches='tight')
    print(f"   Saved to: {viz1_path}")
    plt.close()
    viz_paths['distribution'] = viz1_path

    # === VISUALIZATION 2: Correlation - Card Co-occurrence Heatmap ===
    print("\n2. Creating card co-occurrence correlation heatmap...")

    # Get top 12 cards for readability
    top_12_cards = list(dict(card_freq.most_common(12)).keys())

    # Create co-occurrence matrix
    cooccurrence = np.zeros((len(top_12_cards), len(top_12_cards)))

    for cards in deck_data['cards']:
        for i, card1 in enumerate(top_12_cards):
            for j, card2 in enumerate(top_12_cards):
                if card1 in cards and card2 in cards:
                    cooccurrence[i][j] += 1

    # Normalize by diagonal (individual card frequency)
    for i in range(len(top_12_cards)):
        if cooccurrence[i][i] > 0:
            cooccurrence[i] = cooccurrence[i] / cooccurrence[i][i]

    plt.figure(figsize=(10, 8))
    sns.heatmap(cooccurrence,
                xticklabels=top_12_cards,
                yticklabels=top_12_cards,
                annot=True,
                fmt='.2f',
                cmap='YlOrRd',
                cbar_kws={'label': 'Co-occurrence Rate'})
    plt.title('Card Co-occurrence Correlation Matrix\n(Shows which cards are frequently used together)',
              fontsize=14, fontweight='bold')
    plt.xlabel('Card Name', fontsize=12, fontweight='bold')
    plt.ylabel('Card Name', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    viz2_path = f"{output_dir}/viz2_card_correlation.png"
    plt.savefig(viz2_path, dpi=300, bbox_inches='tight')
    print(f"   Saved to: {viz2_path}")
    plt.close()
    viz_paths['correlation'] = viz2_path

    # === VISUALIZATION 3: Grouping - Regional Card Preferences ===
    print("\n3. Creating regional card preference comparison...")

    # Get top 8 cards
    top_8_cards = list(dict(card_freq.most_common(8)).keys())

    # Calculate usage percentage by region
    regional_usage = {}
    for location in deck_data['location_name'].unique():
        location_data = deck_data[deck_data['location_name'] == location]
        regional_usage[location] = {}

        for card in top_8_cards:
            count = sum(1 for cards in location_data['cards'] if card in cards)
            percentage = (count / len(location_data)) * 100
            regional_usage[location][card] = percentage

    # Create grouped bar chart
    locations = list(regional_usage.keys())
    x = np.arange(len(top_8_cards))
    width = 0.8 / len(locations)

    fig, ax = plt.subplots(figsize=(14, 7))

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']

    for i, location in enumerate(locations):
        values = [regional_usage[location][card] for card in top_8_cards]
        offset = width * i - (width * len(locations) / 2) + width / 2
        bars = ax.bar(x + offset, values, width, label=location, color=colors[i % len(colors)])

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            if height > 5:  # Only label if bar is tall enough
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{height:.0f}%',
                        ha='center', va='bottom', fontsize=8)

    ax.set_xlabel('Card Name', fontsize=12, fontweight='bold')
    ax.set_ylabel('Usage Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Regional Card Usage Comparison\n(Shows strategic differences between regions)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(top_8_cards, rotation=45, ha='right')
    ax.legend(title='Region', loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    viz3_path = f"{output_dir}/viz3_regional_comparison.png"
    plt.savefig(viz3_path, dpi=300, bbox_inches='tight')
    print(f"    Saved to: {viz3_path}")
    plt.close()
    viz_paths['grouping'] = viz3_path

    # === VISUALIZATION 4: Trend - Trophy Distribution by Region === Might not work because it using the top amount of 10k
    print("\n4. Creating trophy distribution by region (box plot)...")

    fig, ax = plt.subplots(figsize=(12, 7))

    # Prepare data for box plot
    trophy_data = []
    labels = []

    for location in deck_data['location_name'].unique():
        location_data = deck_data[deck_data['location_name'] == location]
        trophy_data.append(location_data['trophies'].values)
        labels.append(f"{location}\n(n={len(location_data)})")

    # Create box plot
    bp = ax.boxplot(trophy_data, patch_artist=True,
                    showmeans=True, meanline=True)

    # Color the boxes
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # Style the plot
    ax.set_xlabel('Region', fontsize=12, fontweight='bold')
    ax.set_ylabel('Trophies', fontsize=12, fontweight='bold')
    ax.set_title('Trophy Distribution by Region\n(Shows competitive level differences)',
                 fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Add mean values as text
    means = [np.mean(data) for data in trophy_data]
    for i, mean in enumerate(means):
        ax.text(i + 1, mean, f'μ={int(mean)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()

    viz4_path = f"{output_dir}/viz4_trophy_distribution.png"
    plt.savefig(viz4_path, dpi=300, bbox_inches='tight')
    print(f"    Saved to: {viz4_path}")
    plt.close()
    viz_paths['trend'] = viz4_path

    # === VISUALIZATION 5: Deck Diversity by Region ===
    print("\n5. Creating deck diversity comparison...")

    fig, ax = plt.subplots(figsize=(10, 6))

    diversity_data = []
    for location in deck_data['location_name'].unique():
        location_data = deck_data[deck_data['location_name'] == location]

        # Count unique decks (convert to tuples for hashing)
        unique_decks = set()
        for cards in location_data['cards']:
            unique_decks.add(tuple(sorted(cards)))

        diversity_rate = len(unique_decks) / len(location_data) * 100
        diversity_data.append({
            'Region': location,
            'Diversity Rate': diversity_rate,
            'Total Decks': len(location_data),
            'Unique Decks': len(unique_decks)
        })

    diversity_df = pd.DataFrame(diversity_data)

    bars = ax.bar(diversity_df['Region'], diversity_df['Diversity Rate'],
                  color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'][:len(diversity_df)])

    ax.set_xlabel('Region', fontsize=12, fontweight='bold')
    ax.set_ylabel('Deck Diversity Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Deck Diversity by Region\n(Higher = more unique deck compositions)',
                 fontsize=14, fontweight='bold')


    # Add value labels
    for bar, row in zip(bars, diversity_df.itertuples()):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{height:.1f}%\n({"Unique"}/{"Total Decks"})',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    viz5_path = f"{output_dir}/viz5_deck_diversity.png"
    plt.savefig(viz5_path, dpi=300, bbox_inches='tight')
    print(f"    Saved to: {viz5_path}")
    plt.close()
    viz_paths['diversity'] = viz5_path

    print("\n" + "=" * 60)
    print(" ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  1. {viz1_path} - Card usage distribution")
    print(f"  2. {viz2_path} - Card correlation heatmap")
    print(f"  3. {viz3_path} - Regional comparison")
    print(f"  4. {viz4_path} - Trophy distribution")
    print(f"  5. {viz5_path} - Deck diversity")
    print("\nThese visualizations show:")
    print("  • Distribution: Which cards are most popular overall")
    print("  • Correlation: Which cards are played together (synergies)")
    print("  • Grouping: How card preferences differ by region")
    print("  • Trend: Competitive levels across regions")
    print("  • Diversity: How varied the meta is in each region")

    return viz_paths


# === EXAMPLE USAGE ===
if __name__ == "__main__":

    deck_data = pd.read_csv("../clan_based_deckss.csv")


    import ast

    if isinstance(deck_data['cards'].iloc[0], str):
        deck_data['cards'] = deck_data['cards'].apply(ast.literal_eval)

    # Create visualizations
    viz_paths = create_clash_royale_visualizations(deck_data, output_dir="visualizations")

    print("\n Done! Check the visualizations folder for all charts.")

