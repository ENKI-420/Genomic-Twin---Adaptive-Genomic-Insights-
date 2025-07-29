import streamlit as st
import json
import subprocess
import os
from datetime import datetime

def load_tokenomics_state():
    """Load the current tokenomics state from the JSON file."""
    try:
        with open('tokenomics_state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def load_tokenomics_dashboard_config():
    """Load the tokenomics dashboard configuration."""
    try:
        with open('tokenomics_dashboard.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def run_tokenomics_evolution():
    """Run the tokenomics evolution engine."""
    try:
        result = subprocess.run(['npm', 'run', 'start:tokenomics'], 
                               capture_output=True, text=True, cwd='.')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def display_tokenomics_metrics(state):
    """Display key tokenomics metrics."""
    if not state:
        st.error("No tokenomics data available. Run evolution first.")
        return
    
    final_state = state.get('final_state', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Liquidity Ratio",
            f"{final_state.get('liquidity_ratio', 0) * 100:.1f}%",
            delta=f"Target: 85%"
        )
    
    with col2:
        st.metric(
            "APR",
            f"{final_state.get('apr', 0) * 100:.1f}%",
            delta=f"Target: 12%"
        )
    
    with col3:
        st.metric(
            "Participation Rate",
            f"{final_state.get('participation_rate', 0) * 100:.1f}%",
            delta=f"Target: 70%"
        )
    
    with col4:
        st.metric(
            "Treasury Efficiency",
            f"{final_state.get('treasury_efficiency', 0) * 100:.1f}%",
            delta=f"Target: 75%"
        )

def display_liquidity_pools(dashboard_config):
    """Display liquidity pool information."""
    if not dashboard_config:
        return
    
    pools = dashboard_config.get('pools', [])
    
    st.subheader("🏊 Liquidity Pools")
    
    for pool in pools:
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{pool['name']}**")
            
            with col2:
                st.write(f"TVL: ${pool['liquidity']/1000000:.2f}M")
            
            with col3:
                st.write(f"APR: {pool['apr']*100:.1f}%")

def display_governance_info(dashboard_config):
    """Display governance information."""
    if not dashboard_config:
        return
    
    governance = dashboard_config.get('governance', {})
    
    st.subheader("🗳️ Governance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Active Proposals", governance.get('active_proposals', 0))
        st.metric("Participation Rate", f"{governance.get('participation_rate', 0)*100:.1f}%")
    
    with col2:
        st.metric("Voting Power Distributed", f"{governance.get('voting_power_distributed', 0)*100:.1f}%")

def display_treasury_info(dashboard_config):
    """Display treasury information."""
    if not dashboard_config:
        return
    
    treasury = dashboard_config.get('treasury', {})
    
    st.subheader("🏦 Treasury Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Assets", f"${treasury.get('total_assets', 0)/1000000:.2f}M")
        st.metric("Efficiency Score", f"{treasury.get('efficiency_score', 0)*100:.1f}%")
    
    with col2:
        st.write("**Asset Allocation:**")
        allocation = treasury.get('asset_allocation', {})
        for asset, percentage in allocation.items():
            st.write(f"- {asset.title()}: {percentage*100:.0f}%")

def display_evolution_log(state):
    """Display the evolution log."""
    if not state:
        return
    
    evolution_log = state.get('evolution_log', [])
    
    st.subheader("📊 Evolution History")
    
    # Show recent mutations
    mutations = [log for log in evolution_log if '[MUTATION]' in log]
    if mutations:
        st.write("**Recent Mutations:**")
        for mutation in mutations[-5:]:  # Show last 5 mutations
            st.text(mutation)
    
    # Show key milestones
    milestones = [log for log in evolution_log if '[ALERT]' in log or '[MILESTONE]' in log]
    if milestones:
        st.write("**Key Milestones:**")
        for milestone in milestones:
            st.success(milestone)

def tokenomics_dashboard():
    """Main tokenomics dashboard function."""
    st.title("💰 Tokenomics Dashboard")
    st.caption("Autonomous DeFi Management System")
    
    # Load current state
    state = load_tokenomics_state()
    dashboard_config = load_tokenomics_dashboard_config()
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Run Evolution", use_container_width=True):
            with st.spinner("Running tokenomics evolution..."):
                success, stdout, stderr = run_tokenomics_evolution()
                
                if success:
                    st.success("Evolution completed successfully!")
                    st.rerun()  # Refresh to show new data
                else:
                    st.error(f"Evolution failed: {stderr}")
    
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    with col3:
        if os.path.exists('tokenomics_dashboard.html'):
            with open('tokenomics_dashboard.html', 'rb') as f:
                st.download_button(
                    "📊 Download Dashboard",
                    f.read(),
                    file_name="tokenomics_dashboard.html",
                    mime="text/html",
                    use_container_width=True
                )
    
    # Display status
    if state and state.get('transcendence_achieved'):
        st.success("🎯 **TRANSCENDENCE ACHIEVED** - Autonomous DeFi management is active!")
    elif state:
        st.info("🔄 Evolution in progress...")
    else:
        st.warning("⚠️ No tokenomics data found. Run evolution to start.")
    
    if state:
        # Main metrics
        st.header("📈 Key Metrics")
        display_tokenomics_metrics(state)
        
        # Detailed information
        if dashboard_config:
            col1, col2 = st.columns(2)
            
            with col1:
                display_liquidity_pools(dashboard_config)
                display_governance_info(dashboard_config)
            
            with col2:
                display_treasury_info(dashboard_config)
                display_evolution_log(state)
        
        # Evolution summary
        st.header("🧬 Evolution Summary")
        evolution_summary = {
            "Organism": state.get('organism', 'TokenomicsCore'),
            "Generations": state.get('final_generation', 0),
            "Evolution Completed": state.get('evolution_completed', 'N/A'),
            "Transcendence": "✅ ACHIEVED" if state.get('transcendence_achieved') else "❌ Not Reached",
            "Dashboard Generated": "✅ Generated" if state.get('dashboard_generated') else "❌ Not Generated"
        }
        
        for key, value in evolution_summary.items():
            st.write(f"**{key}:** {value}")
    
    # DNA organism info
    st.header("🧬 TokenomicsCore Organism")
    if os.path.exists('Tokenomics.dna'):
        with st.expander("View Tokenomics.dna"):
            with open('Tokenomics.dna', 'r') as f:
                st.code(f.read(), language='text')
    
    # Raw data
    if state and st.checkbox("Show Raw Data"):
        st.subheader("🔧 Raw State Data")
        st.json(state)
        
        if dashboard_config:
            st.subheader("🔧 Dashboard Config")
            st.json(dashboard_config)

if __name__ == "__main__":
    tokenomics_dashboard()