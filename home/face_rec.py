import face_recognition

def face_validation(image):
    train_image = face_recognition.load_image_file(image)
    l = face_recognition.face_encodings(train_image)
    if len(l) == 1:
        return True
    return False


def match_face(known_img, unknown_img):
    known_image = face_recognition.load_image_file(known_img)
    unknown_image = face_recognition.load_image_file(unknown_img)

    known_face_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

    known_faces = [
        known_face_encoding
    ]
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    return results[0]
