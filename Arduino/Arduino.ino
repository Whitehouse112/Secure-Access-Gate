#include "esp_camera.h"
#define CAMERA_MODEL_AI_THINKER
#include "BluetoothSerial.h"
#include "camera_pins.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

// pins
const int outPin=33;
const int trigPin = 3;
const int echoPin = 1;

// distance
long duration;
int distance;

// input symbol
// 0:released, 1:pressed
int inSymb;

// states
// 0:A, 1:B
int iState;
int futureState;

void setup() {
  Serial.begin(115200);
  initBT();
  initCamera();
    
  pinMode(outPin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // initial state
  iState = 0;
}

void callback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param) {
  if (event == ESP_SPP_SRV_OPEN_EVT) {
    Serial.println("\nClient Connected has address:");
    for (int i = 0; i < 6; i++) {
      Serial.printf("%02X", param->srv_open.rem_bda[i]);
      if (i < 5) {
        Serial.print(":");
      }
    }
  }
  else if(event == ESP_SPP_DATA_IND_EVT){
    Serial.printf("\n\nESP_SPP_DATA_IND_EVT len=%d, handle=%d", param->data_ind.len, param->data_ind.handle);
    String stringRead = String(*param->data_ind.data);
    int paramInt = stringRead.toInt() - 48;
    Serial.printf("\nparamInt: %d", paramInt);
    //setCameraParam(paramInt);
  }
}

void initBT(){
  if(!SerialBT.begin("ESP32CAM-BT")){
    Serial.println("\nAn error occurred initializing Bluetooth");
    ESP.restart();
  }else{
    Serial.println("\nBluetooth initialized");
  }
  Serial.println("The device started, now you can pair it with bluetooth");
  SerialBT.register_callback(callback);
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
    config.frame_size = FRAMESIZE_SXGA;
    config.jpeg_quality = 15;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SXGA;
    config.jpeg_quality = 10;
    config.fb_count = 1;
  }
  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("\nCamera init failed with error 0x%x", err);
    ESP.restart();
  }
}

void setCameraParam(int paramInt){
  sensor_t *s = esp_camera_sensor_get();
  switch(paramInt){
    case 3:
      s->set_framesize(s, FRAMESIZE_UXGA);
      Serial.print("\nImage's quality changed to UXGA");
    break;
    case 2:
      s->set_framesize(s, FRAMESIZE_SXGA);
      Serial.print("\nImage's quality changed to SXGA");
    break;
    case 1:
      s->set_framesize(s, FRAMESIZE_SVGA);
      Serial.print("\nImage's quality changed to SVGA");
    break;
    case 0:
      s->set_framesize(s, FRAMESIZE_VGA);
      Serial.print("\nImage's quality changed to VGA");
    break;
  }
}

void capture(){
  Serial.print("\n\nCapturing...");
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
  Serial.print("\nSending image...");
  writeSerialBT(fb);
  esp_camera_fb_return(fb);
}

void writeSerialBT(camera_fb_t *fb){
  Serial.printf("\nStart sending %d bytes", fb->len);
  //fb->buf = &fb->buf[100000];
  SerialBT.write(fb->buf, fb->len);
  SerialBT.flush();
  Serial.print("\nSent\n");
}

void loop() {
 
  // 0) Setup ultrasonic sensor function
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; 

  // 1) Read external inputs and generate input symbols
  int inval = distance;
  if (inval > 40)
    inSymb = 0;
  else
    inSymb = 1;

  // 2) Future state estimation
  switch(iState){
    case 0:{
      if(inSymb == 1) //distance < 40cm
        futureState = 1;
      if(inSymb == 0) //distance > 40cm
        futureState = 0;
      break;
    }
    case 1:{
      if(inSymb == 1) //distance < 40cm
        futureState = 1;
      if(inSymb == 0) //distance > 40cm
        futureState = 0;
      break;
    }     
  }

  // 3) OnEntry and onExit actions
  if ((iState == 0) && (futureState == 1)){
    if (Serial.available()) { 
      capture();
      delay(3000);
    }
  }

  // 4) State transition [clock edge]
  iState = futureState;

  // 5) Output update
  //switch(iState){
  //    case 0: digitalWrite(outPin, HIGH); break;
  //    case 1: digitalWrite(outPin, LOW); break;
  //}
}
