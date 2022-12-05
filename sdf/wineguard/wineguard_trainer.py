# System imports
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from time import time
from typing import Any, Dict


# Local packages
from sdf.compute.base_compute import ComputeModule
from sdf.farmbios.base_handler import BaseRPCHandler 
from sdf.farmbios.proto.compute_pb2 import ComputeRPC
from sdf.farmbios.proto.farmbios_pb2 import FarmBIOSMessage
from sdf.farmbios.proto.shared_pb2 import CallType
from sdf.helper_typedefs import Modules as mod
from sdf.network.network_controller import NetworkController 
from sdf.wineguard.callback_enum_defs import WineGuardComputeCallBacks \
                                             as wing_co_cb 
from sdf.wineguard.proto.wineguard_pb2 import ExperimentResult
from sdf.wineguard.wineguard_config import WineGuardComputeConfig 

# Third party packages
from azureml.core import Dataset, Workspace


__author__ = "Gloire Rubambiza"
__email__ = "gbr26@cornell.edu"
__credits__ = ["Gloire Rubambiza"]


# @brief: The trainer module for the WineGuard application.
class WineGuardTrainer(ComputeModule):

    def __init__(self,
                 config: WineGuardComputeConfig,
                 *args: Any,
                 **kwargs: Any):
        super().__init__()
        self.config = config


    def set_dispatcher(self, dispatcher: Any):
        """
           Set the dispatcher that sends requests and responses to peer modules.
           :param dispatcher: Self-explanatory.
        """
        self.dispatcher = dispatcher


    def handle_callback(self,
                        message: FarmBIOSMessage,
                        callback_func: wing_co_cb,
                        **kwargs):
       """
           Call the appropriate handler for compute module call backs.
           :param message: The message with the response for the call back.
           :param callback_func: The local function to pass the message to.
       """
       self.log("HANDLING CALL BACK FOR: %s\n" % callback_func.name)
       if callback_func == wing_co_cb.PROCESS_RESULTS:
           return self.process_results(message)
       else:
           self.log("Unknown call back %s\n" % callback_func.name)
           return None, None


    def process_results(self, message: FarmBIOSMessage):
        """
           Process the results from the training/prediction run.
           :param message: The message from the wire.
        """
        result_msg = ExperimentResult()
        result_msg.ParseFromString(message.data)
        summary = result_msg.resultSummary
        if (type(summary) == str) and ("portal" in summary):
            self.log("\nResult can be seen at %s\n" % summary)
        else:
            self.log("\nResult: %s\n" % summary)

        return None, None


    def run(self,
            net_ctrl: NetworkController,
            handlers: Dict[mod, BaseRPCHandler]):
        """
           Run the thread for listening to user requests
           :param net_ctrl: The network handler.
           :param handlers: The dictionary of request handlers.
        """
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


    def analytics(self):
        """
           Submit a model training experiment.
        """
        compute_msg = ComputeRPC()
        compute_msg.procedure.call = CallType.RUN
        exp_name = self.config.exp_setup.experimentName
        exp_name = 'farmbioswineguard-' + str(date.today()) 
        exp_name += '-' + str(int(time()))
        self.config.exp_setup.experimentName = exp_name
        compute_msg.proc_args = self.config.exp_setup.SerializeToString()

        # Register a call back to process the results
        outgoing_msg = self.dispatcher.compose_outbound(compute_msg,
                                                        mod.COMPUTE,
                                                        mod.COMPUTE,
                                                        wing_co_cb.PROCESS_RESULTS
                                                       )
        self.dispatcher.dispatch_message(outgoing_msg)

        # Insert model training/registration stuff somewhere here.


    def get_workspace(self, args):
        """ 
            Set up the workspace configuration.
        """
        pass
