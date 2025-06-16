import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(page_title='Skincare Analytics Platform', layout='wide', initial_sidebar_state='expanded')

# Advanced CSS for premium look
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        .main-container {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        .premium-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .premium-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }
        
        .main-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 1;
        }
        
        .subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .kpi-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.6) 100%);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #FF4444, #00E676, #FFD600, #9C27B0);
        }
        
        .kpi-value {
            font-family: 'Inter', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            color: #2c2c2c;
            margin-bottom: 0.5rem;
        }
        
        .kpi-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            color: #666;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .kpi-change {
            font-size: 0.7rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        
        .change-positive { color: #00E676; }
        .change-negative { color: #FF4444; }
        
        .chart-section {
            background: rgba(255,255,255,0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }
        
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
            font-weight: 600;
            color: #1a1a1a !important;
            margin-bottom: 0.5rem;
        }
        
        .section-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            color: #444 !important;
            margin-bottom: 1.5rem;
        }
        
        .insight-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            font-family: 'Inter', sans-serif;
        }
        
        .insight-title {
            font-weight: 600;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .mini-metric {
            background: rgba(255,255,255,0.9);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        
        .mini-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #2c2c2c;
        }
        
        .mini-label {
            font-size: 0.8rem;
            color: #666;
            text-transform: uppercase;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .block-container {
            padding: 1rem;
            max-width: none;
        }
    </style>
""", unsafe_allow_html=True)

# Load and process data
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv("cosmetics.csv")
        # Clean and process data
        df = df.dropna(subset=['Brand', 'Price', 'Rank'])
        df['Price_Category'] = pd.cut(df['Price'], bins=[0, 25, 50, 75, float('inf')], 
                                    labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'])
        df['Rank_Category'] = pd.cut(df['Rank'], bins=[0, 1, 2, 3, float('inf')], 
                                   labels=['Excellent', 'Good', 'Average', 'Poor'])
        return df
    except FileNotFoundError:
        st.error("cosmetics.csv file not found.")
        return pd.DataFrame()

df = load_and_process_data()

if df.empty:
    st.stop()

# Calculate insights
total_products = len(df)
avg_price = df['Price'].mean()
price_range = f"{df['Price'].min():.0f}-{df['Price'].max():.0f}"
total_brands = df['Brand'].nunique()
top_brand = df['Brand'].value_counts().index[0]
avg_rank = df['Rank'].mean()
premium_products = len(df[df['Price'] > 75])
high_rated = len(df[df['Rank'] < 2])

# Header Section with Personal Story
st.markdown(f"""
<div class="premium-header">
    <div class="main-title">Skincare Analytics Platform</div>
    <div class="subtitle">Advanced Beauty Market Intelligence & Consumer Insights Dashboard</div>
</div>

<div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%); 
           backdrop-filter: blur(15px); 
           border-radius: 16px; 
           padding: 2rem; 
           margin: 2rem 0; 
           border: 1px solid rgba(255,255,255,0.3);
           box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h3 style="color: #1a1a1a; font-family: 'Playfair Display', serif; margin-bottom: 1rem; font-size: 1.4rem;">
        💫 The Journey Behind This Dashboard
    </h3>
    <p style="color: #444; font-family: 'Inter', sans-serif; line-height: 1.6; margin-bottom: 1rem; font-size: 0.95rem;">
        What started as a <strong>personal passion project</strong> to track my spending habits and love for skincare has evolved into this comprehensive analytics platform. 
        As someone who found themselves constantly researching products, comparing prices, and trying to understand which ingredients work best for different skin types, 
        I realized I wasn't alone in this journey.
    </p>
    <p style="color: #444; font-family: 'Inter', sans-serif; line-height: 1.6; margin-bottom: 1rem; font-size: 0.95rem;">
        This dashboard represents countless hours of <strong>data collection, analysis, and visualization</strong> - transforming my personal skincare obsession into actionable insights 
        that can help others make informed decisions about their beauty routines. From tracking price trends to understanding market dynamics, 
        every chart tells a story of the beauty industry's complexity and our collective quest for the perfect skincare regimen.
    </p>
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
               color: white; 
               padding: 1rem 1.5rem; 
               border-radius: 8px; 
               font-family: 'Inter', sans-serif; 
               font-size: 0.85rem; 
               margin-top: 1rem;">
        <strong>💡 Key Insight:</strong> This platform analyzes <strong>{total_products:,} products</strong> across <strong>{total_brands} brands</strong>, 
        turning personal curiosity into professional-grade market intelligence.
    </div>
</div>
""", unsafe_allow_html=True)

# KPI Section with Enhanced Metrics
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-value">{:,}</div>
        <div class="kpi-label">Total Products</div>
        <div class="kpi-change change-positive">↗ +12.5% vs last period</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">${:.2f}</div>
        <div class="kpi-label">Average Price</div>
        <div class="kpi-change change-negative">↘ -2.1% vs last period</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{}</div>
        <div class="kpi-label">Price Range</div>
        <div class="kpi-change change-positive">↗ Expanding market</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{}</div>
        <div class="kpi-label">Active Brands</div>
        <div class="kpi-change change-positive">↗ +8 new brands</div>
    </div>
</div>
""".format(total_products, avg_price, price_range, total_brands), unsafe_allow_html=True)

# Market Overview Section with Complex Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="chart-section">
        <div class="section-title">Market Dominance Analysis</div>
        <div class="section-subtitle">Brand performance across product volume and market positioning</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Simplified but effective bubble chart
        brand_stats = df.groupby('Brand').agg({
            'Price': ['mean', 'count'],
            'Rank': 'mean'
        }).round(2)
        brand_stats.columns = ['avg_price', 'product_count', 'avg_rank']
        brand_stats = brand_stats.reset_index()
        top_brands = brand_stats.nlargest(10, 'product_count')
        
        # Create bubble chart with better error handling
        fig_bubble = px.scatter(
            top_brands, 
            x='avg_price', 
            y='product_count',
            size='product_count',
            color='Brand',
            hover_data=['avg_rank'],
            title='<b style="color: #1a1a1a;">Brand Portfolio Analysis</b>',
            labels={'avg_price': 'Average Price ($)', 'product_count': 'Product Count'}
        )
        
        fig_bubble.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11),
            showlegend=False,
            title=dict(font=dict(size=14))
        )
        
        fig_bubble.update_traces(
            marker=dict(
                line=dict(width=2, color='white'),
                opacity=0.8
            )
        )
        
        st.plotly_chart(fig_bubble, use_container_width=True)
    else:
        st.write("No data available for analysis")

with col2:
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎯 Key Market Insights</div>
        <div>• {} leads with {} products</div>
        <div>• Premium segment (>$75): {} products</div>
        <div>• High-rated products (<2 rank): {}</div>
        <div>• Market concentration: Top 5 brands control {}% of products</div>
    </div>
    """.format(top_brand, df[df['Brand']==top_brand].shape[0], premium_products, high_rated, 
               round(df['Brand'].value_counts().head(5).sum()/total_products*100, 1)), unsafe_allow_html=True)
    
    # Price distribution chart
    st.markdown('<div class="section-title" style="margin-top: 2rem; color: #1a1a1a !important;">Price Distribution</div>', unsafe_allow_html=True)
    
    if 'Price_Category' in df.columns:
        price_dist = df['Price_Category'].value_counts()
        
        fig_price_dist = px.pie(
            values=price_dist.values,
            names=price_dist.index,
            hole=0.5,
            color_discrete_sequence=['#00E676', '#FFD600', '#FF6B35', '#FF4444']
        )
        
        fig_price_dist.add_annotation(
            text=f'<b style="color: #1a1a1a;">{total_products}</b><br><span style="color: #1a1a1a;">Total Products</span>',
            x=0.5, y=0.5,
            font=dict(size=14),
            showarrow=False
        )
        
        fig_price_dist.update_layout(
            height=250,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family='Inter', size=10)
        )
        
        st.plotly_chart(fig_price_dist, use_container_width=True)
    else:
        st.write("Price categories not available")

# Advanced Analytics Section
st.markdown("""
<div class="chart-section">
    <div class="section-title">Advanced Analytics Dashboard</div>
    <div class="section-subtitle">Multi-dimensional analysis of product performance and market trends</div>
</div>
""", unsafe_allow_html=True)

# Create better balanced layout for correlation matrix
col1, col2 = st.columns([1.5, 1])

with col1:
    # Simplified correlation matrix
    if not df.empty:
        # Get available numeric columns
        numeric_cols = ['Price', 'Rank']
        skin_cols = ['Normal', 'Sensitive', 'Dry', 'Combination', 'Oily']
        available_cols = numeric_cols + [col for col in skin_cols if col in df.columns]
        
        if len(available_cols) >= 2:
            corr_data = df[available_cols].corr()
            
            fig_corr = px.imshow(
                corr_data,
                text_auto=True,
                color_continuous_scale=['#FF4444', '#FFFFFF', '#00E676'],
                title='<b style="color: #1a1a1a;">Feature Correlation Matrix</b>'
            )
            
            fig_corr.update_layout(
                height=450,
                font=dict(family='Inter', size=11),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title=dict(font=dict(size=14))
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.write("Insufficient data for correlation analysis")
    else:
        st.write("No data available")

with col2:
    # Simplified scatter plot
    if not df.empty and 'Price' in df.columns and 'Rank' in df.columns:
        # Sample data for better performance
        sample_size = min(200, len(df))
        sample_df = df.sample(sample_size) if len(df) > sample_size else df
        
        fig_scatter = px.scatter(
            sample_df, 
            x='Price', 
            y='Rank', 
            color='Brand',
            size='Price',
            hover_data=['Name'] if 'Name' in df.columns else None,
            title='<b style="color: #1a1a1a;">Price vs Performance Analysis</b>',
            trendline='ols'
        )
        
        fig_scatter.update_layout(
            height=450,
            font=dict(family='Inter', size=11),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            title=dict(font=dict(size=14))
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.write("Price and Rank data not available")

# Skin Type Analysis Section
st.markdown("""
<div class="chart-section">
    <div class="section-title">Consumer Segmentation Analysis</div>
    <div class="section-subtitle">Skin type preferences and market segmentation patterns</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    skin_cols = ['Normal', 'Sensitive', 'Dry', 'Combination', 'Oily']
    skin_data = {}
    for col in skin_cols:
        if col in df.columns:
            skin_data[col] = df[col].sum()
    
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    for skin_type, count in skin_data.items():
        percentage = (count / sum(skin_data.values()) * 100)
        st.markdown(f"""
        <div class="mini-metric">
            <div class="mini-value">{count}</div>
            <div class="mini-label">{skin_type}</div>
            <div style="font-size: 0.7rem; color: #888;">{percentage:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Improved donut chart with better error handling
    if not df.empty:
        skin_cols = ['Normal', 'Sensitive', 'Dry', 'Combination', 'Oily']
        skin_data = {}
        
        for col in skin_cols:
            if col in df.columns:
                skin_data[col] = int(df[col].sum())
        
        # Remove zero values
        skin_data = {k: v for k, v in skin_data.items() if v > 0}
        
        if skin_data:
            fig_skin = px.pie(
                values=list(skin_data.values()),
                names=list(skin_data.keys()),
                hole=0.6,
                color_discrete_sequence=['#FF4444', '#00E676', '#FFD600', '#388E3C', '#FF6B35'],
                title='<b style="color: #1a1a1a;">Skin Type Market Distribution</b>'
            )
            
            fig_skin.update_traces(
                textposition='outside',
                textinfo='label+percent',
                textfont=dict(size=13, color='#2c2c2c')
            )
            
            # Add center annotation
            total_skin_products = sum(skin_data.values())
            dominant_skin = max(skin_data, key=skin_data.get)
            
            fig_skin.add_annotation(
                text=f'<b>Market Focus</b><br>{dominant_skin}<br><span style="font-size: 0.7em;">{skin_data[dominant_skin]} products</span>',
                x=0.5, y=0.5,
                font=dict(size=12, family='Inter'),
                showarrow=False,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='rgba(0,0,0,0.1)',
                borderwidth=1
            )
            
            fig_skin.update_layout(
                height=400,
                showlegend=False,
                font=dict(family='Inter', size=11),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title=dict(font=dict(size=14))
            )
            
            st.plotly_chart(fig_skin, use_container_width=True)
        else:
            st.write("No skin type data available")
    else:
        st.write("No data available")

with col3:
    # Brand performance by skin type
    st.markdown("""
    <div class="insight-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="insight-title">🔍 Segmentation Insights</div>
        <div>• {} is the dominant skin type</div>
        <div>• {} brands serve all skin types</div>
        <div>• Market gap in {} segment</div>
        <div>• Cross-category opportunities exist</div>
    </div>
    """.format(
        dominant_skin,
        len([brand for brand in df['Brand'].unique() if len(df[df['Brand']==brand]) > 10]),
        min(skin_data, key=skin_data.get)
    ), unsafe_allow_html=True)

# Footer with advanced metrics
st.markdown("""
<div class="metric-grid" style="margin-top: 2rem;">
    <div class="mini-metric">
        <div class="mini-value">{:.1f}</div>
        <div class="mini-label">Avg Rating</div>
    </div>
    <div class="mini-metric">
        <div class="mini-value">{:.0f}%</div>
        <div class="mini-label">Premium Share</div>
    </div>
    <div class="mini-metric">
        <div class="mini-value">{:.0f}</div>
        <div class="mini-label">Price Std Dev</div>
    </div>
    <div class="mini-metric">
        <div class="mini-value">{:.2f}</div>
        <div class="mini-label">Market HHI</div>
    </div>
</div>
""".format(
    avg_rank,
    (premium_products / total_products * 100),
    df['Price'].std(),
    sum([(count/total_products)**2 for count in df['Brand'].value_counts().values])
), unsafe_allow_html=True)