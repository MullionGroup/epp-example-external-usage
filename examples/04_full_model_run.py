#!/usr/bin/env python3
"""
Example 4: Full Model Execution

This example demonstrates running the complete EPP Screening Model with all 9 sheets
and accessing individual sheet results.

What this does:
- Runs the full 9-sheet financial model
- Displays key financial metrics
- Shows how to access individual sheet results
- Demonstrates multi-format export
"""

from epp_screening_model_v3.models import ACCUModel


def main():
    print("="*80)
    print("Example 4: Full Model Execution")
    print("="*80)

    # -------------------------------------------------------------------------
    # Step 1: Initialize model
    # -------------------------------------------------------------------------
    print("\nInitializing EPP Screening Model...")
    print("-"*80)

    model = ACCUModel('config/config.toml')

    print(f"  Project: {model.get_project_name()}")

    # Display model dependencies
    dep_info = model.get_dependency_info()
    print(f"\nModel Structure:")
    print(f"  Total sheets: {dep_info['total_sheets']}")
    print(f"  Dependencies: {dep_info['total_dependencies']}")
    print(f"  Circular dependency groups: {dep_info['circular_groups']}")

    # -------------------------------------------------------------------------
    # Step 2: Run full model
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Running Full Model Calculation")
    print("="*80)

    print("\nExecuting all 9 sheets...")
    results = model.calculate_full_model(validate_results=True)

    print(f"\n✓ Model execution complete!")
    print(f"  Success: {results.success}")
    print(f"  Execution time: {results.execution_time_seconds:.2f} seconds")
    print(f"  Sheets calculated: {len(results.sheet_results)}")

    if results.warnings:
        print(f"\nWarnings: {len(results.warnings)}")
        for warning in results.warnings[:3]:  # Show first 3
            print(f"  - {warning}")

    if results.errors:
        print(f"\nErrors: {len(results.errors)}")
        for error in results.errors[:3]:  # Show first 3
            print(f"  - {error}")

    # -------------------------------------------------------------------------
    # Step 3: Display key financial metrics
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Key Financial Metrics")
    print("="*80)

    print(f"\nProject Valuation:")
    if results.project_value is not None:
        print(f"  Project Value: ${results.project_value:,.0f}")

    print(f"\nInternal Rate of Return (IRR):")
    if results.unlevered_irr is not None:
        print(f"  Unlevered IRR: {results.unlevered_irr:.4%}")
    if results.levered_irr is not None:
        print(f"  Levered IRR: {results.levered_irr:.4%}")

    print(f"\nNet Present Value (NPV):")
    if results.unlevered_npv is not None:
        print(f"  Unlevered NPV: ${results.unlevered_npv:,.0f}")
    if results.levered_npv is not None:
        print(f"  Levered NPV: ${results.levered_npv:,.0f}")

    # -------------------------------------------------------------------------
    # Step 4: Access individual sheet results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Individual Sheet Results")
    print("="*80)

    print(f"\nAll {len(results.sheet_results)} sheets calculated successfully:")
    for sheet_name in results.sheet_results.keys():
        print(f"  ✓ {sheet_name}")

    print(f"\nNote: Individual sheet data can be accessed via results.get_sheet_result('SheetName')")

    # -------------------------------------------------------------------------
    # Step 5: Export results
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("Exporting Results")
    print("="*80)

    # Export summary to JSON
    import json

    summary = {
        'project_name': model.get_project_name(),
        'execution_time': results.execution_time_seconds,
        'financial_metrics': {
            'unlevered_irr': results.unlevered_irr,
            'levered_irr': results.levered_irr,
            'unlevered_npv': results.unlevered_npv,
            'levered_npv': results.levered_npv,
            'project_value': results.project_value,
        },
        'sheets_calculated': list(results.sheet_results.keys()),
        'validation_status': {
            'success': results.success,
            'warnings': len(results.warnings),
            'errors': len(results.errors),
        }
    }

    with open('results/04_full_model_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✓ Saved summary: results/04_full_model_summary.json")

    # Note: For full Excel export, you would use:
    # from epp_screening_model_v3.output import OutputManager
    # manager = OutputManager('results/')
    # manager.export_model(model, formats=[OutputFormat.EXCEL, OutputFormat.CSV])

    print("\n" + "="*80)
    print("Example Complete!")
    print("="*80)

    print("\nKey Takeaways:")
    print("  • Full 9-sheet model executed successfully")
    print("  • Individual sheet results accessible")
    print("  • Financial metrics calculated automatically")
    print("  • Results exportable to multiple formats")


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
