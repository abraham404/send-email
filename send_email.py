from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__)
CORS(app)

def send_email(subject, body, to_emails, from_email, from_password, files=[]):
    # Crear el contenedor del mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar archivos
    for file in files:
        with open(file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file}')
            msg.attach(part)

    # Iniciar sesión en el servidor y enviar el correo
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)  # Puedes cambiarlo por tu servidor SMTP
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_emails, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")



@app.post('/api/data')
def sendData(): 
    
    data = request.json  # Obtener datos JSON enviados desde el frontend
    email = data.get('email')
    password = data.get('password')
    company = data.get('company')
    period = data.get('period')
    year = data.get('year')

    # Especificar el directorio
    #directorio = Path('C:/Users/Abraham-TI/Desktop/mail')
    #directorio = Path('\\\\192.168.101.108\\Users\\Abraham\\Desktop\\emailAbraham')
    if company == 'ctECO_BAJA_TOURS_2020Q':

        directorio = Path(r'\\192.168.101.130\CFDI de nominas')

    elif company == 'ctTRANSPORTE_ULPZS':

        directorio = Path(r'\\192.168.101.130\CFDI de nominas2')
    
    elif company == 'ctBAJA_PACK_SA_CULQ':
    
        directorio = Path(r'\\192.168.101.220\CFDI de nominas')
    
    elif company == 'ctBAJA_PACK_SA_LAPQ':
    
        directorio = Path(r'\\192.168.101.220\CFDI de nominas2')
        
    elif company == 'prueba':
    
        directorio = Path('\\\\192.168.101.108\\Users\\Abraham\\Desktop\\emailAbraham')


    i = 1
    regex = r'(?:[^_]*_){5}([^_]+)'
    regex2 = r'(\d{4})_(\d{1,2})'
    print(f"Email: {email}, Password: {password}, Company: { type(company)}, Period: {period}, Year: {year}")
    print(type("hola"))
    
    try:
        #Conexión a la base de datos
        db_conection=sqlite3.connect("C:/sqlite/database_rh.db")
        cursor=db_conection.cursor()

        # Recorrer los archivos en el directorio
        for file in os.listdir(directorio):
            i=i+1
            if i%2 != 0:
                full_path = os.path.join(directorio, file)
                if os.path.isfile(full_path):  # Verificar si es un archivo
                    with open(full_path, 'r', encoding='utf-8') as f:
                    
                        name_ruta = file[0:-4]
                        period_year = re.search(regex2, name_ruta)
                    
                        year_link = period_year.group(1)
                        period_link = period_year.group(2)

                        if year_link == year and period_link == period:
                            num_employee = re.search(regex, name_ruta)
                            code_employee = num_employee.group(1)
                        
                            cursor.execute(f"SELECT email, nombre FROM {company} WHERE num_empleado = ?", (code_employee,))
                            emails_destina=cursor.fetchall()
                            for email_destina in emails_destina:
                                try:
                                    print(email_destina[0])
                                    print(f'Serie de caracteres extraídos: {code_employee}')
                                    if __name__ == "__main__":
                                        subject = "Recibo de nomina de: " + email_destina[1]
                                        body = "Recibo de nomina"
                                        to_emails = [email_destina[0]]
                                        from_email = email
                                        from_password = password
                                    
                                        #Crear rutas de archivos dinámicamente
                                        files = [
                                            directorio / f"{name_ruta}.pdf",
                                            directorio / f"{name_ruta}.xml"
                                        ]

                                        # Convertir a cadenas de texto para la función de envío de correo
                                        files = [str(file) for file in files]

                                        #files = [directorio2+"/"+name_ruta+".pdf", directorio2+"/"+name_ruta+".xml"]  # Lista de archivos a adjuntar
                                    send_email(subject, body, to_emails, from_email, from_password, files)
                                     
                                    print('--- Fin del archivo ---\n')
                                     # Retorna una respuesta JSON
                                    #message = {"msg": "¡Correos enviados con exito!"}
                                    #   return jsonify(message) 
                                except Exception as ex:
                                    print(ex)
                                    message = {"msg": "¡Hubo un problema!"}
                                    return jsonify(message)
                    
    except Exception as ex:
        print(ex)

        # Asegúrate de que el archivo exista y esté en la carpeta correcta
 
    #return jsonify({"message": "Datos recibidos con éxito"}), 200
    message = {"msg": "¡Correos enviados con exito!"}
    return jsonify(message)


@app.post('/api/employee')
def add_employee():
    
    new_employee = request.json  # Obtener datos JSON enviados desde el frontend
    number_emplo = new_employee.get('number_emplo')
    name_emplo = new_employee.get('name_emplo')
    email_emplo = new_employee.get('email_emplo')
    company_emplo = new_employee.get('company_emplo')
    
    db_conection=sqlite3.connect("C:/sqlite/database_rh.db")
    cursor=db_conection.cursor()
    
    
    #print("number_emplo, name_emplo, email_emplo, company_emplo")
    print(f"Numero del empleado: {number_emplo}, nombre: {name_emplo}, Email: { email_emplo }, Empresa: {company_emplo}")
    #print(request.get_json())
    
    # Consulta SQL para insertar los datos
    query = f'''
    INSERT INTO {company_emplo} (num_empleado, nombre, email, empresa)
    VALUES (?, ?, ?, ?)
    '''
    # Ejecutar la consulta
    cursor.execute(query, (number_emplo, name_emplo, email_emplo, company_emplo))

    # Guardar los cambios en la base de datos
    db_conection.commit()

    # Cerrar la conexión
    db_conection.close()
    
    message = {"msg": "Empleado guardado con éxito"}
    return jsonify(message)
        

@app.route('/api/employee/<string:id>/<string:company>', methods=['GET'])
def get_employee(id,company):
    
    

    try:
        # Conectar a la base de datos
        db_conection = sqlite3.connect("C:/sqlite/database_rh.db")
        cursor = db_conection.cursor()

        # Consulta SQL segura con el ID parametrizado
        query = f'''
        SELECT num_empleado, nombre, email FROM {company} WHERE num_empleado = ?
        '''

        # Ejecutar la consulta pasando el ID como parámetro
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        # Verificar si se encontró un resultado
        if result:
            return jsonify({'status': 'success', 'employee': {
                'num_employee': result[0],
                'name': result[1],
                'email': result[2]
            }})
        else:
            return jsonify({'status': 'error', 'message': 'Empleado no encontrado'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        db_conection.close()
        

@app.route('/api/employee/<string:id>/<string:company>', methods=['PUT'])
def update_employee(id, company):
    
    update_employee_data = request.json  # Obtener datos JSON enviados desde el frontend
    new_number_emplo = update_employee_data.get('number_emplo')
    name_emplo = update_employee_data.get('name_emplo')
    email_emplo = update_employee_data.get('email_emplo')
    #company_emplo = update_employee_data.get('company_emplo')
    

    
    try:
        db_conection = sqlite3.connect("C:/sqlite/database_rh.db")
        cursor = db_conection.cursor()
        
        # Consulta SQL segura con el ID parametrizado
        query = '''
        UPDATE prueba 
        SET num_empleado = ?, nombre = ?, email = ?, empresa = ? 
        WHERE num_empleado = ?;
        '''

        cursor.execute(query, (new_number_emplo, name_emplo, email_emplo, company, id))


        # Guardar los cambios en la base de datos
        db_conection.commit()

        # Cerrar la conexión
        db_conection.close()
        
        message = {"msg": "Empleado actualizado con éxito"}
        return jsonify(message)
        

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        db_conection.close()
        
        



@app.get('/')
def home():
    return send_file('static/index.html')


if __name__== '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
    


    

