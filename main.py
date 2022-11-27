import cv2
import webbrowser
import re

captura = cv2.VideoCapture(0)
qrDecoder = cv2.QRCodeDetector()

frame = None
conteudo = None
box = None
ehUmLink = False

def desenharBox():
    if box is not None:
        box2 = [box[0].astype(int)]
        n = len(box[0])
        for i in range(n):
            cv2.line(frame, tuple(box2[0][i]), tuple(box2[0][(i+1) % n]), (0,255,0), 3)

def verificarSeEhLink(texto=''):
    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return re. match(url_pattern, texto) is not None


def mostrarConteudo():
    if conteudo is None:
        return

    cv2.putText(img=frame, text=conteudo, org=(10, 50),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.2, color=[0, 0, 0], lineType=cv2.LINE_AA, thickness=2)
    cv2.putText(img=frame, text=conteudo, org=(10, 50),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.2, color=[255, 255, 255], lineType=cv2.LINE_AA,
                thickness=1)

    if ehUmLink:
        altura = frame.shape[0]

        cv2.putText(img=frame, text='Pressione espaco para abrir o link', org=(10, altura - 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.2, color=[0, 0, 0], lineType=cv2.LINE_AA, thickness=2)
        cv2.putText(img=frame, text='Pressione espaco para abrir o link', org=(10, altura - 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.2, color=[255, 255, 255], lineType=cv2.LINE_AA,
                    thickness=1)


def pressionouEspaco():
    if ehUmLink:
        webbrowser.open(conteudo)


while True:
    ret, frame = captura.read()

    conteudo, box, rectifiedImage = qrDecoder.detectAndDecode(frame)

    ehUmLink = verificarSeEhLink(conteudo)

    desenharBox()
    mostrarConteudo()

    cv2.imshow("Video", frame)

    k = cv2.waitKey(30)
    if k == 27:
        break
    elif k == 32:
        pressionouEspaco()

captura.release()
cv2.destroyAllWindows()
