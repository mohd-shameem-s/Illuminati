import re

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Common weak passwords
COMMON_PASSWORDS = [
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "12345678", "iloveyou", "admin", "welcome"
]

def check_password_strength(password):
    """Analyze the strength of a given password."""
    print(f"\n{CYAN}{BOLD}🔐 Checking Password Strength...{RESET}\n")

    # Criteria rules
    criteria = {
        "Length (>= 12 chars)": len(password) >= 12,
        "Uppercase Letter": bool(re.search(r"[A-Z]", password)),
        "Lowercase Letter": bool(re.search(r"[a-z]", password)),
        "Digit": bool(re.search(r"\d", password)),
        "Special Character": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }

    # Show individual rule results
    for rule, passed in criteria.items():
        print(f"[{GREEN}✅{RESET}]" if passed else f"[{RED}❌{RESET}]", end=" ")
        print(f"{rule}")

    # Total score
    strength = sum(criteria.values())

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        print(f"\n{YELLOW}[⚠] WARNING: This is a commonly used weak password!{RESET}")
        strength = 0  # Force very weak

    # Strength classification
    print(f"\n{BLUE}[+] Password Strength:{RESET} ", end="")
    if strength == 5:
        print(f"{GREEN}{BOLD}Very Strong ✅{RESET}")
    elif strength >= 3:
        print(f"{YELLOW}{BOLD}Strong 💪{RESET}")
    elif strength == 2:
        print(f"{YELLOW}{BOLD}Weak ⚠{RESET}")
    else:
        print(f"{RED}{BOLD}Very Weak ❌{RESET}")

    # Suggestions
    print(f"\n{CYAN}📌 Suggestions to improve your password:{RESET}")
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
    print(f"{BOLD}{CYAN}🔐 Password Strength Checker{RESET}")
    user_password = input("Enter your password to check its strength: ").strip()

    if not user_password:
        print(f"{RED}[!] Invalid input. Please enter a valid password.{RESET}")
        exit(1)

    check_password_strength(user_password)
