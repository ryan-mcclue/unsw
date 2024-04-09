FROM ubuntu:latest

COPY lookt /usr/local/bin/lookt

ENTRYPOINT ["/usr/local/bin/lookt"]

# docker build -t <name> .
#   docker images

# docker run --network host --rm <name> <arg1> <arg2>
#   the '--rm' prevents being saved for: docker ps -a 
#   and subsequent force removal: docker rmi -f <name>
#   would add '-it' if want to interact with terminal
