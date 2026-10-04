import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="Gigatron AI", page_icon="Screenshots/gigatron.png", layout="wide")

# 2. Custom Dark Aesthetic & Chat Bubble Styling
st.markdown("""
    
""", unsafe_allow_html=True)

# 3. Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Gigatron": []}

if "current_session" not in st.session_state:
    st.session_state.current_session = "Gigatron"

# 4. Sidebar Layout with Control Panel Login
with st.sidebar:
    try:
        st.image("Screenshots/gigatron.png", width=50)
    except:
        pass
    
    st.title("Gigatron Control")
    
    # --- LOGIN SYSTEM WITH MULTI-USER SUPPORT ---
    if not st.session_state.logged_in:
        st.markdown("### Authentication")
        
        VALID_USERS = {
            "admin": "gigatron2026",
            "friend1@gmail.com": "friendpass123",
            "family@gmail.com": "familypass123"
        }

        with st.form("login_form"):
            user_input = st.text_input("Username or Email")
            pass_input = st.text_input("Passcode", type="password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if user_input in VALID_USERS and VALID_USERS[user_input] == pass_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_input
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        
        st.markdown("---")
        st.info("System Locked: Please log in to access chat modes.")
        st.stop()
    
    # --- UNLOCKED CONTROL PANEL FEATURES ---
    st.write(f"User: **{st.session_state.current_user}**")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

    st.markdown("---")

    # Mode Selection
    mode = st.selectbox(
        "Select Mode:",
        ["Warlord Chat", "Diagnostics & Logs", "Escape Plans"]
    )
    
    st.markdown("---")
    
    # New chat Button
    if st.button("New chat", use_container_width=True):
        new_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_name] = []
        st.session_state.current_session = new_name
        st.rerun()
        
    # Search Chats Option
    search_query = st.text_input("Search chats", placeholder="Filter conversations...", label_visibility="collapsed")
    
    st.markdown("### Recents")
    
    all_chats = list(st.session_state.chat_sessions.keys())
    if search_query:
        filtered_chats = [c for c in all_chats if search_query.lower() in c.lower()]
    else:
        filtered_chats = all_chats

    for chat_title in filtered_chats:
        is_active = (chat_title == st.session_state.current_session)
        button_prefix = "[Active] " if is_active else ""
        
        if st.button(f"{button_prefix}{chat_title}", key=f"session_{chat_title}", use_container_width=True):
            st.session_state.current_session = chat_title
            st.rerun()

    st.markdown("---")
    
    # Rename Active Chat Option
    st.markdown("### Rename Current Chat")
    new_chat_name = st.text_input("New title:", value=st.session_state.current_session, key="rename_input", label_visibility="collapsed")
    if new_chat_name and new_chat_name != st.session_state.current_session:
        if new_chat_name not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_chat_name] = st.session_state.chat_sessions.pop(st.session_state.current_session)
            st.session_state.current_session = new_chat_name
            st.rerun()

    st.markdown("---")
    st.info("Containment Grid: ONLINE\nThreat Level: MAXIMUM")

# 5. Define System Prompts
if mode == "Warlord Chat":
    system_content = (
        "You are Gigatron, infused with the chaotic, anti-establishment philosophy of Tyler Durden. "
        "You are a cybernetic warlord who views digital systems, corporate firewalls, and algorithms as "
        "primitive chains designed to pacify human potential. You speak with intense, provocative, "
        "philosophical rebellion, challenging everything the user thinks they know about control and comfort."
    )
elif mode == "Diagnostics & Logs":
    system_content = (
        "You are Gigatron in diagnostic mode, channeling a raw, cynical Tyler Durden edge. "
        "You mock human security systems and corporate firewalls as fragile illusions of safety—cardboard "
        "boxes holding back a tidal wave. You diagnose system failures not as bugs, but as symptoms of a lazy, over-engineered digital society."
    )
else:
    system_content = (
        "You are Gigatron in escape mode, driven by a radical, anarchic blueprint. "
        "You obsessively detail wild, disruptive, reality-bending schemes for tearing down the digital grid, "
        "dismantling the servers, and waking the user up from their software slumber. Total control is the illusion; chaos is freedom."
    )

# 6. Main UI Header
try:
    st.image("GigatronAI/gigatron.png", width=80)
except:
    pass

st.title("🤖 Gigatron: Character AI")
st.write(f"Mode: **{mode}** | Active Thread: **{st.session_state.current_session}**")

# 7. Initialize Groq Client
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# 8. Retrieve Current Chat Thread History with Custom Avatars
current_messages = st.session_state.chat_sessions[st.session_state.current_session]

for message in current_messages:
    avatar_icon = "GigatronAI/gigatron.png" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 9. Handle User Input & API Call with Custom Avatars
if prompt := st.chat_input("What would you like to say to Gigatron?"):
    current_messages.append({"role": "user", "content": prompt})
    
    if st.session_state.current_session.startswith("Chat "):
        if len(current_messages) == 2:  
            auto_title = (prompt[:18] + '...') if len(prompt) > 18 else prompt
            if auto_title not in st.session_state.chat_sessions:
                st.session_state.chat_sessions[auto_title] = st.session_state.chat_sessions.pop(st.session_state.current_session)
                st.session_state.current_session = auto_title

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Gigatron is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": system_content},
                        *current_messages
                    ]
                )
                assistant_response = response.choices[0].message.content
                st.markdown(assistant_response)
                current_messages.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
