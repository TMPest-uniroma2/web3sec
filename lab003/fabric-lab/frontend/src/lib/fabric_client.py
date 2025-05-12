import os
import json
from hfc.fabric import Client as FabricClient
from hfc.fabric_ca.caservice import CAClient, CAService
from hfc.fabric.transaction.tx_context import TXContext
from hfc.fabric.transaction.tx_proposal_request import TXProposalRequest

class FabricHelper:
    def __init__(self, net_profile, channel_name, org_name, user_name, cc_name):
        # Create a client instance
        self.client = FabricClient(net_profile=net_profile)
        self.channel_name = channel_name
        self.org_name = org_name
        self.user_name = user_name
        self.cc_name = cc_name
        self.net_profile = net_profile

        # Print debug information
        print(f"Initializing Fabric client:")
        print(f"  Channel: {channel_name}")
        print(f"  Organization: {org_name}")
        print(f"  User: {user_name}")
        print(f"  Chaincode: {cc_name}")

        # Initialize CA client
        self._init_ca_client()

        # Enroll the user if necessary
        self._ensure_user_enrolled()

    def _init_ca_client(self):
       try:
           with open(self.net_profile, 'r') as f:
               net_profile_data = json.load(f)

           ca_name_key = f"ca.{self.org_name.lower()}.example.com"
           if ca_name_key in net_profile_data.get('certificateAuthorities', {}):
               ca_info = net_profile_data['certificateAuthorities'][ca_name_key]
               ca_url = ca_info['url']
               ca_name = ca_info.get('caName', ca_name_key)

               # Initialize CAService directly
               self.ca_service = CAService(ca_name=ca_name, target=ca_url)

               print(f"CA Service initialized for: {ca_url}")
               return self.ca_service
           else:
               raise ValueError(f"CA information not found for {ca_name_key}")
       except Exception as e:
           print(f"Error initializing CA client: {e}")
           raise


    def _ensure_user_enrolled(self):
        try:
            user = self.client.get_user(self.org_name, self.user_name)
            if user:
                print(f"User {self.user_name} already exists in wallet/store.")
            else:
                print(f"User {self.user_name} not found, enrolling.")
                user = self._enroll_user()

            print(f"Loaded user: {user}, MSP: {getattr(user, 'msp_id', None)}")
            return user
        except Exception as e:
            print(f"User {self.user_name} not found or error occurred: {e}")
            return self._enroll_user()

    def _enroll_user(self):
        """Enroll the user with the CA"""
        try:
            # Get CA credentials from connection profile
            with open(self.net_profile, 'r') as f:
                net_profile_data = json.load(f)

            ca_name = f"ca.{self.org_name.lower()}.example.com"
            if ca_name in net_profile_data.get('certificateAuthorities', {}):
                ca_info = net_profile_data['certificateAuthorities'][ca_name]
                if 'registrar' in ca_info:
                    password = ca_info['registrar'].get('enrollSecret', 'adminpw')
                else:
                    password = 'adminpw'  # Default
            else:
                password = 'adminpw'  # Default

            # Enroll the user
            enrollment = self.ca_service.enroll(self.user_name, password)

            # Get the MSP ID for the organization
            msp_id = f"{self.org_name}MSP"
            if self.org_name in net_profile_data.get('organizations', {}):
                org_info = net_profile_data['organizations'][self.org_name]
                msp_id = org_info.get('mspid', msp_id)

            # Create the user
            user = self.client.create_user(
                name=self.user_name,
                org=self.org_name,
                state_store=self.client.state_store,
                msp_id=msp_id,
                enrollment=enrollment
            )

            print(f"Successfully enrolled user {self.user_name}")
            return user
        except Exception as e:
            print(f"Failed to enroll user: {e}")
            raise

    def set_data(self, key, value):
        """Set data in the chaincode"""
        print(f"Setting data: key={key}, value={value}")

        try:
            # Make sure we have an enrolled user
            user = self._ensure_user_enrolled()

            # Create a new transaction ID
            tx_id = TXContext(user, self.client.crypto_suite)

            # Get the channel
            channel = self.client.get_channel(self.channel_name)
            if channel is None:
                print(f"Channel {self.channel_name} not found, creating it")
                channel = self.client.new_channel(self.channel_name)

            # Use the chaincode invoke method
            args = [key, value]

            # Get peers and orderers
            peers = list(channel.peers.values())
            orderers = list(channel.orderers.values())

            if not peers:
                raise ValueError("No peers found in the channel")
            if not orderers:
                raise ValueError("No orderers found in the channel")

            print(f"Available peers: {[p.name for p in peers]}")
            print(f"Available orderers: {[o.name for o in orderers]}")

            # Create a proposal
            proposal = channel.chaincode_invoke_proposal(
                tx_id,
                peers[0],
                self.cc_name,
                args,
                'SetData'
            )

            # Send the proposal
            responses, proposal, header = channel.send_proposal(proposal)

            # Check responses
            print(f"Received {len(responses)} response(s)")
            for i, response in enumerate(responses):
                print(f"Response {i}: status={response.response.status}, message={response.response.message}")

            # Send the transaction
            response = channel.send_transaction((responses, proposal, header), orderers[0])

            print(f"Transaction response: {response}")
            return response
        except Exception as e:
            print(f"Error in set_data: {e}")
            print(f"Error type: {type(e)}")
            raise


    def get_data(self, key):
        """Get data from the chaincode"""
        print(f"Getting data for key: {key}")

        try:
            # Ensure the user is enrolled
            user = self._ensure_user_enrolled()

            # Create the transaction proposal request
            tx_prop_req = TXProposalRequest()
            tx_prop_req.args = [key]
            tx_prop_req.fcn = 'GetData'
            tx_prop_req.cc_name = self.cc_name
            tx_prop_req.cc_type = 'golang'  # Adjust if using a different chaincode language

            # Create the transaction context
            tx_context = TXContext(user, self.client.crypto_suite, tx_prop_req)

            # Get the channel
            channel = self.client.get_channel(self.channel_name)
            if channel is None:
                print(f"Channel {self.channel_name} not found, creating it")
                channel = self.client.new_channel(self.channel_name)

            # Get peers
            peers = list(channel.peers.values())
            if not peers:
                raise ValueError("No peers found in the channel")

            print(f"Available peers: {[p.name for p in peers]}")

            # Create and send the proposal
            proposal = channel.chaincode_query_proposal(
                tx_context,
                peers[0],
                self.cc_name,
                [key],
                'GetData'
            )
            responses, proposal, header = channel.send_proposal(proposal)

            # Process responses
            print(f"Received {len(responses)} response(s)")
            for i, response in enumerate(responses):
                print(f"Response {i}: status={response.response.status}, message={response.response.message}")
                if response.response.payload:
                    print(f"Payload: {response.response.payload}")

            # Return the payload from the first response
            if responses and len(responses) > 0:
                response = responses[0]
                if response.response and response.response.payload:
                    payload = response.response.payload
                    if isinstance(payload, bytes):
                        payload = payload.decode('utf-8')
                    try:
                        return json.loads(payload)
                    except json.JSONDecodeError:
                        return payload

            return None
        except Exception as e:
            print(f"Error in get_data: {e}")
            print(f"Error type: {type(e)}")
            raise


