import pickle
with open('lf.pkl', 'rb') as f:
    a = pickle.load(f)

for key, value in a.items():
    print(len(set(value)))