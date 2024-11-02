import json

def parse_medical_data(json_string):
    try:
        # Clean up the input string by removing Markdown formatting
        cleaned_string = json_string.replace("```json\n", "").replace("```", "").strip()
        
        # Parse the cleaned string into a Python dictionary
        data = json.loads(cleaned_string)

        # Extract relevant fields from the parsed data
        patient_info = {
            "patientName": data.get("patientName", ""),
            "age": data.get("age", ""),
            "medicines": [],
            "healthData": [],
            "tests": data.get("test", [])
        }
        
        # Extract medicine data
        for medicine in data.get("data", []):
            medicine_entry = {
                "medicineName": medicine.get("medicineName", ""),
                "takingTime": medicine.get("takingTime", ""),
                "isNeedEmptyStomach": medicine.get("isNeedEmptyStomach", ""),
                "medicineUsage": medicine.get("medicineUsage", ""),
                "sideEffect": medicine.get("sideEffect", "")
            }
            patient_info["medicines"].append(medicine_entry)

        # Extract health data
        for health in data.get("healthData", []):
            health_entry = {
                "type": health.get("type", ""),
                "value": health.get("value", "")
            }
            patient_info["healthData"].append(health_entry)

        return patient_info
    
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        return None





# Example usage
json_string = "```json\n{\n  \"patientName\": \"DEMO PATIENT\",\n  \"age\": \"36\",\n  \"data\": [\n    {\n      \"medicineName\": \"TAB. DEMO MEDICINE 1\",\n      \"takingTime\": \"1+0+1\",\n      \"isNeedEmptyStomach\": \"yes-no-x\",\n      \"medicineUsage\": \"Before Food\",\n      \"sideEffect\": \"\"\n    },\n    {\n      \"medicineName\": \"CAP. DEMO MEDICINE 2\",\n      \"takingTime\": \"1+0+1\",\n      \"isNeedEmptyStomach\": \"yes-no-x\",\n      \"medicineUsage\": \"Before Food\",\n      \"sideEffect\": \"\"\n    },\n    {\n      \"medicineName\": \"TAB. DEMO MEDICINE 3\",\n      \"takingTime\": \"1+1+1\",\n      \"isNeedEmptyStomach\": \"no-no-yes\",\n      \"medicineUsage\": \"After Food\",\n      \"sideEffect\": \"\"\n    },\n    {\n      \"medicineName\": \"TAB. DEMO MEDICINE 4\",\n      \"takingTime\": \"1+0+0\",\n      \"isNeedEmptyStomach\": \"yes-no-x\",\n      \"medicineUsage\": \"After Food\",\n      \"sideEffect\": \"\"\n    }\n  ],\n  \"healthData\": [\n    {\n      \"type\": \"Temperature\",\n      \"value\": \"36°C\"\n    },\n    {\n      \"type"

result = parse_medical_data(json_string)
print(result)
