#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <WiFiManager.h>

const char* ssid = "naser";
const char* password = "M@7924226555";
const char* mqtt_server = "85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud";
const char* mqtt_username = "hqttt";
const char* mqtt_password = "Aa1AAAAA";
const int mqtt_port =8883;

bool isTouched = false;
int relayPin = D6;
int touchPin = D7;
bool lastTouchState = LOW;
String state;

WiFiClientSecure espClient;
WiFiManager wifiManager;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
String Message;


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";   // Create a random client ID
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("connected");

      client.subscribe("esp8266_data");   // subscribe the topics here

    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 2 seconds");   // Wait 5 seconds before retrying
      delay(2000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String incomingMessage = "";
  for (int i = 0; i < length; i++) {
    incomingMessage += (char)payload[i];
  }
  Message = incomingMessage;

  Serial.println("Message arrived [" + String(topic) + "]: " + incomingMessage);

}

void publishMessage(const char* topic, String payload , boolean retained){
  if (client.publish(topic, payload.c_str(), true))
      Serial.println("Message publised ["+String(topic)+"]: "+payload);
}

String readMACaddr() {
  int i;
  uint8_t macBin[6];
  String macStr;
  String byt;
  WiFi.macAddress(macBin);
  for (i = 0; i < 6; i++) {
    byt = String(macBin[i], HEX);
    macStr = byt.length() == 1 ? macStr + "0" + byt : macStr + byt;
  }
  return macStr;
}

bool getStateForMacAddr(const String& jsonStr, const String& macAddr) {
  // Parse the JSON string
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, jsonStr);

  // Get the JSON array
  JsonArray jsonArray = doc.as<JsonArray>();

  // Print the size of the array
  Serial.println("Array size: " + String(jsonArray.size()));

  // Iterate through the JSON array
  for (int i = 0; i < jsonArray.size(); i++) {
    // Access the current object in the array
    JsonObject obj = jsonArray[i];

    // Check if the "name" field matches the target MAC address
    String currentMac = obj["mac_addr"].as<String>();
    Serial.println("Checking MAC address in JSON: " + macAddr);

    if (currentMac == macAddr) {
      // Return the corresponding state
      Serial.print("MAC address found in the JSON: ");
      Serial.print(currentMac);
      Serial.print(" State: ");
      Serial.println(obj["state"].as<String>());
      return obj["state"].as<bool>();
    }
  }

  // Return false if the MAC address is not found in the JSON
  Serial.println("MAC address is not found in the JSON");
  return false;
}

String getValueFromJSON(String jsonString, String key) {
  // Parse the JSON string
  DynamicJsonDocument jsonBuffer(256); // Adjust the buffer size according to your JSON string size
  deserializeJson(jsonBuffer, jsonString);
  
  // Extract the value based on the key
  if (jsonBuffer.containsKey(key)) {
    if (jsonBuffer[key].is<bool>()) {
      // If the value is boolean, return it as a string
      return jsonBuffer[key].as<String>();
    } else {
      // If the value is not boolean, return it as usual
      return jsonBuffer[key];
    }
  } else {
    return ""; // Key not found
  }
}

String makeLowercase(String str) {
  String result = "";

  // Loop through each character in the string
  for (int i = 0; i < str.length(); i++) {
    // Convert each character to lowercase and append it to the result string
    result += tolower(str.charAt(i));
  }

  return result;
}

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  pinMode(touchPin, INPUT);
  wifiManager.autoConnect("switch", "password");
  while (!Serial) delay(1);
  espClient.setInsecure();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  int touchState = digitalRead(touchPin);

  if (!client.connected()) reconnect(); // check if client is connected
  client.loop();

  if (touchState == HIGH && lastTouchState == LOW) {
    isTouched = !isTouched;  // Toggle the touch state

    // Make a GET request to your localhost server
    String macAddr = readMACaddr();
    if(isTouched) {
      state = "True";
    } else {
      state = "False";
    }

    DynamicJsonDocument doc(1024);
    char mqtt_message[128];

    doc["mac_addr"] = readMACaddr();
    doc["state"] = state;


    serializeJson(doc, mqtt_message);

    publishMessage("esp8266_data", mqtt_message, true);
  }
  Message.toLowerCase();
  if(Message != "") {
    String parsed_mac_addr = getValueFromJSON(Message, "mac_addr");
    Serial.print(parsed_mac_addr + "==" + readMACaddr() + " ( " + Message + " ) ");
    if(parsed_mac_addr == readMACaddr()) {
      state = getValueFromJSON(Message, "state");
      Serial.println(state);
      if (state == "true") {
          isTouched = true;
      } else if (state == "false") {
          isTouched = false;
      }
    }
  }
  Message = "";
  digitalWrite(relayPin, isTouched);
  lastTouchState = touchState;
}