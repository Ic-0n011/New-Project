scores = [
    {'name': 'John', 'points': 100},
    {'name': 'Jane', 'points': 90},
]

def sort_by_points(score):
    return -score['points']

sorted_scores = sorted(scores, key=sort_by_points)
print(sorted_scores)