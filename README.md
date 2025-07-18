# 🌱 Sustainability Training AI

**AI-Powered Training for Compliant Sustainability Messaging**

An intelligent training platform that uses multiple AI agents to create personalized sustainability communication courses, helping marketing professionals avoid greenwashing and ensure regulatory compliance.

![startwindow](https://github.com/Yosolita1978/screenshoots/blob/2af77d31415283f654208d776053677795c6abb6/2025/Screenshot%202025-07-18%20at%2012.00.54.png)
![firstmessage](https://github.com/Yosolita1978/screenshoots/blob/2af77d31415283f654208d776053677795c6abb6/2025/Screenshot%202025-07-18%20at%2012.01.30.png)
![downloadreport](https://github.com/Yosolita1978/screenshoots/blob/2af77d31415283f654208d776053677795c6abb6/2025/Screenshot%202025-07-18%20at%2012.03.47.png)
![finalReport](https://github.com/Yosolita1978/screenshoots/blob/2af77d31415283f654208d776053677795c6abb6/2025/Screenshot%202025-07-18%20at%2012.04.31.png)

## 🎯 Overview

The Sustainability Training AI is a sophisticated web application that leverages multi-agent AI systems to deliver personalized training on sustainability messaging compliance. It automatically researches current market trends, regulatory requirements, and real-world examples to create comprehensive training materials tailored to your industry and role.

### Key Features

- **🤖 Multi-Agent AI System**: Four specialized AI agents work together to create comprehensive training content
- **🔍 Real-Time Research**: Searches current sustainability trends and regulatory updates
- **📊 Personalized Content**: Tailored scenarios based on your industry and regional regulations
- **⚠️ Greenwashing Detection**: Identifies problematic messaging patterns with detailed explanations
- **✅ Compliance Guidance**: Provides corrected alternatives following current best practices
- **📝 Assessment Tools**: Generates knowledge-testing questions with detailed explanations
- **📄 Professional Reports**: Comprehensive markdown reports ready for PDF conversion
- **🌐 Web Interface**: User-friendly Panel-based interface for easy configuration and monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ 
- OpenAI API key
- Serper API key (for web search)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sustainability-training-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application:**
   ```bash
   panel serve app.py --port=5007 --show
   ```

5. **Access the web interface:**
   Open `http://localhost:5007` in your browser

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following required variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

Optional variables:
```env
DEEPSEEK_API_KEY=your_deepseek_key  # Alternative LLM
GOOGLE_API_KEY=your_google_key      # Alternative search
```

### User Preferences

Customize your training profile in `knowledge/user_preference.txt`:

```
USER_PROFILE:
Name: Your Name
Role: Marketing Director
Company_Type: Your Company Type
Location: Your Region
Industry_Focus: Your Target Industries

SUSTAINABILITY_TRAINING_PREFERENCES:
Experience_Level: Beginner/Intermediate/Advanced
Primary_Interest: Your Training Focus
Training_Goal: Your Objectives
```

## 🎓 How It Works

### The Four-Agent System

1. **🏢 Scenario Builder Agent**
   - Researches current market trends
   - Creates realistic business scenarios
   - Incorporates industry-specific context

2. **⚠️ Mistake Illustrator Agent** 
   - Finds real greenwashing examples
   - Identifies problematic messaging patterns
   - Explains regulatory violations

3. **✅ Best Practice Coach Agent**
   - Researches successful sustainability communications
   - Transforms problematic messages into compliant alternatives
   - Provides regulatory compliance guidance

4. **📝 Assessment Agent**
   - Creates knowledge-testing questions
   - Generates comprehensive training reports
   - Provides personalized feedback and recommendations

### Training Process

1. **Configure** your industry focus and regulatory framework
2. **Start Training** - AI agents begin collaborative research and content creation
3. **Monitor Progress** - Real-time updates show agent activities and discoveries
4. **Review Results** - Comprehensive training materials with scenarios, corrections, and assessments
5. **Download Reports** - Professional markdown reports ready for PDF conversion

## 🌍 Supported Industries & Regulations

### Industries
- Marketing & Communications Agencies
- Consumer Goods & Retail
- Fashion & Apparel
- Food & Beverage
- Technology & Software
- Financial Services
- Healthcare & Pharmaceuticals
- Energy & Utilities
- Automotive
- Real Estate

### Regulatory Frameworks
- **EU**: Green Claims Directive, CSRD (Corporate Sustainability Reporting Directive)
- **US**: FTC Green Guides
- **UK**: CMA Guidelines
- **Canada**: Competition Bureau Guidelines
- **Australia**: ACCC Guidelines
- **Global**: Best Practices Compilation

## 🏗️ Architecture

### Technology Stack

- **🔧 Backend Framework**: CrewAI for multi-agent orchestration
- **🌐 Web Interface**: Panel for interactive web applications
- **🤖 AI Models**: OpenAI GPT-4o, GPT-4o-mini
- **🔍 Web Search**: Serper API for real-time research
- **📊 Data Validation**: Pydantic for structured outputs
- **☁️ Deployment**: Render-ready with Docker support

### Project Structure

```
sustainability-training-ai/
├── src/sustainability/           # Core application
│   ├── config/                  # Agent and task configurations
│   ├── tools/                   # Custom search and utility tools
│   ├── crew.py                  # Multi-agent system definition
│   ├── panel_bridge.py          # Web interface implementation
│   └── callbacks.py             # Real-time progress tracking
├── knowledge/                   # User preferences and training data
├── outputs/                     # Generated reports and results
├── requirements.txt             # Python dependencies
├── app.py                      # Production web entry point
└── render.yaml                 # Deployment configuration
```

## 🚀 Deployment

### Render Deployment (Recommended)

1. **Connect your repository** to Render
2. **Set environment variables** in Render dashboard:
   - `OPENAI_API_KEY`
   - `SERPER_API_KEY`
3. **Deploy** using the included `render.yaml` configuration

The application will automatically deploy and be accessible via your Render URL.

### Local Development

```bash
# Development server with auto-reload
panel serve panel_app.py --dev --show

# Production-like server
panel serve app.py --port=5007 --allow-websocket-origin=*
```

## 📊 Sample Output

### Training Report Includes:

- **📋 Executive Summary**: Overview of training objectives and outcomes
- **🏢 Business Scenario**: Realistic company context with sustainability challenges  
- **⚠️ Problematic Messages**: Examples with detailed regulatory analysis
- **✅ Corrected Alternatives**: Compliant messaging with best practice explanations
- **📝 Knowledge Assessment**: 5-7 practical questions testing understanding
- **🎯 Personalized Feedback**: Role-specific tips and implementation strategies
- **📋 Compliance Checklist**: Step-by-step verification guidelines

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for:

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🌍 Additional regulatory frameworks
- 🏭 New industry focus areas

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- **📖 Documentation**: Check this README and inline code comments
- **🐛 Issues**: Open a GitHub issue for bugs or feature requests
- **💬 Discussions**: Join our community discussions for questions

### API Requirements

- **OpenAI API**: GPT-4o access recommended for best results
- **Serper API**: For real-time web search and market research

---

**🌱 Built with sustainability in mind - helping organizations communicate their environmental commitments with confidence and compliance.**

For more information, visit our [documentation](docs/) or [contact the development team](mailto:contact@example.com).