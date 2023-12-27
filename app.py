import openai
from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime
from collections import Counter
import unicodedata
from konlpy.tag import Okt
import re
import os
from tqdm import tqdm
import time
import pprint
from flask import Flask, render_template, request, session,redirect,url_for
from flask_paginate import Pagination, get_page_args
from jinja2 import Template
import json

def select_scan():
    print(f'demo_select_scan')
    
    item_list=[]
    dynamo_response = {'LastEvaluatedKey':False}
    while 'LastEvaluatedKey' in dynamo_response:
        if dynamo_response['LastEvaluatedKey']:
            dynamo_response = demo_table.scan(
                ExclusiveStartKey = dynamo_response['LastEvaluatedKey']
            )
            #print(f'response-if: {dynamo_response}')
        else:
            dynamo_response = demo_table.scan()
            #print(f'response-else: {dynamo_response}')
            
        for i in dynamo_response['Items']:
            item_list.append(i)
    
    print(f'Number of input tasks to process: {len(item_list)}')
    # for item in item_list:
    #    print(f'Item: {item}')
    return item_list

def count_occurrences(title_list, col_data_list):
    occurrences = {word: col_data_list.count(word) for word in title_list}
    total_occurrences = sum(occurrences.values())
    num_words = len(title_list)
    average_occurrences = total_occurrences / num_words
    return occurrences,average_occurrences

def correlation(data,tokenized_input,tokenized_searched_words):
    result_list=[]
    for i in tqdm(range(len(data)),desc="Processing", unit="step"):
        col_values = [data[i]['columns'][key] for key in data[i]['columns'] if key.startswith('col')]
        url_values = [data[i]['columns'][key] for key in data[i]['columns'] if key.startswith('url')]
        Name_values = data[i]['Name']
        string = Name_values
        uni1 = unicodedata.normalize('NFD',string)
        uni2 = unicodedata.normalize('NFC',uni1)


        name_text = uni2
        tokenized_noun_Name = tokenizer.nouns(name_text)  # 본 프로젝트의 프로토타입은 명사로만 진행

        tokenized_words=[]
        for word in col_values:
            tokens = tokenizer.nouns(word)
            tokenized_words.extend(tokens)


        title = tokenized_input
        search_title = tokenized_searched_words
        name_data = tokenized_noun_Name
        col_data =tokenized_words


        title_in_name,title_in_name_average = count_occurrences(title, name_data) # 가중치 제일 많이 *3
        title_in_col,title_in_col_average = count_occurrences(title, col_data) # 가중치 *2
        search_title_in_name,search_title_in_name_average = count_occurrences(search_title, name_data) #가중치 *2
        search_title_in_col,search_title_in_col_average = count_occurrences(search_title, col_data) #가중치 X

        result = title_in_name_average*0.5 + title_in_col_average*0.2 +search_title_in_name_average*0.2 +search_title_in_col_average*0.1
        result_dict = {
            'Name_values': Name_values,
            'correlation_result': result,
            'url': url_values
        }
        result_list.append(result_dict)
        result_list = sorted(result_list, key=lambda x: x['correlation_result'], reverse=True)

    return result_list


def API_with_processbar(KEY, input_text):
    tokenized_searched_words = []
    tokenized_input = tokenizer.nouns(input_text)
    text = input_text + '과/와 관련된 단어 10가지를 설명 없이 단어만 알려줘'
    with tqdm(desc="Loading", leave=True) as pbar:
        comletion= openai.ChatCompletion.create(
        model ="gpt-4-1106-preview",
        messages=[{"role": "user", "content":text}]
        )
        pbar.update()
    pattern = r'\b[^\d\W]+\b'
    words = re.findall(pattern,comletion.choices[0].message.content)
    print(words)
    searched_words = list(words)
    
    # 네트워크 통신에 프로세스바 추가
    searched_words_count = len(searched_words)
    with tqdm(total=searched_words_count, desc="Fetching Data", unit="word") as pbar:
        for word in searched_words:
            tokens = tokenizer.nouns(word)
            tokenized_searched_words.extend(tokens)
            pbar.update(1)
    
    tokenized_searched_words = list(set(tokenized_searched_words))

    return tokenized_input, tokenized_searched_words





access_ID = ''
secret_key = ''
region = 'ap-northeast-2'


openai.api_key =""


tokenizer = Okt()
demo_table = resource('dynamodb',aws_access_key_id=access_ID,aws_secret_access_key=secret_key,region_name=region).Table('datafabric_metadata')
data = select_scan()



app =Flask(__name__,static_url_path='/static', static_folder='static')

app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

def get_data(result, offset=0, per_page=10):
    return result[offset: offset+per_page]



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form.get("content")
        tokenized_input, tokenized_searched_words = API_with_processbar(openai.api_key, input_text)
        session["result"] = correlation(data, tokenized_input, tokenized_searched_words)
        return redirect(url_for('search'))
    return render_template('index.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    per_page = 10
    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

    result=session.get("result",None)
    #result=get_data(result, offset=offset, per_page=per_page)
    
    start = (page - 1) * per_page
    end = start + per_page
    result_page = result[start:end]

    total=len(result)
    return render_template('search.html', result=result_page,
                        page=page,
                        per_page=per_page,
                        pagination=Pagination(
                            page=page,
                            total=total,
                            per_page=per_page,
                            prev_label="<<",
                            next_label=">>",
                            format_total=True
                        ),
                        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)