#include "esp_camera.h"
#define CAMERA_MODEL_AI_THINKER
#include "BluetoothSerial.h"
#include "camera_pins.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

const int outPin=33;
const int outLed=1;
const int inPin=3;

// input symbol
// 0:released, 1:pressed
int inSymb;

// states
// 0:A, 1:B
int iState;
int futureState;

void callback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param) {
  if (event == ESP_SPP_SRV_OPEN_EVT) {
    Serial.println("Client Connected has address:");
    for (int i = 0; i < 6; i++) {
      Serial.printf("%02X", param->srv_open.rem_bda[i]);
      if (i < 5) {
        Serial.print(":");
      }
    }
  }
}

void initBT(){
  SerialBT.register_callback(callback);
  if(!SerialBT.begin("ESP32CAM-BT")){
    Serial.println("An error occurred initializing Bluetooth");
    ESP.restart();
  }else{
    Serial.println("Bluetooth initialized");
  }
  Serial.println("The device started, now you can pair it with bluetooth");
}

void setup() {
  Serial.begin(115200);
  Serial.print("Starting............");
  initBT();
  initCamera();
  
  pinMode(outPin, OUTPUT);
  //pinMode(outLed, OUTPUT);
  //pinMode(inPin, INPUT);
  digitalWrite(outLed, HIGH); 

  // initial state
  iState = 0;
}

void writeSerialBT(camera_fb_t *fb){
  SerialBT.write(fb->buf, fb->len);
  SerialBT.flush();
}

void initCamera(){
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  //init with high specs to pre-allocate larger buffers
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    ESP.restart();
  }
}

void capture(){
  camera_fb_t *fb = NULL;
  esp_err_t res = ESP_OK;
  fb = esp_camera_fb_get();
  if(!fb){
    esp_camera_fb_return(fb);
    return;
  }
  if(fb->format != PIXFORMAT_JPEG){
    return;
  }
  writeSerialBT(fb);
  esp_camera_fb_return(fb);
}

void loop() {
  
  // 1) Read external inputs and generate input symbols
  // punto da cambiare quando si dovrà leggere il valore del sensore ultrasonico
  int inval = digitalRead(inPin);
  if (inval == LOW)
    inSymb = 0;
  else
    inSymb = 1;

  // 2) Future state estimation
  switch(iState){
    case 0:{
      if(inSymb == 1) //Pressed
        futureState = 1;
      if(inSymb == 0) //Released
        futureState = 0;
      break;
    }
    case 1:{
      if(inSymb == 1) //Pressed
        futureState = 1;
      if(inSymb == 0) //Released
        futureState = 0;
      break;
    }     
  }

  // 3) OnEntry and onExit actions
  if ((iState == 1) && (futureState == 0)){
    if (Serial.available()) { 
      //capture();
      SerialBT.write('C');
    }
  }

  // 4) State transition [clock edge]
  iState = futureState;

  // 5) Output update
  switch(iState){
      case 0: digitalWrite(outPin, HIGH); break;
      case 1: digitalWrite(outPin, LOW); break;
  }
}
