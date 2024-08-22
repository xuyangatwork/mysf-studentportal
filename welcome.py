import streamlit as st

   
def welcome_page():

    st.subheader("This tool is designed to help you analyze and sense making your RIASEC, Career Inspiration and Goals.")

    # Custom CSS for icons, containers, fixed height, and footnote
    st.markdown("""
    <style>
    .container {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        height: 200px;
        overflow-y: auto;
    }
    .container h3 {
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 18px;
    }
    .container ul, .container ol {
        margin: 0;
        padding-left: 20px;
    }
    .footnote {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        color: #666;
        text-align: center;
        padding: 5px;
        font-style: italic;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        # 1. Functionality of tool
        st.markdown("""
        <div class="container">
            <h3>🚀  Functionality</h3>
            <ul>
                <li>RIASEC</li>
                <li>Career Inspiration and Goal</li>
                <li>Generative AI Advice</li>
                <li>Prompt Engineering</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Team Members behind this tool
        st.markdown("""
        <div class="container">
            <h3>👥  Team Members</h3>
            <ul>
                <li>POC1: XU Yang - ITD</li>
                <li>POC2: Yu Chyi - ECGB</li>
                <li>Hui Shan, Benin - ECGB</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


    with col2:
        # 2. Reminder on the use of tool
        st.markdown("""
        <div class="container">
            <h3>⚠️  Reminder</h3>
            <ul>
                <li>For advice only; not sole basis for decision</li>
                <li>Ensure right to use and analyse data</li>
                <li>Do not enter sensitive or personal data</li>
                <li>AI may produce inaccurate results; verify findings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Version info
        st.markdown("""
        <div class="container">
            <h3>ℹ️  Version</h3>
            <ul>
                <li>Current Version: 0.1</li>
                <li>Last Updated: 22 Aug 2024</li>
                <li>Streamlit Version: 1.24.0</li>
                <li>Python Version: 3.9.5</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("For support, please contact: 📧 xu_yang@moe.gov.sg, 📧 chan_yu_chyi@moe.gov.sg")


    # Add footnote
    st.markdown("""
    <div class="footnote">
         🌸 This prototype is evolving faster than climate change, fueled by our team's bursts of inspiration (and available time).🐌
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    welcome_page()