import re

def get_response(message_text):
    msg = message_text.lower().strip()
    
    # Greeting
    if any(word in msg for word in ["hi", "hello", "hey", "salam", "assalam"]):
        return "👋 Welcome to VELOUR! I'm here to help with sizes, prices, delivery, returns, and more. Just ask!"
    
    # Sizing
    if any(word in msg for word in ["size", "sizing", "fit", "measurement", "chest", "waist"]):
        return "📏 VELOUR Size Guide:\nXS: Chest 32-34\", Waist 24-26\"\nS: 34-36\", 26-28\"\nM: 36-38\", 28-30\"\nL: 38-40\", 30-32\"\nXL: 40-42\", 32-34\"\nXXL: 42-44\", 34-36\""
    
    # Pricing
    if any(word in msg for word in ["price", "cost", "rate", "pkr", "rupee", "kitna"]):
        return "💰 VELOUR Prices:\nOversized Tee: PKR 1,800-2,200\nCargo Trousers: PKR 3,500-4,500\nPullover Hoodie: PKR 4,200-5,500\nCord Jacket: PKR 6,000-8,500\nRibbed Polo: PKR 2,400-2,800\nWashed Shorts: PKR 2,200-2,600"
    
    # Delivery
    if any(word in msg for word in ["deliver", "shipping", "ship", "dispatch", "days"]):
        return "🚚 Delivery: Lahore/Karachi/Islamabad: 2-3 days, Other cities: 4-6 days. Flat PKR 200, FREE above PKR 5,000."
    
    # Returns
    if any(word in msg for word in ["return", "exchange", "refund", "wrong size"]):
        return "🔄 Returns: Within 7 days, unworn with tags. Share your order ID to start."
    
    # Payment
    if any(word in msg for word in ["pay", "payment", "jazzcash", "easypaisa", "cod", "cash"]):
        return "💳 Payment: JazzCash, EasyPaisa, Bank Transfer, and Cash on Delivery available."
    
    # New arrivals
    if any(word in msg for word in ["new", "drop", "latest", "restock", "collection"]):
        return "🆕 New collections every Friday! Follow @shopvelour on Instagram for updates."
    
    # Order status
    if any(word in msg for word in ["order", "track", "parcel", "status", "where is"]):
        return "📦 Please share your order ID and I'll check the status for you."
    
    # Fallback
    return "Thanks for your message! Our team will get back to you shortly. For instant updates, follow @shopvelour."