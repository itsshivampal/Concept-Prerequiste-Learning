import pandas as pd


def read_csv_file(df):
    topic_pair_list = {}
    index_length = df.shape[0]
    for i in range(index_length):
        topic_pair_list[i] = {
            'topic_a': df[["topic_a"]].iloc[i].values[0],
            'topic_b': df[["topic_b"]].iloc[i].values[0]
        }
    return topic_pair_list


def swap_cols_csv(df):
    topic_pair_list = {}
    index_length = df.shape[0]
    for i in range(index_length):
        topic_pair_list[i] = {
            'topic_a': df[["topic_b"]].iloc[i].values[0],
            'topic_b': df[["topic_a"]].iloc[i].values[0]
        }
    return topic_pair_list


def count_no_same_pairs(dataset1, dataset2):
    count = 0
    for i in range(len(dataset1)):
        flag = False
        for j in range(len(dataset2)):
            x1 = dataset1[i]
            x2 = dataset2[j]
            if x1["topic_a"] == x2["topic_a"] and x1["topic_b"] == x2["topic_b"]:
                flag = True
        if flag:
            count += 1
    return count


def count_no_opp_pairs(dataset1, dataset2):
    count = 0
    for i in range(len(dataset1)):
        flag = False
        for j in range(len(dataset2)):
            x1 = dataset1[i]
            x2 = dataset2[j]
            if x1["topic_a"] == x2["topic_b"] and x1["topic_b"] == x2["topic_a"]:
                flag = True
        if flag:
            count += 1
    return count



def number_same_pairs(df1, df2):
    dataset1 = read_csv_file(df1)
    dataset2 = read_csv_file(df2)
    count = count_no_same_pairs(dataset1, dataset2)
    return count

def number_opp_pairs(df1, df2):
    dataset1 = read_csv_file(df1)
    dataset2 = read_csv_file(df2)
    count = count_no_opp_pairs(dataset1, dataset2)
    return count



def check_opp_pairs(df):
    dataset1 = read_csv_file(df)
    dataset2 = swap_cols_csv(df)
    count = count_no_same_pairs(dataset1, dataset2)
    return(count)


def compare_datasets(df1, df2):
    given_length = df1.shape[0]
    count1 = number_same_pairs(df1, df2) # count_same_pair
    count2 = number_opp_pairs(df1, df2) # count_opp_pair
    count3 = given_length - count1 - count2 # count_absent_pairs
    return (count1, count2, count3)


def confusion_matrix_formation(count1, count2, count3, count4, count5, count6):
    true_positive = count1
    false_negative = count3
    false_positive = count2 + count4 + count5
    true_negative = count6
    return (true_positive, false_negative, false_positive, true_negative)


def estimation_measures(TP, FN, FP, TN):
    precision = TP/(TP + FP)
    recall = TP/(TP + FN)
    accuracy = (TP + TN)/(TP + TN + FN + FP)
    f1_score = 2*precision*recall/(precision + recall)
    data = {
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1_score": f1_score
    }
    return data


def evaluate_prereq_estimation(data_pos, data_neg, data_est):
    count1, count2, count3 = compare_datasets(data_pos, data_est)
    count4, count5, count6 = compare_datasets(data_neg, data_est)
    # print(count1, count2, count3)
    if count3 < 0 or count4 < 0:
        print("Bug....")
    # print(count4, count5, count6)
    TP, FN, FP, TN = confusion_matrix_formation(count1, count2, count3, count4, count5, count6)
    data = estimation_measures(TP, FN, FP, TN)
    return data
