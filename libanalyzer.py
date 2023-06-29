import json
import csv
import streamlit as st
import tempfile
from jsonschema import validate
from json2html import json2html

def count_qid_nodes(data):
    count = 0
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "qid":
                count += 1
            if isinstance(value, dict) or isinstance(value, list):
                count += count_qid_nodes(value)
    elif isinstance(data, list):
        for item in data:
            count += count_qid_nodes(item)
    return count

def generate_schema(data):
    schema = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                schema[key] = generate_schema(value)
            else:
                schema[key] = str(type(value).__name__)
    elif isinstance(data, list):
        if data:
            schema = [generate_schema(data[0])]
    return schema

def visualize_schema(schema):
    html = json2html.convert(json=schema)
    st.markdown(html, unsafe_allow_html=True)


def export_csv(data):
    rows = []
    if isinstance(data, dict):
        row = []
        if "qid" in data:
            row.append(data["qid"])
        else:
            row.append("")
        if "details" in data:
            row.append(data["details"])
        else:
            row.append("")
        rows.append(row)
        for value in data.values():
            if isinstance(value, dict) or isinstance(value, list):
                rows.extend(export_csv(value))
            elif isinstance(value, str):
                rows[-1].append(value.encode("utf-8"))  # Encode the anstext field as bytes
    elif isinstance(data, list):
        for item in data:
            rows.extend(export_csv(item))
    return rows
    
def main():
    st.title("JSON Schema Visualizer and QID Node Counter")

    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            schema = generate_schema(data)
            visualize_schema(schema)
            qid_count = count_qid_nodes(data)
            st.write(f"Total Number of 'qid' Nodes: {qid_count}")
            
            if st.button("Export CSV"):
                rows = export_csv(data)
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    writer = csv.writer(temp_file)
                    writer.writerows(rows)
                    temp_file.close()
                    st.download_button(
                        "Download CSV",
                        temp_file.name,
                        mime="text/csv",
                        file_name="output.csv"
                    )
        except json.JSONDecodeError:
            st.error("Invalid JSON file format.")

if __name__ == "__main__":
    main()

