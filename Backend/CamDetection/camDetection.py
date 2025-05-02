import cv2
from ultralytics import YOLO

# Carrega os dois modelos
model_padrao = YOLO("yolov5s.pt")  # ou yolov5s.pt
model_buracos = YOLO("runs/detect/train/weights/best.pt")

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

        # Inferência dos dois modelos
        results_padrao = model_padrao(frame)
        results_buracos = model_buracos(frame)

        # Renderizar separadamente
        annotated_padrao = results_padrao[0].plot()
        annotated_buracos = results_buracos[0].plot()

        # Combinar as duas imagens (usando transparência com addWeighted)
        annotated_combined = cv2.addWeighted(annotated_padrao, 0.5, annotated_buracos, 0.5, 0)

        # Mostrar
        cv2.imshow("Detecção Combinada", annotated_combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()
