import re

# List of common weak passwords
COMMON_PASSWORDS = [
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "12345678", "iloveyou", "admin", "welcome"
]

def check_password_strength(password):
    """Analyze the strength of a given password."""
    print("\n🔐 Checking Password Strength...\n")

    # Rules to check
    criteria = {
        "Length (>= 12 chars)": len(password) >= 12,
        "Uppercase Letter": bool(re.search(r"[A-Z]", password)),
        "Lowercase Letter": bool(re.search(r"[a-z]", password)),
        "Digit": bool(re.search(r"\d", password)),
        "Special Character": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }

    # Print rule results
    for rule, passed in criteria.items():
        print(f"[{'✅' if passed else '❌'}] {rule}")

    # Count how many criteria passed
    strength = sum(criteria.values())

    # Check for common password
    if password.lower() in COMMON_PASSWORDS:
        print("\n[⚠] WARNING: This is a commonly used weak password!")
        strength = 0  # Force Very Weak

    # Strength classification
    if strength == 5:
        strength_result = "Very Strong ✅"
    elif strength >= 3:
        strength_result = "Strong 💪"
    elif strength == 2:
        strength_result = "Weak ⚠"
    else:
        strength_result = "Very Weak ❌"

    print(f"\n[+] Password Strength: {strength_result}")

    # Suggestions
    print("\n📌 Suggestions to improve your password:")
    if len(password) < 12:
        print(" - Use at least 12 characters.")
    if not criteria["Uppercase Letter"]:
        print(" - Add uppercase letters (A-Z).")
    if not criteria["Lowercase Letter"]:
        print(" - Include lowercase letters (a-z).")
    if not criteria["Digit"]:
        print(" - Use numbers (0-9).")
    if not criteria["Special Character"]:
        print(" - Add special characters (e.g., !@#$%).")
    if password.lower() in COMMON_PASSWORDS:
        print(" - Avoid common passwords (e.g., 'admin', '123456', 'password').")

if __name__ == "__main__":
    user_password = input("🔐 Enter your password to check its strength: ").strip()

    if not user_password:
        print("[!] Invalid input. Please enter a valid password.")
        exit(1)

    check_password_strength(user_password)
