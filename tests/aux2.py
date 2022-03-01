from time import sleep

try:
    while True:
        sleep(0.5)
        print("Still running...")
except KeyboardInterrupt:
    print("Keyboard interrupt")
    sleep(2)
    print("programa terminado correctamente")
    