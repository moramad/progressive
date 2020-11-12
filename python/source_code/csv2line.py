import pandas as pd
#convert csv to line protocol;

#convert sample data to line protocol (with nanosecond precision)
df = pd.read_csv("data/BTC_sm_ns.csv")
lines = [“price”
         + ",type=BTC"
         + " "
         + "close=" + str(df["close"][d]) + ","
         + "high=" + str(df["high"][d]) + ","
         + "low=" + str(df["low"][d]) + ","
         + "open=" + str(df["open"][d]) + ","
         + "volume=" + str(df["volume"][d])
         + " " + str(df["time"][d]) for d in range(len(df))]
thefile = open('data/chronograf.txt', 'w')
for item in lines:
    thefile.write("%s\n" % item)