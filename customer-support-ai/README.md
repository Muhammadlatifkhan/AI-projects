# Customer Support AI System 
 
## Overview 
An AI-powered customer support system that processes messages and provides three outputs: 
1. **Message Classification** (Complaint, Refund/Return, Sales Inquiry, Delivery Question, Account/Technical Issue, General Query, or Spam) 
2. **Sentiment Analysis** (Positive, Neutral, or Negative) 
3. **Auto-reply Generation** (Professional, context-appropriate responses) 
 
## Features 
- Real-time message processing using Groq AI API 
- Web-based interface built with Flask 
- Clean, responsive UI with CSS styling 
- Fast response generation with LLaMA 3.1 model 
 
## Technology Stack 
- **Backend**: Python, Flask 
- **AI API**: Groq Cloud with LLaMA 3.1 model 
- **Frontend**: HTML, CSS 
- **Deployment**: Local server or cloud-ready 
 
## Project Structure 
\`\`\` 
customer-support-ai/ 
ÃÄÄ main.py              # Flask application 
ÃÄÄ requirements.txt     # Python dependencies 
ÃÄÄ README.md           # This documentation 
ÃÄÄ .gitignore          # Git ignore rules 
ÃÄÄ static/             # CSS styles 
³   ÀÄÄ style.css       # Styling file 
ÀÄÄ templates/          # HTML templates 
    ÀÄÄ index.html      # Web interface 
\`\`\` 
 
## Installation 
 
### 1. Clone the repository 
\`\`\`bash 
git clone https://github.com/YOUR-USERNAME/customer-support-ai.git 
cd customer-support-ai 
\`\`\` 
 
### 2. Create virtual environment 
\`\`\`bash 
python -m venv venv 
venv\Scripts\activate  # On Windows 
# source venv/bin/activate  # On Mac/Linux 
\`\`\` 
 
### 3. Install dependencies 
\`\`\`bash 
pip install -r requirements.txt 
\`\`\` 
 
### 4. Set up Groq API Key 
1. Get API key from [Groq Cloud](https://console.groq.com) 
2. Replace \`api_key\` in \`main.py\` with your key 
 
### 5. Run the application 
\`\`\`bash 
python main.py 
\`\`\` 
 
### 6. Access the system 
Open browser: \`http://localhost:5000\` 
 
## How It Works 
 
### Input Example: 
\`\`\` 
"The product arrived damaged and I need a refund immediately." 
\`\`\` 
 
### Output Format: 
\`\`\` 
Category: Complaint 
Sentiment: Negative 
Auto-Reply: We sincerely apologize for the damaged product... 
\`\`\` 
 
## Author 
Muhammad Latif - Computer Systems Engineer 
 
## License 
MIT License 
