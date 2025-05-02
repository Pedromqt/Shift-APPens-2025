import cv2
from ultralytics import YOLO

# Carrega os dois modelos
model_padrao = YOLO("yolov5s.pt")
model_buracos = YOLO("runs/detect/train/weights/best.pt")

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
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, "Buraco", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


def holesFace(results_padrao, results_buracos):
    buracos_filtrados = []

    # Obtem as caixas de pessoas
    pessoas = []
    for box_padrao in results_padrao[0].boxes:
        # buscar o tipo (ex: Person)
        cls = int(box_padrao.cls[0].item())
        # se for person adiciona ao array de pessoas
        if cls == 0:  
            pessoas.append(box_padrao.xyxy[0].tolist())

    # Filtrar buracos para não coincidirem com pessoas
    for box_buraco in results_buracos[0].boxes:
        # Coordenadas do buraco
        x1, y1, x2, y2 = box_buraco.xyxy[0].tolist()
        buraco_box = [x1, y1, x2, y2]

        # Se algum buraco sobrepor uma pessoa o any retorna True
        sobrepoe_pessoa = any(boxes_intersect(buraco_box, pessoa_box) for pessoa_box in pessoas)

        # se o buraco não sobrepor a pessoa, adicionamos aos buracos filtrados este buraco
        if not sobrepoe_pessoa:
            buracos_filtrados.append(box_buraco)

    return buracos_filtrados


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

        # Anotações visuais do modelo padrão
        annotated = results_padrao[0].plot()

        # Filtra buracos que não estão sobre pessoas
        buracos_validos = holesFace(results_padrao, results_buracos)

        # Desenha os buracos válidos
        draw_filtered_holes(annotated, buracos_validos)

        cv2.imshow("Detecção Combinada", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()
