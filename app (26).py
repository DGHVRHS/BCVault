%%writefile app.py
import streamlit as st
import math
import re
import ast
import operator

st.set_page_config(page_title="Unlock the Vault: Calculus!", layout="wide")

# Safe math parser supporting integers, fractions, decimals, pi, and sqrt(...)
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def parse_math_answer(raw_text):
    if not raw_text or not raw_text.strip():
        return None
    expr = raw_text.strip().lower().replace("π", "pi").replace("√", "sqrt").replace("^", "**")
    # Convert implicit multiplication like "2pi" or "3sqrt(2)" into "2*pi" or "3*sqrt(2)"
    expr = re.sub(r"(\d)\s*(pi|sqrt)\b", r"\1*\2", expr)
    expr = re.sub(r"\)\s*\(", r")*(", expr)
    expr = re.sub(r"\)\s*(pi|sqrt|\d)", r")*\1", expr)

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id == "pi":
            return math.pi
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "sqrt"
            and len(node.args) == 1
        ):
            arg_val = _eval(node.args[0])
            if arg_val < 0:
                raise ValueError("Negative sqrt")
            return math.sqrt(arg_val)
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression")

    try:
        tree = ast.parse(expr, mode="eval")
        val = _eval(tree)
        if math.isnan(val) or math.isinf(val):
            return None
        return float(val)
    except Exception:
        return None


# 2 Distinct Versions (6 Calculus Locks per Version -> 6-Digit Vault Passcode)
VAULT_VERSIONS = {
    "Team 1 — Alpha Vault": {
        "color": "🔵",
        "passcode": ["8", "3", "5", "1", "9", "4"],
        "locks": [
            {
                "title": "Lock 1: Related Rates (Dock & Pulley)",
                "problem": (
                    r"A boat is being pulled toward a dock by a rope attached to the bow of the boat and passing "
                    r"through a pulley on the dock that is $5\text{ feet}$ higher than the bow. If the rope is pulled "
                    r"in at a constant rate of $2\text{ ft/s}$ ($\frac{dc}{dt} = -2$), find $\frac{da}{dt}$ (in $\text{ft/s}$), "
                    r"the rate of change of the horizontal distance $a$ between the boat and the dock, at the instant "
                    r"when the boat is $12\text{ feet}$ away from the dock ($a = 12$)."
                ),
                "formula": r"$a^2 + b^2 = c^2$",
                "answer_val": -13.0 / 6.0,
                "answer_disp": r"$-\frac{13}{6}\text{ ft/s}$ ($\approx -2.17\text{ ft/s}$)"
            },
            {
                "title": "Lock 2: Linear Approximation",
                "problem": (
                    r"Find the linearization $L(x)$ of the function $f(x) = \sqrt[3]{x + 19}$ centered at $a = 8$, "
                    r"and use $L(x)$ to approximate the value of $\sqrt[3]{26.73}$."
                ),
                "formula": r"$L(x) = f(a) + f'(a)(x - a)$",
                "answer_val": 2.99,
                "answer_disp": r"$2.99$"
            },
            {
                "title": "Lock 3: Mean Value Theorem",
                "problem": (
                    r"The function $f(x) = x + \frac{4}{x}$ satisfies the hypotheses of the Mean Value Theorem on the "
                    r"closed interval $[1, 2]$. Find the value of $c$ in $(1, 2)$ that satisfies the conclusion of the theorem."
                ),
                "formula": r"$f'(c) = \frac{f(b) - f(a)}{b - a}$",
                "answer_val": math.sqrt(2.0),
                "answer_disp": r"$\sqrt{2}$ ($\approx 1.414$)"
            },
            {
                "title": "Lock 4: Extrema of a Polynomial",
                "problem": (
                    r"Consider the polynomial function $f(x) = 3x^4 - 8x^3 + 6x^2 + 1$. Find the **minimum value** "
                    r"(the $y$-coordinate of the local and absolute minimum point) of $f(x)$."
                ),
                "formula": r"Critical numbers occur where $f'(x) = 0$ or $f'(x)$ does not exist.",
                "answer_val": 1.0,
                "answer_disp": r"$1$ (at the point $(0, 1)$)"
            },
            {
                "title": "Lock 5: L'Hôpital's Rule",
                "problem": (
                    r"Evaluate the following limit: $$\lim_{x \to 0} \frac{\sin(3x) - 3x}{x^3}$$"
                ),
                "formula": r"L'Hôpital's Rule (for $\frac{0}{0}$ or $\frac{\infty}{\infty}$): $\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$",
                "answer_val": -4.5,
                "answer_disp": r"$-\frac{9}{2}$ or $-4.5$"
            },
            {
                "title": "Lock 6: Profit Optimization (Final Lock)",
                "problem": (
                    r"A small electronics company produces and sells $x$ custom keyboards per week. The price per keyboard "
                    r"(in dollars) is modeled by $p(x) = 220 - 0.5x$, and the total weekly cost (in dollars) is "
                    r"$C(x) = 1500 + 40x + 0.25x^2$. Determine the weekly production level $x$ (number of keyboards) "
                    r"that **maximizes weekly profit**."
                ),
                "formula": r"$\text{Revenue } R(x) = x \cdot p(x)$  and  $\text{Profit } P(x) = R(x) - C(x)$",
                "answer_val": 120.0,
                "answer_disp": r"$120\text{ keyboards}$ (Max weekly profit: $\$9,300$)"
            }
        ]
    },
    "Team 2 — Bravo Vault": {
        "color": "🔴",
        "passcode": ["6", "2", "9", "5", "7", "3"],
        "locks": [
            {
                "title": "Lock 1: Related Rates (Dock & Pulley)",
                "problem": (
                    r"A boat is being pulled toward a dock by a rope attached to the bow of the boat and passing "
                    r"through a pulley on the dock that is $8\text{ feet}$ higher than the bow. If the rope is pulled "
                    r"in at a constant rate of $3\text{ ft/s}$ ($\frac{dc}{dt} = -3$), find $\frac{da}{dt}$ (in $\text{ft/s}$), "
                    r"the rate of change of the horizontal distance $a$ between the boat and the dock, at the instant "
                    r"when the boat is $15\text{ feet}$ away from the dock ($a = 15$)."
                ),
                "formula": r"$a^2 + b^2 = c^2$",
                "answer_val": -3.4,
                "answer_disp": r"$-\frac{17}{5}\text{ ft/s}$ or $-3.4\text{ ft/s}$"
            },
            {
                "title": "Lock 2: Linear Approximation",
                "problem": (
                    r"Find the linearization $L(x)$ of the function $f(x) = \sqrt[3]{x + 56}$ centered at $a = 8$, "
                    r"and use $L(x)$ to approximate the value of $\sqrt[3]{63.52}$."
                ),
                "formula": r"$L(x) = f(a) + f'(a)(x - a)$",
                "answer_val": 3.99,
                "answer_disp": r"$3.99$"
            },
            {
                "title": "Lock 3: Mean Value Theorem",
                "problem": (
                    r"The function $f(x) = x + \frac{9}{x}$ satisfies the hypotheses of the Mean Value Theorem on the "
                    r"closed interval $[1, 3]$. Find the value of $c$ in $(1, 3)$ that satisfies the conclusion of the theorem."
                ),
                "formula": r"$f'(c) = \frac{f(b) - f(a)}{b - a}$",
                "answer_val": math.sqrt(3.0),
                "answer_disp": r"$\sqrt{3}$ ($\approx 1.732$)"
            },
            {
                "title": "Lock 4: Extrema of a Polynomial",
                "problem": (
                    r"Consider the polynomial function $f(x) = 3x^4 - 16x^3 + 24x^2 + 5$. Find the **minimum value** "
                    r"(the $y$-coordinate of the local and absolute minimum point) of $f(x)$."
                ),
                "formula": r"Critical numbers occur where $f'(x) = 0$ or $f'(x)$ does not exist.",
                "answer_val": 5.0,
                "answer_disp": r"$5$ (at the point $(0, 5)$)"
            },
            {
                "title": "Lock 5: L'Hôpital's Rule",
                "problem": (
                    r"Evaluate the following limit: $$\lim_{x \to 0} \frac{\sin(2x) - 2x}{x^3}$$"
                ),
                "formula": r"L'Hôpital's Rule (for $\frac{0}{0}$ or $\frac{\infty}{\infty}$): $\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$",
                "answer_val": -4.0 / 3.0,
                "answer_disp": r"$-\frac{4}{3}$ ($\approx -1.333$)"
            },
            {
                "title": "Lock 6: Profit Optimization (Final Lock)",
                "problem": (
                    r"A boutique audio company produces and sells $x$ custom headphones per week. The price per pair "
                    r"(in dollars) is modeled by $p(x) = 260 - 0.6x$, and the total weekly cost (in dollars) is "
                    r"$C(x) = 1200 + 50x + 0.15x^2$. Determine the weekly production level $x$ (number of headphones) "
                    r"that **maximizes weekly profit**."
                ),
                "formula": r"$\text{Revenue } R(x) = x \cdot p(x)$  and  $\text{Profit } P(x) = R(x) - C(x)$",
                "answer_val": 140.0,
                "answer_disp": r"$140\text{ headphones}$ (Max weekly profit: $\$13,500$)"
            }
        ]
    }
}

# --- SESSION STATE INITIALIZATION ---
if "solved_locks" not in st.session_state:
    st.session_state.solved_locks = {v: set() for v in VAULT_VERSIONS}
if "vault_opened" not in st.session_state:
    st.session_state.vault_opened = {v: False for v in VAULT_VERSIONS}

# --- HEADER & VERSION SELECTOR ---
st.title("🔐 Unlock the Vault: AP Calculus Race")
st.markdown(
    "Solve all **6 Calculus problems** to reveal the **6 digits** of your team's vault passcode. "
    "Enter the complete 6-digit combination into the keypad at the bottom to crack open your vault first!"
)

sel_col, name_col, reset_col = st.columns([1.5, 1.5, 0.8])
with sel_col:
    selected_version = st.selectbox("Select Your Team's Vault Version:", list(VAULT_VERSIONS.keys()))
with name_col:
    team_members = st.text_input("Team Members:", placeholder="Enter your names")
with reset_col:
    st.write("")
    st.write("")
    if st.button("🔄 Reset This Vault", use_container_width=True):
        st.session_state.solved_locks[selected_version] = set()
        st.session_state.vault_opened[selected_version] = False
        st.rerun()

v_data = VAULT_VERSIONS[selected_version]
solved_set = st.session_state.solved_locks[selected_version]
passcode_digits = v_data["passcode"]

# --- LIVE PASSCODE TRACKER DISPLAY ---
st.divider()
st.subheader(f"{v_data['color']} {selected_version} — Collected Passcode Digits ({len(solved_set)} / 6)")

digit_cols = st.columns(6)
for idx in range(6):
    with digit_cols[idx]:
        with st.container(border=True):
            st.caption(f"Digit #{idx + 1}")
            if idx in solved_set:
                st.markdown(f"## 🔓 `{passcode_digits[idx]}`")
            else:
                st.markdown("## 🔒 `?`")

# --- 6 CALCULUS CHALLENGES ---
st.divider()
st.header("Calculus Security Locks")
st.caption("Tip: You can enter integers (`120`), fractions (`-13/6`), square roots (`sqrt(2)`), or decimals rounded to at least two decimal places (`2.99`).")

for idx, lock in enumerate(v_data["locks"]):
    is_solved = idx in solved_set
    status_icon = "✅ UNLOCKED" if is_solved else "🔒 LOCKED"

    with st.container(border=True):
        st.subheader(f"{lock['title']} — {status_icon}")
        st.markdown(lock["problem"])
        st.info(f"**Given Formula:** {lock['formula']}")

        if is_solved:
            st.success(
                f"🎉 **Correct!** Answer: {lock['answer_disp']}  |  "
                f"**Vault Digit #{idx + 1} Revealed:** **`{passcode_digits[idx]}`**"
            )
        else:
            in_col, btn_col = st.columns([3, 1])
            with in_col:
                user_raw = st.text_input(
                    f"Enter your answer for Lock {idx + 1}:",
                    key=f"input_{selected_version}_{idx}",
                    placeholder="e.g., -13/6, 2.99, or sqrt(2)"
                )
            with btn_col:
                st.write("")
                st.write("")
                check_clicked = st.button("Check Answer", key=f"btn_{selected_version}_{idx}", use_container_width=True)

            if check_clicked:
                parsed = parse_math_answer(user_raw)
                if parsed is None:
                    st.error("⚠️ Please enter a valid number, fraction, or square root (such as `-13/6`, `2.99`, or `sqrt(2)`).")
                elif abs(parsed - lock["answer_val"]) <= 0.02:
                    st.session_state.solved_locks[selected_version].add(idx)
                    st.rerun()
                else:
                    st.error("❌ Incorrect value — check your derivatives, signs, and arithmetic, then try again!")

# --- FINAL VAULT KEYPAD ---
st.divider()
st.header("🏦 Final Vault Keypad")

full_code = "".join(passcode_digits)

if st.session_state.vault_opened[selected_version]:
    st.balloons()
    who = team_members.strip() if team_members.strip() else selected_version
    st.success(
        f"🏆 **VAULT UNLOCKED!** Congratulations **{who}**! You cracked **{selected_version}** "
        f"with passcode **`{full_code}`**! Raise your hand to claim victory!"
    )
else:
    if len(solved_set) < 6:
        st.info(f"Solve all 6 locks above to reveal every digit of your passcode ({6 - len(solved_set)} remaining).")

    k_col1, k_col2 = st.columns([2, 1])
    with k_col1:
        code_attempt = st.text_input(
            "Enter the 6-Digit Vault Passcode:",
            max_chars=6,
            placeholder="######",
            key=f"keypad_{selected_version}"
        )
    with k_col2:
        st.write("")
        st.write("")
        if st.button("🔓 UNLOCK VAULT", type="primary", use_container_width=True):
            if code_attempt.strip() == full_code:
                st.session_state.vault_opened[selected_version] = True
                st.rerun()
            else:
                st.error("🚨 **ACCESS DENIED!** Incorrect 6-digit passcode.")
