#!/usr/bin/env 

import sqlite3

""" Conexão e criação do cursor. """

connection = sqlite3.connect('reconhecimento.db')
cursor = connection.cursor()
