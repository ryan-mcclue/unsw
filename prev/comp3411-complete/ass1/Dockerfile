FROM ubuntu:latest

COPY bridgen /usr/local/bin/bridgen

ENTRYPOINT ["/usr/local/bin/bridgen"]

# docker build -t <name> .
#   docker images

# docker run --rm example <arg1> <arg2>
#   the '--rm' prevents being saved for: docker ps -a 
#   and subsequent force removal: docker rmi -f <name>
#   would add '-it' if want to interact with terminal
