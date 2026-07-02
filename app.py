import streamlit as st
import math

def erlang_b(m: int, A: float) -> float:
    b = 1.0
    for n in range(1, m + 1):
        b = (A * b) / (n + A * b)
    return b

def erlang_c(m: int, A: float) -> float:
    if m <= A:
        return 1.0  # system unstable/saturated, always queues
    eb = erlang_b(m, A)
    return (m * eb) / (m - A * (1 - eb))

def service_level(m: int, A: float, aht_seconds: float,
                  target_answer_seconds: float) -> float:
    if m <= A:
        return 0.0
    ec = erlang_c(m, A)
    exponent = -(m - A) * (target_answer_seconds / aht_seconds)
    return 1.0 - ec * math.exp(exponent)

def average_speed_of_answer(m: int, A: float, aht_seconds: float) -> float:
    if m <= A:
        return float('inf')
    ec = erlang_c(m, A)
    return (ec * aht_seconds) / (m - A)

def main():
    st.title("Erlang C Workforce Calculator — built by Hatem Shalaby | github.com/HatemShalaby")

    calls_per_hour = st.number_input("Calls per hour", min_value=1, value=100)
    avg_handle_time_seconds = st.number_input("Average handle time (seconds)", min_value=1, value=300)
    target_service_level = st.slider("Target service level", 0.50, 0.99, 0.80)
    target_answer_time_seconds = st.number_input("Target answer time (seconds)", min_value=1, value=20)
    shrinkage_percent = st.slider("Shrinkage percent (%)", 0.0, 50.0, 30.0)

    A = (calls_per_hour * avg_handle_time_seconds) / 3600.0

    raw_agents_found = None
    achieved_service_level = 0.0
    aht = avg_handle_time_seconds
    target_answer = target_answer_time_seconds
    target_sl = target_service_level

    min_m = math.ceil(A) + 1
    max_m = min_m + 500

    for m in range(min_m, max_m + 1):
        sl = service_level(m, A, aht, target_answer)
        if sl >= target_sl:
            raw_agents_found = m
            achieved_service_level = sl
            break

    if raw_agents_found is None:
        raise ValueError("Target service level unreachable")

    final_headcount = math.ceil(raw_agents_found / (1 - shrinkage_percent / 100))
    asa = average_speed_of_answer(raw_agents_found, A, aht)

    st.subheader("Results")
    st.write(f"**Traffic Intensity (Erlangs):** {A:.2f}")
    st.write(f"**Raw Agents Required (before shrinkage):** {raw_agents_found}")
    st.write(f"**Shrinkage-Adjusted Headcount:** {final_headcount}")

    achieved_sl_percent = achieved_service_level * 100
    st.write(f"**Achieved Service Level (%):** {achieved_sl_percent:.2f}%")

    if math.isinf(asa):
        st.write("**Average Speed of Answer (seconds):** N/A (understaffed)")
    else:
        st.write(f"**Average Speed of Answer (seconds):** {asa:.2f}")

    # Prepare chart data
    base_m = raw_agents_found - 3
    if base_m < min_m:
        base_m = min_m
    m_values = range(base_m, base_m + 7)
    target_percent = target_sl * 100

    data = []
    for m in m_values:
        sl = service_level(m, A, aht, target_answer) * 100
        data.append({"Agents": m, "Service Level (%)": sl})

    # Add target column (constant)
    for row in data:
        row["Target (%)"] = target_percent

    st.line_chart(data, x="Agents", y=["Service Level (%)", "Target (%)"])

if __name__ == "__main__":
    main()