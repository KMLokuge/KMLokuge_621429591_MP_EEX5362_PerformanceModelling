import simpy
import pandas as pd

# ---------------------------------------------------------
# Morning session dataset based on Matale General Hospital
# ---------------------------------------------------------
morning_data = [
    {"Patient_ID": "M001", "Arrival": 0, "Service": 10},
    {"Patient_ID": "M002", "Arrival": 2, "Service": 9},
    {"Patient_ID": "M003", "Arrival": 3, "Service": 11},
    {"Patient_ID": "M004", "Arrival": 5, "Service": 8},
    {"Patient_ID": "M005", "Arrival": 6, "Service": 12},
    {"Patient_ID": "M006", "Arrival": 8, "Service": 10},
    {"Patient_ID": "M007", "Arrival": 10, "Service": 9},
    {"Patient_ID": "M008", "Arrival": 12, "Service": 11},
    {"Patient_ID": "M009", "Arrival": 14, "Service": 10},
    {"Patient_ID": "M010", "Arrival": 16, "Service": 8},
    {"Patient_ID": "M011", "Arrival": 19, "Service": 12},
    {"Patient_ID": "M012", "Arrival": 22, "Service": 9},
    {"Patient_ID": "M013", "Arrival": 25, "Service": 11},
    {"Patient_ID": "M014", "Arrival": 28, "Service": 10},
    {"Patient_ID": "M015", "Arrival": 31, "Service": 12},
    {"Patient_ID": "M016", "Arrival": 35, "Service": 9},
    {"Patient_ID": "M017", "Arrival": 40, "Service": 11},
    {"Patient_ID": "M018", "Arrival": 45, "Service": 10},
    {"Patient_ID": "M019", "Arrival": 50, "Service": 12},
    {"Patient_ID": "M020", "Arrival": 56, "Service": 9},
    {"Patient_ID": "M021", "Arrival": 62, "Service": 11},
    {"Patient_ID": "M022", "Arrival": 69, "Service": 10},
    {"Patient_ID": "M023", "Arrival": 76, "Service": 12},
    {"Patient_ID": "M024", "Arrival": 84, "Service": 9},
    {"Patient_ID": "M025", "Arrival": 92, "Service": 11},
]

# ---------------------------
# Patient waiting process
# ---------------------------
def patient_process(env, patient, doctors, records):
    arrival = patient["Arrival"]
    service_time = patient["Service"]
    
    # Wait until patient arrives
    yield env.timeout(arrival - env.now)
    
    with doctors.request() as request:
        yield request
        start_time = env.now
        wait_time = start_time - arrival
        yield env.timeout(service_time)
        departure = env.now
        
        records.append({
            "Patient_ID": patient["Patient_ID"],
            "Arrival_Time": arrival,
            "Service_Start_Time": round(start_time, 2),
            "Wait_Time": round(wait_time, 2),
            "Service_Time": service_time,
            "Departure_Time": round(departure, 2)
        })

# --------------------------------------------
# Run simulation with flexible doctor count
# --------------------------------------------

# current doctor count in an OPD room is 3

def run_morning_session(patient_data, num_doctors=3):
    env = simpy.Environment()
    doctors = simpy.Resource(env, capacity=num_doctors)
    records = []
    
    for patient in patient_data:
        env.process(patient_process(env, patient, doctors, records))
    
    env.run()
    
    df = pd.DataFrame(records).sort_values("Arrival_Time").reset_index(drop=True)
    print(f"\n--- Morning Session Table ({num_doctors} doctors) ---")
    print(df)
    
    print(f"\n--- Morning Session Performance Summary ({num_doctors} doctors) ---")
    print(f"Number of patients served: {len(df)}")
    print(f"Average waiting time: {df['Wait_Time'].mean():.2f} minutes")
    print(f"Maximum waiting time: {df['Wait_Time'].max():.2f} minutes")
    print(f"Minimum waiting time: {df['Wait_Time'].min():.2f} minutes")

# ---------------------------------------------
# Example usage: change number of doctors here
# ---------------------------------------------

# increase doctor count to 4 and 5

for doctors_count in [3, 4, 5]:
    run_morning_session(morning_data, num_doctors=doctors_count)
