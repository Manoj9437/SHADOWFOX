#!/usr/bin/env python3
"""
Test script to check for errors in the cricket fielding analysis app
"""

import pandas as pd
import sys
import traceback
from utils.data_processor import DataProcessor
from utils.visualization import Visualizer
from utils.metrics_calculator import MetricsCalculator

def test_complete_workflow():
    """Test the complete workflow to identify any errors"""
    print("Testing Cricket Fielding Analysis App...")
    
    try:
        # Load sample data
        print("1. Loading sample data...")
        data = pd.read_csv('sample_cricket_data.csv')
        print(f"   ✓ Loaded {len(data)} records")
        
        # Test data validation
        print("2. Testing data validation...")
        dp = DataProcessor()
        validation = dp.validate_data(data)
        if validation['is_valid']:
            print("   ✓ Data validation passed")
        else:
            print("   ✗ Data validation failed:")
            for error in validation['errors']:
                print(f"     - {error}")
            return False
        
        # Test data processing
        print("3. Testing data processing...")
        processed_data = dp.process_data(data)
        print(f"   ✓ Data processed successfully: {len(processed_data)} rows")
        
        # Test metrics calculation
        print("4. Testing metrics calculation...")
        mc = MetricsCalculator()
        
        # Test individual player metrics
        player_name = processed_data['Player_Name'].iloc[0]
        player_data = processed_data[processed_data['Player_Name'] == player_name]
        metrics = mc.calculate_player_metrics(player_data)
        print(f"   ✓ Player metrics calculated for {player_name}")
        
        # Test comparison metrics
        comparison_data = processed_data.head(6)  # First 6 records
        comp_metrics = mc.calculate_comparison_metrics(comparison_data)
        print(f"   ✓ Comparison metrics calculated: {len(comp_metrics)} players")
        
        # Test team metrics
        match_data = processed_data[processed_data['Match_No'] == 1]
        team_metrics = mc.calculate_team_metrics(match_data)
        print(f"   ✓ Team metrics calculated for match 1")
        
        # Test visualizations
        print("5. Testing visualizations...")
        viz = Visualizer()
        
        # Test player overview chart
        fig1 = viz.create_player_overview(player_data, player_name)
        print("   ✓ Player overview chart created")
        
        # Test radar comparison
        players_for_comparison = processed_data['Player_Name'].unique()[:3]
        comparison_subset = processed_data[processed_data['Player_Name'].isin(players_for_comparison)]
        fig2 = viz.create_radar_comparison(comparison_subset, players_for_comparison)
        print("   ✓ Radar comparison chart created")
        
        # Test team visualizations
        fig3 = viz.create_team_contribution(match_data)
        print("   ✓ Team contribution chart created")
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1)