from datetime import datetime

current_timestamp = datetime.now()

items = 'CREATE TABLE items (id serial primary key, body text, created timestamp)'
item1 = 'INSERT INTO items VALUES (1, "body_1", current_timestamp)'

users = 'CREATE TABLE users ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "username" TEXT NOT NULL UNIQUE, "name" TEXT NOT NULL UNIQUE )'
grades = 'CREATE TABLE grades ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "grade" TEXT NOT NULL UNIQUE)'
groups = 'CREATE TABLE groups ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "groupe" TEXT NOT NULL UNIQUE)'

tickets = 'CREATE TABLE tickets ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, "date" DATETIME NOT NULL DEFAULT CURRENT_DATE, "dependiente" TEXT NOT NULL, "alumno" TEXT NOT NULL, "curso" TEXT NOT NULL, "items" TEXT NOT NULL, "total" NUMERIC NOT NULL )'
students = 'CREATE TABLE students ("id" INTEGER PRIMARY KEY NOT NULL, "curso" TEXT, "nombre" TEXT, "tutor" TEXT DEFAULT (null), "hermano" TEXT, "tel1" TEXT, "tel2" TEXT, "mail1" TEXT, "mail2" TEXT, "socio" BOOL, "grupo" TEXT)'
books = 'CREATE TABLE books ("id" INTEGER PRIMARY KEY NOT NULL, "curso" TEXT, "isbn" TEXT, "titulo" TEXT, "editorial" TEXT, "precio" TEXT, "stock" INTEGER, "grupo" TEXT)'

admin = 'INSERT INTO users VALUES (1, "admin", "Administrador")'
default_grade = 'INSERT INTO grades VALUES (1, "todos")'
default_group = 'INSERT INTO groups VALUES (1, "todos")'