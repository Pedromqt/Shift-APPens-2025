import cv2
from ultralytics import YOLO

# Carrega o modelo (yolov5s.pt deve estar no mesmo diretório)
model = YOLO("yolov5s.pt")

def capture():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Cam não abriu")
        exit()

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Erro ao capturar frame")
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Realiza a detecção de objetos
        results = model(img_rgb)  # Rodar a inferência

        # A renderização do resultado será no formato de uma lista, então pegamos o primeiro
        annotated_frame = results[0].plot()  # Renderiza a imagem com as caixas de detecção
        cv2.imshow("Detecção", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()
