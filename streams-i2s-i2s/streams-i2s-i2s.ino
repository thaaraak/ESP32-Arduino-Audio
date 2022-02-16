/**
 * @file streams-i2s-filter-i2s.ino
 * @brief Copy audio from I2S to I2S using an FIR filter
 * @author Phil Schatzmann
 * @copyright GPLv3
 */

#include "AudioTools.h"
 
uint16_t sample_rate=44100;
uint16_t channels = 2;
I2SStream in;
StreamCopy copier(in, in); // copies sound into i2s

// Arduino Setup
void setup(void) {  
  // Open Serial 

  Serial.begin(115200);
  // change to Warning to improve the quality
  AudioLogger::instance().begin(Serial, AudioLogger::Error); 

  // start I2S in
  auto config = in.defaultConfig(RXTX_MODE);
  config.sample_rate = sample_rate;
  config.bits_per_sample = 16;
  config.i2s_format = I2S_STD_FORMAT;
  config.is_master = true;
  config.port_no = 0;
  config.pin_ws = 18;
  config.pin_bck = 5;
  config.pin_data = 19;
  config.pin_data_rx = 17;
  config.pin_mck = 0;
  config.use_apll = true;
  in.begin(config);

  Serial.println("I2S started...");
}

// Arduino loop - copy sound to out 
void loop() {
  copier.copy();
}
