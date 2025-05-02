from ultralytics import YOLO
import torch

def train_model():
    
    if torch.cuda.is_available():
        print(f"CUDA disponível! Usando GPU: {torch.cuda.get_device_name(0)}")
        device = 'cuda'
    else:
        print("CUDA não disponível. Usando CPU.")
        device = 'cpu'

    
    model = YOLO("yolov5s.pt")

    
    model.train(
        data="datasets1/data.yaml",  
        epochs=25,
        imgsz=640,                  
        batch=8,                    
        device=device
    )

if __name__ == '__main__':
    train_model()
