import cv2
import torch


class ObjectDetection:
    def __init__(self):
        self.__model = self.__load_model()
        self.classes = self.__model.names

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model.to(device)

    def __load_model(self):
        model = torch.hub.load(
            'ultralytics/yolov5', 'yolov5x', pretrained=True
        )
        return model

    def detect_objects(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            return

        results = self.__model(img)
        detections = results.xyxy[0].cpu().numpy()

        for detect in detections:
            x1, y1, x2, y2, conf, class_id = detect
            x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)
            label = f'{self.classes[class_id]}: {conf * 100:.2f}%'
            print(label)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1
            )

        cv2.imshow('Detecting object', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    obj = ObjectDetection()
    print(obj.classes)
    obj.detect_objects(image_path='opencv/img/moh.jpeg')
