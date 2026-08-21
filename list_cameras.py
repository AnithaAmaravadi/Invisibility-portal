import cv2

MAX_INDEX_TO_TRY = 6  # Checks indices 0 through 5

def main():
    found = []
    for idx in range(MAX_INDEX_TO_TRY):
        cap = cv2.VideoCapture(idx)
        if not cap.isOpened():
            cap.release()
            continue

        ok, frame = cap.read()
        if not ok or frame is None:
            cap.release()
            continue

        found.append(idx)
        print(f"Camera index {idx}: opened successfully, showing preview...")

        window_name = f"Camera index {idx} - press any key for next"
        cv2.imshow(window_name, frame)

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                print("\nQuitting early. Cameras found so far:", found)
                return
            if key != 255:  # Any other key pressed
                break

        cap.release()
        cv2.destroyWindow(window_name)

    cv2.destroyAllWindows()
    print("\nDone. Working camera indices:", found)
    print("Use the index that showed your desired camera as CAM_INDEX in invisibility_portal.py")

if __name__ == "__main__":
    main()