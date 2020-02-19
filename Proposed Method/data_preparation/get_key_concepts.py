import pandas as pd


def extract_topics(line):
    topics = line.split(",")
    a = " ".join(topics[0].split("_")).strip()
    b = " ".join(topics[1].split("_")).strip()
    return a, b


def save_data(all_topics, output_location):
    columns = ["topic"]
    df = pd.DataFrame({'topic': all_topics})
    df.to_csv(output_location)


def get_topics(pairs_file, output_location):
    f1 = open(pairs_file, "r")
    all_topics = []
    for line in f1:
        a, b = extract_topics(line)
        all_topics.append(a)
        all_topics.append(b)

    all_topics = list(set(all_topics))
    save_data(all_topics, output_location)
    return True


pairs_file = "dataset/physics.pairs"
output_location = "output/physics_concepts.csv"

get_topics(pairs_file, output_location)
