from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated

from pyramid.session import UnencryptedCookieSessionFactoryConfig
import os
import logging

from .models import (
    DBSession,
    Base,
    )

here = os.path.dirname(os.path.abspath(__file__))
log = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    settings['mako.directories'] = os.path.join(here,'templates')

    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(settings=settings,root_factory='.models.RootFactory', session_factory=session_factory)

    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission(Authenticated)

    config.add_static_view('static', 'static')
    config.add_static_view('attachment',os.path.join(here, 'static/attachments'))
    config.add_static_view('css',os.path.join(here, 'static/css'))
    config.add_static_view('js',os.path.join(here, 'static/js'))
    config.include('pyramid_chameleon')


    """ Routes Here """
    config.add_route('home', '/')
    config.add_route('profile', '/profile')
    config.add_route('about', '/about')
    
    config.add_route('registerStudent', '/register_student')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('instituteGetAll', '/institute_get_all')
    config.add_route('instituteGet', '/institute_get/{id}')

    config.add_route('studentCourses', '/student_courses')

    config.add_route('courseGetAll', '/course_get_all')
    config.add_route('courseInstituteGetAll', '/course_institute_get_all')
    config.add_route('courseFaculty', '/course_faculty/{course_id}')
    config.add_route('courseResource', '/course_resource/{course_id}')
    config.add_route('courseAssignment', '/course_assignment/{course_id}')
    config.add_route('courseMarks', '/course_marks/{course_id}')
    config.add_route('courseQuiz', '/course_quiz/{course_id}')
    config.add_route('courseGet', '/course_get/{id}')

    config.add_route('courseRegister', '/course_register')
    
    config.scan()
    return config.make_wsgi_app()
