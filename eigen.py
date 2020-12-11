import cv2
from database import *
import os

camera = cv2.VideoCapture(0)
detectorFace = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
reconhecedor = cv2.face.EigenFaceRecognizer_create()
reconhecedor.read("classificadorEigen.yml")
largura,altura = 220,220
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

while (True):
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem,cv2.COLOR_BGR2GRAY)
    facesDetectadas = detectorFace.detectMultiScale(imagemCinza, minNeighbors=20, minSize=(30, 30), maxSize=(400, 400))
    for (x,y,l,a) in facesDetectadas:
        imagemFace = cv2.resize(imagemCinza[y:y+a,x:x+l],(largura,altura))
        cv2.rectangle(imagem,(x,y),(x+l,y+a),(0,0,255),2)
        id,confianca = reconhecedor.predict(imagemFace)
        print(id)
        cursor.execute("SELECT nome FROM users WHERE id = ?",(int(id),))
        resultado = cursor.fetchall()
        print(resultado)
        if not resultado:
            cv2.putText(imagem, "Nenhum user encontrado".strip("(),'"), (x, y + (a + 30)), font, 2, (0, 0, 255))
        else:
            cv2.putText(imagem, str(resultado[0]).strip("(),'"), (x, y + (a + 30)), font, 2, (0, 0, 255))

    cv2.imshow("Face",imagem)

    if cv2.waitKey(1) == ord('q'):
        break

from training import *
camera.release()
cv2.destroyAllWindows()