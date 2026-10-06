# 🤖 AI-Powered Business Intelligence Agent

An **AI-powered Business Intelligence Agent** that allows users to ask business questions in natural language and automatically generates **data analysis, insights, visualizations, and recommendations** from structured datasets.

Built with **Python, Streamlit, Pandas, Plotly, and Google Gemini API**.

---

## 🚀 Features

- 💬 Ask business questions using **natural language**
- 🤖 Uses **Google Gemini** to generate data-analysis logic
- 🐍 Automatically generates and executes **Python analysis code**
- 📊 Generates interactive **Plotly visualizations**
- 📈 Displays calculated datasets and business metrics
- 💡 Provides AI-generated **business insights and recommendations**
- 📂 Supports custom **CSV dataset uploads**
- 📋 Includes sample customer and order datasets
- ⚡ Uses Streamlit caching for efficient data loading
- 🔍 Displays generated Python code for transparency and debugging
- 📌 Provides an executive KPI dashboard

---

## 🧠 How It Works

```text
User Business Question
        ↓
Streamlit Interface
        ↓
Google Gemini API
        ↓
AI-Generated Python Analysis
        ↓
Execute Analysis on Dataset
        ↓
┌──────────────┬──────────────┬──────────────┐
│   Insights   │ Visualization│ Calculations │
└──────────────┴──────────────┴──────────────┘
        ↓
Business Recommendations
```

---

## 🛠️ Tech Stack

### Programming
- Python

### AI / GenAI
- Google Gemini API
- Generative AI
- Natural Language Querying
- AI-generated Python analysis

### Data Analytics
- Pandas
- Data Processing
- Data Aggregation
- KPI Analysis

### Visualization
- Plotly
- Interactive Charts

### Application
- Streamlit

### Configuration
- Python-dotenv
- Environment Variables

---

## 📊 Dataset

The application works with two related datasets:

### Customers

Contains customer-related information such as:

- Customer ID
- Customer demographics
- City
- Preferred device
- Age group

### Orders

Contains order-related information such as:

- Order ID
- Customer ID
- Order status
- Delivery city
- Order information

The application merges the datasets before performing analysis.

---

## 💻 Example Questions

Users can ask questions such as:

> Which city generates the highest number of orders?

> What is the distribution of orders by order status?

> What percentage of customers belong to each age group?

> Which preferred device drives the most orders?

The agent analyzes the dataset and returns the relevant **calculation, visualization, and business insight**.

---

## 📁 Project Structure

```text
Bi-Agent/
│
├── data/
│   ├── customers.csv
│   └── orders.csv
│
├── src/
│   ├── agent.py
│   └── data_loader.py
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sneha200421/Bi-Agent.git
cd Bi-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Alternatively, the application allows the Gemini API key to be entered through the Streamlit sidebar.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🎯 Use Cases

This project can be used for:

- 📊 Business Intelligence
- 📈 Sales Analytics
- 👥 Customer Analytics
- 🛒 E-commerce Analytics
- 📋 KPI Monitoring
- 🤖 AI-Assisted Data Analysis
- 💡 Natural Language Business Insights
- 📑 Decision Support

---

## 🌟 Key Highlights

- **Natural Language → Data Analysis**
- **AI-generated analytical code**
- **Automated visualization**
- **Business insight generation**
- **Custom dataset support**
- **Interactive analytics dashboard**

---

## 🔮 Future Improvements

- [ ] SQL database integration
- [ ] Multi-agent architecture
- [ ] Conversational chat history
- [ ] Authentication
- [ ] Automated report generation
- [ ] PDF/Excel report export
- [ ] More advanced statistical analysis
- [ ] Cloud deployment
- [ ] Role-based dashboards
- [ ] Support for larger datasets

---

## 👩‍💻 Author

### Sneha Saini

**B.Tech Computer Science & Engineering**

Interested in **AI Engineering, Data Analytics, Generative AI, and Software Development**.

### 🔗 Links

- GitHub: https://github.com/sneha200421
- Project: https://github.com/sneha200421/Bi-Agent

---

## ⭐ If You Like This Project

Give the repository a ⭐ and feel free to explore, fork, or contribute!

#Python #ArtificialIntelligence #GenerativeAI #GeminiAI #BusinessIntelligence #DataAnalytics #DataScience #MachineLearning #Pandas #Plotly #Streamlit #GenAI #AIEngineering #PythonProjects #DataVisualization #BusinessAnalytics #GitHub #SoftwareDevelopment
