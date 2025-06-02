import streamlit as st
import qrcode
from io import BytesIO
import base64
import time

# Set page config
st.set_page_config(
    page_title="Dragon 80 Ate - Digital Menu",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Restaurant-style CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #8B0000, #A0522D, #8B0000);
        color: #FFD700;
    }
    
    .stApp {
        background: linear-gradient(135deg, #8B0000, #A0522D, #8B0000);
    }
    
    .restaurant-header {
        background: linear-gradient(135deg, #8B0000, #DC143C, #8B0000);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #FFD700;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .restaurant-title {
        font-family: 'Brush Script MT', cursive;
        font-size: 4rem;
        color: #FFD700;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin-bottom: 0.5rem;
    }
    
    .restaurant-subtitle {
        font-size: 1.5rem;
        color: #FFF8DC;
        letter-spacing: 3px;
        margin-bottom: 1rem;
    }
    
    .menu-section {
        background: linear-gradient(135deg, #8B0000, #A0522D);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #FFD700;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    
    .section-title {
        font-size: 2.5rem;
        color: #FFD700;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-bottom: 3px solid #FFD700;
        padding-bottom: 0.5rem;
    }
    
    .menu-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        background: rgba(139, 0, 0, 0.3);
        border-radius: 5px;
        border-left: 4px solid #FFD700;
    }
    
    /* MODIFIED: Item Name Styling */
    .item-name {
        color: #FFD700; /* Changed color to match section title and borders */
        font-size: 1.1rem;
        font-weight: bold; /* Made bold */
    }
    
    .item-price {
        color: #FFD700;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .dragon-emoji {
        font-size: 3rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .contact-info {
        background: rgba(139, 0, 0, 0.8);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #FFD700;
        color: #FFF8DC;
        text-align: center;
    }
    
    .stSelectbox > div > div {
        background-color: #8B0000;
        color: #FFD700;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #8B0000;
        border: 2px solid #8B0000;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFA500, #FFD700);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }

    /* Additional styles for scanner interface */
    .scanner-header {
        background: linear-gradient(135deg, #A0522D, #8B0000);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #FFD700;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .scanner-title {
        font-family: 'Brush Script MT', cursive;
        font-size: 3.5rem;
        color: #FFD700;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin-bottom: 0.5rem;
    }
    
    .scanner-subtitle {
        font-size: 1.2rem;
        color: #FFF8DC;
        letter-spacing: 2px;
    }

    .scanner-status {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
    }

    .status-ready {
        background-color: rgba(60, 179, 113, 0.7); /* MediumSeaGreen with transparency */
        color: white;
    }

    .status-scanning {
        background-color: rgba(255, 165, 0, 0.7); /* Orange with transparency */
        color: white;
    }

    .status-success {
        background-color: rgba(34, 139, 34, 0.7); /* ForestGreen with transparency */
        color: white;
    }

    .camera-container {
        margin-top: 2rem;
        border: 2px dashed #FFD700;
        border-radius: 20px;
        overflow: hidden;
        position: relative;
    }

    .camera-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(
            45deg,
            rgba(255,255,255,0.1),
            rgba(255,255,255,0.1) 10px,
            transparent 10px,
            transparent 20px
        );
        z-index: 1;
    }

    /* Menu specific styles for the actual menu display */
    .menu-container {
        padding: 2rem;
        background: linear-gradient(135deg, #8B0000, #A0522D, #8B0000);
        border-radius: 15px;
        border: 3px solid #FFD700;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .menu-title {
        font-family: 'Brush Script MT', cursive;
        font-size: 4.5rem;
        color: #FFD700;
        text-align: center;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.6);
        margin-bottom: 0.5rem;
    }

    .menu-subtitle {
        font-size: 2rem;
        color: #FFF8DC;
        text-align: center;
        letter-spacing: 4px;
        margin-bottom: 1rem;
    }

    .menu-tagline {
        font-size: 1.2rem;
        color: #FFF8DC;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }

    .section-header {
        font-size: 2.2rem;
        color: #FFD700;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-bottom: 3px solid #FFD700;
        padding-bottom: 0.5rem;
    }

    .item-code {
        color: #FFA500; /* Orange for codes, stands out */
        font-weight: bold;
        margin-right: 8px;
    }

    .footer-text {
        color: #FFF8DC;
        text-align: center;
        margin-top: 2rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }

</style>
""", unsafe_allow_html=True)

# Initializer for restaurant info (though not directly used in the current display functions)
class RestaurantInfo:
    def __init__(self):
        self.restaurant_name = "Dragon 80 Ate"
        self.tagline = "A Taste of Comfort"
        self.contact_info = {
            "website": "www.Dragon80Ate.com",
            "phone": "403-272-8701",
            "address": "2408 17 Avenue South East, Calgary, Alberta T2A0B6"
        }
# Menu data
menu_sections = [
    {
        "title": "APPETIZERS",
        "items": [
            {"name": "Vegetable Spring Roll (2pc)", "price": "$4.50"},
            {"name": "Egg Roll (2pc)", "price": "$4.50"},
            {"name": "Lollipop Chicken (8pc)", "price": "$14.98"},
            {"name": "Deep Fried Wings Salt & Pepper or Honey Garlic or Hot & Spicy (10)", "price": "$14.98"},
            {"name": "Pan Fried Dumplings (8)", "price": "$11.98"},
            {"name": "Chinese Style Deep Fried Wings (10)", "price": "$14.98"},
            {"name": "Deep Fried Wontons", "price": "$11.99"},
            {"name": "Vegetable or Chicken Momos (Steamed Dumpling)", "price": "$14.98"},
            {"name": "Fish Pakora", "price": "$15.98"},
            {"name": "Chicken or Paneer Pakora", "price": "$14.98"},
            {"name": "Steam Edamame Beans", "price": "$5.98"},
            {"name": "Prawn Crackers", "price": "$4.98"},
            {"name": "French Fries", "price": "$6.99"}
        ]
    },
    {
        "title": "SOUP AND SIZZLING RICE",
        "items": [
            {"code": "SP1", "name": "Wonton Soup (4pc)", "price": "$5.50 / $9.00"},
            {"code": "SP2", "name": "Wor Wonton Soup", "price": "$11.00 / $15.00"},
            {"code": "SP3", "name": "Chicken Corn Soup", "price": "$10.00 / $15.00"},
            {"code": "SP4", "name": "Crab Corn Soup", "price": "$10.00 / $16.00"},
            {"code": "SP5", "name": "Vegetable Corn Soup", "price": "$10.00 / $16.00"},
            {"code": "SP6", "name": "Hot and Sour Soup (Chicken or Vegetable or Shrimp +$2)", "price": "$10.00 / $15.00"},
            {"code": "SP7", "name": "Mixed Seafood Tofu Soup", "price": "$11.00 / $17.00"},
            {"code": "SP8", "name": "Manchurian Soup (Chicken or Vegetable or Shrimp +$2)", "price": "$11.00 / $17.00"},
            {"code": "SP9", "name": "Fish Maw Soup", "price": "$15.00 / $22.00"},
            {"code": "SP10", "name": "Hot and Sour Soup on Sizzling Rice (One Size)", "price": "$13.88"}
        ]
    },
    {
        "title": "Seafood",
        "items": [
            { "code": "S1", "name": "Steam Fish (Boneless)", "price": "$28.00" },
            { "code": "S2", "name": "Ginger Fish or Ginger Squid", "price": "$17.00" },
            { "code": "S3", "name": "Celashor Chilli Prawns Hakka Style", "price": "$17.00" },
            { "code": "S4", "name": "Ginger Prawns (12)", "price": "$17.00" },
            { "code": "S5", "name": "Palace Style Prawns (12)", "price": "$17.00" },
            { "code": "S6", "name": "Sweet & Sour Pineapple Prawns", "price": "$17.00" },
            { "code": "S7", "name": "Prawns with Broccoli (12)", "price": "$17.00" },
            { "code": "S8", "name": "Deep Fried Prawns", "price": "$17.00" },
            { "code": "S9", "name": "Prawns with Snow Peas (12)", "price": "$17.00" },
            { "code": "S10", "name": "Lemon Prawns (12)", "price": "$17.00" },
            { "code": "S11", "name": "Salt and Pepper Prawns (12)", "price": "$17.00" },
            { "code": "S12", "name": "Prawns in Black Bean Sauce (12)", "price": "$17.00" },
            { "code": "S13", "name": "Manchutian Fish or Prawns", "price": "$17.00" },
            { "code": "S14", "name": "Salt and Pepper Squid or Fish", "price": "$17.00" },
            { "code": "S15", "name": "Sweet & Sour Fish", "price": "$17.00" },
            { "code": "S16", "name": "Shrimp with Cashew Nuts & Yellow Beans", "price": "$17.00" },
            { "code": "S17", "name": "Prawns with Mixed Vegetables (12)", "price": "$17.00" },
            { "code": "S18", "name": "Curry Prawns with Greens (12)", "price": "$17.00" },
            { "code": "S19", "name": "Prawns with Baby Corn and Mushrooms (12)", "price": "$17.00" },
            { "code": "S20", "name": "Prawns or Fish with Szechuan Sauce", "price": "$17.00" },
            { "code": "S21", "name": "Salt & Pepper with 3 Kinds of Seafood", "price": "$17.00" },
            { "code": "S22", "name": "Ginger and Scallions Prawns or Fish", "price": "$18.00" }
        ]
},
{
  "title": "CHICKEN",
  "items": [
    {"name": "Almond Soo Gai (Almond Chicken)", "price": "$15.00"},
    {"name": "Sliced Chicken with Snow Peas", "price": "$16.00"},
    {"name": "Mushroom with Chicken", "price": "$15.00"},
    {"name": "Sliced Chicken with Curry Sauce", "price": "$15.00"},
    {"name": "Orange Chicken", "price": "$15.00"},
    {"name": "Sliced Chicken in Black Bean Sauce", "price": "$16.00"},
    {"name": "Sliced Chicken in Black Pepper Sauce", "price": "$16.00"},
    {"name": "Sliced Chicken with Mushrooms and Baby Corn", "price": "$15.00"},
    {"name": "Honey Lemon Sliced Chicken", "price": "$15.00"},
    {"name": "Sweet & Sour Chicken Balls", "price": "$16.00"},
    {"name": "Chilli Chicken Not Spicy", "price": "$16.00"}
  ]
},
{
  "title": "BEEF",
  "items": [
    {"code": "B1", "name": "Ginger Beef", "price": "$16.00"},
    {"code": "B2", "name": "Beef in Oyster Sauce", "price": "$16.00"},
    {"code": "B3", "name": "Beef with Broccoli", "price": "$16.00"},
    {"code": "B4", "name": "Beef with Szechuan Sauce", "price": "$16.00"},
    {"code": "B5", "name": "Beef with Snow Peas Pod", "price": "$16.00"},
    {"code": "B6", "name": "Chilli Beef Hakka Style", "price": "$16.00"},
    {"code": "B7", "name": "Beef with Mixed Vegetables", "price": "$16.00"},
    {"code": "B8", "name": "Kung Pao Beef", "price": "$16.00"},
    {"code": "B9", "name": "Beef with Fresh Mushrooms", "price": "$16.00"},
    {"code": "B10", "name": "Beef with Mushroom and Baby Corn", "price": "$16.00"},
    {"code": "B11", "name": "Curry Beef with Greens", "price": "$16.00"},
    {"code": "B12", "name": "Beef in Satay Sauce", "price": "$16.00"},
    {"code": "B13", "name": "Garlic Beef (Sizzler)", "price": "$16.00"}
  ]
},

   {
  "title": "CHICKEN", # Second Chicken section (with codes)
  "items": [
    {"code": "C1", "name": "Sweet & Sour Chicken (Pineapple Optional)", "price": "$15.00"},
    {"code": "C2", "name": "Palace Style Chicken", "price": "$15.00"},
    {"code": "C3", "name": "Chicken with Szechuan Sauce", "price": "$15.00"},
    {"code": "C4", "name": "Ginger Chicken", "price": "$15.00"},
    {"code": "C5", "name": "Sliced Chicken with Broccoli", "price": "$15.00"},
    {"code": "C6", "name": "Diced Mixed Vegetables with Chicken and Almonds", "price": "$15.00"},
    {"code": "C7", "name": "Lemon Chicken", "price": "$15.00"},
    {"code": "C8", "name": "Manchurian Chicken Hakka Style", "price": "$15.00"},
    {"code": "C9", "name": "General Tso’s Chicken", "price": "$15.00"},
    {"code": "C10", "name": "Chili Chicken Hakka Style", "price": "$15.00"},
    {"code": "C11", "name": "Sliced Chicken with 2 Kinds of Mushrooms", "price": "$15.00"},
    {"code": "C12", "name": "Sliced Chicken with Mixed Vegetables", "price": "$15.00"},
    {"code": "C13", "name": "Kung Pao Chicken", "price": "$15.00"},
    {"code": "C14", "name": "Salt & Pepper Chicken", "price": "$15.00"},
    {"code": "C15", "name": "Diced Chicken with Cashew Nuts in Yellow Bean Sauce", "price": "$15.00"},
    {"code": "C16", "name": "Lemon Soo Gai (Lemon Chicken)", "price": "$15.00"}
  ]
},
 
{
    "title": "RICE",
    "items": [
      {"code": "R1", "name": "Steam Rice", "price": "$4.00"},
      {"code": "R2", "name": "Egg Fried Rice", "price": "$12.00"},
      {"code": "R3", "name": "Vegetable Fried Rice", "price": "$12.00"},
      {"code": "R4", "name": "Chicken Fried Rice", "price": "$12.00"},
      {"code": "R5", "name": "Beef Fried Rice", "price": "$13.00"},
      {"code": "R6", "name": "Szechuan Fried Rice (Vegetable or Chicken or Beef or Shrimp)", "price": "$15.00"},
      {"code": "R7", "name": "Manchurian Fried Rice (Vegetable or Chicken or Beef or Shrimp)", "price": "$15.00"},
      {"code": "R8", "name": "Tofu Fried Rice", "price": "$13.00"},
      {"code": "R9", "name": "Dragon 80ATE Special Fried Rice (Chicken or Beef or Shrimp)", "price": "$15.00"},
      {"code": "R10", "name": "Mushroom Fried Rice", "price": "$12.00"},
      {"code": "R11", "name": "Prawn Fried Rice", "price": "$15.00"},
      {"code": "R12", "name": "Fook Kin Fried Rice", "price": "$18.00"},
      {"code": "R13", "name": "Coconut Rice", "price": "$6.00"},
      {"code": "R14", "name": "Seafood Fried Rice", "price": "$16.00"},
      {"code": "R15", "name": "Pineapple Fried Rice (Chicken or Beef or Shrimp)", "price": "$14.00"},
      {"code": "R16", "name": "Singapore Fried Rice (Vegetable or Chicken or Beef or Shrimp)", "price": "$15.00"}
    ]
  },
  {
    "title": "HOT PLATE SIZZLERS",
    "items": [
      {"code": "HP1", "name": "Sliced Beef or Chicken with Black Pepper Sauce on Hot Plate", "price": "$17.00"},
      {"code": "HP2", "name": "Sliced Beef or Chicken with Black Bean Sauce on Hot Plate", "price": "$17.00"},
      {"code": "HP3", "name": "Prawn & Fish with Szechuan Style Sauce on Hot Plate", "price": "$19.00"},
      {"code": "HP4", "name": "Seafood with Black Bean Sauce on Hot Plate", "price": "$19.00"},
      {"code": "HP5", "name": "Chicken & Prawn in Honey Black Pepper Sauce on Hot Plate", "price": "$18.00"},
      {"code": "HP6", "name": "Prawn & Fish with Broccoli Garlic Butter Sauce", "price": "$19.88"},
      {"code": "HP7", "name": "Mongolian Beef", "price": "$17.00"}
    ]
  },
  {
    "title": "CHOP SUEY",
    "items": [
      {"code": "E1", "name": "Chicken", "price": "$12.28"},
      {"code": "E2", "name": "Beef", "price": "$12.88"},
      {"code": "E3", "name": "Shrimp", "price": "$13.88"},
      {"code": "E4", "name": "Vegetable", "price": "$12.28"},
      {"code": "E5", "name": "Special (Chicken, Prawn & Beef)", "price": "$14.88"}
    ]
  },
  {
  "title": "NOODLES",
  "items": [
    {"name": "Shanghai Noodle with Minced Vegetables (Thick Noodles), Chicken or Beef or Vegetable Chowmein", "price": "$13.00"},
    {"name": "Manchurian Noodles (Vegetable or Chicken or Beef) (Thick Noodles)", "price": "$14.00"},
    {"name": "Seafood Noodles Chow Mein", "price": "$15.00"},
    {"name": "Hakka Style Noodles (Vegetable or Beef or Chicken)", "price": "$15.00"},
    {"name": "Dragon 80ATE Special Chowmein (Chicken, Beef & Shrimp)", "price": "$17.00"},
    {"name": "Shanghai Noodles with Kinds of Meat (in Szechuan Sauce) Thick Noodles", "price": "$16.00"},
    {"name": "Szechuan Chicken Chow Mein", "price": "$16.00"},
    {"name": "Shanghai Noodle with Three Kinds of Seafood (Prawn, Fish & Squid) (Thick Noodles)", "price": "$15.00"},
    {"name": "Shanghai Noodles with Beef in Satay Sauce (Thick Noodles)", "price": "$17.00"},
    {"name": "Prawn Chowmein", "price": "$14.00"},
    {"name": "Cantonese Style Chicken Chow Mein (Crispy Thin Noodles)", "price": "$16.00"},
    {"name": "Cantonese Style Seafood Chowmein (Crispy Thin Noodles)", "price": "$16.00"},
    {"name": "Singapore Rice Noodle (Chicken or Beef) (Thin Rice Noodle)", "price": "$17.00"},
    {"name": "Shanghai Noodle with Sliced Chicken and Black Bean Sauce (Thick Noodle)", "price": "$14.00"},
    {"name": "American Chop Suey (Chicken or Vegetable) (Crispy Thin Noodle)", "price": "$16.00"},
    {"name": "Singapore Rice Noodle with Shrimp (The Rice Noodle)", "price": "$17.00"}
  ]
},
]

# Initialize session state
if 'scanner_active' not in st.session_state:
    st.session_state.scanner_active = False
if 'menu_visible' not in st.session_state:
    st.session_state.menu_visible = False
if 'scan_success' not in st.session_state:
    st.session_state.scan_success = False

def generate_qr_code(text):
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def detect_qr_code_simulation():
    """Simulate QR code detection"""
    time.sleep(2)  # Simulate scanning time
    return True

def display_scanner_interface():
    # Header
    st.markdown("""
    <div class="scanner-header">
        <h1 class="scanner-title">Dragon 80 ATE</h1>
        <p class="scanner-subtitle">Table Scanner - Point camera at QR code to view menu</p>
    </div>
    """, unsafe_allow_html=True)
    
   # Scanner status
    if not st.session_state.scanner_active and not st.session_state.menu_visible:
        st.markdown("""
        <div class="scanner-status status-ready">
            📱 Ready to Scan - Tap "Start Scanner" to begin
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.scanner_active:
        st.markdown("""
        <div class="scanner-status status-scanning">
            🔍 Scanning... Point camera at QR code
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.scan_success:
        st.markdown("""
        <div class="scanner-status status-success">
            ✅ QR Code Detected! Menu loaded successfully
        </div>
        """, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.scanner_active and not st.session_state.menu_visible:
            if st.button("📱 Start Scanner", key="start_scan", help="Activate camera to scan QR code"):
                st.session_state.scanner_active = True
                st.rerun()
        
        elif st.session_state.scanner_active:
            if st.button("⏹️ Stop Scanner", key="stop_scan"):
                st.session_state.scanner_active = False
                st.rerun()
        
        elif st.session_state.menu_visible:
            if st.button("🔄 Scan Again", key="scan_again"):
                st.session_state.menu_visible = False
                st.session_state.scan_success = False
                st.rerun()
    # Scanner simulation
    if st.session_state.scanner_active:
        # Camera placeholder
        st.markdown("""
        <div class="camera-container">
            <div style="height: 400px; display: flex; align-items: center; justify-content: center; background: #1a1a1a; border-radius: 15px;">
                <div style="text-align: center; color: #FFD700;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">📷</div>
                    <div style="font-size: 1.2rem;">Camera Active</div>
                    <div style="font-size: 1rem; opacity: 0.8;">Point at QR code to scan</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-detect simulation
        with st.spinner("Scanning for QR codes..."):
            if detect_qr_code_simulation():
                st.session_state.scanner_active = False
                st.session_state.menu_visible = True
                st.session_state.scan_success = True
                st.balloons()
                st.rerun()
    
    # Instructions when not scanning
    if not st.session_state.scanner_active and not st.session_state.menu_visible:
        st.markdown("""
        <div class="scan-instructions">
            <h3>📋 How to Use</h3>
            <p>1. Tap "Start Scanner" to activate the camera</p>
            <p>2. Point your device at the QR code on your table</p>
            <p>3. The menu will appear automatically when detected</p>
            <br>
            <p><strong>💡 Tip:</strong> Make sure the QR code is well-lit and clearly visible</p>
        </div>
        """, unsafe_allow_html=True)
    
     # Demo QR code
        st.markdown("### 🧪 Demo QR Code")
        st.markdown("Scan this code to test the scanner:")
        
        qr_img = generate_qr_code("")
        st.markdown(f"""
        <div class="qr-display">
            <img src="{qr_img}" width="200" alt="Demo QR Code">
            <p style="color: #333; margin-top: 10px; font-weight: bold;"></p>
        </div>
        """, unsafe_allow_html=True)

def display_menu():
    st.markdown("""
    <div class="menu-container">
        <h1 class="menu-title">Dragon 80 ATE</h1>
        <h2 class="menu-subtitle">FOOD MENU</h2>
        <p class="menu-tagline">Treat yourself to our exquisite cuisine, where every dish tells a story!</p>
        
        <div class="contact-info">
            📍 4408 17 Avenue South East, Calgary Alberta T2A0B6<br>
            📞 403-272-8701 | 🌐 www.Dragon80Ate.com
        </div>
    """, unsafe_allow_html=True)
    
    # Menu sections
    for section in menu_sections:
        st.markdown(f'<div class="section-header">{section["title"]}</div>', unsafe_allow_html=True)
        
        for item in section["items"]:
            code_display = f'<span class="item-code">{item["code"]}</span>' if "code" in item else ""
            st.markdown(f"""
            <div class="menu-item">
                <div class="item-name">
                    {code_display}{item['name']}
                </div>
                <div class="item-price">{item['price']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
        <p class="footer-text"></p>
    </div>
    """, unsafe_allow_html=True)

# Main app
def main():
    if st.session_state.menu_visible:
        display_menu()
    else:
        display_scanner_interface()

if __name__ == "__main__":
    main()