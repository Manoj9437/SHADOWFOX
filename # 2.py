# 2.1
def convert_and_display(value, pattern):
    formatted_value = format(value, pattern)
    message = f"The number {value} formatted as '{pattern}' is: {formatted_value}"
    print(message)
    return formatted_value
convert_and_display(145, 'o')
