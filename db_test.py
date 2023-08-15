import mysql.connector

def db_insert(db, data):
    cursor = db.cursor(buffered=True)
    sql_insert_command = "INSERT INTO NumberPlateVerification (name, plateno, phoneno) VALUES (%s, %s, %s)"
    cursor.execute(sql_insert_command, data)
    mydb.commit()

def plateNumber_to_phoneNumber(db, plate_number):
    cursor = db.cursor(buffered=True) 
    cursor.execute("SELECT PHONENO FROM NumberPlateVerification where plateno = '" + plate_number + "'")
    result = cursor.fetchall()
    phone_number = result[0][0]
    print("num = ", phone_number)

mydb = mysql.connector.connect(
host = "localhost",
user = "pi",
password = "raspberry",
database = "vehicle"
)

plateNumber_to_phoneNumber(mydb, "MD20DV2363")

