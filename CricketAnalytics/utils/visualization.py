import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self):
        self.colors = px.colors.qualitative.Set3
        
    def create_player_overview(self, player_data, player_name):
        """Create overview visualization for a single player"""
        # Aggregate data across matches
        total_stats = {
            'Catches Taken': player_data['Catches_Taken'].sum(),
            'Catches Dropped': player_data['Catches_Dropped'].sum(),
            'Run-outs Executed': player_data['Run_Outs_Executed'].sum(),
            'Run-outs Missed': player_data['Run_Outs_Missed'].sum(),
            'Boundaries Saved': player_data['Boundaries_Saved'].sum(),
            'Direct Hits': player_data['Direct_Hits'].sum(),
            'Fumbles': player_data['Fumbles'].sum()
        }
        
        fig = go.Figure()
        
        # Positive actions
        positive_actions = ['Catches Taken', 'Run-outs Executed', 'Boundaries Saved', 'Direct Hits']
        negative_actions = ['Catches Dropped', 'Run-outs Missed', 'Fumbles']
        
        fig.add_trace(go.Bar(
            x=[action for action in positive_actions],
            y=[total_stats[action] for action in positive_actions],
            name='Positive Actions',
            marker_color='green',
            opacity=0.7
        ))
        
        fig.add_trace(go.Bar(
            x=[action for action in negative_actions],
            y=[total_stats[action] for action in negative_actions],
            name='Errors/Misses',
            marker_color='red',
            opacity=0.7
        ))
        
        fig.update_layout(
            title=f'Fielding Performance Overview - {player_name}',
            xaxis_title='Fielding Actions',
            yaxis_title='Count',
            barmode='group'
        )
        
        return fig
    
    def create_match_trends(self, player_data, player_name):
        """Create match-wise trend analysis"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Catch Success Rate', 'Run-out Success Rate', 
                          'Fielding Efficiency', 'Total Actions'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        matches = player_data['Match_No'].tolist()
        
        # Catch Success Rate
        fig.add_trace(
            go.Scatter(x=matches, y=player_data['Catch_Success_Rate']*100,
                      mode='lines+markers', name='Catch Success %'),
            row=1, col=1
        )
        
        # Run-out Success Rate
        fig.add_trace(
            go.Scatter(x=matches, y=player_data['Runout_Success_Rate']*100,
                      mode='lines+markers', name='Run-out Success %'),
            row=1, col=2
        )
        
        # Fielding Efficiency
        fig.add_trace(
            go.Scatter(x=matches, y=player_data['Fielding_Efficiency']*100,
                      mode='lines+markers', name='Efficiency %'),
            row=2, col=1
        )
        
        # Total Actions
        fig.add_trace(
            go.Bar(x=matches, y=player_data['Total_Fielding_Actions'],
                   name='Total Actions'),
            row=2, col=2
        )
        
        fig.update_layout(
            title=f'Match-wise Performance Trends - {player_name}',
            showlegend=False
        )
        
        return fig
    
    def create_action_breakdown(self, player_data, player_name):
        """Create pie chart showing action breakdown"""
        total_stats = {
            'Catches Taken': player_data['Catches_Taken'].sum(),
            'Run-outs Executed': player_data['Run_Outs_Executed'].sum(),
            'Boundaries Saved': player_data['Boundaries_Saved'].sum(),
            'Direct Hits': player_data['Direct_Hits'].sum(),
            'Catches Dropped': player_data['Catches_Dropped'].sum(),
            'Run-outs Missed': player_data['Run_Outs_Missed'].sum(),
            'Fumbles': player_data['Fumbles'].sum()
        }
        
        # Filter out zero values
        filtered_stats = {k: v for k, v in total_stats.items() if v > 0}
        
        fig = go.Figure(data=[go.Pie(
            labels=list(filtered_stats.keys()),
            values=list(filtered_stats.values()),
            hole=0.3
        )])
        
        fig.update_layout(
            title=f'Fielding Actions Breakdown - {player_name}',
            annotations=[dict(text=player_name, x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig
    
    def create_efficiency_analysis(self, player_data, player_name):
        """Create efficiency analysis scatter plot"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=player_data['Total_Fielding_Actions'],
            y=player_data['Fielding_Efficiency']*100,
            mode='markers',
            marker=dict(
                size=player_data['Impact_Score']*2,
                color=player_data['Match_No'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Match No.")
            ),
            text=[f"Match {match}" for match in player_data['Match_No']],
            textposition="top center"
        ))
        
        fig.update_layout(
            title=f'Efficiency vs Action Volume - {player_name}',
            xaxis_title='Total Fielding Actions',
            yaxis_title='Fielding Efficiency (%)',
            hovermode='closest'
        )
        
        return fig
    
    def create_radar_comparison(self, comparison_data, selected_players):
        """Create radar chart for player comparison"""
        # Calculate average metrics for each player
        player_metrics = []
        
        for player in selected_players:
            player_data = comparison_data[comparison_data['Player_Name'] == player]
            metrics = {
                'Player': player,
                'Catch Success': player_data['Catch_Success_Rate'].mean() * 100,
                'Run-out Success': player_data['Runout_Success_Rate'].mean() * 100,
                'Fielding Efficiency': player_data['Fielding_Efficiency'].mean() * 100,
                'Low Error Rate': (1 - player_data['Error_Rate'].mean()) * 100,
                'Impact Score': player_data['Impact_Score'].mean()
            }
            player_metrics.append(metrics)
        
        fig = go.Figure()
        
        categories = ['Catch Success', 'Run-out Success', 'Fielding Efficiency', 
                     'Low Error Rate', 'Impact Score']
        
        for i, player_metric in enumerate(player_metrics):
            values = [player_metric[cat] for cat in categories]
            values.append(values[0])  # Complete the circle
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=player_metric['Player'],
                line_color=self.colors[i % len(self.colors)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            title="Player Performance Comparison - Radar Chart"
        )
        
        return fig
    
    def create_success_rates_comparison(self, comparison_data, selected_players):
        """Create success rates comparison chart"""
        player_stats = []
        
        for player in selected_players:
            player_data = comparison_data[comparison_data['Player_Name'] == player]
            stats = {
                'Player': player,
                'Catch Success Rate': player_data['Catch_Success_Rate'].mean() * 100,
                'Run-out Success Rate': player_data['Runout_Success_Rate'].mean() * 100,
                'Fielding Efficiency': player_data['Fielding_Efficiency'].mean() * 100
            }
            player_stats.append(stats)
        
        df_stats = pd.DataFrame(player_stats)
        
        fig = go.Figure()
        
        metrics = ['Catch Success Rate', 'Run-out Success Rate', 'Fielding Efficiency']
        
        for metric in metrics:
            fig.add_trace(go.Bar(
                name=metric,
                x=df_stats['Player'],
                y=df_stats[metric]
            ))
        
        fig.update_layout(
            title='Success Rates Comparison',
            xaxis_title='Players',
            yaxis_title='Success Rate (%)',
            barmode='group'
        )
        
        return fig
    
    def create_action_volume_comparison(self, comparison_data, selected_players):
        """Create action volume comparison"""
        player_actions = []
        
        for player in selected_players:
            player_data = comparison_data[comparison_data['Player_Name'] == player]
            actions = {
                'Player': player,
                'Catches Taken': player_data['Catches_Taken'].sum(),
                'Run-outs Executed': player_data['Run_Outs_Executed'].sum(),
                'Boundaries Saved': player_data['Boundaries_Saved'].sum(),
                'Direct Hits': player_data['Direct_Hits'].sum()
            }
            player_actions.append(actions)
        
        df_actions = pd.DataFrame(player_actions)
        
        fig = go.Figure()
        
        action_types = ['Catches Taken', 'Run-outs Executed', 'Boundaries Saved', 'Direct Hits']
        
        for action in action_types:
            fig.add_trace(go.Bar(
                name=action,
                x=df_actions['Player'],
                y=df_actions[action]
            ))
        
        fig.update_layout(
            title='Action Volume Comparison',
            xaxis_title='Players',
            yaxis_title='Count',
            barmode='stack'
        )
        
        return fig
    
    def create_efficiency_scatter(self, comparison_data, selected_players):
        """Create efficiency scatter plot for comparison"""
        fig = go.Figure()
        
        for i, player in enumerate(selected_players):
            player_data = comparison_data[comparison_data['Player_Name'] == player]
            
            fig.add_trace(go.Scatter(
                x=player_data['Total_Fielding_Actions'],
                y=player_data['Fielding_Efficiency']*100,
                mode='markers',
                name=player,
                marker=dict(
                    size=10,
                    color=self.colors[i % len(self.colors)]
                ),
                text=[f"Match {match}" for match in player_data['Match_No']],
                textposition="top center"
            ))
        
        fig.update_layout(
            title='Efficiency vs Action Volume - Player Comparison',
            xaxis_title='Total Fielding Actions',
            yaxis_title='Fielding Efficiency (%)',
            hovermode='closest'
        )
        
        return fig
    
    def create_team_contribution(self, match_data):
        """Create team contribution pie chart"""
        player_contributions = match_data.groupby('Player_Name')['Total_Fielding_Actions'].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=player_contributions.index,
            values=player_contributions.values,
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title='Individual Contribution to Team Fielding Actions'
        )
        
        return fig
    
    def create_team_performance_breakdown(self, match_data):
        """Create team performance breakdown"""
        team_stats = {
            'Total Catches': match_data['Catches_Taken'].sum(),
            'Total Run-outs': match_data['Run_Outs_Executed'].sum(),
            'Boundaries Saved': match_data['Boundaries_Saved'].sum(),
            'Direct Hits': match_data['Direct_Hits'].sum(),
            'Catches Dropped': match_data['Catches_Dropped'].sum(),
            'Run-outs Missed': match_data['Run_Outs_Missed'].sum(),
            'Fumbles': match_data['Fumbles'].sum()
        }
        
        # Separate positive and negative actions
        positive_actions = ['Total Catches', 'Total Run-outs', 'Boundaries Saved', 'Direct Hits']
        negative_actions = ['Catches Dropped', 'Run-outs Missed', 'Fumbles']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Positive Actions',
            x=positive_actions,
            y=[team_stats[action] for action in positive_actions],
            marker_color='green',
            opacity=0.7
        ))
        
        fig.add_trace(go.Bar(
            name='Errors/Misses',
            x=negative_actions,
            y=[team_stats[action] for action in negative_actions],
            marker_color='red',
            opacity=0.7
        ))
        
        fig.update_layout(
            title='Team Performance Breakdown',
            xaxis_title='Action Type',
            yaxis_title='Count',
            barmode='group'
        )
        
        return fig
