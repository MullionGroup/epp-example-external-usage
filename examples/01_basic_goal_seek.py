#!/usr/bin/env python3
"""
Example 1: Basic Goal Seek Using Presets

This example demonstrates the simplest way to use the EPP Screening Model
for goal seek optimization using predefined presets.

What this does:
- Uses a preset to find the optimal LVR (Loan-to-Value Ratio)
- Targets a specific debt-to-capital ratio (60%)
- Returns financial metrics (levered and unlevered returns)
"""

from epp_screening_model_v3.models.goal_seek import GoalSeekSolver, get_preset, list_presets_by_category


def main():
    print("="*80)
    print("Example 1: Basic Goal Seek Using Presets")
    print("="*80)

    # -------------------------------------------------------------------------
    # Step 1: List available presets
    # -------------------------------------------------------------------------
    print("\nAvailable Goal Seek Presets:")
    print("-"*80)

    presets = list_presets_by_category()
    for category, preset_names in presets.items():
        print(f"\n{category}:")
        for preset_name in preset_names:
            preset = get_preset(preset_name)
            print(f"  • {preset.name:30s} - {preset.description}")

    # -------------------------------------------------------------------------
    # Step 2: Run goal seek with a preset
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Running Goal Seek: debt-ratio-60")
    print("="*80)

    # Initialize solver with your config file
    # Note: You'll need to create config/config.toml based on the EPP template
    solver = GoalSeekSolver('config/config.toml')

    # Get the preset configuration
    preset = get_preset('debt-ratio-60')

    print(f"\nPreset Details:")
    print(f"  Name: {preset.name}")
    print(f"  Description: {preset.description}")
    print(f"  Input Cell: {preset.input_cell} (LVR to Property Value)")
    print(f"  Target Cell: {preset.target_cell} (Debt to CapEx Ratio)")
    print(f"  Target Value: {preset.target_value:.2%}")
    print(f"  Bounds: [{preset.min_value}, {preset.max_value}]")

    # Run the goal seek
    print("\nRunning solver...")
    result = solver.solve(
        input_cell=preset.input_cell,
        target_cell=preset.target_cell,
        target_value=preset.target_value,
        bounds=(preset.min_value, preset.max_value),
        method=preset.suggested_method
    )

    # -------------------------------------------------------------------------
    # Step 3: Display results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Goal Seek Results")
    print("="*80)

    print(f"\n✓ Converged: {result.converged}")
    print(f"  Iterations: {result.iterations}")
    print(f"  Function calls: {result.function_calls}")

    print(f"\nOptimal Solution:")
    print(f"  LVR (Loan-to-Value): {result.solution:.4f} ({result.solution*100:.2f}%)")

    print(f"\nTarget Achievement:")
    print(f"  Target Debt Ratio: {result.target_value:.4f}")
    print(f"  Achieved: {result.achieved_value:.4f}")
    print(f"  Error: {abs(result.achieved_value - result.target_value):.2e}")

    if result.unlevered_return is not None and result.levered_return is not None:
        print(f"\nFinancial Metrics:")
        print(f"  Unlevered Return (IRR): {result.unlevered_return:.4%}")
        print(f"  Levered Return (IRR): {result.levered_return:.4%}")

    # -------------------------------------------------------------------------
    # Step 4: Save results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Saving Results")
    print("="*80)

    # Save to JSON
    result.to_json('results/01_basic_goal_seek_result.json')
    print(f"✓ Saved JSON: results/01_basic_goal_seek_result.json")

    # Save optimized config
    result.save_optimized_config('results/01_optimized_config.toml')
    print(f"✓ Saved config: results/01_optimized_config.toml")

    print("\n" + "="*80)
    print("Example Complete!")
    print("="*80)


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Created config/config.toml (see EPP package for template)")
        print("  2. Installed the EPP package (see README.md)")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
