import React from "react";
import { Text, View, Pressable, Modal, TextInput } from "react-native";

import Icon from "react-native-vector-icons/AntDesign";

export default function JoinModal({ navigation, modalVisible, toggleModal }) {
  return (
    <Modal
      animationType="fade"
      transparent={false}
      visible={modalVisible}
      onRequestClose={() => {
        toggleModal(false);
      }}
    >
      <View className="flex-1 bg-[#DEB887] p-12">
        <Pressable className="-ml-4 mt-6" onPress={() => toggleModal(false)}>
          <Text className="text-xl font-semibold text-gray-900">
            <Icon name="back" size={24} color="#111827" />
            &nbsp;Go Back
          </Text>
        </Pressable>
        <View className="flex flex-col">
          <Text className="my-2 ml-2 mt-20 font-semibold">Quest ID</Text>
          <TextInput className="mb-2 w-full rounded-3xl bg-[#ECD7BC] p-4 shadow-2xl" />
        </View>
        <Pressable
          className="my-4 w-full rounded-3xl border-2 border-[#283D3B] bg-[#ECD7BC] p-2"
          onPress={() => {
            toggleModal(false);
            navigation.navigate("Play");
          }}
        >
          <Text className="text-center text-xl font-semibold text-[#4E7470]">
            Join!
          </Text>
        </Pressable>
      </View>
    </Modal>
  );
}
