import sqlite3
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def connect_db():
    conexao = sqlite3.connect('banco.db')
    return conexao

def create_table():
    conexao = connect_db()
    conexao.executescript("""
    CREATE TABLE IF NOT EXISTS dados(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS alunos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    periodo INTEGER NOT NULL
    )
    
    """)
    conexao.close()
    
    

def get_id(id):
    item = {}
    try:
        conexao = connect_db()
        conexao.row_factory  = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("""
                       SELECT * FROM dados
                       WHERE id=?""", (id,))
        row = cursor.fetchone()
        
        item['id'] = row['id']
        item['nome'] = row['nome']
        item['idade'] = row['idade']
        
    except:
        item = {}
        
    return item

def get_all():
    itens= []
    try:
        conexao = connect_db()
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute(
            '''
            SELECT * FROM dados
            '''
        )
        rows = cursor.fetchall()
        
        for row in rows:
            item = {
                'id':row['id'],
                'nome':row['nome'],
                'idade':row['idade']
            }
            itens.append(item)
    
        
    except:
        itens = []
    return itens


def insert(item):
    inserted_item = {}
    try:
        conexao = connect_db()
        cursor = conexao.cursor()
        cursor.execute('''
                       INSERT INTO dados (nome, idade) VALUES (?, ?);''',
                       (item['nome'], item['idade']))
        conexao.commit()
        inserted_item = get_id(cursor.lastrowid)
    except:
        conexao.rollback()
    finally:
        conexao.close()
        
    return inserted_item

def delete(id):
    message = {}
    try:
        pessoa = get_id(id)
        conexao = connect_db()
        cursor = conexao.cursor()
        cursor.execute('''
                       DELETE FROM dados
                       WHERE id = ?;
                       ''', (id, ))
        conexao.commit()
        if len(pessoa) > 0:
            message['Estado'] = "item deletado com sucesso!"
        else:
            message['Estado'] = "Item a ser deletado inexistente"
            
    except:
        conexao.rollback()
        message['Estado'] = "não foi possivel realizar a deleção"
    finally:
        conexao.close()
    return message

        
