def main():
    args = get_args()

    cap = cv.VideoCapture(args.device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, args.height)

    # Load mediapipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=args.use_static_image_mode,
        max_num_hands=1,
        min_detection_confidence=args.min_detection_confidence,
        min_tracking_confidence=args.min_tracking_confidence,
    )

    # Ask which gesture to record
    gesture_number = int(input("Enter gesture number label (0–9): "))
    target_samples = int(input("How many samples do you want to record? "))
    print(f"Recording gesture {gesture_number} for {target_samples} samples...")

    cvFpsCalc = CvFpsCalc(buffer_len=10)

    sample_count = 0

    while True:
        fps = cvFpsCalc.get()

        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)
        debug_image = copy.deepcopy(image)

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                if sample_count < target_samples:
                    logging_csv_single(gesture_number, pre_processed_landmark_list)
                    sample_count += 1
                    print(f"Saved sample {sample_count}/{target_samples}", end="\r")

                debug_image = draw_bounding_rect(True, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)

        debug_image = draw_info(debug_image, fps, 1, gesture_number)
        cv.putText(debug_image, f"Samples: {sample_count}/{target_samples}",
                   (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv.imshow('Data Collection', debug_image)

        key = cv.waitKey(10)
        if key == 27:  # ESC to stop early
            break

        if sample_count >= target_samples:
            print("\nFinished recording.")
            break

    cap.release()
    cv.destroyAllWindows()


def logging_csv_single(number, landmark_list):
    csv_path = 'model/keypoint_classifier/keypoint.csv'
    with open(csv_path, 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([number, *landmark_list])


if __name__ == '__main__':
    main()
