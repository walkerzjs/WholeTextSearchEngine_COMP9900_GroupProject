#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 22:19:41 2018

@author: junshuaizhang
"""
import pickle
def load_file(input_path):
    with open(input_path, 'rb') as file:
        x = pickle.load(file)
    return x

def write_file(out_file, output_path):
    with open(output_path, 'wb') as file:
        pickle.dump(out_file, file)