import math
from datetime import datetime


def calculate_memory_strength(memory_strength, last_practice) -> float:
    now = datetime.now()
    time_since_last_practice = (now - last_practice).days
    new_memory_strength = memory_strength
    print(f'Prev Strength of {'Character'} is {new_memory_strength}')

    # Decay Theory: memory strength decays over time
    decay_rate = 0.05  # adjust this value to control the decay rate
    new_memory_strength *= math.exp(-decay_rate * time_since_last_practice)

    # Forgetting Curve: rapid decline in memory retention initially, then levels off
    forgetting_curve_rate = 0.2  # adjust this value to control the forgetting curve rate
    new_memory_strength *= math.pow(1 - forgetting_curve_rate, time_since_last_practice)

    new_memory_strength = max(0, min(1, new_memory_strength))

    memory_strength = new_memory_strength
    print(f'Now Strength of {'Character'} is {new_memory_strength}')
    return memory_strength

v = calculate_memory_strength(memory_strength=0.8, last_practice=datetime(2024, 5, 1))
print('v ', v )