import pandas as pd

final = pd.DataFrame()

for i in range(2, 18):
    if (i == 1 or i == 12): continue
    dat = pd.read_pickle(f"S{i}/S{i}.pkl")
    HR = pd.read_csv(f"S{i}/S{i}_E4_Data/HR.csv", header=None)
    BVP = pd.read_csv(f"S{i}/S{i}_E4_Data/BVP.csv", header=None)
    if (HR.loc[0][0] - BVP.loc[0][0] > 0):
        time_diff = round(HR.loc[0][0] - BVP.loc[0][0])
        BVP_started_after = False
    else:
        time_diff = round(BVP.loc[0][0] - HR.loc[0][0])
        BVP_started_after = True

    HR = HR[2:].reset_index(drop=True)
    BVP = BVP[2:].reset_index(drop=True)

    # BVP is 64 Hz, HR is 1 Hz

    if (len(BVP) < len(dat["signal"]["wrist"]["BVP"])): raise Exception("BVP data can be shorter doofus")
    # Find first 5 values in sync data
    initSeq = dat["signal"]["wrist"]["BVP"][0:5].tolist()
    seq = [0, 0, 0, 0, 0]
    for count, elem in enumerate(initSeq):
        seq[count] = elem[0]

    # Find the correct index in the HR data

    m = BVP[0].rolling(len(seq)).apply(lambda x: x.eq(seq).all())
    start = m[m.eq(1)].index[0] - 3
    end = start + len(dat["signal"]["wrist"]["BVP"]) - 1
    if (end > len(BVP)): raise Exception("BVP ended before pkl doofus")

    # Extract HR data
    # HR sensor measurred before BVP
    if (BVP_started_after):
        HR_start = start + time_diff * 64
        HR_end = end + time_diff * 64
        ACC_out = pd.DataFrame(dat["signal"]["wrist"]["ACC"][::32]).reset_index(drop=True)
        HR_out = HR[round(HR_start/64):round(HR_end/64)]
        HR_out = HR_out.reset_index(drop=True)
        LAB_out = pd.DataFrame(dat["label"][::700]).rename(columns={0: "label"})

    # BVP sensor started measuring before HR
    else:
        hr_start = start - time_diff * 64
        hr_end = end - time_diff * 64
        ACC_out = pd.DataFrame(dat["signal"]["wrist"]["ACC"][::32]).reset_index(drop=True)
        HR_out = HR[round(hr_start/64):round(hr_end/64)]
        HR_out = HR_out.reset_index(drop=True)
        LAB_out = pd.DataFrame(dat["label"][::700]).rename(columns={0: "label"})

    HR_out.rename(columns={0: "HR"}, inplace=True)
    ACC_out.rename(columns={0: "acc_x", 1: "acc_y", 2: "acc_z"}, inplace=True)
    dat_out = pd.concat([HR_out, ACC_out, LAB_out], axis=1).dropna()
    final = pd.concat([final, dat_out])

final.to_csv("wesad_sync.csv", index=False)