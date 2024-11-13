# hardware.py
try:
    import RPi.GPIO as GPIO  # type: ignore # För riktiga Raspberry Pi-enheter
    IS_PI = True
except ImportError:
    # Mock GPIO för utveckling på andra system
    class MockGPIO:
        BCM = "BCM"
        IN = "IN"
        HIGH = 1
        LOW = 0

        @staticmethod
        def setmode(mode):
            print(f"Mock setmode: {mode}")

        @staticmethod
        def setup(pin, mode):
            print(f"Mock setup: pin={pin}, mode={mode}")

        @staticmethod
        def input(pin):
            print(f"Mock input: pin={pin}")
            return MockGPIO.LOW  # Returnera LOW för test
            #return MockGPIO.HIGH  # Returnera HIGH för att simulera att sensorn aktiveras

        @staticmethod
        def cleanup():
            print("Mock cleanup")

    GPIO = MockGPIO
    IS_PI = False

# Funktion för att initiera hårdvaruinställningar
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
    GPIO.setup(27, GPIO.IN)

# Funktion för att läsa en GPIO-ingång
def read_gpio(pin):
    return GPIO.input(pin)

# Funktion för att städa upp
def cleanup_gpio():
    GPIO.cleanup()
