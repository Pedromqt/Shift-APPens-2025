import time
import cv2
from ultralytics import YOLO
import threading

import os
# Caminho base onde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos relativos para os modelos
# Carregar os modelos com YOLO
model_padrao = YOLO(os.path.join(BASE_DIR, "yolov5s.pt"))
model_buracos = YOLO(os.path.join(BASE_DIR,"runs", "detect", "train", "weights", "best.pt"))
model_sidewalk = YOLO(os.path.join(BASE_DIR,"runs", "detect", "train2", "weights", "best.pt"))

# Controle de alertas
ultimo_alerta = ""
ultimo_tempo_alerta = 0

# Mensagens de voz
mensagensPrioritarias = {
    'buraco': "Cuidado! Há um buraco à frente.",
    'crosswalk': "Atenção! Passadeira à frente.",
    'red-crossing': "Semáforo vermelho, não passe.",
    'geen-crossing': "Semáforo verde, pode passar."
}

def boxes_intersect(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    return interArea > 0

def draw_filtered_holes(frame, boxes):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = box.conf[0].item()
        label = f"Buraco {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

def draw_sidewalk_detections(frame, results):
    for r in results:
        for box in r.boxes:
            conf = box.conf[0].item()
            if conf < 0.6:
                continue
            cls_idx = int(box.cls[0].item())
            label_name = r.names[cls_idx]
            label = f"{label_name} {conf:.2f}"
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            color = (255, 255, 0) if label_name == "crosswalk" else (0, 255, 0) if label_name == "green-crossing" else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def holesFace(results_padrao, results_buracos):
    buracos_filtrados = []
    pessoas = []
    for box_padrao in results_padrao[0].boxes:
        if int(box_padrao.cls[0].item()) == 0:
            pessoas.append(box_padrao.xyxy[0].tolist())

    for box_buraco in results_buracos[0].boxes:
        if box_buraco.conf[0].item() < 0.6:
            continue
        x1, y1, x2, y2 = box_buraco.xyxy[0].tolist()
        buraco_box = [x1, y1, x2, y2]
        sobrepoe_pessoa = any(boxes_intersect(buraco_box, pessoa_box) for pessoa_box in pessoas)
        if not sobrepoe_pessoa:
            buracos_filtrados.append(box_buraco)

    return buracos_filtrados

def verificar_alertas(results, alertsQueue, threshold=0.6):
    for r in results:
        for box in r.boxes:
            conf = box.conf[0].item()
            if conf < threshold:
                continue
            cls_idx = int(box.cls[0].item())
            classe = r.names[cls_idx]
            if classe in mensagensPrioritarias:
                alertsQueue.put(mensagensPrioritarias[classe])
                
                
def capture(stop_event,alertsQueue):
    cam = cv2.VideoCapture(1)
    if not cam.isOpened():
        print("Cam não abriu")
        exit()

    while not stop_event.is_set():
        ret, frame = cam.read()
        if not ret:
            print("Erro ao capturar frame")
            break

        # Inferência dos modelos
        results_padrao = model_padrao(frame,verbose=False)
        results_buracos = model_buracos(frame,verbose=False)
        results_sidewalk = model_sidewalk(frame,verbose=False)
        
        # Anotações visuais base
        annotated = results_padrao[0].plot()

        # Verifica e desenha buracos válidos
        buracos_validos = holesFace(results_padrao, results_buracos)
        draw_filtered_holes(annotated, buracos_validos)

        # Desenha deteções de passadeiras/semaforosj
        draw_sidewalk_detections(annotated, results_sidewalk)
        
        verificar_alertas(results_padrao, alertsQueue, threshold=0.6)
        verificar_alertas(results_buracos, alertsQueue, threshold=0.6)
        verificar_alertas(results_sidewalk, alertsQueue, threshold=0.6)
        
        cv2.imshow("Detecção Combinada", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

