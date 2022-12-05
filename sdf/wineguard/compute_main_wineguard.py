# System packages
from concurrent.futures import ThreadPoolExecutor
from json import loads


# Local packages
from sdf.utils.user_input import parse_main_args, create_request
from sdf.farmbios.dispatcher import Dispatcher
from sdf.farmbios.compute_handler import ComputeRPCHandler
from sdf.helper_typedefs import Modules as mod
from sdf.network.status import CommunicationStatus as comstatus
from sdf.network.network_controller import NetworkController 
from sdf.wineguard.wineguard_compute import WineGuardCompute 
from sdf.wineguard.wineguard_config import WineGuardComputeConfig


__author__ = "Gloire Rubambiza"
__email__ = "gbr26@cornell.edu"
__credits__ = ["Gloire Rubambiza"]


# Main method
if __name__ == "__main__":
    
    args =  parse_main_args()
    config_file_path = args['config_file']

    # Read the application config and create the module config object
    config = None
    try:
        with open(config_file_path, 'r') as fd:
            config = loads(fd.read())
            config = WineGuardComputeConfig(config)
    except FileNotFoundError as fnf:
        print("Config file %s not found... exiting" % config_file_path)
        exit(1)


    # Create the net_ctrl that drives the underlying network layer sockets.
    net_ctrl = NetworkController()
    net_ctrl.create_components(config.compute_address[1])

    # Set the configuration's network controller
    config.net_ctrl = net_ctrl

    # Create the modules to be used
    compute_module = WineGuardCompute(config)
                                                
    # Create the handlers to be used by the dispatch.
    handlers = {
                mod.COMPUTE: ComputeRPCHandler(compute_module),
               } 

    # Create the RPC dispatcher
    dispatcher = Dispatcher(handlers, config)

    # Set the network controller's dispatcher
    net_ctrl.set_dispatcher(dispatcher)

    # Set the dispacher's network manager.
    dispatcher.set_network_manager(net_ctrl.net_mgr)

    # A pool of threads to be used for file and message checks. 
    pool = ThreadPoolExecutor(1)

    # Run a thread whose job is to check for new messages.
    spin_thread_future = pool.submit(net_ctrl.spin_server_forever)
    spin_thread_future.add_done_callback(net_ctrl.check_on_threads)

    # Take user requests.
    while True:
        request = create_request()
        if request[0] == "add_server":
            remote_host = request[1]
            remote_port = int(request[2])
            conn = net_ctrl.client.connect_to_peer(remote_host,
                                                   remote_port)
            if conn != comstatus.SOCKET_ERROR:
                net_ctrl.net_mgr.add_connection(conn, port=remote_port,
                                                outgoing=True)
                net_ctrl.net_mgr.add_remote_peer(tuple([remote_host,
                                                       remote_port]))
            else:
                 print("Connection to (%s, %s) failed...\n" % (remote_host,
                                                              remote_port))
        else: # Exit
            print("Received a signal to exit, releasing resources\n")
            net_ctrl.exit_signal = True
            handlers[mod.COMPUTE].module.exit_signal = True
            break 

    # Wait on all the threads to exit
    pool.shutdown(wait=True)
