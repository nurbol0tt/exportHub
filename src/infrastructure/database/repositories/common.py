from src.domain.common.interfaces.uow import get_session


class SQLAlchemyRepo:
    def __init__(self, session: get_session):
        self.session = session
