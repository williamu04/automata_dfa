import streamlit as st

def render_table(dfa_visual):
    table_header = ["State"] + sorted(dfa_visual["alphabet"]) + ["Accept State?"]
    table_rows = []

    for state in sorted(dfa_visual["states"]):
        row = [f"**{state}**" + (" (start)" if state == dfa_visual["start_state"] else "")]
        for symbol in sorted(dfa_visual["alphabet"]):
            dest = dfa_visual["transitions"].get(state, {}).get(symbol, "∅")
            row.append(dest)
        row.append("✓" if state in dfa_visual["accept_states"] else "✗")
        table_rows.append(row)

    # Convert to markdown table
    table_md = "| " + " | ".join(table_header) + " |\n"
    table_md += "| " + " | ".join(["---"] * len(table_header)) + " |\n"
    for row in table_rows:
        table_md += "| " + " | ".join(map(str, row)) + " |\n"

    st.markdown(table_md)