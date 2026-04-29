# VELOUR DM Bot - Instagram Automated Messaging System

An intelligent Instagram DM bot that automatically replies to customer questions for VELOUR clothing brand. Built with Python, Flask, and Meta's Graph API.

## 🚀 Features

- ✅ **Real-time DM processing** - Instantly responds to customer messages
- ✅ **Smart keyword detection** - Matches customer questions to relevant responses
- ✅ **24/7 operation** - Never misses a customer inquiry
- ✅ **Multi-language support** - Handles both English and Urdu mixed text
- ✅ **Complete brand integration** - Contains VELOUR's products, pricing, and policies

## 📋 Response Capabilities

| Topic | Keywords | Response |
|-------|----------|----------|
| Greeting | hi, hello, salam | Welcome message with bot capabilities |
| Sizing | size, fit, chest | Complete size chart XS-XXL |
| Pricing | price, cost, PKR | Full product price ranges |
| Delivery | shipping, delivery time | City-wise delivery timelines |
| Returns | return, exchange | 7-day return policy details |
| Payment | jazzcash, easypaisa, COD | All accepted payment methods |

## 🛠️ Tech Stack

- **Backend:** Python 3.11+, Flask
- **API:** Meta Graph API v18.0, Instagram Messenger API
- **Tunneling:** ngrok (development)
- **Deployment:** Railway / Render (production ready)

## 📁 Project Structure

```
velour-dm-bot/
├── app.py              # Main Flask server & webhook handler
├── responses.py        # Keyword matching & response logic
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
└── README.md          # Project documentation
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8+
- Instagram Business Account
- Facebook Developer Account
- ngrok account (free)

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/velour-dm-bot.git
cd velour-dm-bot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Environment Variables

Create `.env` file:

```env
IG_ACCESS_TOKEN=your_page_access_token_here
IG_ACCOUNT_ID=your_instagram_account_id
VERIFY_TOKEN=VELOUR_VERIFY_123
```

### Step 4: Run Flask Server

```bash
python app.py
```

### Step 5: Expose with ngrok

```bash
ngrok http 5000
```

### Step 6: Configure Meta Webhook

Set callback URL to: `https://your-ngrok-url.ngrok.io/webhook`

## 📊 VELOUR Brand Data

### Product Price Range

| Product | Price (PKR) | Sizes |
|---------|-------------|-------|
| Oversized Tee | 1,800 – 2,200 | XS-XXL |
| Cargo Trousers | 3,500 – 4,500 | S-XL |
| Pullover Hoodie | 4,200 – 5,500 | S-XXL |
| Cord Jacket | 6,000 – 8,500 | M-XL |
| Ribbed Polo | 2,400 – 2,800 | S-XL |
| Washed Shorts | 2,200 – 2,600 | S-XL |

### Delivery Policy

- Lahore, Karachi, Islamabad: 2-3 working days
- Other cities: 4-6 working days
- Flat rate: PKR 200
- Free shipping: Orders above PKR 5,000

## 🧪 Testing

Send these test messages to your Instagram Business account:

| Message | Expected Response |
|---------|-------------------|
| "Hello" | Welcome message |
| "Size guide" | XS-XXL measurements |
| "Hoodie price" | PKR 4,200 – 5,500 |
| "Delivery to Karachi" | 2-3 days, PKR 200 |
| "Return policy" | 7-day return window |

## 📝 Webhook Flow

1. Customer sends DM to Instagram Business account
2. Meta forwards message to your webhook (POST request)
3. Flask server processes message and extracts text
4. Keyword matching identifies intent
5. Appropriate response is generated
6. Reply sent back via Graph API
7. Customer receives auto-reply

## 🔒 Security

- ✅ Access tokens stored in `.env` (never committed)
- ✅ Webhook verification token validation
- ✅ HTTPS via ngrok (production: use SSL)
- ✅ `.gitignore` configured for sensitive files

## 🚀 Deployment

### Deploy to Railway (Recommended)

1. Push code to GitHub
2. Connect repository to Railway
3. Add environment variables
4. Deploy automatically

### Deploy to Render

```bash
# Create render.yaml or use web dashboard
# Set start command: gunicorn app:app
```

## 📈 Future Enhancements

- [ ] Integrate Groq AI for natural language understanding
- [ ] Add database for conversation history
- [ ] Implement sentiment analysis
- [ ] Multi-brand support
- [ ] Analytics dashboard

## 🤝 Contributing

This project was completed as part of an AI development internship. For questions or suggestions, please open an issue.

## 📧 Contact

**Developer:** Muhammad Latif  
**Email:** laahmad7777@gmail.com
**GitHub:** **GitHub:** [Muhammadlatifkhan](https://github.com/Muhammadlatifkhan)

## 📄 License

This project is for portfolio/demonstration purposes.

---

## 🎯 Project Status

✅ **COMPLETE** - All core functionality implemented and tested

- Webhook integration: ✅ Working
- DM reception: ✅ Working  
- Response generation: ✅ Working
- Auto-reply sending: ⏳ Awaiting Meta approval

*The bot successfully receives and processes all DMs. Reply sending requires Meta's business verification for production use.*

---

**Built with Python, Flask, and Meta Graph API** | 6th AI Project
