To accomplish this task, we'll need to use several classes and modules effectively. We'll also configure Streamlit for deployment and use AWS Rekognition for facial analysis. I'll provide Python code for this application with detailed docstrings, logging, and proper class structure. 

1. **AWS Rekognition Handler for Facial Analysis**
2. **Streamlit App for User Interaction**
3. **Command-Line Argument Parsing**

Here's a sequence of steps to achieve the functionality:

1. **Set up AWS Rekognition for facial analysis.**
2. **Set up Streamlit for user interaction and file input.**
3. **Handle facial analysis and display results.**
4. **Use appropriate logging throughout the application.**

Here’s the code implementation:

### awsrekognition.py

```python
import boto3
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class RekognitionHandler:
    """
    A class to handle AWS Rekognition operations including facial analysis.

    Attributes:
        client (boto3.client): A Boto3 Rekognition client.
    """
    
    def __init__(self):
        """Initializes the RekognitionHandler by creating a client."""
        self.client = boto3.client('rekognition')
        logging.info("Initialized Rekognition client.")

    def analyze_emotions(self, image_bytes: bytes) -> List[Dict]:
        """
        Analyzes emotions in an image using AWS Rekognition.

        Args:
            image_bytes (bytes): The image data in bytes.

        Returns:
            List[Dict]: A list of dictionaries containing emotion data for each face detected.
        """
        try:
            response = self.client.detect_faces(
                Image={'Bytes': image_bytes},
                Attributes=['ALL']
            )
            emotions = [
                {'Confidence': face_detail['Confidence'], 'Emotions': face_detail['Emotions']}
                for face_detail in response['FaceDetails']
            ]
            logging.info("Successfully analyzed emotions.")
            return emotions
        except Exception as e:
            logging.error(f"Error analyzing emotions: {e}")
            return []
```

### streamlit_app.py

```python
import streamlit as st
import logging
from awsrekognition import RekognitionHandler
from argparse import ArgumentParser

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class StreamlitEmotionsApp:
    """
    A class to create and run a Streamlit app for analyzing emotions in images using AWS Rekognition.

    Attributes:
        rekognition_handler (RekognitionHandler): The RekognitionHandler instance for processing images.
    """
    
    def __init__(self):
        """Initializes the StreamlitEmotionsApp with a RekognitionHandler instance."""
        self.rekognition_handler = RekognitionHandler()

    def upload_and_analyze_image(self):
        """
        Interface for uploading an image and analyzing emotions.
        """
        st.title("Emotion Analysis using AWS Rekognition")
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            image_bytes = uploaded_file.read()
            emotions = self.rekognition_handler.analyze_emotions(image_bytes)
            
            if emotions:
                for idx, face in enumerate(emotions):
                    st.write(f"Face {idx + 1}:")
                    st.write(f"Confidence: {face['Confidence']}")
                    st.write("Emotions:")
                    for emotion in face['Emotions']:
                        st.write(f"  - {emotion['Type']}: {emotion['Confidence']}")
                logging.info("Displayed emotions for uploaded image.")
            else:
                st.write("No faces detected.")
                logging.warning("No faces detected in uploaded image.")

    def run(self):
        """Runs the Streamlit application."""
        self.upload_and_analyze_image()

def main():
    parser = ArgumentParser(description="Streamlit App for AWS Rekognition Emotion Analysis")
    args = parser.parse_args()

    app = StreamlitEmotionsApp()
    app.run()

if __name__ == "__main__":
    main()
```

### `.streamlit/secrets.toml`
Add your AWS credentials in the `.streamlit/secrets.toml` to access AWS Rekognition:

```toml
[aws]
aws_access_key_id = "YOUR_ACCESS_KEY"
aws_secret_access_key = "YOUR_SECRET_KEY"
region_name = "YOUR_REGION"
```

Make sure you have the following dependencies installed:

```shell
pip install streamlit boto3 pandas
```

### Running the Application

You can run the main Streamlit app using:

```bash
streamlit run streamlit_app.py
```

### UML Sequence Diagram

Here’s a simple UML Sequence Diagram for the flow:

```plaintext
Client -> StreamlitEmotionsApp -> RekognitionHandler -> Rekognition (AWS API) 
```

1. **Client uploads the image** on the Streamlit interface.
2. **StreamlitEmotionsApp** handles the upload and passes the image bytes to RekognitionHandler.
3. **RekognitionHandler** uses AWS Rekognition API to analyze the image and return emotion data.
4. The **results are displayed** on the Streamlit interface.

This code provides a structured approach using OOP and best practices in Python, including detailed docstrings, logging, and argument parsing. The diagram represents how data flows through the application, starting from the user (client) interaction to the final display of emotions detected by AWS Rekognition.