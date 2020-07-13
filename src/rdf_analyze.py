import os
os.chdir("..")
TRIPLES_PATH = os.getcwd() + "/data/vaccine-articles/triples"
for roots, dirs, files in os.walk(TRIPLES_PATH):
    for file in files:
        if file.endswith(".txt"):
            print(file)


