from sqlalchemy import text



def test_db_connect(test_session):
    result = test_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

