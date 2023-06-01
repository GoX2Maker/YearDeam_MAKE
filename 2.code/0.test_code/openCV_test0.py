import cv2


class openCVTEST:
    """
    openCV 테스트 클래스
    ==


    Todo:
    --
    * 앞으로 할 것의 목록
    * `Todo`는 모듈이나 패키지, 함수, 클래스 등에 자유롭게
        사용할 수 있습니다.
    * 사용자 입장에서 서술하는 것이 좋습니다.
    """

    def show(self, path, title):
        """이미지출력
        ==
        Args:
        --
            `path [string]` : 이미지 경로

            `title [string]` : 창 이름

        Returns:
        ---
            None

        """

        # 이미지 파일을 읽습니다.
        img = cv2.imread(path)

        # 이미지를 화면에 출력합니다.
        cv2.imshow(title, img)

        # 키보드 동작을 기달립니다.(0 : inf)
        cv2.waitKey(0)

        # 이미지 창을 종료합니다.
        cv2.destroyAllWindows()


opencvtest = openCVTEST()
opencvtest.show("1.data/0.test/img/prescription.png", "test")
