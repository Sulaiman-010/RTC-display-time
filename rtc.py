from machine import Pin, I2C
import utime

# Define the I2C bus
i2c = I2C(scl=Pin(22), sda=Pin(21))

# RTC3231 address
RTC_ADDR = 0x68

# Function to read time from RTC
def read_rtc_time():
    # Send a command byte to set the RTC register pointer to the time
    i2c.writeto(RTC_ADDR, bytes([0x00]))
    
    # Read 7 bytes of data from the RTC
    rtc_data = i2c.readfrom(RTC_ADDR, 7)
    
    # Extract the time components
    # end wali the most significant bit remove hoti wo show krwati ke kesy clock chal rhi ya nai is liye
    # 0x7f likha ha
    second = bcd_to_decimal(rtc_data[0] & 0x7F)  # Seconds (0-59)
    minute = bcd_to_decimal(rtc_data[1] & 0x7F)  # Minutes (0-59)
    hour = bcd_to_decimal(rtc_data[2] & 0x3F)    # Hours (0-23 for 24-hour format)
    return hour, minute, second

# Function to convert BCD to decimal
def bcd_to_decimal(bcd_value):
    return ((bcd_value & 0xF0) >> 4) * 10 + (bcd_value & 0x0F)
    # 0xf0 means 11110000     0x0f means 00001111

while True:
    # Read time from RTC
    hour, minute, second = read_rtc_time()
    # Print the time
    print("Time from RTC: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
    utime.sleep(1)  # Wait for 1 second
