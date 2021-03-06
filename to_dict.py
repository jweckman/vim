from sys import argv,stdin
from statistics import median, mean
import pprint
"""Vim tool for transforming key value pair text to python dictionary / json format.
    Does not work on nested structures. Takes in stdin and prints out a pretty printed python dictionary.
    Supports the delimiters defined in the detect_input_delimiters function.

    Usage
    Select the key value pair text in vim either with visual or the entire file and feed it to this script. The script will then return the string formatted as a dictionary stirng.

    Sample input
    key1,value1
    key2,value2
    key3,value3
"""
pp = pprint.PrettyPrinter(indent=4)

def input_to_list(ip):
    if isinstance(ip, str):
        lines = ip.split('\n')
    else:
        lines = ip
    return lines


def detect_input_delimiter(lines):
    delimiters = {' ': 0, '\t': 0, ',': 0, ';': 0} 
    line_lengths = []
    avposdist = {' ': [], '\t': [], ',': [], ';': []}
    for l in lines:
        line_lengths.append(len(l))
        positions = {' ': [], '\t': [], ',': [], ';': []}
        for i,c in enumerate(l):
            if c in delimiters.keys():
                positions[c].append(i)
                delimiters[c] += 1
        for delim, ps in positions.items():
            if len(ps) != 0:
                avposdist[delim].append(mean(ps))
            else:
                avposdist[delim] = []

    m_line_length = median(line_lengths)
    for k,v in avposdist.items():
        if len(avposdist[k]) != 0:
            avposdist[k] = mean(avposdist[k]) - (m_line_length / 2) 
        else:
            avposdist[k] = 1000000
    avcount = dict()
    for d, count in delimiters.items():
        avcount[d] = count / len(lines)
        
    # Criteria for selecting delimiter is that count per line should be closest to 1
    # Option to use delimiter closest to middle of line implemented, but currently not used as count closest to 1 probably is sufficient for 99% of the cases.
    delim_closest_to_middle = min(avposdist, key=avposdist.get)   
    delim_closest_to_one = min(avcount.items(), key=lambda x: abs(1 - x[1]))[0]

    return delim_closest_to_one, delim_closest_to_middle

def input_to_dictstring(lines, delimiter):
    o = dict() 
    for i,l in enumerate(lines):
        try:
            key, value = l.split(delimiter)
        except:
            pass
        o[key] = value
    pp.pprint(o)

if __name__ == '__main__':
    ip = stdin.read() 
    lines = input_to_list(ip)
    dcto, dctm = detect_input_delimiter(lines)
    input_to_dictstring(lines, dcto)



