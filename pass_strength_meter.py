import streamlit as st # type: ignore
import random
import string
import hashlib
import requests # type: ignore

def check_password_strength(password):
    length_score = min(len(password) / 8, 1) * 40  # Max 40 points
    digit_score = min(sum(c.isdigit() for c in password), 2) * 10  # Max 20 points
    special_score = min(sum(c in string.punctuation for c in password), 2) * 10  # Max 20 points
    uppercase_score = min(sum(c.isupper() for c in password), 2) * 10  # Max 20 points
    
    total_score = length_score + digit_score + special_score + uppercase_score
    
    if total_score >= 80:
        return "Strong", "green"
    elif total_score >= 50:
        return "Moderate", "orange"
    else:
        return "Weak", "red"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def check_breach(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    response = requests.get(url)
    if response.status_code == 200:
        hashes = response.text.splitlines()
        for line in hashes:
            hash_suffix, count = line.split(":")
            if hash_suffix == suffix:
                return True, int(count)
    return False, 0

st.set_page_config(page_title="Password Security Suite", layout="centered")
st.title("🔒 Password Security Suite")

st.sidebar.title("Options")
mode = st.sidebar.radio("Choose Mode:", ["Check Password Strength", "Generate Password", "Check Breach History"])

dark_mode = st.sidebar.checkbox("Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            body {
                background-color: #1e1e1e;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

if mode == "Check Password Strength":
    password = st.text_input("Enter your password:", type="password")
    if password:
        strength, color = check_password_strength(password)
        st.markdown(f"**Strength:** <span style='color:{color}'>{strength}</span>", unsafe_allow_html=True)

elif mode == "Generate Password":
    length = st.slider("Select password length:", 8, 32, 12)
    if st.button("Generate"):
        new_password = generate_password(length)
        st.code(new_password, language='plaintext')

elif mode == "Check Breach History":
    password = st.text_input("Enter your password:", type="password")
    if password and st.button("Check"):
        breached, count = check_breach(password)
        if breached:
            st.error(f"⚠️ Your password has been found in {count} breaches! Change it immediately.")
        else:
            st.success("✅ Your password is safe and has not been found in breaches.")
