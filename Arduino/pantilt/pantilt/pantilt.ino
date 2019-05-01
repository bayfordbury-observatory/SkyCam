

    // defines pins numbers
    const int AzenPin = 4; 
    const int AzstepPin = 3; 
    const int AzdirPin = 2; 

    const uint32_t full = 32768;

    uint32_t distance=0;

    int32_t stepDelay=200;

    String inData;
    bool newMsg = false;

    const float degs = 0.01098632812;

    uint32_t position = 0;
    uint32_t target = 0;
     
    void setup() {
      // Sets the two pins as Outputs

      Serial.begin(9600);
      
      pinMode(AzenPin,OUTPUT); 
      pinMode(AzstepPin,OUTPUT); 
      pinMode(AzdirPin,OUTPUT);

       digitalWrite(AzenPin,HIGH);
       delay(500);
    }
    void loop() {

         while (Serial.available() > 0){
                
              char recieved = Serial.read();
              //Serial.print(recieved);
              // Process message when new line character is recieved
            if (recieved == '\n' && newMsg){
              String dataS(inData);
              target = dataS.toInt();
              Serial.print("position ");
              Serial.print(position);
              Serial.print(" target ");
              Serial.println(target);
              inData = ""; // Clear recieved buffer
              newMsg=false;

              if(target>=0 && target<32768){
                  if(target<position){
                      distance = position-target;                    
                  }else{
                      distance = target-position;                  
                  }
                  
                  if(distance>0){
                    Serial.print("moving ");
                    Serial.println(distance);

                    digitalWrite(AzenPin,LOW);
                    delay(10);

                    if(target<position){
                        digitalWrite(AzdirPin,HIGH);                      
                    }else{
                        digitalWrite(AzdirPin,LOW);                    
                    }
                    delay(10);

                    for(uint32_t x = 0; x < distance; x++) {

                        if(x<250){
                               stepDelay=((int32_t)x*-3.2)+1000 ;                          
                        }else if(x>(distance-250)){
                              int32_t fromEnd=(int32_t)distance-(int32_t)x;
                              stepDelay=(fromEnd*-3.2)+1000 ; 
                          
                        }else{
                              stepDelay=200;
                          
                        }
                      
                        digitalWrite(AzstepPin,HIGH);
                        delayMicroseconds(stepDelay);
                        digitalWrite(AzstepPin,LOW);
                        delayMicroseconds(stepDelay);
                    }

                    digitalWrite(AzenPin,HIGH);
                    
                    position = target;
                  }
              }
              
            }else if(recieved == '#'){
                newMsg=true;
          
            }else if(newMsg){
               inData += recieved; 
            }
              
        }  

      
    }
