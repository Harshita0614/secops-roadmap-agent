import pandas as pd

def get_step_status(xlsx_path: str = "C:/Users/Harshita Mehta/OneDrive/Desktop/secops-roadmap-agent/demo_data/Project -Google Chronicle SIEM tracker.xlsx") -> dict:
    try:
        sheet_name = "SIEM Usecases"
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name)

        print("✅ Extracting status from columns: 'Rule Name' and 'Status'")

        # Directly use correct columns
        step_col = "Rule Name"
        status_col = "Status"

        status_dict = {}
        for _, row in df.iterrows():
            step = str(row[step_col]).strip()
            status = str(row[status_col]).strip()
            if step and status:
                status_dict[step] = status

        return status_dict

    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return {}
