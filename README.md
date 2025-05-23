# Streamlit LLM Application

This project is a Streamlit application that leverages a Large Language Model (LLM) to provide interactive features. Below are the details for setting up and running the application.

## Project Structure

```
streamlit-llm-app
├── app
│   ├── main.py        # Main entry point of the Streamlit application
│   └── utils.py       # Utility functions for data processing and model interaction
├── requirements.txt    # Python dependencies
├── azure-pipelines.yml  # Azure DevOps pipeline configuration
├── Dockerfile           # Instructions to build the Docker image
├── .env                 # Environment variables
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd streamlit-llm-app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add the necessary environment variables, such as API keys.

## Running the Application

To run the Streamlit application, execute the following command:

```bash
streamlit run app/main.py
```

## Deployment

This application can be deployed to Azure Web Apps. Refer to the `azure-pipelines.yml` for the CI/CD pipeline configuration.

## Usage

Once the application is running, you can interact with the LLM through the Streamlit interface. Follow the on-screen instructions to utilize the features provided by the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.