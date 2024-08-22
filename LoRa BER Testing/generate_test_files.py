import os
import random

def generate_random_ascii_line(length):
    """Generate a string of random ASCII characters with a specified length."""
    return ''.join(chr(random.randint(32, 126)) for _ in range(length))

def generate_file_with_newline(filename, num_lines, line_length):
    """Generate a file where each byte of random ASCII characters is on a new line."""
    with open(filename, 'w') as file:
        for _ in range(num_lines):
            line = generate_random_ascii_line(line_length)
            for char in line:
                file.write(char + '\n')

def generate_file_with_comma(filename, num_lines, line_length):
    """Generate a file where each byte of random ASCII characters is separated by a comma."""
    with open(filename, 'w') as file:
        for _ in range(num_lines):
            line = generate_random_ascii_line(line_length)
            file.write(','.join(line) + '\n')

if __name__ == "__main__":
    output_file_newline = 'tx_test_comp.txt'
    output_file_comma = 'tx_test_csv.txt'
    lines_count = 100
    bytes_per_line = 250
    
    generate_file_with_newline(output_file_newline, lines_count, bytes_per_line)
    generate_file_with_comma(output_file_comma, lines_count, bytes_per_line)
    
    print(f"File '{output_file_newline}' with each byte on a new line has been created.")
    print(f"File '{output_file_comma}' with bytes separated by commas has been created.")
