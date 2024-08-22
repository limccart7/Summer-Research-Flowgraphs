import os
import random

def generate_random_ascii_line(length):
    """Generate a string of random ASCII characters with a specified length."""
    return ''.join(chr(random.randint(32, 126)) for _ in range(length))

def generate_files(filename_newline, filename_comma, num_lines, line_length):
    """Generate two files: one with each byte on a new line and one with bytes separated by commas."""
    with open(filename_newline, 'w') as file_newline, open(filename_comma, 'w') as file_comma:
        for _ in range(num_lines):
            line = generate_random_ascii_line(line_length)
            
            # Write to the file with each byte on a new line
            for char in line:
                file_newline.write(char + '\n')
            
            # Write to the file with bytes separated by commas
            file_comma.write(','.join(line) + '\n')

if __name__ == "__main__":
    output_file_newline = 'tx_test_comp.txt'
    output_file_comma = 'tx_test_csv.txt'
    lines_count = 100
    bytes_per_line = 250
    
    generate_files(output_file_newline, output_file_comma, lines_count, bytes_per_line)
    
    print(f"Files '{output_file_newline}' and '{output_file_comma}' have been created with the same data formatted differently.")
