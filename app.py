import streamlit as st

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Simple user credentials (in production, use a proper database)
VALID_USERS = {
    "admin": "admin123",
    "user": "user123"
}

def login_page():
    """Login page for authentication"""
    st.title("🔐 Login")
    st.markdown("---")
    
    # Create a centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Please enter your credentials")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful! Redirecting to chat...")
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        st.markdown("---")
        st.caption("Demo credentials:")
        st.caption("Username: `admin` | Password: `admin123`")
        st.caption("Username: `user` | Password: `user123`")

def chat_page():
    """Chat interface page"""
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.title("💬 Chat App")
        st.markdown("---")
        st.write(f"👤 Logged in as: **{st.session_state.username}**")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat area
    st.title("💬 Chat Interface")
    st.markdown(f"Welcome, **{st.session_state.username}**! Start chatting below.")
    st.markdown("---")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate a simple bot response (you can integrate with an AI model here)
        bot_response = generate_response(prompt)
        
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Display assistant message
        with st.chat_message("assistant"):
            st.markdown(bot_response)

def generate_response(user_input: str) -> str:
    """
    Generate a simple response based on user input.
    In a real application, you would integrate with an AI model like OpenAI, etc.
    """
    user_input_lower = user_input.lower()
    
    if "hello" in user_input_lower or "hi" in user_input_lower:
        return f"Hello {st.session_state.username}! 👋 How can I help you today?"
    elif "how are you" in user_input_lower:
        return "I'm doing great, thank you for asking! 😊 How about you?"
    elif "bye" in user_input_lower or "goodbye" in user_input_lower:
        return "Goodbye! Have a great day! 👋"
    elif "help" in user_input_lower:
        return """I'm a simple chat bot. Here are some things you can try:
- Say "hello" or "hi" to greet me
- Ask "how are you"
- Say "bye" to end the conversation
- Or just type anything and I'll respond!"""
    elif "time" in user_input_lower:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M:%S')} ⏰"
    elif "date" in user_input_lower:
        from datetime import datetime
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')} 📅"
    else:
        return f"You said: '{user_input}'. This is a demo chat interface. In a real app, you could integrate with AI models like OpenAI GPT for intelligent responses! 🤖"

def main():
    """Main function to handle page routing"""
    st.set_page_config(
        page_title="Streamlit Auth & Chat Demo",
        page_icon="💬",
        layout="centered"
    )
    
    # Route based on authentication status
    if st.session_state.authenticated:
        chat_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
