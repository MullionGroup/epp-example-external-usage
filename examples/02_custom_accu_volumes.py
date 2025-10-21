#!/usr/bin/env python3
"""
Example 2: Goal Seek with Custom ACCU Volumes

This example demonstrates how to run goal seek with custom ACCU (Australian Carbon
Credit Unit) volumes passed programmatically as Python lists.

What this does:
- Defines custom ACCU production volumes (27 annual values)
- Runs goal seek with these volumes
- No TOML scenario files required!
"""

from epp_screening_model_v3.models.goal_seek import get_preset
from epp_screening_model_v3.notebooks.epp_jupyter_helpers import goal_seek_with_accu_volumes


def main():
    print("="*80)
    print("Example 2: Goal Seek with Custom ACCU Volumes")
    print("="*80)

    # -------------------------------------------------------------------------
    # Step 1: Define custom ACCU volumes
    # -------------------------------------------------------------------------
    print("\nDefining Custom ACCU Volumes...")
    print("-"*80)

    # Custom ACCU production volumes for 27 years (Year 0 through Year 26)
    # These represent annual carbon credit generation
    custom_accu_volumes = [
        0.0,       # Year 0 - No production
        6750.0,    # Year 1 - Initial production
        24605.5,   # Year 2 - Ramping up
        36785.2,   # Year 3
        42933.1,   # Year 4
        44904.4,   # Year 5 - Peak production
        44481.5,   # Year 6 - Gradual decline begins
        42799.0,   # Year 7
        40511.9,   # Year 8
        37986.9,   # Year 9
        35426.2,   # Year 10
        32939.2,   # Year 11
        30581.6,   # Year 12
        28379.3,   # Year 13
        26340.3,   # Year 14
        24463.0,   # Year 15
        22740.6,   # Year 16
        21163.1,   # Year 17
        19719.8,   # Year 18
        18399.5,   # Year 19
        17191.5,   # Year 20
        16085.5,   # Year 21
        15072.1,   # Year 22
        14142.5,   # Year 23
        13288.8,   # Year 24
        0.0,       # Year 25 - End of crediting period
        0.0        # Year 26
    ]

    print(f"  ACCU Volumes: {len(custom_accu_volumes)} years")
    print(f"  Total ACCUs: {sum(custom_accu_volumes):,.0f}")
    print(f"  Peak production: {max(custom_accu_volumes):,.0f} (Year {custom_accu_volumes.index(max(custom_accu_volumes))})")

    # -------------------------------------------------------------------------
    # Step 2: Run goal seek with custom volumes
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Running Goal Seek with Custom ACCU Volumes")
    print("="*80)

    # Get preset
    preset = get_preset('debt-ratio-60')

    print(f"\nUsing Preset: {preset.name}")
    print(f"  Target: {preset.target_value:.0%} debt ratio")

    # Run goal seek using helper function
    # This automatically handles scenario creation - no TOML files needed!
    print("\nRunning solver with custom ACCU volumes...")
    result = goal_seek_with_accu_volumes(
        preset_name='debt-ratio-60',
        accu_volumes=custom_accu_volumes,
        config_path='config/config.toml',
        verbose=False  # Suppress progress messages
    )

    # -------------------------------------------------------------------------
    # Step 4: Display results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Results")
    print("="*80)

    print(f"\n✓ Converged: {result.converged} (in {result.iterations} iterations)")

    print(f"\nOptimal Solution:")
    print(f"  LVR: {result.solution:.4f} ({result.solution*100:.2f}%)")

    print(f"\nTarget Achievement:")
    print(f"  Target: {result.target_value:.4f}")
    print(f"  Achieved: {result.achieved_value:.4f}")

    if result.unlevered_return and result.levered_return:
        print(f"\nFinancial Returns:")
        print(f"  Unlevered IRR: {result.unlevered_return:.4%}")
        print(f"  Levered IRR: {result.levered_return:.4%}")

    print(f"\nScenario Information:")
    print(f"  Scenario: {result.scenario_name}")
    if result.scenario_overrides:
        print(f"  Overrides applied: {len(result.scenario_overrides)}")

    # -------------------------------------------------------------------------
    # Step 5: Save results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Saving Results")
    print("="*80)

    result.to_json('results/02_custom_accu_result.json')
    print(f"✓ Saved: results/02_custom_accu_result.json")

    result.save_optimized_config('results/02_optimized_config.toml')
    print(f"✓ Saved: results/02_optimized_config.toml")

    print("\n" + "="*80)
    print("Example Complete!")
    print("="*80)

    print("\nKey Takeaways:")
    print("  • ACCU volumes passed as Python list (no TOML file!)")
    print("  • Scenario created programmatically")
    print("  • Results include scenario information")


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
