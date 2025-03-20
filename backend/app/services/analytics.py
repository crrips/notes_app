from collections import Counter
from typing import List

import pandas as pd
import numpy as np

from models.note import Note

def analyze(notes: List[Note]) -> dict:
    notes_data = pd.DataFrame([{
        'id': note.id,
        'name': note.name,
        'description': note.description
    } for note in notes])

    word_counts = np.array([len(note.split()) for note in notes_data['description']])
    total_word_count = word_counts.sum()
    avg_note_length = word_counts.mean()

    all_words = ' '.join(notes_data['description']).split()
    word_counts = Counter(all_words)
    most_common_words = word_counts.most_common(10)

    notes_data['description_length'] = notes_data['description'].apply(len)
    notes_data['word_count'] = notes_data['description'].apply(lambda x: len(x.split()))

    top_3_longest = notes_data.nlargest(3, 'description_length')[['id', 'name', 'description_length', 'word_count']]
    top_3_shortest = notes_data.nsmallest(3, 'description_length')[['id', 'name', 'description_length', 'word_count']]

    analytics = {
        'total_word_count': int(total_word_count),
        'avg_note_length': float(avg_note_length),
        'most_common_words': most_common_words,
        'top_3_longest_notes': top_3_longest.astype({'description_length': int, 'word_count': int}).to_dict(orient='records'),
        'top_3_shortest_notes': top_3_shortest.astype({'description_length': int, 'word_count': int}).to_dict(orient='records')
    }

    return analytics