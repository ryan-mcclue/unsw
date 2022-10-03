
// Commands:
// EDG (Edge Data Generation) which means the client side helps to generate data to simulate the data collection function in the real edge device, 
// UED (Upload Edge Data) it allows the edge device to upload a particular edge data file to the central server,
// SCS (Server Computation Service) the edge device can practice this command to request the server to
//do some basic computations on a particular data file, 
// DTE (Delete the data file (server side)), 
// AED (Active Edge Devices), request and display the active edge devices, OUT: exit this edge network, and
// UVF (Peer-to-peer Uploading Video Files)

int
main(int argc, char *argv[])
{
  if (argc == 4)
  {
    // prompt_credentials()
    // send_authentication()
    // parse_return()
    // if (success)
    // {
    //   send_udp_port_num()
    //   prompt_for_command()
    // }
    
    // running a udp server concurrently
    // furthermore, new thread for client upload
  }
  else
  {
    fprintf(stderr, "Usage: ./client <server-ip> <server-port> <client-udp_port>\n");
  }
  // request_connection()
  // send_name_and_password() 
  // --> recieve welcome message and command listing prompt
  // send_p2p_udp_port_num()

  return 0;
}
