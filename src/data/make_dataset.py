import pandas as pd
from glob import glob
# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
single_file_acc = pd.read_csv("C:/Users/USER/Desktop/pfa2025/dataScience/data/raw/dataset/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")
single_file_ge = pd.read_csv("C:/Users/USER/Desktop/pfa2025/dataScience/data/raw/dataset/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")
# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files =  glob("C:/Users/USER/Desktop/pfa2025/dataScience/data/raw/dataset/*.csv")
len(files)
# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
data_path = "C:/Users/USER/Desktop/pfa2025/dataScience/data/raw/dataset\\"
f = files[100]
participants = f.split("-")[0].replace(data_path,"")
label = f.split("-")[1]
category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
df=pd.read_csv(f)
df["participants"]=participants
df["label"]=label
df["category"]=category
df.head()
# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------

acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

acc_set = 1
gyr_set = 1

for f in files:
    participants = f.split("-")[0].replace(data_path,"")
    label = f.split("-")[1]
    category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
    df=pd.read_csv(f)
    df["participants"]=participants
    df["label"]=label
    df["category"]=category
    
    if "Accelerometer" in f :
        df["set"]=acc_set
        acc_set+=1
        acc_df =pd.concat([acc_df,df])
    if "Gyroscope" in f:
        df["set"]=gyr_set
        gyr_set+=1
        gyr_df = pd.concat([gyr_df,df])
        
# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------
acc_df.index = pd.to_datetime(acc_df["epoch (ms)"] , unit="ms")
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"] , unit="ms")

del acc_df["epoch (ms)"]
del acc_df["time (01:00)"]
del acc_df["elapsed (s)"]

del gyr_df["epoch (ms)"]
del gyr_df["time (01:00)"]
del gyr_df["elapsed (s)"]
# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
def read_data(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1
    
    data_path = "C:/Users/USER/Desktop/pfa2025/dataScience/data/raw/dataset\\"


    for f in files:
        participants = f.split("-")[0].replace(data_path,"")
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
        df=pd.read_csv(f)
        df["participants"]=participants
        df["label"]=label
        df["category"]=category
        
        if "Accelerometer" in f :
            df["set"]=acc_set
            acc_set+=1
            acc_df =pd.concat([acc_df,df])
        if "Gyroscope" in f:
            df["set"]=gyr_set
            gyr_set+=1
            gyr_df = pd.concat([gyr_df,df])
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"] , unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"] , unit="ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]
    
    return acc_df , gyr_df


acc_df1 , gyr_df2 = read_data(files)

# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------

data_merged = pd.concat([acc_df1.iloc[:,:3],gyr_df2],axis=1)
# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz
sampling = {
    'x-axis (g)':"mean", 
    'y-axis (g)':"mean", 
    'z-axis (g)':"mean", 
    'x-axis (deg/s)':"mean",
    'y-axis (deg/s)':"mean", 
    'z-axis (deg/s)':"mean", 
    'participants':"last", 
    'label':"last", 
    'category':"last",
    'set':"last"
}
data_merged[:100].resample(rule="200ms").apply(sampling)
days =[g for n , g in data_merged.groupby(pd.Grouper(freq="D"))]
data_resampled = pd.concat([df.resample(rule="200ms").apply(sampling).dropna() for df in days])
data_resampled.info()
data_resampled["set"]=data_resampled["set"].astype(int)


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle("C:/Users/USER/Desktop/pfa2025/dataScience/data/intermim/data_resampled.pkl")