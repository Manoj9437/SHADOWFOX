import pandas as pd
import numpy as np

class MetricsCalculator:
    def __init__(self):
        pass
    
    def calculate_player_metrics(self, player_data):
        """Calculate comprehensive metrics for a single player"""
        # Basic success rates
        total_catch_attempts = player_data['Catches_Taken'].sum() + player_data['Catches_Dropped'].sum()
        catch_success_rate = player_data['Catches_Taken'].sum() / total_catch_attempts if total_catch_attempts > 0 else 0
        
        total_runout_attempts = player_data['Run_Outs_Executed'].sum() + player_data['Run_Outs_Missed'].sum()
        runout_success_rate = player_data['Run_Outs_Executed'].sum() / total_runout_attempts if total_runout_attempts > 0 else 0
        
        # Fielding efficiency
        total_actions = player_data['Total_Fielding_Actions'].sum()
        positive_actions = (
            player_data['Catches_Taken'].sum() + 
            player_data['Run_Outs_Executed'].sum() + 
            player_data['Boundaries_Saved'].sum() + 
            player_data['Direct_Hits'].sum()
        )
        fielding_efficiency = positive_actions / total_actions if total_actions > 0 else 0
        
        # Error rate
        total_errors = player_data['Catches_Dropped'].sum() + player_data['Fumbles'].sum()
        error_rate = total_errors / total_actions if total_actions > 0 else 0
        
        # Impact score
        impact_score = player_data['Impact_Score'].sum()
        
        # Consistency (coefficient of variation of efficiency across matches)
        if len(player_data) > 1:
            efficiency_cv = player_data['Fielding_Efficiency'].std() / player_data['Fielding_Efficiency'].mean() if player_data['Fielding_Efficiency'].mean() > 0 else 0
        else:
            efficiency_cv = 0
        
        return {
            'catch_success_rate': catch_success_rate,
            'runout_success_rate': runout_success_rate,
            'fielding_efficiency': fielding_efficiency,
            'error_rate': error_rate,
            'impact_score': impact_score,
            'consistency_score': 1 - efficiency_cv,  # Higher is better
            'total_actions': total_actions,
            'matches_played': len(player_data)
        }
    
    def calculate_comparison_metrics(self, comparison_data):
        """Calculate metrics for player comparison"""
        players = comparison_data['Player_Name'].unique()
        comparison_stats = []
        
        for player in players:
            player_data = comparison_data[comparison_data['Player_Name'] == player]
            metrics = self.calculate_player_metrics(player_data)
            
            stats = {
                'Player': player,
                'Matches': metrics['matches_played'],
                'Total Actions': int(metrics['total_actions']),
                'Catch Success %': f"{metrics['catch_success_rate']:.1%}",
                'Run-out Success %': f"{metrics['runout_success_rate']:.1%}",
                'Fielding Efficiency %': f"{metrics['fielding_efficiency']:.1%}",
                'Error Rate %': f"{metrics['error_rate']:.1%}",
                'Impact Score': f"{metrics['impact_score']:.1f}",
                'Consistency': f"{metrics['consistency_score']:.3f}"
            }
            comparison_stats.append(stats)
        
        return pd.DataFrame(comparison_stats)
    
    def calculate_team_metrics(self, match_data):
        """Calculate team-level metrics for a specific match"""
        # Team success rates
        total_catch_attempts = match_data['Catches_Taken'].sum() + match_data['Catches_Dropped'].sum()
        team_catch_success = match_data['Catches_Taken'].sum() / total_catch_attempts if total_catch_attempts > 0 else 0
        
        total_runout_attempts = match_data['Run_Outs_Executed'].sum() + match_data['Run_Outs_Missed'].sum()
        team_runout_success = match_data['Run_Outs_Executed'].sum() / total_runout_attempts if total_runout_attempts > 0 else 0
        
        # Team fielding efficiency
        total_actions = match_data['Total_Fielding_Actions'].sum()
        positive_actions = (
            match_data['Catches_Taken'].sum() + 
            match_data['Run_Outs_Executed'].sum() + 
            match_data['Boundaries_Saved'].sum() + 
            match_data['Direct_Hits'].sum()
        )
        team_efficiency = positive_actions / total_actions if total_actions > 0 else 0
        
        # Team error rate
        total_errors = match_data['Catches_Dropped'].sum() + match_data['Fumbles'].sum()
        team_error_rate = total_errors / total_actions if total_actions > 0 else 0
        
        # Team impact score
        team_impact = match_data['Impact_Score'].sum()
        
        return {
            'team_catch_success': team_catch_success,
            'team_runout_success': team_runout_success,
            'team_efficiency': team_efficiency,
            'team_error_rate': team_error_rate,
            'team_impact': team_impact,
            'total_actions': total_actions,
            'active_players': len(match_data)
        }
    
    def calculate_player_rankings(self, match_data):
        """Calculate player rankings for a specific match"""
        rankings = []
        
        for _, player_row in match_data.iterrows():
            player_metrics = self.calculate_player_metrics(pd.DataFrame([player_row]))
            
            ranking = {
                'Player': player_row['Player_Name'],
                'Total Actions': int(player_row['Total_Fielding_Actions']),
                'Efficiency %': f"{player_metrics['fielding_efficiency']:.1%}",
                'Impact Score': f"{player_metrics['impact_score']:.1f}",
                'Catches': f"{player_row['Catches_Taken']}/{player_row['Catches_Taken'] + player_row['Catches_Dropped']}",
                'Run-outs': f"{player_row['Run_Outs_Executed']}/{player_row['Run_Outs_Executed'] + player_row['Run_Outs_Missed']}",
                'Boundaries Saved': int(player_row['Boundaries_Saved']),
                'Direct Hits': int(player_row['Direct_Hits']),
                'Errors': int(player_row['Catches_Dropped'] + player_row['Fumbles'])
            }
            rankings.append(ranking)
        
        rankings_df = pd.DataFrame(rankings)
        
        # Sort by impact score (descending)
        impact_scores = [float(score) for score in rankings_df['Impact Score']]
        rankings_df['Impact_Score_Numeric'] = impact_scores
        rankings_df = rankings_df.sort_values('Impact_Score_Numeric', ascending=False).drop('Impact_Score_Numeric', axis=1)
        
        # Add rank column
        rankings_df['Rank'] = range(1, len(rankings_df) + 1)
        rankings_df = rankings_df[['Rank'] + [col for col in rankings_df.columns if col != 'Rank']]
        
        return rankings_df
    
    def get_detailed_stats(self, player_data):
        """Get detailed statistics table for a player"""
        detailed_stats = []
        
        for _, match_row in player_data.iterrows():
            stats = {
                'Match': int(match_row['Match_No']),
                'Total Actions': int(match_row['Total_Fielding_Actions']),
                'Catches Taken': int(match_row['Catches_Taken']),
                'Catches Dropped': int(match_row['Catches_Dropped']),
                'Run-outs Made': int(match_row['Run_Outs_Executed']),
                'Run-outs Missed': int(match_row['Run_Outs_Missed']),
                'Boundaries Saved': int(match_row['Boundaries_Saved']),
                'Direct Hits': int(match_row['Direct_Hits']),
                'Fumbles': int(match_row['Fumbles']),
                'Catch Success %': f"{match_row['Catch_Success_Rate']:.1%}",
                'Run-out Success %': f"{match_row['Runout_Success_Rate']:.1%}",
                'Efficiency %': f"{match_row['Fielding_Efficiency']:.1%}",
                'Error Rate %': f"{match_row['Error_Rate']:.1%}",
                'Impact Score': f"{match_row['Impact_Score']:.1f}"
            }
            detailed_stats.append(stats)
        
        return pd.DataFrame(detailed_stats)
    
    def generate_summary_report(self, data):
        """Generate a comprehensive summary report"""
        report_lines = []
        report_lines.append("CRICKET FIELDING ANALYSIS SUMMARY REPORT")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # Overall statistics
        total_matches = data['Match_No'].nunique()
        total_players = data['Player_Name'].nunique()
        total_actions = data['Total_Fielding_Actions'].sum()
        
        report_lines.append(f"Dataset Overview:")
        report_lines.append(f"- Total Matches Analyzed: {total_matches}")
        report_lines.append(f"- Total Players: {total_players}")
        report_lines.append(f"- Total Fielding Actions: {total_actions}")
        report_lines.append("")
        
        # Team performance summary
        team_catches = data['Catches_Taken'].sum()
        team_drops = data['Catches_Dropped'].sum()
        team_runouts = data['Run_Outs_Executed'].sum()
        team_runout_misses = data['Run_Outs_Missed'].sum()
        
        team_catch_rate = team_catches / (team_catches + team_drops) if (team_catches + team_drops) > 0 else 0
        team_runout_rate = team_runouts / (team_runouts + team_runout_misses) if (team_runouts + team_runout_misses) > 0 else 0
        
        report_lines.append(f"Overall Team Performance:")
        report_lines.append(f"- Team Catch Success Rate: {team_catch_rate:.1%}")
        report_lines.append(f"- Team Run-out Success Rate: {team_runout_rate:.1%}")
        report_lines.append(f"- Total Boundaries Saved: {data['Boundaries_Saved'].sum()}")
        report_lines.append(f"- Total Direct Hits: {data['Direct_Hits'].sum()}")
        report_lines.append("")
        
        # Top performers
        player_summary = data.groupby('Player_Name').agg({
            'Impact_Score': 'sum',
            'Fielding_Efficiency': 'mean',
            'Total_Fielding_Actions': 'sum'
        }).round(3)
        
        top_impact = player_summary.nlargest(3, 'Impact_Score')
        top_efficiency = player_summary.nlargest(3, 'Fielding_Efficiency')
        
        report_lines.append("Top Performers by Impact Score:")
        for i, (player, stats) in enumerate(top_impact.iterrows(), 1):
            report_lines.append(f"{i}. {player}: {stats['Impact_Score']:.1f}")
        report_lines.append("")
        
        report_lines.append("Top Performers by Efficiency:")
        for i, (player, stats) in enumerate(top_efficiency.iterrows(), 1):
            report_lines.append(f"{i}. {player}: {stats['Fielding_Efficiency']:.1%}")
        report_lines.append("")
        
        # Match-by-match summary
        report_lines.append("Match-by-Match Summary:")
        for match in sorted(data['Match_No'].unique()):
            match_data = data[data['Match_No'] == match]
            match_metrics = self.calculate_team_metrics(match_data)
            
            report_lines.append(f"Match {match}:")
            report_lines.append(f"  - Total Actions: {int(match_metrics['total_actions'])}")
            report_lines.append(f"  - Team Efficiency: {match_metrics['team_efficiency']:.1%}")
            report_lines.append(f"  - Error Rate: {match_metrics['team_error_rate']:.1%}")
            report_lines.append("")
        
        report_lines.append("Report generated by Cricket Fielding Analysis Tool")
        
        return "\n".join(report_lines)
