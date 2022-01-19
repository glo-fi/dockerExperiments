FROM alpine:3.5

RUN apk add --no-cache tcpdump

VOLUME ["/data"]

ENTRYPOINT ["/usr/sbin/tcpdump"]
