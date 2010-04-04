import sys
# Install the Linux Epoll Reactor
from twisted.internet import epollreactor
epollreactor.install()
        
from goliat.webserver.site import SetupSite, SiteConfig
from twisted.application import internet, service
        
application = service.Application("Goliat Application")
        
goliat_app_site = SetupSite()
httpserver = internet.TCPServer(SiteConfig.getPort(), goliat_app_site)
httpserver.setServiceParent(application)
