import numpy as np
import matplotlib.pyplot as plt
import glob
import os

WALKING_PATH = 'datasets pulish/walking/*.csv'
JOGGING_PATH = 'datasets pulish/jogging/*.csv'

fs = 100
maxNumM = 100

def AllanDeviation(data, fs, maxNumM=100):

    data = data[~np.isnan(data)]
    N = len(data)
    ts = 1.0 / fs
    # Cluster sizes
    m = np.unique(
        np.geomspace(1, max(2, N // 2), num=maxNumM).astype(int))

    tau = m * ts
    adev = np.zeros(len(m))
    for i, mi in enumerate(m):
        if (N - 2 * mi) <= 0:
            continue
        sum_sq = np.sum((data[2*mi:N]- 2*data[mi:N-mi]+ data[0:N-2*mi])**2)
        allan_var = sum_sq / (2 * (tau[i]**2) * (N - 2*mi))
        adev[i] = np.sqrt(allan_var)

    return tau, adev


def load_umafall_data(filename):

    data = np.genfromtxt(
        filename,
        delimiter=';',
        comments='%',
        dtype=float)

  
    data = data[~np.isnan(data).any(axis=1)]
    return data

def process_dataset(data):

    gx = data[:, 2]
    gy = data[:, 3]
    gz = data[:, 4]

    ts = 1.0 / fs

    # Integrated angle
    thetax = np.cumsum(gx) * ts
    thetay = np.cumsum(gy) * ts
    thetaz = np.cumsum(gz) * ts

    return gx, gy, gz, thetax, thetay, thetaz

def signal_energy(x, y, z):
    return np.mean(x**2 + y**2 + z**2)

walking_files = glob.glob(WALKING_PATH)
jogging_files = glob.glob(JOGGING_PATH)

print("TOTAL DATASET")
print(f'Walking files : {len(walking_files)}')
print(f'Jogging files : {len(jogging_files)}')

if len(walking_files) == 0:
    print("\nERROR: No walking CSV files found.")
    exit()

if len(jogging_files) == 0:
    print("\nERROR: No jogging CSV files found.")
    exit()

walking_energies = []
jogging_energies = []

walk_gx_all = []
walk_gy_all = []
walk_gz_all = []

jog_gx_all = []
jog_gy_all = []
jog_gz_all = []

walk_adx_all = []
walk_ady_all = []
walk_adz_all = []

jog_adx_all = []
jog_ady_all = []
jog_adz_all = []

walk_tau_all = []
jog_tau_all = []

print("PROCESSING WALKING DATA")

for file in walking_files:
    print(f'Processing: {os.path.basename(file)}')
    data = load_umafall_data(file)
    gx, gy, gz, tx, ty, tz = process_dataset(data)
    # Energy
    energy = signal_energy(gx, gy, gz)
    walking_energies.append(energy)
    # Store raw signal
    walk_gx_all.append(gx)
    walk_gy_all.append(gy)
    walk_gz_all.append(gz)

    # Allan Deviation
    tau_x, adx = AllanDeviation(tx, fs, maxNumM)
    tau_y, ady = AllanDeviation(ty, fs, maxNumM)
    tau_z, adz = AllanDeviation(tz, fs, maxNumM)

    walk_tau_all.append(tau_x)

    walk_adx_all.append(adx)
    walk_ady_all.append(ady)
    walk_adz_all.append(adz)

print("PROCESSING JOGGING DATA")

for file in jogging_files:

    print(f'Processing: {os.path.basename(file)}')
    data = load_umafall_data(file)
    gx, gy, gz, tx, ty, tz = process_dataset(data)
    # Energy
    energy = signal_energy(gx, gy, gz)
    jogging_energies.append(energy)
    # Store raw signal
    jog_gx_all.append(gx)
    jog_gy_all.append(gy)
    jog_gz_all.append(gz)

    # Allan Deviation
    tau_x2, adx = AllanDeviation(tx, fs, maxNumM)
    tau_y2, ady = AllanDeviation(ty, fs, maxNumM)
    tau_z2, adz = AllanDeviation(tz, fs, maxNumM)

    jog_tau_all.append(tau_x2)

    jog_adx_all.append(adx)
    jog_ady_all.append(ady)
    jog_adz_all.append(adz)

min_walk_len = min(len(x) for x in walk_gx_all)
min_jog_len = min(len(x) for x in jog_gx_all)

walk_gx_avg = np.mean(
    [x[:min_walk_len] for x in walk_gx_all],
    axis=0)

jog_gx_avg = np.mean(
    [x[:min_jog_len] for x in jog_gx_all],
    axis=0)

min_walk_ad_len = min(len(x) for x in walk_adx_all)
min_jog_ad_len = min(len(x) for x in jog_adx_all)

# Walking
walk_adx_avg = np.mean(
    [x[:min_walk_ad_len] for x in walk_adx_all],
    axis=0)

walk_ady_avg = np.mean(
    [x[:min_walk_ad_len] for x in walk_ady_all],
    axis=0)

walk_adz_avg = np.mean(
    [x[:min_walk_ad_len] for x in walk_adz_all],
    axis=0)

walk_tau_avg = np.mean(
    [x[:min_walk_ad_len] for x in walk_tau_all],
    axis=0)

# Jogging
jog_adx_avg = np.mean(
    [x[:min_jog_ad_len] for x in jog_adx_all],
    axis=0)

jog_ady_avg = np.mean(
    [x[:min_jog_ad_len] for x in jog_ady_all],
    axis=0)

jog_adz_avg = np.mean(
    [x[:min_jog_ad_len] for x in jog_adz_all],
    axis=0)

jog_tau_avg = np.mean(
    [x[:min_jog_ad_len] for x in jog_tau_all],
    axis=0)

plt.figure(figsize=(14,6))

plt.plot(walk_gx_avg, label='Walking X-axis')
plt.plot(jog_gx_avg, label='Jogging X-axis')

plt.title('Raw IMU Signal Comparison')

plt.xlabel('Times')
plt.ylabel('Amplitude')

plt.grid(True)
plt.legend()


plt.figure(figsize=(10,6))

plt.plot(walk_tau_avg, walk_adx_avg, label='X-axis')
plt.plot(walk_tau_avg, walk_ady_avg, label='Y-axis')
plt.plot(walk_tau_avg, walk_adz_avg, label='Z-axis')

plt.xscale('log')
plt.yscale('log')

plt.title('Walking - Gyro Allan Deviation')

plt.xlabel('Tau [sec]')
plt.ylabel('Deviation')

plt.grid(True, which='both')
plt.legend()


plt.figure(figsize=(10,6))

plt.plot(jog_tau_avg, jog_adx_avg, label='X-axis')
plt.plot(jog_tau_avg, jog_ady_avg, label='Y-axis')
plt.plot(jog_tau_avg, jog_adz_avg, label='Z-axis')

plt.xscale('log')
plt.yscale('log')

plt.title('Jogging - Gyro Allan Deviation')

plt.xlabel('Tau [sec]')
plt.ylabel('Deviation')

plt.grid(True, which='both')
plt.legend()


plt.figure(figsize=(10,6))

plt.plot(walk_tau_avg, walk_adx_avg, label='Walking X-axis')
plt.plot(jog_tau_avg, jog_adx_avg, label='Jogging X-axis')

plt.xscale('log')
plt.yscale('log')

plt.title('Walking vs Jogging Allan Deviation')

plt.xlabel('Tau [sec]')
plt.ylabel('Deviation')

plt.grid(True, which='both')
plt.legend()


avg_walk_energy = np.mean(walking_energies)
avg_jog_energy = np.mean(jogging_energies)

std_walk = np.std(walking_energies)
std_jog = np.std(jogging_energies)

print("FINAL RESULT")

print(f'Total Walking Data : {len(walking_files)}')
print(f'Total Jogging Data : {len(jogging_files)}')

print()

print(f'Average Walking Energy : {avg_walk_energy:.2f}')
print(f'STD Walking Energy     : {std_walk:.2f}')

print()

print(f'Average Jogging Energy : {avg_jog_energy:.2f}')
print(f'STD Jogging Energy     : {std_jog:.2f}')

print("CONCLUSION")

if avg_jog_energy > avg_walk_energy:

    print(
        "Jogging activity has higher motion energy "
        "and larger dynamic movement compared to walking."
    )

    print(
        "The Allan deviation graph also shows "
        "that jogging produces more unstable "
        "and aggressive motion characteristics."
    )

else:

    print(
        "Walking activity has higher motion energy "
        "than jogging."
    )

plt.show()