import re

# List of common weak passwords
COMMON_PASSWORDS = [
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "12345678", "iloveyou", "admin", "welcome"
]

def check_password_strength(password):
    """Analyze the strength of a given password."""
    strength = 0
    criteria = {
        "Length (>=12 chars)": len(password) >= 12,
        "Uppercase Letter": bool(re.search(r"[A-Z]", password)),
        "Lowercase Letter": bool(re.search(r"[a-z]", password)),
        "Digit": bool(re.search(r"\d", password)),
        "Special Character": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }

    # Calculate strength based on fulfilled criteria
    for rule, passed in criteria.items():
        if passed:
            strength += 1

    # Check if the password is in the list of common passwords
    if password.lower() in COMMON_PASSWORDS:
        print("\n[⚠] WARNING: This is a commonly used weak password!")
        return "Very Weak ❌"

    # Strength classification
    if strength == 5:
        return "Very Strong ✅"
    elif strength >= 3:
        return "Strong 💪"
    elif strength == 2:
        return "Weak ⚠"
    else:
        return "Very Weak ❌"

if __name__ == "__main__":
    user_password = input("Enter your password to check its strength: ").strip()

    if not user_password:
        print("[!] Invalid input. Please enter a valid password.")
        exit(1)

    result = check_password_strength(user_password)
    print(f"\n[+] Password Strength: {result}")
