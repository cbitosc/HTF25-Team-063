import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from PIL import Image
import glob
import time

st.set_page_config(page_title="Traffic Violation Dashboard", layout="wide")

st.title("🚦 AI Traffic Violation Detector Dashboard")

# Function to load evidence from images directory
def load_evidence():
    """Load evidence from the evidence/images directory"""
    evidence_list = []
    images_dir = "evidence/images/"

    if not os.path.exists(images_dir):
        return evidence_list

    # Get all image files
    image_files = glob.glob(os.path.join(images_dir, "*.jpg"))

    for image_path in image_files:
        filename = os.path.basename(image_path)
        # Parse filename: violation_type_vehicle_id_timestamp.jpg
        parts = filename.replace('.jpg', '').split('_')
        if len(parts) >= 3:
            violation_type = '_'.join(parts[:-2])  # Handle multi-word types like signal_jump
            vehicle_id = parts[-2]
            timestamp_str = parts[-1]

            try:
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            except ValueError:
                timestamp = datetime.now()

            evidence_list.append({
                'violation_type': violation_type,
                'timestamp': timestamp,
                'image_path': image_path,
                'license_plate': f"LP-{vehicle_id}",  # Mock license plate
                'vehicle_id': vehicle_id
            })

    # Sort by timestamp (newest first)
    evidence_list.sort(key=lambda x: x['timestamp'], reverse=True)
    return evidence_list

# Load evidence data
violations = load_evidence()

# Sidebar filters
st.sidebar.header("Filters")
violation_types = ["All"] + list(set([v['violation_type'] for v in violations]))
violation_type = st.sidebar.selectbox("Violation Type", violation_types)
time_range = st.sidebar.selectbox("Time Range", ["Last Hour", "Last 24 Hours", "Last Week", "All Time"])

# Filter violations based on selection
filtered_violations = violations

if violation_type != "All":
    filtered_violations = [v for v in violations if v['violation_type'] == violation_type]

# Time filtering
now = datetime.now()
if time_range == "Last Hour":
    cutoff = now - timedelta(hours=1)
elif time_range == "Last 24 Hours":
    cutoff = now - timedelta(days=1)
elif time_range == "Last Week":
    cutoff = now - timedelta(weeks=1)
else:
    cutoff = datetime.min

filtered_violations = [v for v in filtered_violations if v['timestamp'] >= cutoff]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Recent Violations")

    if filtered_violations:
        for violation in filtered_violations[:20]:  # Show last 20 violations
            with st.expander(f"{violation['violation_type'].replace('_', ' ').title()} - {violation['timestamp'].strftime('%H:%M:%S %d/%m/%Y')}"):
                col_a, col_b = st.columns([1, 2])

                with col_a:
                    try:
                        # Load and display actual evidence image
                        image = Image.open(violation['image_path'])
                        st.image(image, caption="Violation Evidence", use_column_width=True)
                    except Exception as e:
                        st.error(f"Could not load image: {e}")

                with col_b:
                    st.write(f"**Type:** {violation['violation_type'].replace('_', ' ').title()}")
                    st.write(f"**Time:** {violation['timestamp'].strftime('%H:%M:%S %d/%m/%Y')}")
                    st.write(f"**License Plate:** {violation['license_plate']}")
                    st.write(f"**Vehicle ID:** {violation['vehicle_id']}")

                    if st.button("View Full Image", key=f"view_{violation['timestamp']}_{violation['vehicle_id']}"):
                        try:
                            full_image = Image.open(violation['image_path'])
                            st.image(full_image, caption="Full Evidence Image", width=640)
                        except Exception as e:
                            st.error(f"Could not load full image: {e}")

                    if st.button("Download Evidence", key=f"download_{violation['timestamp']}_{violation['vehicle_id']}"):
                        st.success("Evidence downloaded!")
    else:
        st.info("No violations detected in the selected time range.")

with col2:
    st.subheader("Statistics")

    total_violations = len(filtered_violations)
    violation_type_counts = {}
    for v in filtered_violations:
        vt = v['violation_type']
        violation_type_counts[vt] = violation_type_counts.get(vt, 0) + 1

    st.metric("Total Violations", total_violations)

    st.subheader("Violation Types")
    for vt, count in violation_type_counts.items():
        st.metric(vt.replace('_', ' ').title(), count)

    # Violations over time chart
    if filtered_violations:
        st.subheader("Violations Over Time")
        # Group by hour
        hourly_counts = {}
        for v in filtered_violations:
            hour_key = v['timestamp'].strftime('%Y-%m-%d %H:00')
            hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1

        # Sort by time
        sorted_hours = sorted(hourly_counts.items())
        if sorted_hours:
            hours, counts = zip(*sorted_hours)
            chart_data = pd.DataFrame({'Hour': hours, 'Violations': counts})
            st.line_chart(chart_data.set_index('Hour'))

# Footer
st.markdown("---")
st.markdown("**AI Traffic Violation Detector** - Real-time monitoring for safer roads")

if st.sidebar.button("Export Report"):
    if filtered_violations:
        # Create CSV report
        report_data = []
        for v in filtered_violations:
            report_data.append({
                'Violation Type': v['violation_type'],
                'Timestamp': v['timestamp'],
                'License Plate': v['license_plate'],
                'Vehicle ID': v['vehicle_id'],
                'Image Path': v['image_path']
            })

        df = pd.DataFrame(report_data)
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV Report",
            data=csv,
            file_name="violation_report.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.warning("No violations to export.")
