from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember,authenticated_userid, forget, Authenticated

from pyramid.httpexceptions import HTTPFound

from .models import DBSession
from .models import Institute

from sqlalchemy import and_

@view_config(
	route_name='instituteGetAll',
	renderer='json',
	request_method='GET',
	permission='__no_permission_required__'
)
def instituteGetAll(request):

	instituteQuery = DBSession.query(Institute)

	institutes = []
	for institute in instituteQuery.all():
		institutes.append(institute.getJSON())

	return {'institutes' : institutes}

