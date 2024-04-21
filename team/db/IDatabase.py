from typing import Protocol, List


class IDatabase(Protocol):
    @staticmethod
    def __get_db() -> None:
        raise NotImplementedError

    @staticmethod
    def close_db() -> None:
        raise NotImplementedError

    @staticmethod
    def init_db() -> None:
        raise NotImplementedError

    @staticmethod
    def reset() -> None:
        raise NotImplementedError

    @staticmethod
    def get_records() -> List:
        raise NotImplementedError

    @staticmethod
    def add_record():
        raise NotImplementedError

    @staticmethod
    def edit_record():
        raise NotImplementedError
