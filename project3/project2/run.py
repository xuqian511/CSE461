import sys
import proxy as proxy

if __name__ == "__main__":
    server = proxy.ProxyServer('', int(sys.argv[1]))
    try:
        server.run()
    except KeyboardInterrupt:
        print('KeyboardInterrupt: stopping server')
        sys.exit(1)