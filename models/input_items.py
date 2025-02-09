class InputItem:
    _reference_file_path_list = None
    _video_path = None

    def __init__(self, reference_file_path_list: list, video_path: str):
        """InputItemsクラスの初期化

        Args:
            reference_file_path_list (list): 参照ファイルのパスリスト
            video_path (str): 動画のパス
        """
        self._reference_file_path_list = reference_file_path_list
        self._video_path = video_path

    def get_reference_file_path_list(self):
        """参照ファイルのパスリスト取得

        Returns:
            参照ファイルのパスリスト
        """
        return self._reference_file_path_list

    def get_video_path(self):
        """動画のパス取得

        Returns:
            動画のパス
        """
        return self._video_path
