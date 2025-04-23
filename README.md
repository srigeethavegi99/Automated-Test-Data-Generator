# Automated-Test-Data-Generator
🎯 Automated Test Data Generator

 🔍 Overview
The Automated Test Data Generator is a comprehensive tool designed to streamline the creation of high-quality, adaptable synthetic test data for various development and testing scenarios. By combining a user-friendly Streamlit interface with the power of Large Language Models (LLMs) and LocalStack for AWS simulation, this tool offers a secure, cost-effective solution for generating realistic test datasets.

 🚀 Purpose
This project addresses a common challenge in software development: creating realistic test data efficiently and securely. By leveraging AI capabilities to generate customized data scripts and simulating cloud services locally, the tool eliminates the expenses associated with using real AWS services while enhancing security by keeping sensitive testing within a controlled environment.

 ✨ Key Features
- **🤖 AI-Powered Script Generation**: Uses LLMs to create customized data generation scripts based on user specifications
- **☁️ Local AWS Simulation**: Implements LocalStack to provide a simulated AWS environment without cloud costs
- **🖥️ User-Friendly Interface**: Built with Streamlit for intuitive operation and visualization
- **🔧 Customizable Data Generation**: Supports various data types and constraints to meet specific testing requirements
- **🔒 Secure Testing Environment**: Enables comprehensive testing without risking exposure of sensitive data

## 🛠️ Technology Stack
- **🎨 Frontend**: Streamlit
- **⚙️ Backend**: Python, Faker library
- **🧠 AI Integration**: Large Language Models
- **☁️ Cloud Simulation**: LocalStack (AWS services simulation)

## 🎯 Problems Solved
- **💰 Cost Reduction**: Eliminates expenses associated with using real cloud services for testing
- **🧩 Complexity Management**: Automates the creation of realistic test data, reducing manual effort
- **🛡️ Security Enhancement**: Keeps testing within a controlled local environment
- **🔍 Testing Thoroughness**: Facilitates comprehensive testing without affecting production resources

# Getting Started with Automated Test Data Generator

This guide will help you set up and start using the Automated Test Data Generator on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Docker (for running LocalStack)

## Installation

###  Clone the repository

```bash
git clone https://github.com/srigeethavegi99/automated-test-data-generator.git
cd automated-test-data-generator
```

### Install dependencies

```bash
pip install streamlit
pip install boto3
pip install aws-cli
```

### Set up LocalStack

Pull and run the LocalStack Docker image:
Open Docker in Desktop and keep it running
```bash
localstack start -d
```

### Configure environment variables

Create a `.env` file in the project root directory:


## Running the Application

Start the Streamlit application:

```bash
streamlit run main.py
```

## Basic Usage

1. **Configure Data Schema**: Define the structure of your test data using the intuitive UI
2. **Set Parameters**: Specify the amount and characteristics of the data you need
3. **Generate Data**: Click the "Generate" button to create your synthetic dataset
4. **Export Options**: Download your data in .CSV or store directly in the simulated AWS services

**LLM Integration Problems**:
- Ensure your API key is correctly set in the `.env` file
- Check your internet connection as LLM services require online access

### Tools and Libraries

- [Streamlit](https://streamlit.io/) - Used for creating the web interface
- [LocalStack](https://localstack.cloud/) - AWS service emulation for local development
- [Faker](https://faker.readthedocs.io/) - Python library for generating fake data
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - For AWS service interaction

### Learning Resources

- [AWS Official Documentation](https://docs.aws.amazon.com/)
- [LocalStack GitHub Repository](https://github.com/localstack/localstack)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Faker Documentation](https://faker.readthedocs.io/en/master/)
- [Python Data Generation Patterns](https://realpython.com/generating-random-data-in-python/)

## 👥 Target Users
- 👨‍💻 Software Developers
- 🧪 QA Engineers
- 📊 Data Scientists
- 🤖 Machine Learning Engineers

## 📚 Learning Outcomes
Through developing this project, I gained experience in:

- **🔢 Synthetic Data Generation**: Deep understanding of techniques for creating realistic simulated data
- **🤖 AI Integration**: Practical implementation of LLMs within a web application context
- **☁️ Cloud Service Simulation**: Expertise in using LocalStack to replicate AWS functionality locally
- **📋 Requirements Engineering**: Application of formal requirements gathering and specification techniques 
- **🏗️ System Architecture Design**: Creation of a modular, scalable system that integrates multiple technologies
- **📊 Data Visualization**: Implementation of intuitive visualizations to represent complex datasets
- **🌐 Web Application Development**: Full-stack integration of frontend and backend components

## 🎓 Academic Foundations
This project builds upon knowledge gained from several graduate-level Computer Science courses:
- **🔷 CIS 500 (Fundamentals of Software Practice)**: Applied software development principles and Python expertise
- **🔷 CIS 612 (Requirements Specification)**: Utilized structured requirements gathering to ensure clear project scope
- **🔷 CIS 671 (Information Visualization)**: Implemented visualization concepts to enhance data representation
- **🔷 CIS 658 (Web Architectures)**: Leveraged principles of robust web application design for system integration

## 🔮 Next Steps
- 🔄 Integration with additional data sources
- 🔗 Support for more complex data relationships
- 📈 Enhanced visualization options
- 🌩️ Expanded cloud service simulations

---

*This project demonstrates the practical application of advanced computer science concepts to solve real-world testing challenges while highlighting the benefits of using simulated environments for development and testing purposes.*
