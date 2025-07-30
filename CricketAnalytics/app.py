import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils.data_processor import DataProcessor
from utils.visualization import Visualizer
from utils.metrics_calculator import MetricsCalculator

# Page configuration
st.set_page_config(
    page_title="Cricket Fielding Analysis Tool",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

def main():
    st.title("🏏 Cricket Fielding Analysis Tool")
    st.markdown("### T20 Match Fielding Performance Evaluation")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose Analysis Section",
        ["Data Upload", "Player Analysis", "Comparative Analysis", "Team Performance", "Export Results"]
    )
    
    # Initialize processors
    data_processor = DataProcessor()
    visualizer = Visualizer()
    metrics_calculator = MetricsCalculator()
    
    if page == "Data Upload":
        data_upload_page(data_processor)
    elif page == "Player Analysis":
        player_analysis_page(visualizer, metrics_calculator)
    elif page == "Comparative Analysis":
        comparative_analysis_page(visualizer, metrics_calculator)
    elif page == "Team Performance":
        team_performance_page(visualizer, metrics_calculator)
    elif page == "Export Results":
        export_results_page()

def data_upload_page(data_processor):
    st.header("📁 Data Upload and Validation")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Cricket Fielding Data (CSV format)",
        type=['csv'],
        help="Upload a CSV file containing fielding performance data"
    )
    
    if uploaded_file is not None:
        try:
            # Read and validate data
            raw_data = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            
            # Display raw data preview
            st.subheader("Raw Data Preview")
            st.dataframe(raw_data.head(10))
            
            # Data validation and processing
            with st.spinner("Validating and processing data..."):
                validation_result = data_processor.validate_data(raw_data)
                
                if validation_result['is_valid']:
                    processed_data = data_processor.process_data(raw_data)
                    st.session_state.data = raw_data
                    st.session_state.processed_data = processed_data
                    
                    st.success("✅ Data validation successful!")
                    
                    # Display data summary
                    st.subheader("Data Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Records", len(processed_data))
                    with col2:
                        st.metric("Players", processed_data['Player_Name'].nunique())
                    with col3:
                        st.metric("Matches", processed_data['Match_No'].nunique())
                    with col4:
                        st.metric("Total Actions", processed_data['Total_Fielding_Actions'].sum())
                    
                    # Display processed data
                    st.subheader("Processed Data")
                    st.dataframe(processed_data)
                    
                else:
                    st.error("❌ Data validation failed!")
                    for error in validation_result['errors']:
                        st.error(f"• {error}")
                    
                    st.info("Please ensure your CSV file contains the following required columns:")
                    required_columns = [
                        "Match_No", "Player_Name", "Catches_Taken", "Catches_Dropped",
                        "Run_Outs_Executed", "Run_Outs_Missed", "Boundaries_Saved",
                        "Direct_Hits", "Fumbles", "Total_Fielding_Actions"
                    ]
                    for col in required_columns:
                        st.write(f"• {col}")
                        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please ensure the file is a valid CSV format.")
    
    else:
        st.info("Please upload a CSV file to begin analysis.")
        
        # Display sample data format
        st.subheader("Expected Data Format")
        sample_data = {
            'Match_No': [1, 1, 2],
            'Player_Name': ['Player A', 'Player B', 'Player A'],
            'Catches_Taken': [3, 2, 1],
            'Catches_Dropped': [1, 0, 2],
            'Run_Outs_Executed': [1, 2, 0],
            'Run_Outs_Missed': [0, 1, 1],
            'Boundaries_Saved': [2, 3, 1],
            'Direct_Hits': [1, 1, 0],
            'Fumbles': [2, 1, 3],
            'Total_Fielding_Actions': [10, 10, 8]
        }
        st.dataframe(pd.DataFrame(sample_data))

def player_analysis_page(visualizer, metrics_calculator):
    st.header("👤 Individual Player Analysis")
    
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload data first in the Data Upload section.")
        return
    
    data = st.session_state.processed_data
    
    # Player selection
    selected_player = st.selectbox(
        "Select Player for Analysis",
        options=data['Player_Name'].unique(),
        help="Choose a player to analyze their fielding performance"
    )
    
    if selected_player:
        player_data = data[data['Player_Name'] == selected_player]
        
        # Calculate metrics
        metrics = metrics_calculator.calculate_player_metrics(player_data)
        
        # Display key metrics
        st.subheader(f"📊 Performance Metrics for {selected_player}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Catch Success Rate", f"{metrics['catch_success_rate']:.1%}")
        with col2:
            st.metric("Run-out Success Rate", f"{metrics['runout_success_rate']:.1%}")
        with col3:
            st.metric("Fielding Efficiency", f"{metrics['fielding_efficiency']:.1%}")
        with col4:
            st.metric("Error Rate", f"{metrics['error_rate']:.1%}")
        
        # Visualization options
        st.subheader("📈 Visualizations")
        
        viz_type = st.selectbox(
            "Select Visualization Type",
            ["Performance Overview", "Match-wise Trends", "Action Breakdown", "Efficiency Analysis"]
        )
        
        if viz_type == "Performance Overview":
            fig = visualizer.create_player_overview(player_data, selected_player)
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Match-wise Trends":
            fig = visualizer.create_match_trends(player_data, selected_player)
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Action Breakdown":
            fig = visualizer.create_action_breakdown(player_data, selected_player)
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Efficiency Analysis":
            fig = visualizer.create_efficiency_analysis(player_data, selected_player)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed statistics table
        st.subheader("📋 Detailed Statistics")
        detailed_stats = metrics_calculator.get_detailed_stats(player_data)
        st.dataframe(detailed_stats)

def comparative_analysis_page(visualizer, metrics_calculator):
    st.header("⚖️ Comparative Player Analysis")
    
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload data first in the Data Upload section.")
        return
    
    data = st.session_state.processed_data
    
    # Multi-player selection
    selected_players = st.multiselect(
        "Select Players for Comparison (2-6 players recommended)",
        options=data['Player_Name'].unique(),
        help="Choose multiple players to compare their performance"
    )
    
    if len(selected_players) < 2:
        st.info("Please select at least 2 players for comparison.")
        return
    
    comparison_data = data[data['Player_Name'].isin(selected_players)]
    
    # Comparison metrics
    st.subheader("📊 Comparison Metrics")
    comparison_metrics = metrics_calculator.calculate_comparison_metrics(comparison_data)
    st.dataframe(comparison_metrics)
    
    # Visualization options
    st.subheader("📈 Comparison Visualizations")
    
    comparison_type = st.selectbox(
        "Select Comparison Type",
        ["Overall Performance Radar", "Success Rates Comparison", "Action Volume Comparison", "Efficiency Scatter Plot"]
    )
    
    if comparison_type == "Overall Performance Radar":
        fig = visualizer.create_radar_comparison(comparison_data, selected_players)
        st.plotly_chart(fig, use_container_width=True)
        
    elif comparison_type == "Success Rates Comparison":
        fig = visualizer.create_success_rates_comparison(comparison_data, selected_players)
        st.plotly_chart(fig, use_container_width=True)
        
    elif comparison_type == "Action Volume Comparison":
        fig = visualizer.create_action_volume_comparison(comparison_data, selected_players)
        st.plotly_chart(fig, use_container_width=True)
        
    elif comparison_type == "Efficiency Scatter Plot":
        fig = visualizer.create_efficiency_scatter(comparison_data, selected_players)
        st.plotly_chart(fig, use_container_width=True)

def team_performance_page(visualizer, metrics_calculator):
    st.header("🏏 Team Performance Analysis")
    
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload data first in the Data Upload section.")
        return
    
    data = st.session_state.processed_data
    
    # Match selection for team analysis
    selected_match = st.selectbox(
        "Select Match for Team Analysis",
        options=sorted(data['Match_No'].unique()),
        help="Choose a match to analyze overall team fielding performance"
    )
    
    match_data = data[data['Match_No'] == selected_match]
    
    # Team metrics
    st.subheader(f"📊 Team Performance - Match {selected_match}")
    team_metrics = metrics_calculator.calculate_team_metrics(match_data)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Team Catch Success", f"{team_metrics['team_catch_success']:.1%}")
    with col2:
        st.metric("Team Run-out Success", f"{team_metrics['team_runout_success']:.1%}")
    with col3:
        st.metric("Total Actions", int(team_metrics['total_actions']))
    with col4:
        st.metric("Team Error Rate", f"{team_metrics['team_error_rate']:.1%}")
    
    # Team visualizations
    st.subheader("📈 Team Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_contribution = visualizer.create_team_contribution(match_data)
        st.plotly_chart(fig_contribution, use_container_width=True)
    
    with col2:
        fig_performance = visualizer.create_team_performance_breakdown(match_data)
        st.plotly_chart(fig_performance, use_container_width=True)
    
    # Player rankings for the match
    st.subheader("🏆 Player Rankings (Current Match)")
    rankings = metrics_calculator.calculate_player_rankings(match_data)
    st.dataframe(rankings)

def export_results_page():
    st.header("📤 Export Results")
    
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload and process data first.")
        return
    
    data = st.session_state.processed_data
    
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export processed data
        if st.button("📊 Export Processed Data"):
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="cricket_fielding_analysis.csv",
                mime="text/csv"
            )
    
    with col2:
        # Export summary report
        if st.button("📋 Export Summary Report"):
            metrics_calc = MetricsCalculator()
            summary_report = metrics_calc.generate_summary_report(data)
            
            st.download_button(
                label="Download Report",
                data=summary_report,
                file_name="fielding_analysis_report.txt",
                mime="text/plain"
            )
    
    # Export options information
    st.info("💡 Tip: You can also use your browser's print function to save visualizations as PDF.")

if __name__ == "__main__":
    main()
