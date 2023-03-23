//在這個檔案裡，只要在serial上print出來並以'\n'為結尾的東西都會被傳送到藍牙，不知道為什麼，反正就是這樣
//例如，執行Serial.print(F("We will get A+\n"))，python就會接收到"We will get A+"這個str。
//Serial.println無法取代\n，但是會讓結尾多一個\r。
//現在的BT.py會截斷結尾的\r
//每次上傳板子時，須將藍芽模組的藍色接線從主機板拔除，否則會無法上傳

//馬達（車輪）
int ENA = 9;
int ENB = 3;
int IN1 = 7;
int IN2 = 6;
int IN3 = 4;
int IN4 = 5;

//紅外線偵測、循跡變數
int SEN_L1 = A0;
int SEN_L2 = A1;
int SEN_M = A2;
int SEN_R2 = A3;
int SEN_R1 = A4;
int index = 0;
bool tracing_mode = true;

//藍牙
int Rx = 0;
int Tx = 1;

//RFID
int RST_PIN = 9;  
int SS_PIN = 10;

// 引入 SPI 程式庫 與 MFRC522 程式庫(RFID)
#include <SPI.h>
#include <MFRC522.h>


#include <SoftwareSerial.h>
MFRC522 *mfrc522;
SoftwareSerial BT(Rx,Tx);
char msg;

void setup() {
  // put your setup code here, to run once:

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(SEN_L1, INPUT);
  pinMode(SEN_L2, INPUT);
  pinMode(SEN_M, INPUT);
  pinMode(SEN_R2, INPUT);
  pinMode(SEN_R1, INPUT);
  Serial.begin(9600);
  SPI.begin();
  mfrc522 = new MFRC522(SS_PIN, RST_PIN); 
  mfrc522->PCD_Init();
  BT.begin(9600);
  // Serial.println(F("Car ready\n")); // 傳送訊息以表示初始化完成。但是突然發現每次初始化都是剛上傳好藍牙還沒接上的時候，所以好像沒有用，就註解掉了
}

void MotorWriting(double VR,double VL) {
  if( VL >= 0) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);  
  }else {
    VL = -VL;
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }if (VR >= 0) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  }else {
    VR = -VR;
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }
  analogWrite(ENA, VL);
  analogWrite(ENB, VR);
}
void Track() {
  //循跡模式內容
  if (digitalRead(SEN_M) == LOW){
    index=0;
  } 
  else {
    index=50;
  }
  
  //抵達node
  if (digitalRead(SEN_L1) == HIGH && digitalRead(SEN_L2) == HIGH && digitalRead(SEN_M) == HIGH && digitalRead(SEN_R2) == HIGH && digitalRead(SEN_R1) == HIGH ){
    MotorWriting(255,255);
    delay(200); 
    MotorWriting(0,0);
    tracing_mode = false; //跳出循跡模式
    Serial.println(F("done\n")); //「抵達node」的訊息: "done"

  }
  else if (digitalRead(SEN_R1) == LOW && digitalRead(SEN_L1) == LOW){    //黑:high 白:low
    //Serial.println("R1 = HIGH && L1 = HIGH");
    MotorWriting(150,150);
  }
  else if (digitalRead(SEN_R1) == HIGH && digitalRead(SEN_R2) == HIGH){
    //Serial.println("L1 = LOW && L2 = LOW");
    MotorWriting(50-index,200+index);
  }
  else if (digitalRead(SEN_R1) == HIGH){
    //Serial.println("L1 = LOW");
    MotorWriting(-200-index,200+index);
  }
  else if (digitalRead(SEN_L1) == HIGH && digitalRead(SEN_L2) == HIGH){
    //Serial.println("R1 = LOW && R2 = LOW");
    MotorWriting(200+index,50-index);
  }
  else if (digitalRead(SEN_L1) == HIGH){
    //Serial.println("R1 = LOW");
    MotorWriting(200+index,-200-index);
  }
 
        
}

void RFID() {
  //偵測UID並傳送至Python
  if(!mfrc522->PICC_IsNewCardPresent()) {
    return; //直接結束程式。我覺得沒必要用goto FuncEnd; by 廖
  }     //PICC_IsNewCardPresent()：是否感應到新的卡片?
  if(!mfrc522->PICC_ReadCardSerial()) {
    return;
  }      //PICC_ReadCardSerial()：是否成功讀取資料?
  Serial.print(F("RFID Detected: ")); //偵測到RFID的指令（的一半），還沒傳送出去
  
  /*讀出 UID 並回傳至Python*/
  byte *idPointer = mfrc522->uid.uidByte;   // 取得卡片的UID
  byte idSize = mfrc522->uid.size;   // 取得UID的長度
  for (int i=0; i<idSize; i++) {
    Serial.print(idPointer[i],HEX); // 以16進位制傳送
  }
  Serial.print('\n'); //發送。這裡發送出去的時候會多一個\n，老天鵝啊我不知道為什麼。總之不需要println了
  
  mfrc522->PICC_HaltA();                         // 讓卡片進入停止模式
  mfrc522->PCD_StopCrypto1();               // 停止 Crypto1
}

void loop() {
  RFID();
  // 若收到藍牙模組的資料，則執行指令內容
  // python執行迷宮路徑的計算並將指令傳送至車子
  // 指令列表：
  // 'F': (持續)前進，550毫秒後傳送"done"訊息
  // 'B': (持續)後退
  // 'V': 右迴轉
  // 'L': 左轉90度，完成後傳送"done"訊息
  // 'R': 右轉90度，完成後傳送"done"訊息
  // 'S': 停止
  // 'T': 回到循跡模式，直到抵達node或是接收到下一個指令
  if (BT.available()) {
    msg = BT.read();
    if (msg == 'F') {
      MotorWriting(150,150);
      delay(1200);
      Serial.println(F("done\n"));
    }
    if (msg == 'B') {
      MotorWriting(-150,-150);
    }
    if (msg == 'V') {
      MotorWriting(-255,255);
      delay(950);
      MotorWriting(0,0);
      Serial.println(F("done\n"));
    }
    if (msg == 'L') {
      MotorWriting(255,0);
      delay(700);
      MotorWriting(0,0);
      Serial.println(F("done\n"));
    }
    if (msg == 'R') {
      MotorWriting(0,255);
      delay(700);
      MotorWriting(0,0);
      Serial.println(F("done\n"));
    }
    if (msg == 'S') {
      MotorWriting(0,0);
    }
    if (msg == 'T') {
      tracing_mode = true;
        while (tracing_mode && !BT.available() ) {
          Track();
        
      }
    }
      
  }
}
    
