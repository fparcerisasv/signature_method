import os

def main():
    directory = "experimental_results"
    metrics = {"raw": [], "signature": [], "pca": []}  
    for sub_dir in os.listdir(directory):
        k = int(sub_dir.split("_")[1])
        for file in os.listdir(os.path.join(directory, sub_dir)):
            if file.endswith(".csv"):
                type = file.split("_")[0]
                with open(os.path.join(directory,sub_dir, file)) as f:
                    auc_roc = []
                    auc_pr = []
                    time = []
                    headers = f.readline().split(",")   
                    for line in f:
                        auc_roc.append(float(line.split(",")[1]))
                        auc_pr.append(float(line.split(",")[2]))
                        time.append(float(line.split(",")[3]))
                    mean_auc_roc = sum(auc_roc) / len(auc_roc)
                    mean_auc_pr = sum(auc_pr) / len(auc_pr)
                    mean_time = sum(time) / len(time)
                    metrics[type].append({"k": k, "auc_roc": mean_auc_roc, "auc_pr": mean_auc_pr, "time": mean_time})
    for key in metrics.keys():
        print(key, metrics[key])

if __name__ == "__main__":
    main()
