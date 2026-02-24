# 💎 Data Intelligence Dashboard

A high-performance, premium Streamlit dashboard for professional data analytics. This project provides deep-dive insights, interactive visualizations, and real-time processing of CSV datasets.

## 🚀 Features

- **Key Performance Indicators (KPIs)**: Instantly track Unique Users, Sessions, Conversion Rates, and Engagement.
- **Interactive Visualizations**: Powered by Plotly, including:
  - Traffic Source Distribution (Pie Chart)
  - Device Usage (Bar Chart)
  - Engagement Trends (Area Chart)
  - Regional Footprint (Horizontal Bar Chart)
  - Page Popularity Map (Treemap)
- **User behavior Funnel**: Analyze conversion rates by user status.
- **Data Inspector**: View and download the processed dataset.
- **Premium UI/UX**: Custom CSS styling with glassmorphism effects, hover animations, and a modern typography (Inter).

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/SMA_Dashboard.git
   cd SMA_Dashboard
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📈 Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run dashboard.py
   ```

2. **Upload your dataset**:
   - Use the sidebar to upload a CSV file.
   - If you don't have one, you can generate a sample dataset using the provided Jupyter notebook `Generate_info.ipynb`.

## 📁 Project Structure

- `dashboard.py`: The main Streamlit application.
- `Generate_info.ipynb`: A utility notebook to create synthetic professional datasets.
- `analytics_dataset.csv`: Sample dataset (generated).
- `requirements.txt`: List of Python dependencies.
- `.gitignore`: Files and directories to ignore in Git.

## 🛡️ License

This project is open-source and available under the MIT License.

---
Built with ❤️ by [Your Name]
