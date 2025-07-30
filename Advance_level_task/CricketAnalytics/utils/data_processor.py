import pandas as pd
import numpy as np
import streamlit as st

class DataProcessor:
    def __init__(self):
        self.required_columns = [
            'Match_No', 'Player_Name', 'Catches_Taken', 'Catches_Dropped',
            'Run_Outs_Executed', 'Run_Outs_Missed', 'Boundaries_Saved',
            'Direct_Hits', 'Fumbles', 'Total_Fielding_Actions'
        ]
    
    def validate_data(self, data):
        """Validate the uploaded data format and content"""
        errors = []
        
        # Check if data is empty
        if data.empty:
            errors.append("The uploaded file is empty")
            return {'is_valid': False, 'errors': errors}
        
        # Check required columns
        missing_columns = [col for col in self.required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check data types for numeric columns
        numeric_columns = [col for col in self.required_columns if col not in ['Player_Name']]
        for col in numeric_columns:
            if col in data.columns:
                if not pd.api.types.is_numeric_dtype(data[col]):
                    try:
                        pd.to_numeric(data[col], errors='raise')
                    except:
                        errors.append(f"Column '{col}' contains non-numeric values")
        
        # Check for negative values in fielding statistics
        fielding_stats_columns = [
            'Catches_Taken', 'Catches_Dropped', 'Run_Outs_Executed', 
            'Run_Outs_Missed', 'Boundaries_Saved', 'Direct_Hits', 
            'Fumbles', 'Total_Fielding_Actions'
        ]
        
        for col in fielding_stats_columns:
            if col in data.columns:
                if (data[col] < 0).any():
                    errors.append(f"Column '{col}' contains negative values")
        
        # Check if player names are valid
        if 'Player_Name' in data.columns:
            if data['Player_Name'].isnull().any():
                errors.append("Player_Name column contains missing values")
        
        # Check logical consistency
        if all(col in data.columns for col in ['Catches_Taken', 'Catches_Dropped', 'Total_Fielding_Actions']):
            inconsistent_rows = data[
                (data['Catches_Taken'] + data['Catches_Dropped']) > data['Total_Fielding_Actions']
            ]
            if not inconsistent_rows.empty:
                errors.append("Some rows have catch actions exceeding total fielding actions")
        
        return {'is_valid': len(errors) == 0, 'errors': errors}
    
    def process_data(self, data):
        """Process and clean the validated data"""
        processed_data = data.copy()
        
        # Convert numeric columns to appropriate data types
        numeric_columns = [col for col in self.required_columns if col not in ['Player_Name']]
        for col in numeric_columns:
            if col in processed_data.columns:
                processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce')
                processed_data[col] = processed_data[col].fillna(0)
        
        # Clean player names
        if 'Player_Name' in processed_data.columns:
            processed_data['Player_Name'] = processed_data['Player_Name'].str.strip()
        
        # Calculate derived metrics
        processed_data = self._calculate_derived_metrics(processed_data)
        
        # Sort by match number and player name
        processed_data = processed_data.sort_values(['Match_No', 'Player_Name']).reset_index(drop=True)
        
        return processed_data
    
    def _calculate_derived_metrics(self, data):
        """Calculate additional fielding metrics"""
        # Catch success rate
        data['Catch_Success_Rate'] = np.where(
            (data['Catches_Taken'] + data['Catches_Dropped']) > 0,
            data['Catches_Taken'] / (data['Catches_Taken'] + data['Catches_Dropped']),
            0
        )
        
        # Run-out success rate
        data['Runout_Success_Rate'] = np.where(
            (data['Run_Outs_Executed'] + data['Run_Outs_Missed']) > 0,
            data['Run_Outs_Executed'] / (data['Run_Outs_Executed'] + data['Run_Outs_Missed']),
            0
        )
        
        # Fielding efficiency (positive actions / total actions)
        positive_actions = (
            data['Catches_Taken'] + data['Run_Outs_Executed'] + 
            data['Boundaries_Saved'] + data['Direct_Hits']
        )
        data['Fielding_Efficiency'] = np.where(
            data['Total_Fielding_Actions'] > 0,
            positive_actions / data['Total_Fielding_Actions'],
            0
        )
        
        # Error rate (fumbles + dropped catches) / total actions
        errors = data['Fumbles'] + data['Catches_Dropped']
        data['Error_Rate'] = np.where(
            data['Total_Fielding_Actions'] > 0,
            errors / data['Total_Fielding_Actions'],
            0
        )
        
        # Impact score (weighted combination of key metrics)
        data['Impact_Score'] = (
            data['Catches_Taken'] * 3 +
            data['Run_Outs_Executed'] * 4 +
            data['Direct_Hits'] * 2 +
            data['Boundaries_Saved'] * 2 -
            data['Catches_Dropped'] * 2 -
            data['Fumbles'] * 1
        )
        
        return data
    
    def filter_data(self, data, filters):
        """Apply filters to the data"""
        filtered_data = data.copy()
        
        if 'matches' in filters and filters['matches']:
            filtered_data = filtered_data[filtered_data['Match_No'].isin(filters['matches'])]
        
        if 'players' in filters and filters['players']:
            filtered_data = filtered_data[filtered_data['Player_Name'].isin(filters['players'])]
        
        if 'min_actions' in filters and filters['min_actions'] is not None:
            filtered_data = filtered_data[filtered_data['Total_Fielding_Actions'] >= filters['min_actions']]
        
        return filtered_data
    
    def aggregate_player_data(self, data):
        """Aggregate data by player across all matches"""
        numeric_columns = [
            'Catches_Taken', 'Catches_Dropped', 'Run_Outs_Executed',
            'Run_Outs_Missed', 'Boundaries_Saved', 'Direct_Hits',
            'Fumbles', 'Total_Fielding_Actions'
        ]
        
        aggregated = data.groupby('Player_Name')[numeric_columns].sum().reset_index()
        
        # Recalculate derived metrics for aggregated data
        aggregated = self._calculate_derived_metrics(aggregated)
        
        return aggregated
