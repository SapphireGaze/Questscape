import React, { useState } from "react";
import { Text, Image, View, Pressable, ImageBackground } from "react-native";

import JoinModal from "../components/JoinModal";

export default function LandingScreen({ navigation }) {
  const [modalVisible, setModalVisible] = useState(false);

  return (
    <View className="h-full w-full">
      <ImageBackground
        className="flex-1 items-center justify-center p-12"
        source={require("../assets/background.png")}
      >
        <JoinModal
          navigation={navigation}
          modalVisible={modalVisible}
          toggleModal={setModalVisible}
        />
        <Image
          source={require("../assets/logo.png")}
          style={{ width: 350, height: 75, marginBottom: 350 }}
        />
        <Pressable
          className="m-2 w-full rounded-3xl border-4 border-[#283D3B] bg-[#ECD7BC] p-2"
          onPress={() => navigation.navigate("Create")}
        >
          <Text className="text-center text-xl font-semibold text-[#283D3B]">
            Create a Quest
          </Text>
        </Pressable>
        <Pressable
          className="m-2 w-full rounded-3xl bg-[#283D3B] p-2"
          onPress={() => setModalVisible(true)}
        >
          <Text className="text-center text-xl font-semibold text-[#ECD7BC]">
            Join a Quest
          </Text>
        </Pressable>
      </ImageBackground>
    </View>
  );
}
