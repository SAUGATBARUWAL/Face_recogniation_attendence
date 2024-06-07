import os
import pickle
import sys

def remove_name(name):
    try:
        # Load the names
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)

        # Check if the name is in the list
        if name in names:
            # Delete the files
            if os.path.exists('data/names.pkl'):
                os.remove('data/names.pkl')
            if os.path.exists('data/face_encodings.pkl'):
                os.remove('data/face_encodings.pkl')
            print(f"Files deleted for {name}.")
        else:
            print(f"No data found for {name}.")
    except FileNotFoundError:
        print("No data found to remove.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        remove_name(name)
    else:
        print("No name provided.")
