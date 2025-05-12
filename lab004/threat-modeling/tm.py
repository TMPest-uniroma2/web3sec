from pytm import TM, Boundary, Server, Datastore, Actor, Dataflow

tm = TM("Sample project for students to start with")

# Trust Boundaries
docker_network = Boundary("Docker Network")
user_boundary = Boundary("User Boundary")
blockchain_boundary = Boundary("Blockchain Boundary")

# Actors
user = Actor("User", inBoundary=user_boundary)

# Servers and Services
blockchain = Server("Blockchain", inBoundary=blockchain_boundary)
va = Server("Verification-Authority", inBoundary=blockchain_boundary)
frontend_app = Server("Application (Frontend)", inBoundary=docker_network)
nginx_proxy = Server("Nginx Proxy", inBoundary=docker_network)
db = Datastore("MysqlDB", inBoundary=docker_network, sensitive=True)

# Server Attributes
nginx_proxy.protocol = "HTTPS"
db.encrypted_at_rest = True

# Dataflows
# User Interaction through App
Dataflow(user, nginx_proxy, "User accesses app", protocol="HTTPS")

# TODO

# Outputs the model
tm.process()
