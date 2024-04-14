import { View, Text, Pressable } from "react-native";

import Map from "../components/Map";

import Icon from "react-native-vector-icons/AntDesign";

export default function PlayScreen({ navigation }) {
  return (
    <View className="flex-1 bg-[#DEB887]">
      <Pressable
        className="absolute z-50 ml-6 mt-14"
        onPress={() => navigation.navigate("Landing")}
      >
        <Text className="text-xl font-semibold text-gray-900">
          <Icon name="back" size={24} color="#111827" />
          &nbsp;Go Back
        </Text>
      </Pressable>
      <Map />
    </View>
  );
}
