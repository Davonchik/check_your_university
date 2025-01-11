# from tests.test_1 import db_session
# from src.infrastructure.database.models.request import Request
# from src.infrastructure.database.dao.request_dao import RequestDao


# class TestRequestDao:
#     async def test_get_requests(self, db_session):
#         request_dao = RequestDao(db_session)
#         request = Request(name='test')
#         db_session.add(request)
#         await db_session.commit()
        
#         requests_out = await request_dao.get_requests()
#         assert len(requests_out) == 1
#         assert requests_out[0].name == 'test'

    
#     async def test_update_request(self, db_session):
#         request_dao = RequestDao(db_session)
#         request = Request(name='test')
#         db_session.add(request)
#         await db_session.commit()
        
#         request_out = await request_dao.update_request(1, Request(name='test2'))
#         assert request_out.name == 'test2'


#     async def test_create_request(self, db_session):
#         request_dao = RequestDao(db_session)
#         request = Request(name='test')



#         db_session.add(request)
#         await db_session.commit()
        
#         request_out = await request_dao.create_request(Request(name='test2'))
#         assert request_out.name == 'test2'