#!/usr/bin/env python3
"""
Example 3: Batch Sensitivity Analysis

This example demonstrates how to perform batch sensitivity analysis across
multiple ACCU production scenarios to compare different carbon credit pathways.

What this does:
- Defines multiple ACCU production scenarios
- Runs goal seek for each scenario
- Compares results in a DataFrame
- Exports results to CSV and generates visualization
"""

import pandas as pd
from epp_screening_model_v3.notebooks.epp_jupyter_helpers import batch_goal_seek_analysis
from epp_screening_model_v3.models.goal_seek import get_preset


# Define three ACCU production scenarios
ACCU_SCENARIOS = {
    'Conservative': [
        0.0, 4500.0, 16403.7, 24523.4, 28622.1, 29936.3,
        29654.3, 28532.7, 27007.9, 25324.6, 23617.5, 21959.4,
        20387.8, 18919.5, 17560.2, 16308.7, 15160.4, 14108.7,
        13146.5, 12266.4, 11461.0, 10723.7, 10048.1, 9428.3,
        8859.2, 0.0, 0.0
    ],
    'Baseline': [
        0.0, 6000.0, 21871.6, 32697.9, 38162.8, 39915.0,
        39539.1, 38043.6, 36010.6, 33766.1, 31490.0, 29279.3,
        27183.7, 25226.0, 23413.6, 21744.9, 20213.9, 18811.6,
        17528.7, 16355.2, 15281.4, 14298.3, 13397.4, 12571.1,
        11812.3, 0.0, 0.0
    ],
    'Aggressive': [
        0.0, 6750.0, 24605.5, 36785.2, 42933.1, 44904.4,
        44481.5, 42799.0, 40511.9, 37986.9, 35426.2, 32939.2,
        30581.6, 28379.3, 26340.3, 24463.0, 22740.6, 21163.1,
        19719.8, 18399.5, 17191.5, 16085.5, 15072.1, 14142.5,
        13288.8, 0.0, 0.0
    ]
}


def main():
    print("="*80)
    print("Example 3: Batch Sensitivity Analysis")
    print("="*80)

    # -------------------------------------------------------------------------
    # Step 1: Display scenarios
    # -------------------------------------------------------------------------
    print("\nACCU Production Scenarios:")
    print("-"*80)

    for name, volumes in ACCU_SCENARIOS.items():
        total = sum(volumes)
        peak = max(volumes)
        peak_year = volumes.index(peak)
        print(f"  {name:15s}: Total={total:>10,.0f}, Peak={peak:>10,.0f} (Year {peak_year})")

    # -------------------------------------------------------------------------
    # Step 2: Run batch analysis
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Running Batch Analysis")
    print("="*80)

    preset = get_preset('debt-ratio-60')
    print(f"\nUsing preset: {preset.name}")
    print(f"Target: {preset.target_value:.0%} debt ratio\n")

    # Run batch analysis using helper function
    # This automatically handles all scenario creation and goal seek execution
    df = batch_goal_seek_analysis(
        preset_name='debt-ratio-60',
        accu_scenarios=ACCU_SCENARIOS,
        config_path='config/config.toml'
    )

    # -------------------------------------------------------------------------
    # Step 3: Display results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Results Summary")
    print("="*80)

    # Display all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print("\n" + df.to_string(index=False))

    # -------------------------------------------------------------------------
    # Step 4: Analysis insights
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Key Insights")
    print("="*80)

    if 'Levered Return' in df.columns:
        print(f"\nLevered Return Range:")
        print(f"  Min: {df['Levered Return'].min():.2%} ({df.loc[df['Levered Return'].idxmin(), 'Scenario']})")
        print(f"  Max: {df['Levered Return'].max():.2%} ({df.loc[df['Levered Return'].idxmax(), 'Scenario']})")
        print(f"  Spread: {(df['Levered Return'].max() - df['Levered Return'].min()):.2%}")

        print(f"\nOptimal Solution (LVR) Range:")
        print(f"  Min: {df['Solution'].min():.2%} ({df.loc[df['Solution'].idxmin(), 'Scenario']})")
        print(f"  Max: {df['Solution'].max():.2%} ({df.loc[df['Solution'].idxmax(), 'Scenario']})")

    # -------------------------------------------------------------------------
    # Step 5: Export results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Exporting Results")
    print("="*80)

    df.to_csv('results/03_batch_analysis.csv', index=False)
    print(f"✓ Saved CSV: results/03_batch_analysis.csv")

    df.to_excel('results/03_batch_analysis.xlsx', index=False)
    print(f"✓ Saved Excel: results/03_batch_analysis.xlsx")

    # Optional: Create visualization if matplotlib available
    try:
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Plot 1: Levered Return by scenario
        ax1.barh(df['Scenario'], df['Levered Return'] * 100, color='steelblue', alpha=0.7)
        ax1.set_xlabel('Levered Return (%)')
        ax1.set_title('Levered Return by ACCU Scenario')
        ax1.grid(axis='x', alpha=0.3)

        # Plot 2: Total ACCUs vs Levered Return
        ax2.scatter(df['Total ACCUs'], df['Levered Return'] * 100, s=200, c='coral', alpha=0.7)
        for idx, row in df.iterrows():
            ax2.annotate(row['Scenario'], (row['Total ACCUs'], row['Levered Return'] * 100),
                        xytext=(5, 5), textcoords='offset points', fontsize=9)
        ax2.set_xlabel('Total ACCUs')
        ax2.set_ylabel('Levered Return (%)')
        ax2.set_title('Total ACCUs vs Levered Return')
        ax2.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig('results/03_batch_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved chart: results/03_batch_analysis.png")
        plt.close()

    except ImportError:
        print("  (matplotlib not available - skipping visualization)")

    print("\n" + "="*80)
    print("Example Complete!")
    print("="*80)


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have created config/config.toml")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
