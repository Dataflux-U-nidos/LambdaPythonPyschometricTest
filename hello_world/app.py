import json
import os
import boto3
from botocore.exceptions import ClientError

# Inicializa el cliente S3 (se aprovecharán las credenciales de IAM asignadas a la Lambda).
s3 = boto3.client('s3')

# Opcional: define el nombre del bucket como variable de entorno en la configuración de la Lambda
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'psychometrictest')

def lambda_handler(event, context):
    """
    Espera un evento con al menos:
    {
      "version": 1
    }
    Recupera V{version}/psychometric-test.json de S3 y lo devuelve como JSON.
    """
    # 1. Extraer y validar la versión
    version = event.get('version')
    if version is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Falta el atributo "version" en el evento'})
        }

    # 2. Construir la key
    key = f"V{version}/psychometric-test.json"

    try:
        # 3. Traer el objeto de S3
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=key
        )
        # 4. Leer el cuerpo y parsear JSON
        content = response['Body'].read().decode('utf-8')
        schema = json.loads(content)

        # 5. Retornar el esquema procesado
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'version': version,
                'schema': schema
            })
        }

    except ClientError as e:
        # Manejo de errores de S3 (p.ej. NoSuchKey, NoSuchBucket, AccessDenied)
        code = e.response['Error']['Code']
        message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f"S3 ClientError: {code} - {message}"
            })
        }
    except json.JSONDecodeError:
        # Manejo de error de parseo de JSON
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'El contenido no es un JSON válido'})
        }
