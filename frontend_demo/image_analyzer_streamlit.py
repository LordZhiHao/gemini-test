import streamlit as st
import requests
import base64
from PIL import Image
import io

def main():
    st.set_page_config(
        page_title="Nutrition Image Analyzer",
        page_icon="🍽️",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stImage {
            border-radius: 10px;
        }
        .analysis-box {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("🍽️ Nutrition Image Analyzer")
    st.markdown("Upload a food image to get detailed nutritional analysis")

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image...", 
            type=['jpg', 'jpeg', 'png'],
            help="Upload a food image (JPG or PNG format, max 5MB)"
        )

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Add analyze button
            if st.button("Analyze Image", type="primary"):
                with st.spinner("Analyzing image..."):
                    try:
                        # Prepare the file for API request
                        files = {
                            'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                        }
                        
                        # Make API request
                        response = requests.post(
                            'http://localhost:8000/analyze-image',
                            files=files
                        )
                        
                        if response.status_code == 200:
                            analysis_result = response.json()['analysis']
                            
                            with col2:
                                st.markdown("### Analysis Results")
                                st.markdown(
                                    f"""
                                    <div class="analysis-box">
                                        {analysis_result}
                                    </div>
                                    """, 
                                    unsafe_allow_html=True
                                )
                        else:
                            st.error(f"Error: {response.json()['detail']}")
                            
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

    # Add information about the app
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Upload a food image using the file uploader
    2. Click the 'Analyze Image' button
    3. Wait for the analysis results
    
    ### Features:
    - Supports JPG and PNG images
    - Maximum file size: 5MB
    - Provides detailed nutritional analysis
    """)

    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and FastAPI")

if __name__ == "__main__":
    main()