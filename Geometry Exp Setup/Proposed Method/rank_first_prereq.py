import pandas as pd


def get_rank_score(c1, c2, concept_rank):
    r1 = int(concept_rank[c1])
    r2 = int(concept_rank[c2])

    if r1 >= r2:
        return 1
    else: return 0


def apply_rank_first_prereq(df_prereq, df_rank):
    concept_rank = {df_rank[["concept"]].iloc[i].values[0]: df_rank[["rank"]].iloc[i].values[0] for i in range(df_rank.shape[0])}
    concept_list = df_prereq["concept"].values
    concept_index = {concept_list[i] : i for i in range(0, len(concept_list))}
    df_prereq.set_index("concept", inplace = True)

    for c1 in concept_list:
        for c2 in concept_list:
            score = get_rank_score(c1, c2, concept_rank)
            if score == 0:
                df_prereq.at[c1, c2] = 0

    return df_prereq
