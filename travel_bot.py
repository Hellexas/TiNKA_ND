import streamlit as st
import re
import random
import time

# --- CONFIGURATION & STYLING ---
# Switched to "centered" layout for a more focused, app-like feel
st.set_page_config(page_title="Wanderlust AI", page_icon="🌍", layout="centered")

# Custom CSS for a professional look
st.markdown("""
<style>
    /* --- GLOBAL THEME FIXES --- */
    /* Force Dark Theme Colors with Vertical Gradient */
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #1e293b); /* Slate Dark Gradient */
        color: #e2e8f0; /* Light Grey Text */
    }

    /* Ensure all text in the main area is readable */
    .stApp p, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #e2e8f0 !important;
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: #020617; /* Very Dark Blue/Black */
        color: white !important;
        border-right: 1px solid #1e293b;
    }

    /* Force white text in sidebar */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #334155;
        border-color: #475569;
    }

    /* --- MAIN CONTENT STYLING --- */

    /* Header Styling */
    h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stCaption {
        text-align: center;
        font-size: 1.1rem;
        color: #94a3b8 !important; /* Slate 400 */
        margin-bottom: 2rem;
    }

    /* Chat Message Bubbles */
    .stChatMessage {
        background-color: #1e293b; /* Slate 800 */
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #334155; /* Slate 700 */
    }

    /* Fix text inside chat bubbles */
    .stChatMessage p, .stChatMessage li {
        color: #e2e8f0 !important;
    }

    /* User Messages - Distinct Color */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #334155; /* Slate 700 */
        border-color: #475569;
    }

    /* Input Field Styling */
    .stTextInput input {
        border-radius: 25px;
        border: 1px solid #475569;
        padding: 12px 20px;
        font-size: 16px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: #f8fafc !important; /* Light text */
        background-color: #1e293b !important; /* Dark background */
    }
    .stTextInput input:focus {
        border-color: #60a5fa; /* Blue focus */
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.25);
    }

    /* Hide Streamlit Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


class RuleBasedChatbot:
    def __init__(self):
        # VERSION TAG: Set to 1.6
        self.version = "1.6"
        self.context = {"state": None, "data": {}}

        # --- KNOWLEDGE BASE ---
        self.schengen = {'lithuania', 'poland', 'greece', 'france', 'germany', 'italy', 'spain', 'portugal'}
        self.eu_visa_free_to_china = {'poland', 'greece', 'france', 'germany', 'italy', 'spain'}

        # Tourist Attractions
        self.country_attractions = {
            "lithuania": ["Gediminas Tower", "Trakai Island Castle", "Curonian Spit", "Hill of Crosses"],
            "poland": ["Wawel Castle (Krakow)", "Wieliczka Salt Mine", "Warsaw Old Town", "Malbork Castle"],
            "turkey": ["Hagia Sophia", "Cappadocia Balloons", "Pamukkale Thermal Pools", "Ephesus"],
            "greece": ["Acropolis of Athens", "Santorini Sunsets", "Meteora Monasteries", "Navagio Beach"],
            "russia": ["Red Square", "The Hermitage", "Lake Baikal", "Peterhof Palace"],
            "ukraine": ["Kyiv Pechersk Lavra", "Lviv Old Town", "Tunnel of Love", "Carpathian Mountains"],
            "thailand": ["The Grand Palace", "Phi Phi Islands", "Chiang Mai Night Bazaar", "Ayutthaya"],
            "india": ["Taj Mahal", "Jaipur Pink City", "Varanasi Ghats", "Kerala Backwaters"],
            "china": ["Great Wall of China", "Forbidden City", "Terracotta Army", "The Bund (Shanghai)"],
            "usa": ["Grand Canyon", "Statue of Liberty", "Yellowstone National Park", "Disney World", "Times Square"],
            "uk": ["Big Ben", "Stonehenge", "Edinburgh Castle", "British Museum"],
            "france": ["Eiffel Tower", "Louvre Museum", "Mont Saint-Michel", "French Riviera"],
            "italy": ["Colosseum", "Venice Canals", "Leaning Tower of Pisa", "Amalfi Coast"],
            "germany": ["Brandenburg Gate", "Neuschwanstein Castle", "Cologne Cathedral", "Black Forest"],
            "spain": ["Sagrada Família", "Alhambra", "Park Güell", "Ibiza"],
            "japan": ["Mount Fuji", "Kyoto Temples", "Tokyo Tower", "Osaka Castle"]
        }

        # Detailed Country Info
        self.country_info = {
            "lithuania": {"currency": "Euro (€)", "lang": "Lithuanian", "tip": "Not mandatory, but 10% is appreciated.",
                          "best_time": "May to September"},
            "poland": {"currency": "Polish Złoty (PLN)", "lang": "Polish", "tip": "10% is standard in restaurants.",
                       "best_time": "May to October"},
            "turkey": {"currency": "Turkish Lira (TRY)", "lang": "Turkish", "tip": "5-10% in restaurants is customary.",
                       "best_time": "April-May or September-October"},
            "greece": {"currency": "Euro (€)", "lang": "Greek", "tip": "Round up the bill or 5-10%.",
                       "best_time": "April to June or September to October"},
            "russia": {"currency": "Russian Ruble (RUB)", "lang": "Russian", "tip": "10% is common in cities.",
                       "best_time": "May to September"},
            "ukraine": {"currency": "Ukrainian Hryvnia (UAH)", "lang": "Ukrainian", "tip": "10% is standard.",
                        "best_time": "May to September"},
            "thailand": {"currency": "Thai Baht (THB)", "lang": "Thai",
                         "tip": "Not customary, but loose change is nice.",
                         "best_time": "November to February (Cool season)"},
            "india": {"currency": "Indian Rupee (INR)", "lang": "Hindi & English",
                      "tip": "10% at restaurants, small amount for porters.", "best_time": "October to March"},
            "china": {"currency": "Renminbi (CNY)", "lang": "Mandarin",
                      "tip": "Generally not practiced and can be seen as rude.",
                      "best_time": "April-May or September-October"},
            "usa": {"currency": "US Dollar ($)", "lang": "English", "tip": "15-20% is practically mandatory.",
                    "best_time": "All year round depending on region"},
            "uk": {"currency": "British Pound (£)", "lang": "English", "tip": "10-15% if service not included.",
                   "best_time": "May to September"},
            "france": {"currency": "Euro (€)", "lang": "French", "tip": "Service is included, small change is polite.",
                       "best_time": "April to June or September to November"},
            "italy": {"currency": "Euro (€)", "lang": "Italian", "tip": "Service usually included; just round up.",
                      "best_time": "April to June or September to October"},
            "germany": {"currency": "Euro (€)", "lang": "German", "tip": "Round up or add 5-10%.",
                        "best_time": "May to September"},
            "spain": {"currency": "Euro (€)", "lang": "Spanish", "tip": "Round up or leave loose change.",
                      "best_time": "April to June or September to October"},
            "japan": {"currency": "Japanese Yen (JPY)", "lang": "Japanese",
                      "tip": "No tipping! It can be considered rude.",
                      "best_time": "March-May (Sakura) or September-November"}
        }

        # Average daily cost per person (USD)
        self.daily_costs = {
            "lithuania": 80, "poland": 90, "turkey": 100, "greece": 150,
            "russia": 90, "ukraine": 60, "thailand": 50, "india": 45,
            "china": 110, "usa": 250, "uk": 200, "france": 220,
            "italy": 180, "germany": 170, "spain": 160, "japan": 190
        }

        self.destinations = {
            "beach": ["Maldives", "Bora Bora", "Maui, Hawaii", "Phuket, Thailand", "Antalya, Turkey", "Greek Islands"],
            "mountain": ["Swiss Alps", "Zakopane, Poland", "Kathmandu, Nepal", "Machu Picchu, Peru", "Sochi, Russia"],
            "city": ["Tokyo, Japan", "Shanghai, China", "Paris, France", "London, UK", "Istanbul, Turkey",
                     "Mumbai, India"],
            "budget": ["Bali, Indonesia", "Kyiv, Ukraine", "Bangkok, Thailand", "Goa, India", "Siem Reap, Cambodia"]
        }

        self.packing_lists = {
            "cold": ["Thermal underwear", "Heavy coat", "Wool socks", "Gloves & Beanie", "Lip balm"],
            "hot": ["Sunscreen", "Swimwear", "Sunglasses", "Light linen clothes", "Hat"],
            "general": ["Passport", "Universal adapter", "Power bank", "Toiletries", "First aid kit"]
        }

    def get_visa_rule(self, origin, dest):
        if origin == dest: return "You don't need a visa to travel within your own country! 🏠"
        if origin in self.schengen and dest in self.schengen: return "✅ **Visa Free:** Freedom of movement applies within the Schengen Area."

        if dest in self.schengen:
            if origin in ['usa', 'canada', 'uk', 'japan', 'ukraine', 'brazil']:
                return f"✅ **Visa Free:** Citizens of {origin.title()} can usually enter the Schengen area ({dest.title()}) for 90 days."
            elif origin in ['russia', 'china', 'india', 'turkey', 'thailand']:
                return f"🛂 **Visa Required:** Citizens of {origin.title()} generally need a Schengen Visa."

        if dest == 'turkey':
            if origin in self.schengen or origin in ['ukraine', 'russia', 'thailand', 'uk', 'usa']:
                return "✅ **Visa Free:** generally visa-free for short tourism stays."
            elif origin in ['india', 'china']:
                return "🛂 **Visa Required:** E-Visa or Sticker visa required."

        if dest == 'usa':
            if origin in self.schengen or origin in ['uk',
                                                     'japan']: return "📝 **ESTA Required:** Visa Waiver Program available (ESTA)."
            return "🛂 **Visa Required:** B1/B2 Visa typically needed."

        if dest == 'russia':
            if origin in ['china', 'thailand', 'turkey']:
                return "✅ **Visa Free / Simplified:** Visa-free for groups or simplified entry."
            elif origin in self.schengen or origin in ['usa', 'uk', 'canada', 'india']:
                return "🛂 **Visa Required:** You likely need a visa. (Unified E-visa is available)."

        if dest == 'ukraine':
            if origin in self.schengen or origin in ['usa', 'uk', 'canada', 'turkey']:
                return "✅ **Visa Free:** Up to 90 days within 180 days."
            elif origin == 'india':
                return "🛂 **Visa Required:** E-Visa available."
            elif origin == 'china':
                return "🛂 **Visa Required:** Standard visa required."

        if dest == 'thailand':
            if origin in self.schengen or origin in ['usa', 'uk', 'canada', 'russia', 'turkey', 'china', 'india',
                                                     'ukraine']: return "✅ **Visa Free / VOA:** Thailand currently has very open policies."

        if dest == 'india':
            if origin in ['usa', 'uk', 'russia', 'ukraine', 'thailand',
                          'turkey'] or origin in self.schengen or origin == 'china': return "🛂 **Visa Required:** E-Visa is widely available."

        if dest == 'china':
            if origin == 'thailand': return "✅ **Visa Free:** Permanent mutual visa exemption."
            if origin in self.eu_visa_free_to_china: return "✅ **Visa Free:** 15-day visa-free entry (Trial policy)."
            if origin in ['usa', 'uk', 'canada', 'india', 'lithuania', 'turkey',
                          'ukraine']: return "🛂 **Visa Required:** You generally need a tourist (L) visa."

        return f"Generally, check if {dest.title()} offers an E-Visa for {origin.title()} citizens."

    def calculate_package(self, data):
        country = data.get('country')
        people = data.get('people', 2)
        budget = data.get('budget', 1000)
        min_nights = data.get('min_nights', 3)
        max_nights = data.get('max_nights', 7)

        daily_cost = self.daily_costs.get(country, 100)
        total_daily_burn = daily_cost * people

        if total_daily_burn <= 0: total_daily_burn = 100  # Safety

        affordable_nights = int(budget / total_daily_burn)

        if affordable_nights < min_nights:
            return (f"🎉 **Custom Package for {country.title()}** 🎉\n\n"
                    f"⚠️ **Budget Constraint:** A budget of ${budget} is quite tight for {people} people in {country.title()}. "
                    f"Average daily cost is approx ${total_daily_burn}. You can afford about **{affordable_nights} nights**. "
                    f"I recommend increasing the budget to at least ${total_daily_burn * min_nights} for a short {min_nights}-day trip.")

        suggested_nights = min(affordable_nights, max_nights)
        estimated_cost = suggested_nights * total_daily_burn
        attractions = ", ".join(self.country_attractions.get(country, ["City Center"])[:3])

        return (f"🎉 **Custom Package for {country.title()}** 🎉\n\n"
                f"Based on your budget of **${budget}** for **{people} people**:\n"
                f"- **Recommended Stay:** {suggested_nights} Nights\n"
                f"- **Estimated Total Cost:** ${estimated_cost} (Approx. ${daily_cost}/person/day)\n"
                f"- **Suggested Itinerary:** Visit {attractions}.\n"
                f"- **Travel Tip:** {'Great budget choice!' if suggested_nights == max_nights else 'Note: This maximizes your budget within the given range.'}")

    def extract_package_details(self, text, current_data):
        text = text.lower()
        if 'solo' in text or 'just me' in text:
            current_data['people'] = 1
        elif 'couple' in text:
            current_data['people'] = 2
        else:
            people_match = re.search(r'(\d+)\s*(people|person|pax|travelers)', text)
            if people_match: current_data['people'] = int(people_match.group(1))

        # REGEX for Budget
        budget_match = re.search(r'(\$|€|eur|usd|budget)\s*?(\d+)', text)
        if not budget_match: budget_match = re.search(r'(\d+)\s*(dollars|usd|eur|€|\$)', text)
        if budget_match:
            for group in budget_match.groups():
                if group and group.isdigit():
                    current_data['budget'] = int(group)
                    break

        range_match = re.search(r'(\d+)\s*-\s*(\d+)\s*(nights|days)', text)
        if range_match:
            current_data['min_nights'] = int(range_match.group(1))
            current_data['max_nights'] = int(range_match.group(2))
        else:
            single_night_match = re.search(r'(\d+)\s*(nights|days)', text)
            if single_night_match:
                val = int(single_night_match.group(1))
                current_data['min_nights'] = val
                current_data['max_nights'] = val
            elif "week" in text:
                current_data['min_nights'] = 7
                current_data['max_nights'] = 7
        return current_data

    def detect_country(self, text):
        text = text.lower()
        sorted_countries = sorted(self.country_attractions.keys(), key=len, reverse=True)
        for country in sorted_countries:
            pattern = r'\b' + re.escape(country) + r'\b'
            if re.search(pattern, text): return country
        return None

    def match_rule(self, user_input):
        user_text = user_input.lower().strip()
        mentioned_country = self.detect_country(user_text)

        # 1. TRAVEL PACKAGE STATE HANDLING
        if self.context.get("state") == "planning_package":
            self.context["data"] = self.extract_package_details(user_text, self.context["data"])
            data = self.context["data"]
            if 'people' not in data: return "Got it. How many people are traveling?"
            if 'budget' not in data: return f"Okay, for {data['people']} people. What is your total budget for the trip (in USD/EUR)?"

            if 'min_nights' not in data:
                if 'people' in data and 'budget' in data:
                    self.context["state"] = None
                    return self.calculate_package(data)
                return "Almost done! How many nights do you want to stay? (You can give a range like '5-7 nights')"

            self.context["state"] = None
            return self.calculate_package(data)

        # 2. TRAVEL PACKAGE TRIGGER
        if ("package" in user_text or "plan" in user_text) and mentioned_country and "visa" not in user_text:
            self.context["state"] = "planning_package"
            self.context["data"] = {"country": mentioned_country}
            self.context["data"] = self.extract_package_details(user_text, self.context["data"])
            data = self.context["data"]
            if 'people' not in data:
                return f"I can definitely build a travel package for **{mentioned_country.title()}**! 🎒\nFirst, how many people are traveling?"
            elif 'budget' not in data:
                return f"Building a package for {data['people']} people to {mentioned_country.title()}. What is your total budget?"

            elif 'min_nights' not in data:
                if 'people' in data and 'budget' in data:
                    self.context["state"] = None
                    return self.calculate_package(data)
                return "And how many nights are you planning to stay? (e.g., '5-7 nights')"
            else:
                self.context["state"] = None
                return self.calculate_package(data)

        # 3. VISA INQUIRIES
        visa_match = re.search(r'visa.*from\s+(?P<origin>\w+)\s+to\s+(?P<dest>\w+)', user_text)
        if not visa_match: visa_match = re.search(r'visa.*(?P<origin>\w+)\s+citizen.*\s+(?P<dest>\w+)', user_text)
        if visa_match:
            return self.get_visa_rule(visa_match.group('origin').lower(), visa_match.group('dest').lower())

        if "visa" in user_text:
            if mentioned_country and "from" in user_text:
                return f"I see you're asking about a visa for {mentioned_country.title()}, but I need to know your origin. Try 'Visa from [Origin] to {mentioned_country.title()}'."
            return "To check visas, please tell me: **Where are you from** and **Where are you going?** (e.g., 'Visa from Turkey to Greece')"

        # 4. COMMON QUESTIONS
        if mentioned_country:
            info = self.country_info.get(mentioned_country)
            if info:
                if any(x in user_text for x in ['when', 'best time',
                                                'season']): return f"🗓️ **Best time to visit {mentioned_country.title()}:** {info['best_time']}."
                if any(x in user_text for x in ['currency', 'money',
                                                'pay']): return f"💱 **Currency in {mentioned_country.title()}:** {info['currency']}."
                if any(x in user_text for x in
                       ['tip', 'tipping']): return f"💸 **Tipping in {mentioned_country.title()}:** {info['tip']}"
                if any(x in user_text for x in ['language', 'speak',
                                                'english']): return f"🗣️ **Language in {mentioned_country.title()}:** {info['lang']}."

        # 5. ATTRACTIONS
        if mentioned_country:
            if any(x in user_text for x in ['attractions', 'sightseeing', 'what to see', 'places to visit']):
                attractions = self.country_attractions.get(mentioned_country)
                return f"Top things to see in **{mentioned_country.title()}**: \n- " + "\n- ".join(attractions)

            if any(x in user_text for x in ['visit', 'see']) and "visa" not in user_text and "tip" not in user_text:
                attractions = self.country_attractions.get(mentioned_country)
                return f"Top things to see in **{mentioned_country.title()}**: \n- " + "\n- ".join(attractions)

        # 6. PACKING
        pack_match = re.search(r'(pack|bring|wear).*?for\s+(?P<target>\w+)', user_text)
        if pack_match:
            target = pack_match.group('target')
            if any(x in target for x in ['russia', 'iceland', 'winter', 'snow', 'cold', 'ski', 'poland', 'ukraine']):
                return f"For {target}, it might be chilly! Pack: " + ", ".join(self.packing_lists['cold'])
            elif any(x in target for x in ['beach', 'summer', 'hot', 'thailand', 'india', 'greece', 'turkey']):
                return f"For {target}, enjoy the warmth! Pack: " + ", ".join(self.packing_lists['hot'])
            return "Sticking to general essentials: " + ", ".join(self.packing_lists['general'])

        # 7. SUGGESTIONS
        if any(x in user_text for x in ['suggest', 'recommend', 'where to go']):
            if "beach" in user_text: return f"For a beach trip, I highly recommend **{random.choice(self.destinations['beach'])}**!"
            if "mountain" in user_text: return f"For mountains, **{random.choice(self.destinations['mountain'])}** is amazing."
            if "city" in user_text: return f"If you want city vibes, try **{random.choice(self.destinations['city'])}**."
            if "budget" in user_text: return f"For a budget-friendly trip, consider **{random.choice(self.destinations['budget'])}**."
            return "Do you prefer a **beach**, **mountains**, a bustling **city**, or a **budget-friendly** trip?"

        # 8. BUDGETING
        if re.search(r'\b(cost|price|budget.*?|expensive|cheap)\b', user_text):
            return "Budgeting: \n- **Budget:** Thailand, India, Vietnam ($30-50/day)\n- **Mid:** Turkey, Greece, Poland ($80-120/day)\n- **High:** USA, UK, Switzerland ($200+/day)."

        if re.search(r'\b(hi|hello|hey|greetings|hola)\b', user_text):
            return "Hello! I can help with **Travel Packages**, **Visas**, **Packing**, **Currency**, or **Suggestions**."

        return "I can help with **Travel Packages** (e.g., 'Package for Poland'), **Visas**, **Packing**, **Currency**, **Best Time to Visit**, or **Suggestions**."


# --- STREAMLIT UI SETUP ---
def main():
    if 'bot' not in st.session_state or getattr(st.session_state.bot, 'version', '') != "1.6":
        st.session_state.bot = RuleBasedChatbot()
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Wanderlust AI. How can I help you plan your trip today?"}]

    with st.sidebar:
        st.title("🌍 Wanderlust AI")
        st.markdown("Your intelligent travel companion.")
        st.markdown("---")

        st.subheader("💡 Quick Tips")
        st.info("**Plan a Trip:**\n'Package for Italy, $2000, 2 people'")
        st.info("**Check Visas:**\n'Visa from USA to Japan'")
        st.info("**Local Info:**\n'Best time to visit Thailand'")

        st.markdown("---")
        with st.expander("⚙️ System Controls"):
            st.write(f"Engine v{st.session_state.bot.version}")
            if st.button("Reset Session", type="primary"):
                st.session_state.bot = RuleBasedChatbot()
                st.session_state.messages = []
                st.rerun()

    st.markdown("# ✈️ Wanderlust AI")
    st.caption("Plan your next adventure with ease. Ask about packages, visas, packing, and more.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Ex: Plan a trip to Japan..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Simulate thinking for realism
        with st.spinner("Thinking..."):
            time.sleep(0.6)
            response = st.session_state.bot.match_rule(prompt)

        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
