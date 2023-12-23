def split_record(record):
    name, score = record.split()
    return name, int(score)


record = "John 100"
name, score = split_record(record)
print(f"Name: {name}, Score: {score}")
# Output: Name: John, Score: 100
