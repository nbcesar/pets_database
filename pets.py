# Pets Unit 3 Lesson 2 Assignment 4

import csv
import psycopg2

def insertCSV():
	
	conn = psycopg2.connect("dbname='pets' ")
	cur = conn.cursor()

	with open('pets_to_add.csv', 'rb') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		for line in reader:
			newLine = {}
			print line
			for key in line:
				newKey = key.replace(' ','')

				if newKey == 'sheltername':
					newValue = line[key]
					newValue = newValue.replace(' ','')
				elif newKey == 'age':
					if line[key] == '' or line[key] == ' ':
						newValue = None
					else:
						newValue = int(line[key])
				else:
					newValue = line[key].title()
					newValue = newValue.replace(' ','')

				newLine[newKey] = newValue
			print newLine
			cur.execute("""INSERT INTO pet (name, age, adopted, dead, breed_id, shelter_id)
				VALUES (%(Name)s, %(age)s, %(adopted)s, false, 
					(SELECT id FROM breed 
						WHERE name = %(breedname)s
						AND species_id = (SELECT id FROM species WHERE name = %(speciesname)s)
						),
					(SELECT id FROM shelter WHERE name = %(sheltername)s));""", newLine)

	conn.commit()

	cur.close()
	conn.close()


def connect():
	conn = psycopg2.connect("dbname='pets' ")
	cur = conn.cursor()
	cur.execute("""SELECT id FROM breed WHERE name = %(breedname)s;""", {'breedname': 'Mixed'})
	
	rows = cur.fetchall()
	for row in rows:
		print " ", row

if __name__ == "__main__":
	insertCSV()
	#connect()