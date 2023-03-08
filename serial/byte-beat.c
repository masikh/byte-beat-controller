/**
 * Copyright (c) 2022 GPLv1
 *
 * The pico setup has:
 * two buttons with a led embedded. On push it lids up, else it pulses
 * two potential meters.
 *
 * This program reads the status of the potential meters and buttons (plus the PWM) on core 1
 * On core 0, the pico handles an interrupt (RX on UART) an spits out the read data on the TX line of UART1
 *
 * minicom:
 *      minicom -b 115200 -o -D /dev/tty.usbmodem101
 *      minicom -b 115200 -o -D /dev/tty.usbmodem1101
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"
#include "hardware/irq.h"
#include "hardware/pwm.h"
#include "hardware/spi.h"
#include "hardware/uart.h"
#include "pico/multicore.h"


#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"

int sin_table[180];
int sample_rate = 0;


struct UART_INTERFACE {
    uart_inst_t* uart_id;
    int baud_rate;
    int data_bits;
    int stop_bits;
    uart_parity_t parity;
    int rx;
    int tx;
    int irq;
};

struct LedButton {
    int button_pin;
    int led_pin;
    bool status;
    uint slice_num;
};

struct PotMeter {
    int pin;
    int input;
    uint16_t value;
};

struct LedButton button_0 = {15, 16, false, 0};
struct LedButton button_1 = {14, 17, false, 0};
struct PotMeter pot_meter_0 = {26, 0, 0};
struct PotMeter pot_meter_1 = {27, 1, 0};
struct UART_INTERFACE uart_0 = {uart1, 115200, 8, 1, UART_PARITY_NONE, 4, 5,  0};

// Function for building a sinus table
void create_sinus_table() {
    double accuracy = 0.0001, denominator, sinx, sinval;
    for (int i = 0; i < 180; i++) {
        // Converting degrees to radian
        double n = (double) i * (3.142 / 180.0);
        double x1 = n;

        // maps the sum along the series
        sinx = n;

        // holds the actual value of sin(n)
        sinval = sin(n);
        int j = 1;
        do {
            denominator = 2 * j * (2 * j + 1);
            x1 = -x1 * n * n / denominator;
            sinx = sinx + x1;
            j = j + 1;
        } while (accuracy <= fabs(sinval - sinx));
        sin_table[i] = (int) (sinx * 255);
    }
}

// Interrupt handler
void on_uart_rx() {
    char msg_string[100];

    // read as ascii char
    uint8_t cid = uart_getc(uart_0.uart_id);
    /*
    printf("{\"adc0\": %d, \"adc1\": %d, \"btn0\": %s, \"btn1\": %s, \"sr\": \"%d/s\", \"cid\": %d}",
           pot_meter_0.value, pot_meter_1.value,
           button_0.status ? "true" : "false", button_1.status ? "true" : "false",
           sample_rate,
           cid);
    */
    if (uart_is_writable(uart_0.uart_id)) {
        // Create JSON string
        sprintf(msg_string, "{\"adc0\": %d, \"adc1\": %d, \"btn0\": %s, \"btn1\": %s, \"sr\": \"%d/s\", \"cid\": %d}",
               pot_meter_0.value, pot_meter_1.value,
               button_0.status ? "true" : "false", button_1.status ? "true" : "false",
               sample_rate,
               cid);
        printf("%s", msg_string);

        // Send JSON to UART
        uart_puts(uart_0.uart_id, msg_string);
    }
};

// Initialize all uart, adc, gpio etc...
void initialize () {
    stdio_init_all();

    adc_init();
    adc_gpio_init(pot_meter_0.pin);   // Make sure GPIO is high-impedance, no pullups etc
    adc_gpio_init(pot_meter_1.pin);   // Make sure GPIO is high-impedance, no pullups etc

    gpio_set_function(button_0.led_pin, GPIO_FUNC_PWM);
    gpio_set_function(button_1.led_pin, GPIO_FUNC_PWM);

    button_0.slice_num = pwm_gpio_to_slice_num(button_0.led_pin);
    button_1.slice_num = pwm_gpio_to_slice_num(button_1.led_pin);

    pwm_set_wrap(button_0.slice_num, 255);
    pwm_set_wrap(button_1.slice_num, 255);

    pwm_set_chan_level(button_0.slice_num, PWM_CHAN_A, 0);
    pwm_set_chan_level(button_1.slice_num, PWM_CHAN_B, 0);

    pwm_set_enabled(button_0.slice_num, true);
    pwm_set_enabled(button_1.slice_num, true);

    gpio_init(button_0.button_pin);
    gpio_init(button_1.button_pin);

    gpio_set_dir(button_0.button_pin, GPIO_IN);
    gpio_set_dir(button_1.button_pin, GPIO_IN);

    gpio_pull_up(button_0.button_pin);
    gpio_pull_up(button_1.button_pin);

    // Set up our UART with a basic baud rate.
    uart_init(uart_0.uart_id, 2400);
    gpio_set_function(uart_0.rx, GPIO_FUNC_UART);
    gpio_set_function(uart_0.tx, GPIO_FUNC_UART);
    uart_set_baudrate(uart_0.uart_id, uart_0.baud_rate);
    // Set UART flow control CTS/RTS, we don't want these, so turn them off
    uart_set_hw_flow(uart_0.uart_id, false, false);
    // Set our data format
    uart_set_format(uart_0.uart_id, uart_0.data_bits, uart_0.stop_bits, uart_0.parity);
    // Turn off FIFO's - we want to do this character by character
    uart_set_fifo_enabled(uart_0.uart_id, false);

    // Set up a RX interrupt
    uart_0.irq = uart_0.uart_id == uart0 ? UART0_IRQ : UART1_IRQ;
    // And set up and enable the interrupt handlers
    irq_set_exclusive_handler(uart_0.irq, on_uart_rx);
    irq_set_enabled(uart_0.irq, true);

    // Now enable the UART to send interrupts - RX only
    uart_set_irq_enables(uart_0.uart_id, true, false);
}

// Check if a button has switched
bool button_switch(struct LedButton *button) {
    if (!gpio_get(button->button_pin)) {
        button->status = true;
        return true;
    }
    button->status = false;
    return false;
}

// Read from an ADC
void read_adc(struct PotMeter *adc) {
    adc_select_input(adc->input);
    uint16_t value = adc_read();
    if (value < 25) {
        value = 0;
    }
    value = abs(value - 4095);
    adc->value = value;
}

// Read all sensor data in cpu-core 1
void core1_sensor_reader() {
    bool last_btn0_value = false;
    bool last_btn1_value = false;
    int count = 180;  // size of sinus table
    int sample_count = 0;
    clock_t epoch = time_us_64();
    clock_t epoch2 = time_us_64();

    while (true) {
        if ((time_us_64() - epoch) > 7777) {  // 5555 == 1/180 st of a second in microseconds
            count = (count + 1) % 180;
            epoch = time_us_64();
        }
        // if ((time_us_64() - epoch2) > 500000) { // 1/2 second
        if ((time_us_64() - epoch2) > 500) { // 1/2 second
            epoch2 = time_us_64();
            sample_rate = sample_count * 2;  // samples per second...
            sample_count = 0;
            multicore_fifo_push_blocking(true);
        }
        sample_count += 1;

        bool btn_value0 = button_switch(&button_0);
        bool btn_value1 = button_switch(&button_1);
        if (btn_value0 == true) {
            pwm_set_chan_level(button_0.slice_num, PWM_CHAN_A,255);
        } else {
            pwm_set_chan_level(button_0.slice_num, PWM_CHAN_A, sin_table[count]);
        }

        if (btn_value1 == true) {
            pwm_set_chan_level(button_1.slice_num, PWM_CHAN_B,255);
        } else {
            pwm_set_chan_level(button_1.slice_num, PWM_CHAN_B, sin_table[count]);
        }

        if (last_btn0_value != btn_value0) {
            // Send message to cpu-core0
            multicore_fifo_push_blocking(true);
            last_btn0_value = btn_value0;
        }

        if (last_btn1_value != btn_value1) {
            // Send message to cpu-core0
            multicore_fifo_push_blocking(true);
            last_btn1_value = btn_value1;
        }

        read_adc(&pot_meter_0);  // potential meter
        read_adc(&pot_meter_1);  // potential meter
    }
}

// Main loop on cpu-core 0
int main() {
    initialize();  // setup all IO configurations
    multicore_launch_core1(core1_sensor_reader);
    sleep_ms(1000);
    create_sinus_table();

    printf("\nWelcome to the Byte-Beat IO-Controller v0.3\n\n");
    while (true) {
        // check if core1 reported button status change
        bool got_data = multicore_fifo_rvalid();
        if (got_data) {
            multicore_fifo_pop_blocking();
        }
    }
    return 0;
}

#pragma clang diagnostic pop