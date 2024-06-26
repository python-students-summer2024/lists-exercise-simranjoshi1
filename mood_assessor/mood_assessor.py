import datetime
import os

def get_mood():
    moods = {
        'happy': 2,
        'relaxed': 1,
        'apathetic': 0,
        'sad': -1,
        'angry': -2
    }
    mood = None
    while mood not in moods:
        mood = input("Enter your current mood (happy, relaxed, apathetic, sad, angry): ").strip().lower()
        if mood not in moods:
            print("Invalid mood. Please try again.")
    return mood, moods[mood]

def already_entered(today, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if today in line:
                    return True
    return False

def enter_mood(today, mood_value, file_path):
    with open(file_path, 'a') as file:
        file.write(today + ',' + str(mood_value) + '\n')

def diagnose_mood(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[-7:]
    if len(lines) < 7:
        return None
    
    mood_values = [int(line.strip().split(',')[1]) for line in lines]
    mood_count = {
        'happy': mood_values.count(2),
        'relaxed': mood_values.count(1),
        'apathetic': mood_values.count(0),
        'sad': mood_values.count(-1),
        'angry': mood_values.count(-2)
    }
    
    if mood_count['happy'] >= 5:
        return "manic"
    if mood_count['sad'] >= 4:
        return "depressive"
    if mood_count['apathetic'] >= 6:
        return "schizoid"
    
    average_mood = round(sum(mood_values) / 7.0)
    valid_moods = {
        2: 'happy',
        1: 'relaxed',
        0: 'apathetic',
        -1: 'sad',
        -2: 'angry'
    }
    return valid_moods.get(average_mood, 'unknown')

def assess_mood():
    today = str(datetime.date.today())
    data_dir = 'data'
    file_path = os.path.join(data_dir, 'mood_diary.txt')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    if already_entered(today, file_path):
        print("Sorry, you have already entered your mood today.")
        return
    
    mood, mood_value = get_mood()
    enter_mood(today, mood_value, file_path)
    
    diagnosis = diagnose_mood(file_path)
    if diagnosis:
        print("Your diagnosis: " + diagnosis + "!")
    else:
        print("Mood logged for today. Not enough data for a diagnosis.")