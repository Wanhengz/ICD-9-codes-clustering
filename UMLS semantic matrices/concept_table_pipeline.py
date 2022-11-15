import pandas as pd
import numpy as np
from tqdm import tqdm

        
def get_processing_from_all(contents):
    ctt = []
    process_index = [index for index in range(len(contents)) if contents.startswith('Processing \'',index)]
    for i in range(len(process_index)-1):
        start = process_index[i]
        end = process_index[i+1]
        a = contents[start:end]
        ctt.append(a)
    ctt.append(contents[process_index[-1]:])
    return(ctt)

def get_concept_lines_for_processing(process):
    phrases = process.split('\n\n')[1:]
    concept_lines = []
    for phrase in phrases:
        lines = phrase.split('\n')
        meta_lines_index = [index for index in range(len(lines)) if lines[index].startswith('Meta Mapping')]
        if len(meta_lines_index) == 1:
            concept_line = [line for line in lines if line.startswith('  ')]
        if len(meta_lines_index) == 0: continue
        if len(meta_lines_index) > 1:
            concept_start = meta_lines_index[0]+1
            concept_end = meta_lines_index[1]
            concept_line = lines[concept_start: concept_end]
        concept_lines = concept_lines + concept_line
    return(concept_lines)

def create_semantic_dictionary(contents):
    from collections import defaultdict
    dic = defaultdict(list)
    processes = get_processing_from_all(contents)
    for process in processes:
        concept_lines = get_concept_lines_for_processing(process)
        for line in concept_lines:
            value = line.split('[')[0].split('(')[0][9:-1]
            value = value.lower()
            brasket_contents = line.split('[')[1][:-1]
            brasket_contents = brasket_contents.replace(', ',' ')
            keys = brasket_contents.split(',')
            for key in keys:
                if value not in list(dic[key]): dic[key].append(value)
    dic = dict(dic)
    return dic

def create_semantic_table(contents,des_name):
    #create a empty table with row names and column names
    col_list = []
    e = create_semantic_dictionary(contents)
    for key,values in e.items():
        for value in values:
            y = (key,value)
            col_list.append(y)
    row = des_name
    col= pd.MultiIndex.from_tuples(col_list)
    table = pd.DataFrame(None, row,col)
    # filling the table with indicator
    processes = get_processing_from_all(contents)
    for i in range(len(processes)):
        process = processes[i]
        concept_lines = get_concept_lines_for_processing(process)
        for line in concept_lines:
            keyword = line.split('[')[0].split('(')[0][9:-1]
            keyword = keyword.capitalize()
            brasket = line.split('[')[1][:-1]
            brasket = brasket.replace(', ',' ')
            categories = brasket.split(',')
            des = des_name[i]
            for category in categories:
                table.loc[des,(category,keyword)] = 1
    table = table.fillna(0)
    return(table)


    